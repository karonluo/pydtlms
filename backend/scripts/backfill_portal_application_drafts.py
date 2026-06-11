from __future__ import annotations

import argparse
import sys
from pathlib import Path

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill dtlms_portal_students.application_draft from normalized portal application tables.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only count the affected rows and print a preview without updating data.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a short per-row summary while processing.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        with store._connect(args.database) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT ps.id, ra.candidate_no
                    FROM dtlms_portal_students ps
                    JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id
                    WHERE ps.application_draft IS NULL
                      AND ra.is_deleted = FALSE
                    ORDER BY ra.id ASC
                    """
                )
                candidates = [dict(row) for row in cur.fetchall()]

            print(f"[INFO] Database: {args.database}")
            print(f"[INFO] Candidates to inspect: {len(candidates)}")

            if not candidates:
                return 0

            if args.dry_run:
                preview = [item["candidate_no"] for item in candidates[:10]]
                print(f"[INFO] Dry run preview: {preview}")
                return 0

            updated_count = 0
            skipped_count = 0
            with store._connect(args.database) as conn:
                conn.row_factory = dict_row
                with conn.cursor() as cur:
                    for index, candidate in enumerate(candidates, start=1):
                        portal_student_id = int(candidate["id"])
                        student = store.get_portal_student_detail(portal_student_id)
                        draft = student.get("application_draft") if student else None
                        if not isinstance(draft, dict) or not draft:
                            skipped_count += 1
                            if args.summary:
                                print(f"[SKIP] {candidate['candidate_no']} portal_student_id={portal_student_id} no derived draft")
                            continue

                        cur.execute(
                            """
                            UPDATE dtlms_portal_students
                            SET application_draft = %s::jsonb,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                              AND application_draft IS NULL
                            """,
                            (store._json_payload(draft), portal_student_id),
                        )
                        if cur.rowcount > 0:
                            updated_count += 1
                            if args.summary:
                                print(f"[UPDATE] {candidate['candidate_no']} portal_student_id={portal_student_id} draft restored")
                        else:
                            skipped_count += 1
                            if args.summary:
                                print(f"[SKIP] {candidate['candidate_no']} portal_student_id={portal_student_id} already filled")

                        if index % 25 == 0:
                            conn.commit()

                conn.commit()

            print(f"[INFO] Updated rows: {updated_count}")
            print(f"[INFO] Skipped rows: {skipped_count}")
            return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())