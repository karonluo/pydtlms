from __future__ import annotations

import argparse
from dataclasses import dataclass
import sys
from typing import Any

from psycopg.rows import dict_row

BACKEND_DIR = __import__("pathlib").Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


@dataclass(frozen=True)
class AdvisorProfileRow:
    username: str
    full_name: str
    role_code: str
    role_name: str
    department_name: str
    introduction: str | None
    phone_number: str | None
    email: str | None
    theme_color: str | None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare advisor user profile fields between two PostgreSQL databases and sync test data to production.",
    )
    parser.add_argument("--source-db", default="test25", help="Source database name. Default: test25")
    parser.add_argument("--target-db", default="test26", help="Target database name. Default: test26")
    parser.add_argument("--apply", action="store_true", help="Apply updates to the target database.")
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum number of changed rows to print.")
    return parser


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _load_advisor_profile_rows(store: PostgresStateStore, database_name: str) -> list[AdvisorProfileRow]:
    query = """
        SELECT
            u.username,
            COALESCE(NULLIF(BTRIM(u.full_name), ''), u.username) AS full_name,
            COALESCE(r.role_code, '') AS role_code,
            COALESCE(r.role_name, '') AS role_name,
            COALESCE(NULLIF(BTRIM(up.department_name), ''), NULLIF(BTRIM(u.department_name), ''), '') AS department_name,
            NULLIF(BTRIM(up.introduction), '') AS introduction,
            COALESCE(NULLIF(BTRIM(up.phone_number), ''), NULLIF(BTRIM(u.phone_number), '')) AS phone_number,
            COALESCE(NULLIF(BTRIM(up.email), ''), NULLIF(BTRIM(u.email), '')) AS email,
            COALESCE(NULLIF(BTRIM(up.theme_color), ''), CASE WHEN COALESCE(r.role_code, '') = 'advisor' THEN '#13795b' ELSE '#0f4cbd' END) AS theme_color
        FROM dtlms_users AS u
        LEFT JOIN dtlms_user_roles AS ur ON ur.user_id = u.id
        LEFT JOIN dtlms_roles AS r ON r.id = ur.role_id AND r.is_deleted = FALSE
        LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
        WHERE u.is_deleted = FALSE
          AND COALESCE(r.role_code, '') = 'advisor'
        ORDER BY u.id ASC
    """

    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        AdvisorProfileRow(
            username=str(row["username"]),
            full_name=str(row["full_name"]),
            role_code=str(row["role_code"]),
            role_name=str(row["role_name"]),
            department_name=str(row["department_name"]),
            introduction=_normalize_text(row.get("introduction")),
            phone_number=_normalize_text(row.get("phone_number")),
            email=_normalize_text(row.get("email")),
            theme_color=_normalize_text(row.get("theme_color")),
        )
        for row in rows
    ]


def _rows_by_username(rows: list[AdvisorProfileRow]) -> dict[str, AdvisorProfileRow]:
    return {row.username: row for row in rows}


def _diff_fields(source: AdvisorProfileRow, target: AdvisorProfileRow | None) -> dict[str, tuple[str | None, str | None]]:
    if target is None:
        return {
            "introduction": (None, source.introduction),
            "phone_number": (None, source.phone_number),
            "email": (None, source.email),
        }

    diffs: dict[str, tuple[str | None, str | None]] = {}
    for field_name in ("introduction", "phone_number", "email"):
        source_value = getattr(source, field_name)
        target_value = getattr(target, field_name)
        if source_value != target_value:
            diffs[field_name] = (target_value, source_value)
    return diffs


def _print_diff_preview(diff_rows: list[tuple[AdvisorProfileRow, AdvisorProfileRow | None, dict[str, tuple[str | None, str | None]]]], limit: int) -> None:
    print(f"[INFO] 差异导师数: {len(diff_rows)}")
    if not diff_rows:
        return

    preview_rows = diff_rows if limit <= 0 else diff_rows[:limit]
    for source_row, target_row, diffs in preview_rows:
        target_username = target_row.username if target_row else "<missing>"
        changed_fields = ", ".join(
            f"{field}: {old_value!r} -> {new_value!r}" for field, (old_value, new_value) in diffs.items()
        )
        print(f"[DIFF] {source_row.username} / target={target_username} / {changed_fields}")


def _upsert_target_profile(target_conn, row: AdvisorProfileRow) -> None:
    with target_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dtlms_user_profiles (
                username, full_name, role_name, department_name, introduction, phone_number, email, theme_color
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE
            SET full_name = EXCLUDED.full_name,
                role_name = EXCLUDED.role_name,
                department_name = EXCLUDED.department_name,
                introduction = COALESCE(EXCLUDED.introduction, dtlms_user_profiles.introduction),
                phone_number = COALESCE(EXCLUDED.phone_number, dtlms_user_profiles.phone_number),
                email = COALESCE(EXCLUDED.email, dtlms_user_profiles.email),
                theme_color = COALESCE(NULLIF(BTRIM(dtlms_user_profiles.theme_color), ''), EXCLUDED.theme_color),
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                row.username,
                row.full_name,
                row.role_name or "导师",
                row.department_name,
                row.introduction,
                row.phone_number,
                row.email,
                row.theme_color or "#13795b",
            ),
        )

        cur.execute(
            """
            UPDATE dtlms_users
            SET phone_number = COALESCE(%s, phone_number),
                email = COALESCE(%s, email),
                updated_at = CURRENT_TIMESTAMP
            WHERE username = %s
              AND is_deleted = FALSE
            """,
            (row.phone_number, row.email, row.username),
        )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()

    try:
        source_rows = _load_advisor_profile_rows(store, args.source_db)
        target_rows = _load_advisor_profile_rows(store, args.target_db)
    except Exception as exc:
        print(f"[ERROR] Failed to load advisor rows: {exc}", file=sys.stderr)
        return 1

    source_map = _rows_by_username(source_rows)
    target_map = _rows_by_username(target_rows)

    diff_rows: list[tuple[AdvisorProfileRow, AdvisorProfileRow | None, dict[str, tuple[str | None, str | None]]]] = []
    for username, source_row in source_map.items():
        target_row = target_map.get(username)
        diffs = _diff_fields(source_row, target_row)
        if diffs:
            diff_rows.append((source_row, target_row, diffs))

    print(f"[INFO] Source database: {args.source_db}")
    print(f"[INFO] Target database: {args.target_db}")
    print(f"[INFO] Source advisor rows: {len(source_rows)}")
    print(f"[INFO] Target advisor rows: {len(target_rows)}")
    _print_diff_preview(diff_rows, args.limit)

    if not args.apply:
        print("[INFO] Dry run completed. Re-run with --apply to write updates into the target database.")
        return 0

    updated_count = 0
    try:
        with store._connect(args.target_db) as target_conn:
            for source_row, _, _ in diff_rows:
                _upsert_target_profile(target_conn, source_row)
                updated_count += 1
            target_conn.commit()
    except Exception as exc:
        print(f"[ERROR] Update failed, transaction rolled back: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Update completed successfully. Updated/inserted advisor profiles: {updated_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())