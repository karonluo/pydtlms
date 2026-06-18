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
        description="List or backfill portal students whose latest recruitment application is missing first_choice or second_choice, using draft values when available.",
        epilog=(
            "Examples: "
            "python backend/scripts/list_students_missing_first_choice_but_draft_has_first_choice.py --summary; "
            "python backend/scripts/list_students_missing_first_choice_but_draft_has_first_choice.py --dry-run; "
            "python backend/scripts/list_students_missing_first_choice_but_draft_has_first_choice.py --apply"
        ),
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics in addition to the detailed rows.",
    )
    parser.add_argument(
        "--candidate-no",
        type=str,
        default=None,
        help="Filter by a specific candidate number.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the backfill without writing to the database.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the eligible draft values back to dtlms_recruitment_applications.",
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


def _normalize_candidate_no(value: Any) -> str | None:
    return _normalize_text(value)


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


def _load_rows(candidate_no: str | None = None) -> list[dict[str, Any]]:
    sql = """
    WITH latest_applications AS (
        SELECT DISTINCT ON (ra.portal_student_id)
            ra.id,
            ra.portal_student_id,
            ra.plan_id,
            ra.business_key,
            ra.candidate_no,
            ra.student_name,
            ra.first_choice,
            ra.first_choice_id,
            ra.second_choice,
            ra.second_choice_id,
            ra.application_status,
            ra.applied_at,
            ra.created_at,
            ra.updated_at
        FROM dtlms_recruitment_applications ra
        WHERE ra.is_deleted = FALSE
          AND ra.portal_student_id IS NOT NULL
        ORDER BY ra.portal_student_id,
                 COALESCE(ra.applied_at, ra.created_at) DESC,
                 ra.id DESC
    )
    SELECT
        ps.id AS portal_student_id,
        ps.full_name AS portal_full_name,
        ps.phone_number,
        ps.email,
        ps.id_number,
        la.id AS application_id,
        la.plan_id,
        la.business_key,
        la.candidate_no,
        la.student_name,
        la.application_status,
        la.first_choice,
        la.first_choice_id,
        la.second_choice,
        la.second_choice_id,
        la.applied_at,
        la.created_at AS application_created_at,
        la.updated_at AS application_updated_at,
                COALESCE(NULLIF(ps.application_draft::jsonb ->> 'first_choice', ''), NULLIF(ps.application_draft::jsonb #>> '{preferences,0,advisor_name}', '')) AS draft_first_choice,
                COALESCE(NULLIF(ps.application_draft::jsonb ->> 'first_choice_id', ''), NULLIF(ps.application_draft::jsonb #>> '{preferences,0,advisor_user_id}', '')) AS draft_first_choice_id,
                COALESCE(NULLIF(ps.application_draft::jsonb ->> 'second_choice', ''), NULLIF(ps.application_draft::jsonb #>> '{preferences,1,advisor_name}', '')) AS draft_second_choice,
                COALESCE(NULLIF(ps.application_draft::jsonb ->> 'second_choice_id', ''), NULLIF(ps.application_draft::jsonb #>> '{preferences,1,advisor_user_id}', '')) AS draft_second_choice_id,
        ps.application_draft
    FROM dtlms_portal_students ps
    JOIN latest_applications la ON la.portal_student_id = ps.id
        WHERE NULLIF(la.candidate_no, '') IS NOT NULL
            AND (
                        COALESCE(NULLIF(la.first_choice, ''), NULL) IS NULL
                 OR COALESCE(NULLIF(la.second_choice, ''), NULL) IS NULL
            )
    """
    params: list[Any] = []
    if candidate_no is not None:
        sql += " AND la.candidate_no = %s"
        params.append(candidate_no.strip())
    sql += " ORDER BY ps.id DESC"

    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return [dict(item) for item in cur.fetchall()]


def _is_empty(value: Any) -> bool:
    return _normalize_text(value) is None


def _draft_value(row: dict[str, Any], field_name: str, fallback_key: str) -> str | None:
    value = _normalize_text(row.get(field_name))
    if value:
        return value
    return _normalize_text(row.get(fallback_key))


def _build_backfill_updates(row: dict[str, Any]) -> dict[str, Any]:
    updates: dict[str, Any] = {}

    if _is_empty(row.get("first_choice")):
        draft_first_choice = _draft_value(row, "draft_first_choice", "draft_first_choice")
        if draft_first_choice:
            updates["first_choice"] = draft_first_choice

    if _is_empty(row.get("first_choice_id")):
        draft_first_choice_id = _draft_value(row, "draft_first_choice_id", "draft_first_choice_id")
        if draft_first_choice_id:
            updates["first_choice_id"] = draft_first_choice_id

    if _is_empty(row.get("second_choice")):
        draft_second_choice = _draft_value(row, "draft_second_choice", "draft_second_choice")
        if draft_second_choice:
            updates["second_choice"] = draft_second_choice

    if _is_empty(row.get("second_choice_id")):
        draft_second_choice_id = _draft_value(row, "draft_second_choice_id", "draft_second_choice_id")
        if draft_second_choice_id:
            updates["second_choice_id"] = draft_second_choice_id

    return updates


def _apply_backfill(rows: list[dict[str, Any]], dry_run: bool) -> tuple[list[dict[str, Any]], int]:
    planned_rows: list[dict[str, Any]] = []
    update_count = 0

    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            for row in rows:
                updates = _build_backfill_updates(row)
                if not updates:
                    continue

                planned_rows.append(
                    {
                        "portal_student_id": row.get("portal_student_id"),
                        "application_id": row.get("application_id"),
                        "candidate_no": row.get("candidate_no"),
                        "student_name": row.get("student_name"),
                        "current_first_choice": row.get("first_choice"),
                        "current_first_choice_id": row.get("first_choice_id"),
                        "current_second_choice": row.get("second_choice"),
                        "current_second_choice_id": row.get("second_choice_id"),
                        "draft_first_choice": row.get("draft_first_choice"),
                        "draft_first_choice_id": row.get("draft_first_choice_id"),
                        "draft_second_choice": row.get("draft_second_choice"),
                        "draft_second_choice_id": row.get("draft_second_choice_id"),
                        "updates": updates,
                    }
                )

                if dry_run:
                    continue

                assignments = ", ".join(f"{column} = %s" for column in updates)
                values = list(updates.values())
                values.append(row["application_id"])
                cur.execute(
                    f"""
                    UPDATE dtlms_recruitment_applications
                    SET {assignments}, updated_at = NOW()
                    WHERE id = %s
                      AND is_deleted = FALSE
                    """,
                    values,
                )
                update_count += 1

        if dry_run:
            conn.rollback()
        else:
            conn.commit()

    return planned_rows, update_count


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    counter = Counter()
    for row in rows:
        if _normalize_text(row.get("candidate_no")):
            counter["candidate_no_present"] += 1
        if _is_empty(row.get("first_choice")):
            counter["first_choice_missing"] += 1
        if _is_empty(row.get("second_choice")):
            counter["second_choice_missing"] += 1
    return {
        "total": len(rows),
        "counts": dict(counter),
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.dry_run and args.apply:
        print("[ERROR] --dry-run and --apply cannot be used together.", file=sys.stderr)
        return 1

    try:
        rows = _load_rows(args.candidate_no)
    except Exception as exc:
        print(f"[ERROR] Query failed: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Matched rows: {len(rows)}")

    if not args.dry_run and not args.apply:
        print(json.dumps([_serialize_row(row) for row in rows], ensure_ascii=False, indent=2, default=str))
        if args.summary:
            print(json.dumps(_summary(rows), ensure_ascii=False, indent=2, default=str))
        return 0

    planned_rows, update_count = _apply_backfill(rows, dry_run=not args.apply)

    print(json.dumps([_serialize_row(row) for row in planned_rows], ensure_ascii=False, indent=2, default=str))
    print(f"[INFO] Planned updates: {len(planned_rows)}")
    if args.apply:
        print(f"[INFO] Applied updates: {update_count}")
    else:
        print("[INFO] Mode: dry-run")

    if args.summary:
        print(json.dumps(_summary(rows), ensure_ascii=False, indent=2, default=str))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
