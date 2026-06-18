from __future__ import annotations

from typing import Any

from psycopg.rows import dict_row

from app.core.config import settings
from app.schemas.recruitment import (
    InitialScreeningConfirmationApplicationListResponse,
    InitialScreeningConfirmationApplicationRecord,
)

from .postgres_state_store import PostgresStateStore


query_store = PostgresStateStore()


def list_advisor_screening_submitted_applications(
    *,
    keyword: str | None = None,
    advisor_name: str | None = None,
    advisor_user_id: int | None = None,
    page: int = 1,
    page_size: int = 10,
) -> InitialScreeningConfirmationApplicationListResponse:
    """Query the submitted advisor-screening application list."""
    offset = max(page - 1, 0) * page_size
    normalized_keyword = str(keyword or "").strip()
    normalized_advisor_name = str(advisor_name or "").strip()

    first_where = [
        "ra.first_choice_screening_submitted_at IS NOT NULL",
        "ra.application_status != 'initial_screening_first'",
    ]
    second_where = [
        "ra.second_choice_screening_submitted_at IS NOT NULL",
        "ra.application_status != 'initial_screening_first'",
        "ra.application_status != 'initial_screening_second'",
    ]

    if normalized_advisor_name and advisor_user_id is not None:
        first_where.append("(ra.first_choice = %s OR ra.first_choice_id = %s)")
        second_where.append("(ra.second_choice = %s OR ra.second_choice_id = %s)")
    elif normalized_advisor_name:
        first_where.append("ra.first_choice = %s")
        second_where.append("ra.second_choice = %s")
    elif advisor_user_id is not None:
        first_where.append("ra.first_choice_id = %s")
        second_where.append("ra.second_choice_id = %s")

    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        first_where.append("(stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s)")
        second_where.append("(stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s)")

    first_params: list[Any] = []
    second_params: list[Any] = []

    if normalized_advisor_name and advisor_user_id is not None:
        first_params.extend([normalized_advisor_name, int(advisor_user_id)])
        second_params.extend([normalized_advisor_name, int(advisor_user_id)])
    elif normalized_advisor_name:
        first_params.extend([normalized_advisor_name])
        second_params.extend([normalized_advisor_name])
    elif advisor_user_id is not None:
        first_params.extend([int(advisor_user_id)])
        second_params.extend([int(advisor_user_id)])

    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        first_params.extend([keyword_like, keyword_like])
        second_params.extend([keyword_like, keyword_like])

    params: list[Any] = [*first_params, *second_params]

    query_sql = f"""
      SELECT
        stu.id AS student_id,
                ra.plan_id,
        ra.application_status,
        ra.candidate_no,
        ra.business_key,
        stu.full_name,
        ra.id AS application_id,
        ra.first_choice_screening_submitted_at,
        ra.second_choice_screening_submitted_at,
        ra.first_choice,
        ra.first_choice_id,
        ra.first_choice_screening_score,
        ra.second_choice,
        ra.second_choice_id,
        ra.second_choice_screening_score,
        CASE WHEN ra.first_choice_screening_score < 80 THEN '未通过' ELSE '通过' END AS is_passed,
        '第一志愿' AS choice_name
      FROM dtlms_portal_students AS stu
      LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
      WHERE {' AND '.join(first_where)}
      UNION ALL
      SELECT
        stu.id AS student_id,
                ra.plan_id,
        ra.application_status,
        ra.candidate_no,
        ra.business_key,
        stu.full_name,
        ra.id AS application_id,
        ra.first_choice_screening_submitted_at,
        ra.second_choice_screening_submitted_at,
        ra.first_choice,
        ra.first_choice_id,
        ra.first_choice_screening_score,
        ra.second_choice,
        ra.second_choice_id,
        ra.second_choice_screening_score,
        CASE WHEN ra.second_choice_screening_score < 80 THEN '未通过' ELSE '通过' END AS is_passed,
        '第二志愿' AS choice_name
      FROM dtlms_portal_students AS stu
      LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
      WHERE {' AND '.join(second_where)}
      ORDER BY application_id DESC
      LIMIT %s OFFSET %s
    """

    count_sql = f"""
        SELECT COUNT(*) AS total
        FROM (
            SELECT ra.id AS application_id
            FROM dtlms_portal_students AS stu
            LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
            WHERE {' AND '.join(first_where)}
            UNION ALL
            SELECT ra.id AS application_id
            FROM dtlms_portal_students AS stu
            LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
            WHERE {' AND '.join(second_where)}
        ) t
    """

    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            query_store._execute_dynamic(cur, count_sql, params)
            total_row = cur.fetchone()
            total = int(total_row["total"] if total_row else 0)

            query_store._execute_dynamic(cur, query_sql, [*params, page_size, offset])
            rows = [dict(row) for row in cur.fetchall()]

    records = [InitialScreeningConfirmationApplicationRecord(**row) for row in rows]
    return InitialScreeningConfirmationApplicationListResponse(items=records, total=total, page=page, page_size=page_size)


def count_advisor_screening_submitted_applications(
    *,
    advisor_name: str | None = None,
    advisor_user_id: int | None = None,
    keyword: str | None = None,
) -> int:
    """Count submitted advisor-screening applications using the same filters as the list view."""
    return list_advisor_screening_submitted_applications(
        keyword=keyword,
        advisor_name=advisor_name,
        advisor_user_id=advisor_user_id,
        page=1,
        page_size=1,
    ).total
