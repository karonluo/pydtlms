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
        description="List registered recruitment applications with missing first_choice_id or second_choice_id and at least two background-assessment passes.",
        epilog="Example: python backend/scripts/list_recruitment_applications_missing_choice_ids.py --summary",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics in addition to the detailed rows.",
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


def _serialize_row(row: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in row.items():
        if hasattr(value, "isoformat"):
            try:
                output[key] = value.isoformat()
            except Exception:
                output[key] = str(value)
            continue
        output[key] = value
    return output


def _load_missing_choice_id_rows() -> list[dict[str, Any]]:
    sql = """
    WITH background_assessment_counts AS (
        SELECT
            application_id,
            COUNT(*) FILTER (WHERE assessment_result = '通过')::int AS pass_count,
            COUNT(*) FILTER (WHERE assessment_result = '不通过')::int AS reject_count
        FROM dtlms_background_assessments
        GROUP BY application_id
    )
    SELECT
        ra.id AS application_id,
        ra.business_key,
        ra.candidate_no,
        ra.student_name,
        ra.application_status,
        ra.plan_id,
        ps.full_name AS portal_full_name,
        ps.submitted_at AS portal_submitted_at,
        ra.intended_advisor_name,
        ra.intended_advisor_user_id,
        ra.first_choice,
        ra.second_choice,
        ra.first_choice_id,
        ra.second_choice_id,
        ra.first_choice_screening_submitted_at,
        ra.second_choice_screening_submitted_at,
        ra.first_choice_screening_batch_id,
        ra.second_choice_screening_batch_id,
        bac.pass_count,
        bac.reject_count,
        ra.updated_at
    FROM dtlms_recruitment_applications ra
        JOIN background_assessment_counts bac ON bac.application_id = ra.id
    LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
    WHERE ra.is_deleted = FALSE
      AND ps.submitted_at IS NOT NULL
          AND bac.pass_count >= 2
      AND (
            ra.first_choice_id IS NULL
         OR ra.second_choice_id IS NULL
      )
    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
    """
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql)
            return [dict(item) for item in cur.fetchall()]


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counter = Counter()
    for row in rows:
        if row.get("first_choice_id") is None and row.get("second_choice_id") is None:
            counter["both_missing"] += 1
        elif row.get("first_choice_id") is None:
            counter["first_choice_missing"] += 1
        elif row.get("second_choice_id") is None:
            counter["second_choice_missing"] += 1
    return {
        "total": len(rows),
        "breakdown": dict(counter),
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        rows = _load_missing_choice_id_rows()
    except Exception as exc:
        print(f"[ERROR] Query failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps([_serialize_row(row) for row in rows], ensure_ascii=False, indent=2, default=str))
    print(f"[INFO] Matched rows: {len(rows)}")

    if args.summary:
        print(json.dumps(_summary(rows), ensure_ascii=False, indent=2, default=str))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())