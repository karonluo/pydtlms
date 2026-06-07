"""Dashboard-oriented PostgreSQL query mixin.

This module contains dashboard statistics and drill-down query helpers.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)

class PostgresStateStoreQueryDashboardMixin:
    """Query mixin extracted by functional module."""

    def list_dashboard_undergraduate_school_rankings(self, limit: int = 20) -> list[dict[str, Any]]:
        """Execute query logic for `list_dashboard_undergraduate_school_rankings`."""
        self.ensure_schema()
        normalized_limit = max(int(limit), 1)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    )
                    SELECT school_name, COUNT(*)::int AS student_count
                    FROM latest_application
                    WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                    GROUP BY school_name
                    ORDER BY student_count DESC, school_name ASC
                    LIMIT %s
                    """,
                    (normalized_limit,),
                )
                return [
                    {
                        "school_name": str(row.get("school_name") or ""),
                        "student_count": int(row.get("student_count") or 0),
                    }
                    for row in cur.fetchall()
                ]

    def list_dashboard_undergraduate_school_group_distribution(self) -> dict[str, Any]:
        """Execute query logic for `list_dashboard_undergraduate_school_group_distribution`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH target_groups(dict_type, group_name, group_order) AS (
                        VALUES
                            ('system_c9_university', 'C9大学', 1),
                            ('system_211_university', '211大学', 2),
                            ('system_985_university', '985大学', 3)
                    ),
                    dictionary_schools AS (
                        SELECT
                            tg.dict_type,
                            tg.group_name,
                            tg.group_order,
                            NULLIF(BTRIM(d.label), '') AS school_name,
                            d.sort_order
                        FROM target_groups tg
                        JOIN dtlms_dict_types t
                          ON t.dict_type = tg.dict_type
                         AND t.is_deleted = FALSE
                         AND t.status = '启用'
                        JOIN dtlms_dict_data d
                          ON d.dict_type_id = t.id
                         AND d.dict_type = t.dict_type
                         AND d.is_deleted = FALSE
                         AND d.status = '启用'
                        WHERE NULLIF(BTRIM(d.label), '') IS NOT NULL
                    ),
                    latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    latest_application_total AS (
                        SELECT COUNT(*)::int AS total_applications
                        FROM latest_application
                        WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                    ),
                    school_counts AS (
                        SELECT school_name, COUNT(*)::int AS student_count
                        FROM latest_application
                        WHERE school_name IS NOT NULL AND BTRIM(school_name) <> ''
                        GROUP BY school_name
                    ),
                    grouped_counts AS (
                        SELECT
                            ds.dict_type,
                            ds.group_name,
                            ds.group_order,
                            ds.school_name,
                            ds.sort_order,
                            COALESCE(SUM(sc.student_count), 0)::int AS student_count
                        FROM dictionary_schools ds
                        LEFT JOIN school_counts sc ON sc.school_name LIKE ds.school_name || '%%'
                        GROUP BY ds.dict_type, ds.group_name, ds.group_order, ds.school_name, ds.sort_order
                    )
                    SELECT
                        gc.dict_type,
                        gc.group_name,
                        gc.school_name,
                        gc.student_count,
                        SUM(gc.student_count) OVER (PARTITION BY gc.dict_type)::int AS group_total,
                        lat.total_applications
                    FROM grouped_counts gc
                    CROSS JOIN latest_application_total lat
                    ORDER BY gc.group_order ASC, gc.student_count DESC, gc.sort_order ASC, gc.school_name ASC
                    """
                )
                group_order = [
                    ("system_c9_university", "C9大学"),
                    ("system_211_university", "211大学"),
                    ("system_985_university", "985大学"),
                ]
                groups: dict[str, dict[str, Any]] = {
                    dict_type: {"group_name": group_name, "dict_type": dict_type, "total": 0, "items": []}
                    for dict_type, group_name in group_order
                }
                total_applications = 0
                for row in cur.fetchall():
                    dict_type = str(row.get("dict_type") or "")
                    if dict_type not in groups:
                        continue
                    group_total = int(row.get("group_total") or 0)
                    student_count = int(row.get("student_count") or 0)
                    total_applications = int(row.get("total_applications") or total_applications or 0)
                    groups[dict_type]["total"] = group_total
                    groups[dict_type]["items"].append(
                        {
                            "school_name": str(row.get("school_name") or ""),
                            "student_count": student_count,
                            "percentage": round(student_count * 100 / group_total, 2) if group_total else 0.0,
                        }
                    )

                return {
                    "total_applications": total_applications,
                    "groups": [groups[dict_type] for dict_type, _group_name in group_order],
                }

    def list_dashboard_undergraduate_school_group_students(
        self,
        *,
        dict_type: str,
        school_name: str | None = None,
        bucket: str | None = None,
    ) -> list[dict[str, Any]]:
        """Execute query logic for `list_dashboard_undergraduate_school_group_students`."""
        self.ensure_schema()
        normalized_dict_type = str(dict_type or "").strip()
        normalized_school_name = str(school_name or "").strip()
        normalized_bucket = str(bucket or "").strip().lower()
        allowed_dict_types = {"system_c9_university", "system_211_university", "system_985_university"}
        if normalized_dict_type not in allowed_dict_types:
            return []

        if normalized_bucket == "other":
            selected_condition = "school_rank > %s"
            selected_params: list[Any] = [5]
        elif normalized_school_name:
            selected_condition = "school_name = %s"
            selected_params = [normalized_school_name]
        else:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    WITH dictionary_schools AS (
                        SELECT
                            NULLIF(BTRIM(d.label), '') AS school_name,
                            d.sort_order
                        FROM dtlms_dict_types t
                        JOIN dtlms_dict_data d
                          ON d.dict_type_id = t.id
                         AND d.dict_type = t.dict_type
                         AND d.is_deleted = FALSE
                         AND d.status = '启用'
                        WHERE t.dict_type = %s
                          AND t.is_deleted = FALSE
                          AND t.status = '启用'
                          AND NULLIF(BTRIM(d.label), '') IS NOT NULL
                    ),
                    latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    ),
                    school_counts AS (
                        SELECT
                            ds.school_name,
                            ds.sort_order,
                            COUNT(la.portal_student_id)::int AS student_count
                        FROM dictionary_schools ds
                        LEFT JOIN latest_application la ON la.school_name LIKE ds.school_name || '%%'
                        GROUP BY ds.school_name, ds.sort_order
                    ),
                    ranked_schools AS (
                        SELECT
                            school_name,
                            ROW_NUMBER() OVER (ORDER BY student_count DESC, sort_order ASC, school_name ASC)::int AS school_rank
                        FROM school_counts
                        WHERE student_count > 0
                    ),
                    selected_schools AS (
                        SELECT school_name
                        FROM ranked_schools
                        WHERE {selected_condition}
                    )
                    SELECT
                        la.recruitment_application_id,
                        la.student_name,
                        la.school_name,
                        la.candidate_no,
                        la.registered_at,
                        la.phone_number,
                        la.email
                    FROM latest_application la
                    JOIN selected_schools ss ON la.school_name LIKE ss.school_name || '%%'
                    ORDER BY la.registered_at DESC NULLS LAST, la.recruitment_application_id DESC
                    """,
                    [normalized_dict_type, *selected_params],
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                ]

    def list_dashboard_undergraduate_school_students(self, school_name: str) -> list[dict[str, Any]]:
        """Execute query logic for `list_dashboard_undergraduate_school_students`."""
        self.ensure_schema()
        normalized_school_name = str(school_name or "").strip()
        if not normalized_school_name:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT DISTINCT ON (ps.id)
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            COALESCE(
                                undergraduate_education.school_name,
                                NULLIF(BTRIM(ra.undergraduate_school), '')
                            ) AS school_name
                        FROM dtlms_portal_students ps
                        JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(ee.school_name), '') AS school_name
                            FROM dtlms_portal_application_education_experiences ee
                            WHERE ee.application_id = ra.id
                              AND ee.education_stage IN ('本科在读', '本科毕业')
                              AND NULLIF(BTRIM(ee.school_name), '') IS NOT NULL
                            ORDER BY ee.sort_order ASC, ee.id ASC
                            LIMIT 1
                        ) undergraduate_education ON TRUE
                        ORDER BY ps.id, COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    )
                    SELECT recruitment_application_id, student_name, school_name, candidate_no, registered_at, phone_number, email
                    FROM latest_application
                    WHERE school_name LIKE %s
                    ORDER BY registered_at DESC NULLS LAST, recruitment_application_id DESC
                    """,
                    (f"{normalized_school_name}%",),
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                ]
