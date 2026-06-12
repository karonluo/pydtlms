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
    where_clauses = [
        "app.is_deleted = FALSE",
        "(app.first_choice_screening_submitted_at IS NOT NULL OR app.second_choice_screening_submitted_at IS NOT NULL)",
    ]
    params: list[Any] = []

    normalized_keyword = str(keyword or "").strip()
    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        where_clauses.append("(stu.full_name ILIKE %s OR app.candidate_no ILIKE %s)")
        params.extend([keyword_like, keyword_like])

    normalized_advisor_name = str(advisor_name or "").strip()
    if normalized_advisor_name and advisor_user_id is not None:
        where_clauses.append(
            "(TRIM(app.first_choice) = %s OR TRIM(app.second_choice) = %s OR app.first_choice_id = %s OR app.second_choice_id = %s)"
        )
        params.extend([normalized_advisor_name, normalized_advisor_name, int(advisor_user_id), int(advisor_user_id)])
    elif normalized_advisor_name:
        where_clauses.append("(TRIM(app.first_choice) = %s OR TRIM(app.second_choice) = %s)")
        params.extend([normalized_advisor_name, normalized_advisor_name])
    elif advisor_user_id is not None:
        where_clauses.append("(app.first_choice_id = %s OR app.second_choice_id = %s)")
        params.extend([int(advisor_user_id), int(advisor_user_id)])

    where_sql = " AND ".join(where_clauses)

    query_sql = f"""
      SELECT
        stu.id AS student_id,
        app.plan_id,
        app.candidate_no,
        app.business_key,
        stu.full_name,
        app.id AS application_id,
        app.first_choice_screening_submitted_at,
        app.second_choice_screening_submitted_at,
        app.first_choice,
        app.first_choice_id,
        app.second_choice,
        app.second_choice_id,
        CASE
          WHEN app.first_choice_screening_score IS NOT NULL THEN app.first_choice_screening_score
          WHEN app.second_choice_screening_score IS NOT NULL THEN app.second_choice_screening_score
        END AS choice_score,
        CASE
          WHEN app.first_choice_screening_submitted_at IS NOT NULL THEN '第一志愿'
          WHEN app.second_choice_screening_submitted_at IS NOT NULL THEN '第二志愿'
        END AS choice_name,
        app.application_status,
        app.intended_advisor_name
      FROM dtlms_portal_students AS stu
      LEFT JOIN dtlms_recruitment_applications AS app
        ON app.portal_student_id = stu.id
      WHERE {where_sql}
      ORDER BY app.id DESC
      LIMIT %s OFFSET %s
    """

    count_sql = f"""
        SELECT COUNT(*) AS total
        FROM dtlms_portal_students AS stu
        LEFT JOIN dtlms_recruitment_applications AS app
          ON app.portal_student_id = stu.id
        WHERE {where_sql}
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
