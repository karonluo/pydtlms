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


def load_runtime_teams(
    postgres_store: PostgresStateStore,
    *,
    team_id: int | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    where_clauses = ["1 = 1"]
    params: list[Any] = []
    if team_id is not None:
        where_clauses.append("id = %s")
        params.append(int(team_id))

    limit_sql = ""
    if limit is not None:
        limit_sql = " LIMIT %s"
        params.append(int(limit))

    query = f"""
        SELECT id, payload
        FROM dtlms_runtime_teams
        WHERE {' AND '.join(where_clauses)}
        ORDER BY id ASC
        {limit_sql}
    """
    with postgres_store._connect(settings.postgres_db) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()

    teams: list[dict[str, Any]] = []
    for row in rows:
        payload = row.get("payload") if isinstance(row, dict) else None
        if not isinstance(payload, dict):
            continue
        normalized = dict(payload)
        normalized.setdefault("id", row.get("id"))
        teams.append(normalized)
    return teams


def load_runtime_students(
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
        FROM dtlms_runtime_students
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


def validate_team_payload(team: dict[str, Any]) -> tuple[bool, str | None]:
    for field in ("id", "team_name"):
        if team.get(field) in (None, ""):
            return False, field
    return True, None


def validate_student_payload(student: dict[str, Any]) -> tuple[bool, str | None]:
    for field in ("id", "student_no", "full_name", "advisor_name", "team_name", "degree_type", "enrollment_year"):
        if student.get(field) in (None, ""):
            return False, field
    return True, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill runtime students and teams into relational tables.")
    parser.add_argument("--team-id", type=int, help="Only backfill one team by id.")
    parser.add_argument("--student-id", type=int, help="Only backfill one student by id.")
    parser.add_argument("--team-limit", type=int, help="Only process the first N team records.")
    parser.add_argument("--student-limit", type=int, help="Only process the first N student records.")
    parser.add_argument("--dry-run", action="store_true", help="Read and validate only, do not write to relational tables.")
    parser.add_argument("--summary", action="store_true", help="Print summary as compact JSON.")
    args = parser.parse_args()

    postgres_store = PostgresStateStore()
    postgres_store.ensure_schema()

    runtime_teams = load_runtime_teams(postgres_store, team_id=args.team_id, limit=args.team_limit)
    runtime_students = load_runtime_students(postgres_store, student_id=args.student_id, limit=args.student_limit)

    processed_teams = 0
    processed_students = 0
    invalid_teams: list[dict[str, Any]] = []
    invalid_students: list[dict[str, Any]] = []

    for team in runtime_teams:
        valid, missing_field = validate_team_payload(team)
        if not valid:
            invalid_teams.append({"id": team.get("id"), "missing_field": missing_field})
            continue
        if not args.dry_run:
            postgres_store.sync_updated_center(team, affected_students=[], operation_log=None)
        processed_teams += 1

    for student in runtime_students:
        valid, missing_field = validate_student_payload(student)
        if not valid:
            invalid_students.append({"id": student.get("id"), "missing_field": missing_field})
            continue
        if not args.dry_run:
            postgres_store.sync_updated_student(student, operation_log=None)
        processed_students += 1

    summary = {
        "database": settings.postgres_db,
        "dry_run": bool(args.dry_run),
        "loaded_runtime_teams": len(runtime_teams),
        "processed_teams": processed_teams,
        "invalid_teams": invalid_teams,
        "loaded_runtime_students": len(runtime_students),
        "processed_students": processed_students,
        "invalid_students": invalid_students,
    }
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False))
        return
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()