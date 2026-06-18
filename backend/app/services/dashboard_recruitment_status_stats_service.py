from __future__ import annotations

from typing import Any

from psycopg.rows import dict_row

from app.core.config import settings

from .postgres_state_store import PostgresStateStore


query_store = PostgresStateStore()


def get_recruitment_application_status_stats() -> list[dict[str, Any]]:
    """Return recruitment application status counts for the dashboard."""
    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                select 
                CASE 
                 WHEN application_status = 'terminated' THEN '报名已经终止'
                 WHEN application_status = 'submitted' THEN '报名已提交未审核'
                 WHEN application_status = 'returned' THEN '驳回重填'
                 WHEN application_status = 'background_review' THEN '等待背景评估'
                 WHEN application_status = 'initial_screening_first' THEN '等待第一志愿导师评分'
                 WHEN application_status = 'initial_screening_second' THEN '等待第二志愿导师评分'
                 WHEN application_status = 'initial_screening_confirmation' THEN '等待初筛确认'
                END AS application_status_state
                ,count(application_status) as count
                from dtlms_recruitment_applications
                group by application_status
                """
            )
            return [
                {
                    'application_status_state': str(row.get('application_status_state') or ''),
                    'count': int(row.get('count') or 0),
                }
                for row in cur.fetchall()
            ]


def get_first_choice_pending_grading_statistics(*, page: int = 1, page_size: int = 10, advisor_name: str | None = None) -> dict[str, Any]:
    """Return first-choice advisor pending-grading counts with fake pagination."""
    safe_page = max(int(page or 1), 1)
    safe_page_size = max(int(page_size or 10), 1)
    offset = (safe_page - 1) * safe_page_size
    advisor_name_keyword = str(advisor_name or '').strip()
    where_clauses = [
        "application_status = 'initial_screening_first'",
        "candidate_no is not null",
        "candidate_no <> ''",
        "first_choice_screening_submitted_at is null",
    ]
    params: list[Any] = []
    if advisor_name_keyword:
        where_clauses.append("first_choice ILIKE %s")
        params.append(f"%{advisor_name_keyword}%")
    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select count(*) as total
                from (
                    select first_choice
                    from dtlms_recruitment_applications
                    where {' and '.join(where_clauses)}
                    group by first_choice
                ) t
                """,
                tuple(params),
            )
            total = int(cur.fetchone().get('total') or 0)
            cur.execute(
                f"""
                select
                    first_choice as advisor_name,
                    count(first_choice) as student_count
                from dtlms_recruitment_applications
                where {' and '.join(where_clauses)}
                group by first_choice
                order by student_count desc, first_choice asc
                limit %s offset %s
                """,
                (*params, safe_page_size, offset),
            )
            items = [
                {
                    'advisor_name': str(row.get('advisor_name') or ''),
                    'student_count': int(row.get('student_count') or 0),
                }
                for row in cur.fetchall()
            ]
            return {
                'total': total,
                'page': safe_page,
                'page_size': safe_page_size,
                'items': items,
            }


