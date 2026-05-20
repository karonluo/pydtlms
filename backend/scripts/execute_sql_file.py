from __future__ import annotations

import argparse
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute a SQL file against the configured PostgreSQL database.",
        epilog=(
            "Example: python backend/scripts/execute_sql_file.py "
            "backend/sql/update20260506_1.sql --database test06"
        ),
    )
    parser.add_argument("sql_file", help="Path to the SQL script file to execute.")
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding used to read the SQL script. Default: utf-8",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only validate the file can be read and print execution target without running SQL.",
    )
    return parser


def resolve_sql_file(raw_path: str) -> Path:
    sql_path = Path(raw_path).expanduser()
    if not sql_path.is_absolute():
        sql_path = (Path.cwd() / sql_path).resolve()
    else:
        sql_path = sql_path.resolve()
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    if not sql_path.is_file():
        raise FileNotFoundError(f"SQL path is not a file: {sql_path}")
    return sql_path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        sql_path = resolve_sql_file(args.sql_file)
        sql_text = sql_path.read_text(encoding=args.encoding)
    except Exception as exc:
        print(f"[ERROR] Failed to load SQL file: {exc}", file=sys.stderr)
        return 1

    if not sql_text.strip():
        print(f"[ERROR] SQL file is empty: {sql_path}", file=sys.stderr)
        return 1

    print(f"[INFO] SQL file: {sql_path}")
    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Host: {settings.postgres_host}:{settings.postgres_port}")

    if args.dry_run:
        print("[INFO] Dry run completed. SQL was not executed.")
        return 0

    store = PostgresStateStore()

    try:
        with store._connect(args.database) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_text)
            conn.commit()
    except Exception as exc:
        print(f"[ERROR] SQL execution failed, transaction rolled back: {exc}", file=sys.stderr)
        return 1

    print("[INFO] SQL execution completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())