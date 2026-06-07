"""Training and degree PostgreSQL query mixin.

This module contains training plans, scientific reports, outbound study, and thesis queries.
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

class PostgresStateStoreQueryTrainingDegreeMixin:
    """Query mixin extracted by functional module."""

    def list_training_plans_page(
        self,
        keyword: str | None = None,
        plan_status: str | None = None,
        advisor_name: str | None = None,
        report_cycle: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_training_plans_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["tp.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(tp.scientific_goal, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if plan_status:
            where_clauses.append("tp.plan_status = %s")
            params.append(self._map_training_plan_status(plan_status))
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if report_cycle:
            where_clauses.append("COALESCE(tp.report_cycle, '') = %s")
            params.append(report_cycle)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_training_plans tp
                    JOIN dtlms_students s ON s.id = tp.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = tp.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        tp.id,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        tp.version_no,
                        tp.report_cycle,
                        tp.plan_status,
                        tp.scientific_goal,
                        tp.assessment_rule
                    FROM dtlms_training_plans tp
                    JOIN dtlms_students s ON s.id = tp.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = tp.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY tp.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_training_plan_row(dict(row)) for row in cur.fetchall()], total

    def list_scientific_reports_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        reviewer_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_scientific_reports_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["sr.is_deleted = FALSE"]
        params: list[Any] = []

        if status:
            where_clauses.append("sr.report_status = %s")
            params.append(self._map_report_status(status))
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(sr.business_key, ''),
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(sr.period_label, ''),
                    COALESCE(sr.summary, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if reviewer_name:
            where_clauses.append("COALESCE(reviewer.full_name, '') = %s")
            params.append(reviewer_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_scientific_reports sr
                    JOIN dtlms_students s ON s.id = sr.student_id AND s.is_deleted = FALSE
                    LEFT JOIN dtlms_advisors reviewer ON reviewer.id = sr.reviewer_advisor_id AND reviewer.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        sr.id,
                        sr.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        sr.period_label,
                        sr.report_status,
                        reviewer.full_name AS reviewer_name,
                        sr.review_score,
                        sr.summary
                    FROM dtlms_scientific_reports sr
                    JOIN dtlms_students s ON s.id = sr.student_id AND s.is_deleted = FALSE
                    LEFT JOIN dtlms_advisors reviewer ON reviewer.id = sr.reviewer_advisor_id AND reviewer.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY sr.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_scientific_report_row(dict(row)) for row in cur.fetchall()], total

    def list_outbound_studies_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        study_type: str | None = None,
        advisor_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_outbound_studies_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["os.is_deleted = FALSE"]
        params: list[Any] = []

        if status:
            where_clauses.append("os.approval_status = %s")
            params.append(self._map_outbound_status(status))
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                CONCAT_WS(
                    ' ',
                    COALESCE(os.business_key, ''),
                    COALESCE(s.student_no, ''),
                    COALESCE(s.full_name, ''),
                    COALESCE(os.destination, ''),
                    COALESCE(os.expected_outcome, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")
        if study_type:
            where_clauses.append("COALESCE(os.study_type, '') = %s")
            params.append(study_type)
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_outbound_studies os
                    JOIN dtlms_students s ON s.id = os.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = os.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        os.id,
                        os.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        os.study_type,
                        os.destination,
                        os.start_date,
                        os.end_date,
                        os.approval_status,
                        os.expected_outcome
                    FROM dtlms_outbound_studies os
                    JOIN dtlms_students s ON s.id = os.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = os.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY os.start_date DESC, os.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_outbound_study_row(dict(row)) for row in cur.fetchall()], total

    def list_theses_page(
        self,
        keyword: str | None = None,
        degree_status: str | None = None,
        advisor_name: str | None = None,
        thesis_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_theses_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        if degree_status:
            where_clauses.append(
                """
                CASE
                    WHEN t.degree_granted = 'reviewing' THEN '授位审批中'
                    WHEN t.degree_granted = 'granted' THEN '已授位'
                    WHEN t.defense_date IS NOT NULL THEN '待正式答辩'
                    ELSE '待申请'
                END = %s
                """
            )
            params.append(degree_status)
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if thesis_status:
            where_clauses.append(
                """
                CASE
                    WHEN t.thesis_status = 'plagiarism_passed' THEN '查重通过'
                    WHEN t.thesis_status = 'review_passed' THEN '盲审通过'
                    WHEN t.thesis_status = 'rework' THEN '退回修改'
                    ELSE '待查重'
                END = %s
                """
            )
            params.append(thesis_status)
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.business_key ILIKE %s
                    OR s.student_no ILIKE %s
                    OR s.full_name ILIKE %s
                    OR t.title ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like, keyword_like])

        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_theses t
                    JOIN dtlms_students s ON s.id = t.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = t.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        t.id,
                        t.business_key,
                        s.student_no,
                        s.full_name AS student_name,
                        a.full_name AS advisor_name,
                        t.title,
                        t.plagiarism_rate,
                        t.thesis_status,
                        t.blind_review_status,
                        t.defense_date,
                        t.degree_granted
                    FROM dtlms_theses t
                    JOIN dtlms_students s ON s.id = t.student_id AND s.is_deleted = FALSE
                    JOIN dtlms_advisors a ON a.id = t.advisor_id AND a.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_thesis_row(dict(row)) for row in cur.fetchall()], total

    def list_thesis_reviews_page(
        self,
        thesis_id: int | None = None,
        keyword: str | None = None,
        expert_name: str | None = None,
        review_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_thesis_reviews_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []
        if thesis_id is not None:
            where_clauses.append("tr.thesis_id = %s")
            params.append(int(thesis_id))
        if expert_name:
            where_clauses.append("tr.expert_name = %s")
            params.append(expert_name)
        if review_status:
            where_clauses.append(
                """
                CASE
                    WHEN tr.review_status = 'approved' THEN '通过'
                    WHEN tr.review_status = 'rejected' THEN '不通过'
                    ELSE '待审阅'
                END = %s
                """
            )
            params.append(review_status)
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.title ILIKE %s
                    OR tr.expert_name ILIKE %s
                    OR COALESCE(tr.review_comment, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])

        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_thesis_reviews tr
                    JOIN dtlms_theses t ON t.id = tr.thesis_id AND t.is_deleted = FALSE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        tr.id,
                        tr.thesis_id,
                        t.title AS thesis_title,
                        tr.expert_name,
                        tr.review_score,
                        tr.review_status,
                        tr.review_comment
                    FROM dtlms_thesis_reviews tr
                    JOIN dtlms_theses t ON t.id = tr.thesis_id AND t.is_deleted = FALSE
                    WHERE {where_sql}
                    ORDER BY tr.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_thesis_review_row(dict(row)) for row in cur.fetchall()], total
