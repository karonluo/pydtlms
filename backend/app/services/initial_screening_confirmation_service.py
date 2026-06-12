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


def list_initial_screening_confirmation_applications(
    *,
    plan_id: int,
    keyword: str | None = None,
    advisor_names: list[str] | None = None,
    page: int = 1,
    page_size: int = 10,
) -> InitialScreeningConfirmationApplicationListResponse:
    """Query the initial-screening-confirmation application list."""
    offset = max(page - 1, 0) * page_size
    where_clauses = [
        "app.application_status = 'initial_screening_confirmation'",
        "app.plan_id = %s",
        "app.is_deleted = FALSE",
        "(app.first_choice_screening_score >= 80 OR app.second_choice_screening_score >= 80)",
        "(app.first_choice_screening_submitted_at IS NOT NULL OR app.second_choice_screening_submitted_at IS NOT NULL)",
    ]
    params: list[Any] = [int(plan_id)]

    normalized_keyword = str(keyword or "").strip()
    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        where_clauses.append("(stu.full_name ILIKE %s OR app.candidate_no ILIKE %s)")
        params.extend([keyword_like, keyword_like])

    normalized_advisor_names: list[str] = []
    seen_advisor_names: set[str] = set()
    for item in advisor_names or []:
        normalized_item = str(item or "").strip()
        if not normalized_item or normalized_item in seen_advisor_names:
            continue
        seen_advisor_names.add(normalized_item)
        normalized_advisor_names.append(normalized_item)
    if normalized_advisor_names:
        advisor_match_clauses: list[str] = []
        for advisor_name in normalized_advisor_names:
            advisor_match_clauses.append("(TRIM(app.first_choice) = %s OR TRIM(app.second_choice) = %s)")
            params.extend([advisor_name, advisor_name])
        where_clauses.append("(" + " OR ".join(advisor_match_clauses) + ")")

    where_sql = " AND ".join(where_clauses)

    query_sql = f"""
      SELECT
        app.id AS application_id,
        stu.id AS student_id,
        app.plan_id,
        app.candidate_no,
        stu.full_name,
        app.first_choice,
        app.first_choice_screening_score,
        app.second_choice,
        app.second_choice_screening_score,
        app.first_choice_screening_submitted_at,
        app.second_choice_screening_submitted_at,
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
