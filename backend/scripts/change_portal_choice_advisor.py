from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row
from psycopg import sql


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Change the advisor for first-choice or second-choice recruitment applications.",
        epilog=(
            "Examples:\n"
            "  python backend/scripts/change_portal_choice_advisor.py --r 1 --old_id 123 --new_id 456 --dry-run\n"
            "  python backend/scripts/change_portal_choice_advisor.py --r 2 --old_id 123 --new_id 456 --apply"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--r",
        type=int,
        required=True,
        choices=(1, 2),
        help="Choice round to update: 1 for first choice, 2 for second choice.",
    )
    parser.add_argument(
        "--old-id",
        type=int,
        required=True,
        help="Original advisor user ID.",
    )
    parser.add_argument(
        "--new-id",
        type=int,
        required=True,
        help="New advisor user ID.",
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


def choice_fields(choice_round: int) -> tuple[str, str]:
    if choice_round == 1:
        return "first_choice", "first_choice_id"
    return "second_choice", "second_choice_id"


def load_advisor_name(store: PostgresStateStore, database_name: str, user_id: int) -> str | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.id, TRIM(u.full_name) AS full_name
                FROM dtlms_users u
                JOIN dtlms_user_roles ur ON ur.user_id = u.id
                JOIN dtlms_roles r ON r.id = ur.role_id
                WHERE u.id = %s
                  AND r.role_code = 'advisor'
                LIMIT 1
                """,
                (user_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return normalize_text(row.get("full_name")) or None


def load_target_rows(
    store: PostgresStateStore,
    database_name: str,
    choice_name_field: str,
    choice_id_field: str,
    old_name: str,
    old_id: int,
) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    """
                    SELECT
                        ra.id AS application_id,
                        ra.candidate_no,
                        ra.student_name,
                        ra.{choice_name_field} AS choice_name,
                        ra.{choice_id_field} AS choice_id
                    FROM dtlms_recruitment_applications ra
                    WHERE ra.is_deleted = FALSE
                      AND (
                            ra.{choice_name_field} = %s
                         OR ra.{choice_id_field} = %s
                      )
                    ORDER BY ra.id ASC
                    """
                ).format(
                    choice_name_field=sql.Identifier(choice_name_field),
                    choice_id_field=sql.Identifier(choice_id_field),
                ),
                (old_name, old_id),
            )
            return [dict(row) for row in cur.fetchall()]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.apply and args.dry_run:
        print("[ERROR] --apply and --dry-run cannot be used together.", file=sys.stderr)
        return 1
    if args.old_id <= 0 or args.new_id <= 0:
        print("[ERROR] --old-id and --new-id must be positive integers.", file=sys.stderr)
        return 1
    if args.old_id == args.new_id:
        print("[ERROR] --old-id and --new-id must be different.", file=sys.stderr)
        return 1

    choice_name_field, choice_id_field = choice_fields(args.r)
    choice_label = "第一志愿" if args.r == 1 else "第二志愿"
    store = PostgresStateStore()

    try:
        old_name = load_advisor_name(store, args.database, args.old_id)
        new_name = load_advisor_name(store, args.database, args.new_id)
    except Exception as exc:
        print(f"[ERROR] Failed to load advisor metadata: {exc}", file=sys.stderr)
        return 1

    if old_name is None:
        print(f"[ERROR] Old advisor user ID {args.old_id} is not a valid advisor.", file=sys.stderr)
        return 1
    if new_name is None:
        print(f"[ERROR] New advisor user ID {args.new_id} is not a valid advisor.", file=sys.stderr)
        return 1

    try:
        target_rows = load_target_rows(
            store,
            args.database,
            choice_name_field,
            choice_id_field,
            old_name,
            args.old_id,
        )
    except Exception as exc:
        print(f"[ERROR] Failed to load target rows: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Choice round: {args.r} ({choice_label})")
    print(f"[INFO] Old advisor: {args.old_id} {old_name}")
    print(f"[INFO] New advisor: {args.new_id} {new_name}")
    print(f"[INFO] Match rule: {choice_name_field} = {old_name} OR {choice_id_field} = {args.old_id}")
    print(f"[INFO] Target rows: {len(target_rows)}")

    if not target_rows:
        print("[INFO] No matching rows found. Nothing to do.")
        return 0

    if args.summary:
        for row in target_rows[:200]:
            print(
                f"[PLAN] application_id={row['application_id']} candidate_no={normalize_text(row.get('candidate_no'))} "
                f"student_name={normalize_text(row.get('student_name'))} "
                f"{choice_name_field}={old_name!r} -> {new_name!r}, {choice_id_field}={args.old_id} -> {args.new_id}"
            )
        if len(target_rows) > 200:
            print(f"[INFO] Summary capped at 200 rows, total rows: {len(target_rows)}")

    if args.dry_run or not args.apply:
        print("[INFO] Dry run completed. No changes were written.")
        if not args.apply:
            print("[INFO] Re-run with --apply to persist updates.")
        return 0

    updated_count = 0
    with store._connect(args.database) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            for row in target_rows:
                cur.execute(
                    sql.SQL(
                        """
                        UPDATE dtlms_recruitment_applications
                        SET {choice_name_field} = %s,
                            {choice_id_field} = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                          AND is_deleted = FALSE
                          AND (
                                {choice_name_field} = %s
                             OR {choice_id_field} = %s
                          )
                        """
                    ).format(
                        choice_name_field=sql.Identifier(choice_name_field),
                        choice_id_field=sql.Identifier(choice_id_field),
                    ),
                    (new_name, args.new_id, int(row["application_id"]), old_name, args.old_id),
                )
                if cur.rowcount > 0:
                    updated_count += 1
                    if args.summary:
                        print(
                            f"[UPDATE] application_id={row['application_id']} candidate_no={normalize_text(row.get('candidate_no'))} "
                            f"student_name={normalize_text(row.get('student_name'))}"
                        )

        conn.commit()

    print(f"[INFO] Updated rows: {updated_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())