def get_second_choice_pending_grading_statistics(*, page: int = 1, page_size: int = 10, advisor_name: str | None = None) -> dict[str, Any]:
    """Return second-choice advisor pending-grading counts with fake pagination."""
    safe_page = max(int(page or 1), 1)
    safe_page_size = max(int(page_size or 10), 1)
    offset = (safe_page - 1) * safe_page_size
    advisor_name_keyword = str(advisor_name or '').strip()
    where_clauses = [
        "application_status = 'initial_screening_second'",
        "candidate_no is not null",
        "candidate_no <> ''",
        "first_choice_screening_submitted_at is not null",
        "second_choice_screening_submitted_at is null",
    ]
    params: list[Any] = []
    if advisor_name_keyword:
        where_clauses.append("second_choice ILIKE %s")
        params.append(f"%{advisor_name_keyword}%")
    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select count(*) as total
                from (
                    select second_choice
                    from dtlms_recruitment_applications
                    where {' and '.join(where_clauses)}
                    group by second_choice
                ) t
                """,
                tuple(params),
            )
            total = int(cur.fetchone().get('total') or 0)
            cur.execute(
                f"""
                select
                    second_choice as advisor_name,
                    count(second_choice) as student_count
                from dtlms_recruitment_applications
                where {' and '.join(where_clauses)}
                group by second_choice
                order by student_count desc, second_choice asc
                limit %s offset %s
                """,
                (*params, safe_page_size, offset),
            )
            items = [
                {
                    'advisor_name': str(row.get('advisor_name') or ''),
                    'student_count': int(row.get('student_count') or 0),
                }
                for row in cur.fetchall()
            ]
            return {
                'total': total,
                'page': safe_page,
                'page_size': safe_page_size,
                'items': items,
            }


def get_first_choice_pending_student_list(
    *,
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    advisor_id: str | None = None,
    keyword: str | None = None,
) -> dict[str, Any]:
    """Return first-choice pending grading students with fake pagination."""
    safe_page = max(int(page or 1), 1)
    safe_page_size = max(int(page_size or 10), 1)
    offset = (safe_page - 1) * safe_page_size
    advisor_name_keyword = str(advisor_name or '').strip()
    advisor_id_keyword = str(advisor_id or '').strip()
    keyword_text = str(keyword or '').strip()
    where_clauses = [
        "ra.first_choice_screening_submitted_at IS NULL",
        "ra.application_status = 'initial_screening_first'",
        "ra.candidate_no IS NOT NULL",
        "ra.candidate_no <> ''",
    ]
    params: list[Any] = []
    if advisor_name_keyword or advisor_id_keyword:
        where_clauses.append("(ra.first_choice = %s OR ra.first_choice_id = %s)")
        params.extend([advisor_name_keyword or None, advisor_id_keyword or None])
    if keyword_text:
        where_clauses.append("(ra.candidate_no ILIKE %s OR stu.full_name ILIKE %s)")
        params.extend([f"%{keyword_text}%", f"%{keyword_text}%"])
    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select count(*) as total
                from (
                    select stu.id
                    from dtlms_portal_students stu
                    left join dtlms_recruitment_applications ra on stu.id = ra.portal_student_id
                    where {' and '.join(where_clauses)}
                    group by stu.id
                ) t
                """,
                tuple(params),
            )
            total = int(cur.fetchone().get('total') or 0)
            cur.execute(
                f"""
                select
                    ra.id as application_id,
                    ra.candidate_no,
                    stu.full_name as student_name
                from dtlms_portal_students stu
                left join dtlms_recruitment_applications ra on stu.id = ra.portal_student_id
                where {' and '.join(where_clauses)}
                group by ra.id, ra.candidate_no, stu.full_name
                order by stu.full_name asc, ra.candidate_no asc
                limit %s offset %s
                """,
                (*params, safe_page_size, offset),
            )
            items = [
                {
                    'application_id': int(row.get('application_id') or 0),
                    'candidate_no': str(row.get('candidate_no') or ''),
                    'student_name': str(row.get('student_name') or ''),
                }
                for row in cur.fetchall()
            ]
            return {
                'total': total,
                'page': safe_page,
                'page_size': safe_page_size,
                'items': items,
            }


def get_second_choice_pending_student_list(
    *,
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    advisor_id: str | None = None,
    keyword: str | None = None,
) -> dict[str, Any]:
    """Return second-choice pending grading students with fake pagination."""
    safe_page = max(int(page or 1), 1)
    safe_page_size = max(int(page_size or 10), 1)
    offset = (safe_page - 1) * safe_page_size
    advisor_name_keyword = str(advisor_name or '').strip()
    advisor_id_keyword = str(advisor_id or '').strip()
    keyword_text = str(keyword or '').strip()
    where_clauses = [
        "ra.first_choice_screening_submitted_at IS NOT NULL",
        "ra.second_choice_screening_submitted_at IS NULL",
        "ra.application_status = 'initial_screening_second'",
        "ra.candidate_no IS NOT NULL",
        "ra.candidate_no <> ''",
    ]
    params: list[Any] = []
    if advisor_name_keyword or advisor_id_keyword:
        where_clauses.append("(ra.second_choice = %s OR ra.second_choice_id = %s)")
        params.extend([advisor_name_keyword or None, advisor_id_keyword or None])
    if keyword_text:
        where_clauses.append("(ra.candidate_no ILIKE %s OR stu.full_name ILIKE %s)")
        params.extend([f"%{keyword_text}%", f"%{keyword_text}%"])
    with query_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select count(*) as total
                from (
                    select stu.id
                    from dtlms_portal_students stu
                    left join dtlms_recruitment_applications ra on stu.id = ra.portal_student_id
                    where {' and '.join(where_clauses)}
                    group by stu.id
                ) t
                """,
                tuple(params),
            )
            total = int(cur.fetchone().get('total') or 0)
            cur.execute(
                f"""
                select
                    ra.id as application_id,
                    ra.candidate_no,
                    stu.full_name as student_name
                from dtlms_portal_students stu
                left join dtlms_recruitment_applications ra on stu.id = ra.portal_student_id
                where {' and '.join(where_clauses)}
                group by ra.id, ra.candidate_no, stu.full_name
                order by stu.full_name asc, ra.candidate_no asc
                limit %s offset %s
                """,
                (*params, safe_page_size, offset),
            )
            items = [
                {
                    'application_id': int(row.get('application_id') or 0),
                    'candidate_no': str(row.get('candidate_no') or ''),
                    'student_name': str(row.get('student_name') or ''),
                }
                for row in cur.fetchall()
            ]
            return {
                'total': total,
                'page': safe_page,
                'page_size': safe_page_size,
                'items': items,
            }
