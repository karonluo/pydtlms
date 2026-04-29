from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from psycopg.rows import dict_row

from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def load_runtime_portal_students(
    postgres_store: PostgresStateStore,
    *,
    student_id: int | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    where_clauses = ["1 = 1"]
    params: list[Any] = []
    if student_id is not None:
        where_clauses.append("id = %s")
        params.append(int(student_id))

    limit_sql = ""
    if limit is not None:
        limit_sql = " LIMIT %s"
        params.append(int(limit))

    query = f"""
        SELECT id, payload
        FROM dtlms_runtime_portal_students
        WHERE {' AND '.join(where_clauses)}
        ORDER BY id ASC
        {limit_sql}
    """

    with postgres_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    students: list[dict[str, Any]] = []
    for row in rows:
        payload = row.get("payload") if isinstance(row, dict) else None
        if not isinstance(payload, dict):
            continue
        normalized = dict(payload)
        normalized.setdefault("id", row.get("id"))
        students.append(normalized)
    return students


def validate_student_payload(student: dict[str, Any]) -> tuple[bool, str | None]:
    required_fields = ("id", "full_name", "phone_number", "email", "id_number")
    for field in required_fields:
        value = student.get(field)
        if value in (None, ""):
            return False, field
    return True, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill portal students from runtime JSONB table into relational tables.",
    )
    parser.add_argument("--student-id", type=int, help="Only backfill one portal student by id.")
    parser.add_argument("--limit", type=int, help="Only process the first N runtime records.")
    parser.add_argument("--dry-run", action="store_true", help="Read and validate only, do not write to relational tables.")
    parser.add_argument("--summary", action="store_true", help="Print summary as compact JSON.")
    args = parser.parse_args()

    postgres_store = PostgresStateStore()
    postgres_store.ensure_schema()

    runtime_students = load_runtime_portal_students(
        postgres_store,
        student_id=args.student_id,
        limit=args.limit,
    )

    processed = 0
    skipped = 0
    invalid_students: list[dict[str, Any]] = []

    for student in runtime_students:
        valid, missing_field = validate_student_payload(student)
        if not valid:
            skipped += 1
            invalid_students.append(
                {
                    "id": student.get("id"),
                    "missing_field": missing_field,
                }
            )
            continue

        if not args.dry_run:
            postgres_store.sync_portal_student(student, operation_log=None)
        processed += 1

    summary = {
        "database": settings.postgres_db,
        "dry_run": bool(args.dry_run),
        "loaded_from_runtime": len(runtime_students),
        "processed": processed,
        "skipped": skipped,
        "invalid_students": invalid_students,
    }
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False))
        return

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()