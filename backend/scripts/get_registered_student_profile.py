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
        description="Read one registered student's recruitment info by business_key or candidate_no.",
        epilog="Example: python backend/scripts/get_registered_student_profile.py SH20260001",
    )
    parser.add_argument(
        "registration_no",
        help="Business key or candidate number for the recruitment application.",
    )
    return parser


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _load_recruitment_profile(registration_no: str) -> dict[str, Any] | None:
    sql = """
    WITH matched_application AS (
        SELECT
            ra.id,
            ra.portal_student_id,
            ra.plan_id,
            ra.business_key,
            ra.candidate_no,
            ra.student_name,
            ra.first_choice,
            ra.second_choice,
            ra.first_choice_id,
            ra.second_choice_id,
            ra.intended_advisor_user_id,
            ra.intended_advisor_name,
            ra.application_status,
            ra.advisor_screening_status,
            ra.advisor_screening_round,
            ra.first_choice_screening_score,
            ra.second_choice_screening_score,
            ra.first_choice_screening_batch_id,
            ra.second_choice_screening_batch_id,
            ra.initial_screening_status,
            ra.initial_screening_result,
            ra.applied_at,
            ra.created_at,
            ps.full_name AS portal_full_name,
            ps.submitted_at,
            wf.current_node,
            wf.task_status
        FROM dtlms_recruitment_applications ra
        LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
        LEFT JOIN LATERAL (
            SELECT
                MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status
            FROM (
                SELECT DISTINCT ON (hv.name_)
                    hv.name_,
                    hv.text_value_,
                    hv.json_value_
                FROM dtlms_wf_hi_varinst hv
                WHERE hv.proc_inst_id_ = (
                    SELECT ht.proc_inst_id_
                    FROM dtlms_wf_hi_taskinst ht
                    WHERE ht.business_key_ = ra.business_key
                    ORDER BY ht.start_time_ DESC, ht.id_ DESC
                    LIMIT 1
                )
                ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
            ) latest_var
        ) wf ON TRUE
        WHERE ra.is_deleted = FALSE
          AND (
                ra.business_key = %s
             OR ra.candidate_no = %s
          )
        ORDER BY CASE WHEN ra.business_key = %s THEN 0 ELSE 1 END,
                 COALESCE(ra.applied_at, ra.created_at) DESC,
                 ra.id DESC
        LIMIT 1
    )
    SELECT *
    FROM matched_application
    """
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql, (registration_no, registration_no, registration_no))
            row = cur.fetchone()
            if row is None:
                return None

            application = dict(row)
            application_id = int(application["id"])

            cur.execute(
                """
                SELECT
                    evaluator_user_id,
                    evaluator_username,
                    evaluator_name,
                    evaluator_role_code,
                    assessment_result,
                    assessment_comment,
                    assessed_at
                FROM dtlms_background_assessments
                WHERE application_id = %s
                ORDER BY assessed_at ASC, id ASC
                """,
                (application_id,),
            )
            background_assessments = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT
                    screening_round,
                    batch_id,
                    advisor_score,
                    is_passed,
                    screening_status,
                    created_at,
                    updated_at
                FROM dtlms_advisor_screening_items
                WHERE application_id = %s
                ORDER BY screening_round ASC, id ASC
                """,
                (application_id,),
            )
            advisor_screenings = [dict(item) for item in cur.fetchall()]

    first_choice_screening = next((item for item in advisor_screenings if str(item.get("screening_round") or "").strip() == "first_choice"), None)
    second_choice_screening = next((item for item in advisor_screenings if str(item.get("screening_round") or "").strip() == "second_choice"), None)

    return {
        "student_id": application.get("portal_student_id"),
        "student_name": application.get("portal_full_name") or application.get("student_name"),
        "registration_no": application.get("business_key") or application.get("candidate_no"),
        "business_key": application.get("business_key"),
        "candidate_no": application.get("candidate_no"),
        "first_choice": application.get("first_choice"),
        "second_choice": application.get("second_choice"),
        "first_choice_id": application.get("first_choice_id"),
        "second_choice_id": application.get("second_choice_id"),
        "intended_advisor_user_id": application.get("intended_advisor_user_id"),
        "intended_advisor_name": application.get("intended_advisor_name"),
        "flow_status": application.get("current_node") or application.get("task_status") or application.get("application_status"),
        "application_status": application.get("application_status"),
        "advisor_screening_status": application.get("advisor_screening_status"),
        "advisor_screening_round": application.get("advisor_screening_round"),
        "first_choice_screening_score": application.get("first_choice_screening_score"),
        "first_choice_screening_status": application.get("advisor_screening_status") if application.get("advisor_screening_round") in {"first_choice", "second_choice"} else _normalize_text(first_choice_screening.get("screening_status") if first_choice_screening else None),
        "first_choice_screening_round": _normalize_text(first_choice_screening.get("screening_round") if first_choice_screening else None),
        "first_choice_screening_batch_id": first_choice_screening.get("batch_id") if first_choice_screening else None,
        "second_choice_screening_score": application.get("second_choice_screening_score"),
        "second_choice_screening_status": _normalize_text(second_choice_screening.get("screening_status") if second_choice_screening else None),
        "second_choice_screening_round": _normalize_text(second_choice_screening.get("screening_round") if second_choice_screening else None),
        "second_choice_screening_batch_id": second_choice_screening.get("batch_id") if second_choice_screening else None,
        "background_assessments": background_assessments,
        "advisor_screenings": advisor_screenings,
        "portal_submitted_at": application.get("submitted_at"),
        "application_id": application_id,
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    registration_no = _normalize_text(args.registration_no)
    if not registration_no:
        print("[ERROR] registration_no is required.", file=sys.stderr)
        return 1

    try:
        profile = _load_recruitment_profile(registration_no)
    except Exception as exc:
        print(f"[ERROR] Query failed: {exc}", file=sys.stderr)
        return 1

    if profile is None:
        print(f"[ERROR] No recruitment application found for {registration_no}", file=sys.stderr)
        return 2

    print(json.dumps(profile, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())