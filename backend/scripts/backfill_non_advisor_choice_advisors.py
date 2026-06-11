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
        description="Backfill non-advisor first_choice/second_choice values with the student's selected advisor names.",
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


def is_non_empty(value: Any) -> bool:
    return bool(normalize_text(value))


def load_advisor_names(store: PostgresStateStore, database_name: str) -> set[str]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT TRIM(u.full_name) AS advisor_name
                FROM dtlms_users u
                JOIN dtlms_user_roles ur ON ur.user_id = u.id
                JOIN dtlms_roles r ON r.id = ur.role_id
                WHERE r.role_code = 'advisor'
                  AND u.is_active = TRUE
                  AND COALESCE(TRIM(u.full_name), '') <> ''
                ORDER BY advisor_name ASC
                """
            )
            return {normalize_text(row.get("advisor_name")) for row in cur.fetchall() if normalize_text(row.get("advisor_name"))}


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
                    ra.intended_advisor_name,
                    ps.selected_advisor_name,
                    pref1.advisor_name AS preference_one,
                    pref2.advisor_name AS preference_two
                FROM dtlms_recruitment_applications ra
                JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
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
                  AND ra.portal_student_id IS NOT NULL
                ORDER BY ra.id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def choose_first_choice_replacement(row: dict[str, Any], advisor_names: set[str]) -> str | None:
    for candidate in (
        row.get("preference_one"),
        row.get("intended_advisor_name"),
        row.get("selected_advisor_name"),
    ):
        candidate_text = normalize_text(candidate)
        if candidate_text and candidate_text in advisor_names:
            return candidate_text
    return None


def choose_second_choice_replacement(row: dict[str, Any], advisor_names: set[str]) -> str | None:
    candidate_text = normalize_text(row.get("preference_two"))
    if candidate_text and candidate_text in advisor_names:
        return candidate_text
    return None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        try:
            advisor_names = load_advisor_names(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to load advisor names: {exc}", file=sys.stderr)
            return 1

        try:
            candidate_rows = load_candidate_rows(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to load candidate rows: {exc}", file=sys.stderr)
            return 1

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Advisor names: {len(advisor_names)}")
        print(f"[INFO] Candidate rows: {len(candidate_rows)}")

        planned_updates: list[dict[str, Any]] = []
        skipped_rows = 0
        unrecoverable_first = 0
        unrecoverable_second = 0

        for row in candidate_rows:
            first_choice = normalize_text(row.get("first_choice"))
            second_choice = normalize_text(row.get("second_choice"))
            first_is_advisor = first_choice in advisor_names
            second_is_advisor = second_choice in advisor_names

            update_payload: dict[str, Any] = {
                "application_id": int(row["application_id"]),
                "candidate_no": normalize_text(row.get("candidate_no")),
                "student_name": normalize_text(row.get("student_name")),
            }

            first_replacement = None
            if not first_is_advisor:
                first_replacement = choose_first_choice_replacement(row, advisor_names)
                if first_replacement is None:
                    unrecoverable_first += 1

            second_replacement = None
            if not second_is_advisor:
                second_replacement = choose_second_choice_replacement(row, advisor_names)
                if second_replacement is None:
                    unrecoverable_second += 1

            if first_replacement is not None and first_replacement != first_choice:
                update_payload["first_choice"] = first_replacement

            if second_replacement is not None and second_replacement != second_choice:
                update_payload["second_choice"] = second_replacement

            if len(update_payload) > 3:
                planned_updates.append(update_payload)
                if args.summary:
                    changed_fields: list[str] = []
                    if "first_choice" in update_payload:
                        changed_fields.append(f"first_choice={update_payload['first_choice']}")
                    if "second_choice" in update_payload:
                        changed_fields.append(f"second_choice={update_payload['second_choice']}")
                    print(
                        f"[PLAN] application_id={update_payload['application_id']} candidate_no={update_payload['candidate_no']} "
                        f"student_name={update_payload['student_name']} "
                        f"{' '.join(changed_fields)}"
                    )
            else:
                if not first_is_advisor or not second_is_advisor:
                    skipped_rows += 1

        print(f"[INFO] Planned updates: {len(planned_updates)}")
        print(f"[INFO] Skipped rows: {skipped_rows}")
        print(f"[INFO] Unrecoverable first_choice rows: {unrecoverable_first}")
        print(f"[INFO] Unrecoverable second_choice rows: {unrecoverable_second}")

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
                    if "second_choice" in item:
                        set_clauses.append("second_choice = %s")
                        params.append(item["second_choice"])

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
                            print(f"[UPDATE] application_id={item['application_id']} candidate_no={item['candidate_no']}")

            conn.commit()

        print(f"[INFO] Updated rows: {updated_count}")
        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())