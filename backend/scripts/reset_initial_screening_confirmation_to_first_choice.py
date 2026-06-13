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


TARGET_APPLICATION_STATUS = "initial_screening_confirmation"
TARGET_RESET_STATUS = "initial_screening_first"
TARGET_ADVISOR_SCREENING_STATUS = "pending"
TARGET_ADVISOR_SCREENING_ROUND = "first_choice"
TARGET_WORKFLOW_NODE_KEY = "advisor_screening"
TARGET_WORKFLOW_NODE_LABEL = "导师初筛"
TARGET_WORKFLOW_STATUS = "处理中"
TARGET_WORKFLOW_COMMENT = "重新评分回退至导师初筛环节"
TARGET_WORKFLOW_HANDLER_FALLBACK = "导师"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reset recruitment applications stuck in initial_screening_confirmation with no submitted screening timestamps back to first-choice advisor screening.",
        epilog="Example: python backend/scripts/reset_initial_screening_confirmation_to_first_choice.py --apply",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the rows that would be repaired without writing any changes.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write the repair to PostgreSQL.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a per-row summary while processing.",
    )
    return parser


def normalize_text(value: Any) -> str:
    return str(value or "").strip()


def load_target_rows(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ra.id AS application_id,
                    ra.plan_id,
                    ra.business_key,
                    ra.candidate_no,
                    ra.student_name,
                    ra.application_status,
                    ra.advisor_screening_status,
                    ra.advisor_screening_round,
                    ra.first_choice,
                    ra.second_choice,
                    ra.first_choice_id,
                    ra.second_choice_id,
                    ra.first_choice_screening_batch_id,
                    ra.second_choice_screening_batch_id,
                    ra.first_choice_screening_submitted_at,
                    ra.second_choice_screening_submitted_at,
                    ra.first_choice_screening_score,
                    ra.second_choice_screening_score,
                    ra.initial_screening_status,
                    ra.initial_screening_result,
                    ra.initial_screening_confirmed_at,
                    ra.initial_screening_confirmer_username,
                    ra.initial_screening_confirmer_name,
                    ra.initial_screening_notification_status,
                    ra.initial_screening_notification_sent_at,
                    ra.next_stage_name,
                    ra.updated_at
                FROM dtlms_recruitment_applications AS ra
                WHERE ra.application_status = %s
                  AND ra.first_choice_screening_submitted_at IS NULL
                  AND ra.second_choice_screening_submitted_at IS NULL
                  AND ra.is_deleted = FALSE
                ORDER BY ra.id ASC
                """,
                (TARGET_APPLICATION_STATUS,),
            )
            return [dict(row) for row in cur.fetchall()]


def load_workflow_task_map(store: PostgresStateStore) -> dict[str, dict[str, Any]]:
    try:
        workflow_tasks = store.load_workflow_task_state()
    except Exception as exc:
        print(f"[WARN] Failed to load workflow task snapshots: {exc}")
        return {}

    workflow_task_map: dict[str, dict[str, Any]] = {}
    for task in workflow_tasks:
        business_key = normalize_text(task.get("business_key"))
        if not business_key:
            continue
        workflow_task_map.setdefault(business_key, task)
    return workflow_task_map


def build_application_payload(row: dict[str, Any]) -> dict[str, Any]:
    payload = dict(row)
    payload.update(
        {
            "application_status": TARGET_RESET_STATUS,
            "advisor_screening_status": TARGET_ADVISOR_SCREENING_STATUS,
            "advisor_screening_round": TARGET_ADVISOR_SCREENING_ROUND,
            "first_choice_screening_batch_id": None,
            "second_choice_screening_batch_id": None,
            "first_choice_screening_submitted_at": None,
            "second_choice_screening_submitted_at": None,
            "first_choice_screening_score": None,
            "second_choice_screening_score": None,
            "initial_screening_status": None,
            "initial_screening_result": None,
            "initial_screening_confirmed_at": None,
            "initial_screening_confirmer_username": None,
            "initial_screening_confirmer_name": None,
            "initial_screening_notification_status": None,
            "initial_screening_notification_sent_at": None,
            "next_stage_name": None,
        }
    )
    return payload


def build_workflow_payload(row: dict[str, Any], workflow_task: dict[str, Any]) -> dict[str, Any]:
    handler = normalize_text(row.get("first_choice")) or normalize_text(row.get("second_choice")) or normalize_text(row.get("intended_advisor_name")) or TARGET_WORKFLOW_HANDLER_FALLBACK
    payload = dict(workflow_task)
    payload.update(
        {
            "node_key": TARGET_WORKFLOW_NODE_KEY,
            "current_node": TARGET_WORKFLOW_NODE_LABEL,
            "status": TARGET_WORKFLOW_STATUS,
            "current_handler": handler,
            "latest_comment": TARGET_WORKFLOW_COMMENT,
        }
    )
    return payload


def repair_row(store: PostgresStateStore, database_name: str, row: dict[str, Any], workflow_task: dict[str, Any] | None) -> None:
    application_payload = build_application_payload(row)

    with store._connect(database_name) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE dtlms_recruitment_applications
                SET application_status = %s,
                    advisor_screening_status = %s,
                    advisor_screening_round = %s,
                    first_choice_screening_batch_id = NULL,
                    second_choice_screening_batch_id = NULL,
                    first_choice_screening_submitted_at = NULL,
                    second_choice_screening_submitted_at = NULL,
                    first_choice_screening_score = NULL,
                    second_choice_screening_score = NULL,
                    initial_screening_status = NULL,
                    initial_screening_result = NULL,
                    initial_screening_confirmed_at = NULL,
                    initial_screening_confirmer_username = NULL,
                    initial_screening_confirmer_name = NULL,
                    initial_screening_notification_status = NULL,
                    initial_screening_notification_sent_at = NULL,
                    next_stage_name = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND is_deleted = FALSE
                """,
                (
                    TARGET_RESET_STATUS,
                    TARGET_ADVISOR_SCREENING_STATUS,
                    TARGET_ADVISOR_SCREENING_ROUND,
                    int(row["application_id"]),
                ),
            )
            cur.execute(
                "DELETE FROM dtlms_initial_screening_confirmations WHERE application_id = %s",
                (int(row["application_id"]),),
            )
            cur.execute(
                "DELETE FROM dtlms_initial_screening_notifications WHERE application_id = %s",
                (int(row["application_id"]),),
            )
        conn.commit()

    if workflow_task is not None:
        store.sync_workflow_task(build_workflow_payload(row, workflow_task))


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.apply and args.dry_run:
        print("[ERROR] --apply and --dry-run cannot be used together.", file=sys.stderr)
        return 1

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        try:
            target_rows = load_target_rows(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to load target rows: {exc}", file=sys.stderr)
            return 1

        try:
            workflow_task_map = load_workflow_task_map(store)
        except Exception as exc:
            print(f"[WARN] Workflow task snapshots were not loaded: {exc}")
            workflow_task_map = {}

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Matched applications: {len(target_rows)}")

        for row in target_rows:
            business_key = normalize_text(row.get("business_key"))
            workflow_task = workflow_task_map.get(business_key)
            if args.summary or args.dry_run or not args.apply:
                print(
                    f"[PLAN] application_id={int(row['application_id'])} candidate_no={normalize_text(row.get('candidate_no'))} "
                    f"student_name={normalize_text(row.get('student_name'))} business_key={business_key} "
                    f"workflow_task_found={workflow_task is not None}"
                )

        if args.dry_run or not args.apply:
            print("[INFO] Dry run completed. No changes were written.")
            if not args.apply:
                print("[INFO] Re-run with --apply to execute the repair.")
            return 0

        success_count = 0
        fallback_count = 0
        failed_rows = 0

        for row in target_rows:
            business_key = normalize_text(row.get("business_key"))
            workflow_task = workflow_task_map.get(business_key)
            try:
                repair_row(store, args.database, row, workflow_task)
                if workflow_task is not None:
                    success_count += 1
                else:
                    fallback_count += 1
                print(
                    f"[OK] application_id={int(row['application_id'])} candidate_no={normalize_text(row.get('candidate_no'))} "
                    f"workflow_task_found={workflow_task is not None}"
                )
            except Exception as exc:
                failed_rows += 1
                print(
                    f"[ERROR] application_id={int(row['application_id'])} candidate_no={normalize_text(row.get('candidate_no'))} failed: {exc}",
                    file=sys.stderr,
                )

        print(f"[INFO] Workflow-backed repairs: {success_count}")
        print(f"[INFO] Direct fallback repairs: {fallback_count}")
        print(f"[INFO] Failed rows: {failed_rows}")
        return 0 if failed_rows == 0 else 1
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())