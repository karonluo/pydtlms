from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill first_choice/second_choice advisor names and IDs for recruitment applications.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned updates without writing to PostgreSQL.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the planned updates to PostgreSQL.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a short per-row summary while processing.",
    )
    return parser


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def is_placeholder_choice_text(value: Any) -> bool:
    text = normalize_text(value)
    if not text:
        return True
    return "中心" in text


def is_valid_advisor_name(value: Any, advisor_lookup: dict[str, int]) -> bool:
    text = normalize_text(value)
    return bool(text) and text not in {"研究中心"} and text in advisor_lookup


def load_advisor_lookup(store: PostgresStateStore, database_name: str) -> dict[str, int]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT ON (TRIM(u.full_name))
                    TRIM(u.full_name) AS advisor_name,
                    u.id AS advisor_user_id
                FROM dtlms_users u
                JOIN dtlms_user_roles ur ON ur.user_id = u.id
                JOIN dtlms_roles r ON r.id = ur.role_id
                WHERE r.role_code = 'advisor'
                  AND u.is_active = TRUE
                  AND COALESCE(TRIM(u.full_name), '') <> ''
                ORDER BY TRIM(u.full_name) ASC, u.id ASC
                """
            )
            advisor_lookup: dict[str, int] = {}
            for row in cur.fetchall():
                advisor_name = normalize_text(row.get("advisor_name"))
                advisor_user_id = int(row.get("advisor_user_id") or 0) or None
                if advisor_name and advisor_user_id is not None:
                    advisor_lookup.setdefault(advisor_name, advisor_user_id)
            return advisor_lookup


def load_candidate_rows(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ra.id AS application_id,
                    ra.portal_student_id,
                    ra.candidate_no,
                    ra.student_name,
                    ra.first_choice,
                    ra.second_choice,
                    ra.first_choice_id,
                    ra.second_choice_id,
                    ra.intended_advisor_name,
                    ps.selected_advisor_name,
                    pref1.advisor_name AS preference_one,
                    pref2.advisor_name AS preference_two
                FROM dtlms_recruitment_applications ra
                LEFT JOIN dtlms_portal_students ps
                    ON ps.id = ra.portal_student_id
                LEFT JOIN LATERAL (
                    SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                    FROM dtlms_portal_application_preferences pref
                    WHERE pref.application_id = ra.id
                      AND pref.preference_order = 1
                    ORDER BY pref.id ASC
                    LIMIT 1
                ) pref1 ON TRUE
                LEFT JOIN LATERAL (
                    SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                    FROM dtlms_portal_application_preferences pref
                    WHERE pref.application_id = ra.id
                      AND pref.preference_order = 2
                    ORDER BY pref.id ASC
                    LIMIT 1
                ) pref2 ON TRUE
                WHERE ra.is_deleted = FALSE
                ORDER BY ra.id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def ensure_target_columns(store: PostgresStateStore, database_name: str) -> None:
    with store._connect(database_name) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                ALTER TABLE IF EXISTS dtlms_recruitment_applications
                    ADD COLUMN IF NOT EXISTS first_choice_id BIGINT,
                    ADD COLUMN IF NOT EXISTS second_choice_id BIGINT
                """
            )
        conn.commit()


def resolve_first_choice(row: dict[str, Any], advisor_lookup: dict[str, int]) -> tuple[str | None, int | None, str]:
    current_first = normalize_text(row.get("first_choice"))
    if is_valid_advisor_name(current_first, advisor_lookup):
        return current_first, advisor_lookup[current_first], "current"

    for source_name in ("preference_one", "intended_advisor_name", "selected_advisor_name"):
        candidate_text = normalize_text(row.get(source_name))
        if is_valid_advisor_name(candidate_text, advisor_lookup):
            return candidate_text, advisor_lookup[candidate_text], source_name

    return None, None, "missing"


