from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List recruitment applications rejected twice in background assessment but still retaining advisor-screening residual fields.",
        epilog="Example: python backend/scripts/list_background_assessment_residuals.py --summary",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics in addition to the detailed rows.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="After revalidation, clear advisor_screening_status and advisor_screening_round for the matched rows.",
    )
    return parser


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _load_candidate_queue() -> list[dict[str, Any]]:
    sql = """
    WITH assessment_counts AS (
        SELECT
            application_id,
            COUNT(*) FILTER (WHERE assessment_result = '通过')::int AS pass_count,
            COUNT(*) FILTER (WHERE assessment_result = '不通过')::int AS reject_count
        FROM dtlms_background_assessments
        GROUP BY application_id
    )
    SELECT
        ra.id AS application_id,
        ra.portal_student_id,
        ra.business_key,
        ra.candidate_no,
        ra.student_name,
        ra.application_status,
        ra.advisor_screening_status,
        ra.advisor_screening_round,
        ra.first_choice_screening_score,
        ra.second_choice_screening_score,
        ra.first_choice_screening_batch_id,
        ra.second_choice_screening_batch_id,
        ra.first_choice_screening_submitted_at,
        ra.second_choice_screening_submitted_at,
        ra.updated_at,
        ra.initial_screening_status,
        ra.initial_screening_result,
        ac.pass_count,
        ac.reject_count
    FROM dtlms_recruitment_applications ra
    JOIN assessment_counts ac ON ac.application_id = ra.id
    WHERE ra.is_deleted = FALSE
      AND ac.reject_count >= 2
      AND (
            ra.advisor_screening_status IS NOT NULL
         OR ra.advisor_screening_round IS NOT NULL
         OR ra.first_choice_screening_score IS NOT NULL
         OR ra.second_choice_screening_score IS NOT NULL
         OR ra.first_choice_screening_batch_id IS NOT NULL
         OR ra.second_choice_screening_batch_id IS NOT NULL
         OR ra.first_choice_screening_submitted_at IS NOT NULL
         OR ra.second_choice_screening_submitted_at IS NOT NULL
      )
    ORDER BY ra.id ASC
    """
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = [dict(item) for item in cur.fetchall()]

    return rows


