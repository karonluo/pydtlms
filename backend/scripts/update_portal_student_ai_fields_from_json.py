from __future__ import annotations

import argparse
import json
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
        description="Update ai_industry_opinion and ai_problem_statement by candidate_no from a JSON array file.",
        epilog="Example: python backend/scripts/update_portal_student_ai_fields_from_json.py data.json --apply",
    )
    parser.add_argument(
        "json_file",
        help="Path to the JSON array file containing candidate_no and AI text fields.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the updates to PostgreSQL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only validate and preview the changes without writing to PostgreSQL.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a per-row summary while processing.",
    )
    return parser


def resolve_json_file(raw_path: str) -> Path:
    json_path = Path(raw_path).expanduser()
    if not json_path.is_absolute():
        json_path = (Path.cwd() / json_path).resolve()
    else:
        json_path = json_path.resolve()
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not json_path.is_file():
        raise FileNotFoundError(f"JSON path is not a file: {json_path}")
    return json_path


def load_rows(json_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("JSON root must be a list")

    rows: list[dict[str, Any]] = []
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Row #{index} is not an object")
        candidate_no = str(item.get("candidate_no") or "").strip()
        if not candidate_no:
            raise ValueError(f"Row #{index} is missing candidate_no")
        if "candidate_no" not in item:
            raise ValueError(f"Row #{index} is missing required key: candidate_no")
        if "ai_problem_statement" not in item:
            raise ValueError(f"Row #{index} is missing required key: ai_problem_statement")
        if "ai_industry_opinion" not in item:
            raise ValueError(f"Row #{index} is missing required key: ai_industry_opinion")
        rows.append(
            {
                "candidate_no": candidate_no,
                "ai_problem_statement": _normalize_text(item.get("ai_problem_statement")),
                "ai_industry_opinion": _normalize_text(item.get("ai_industry_opinion")),
            }
        )
    return rows


def _normalize_text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text if text else None


def load_target_application(store: PostgresStateStore, database_name: str, candidate_no: str) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ra.id AS application_id,
                    ra.candidate_no,
                    ra.student_name,
                    ps.ai_problem_statement,
                    ps.ai_industry_opinion
                FROM dtlms_recruitment_applications AS ra
                LEFT JOIN dtlms_portal_application_personal_statements AS ps
                  ON ps.application_id = ra.id
                WHERE ra.candidate_no = %s
                  AND ra.is_deleted = FALSE
                ORDER BY ra.id DESC
                LIMIT 1
                """,
                (candidate_no,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def update_row(store: PostgresStateStore, database_name: str, row: dict[str, Any]) -> bool:
    with store._connect(database_name) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE dtlms_portal_application_personal_statements
                SET ai_problem_statement = %s,
                    ai_industry_opinion = %s,
                    updated_at = CURRENT_TIMESTAMP
                FROM dtlms_recruitment_applications ra
                WHERE dtlms_portal_application_personal_statements.application_id = ra.id
                  AND ra.candidate_no = %s
                  AND ra.is_deleted = FALSE
                """,
                (
                    row["ai_problem_statement"],
                    row["ai_industry_opinion"],
                    row["candidate_no"],
                ),
            )
            updated_count = cur.rowcount
        conn.commit()
    return updated_count > 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        json_path = resolve_json_file(args.json_file)
        rows = load_rows(json_path)
    except Exception as exc:
        print(f"[ERROR] Failed to load JSON file: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] JSON file: {json_path}")
    print(f"[INFO] Database: {args.database}")
    print(f"[INFO] Rows loaded: {len(rows)}")

    if args.dry_run and args.apply:
        print("[ERROR] --dry-run and --apply cannot be used together", file=sys.stderr)
        return 1

    if not args.apply:
        for item in rows[:10]:
            print(
                f"[PREVIEW] candidate_no={item['candidate_no']} ai_problem_statement={item['ai_problem_statement']!r} ai_industry_opinion={item['ai_industry_opinion']!r}"
            )
        print("[INFO] Dry run completed. No database changes were made.")
        return 0

    store = PostgresStateStore()
    updated_count = 0
    skipped_count = 0

    for index, item in enumerate(rows, start=1):
        target_row = load_target_application(store, args.database, item["candidate_no"])
        if target_row is None:
            skipped_count += 1
            if args.summary:
                print(f"[SKIP] {item['candidate_no']} not found")
            continue

        changed = update_row(store, args.database, item)
        if changed:
            updated_count += 1
            if args.summary:
                print(f"[UPDATE] {item['candidate_no']} application_id={target_row['application_id']}")
        else:
            skipped_count += 1
            if args.summary:
                print(f"[SKIP] {item['candidate_no']} already aligned or missing personal statement row")

        if index % 25 == 0:
            print(f"[INFO] Processed {index}/{len(rows)} rows...")

    print(f"[INFO] Updated rows: {updated_count}")
    print(f"[INFO] Skipped rows: {skipped_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