def resolve_second_choice(row: dict[str, Any], advisor_lookup: dict[str, int]) -> tuple[str | None, int | None, str]:
    current_second = normalize_text(row.get("second_choice"))
    if is_valid_advisor_name(current_second, advisor_lookup):
        return current_second, advisor_lookup[current_second], "current"

    candidate_text = normalize_text(row.get("preference_two"))
    if is_valid_advisor_name(candidate_text, advisor_lookup):
        return candidate_text, advisor_lookup[candidate_text], "preference_two"

    return None, None, "missing"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()

    try:
        ensure_target_columns(store, args.database)
        advisor_lookup = load_advisor_lookup(store, args.database)
    except Exception as exc:
        print(f"[ERROR] Failed to load advisor lookup: {exc}", file=sys.stderr)
        return 1

    try:
        candidate_rows = load_candidate_rows(store, args.database)
    except Exception as exc:
        print(f"[ERROR] Failed to load candidate rows: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Advisor names: {len(advisor_lookup)}")
    print(f"[INFO] Candidate rows: {len(candidate_rows)}")

    planned_updates: list[dict[str, Any]] = []
    untouched_rows = 0
    unresolved_first_choice = 0
    unresolved_second_choice = 0

    for row in candidate_rows:
        application_id = int(row["application_id"])
        candidate_no = normalize_text(row.get("candidate_no"))
        student_name = normalize_text(row.get("student_name"))

        current_first = normalize_text(row.get("first_choice"))
        current_second = normalize_text(row.get("second_choice"))
        current_first_id = int(row.get("first_choice_id") or 0) or None
        current_second_id = int(row.get("second_choice_id") or 0) or None

        resolved_first_name, resolved_first_id, first_source = resolve_first_choice(row, advisor_lookup)
        resolved_second_name, resolved_second_id, second_source = resolve_second_choice(row, advisor_lookup)

        update_payload: dict[str, Any] = {"application_id": application_id}

        first_text_should_clear = is_placeholder_choice_text(current_first) or current_first not in advisor_lookup
        second_text_should_clear = is_placeholder_choice_text(current_second) or current_second not in advisor_lookup

        if resolved_first_name is not None:
            if resolved_first_name != current_first:
                update_payload["first_choice"] = resolved_first_name
        elif first_text_should_clear:
            update_payload["first_choice"] = None
            unresolved_first_choice += 1

        if resolved_first_id != current_first_id:
            update_payload["first_choice_id"] = resolved_first_id

        if resolved_second_name is not None:
            if resolved_second_name != current_second:
                update_payload["second_choice"] = resolved_second_name
        elif second_text_should_clear:
            update_payload["second_choice"] = None
            unresolved_second_choice += 1

        if resolved_second_id != current_second_id:
            update_payload["second_choice_id"] = resolved_second_id

        if len(update_payload) > 1:
            planned_updates.append(update_payload)
            if args.summary:
                changed_bits: list[str] = []
                if "first_choice" in update_payload:
                    changed_bits.append(f"first_choice={update_payload['first_choice']!r}")
                if "first_choice_id" in update_payload:
                    changed_bits.append(f"first_choice_id={update_payload['first_choice_id']!r}")
                if "second_choice" in update_payload:
                    changed_bits.append(f"second_choice={update_payload['second_choice']!r}")
                if "second_choice_id" in update_payload:
                    changed_bits.append(f"second_choice_id={update_payload['second_choice_id']!r}")
                print(
                    f"[PLAN] application_id={application_id} candidate_no={candidate_no} student_name={student_name} "
                    f"first_source={first_source} second_source={second_source} {' '.join(changed_bits)}"
                )
        else:
            untouched_rows += 1

    print(f"[INFO] Planned updates: {len(planned_updates)}")
    print(f"[INFO] Untouched rows: {untouched_rows}")
    print(f"[INFO] Unresolved first_choice rows: {unresolved_first_choice}")
    print(f"[INFO] Unresolved second_choice rows: {unresolved_second_choice}")

    if args.dry_run or not args.apply:
        print("[INFO] Dry run completed. No changes were written.")
        if not args.apply:
            print("[INFO] Re-run with --apply to persist updates.")
        return 0

    updated_count = 0
    with store._connect(args.database) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            for item in planned_updates:
                set_clauses: list[str] = []
                params: list[Any] = []

                if "first_choice" in item:
                    set_clauses.append("first_choice = %s")
                    params.append(item["first_choice"])
                if "first_choice_id" in item:
                    set_clauses.append("first_choice_id = %s")
                    params.append(item["first_choice_id"])
                if "second_choice" in item:
                    set_clauses.append("second_choice = %s")
                    params.append(item["second_choice"])
                if "second_choice_id" in item:
                    set_clauses.append("second_choice_id = %s")
                    params.append(item["second_choice_id"])

                if not set_clauses:
                    continue

                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                params.append(int(item["application_id"]))

                cur.execute(
                    f"""
                    UPDATE dtlms_recruitment_applications
                    SET {', '.join(set_clauses)}
                    WHERE id = %s
                      AND is_deleted = FALSE
                    """,
                    params,
                )
                if cur.rowcount > 0:
                    updated_count += 1
                    if args.summary:
                        print(f"[UPDATE] application_id={item['application_id']}")
        conn.commit()

    print(f"[INFO] Updated rows: {updated_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
