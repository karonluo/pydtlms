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
        description="Update a research center's members and leader, including disabled advisor users.",
        epilog=(
            "Examples:\n"
            "  python backend/scripts/update_research_center_members.py --team-id 1001 --user-ids 10,11,12 --leader-id 10 --dry-run\n"
            "  python backend/scripts/update_research_center_members.py --team-id 1001 --user-ids 10,11,12 --leader-id 10 --apply"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--team-id",
        type=int,
        required=True,
        help="Research center ID.",
    )
    parser.add_argument(
        "--user-ids",
        required=True,
        help="Comma-separated advisor user IDs to keep in the center, including the leader.",
    )
    parser.add_argument(
        "--leader-id",
        type=int,
        default=None,
        help="Leader user ID. If omitted or empty, the leader will not be changed.",
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
        help="Print a concise row-level summary while processing.",
    )
    return parser


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def parse_user_ids(raw_value: str) -> list[int]:
    user_ids: list[int] = []
    for part in str(raw_value or "").split(","):
        text = part.strip()
        if not text:
            continue
        try:
            user_id = int(text)
        except ValueError as exc:
            raise ValueError(f"Invalid user id: {text}") from exc
        if user_id <= 0:
            raise ValueError(f"User id must be a positive integer: {text}")
        if user_id not in user_ids:
            user_ids.append(user_id)
    return user_ids


def load_team_row(store: PostgresStateStore, database_name: str, team_id: int) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    t.id,
                    t.team_name,
                    t.lead_user_id,
                    lead_user.full_name AS lead_user_name
                FROM dtlms_teams t
                LEFT JOIN dtlms_users lead_user
                  ON lead_user.id = t.lead_user_id
                 AND lead_user.is_deleted = FALSE
                WHERE t.id = %s
                  AND t.is_deleted = FALSE
                """,
                (int(team_id),),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def load_advisor_user(store: PostgresStateStore, database_name: str, user_id: int) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    u.id,
                    u.full_name
                FROM dtlms_users u
                JOIN dtlms_user_roles ur ON ur.user_id = u.id
                JOIN dtlms_roles r ON r.id = ur.role_id
                WHERE u.id = %s
                  AND u.is_deleted = FALSE
                  AND r.is_deleted = FALSE
                  AND r.role_code = 'advisor'
                LIMIT 1
                """,
                (int(user_id),),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def load_current_center_members(store: PostgresStateStore, database_name: str, team_id: int) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ta.id AS relation_id,
                    ta.advisor_user_id,
                    u.full_name
                FROM dtlms_team_advisors ta
                JOIN dtlms_users u
                  ON u.id = ta.advisor_user_id
                 AND u.is_deleted = FALSE
                WHERE ta.team_id = %s
                  AND ta.is_deleted = FALSE
                ORDER BY ta.id ASC
                """,
                (int(team_id),),
            )
            return [dict(row) for row in cur.fetchall()]


def update_center_members(
    store: PostgresStateStore,
    database_name: str,
    team_id: int,
    user_ids: list[int],
    leader_id: int | None,
    *,
    apply: bool,
) -> dict[str, Any]:
    team_row = load_team_row(store, database_name, team_id)
    if team_row is None:
        raise KeyError(team_id)

    candidate_users = [load_advisor_user(store, database_name, user_id) for user_id in user_ids]
    missing_user_ids = [user_id for user_id, user_row in zip(user_ids, candidate_users) if user_row is None]
    if missing_user_ids:
        raise ValueError(f"These user ids are not active advisor users: {','.join(str(item) for item in missing_user_ids)}")

    if leader_id is not None and leader_id > 0 and leader_id not in user_ids:
        raise ValueError("leader-id must be included in user-ids.")

    current_members = load_current_center_members(store, database_name, team_id)
    current_member_ids = [int(row["advisor_user_id"]) for row in current_members]
    planned_member_ids = user_ids[:]
    if leader_id is not None and leader_id > 0 and leader_id not in planned_member_ids:
        planned_member_ids.insert(0, leader_id)

    result = {
        "team_id": int(team_id),
        "team_name": normalize_text(team_row.get("team_name")),
        "current_leader_id": int(team_row.get("lead_user_id") or 0) or None,
        "current_leader_name": normalize_text(team_row.get("lead_user_name")),
        "current_member_ids": current_member_ids,
        "planned_member_ids": planned_member_ids,
        "planned_leader_id": leader_id if leader_id and leader_id > 0 else int(team_row.get("lead_user_id") or 0) or None,
        "apply": apply,
    }

    if not apply:
        return result

    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            if leader_id is not None and leader_id > 0:
                cur.execute(
                    """
                    UPDATE dtlms_teams
                    SET lead_user_id = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                      AND is_deleted = FALSE
                    """,
                    (int(leader_id), int(team_id)),
                )
                if cur.rowcount <= 0:
                    raise KeyError(team_id)

            cur.execute(
                """
                DELETE FROM dtlms_team_advisors
                WHERE team_id = %s
                """,
                (int(team_id),),
            )

            for user_id in planned_member_ids:
                cur.execute(
                    """
                    INSERT INTO dtlms_team_advisors (
                        team_id,
                        advisor_user_id,
                        is_deleted
                    ) VALUES (%s, %s, FALSE)
                    """,
                    (int(team_id), int(user_id)),
                )

        conn.commit()

    result["updated_member_ids"] = planned_member_ids
    result["updated_leader_id"] = leader_id if leader_id is not None and leader_id > 0 else int(team_row.get("lead_user_id") or 0) or None
    return result


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.apply and args.dry_run:
        print("[ERROR] --apply and --dry-run cannot be used together.", file=sys.stderr)
        return 1
    if args.team_id <= 0:
        print("[ERROR] --team-id must be a positive integer.", file=sys.stderr)
        return 1

    try:
        user_ids = parse_user_ids(args.user_ids)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if not user_ids:
        print("[ERROR] --user-ids cannot be empty.", file=sys.stderr)
        return 1

    if args.leader_id is not None and args.leader_id <= 0:
        print("[ERROR] --leader-id must be a positive integer when provided.", file=sys.stderr)
        return 1

    store = PostgresStateStore()
    try:
        result = update_center_members(
            store,
            args.database,
            args.team_id,
            user_ids,
            args.leader_id,
            apply=args.apply,
        )
    except KeyError:
        print(f"[ERROR] Team {args.team_id} not found.", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[ERROR] Failed to update research center members: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Team ID: {args.team_id}")
    print(f"[INFO] Team name: {result['team_name']}")
    print(f"[INFO] Current leader: {result['current_leader_id']} {result['current_leader_name']}")
    print(f"[INFO] Planned leader: {result['planned_leader_id']}")
    print(f"[INFO] Planned members: {','.join(str(item) for item in result['planned_member_ids'])}")

    if args.summary:
        current_member_ids = result.get("current_member_ids", [])
        print(f"[PLAN] current_member_ids={','.join(str(item) for item in current_member_ids)}")
        print(f"[PLAN] planned_member_ids={','.join(str(item) for item in result['planned_member_ids'])}")

    if not args.apply:
        print("[INFO] Dry run completed. No changes were written.")
        print("[INFO] Re-run with --apply to persist updates.")
        return 0

    print("[INFO] Update applied successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())