def _load_background_assessments(application_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
    if not application_ids:
        return {}

    assessments_sql = """
    SELECT
        application_id,
        evaluator_username,
        evaluator_name,
        evaluator_role_code,
        assessment_result,
        assessment_comment,
        assessed_at
    FROM dtlms_background_assessments
    WHERE application_id = ANY(%s)
    ORDER BY application_id ASC, assessed_at ASC, id ASC
    """
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(assessments_sql, (application_ids,))
            assessment_rows = [dict(item) for item in cur.fetchall()]

    assessments_by_application: dict[int, list[dict[str, Any]]] = {}
    for item in assessment_rows:
        application_id = int(item["application_id"])
        assessments_by_application.setdefault(application_id, []).append(
            {
                "evaluator_username": item.get("evaluator_username"),
                "evaluator_name": item.get("evaluator_name"),
                "evaluator_role_code": item.get("evaluator_role_code"),
                "assessment_result": item.get("assessment_result"),
                "assessment_comment": item.get("assessment_comment"),
                "assessed_at": item.get("assessed_at"),
            }
        )
    return assessments_by_application


def _is_residual_candidate(row: dict[str, Any]) -> bool:
    return (
        _normalize_text(row.get("advisor_screening_status")) is not None
        or _normalize_text(row.get("advisor_screening_round")) is not None
        or row.get("first_choice_screening_score") is not None
        or row.get("second_choice_screening_score") is not None
        or row.get("first_choice_screening_batch_id") is not None
        or row.get("second_choice_screening_batch_id") is not None
        or row.get("first_choice_screening_submitted_at") is not None
        or row.get("second_choice_screening_submitted_at") is not None
    )


def _verify_candidate_row(row: dict[str, Any], assessments_by_application: dict[int, list[dict[str, Any]]]) -> dict[str, Any] | None:
    """Re-read and re-check a coarse candidate before it is considered for cleanup."""
    application_id = int(row["application_id"])
    fresh_sql = """
    SELECT
        ra.id AS application_id,
        ra.portal_student_id,
        ra.business_key,
        ra.candidate_no,
        ra.student_name,
        ra.application_status,
        ra.advisor_screening_status,
        ra.advisor_screening_round,
        ra.first_choice_screening_score,
        ra.second_choice_screening_score,
        ra.first_choice_screening_batch_id,
        ra.second_choice_screening_batch_id,
        ra.first_choice_screening_submitted_at,
        ra.second_choice_screening_submitted_at,
        ra.updated_at,
        ra.initial_screening_status,
        ra.initial_screening_result,
        ac.pass_count,
        ac.reject_count
    FROM dtlms_recruitment_applications ra
    JOIN (
        SELECT
            application_id,
            COUNT(*) FILTER (WHERE assessment_result = '通过')::int AS pass_count,
            COUNT(*) FILTER (WHERE assessment_result = '不通过')::int AS reject_count
        FROM dtlms_background_assessments
        WHERE application_id = %s
        GROUP BY application_id
    ) ac ON ac.application_id = ra.id
    WHERE ra.id = %s
      AND ra.is_deleted = FALSE
    LIMIT 1
    """
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(fresh_sql, (application_id, application_id))
            fresh_row = cur.fetchone()

    if fresh_row is None:
        return None

    fresh_row = dict(fresh_row)
    if int(fresh_row.get("reject_count") or 0) < 2:
        return None
    if not _is_residual_candidate(fresh_row):
        return None

    fresh_row["background_assessments"] = assessments_by_application.get(application_id, [])
    fresh_row["residual_fields"] = {
        "advisor_screening_status": _normalize_text(fresh_row.get("advisor_screening_status")),
        "advisor_screening_round": _normalize_text(fresh_row.get("advisor_screening_round")),
        "first_choice_screening_score": fresh_row.get("first_choice_screening_score"),
        "second_choice_screening_score": fresh_row.get("second_choice_screening_score"),
        "first_choice_screening_batch_id": fresh_row.get("first_choice_screening_batch_id"),
        "second_choice_screening_batch_id": fresh_row.get("second_choice_screening_batch_id"),
        "first_choice_screening_submitted_at": fresh_row.get("first_choice_screening_submitted_at"),
        "second_choice_screening_submitted_at": fresh_row.get("second_choice_screening_submitted_at"),
    }
    return fresh_row


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counter = Counter()
    round_counter = Counter()
    score_counter = Counter()
    assessment_counter = Counter()

    for row in rows:
        status_counter[_normalize_text(row.get("advisor_screening_status")) or "<null>"] += 1
        round_counter[_normalize_text(row.get("advisor_screening_round")) or "<null>"] += 1
        score_counter["first_choice_score_non_null"] += int(row.get("first_choice_screening_score") is not None)
        score_counter["second_choice_score_non_null"] += int(row.get("second_choice_screening_score") is not None)
        for assessment in row.get("background_assessments") or []:
            key = f'{_normalize_text(assessment.get("evaluator_name")) or _normalize_text(assessment.get("evaluator_username")) or "<unknown>"} [{_normalize_text(assessment.get("evaluator_role_code")) or "<unknown>"}] => {_normalize_text(assessment.get("assessment_result")) or "<null>"}'
            assessment_counter[key] += 1

    likely_advisor_screening_count = sum(
        1
        for row in rows
        if _normalize_text(row.get("advisor_screening_status")) is not None
        or _normalize_text(row.get("advisor_screening_round")) is not None
        or row.get("first_choice_screening_score") is not None
        or row.get("second_choice_screening_score") is not None
    )

    return {
        "total_matched": len(rows),
        "likely_still_pointed_to_advisor_screening": likely_advisor_screening_count,
        "status_counter": dict(status_counter),
        "round_counter": dict(round_counter),
        "score_counter": dict(score_counter),
        "assessment_counter": dict(sorted(assessment_counter.items())),
    }


def _clear_residual_rows(rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0

    sql = """
    UPDATE dtlms_recruitment_applications
    SET advisor_screening_status = NULL,
        advisor_screening_round = NULL,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = %s
      AND is_deleted = FALSE
    """
    with psycopg.connect(_conninfo()) as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(sql, (int(row["application_id"]),))
        conn.commit()
    return len(rows)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        candidate_rows = _load_candidate_queue()
    except Exception as exc:
        print(f"[ERROR] Query failed: {exc}", file=sys.stderr)
        return 1

    assessments_by_application = _load_background_assessments([int(row["application_id"]) for row in candidate_rows])

    verified_rows: list[dict[str, Any]] = []
    dropped_rows: list[dict[str, Any]] = []
    for candidate_row in candidate_rows:
        verified_row = _verify_candidate_row(candidate_row, assessments_by_application)
        if verified_row is None:
            dropped_rows.append(candidate_row)
            continue
        verified_rows.append(verified_row)

    print(json.dumps(verified_rows, ensure_ascii=False, indent=2, default=str))
    print(f"[INFO] Candidate rows: {len(candidate_rows)}")
    print(f"[INFO] Verified rows: {len(verified_rows)}")
    print(f"[INFO] Dropped after revalidation: {len(dropped_rows)}")

    if args.summary:
        print(json.dumps(_summary(verified_rows), ensure_ascii=False, indent=2, default=str))

    if args.apply:
        try:
            cleared_count = _clear_residual_rows(verified_rows)
        except Exception as exc:
            print(f"[ERROR] Clear failed: {exc}", file=sys.stderr)
            return 1
        print(f"[INFO] Cleared rows: {cleared_count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())