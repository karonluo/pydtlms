from __future__ import annotations

import argparse
import json
import sys
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
        description="Execute a SQL file or inline SQL against PostgreSQL and print the result.",
        epilog=(
            "Examples:\n"
            "  python backend/scripts/query_sql_file.py query.sql\n"
            "  python backend/scripts/query_sql_file.py --sql \"SELECT * FROM dtlms_recruitment_applications LIMIT 3\""
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("sql_file", nargs="?", help="Path to a SQL file to execute.")
    source.add_argument("--sql", help="Inline SQL text to execute.")
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


def load_sql(args: argparse.Namespace) -> str:
    if args.sql is not None:
        return str(args.sql)
    sql_path = resolve_sql_file(args.sql_file)
    return sql_path.read_text(encoding=args.encoding)


def serialize_value(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            return str(value)
    return value


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        sql_text = load_sql(args)
    except Exception as exc:
        print(f"[ERROR] Failed to load SQL: {exc}", file=sys.stderr)
        return 1

    if not sql_text.strip():
        print("[ERROR] SQL is empty.", file=sys.stderr)
        return 1

    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Host: {settings.postgres_host}:{settings.postgres_port}")

    try:
        with psycopg.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=args.database,
            user=settings.postgres_user,
            password=settings.postgres_password,
            row_factory=dict_row,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_text)
                if cur.description is None:
                    conn.commit()
                    print(json.dumps({"rowcount": cur.rowcount, "status": "ok"}, ensure_ascii=False, indent=2))
                    return 0

                rows = [serialize_value(dict(row)) for row in cur.fetchall()]
                print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
                return 0
    except Exception as exc:
        print(f"[ERROR] SQL execution failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())