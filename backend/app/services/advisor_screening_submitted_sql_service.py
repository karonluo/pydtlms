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
    """Query the advisor-screening submitted list with pagination."""
    normalized_advisor_name = str(advisor_name or "").strip()
    normalized_keyword = str(keyword or "").strip()
    offset = max(page - 1, 0) * page_size

    first_where = [
        "( first_choice = %s OR first_choice_id = %s )",
        "( first_choice_screening_submitted_at IS NOT NULL )",
        "ra.application_status != 'initial_screening_first'",
    ]
    second_where = [
        "( second_choice = %s OR second_choice_id = %s )",
        "( second_choice_screening_submitted_at IS NOT NULL )",
        "ra.application_status != 'initial_screening_first'",
        "ra.application_status != 'initial_screening_second'",
    ]

    first_params: list[Any] = []
    second_params: list[Any] = []

    if normalized_advisor_name:
      first_params.append(normalized_advisor_name)
      second_params.append(normalized_advisor_name)
    if advisor_user_id is not None:
      first_params.append(int(advisor_user_id))
      second_params.append(int(advisor_user_id))

    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        first_where.append("( stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s )")
        second_where.append("( stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s )")
        first_params.extend([keyword_like, keyword_like])
        second_params.extend([keyword_like, keyword_like])

    where_first_sql = " AND ".join(first_where)
    where_second_sql = " AND ".join(second_where)

    query_sql = f"""
      WITH submitted_rows AS (
        SELECT
          stu.id AS student_id,
          ra.plan_id,
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
          ra.application_status,
          CASE WHEN ra.first_choice_screening_score < 80 THEN '未通过' ELSE '通过' END AS is_passed,
          '第一志愿' AS choice_name
        FROM dtlms_portal_students AS stu
        LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
        WHERE {where_first_sql}
        UNION ALL
        SELECT
          stu.id AS student_id,
          ra.plan_id,
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
          ra.application_status,
          CASE WHEN ra.second_choice_screening_score < 80 THEN '未通过' ELSE '通过' END AS is_passed,
          '第二志愿' AS choice_name
        FROM dtlms_portal_students AS stu
        LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
        WHERE {where_second_sql}
      )
      SELECT *
      FROM submitted_rows
      ORDER BY application_id DESC
      LIMIT %s OFFSET %s
    """

    count_sql = f"""
      WITH submitted_rows AS (
        SELECT
          stu.id AS student_id,
          ra.id AS application_id
        FROM dtlms_portal_students AS stu
        LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
        WHERE {where_first_sql}
        UNION ALL
        SELECT
          stu.id AS student_id,
          ra.id AS application_id
        FROM dtlms_portal_students AS stu
        LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
        WHERE {where_second_sql}
      )
      SELECT COUNT(*) AS total
      FROM submitted_rows
    """

    params: list[Any] = [*first_params, *second_params]

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