from __future__ import annotations

from datetime import datetime
from typing import Any

from psycopg.rows import dict_row

from app.core.config import settings

from .postgres_state_store import PostgresStateStore


query_store = PostgresStateStore()


def _normalize_pending_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized_row = dict(row)
    for field_name in (
        "first_choice_screening_submitted_at",
        "second_choice_screening_submitted_at",
    ):
        field_value = normalized_row.get(field_name)
        if isinstance(field_value, datetime):
            normalized_row[field_name] = field_value.isoformat()
    return normalized_row


def list_advisor_screening_pending_applications(
    *,
    keyword: str | None = None,
    advisor_username: str | None = None,
    advisor_name: str | None = None,
    advisor_user_id: int | None = None,
) -> list[dict[str, Any]]:
    """Query the pending advisor-screening application list without pagination."""
    normalized_advisor_name = str(advisor_name or "").strip()
    normalized_advisor_username = str(advisor_username or "").strip()
    advisor_id = advisor_user_id
    if advisor_id is None and normalized_advisor_username:
        advisor_id = query_store._advisor_user_id_by_username(normalized_advisor_username)
    if advisor_id is None and normalized_advisor_name:
        advisor_id = query_store._advisor_user_id_by_username(normalized_advisor_name)

    first_where = [
        "( first_choice = %s OR first_choice_id = %s )",
        "( first_choice_screening_submitted_at IS NULL )",
        "ra.application_status = 'initial_screening_first'",
    ]
    second_where = [
        "( second_choice = %s OR second_choice_id = %s )",
        "( second_choice_screening_submitted_at IS NULL AND first_choice_screening_submitted_at IS NOT NULL)",
        "ra.application_status = 'initial_screening_second'",
    ]
    first_params: list[Any] = []
    second_params: list[Any] = []

    if normalized_advisor_name and advisor_id is not None:
        first_params.extend([normalized_advisor_name, int(advisor_id)])
        second_params.extend([normalized_advisor_name, int(advisor_id)])
    elif normalized_advisor_name:
        first_params.extend([normalized_advisor_name, normalized_advisor_name])
        second_params.extend([normalized_advisor_name, normalized_advisor_name])
    elif advisor_id is not None:
        first_params.extend([int(advisor_id), int(advisor_id)])
        second_params.extend([int(advisor_id), int(advisor_id)])

    normalized_keyword = str(keyword or "").strip()
    if normalized_keyword:
        keyword_like = f"%{normalized_keyword}%"
        first_where.append("( stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s )")
        second_where.append("( stu.full_name ILIKE %s OR ra.candidate_no ILIKE %s )")
        first_params.extend([keyword_like, keyword_like])
        second_params.extend([keyword_like, keyword_like])

    params: list[Any] = [*first_params, *second_params]

    query_sql = f"""
      SELECT
        stu.id AS student_id,
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
        '第一志愿' AS choice_name
      FROM dtlms_portal_students AS stu
      LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
      WHERE {' AND '.join(first_where)}
      UNION ALL
      SELECT
        stu.id AS student_id,
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
        '第二志愿' AS choice_name
      FROM dtlms_portal_students AS stu
      LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id = ra.portal_student_id
      WHERE {' AND '.join(second_where)}
      ORDER BY application_id DESC
    """

    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            query_store._execute_dynamic(cur, query_sql, params)
            return [_normalize_pending_row(dict(row)) for row in cur.fetchall()]
