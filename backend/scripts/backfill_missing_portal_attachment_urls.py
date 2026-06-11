from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DEFAULT_ATTACHMENTS_ROOT = REPO_ROOT / "frontend" / "public" / "portal-attachments" / "uploads"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


STANDARD_ATTACHMENT_PREFIX = "/api/v1/portal/attachments/"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill missing resume and supporting-material attachment URLs from student-{id}/resume and student-{id}/supporting_material directories.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--attachments-root",
        default=str(DEFAULT_ATTACHMENTS_ROOT),
        help=f"Root directory for portal attachment files. Default: {DEFAULT_ATTACHMENTS_ROOT}",
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
        help="Print a short per-student summary while processing.",
    )
    parser.add_argument(
        "--student-id",
        type=int,
        default=None,
        help="Only process the specified portal student ID. If omitted, process all matching students.",
    )
    parser.add_argument(
        "--english-only",
        action="store_true",
        help="Only backfill English certificate URLs and the reconstructed JSONB draft.",
    )
    parser.add_argument(
        "--resume-only",
        action="store_true",
        help="Only backfill resume attachment URLs when the resume URL is empty.",
    )
    return parser


def resolve_attachments_root(raw_value: str) -> Path:
    attachments_root = Path(raw_value).expanduser()
    if not attachments_root.is_absolute():
        attachments_root = (Path.cwd() / attachments_root).resolve()
    else:
        attachments_root = attachments_root.resolve()
    if not attachments_root.exists():
        raise FileNotFoundError(f"Attachments root not found: {attachments_root}")
    if not attachments_root.is_dir():
        raise FileNotFoundError(f"Attachments root is not a directory: {attachments_root}")
    return attachments_root


def build_public_attachment_url(attachments_root: Path, file_path: Path) -> str:
    relative_path = file_path.resolve().relative_to(attachments_root.resolve())
    return STANDARD_ATTACHMENT_PREFIX + relative_path.as_posix()

def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def get_file_created_timestamp(file_path: Path) -> float:
    stat_result = file_path.stat()
    birth_time = getattr(stat_result, "st_birthtime", None)
    if birth_time is not None:
        return float(birth_time)
    return float(getattr(stat_result, "st_ctime", stat_result.st_mtime))


def list_files_sorted_by_time(directory: Path) -> list[Path]:
    if not directory.exists() or not directory.is_dir():
        return []
    return sorted(
        (item for item in directory.iterdir() if item.is_file()),
        key=lambda item: (-get_file_created_timestamp(item), item.name.lower()),
    )


def student_attachment_directory(attachments_root: Path, student_id: int, category: str) -> Path:
    return (attachments_root / f"student-{student_id}" / category).resolve()


def latest_attachment_file(attachments_root: Path, student_id: int, category: str) -> Path | None:
    files = list_files_sorted_by_time(student_attachment_directory(attachments_root, student_id, category))
    return files[0] if files else None


def list_english_certificate_files(attachments_root: Path, student_id: int) -> list[Path]:
    return list_files_sorted_by_time(student_attachment_directory(attachments_root, student_id, "english_certificate"))


def build_file_match_key(file_candidate: tuple[Any, Path], row_timestamp: float) -> tuple[float, float, str]:
    file_timestamp = float(file_candidate[0])
    file_path = file_candidate[1]
    return abs(file_timestamp - row_timestamp), file_timestamp, file_path.name.lower()


def is_blank_value(value: Any) -> bool:
    return value in (None, "", [], {})


def merge_missing_values(base_value: Any, overlay_value: Any) -> Any:
    if is_blank_value(base_value):
        return overlay_value
    if isinstance(base_value, dict) and isinstance(overlay_value, dict):
        merged = dict(base_value)
        for key, value in overlay_value.items():
            merged[key] = merge_missing_values(merged.get(key), value)
        return merged
    if isinstance(base_value, list):
        return base_value if base_value else overlay_value
    return base_value


def to_timestamp(value: Any) -> float | None:
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=timezone.utc).timestamp()
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed.timestamp()
    return None


def load_candidates(
    store: PostgresStateStore,
    database_name: str,
    student_id: int | None = None,
    english_only: bool = False,
    resume_only: bool = False,
) -> list[dict[str, Any]]:
    if english_only:
        attachment_condition_sql = """
                  AND EXISTS (
                        SELECT 1
                        FROM dtlms_portal_application_english_proficiencies ep
                        WHERE ep.application_id = la.application_id
                          AND COALESCE(BTRIM(ep.certificate_attachment_url), '') = ''
                    )
        """
        draft_condition_sql = ""
    elif resume_only:
        attachment_condition_sql = """
                  AND COALESCE(BTRIM(psm.resume_attachment_url), '') = ''
        """
        draft_condition_sql = ""
    elif resume_only:
        attachment_condition_sql = """
                  AND COALESCE(BTRIM(psm.resume_attachment_url), '') = ''
        """
        draft_condition_sql = ""
    else:
        attachment_condition_sql = """
                  AND (
                        COALESCE(BTRIM(psm.resume_attachment_url), '') = ''
                     OR COALESCE(BTRIM(psm.supporting_material_attachment_url), '') = ''
                     OR EXISTS (
                            SELECT 1
                            FROM dtlms_portal_application_english_proficiencies ep
                            WHERE ep.application_id = la.application_id
                              AND COALESCE(BTRIM(ep.certificate_attachment_url), '') = ''
                        )
                  )
        """
        draft_condition_sql = """
                    AND (
                        ps.application_draft IS NULL
                       OR ps.application_draft = '{{}}'::jsonb
                       OR NOT (ps.application_draft ? 'personal_statement')
                       OR NOT (ps.application_draft ? 'preferences')
                       OR NOT (ps.application_draft ? 'education_experiences')
                       OR NOT (ps.application_draft ? 'practice_experiences')
                       OR NOT (ps.application_draft ? 'english_proficiencies')
                       OR NOT (ps.application_draft ? 'family_members')
                       OR NOT (ps.application_draft ? 'achievement_records')
                       OR NOT (ps.application_draft ? 'declaration')
                    )
        """
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            query = f"""
                WITH latest_applications AS (
                    SELECT DISTINCT ON (ps.id)
                        ps.id AS student_id,
                        ps.full_name AS student_name,
                        ra.id AS application_id,
                        ra.candidate_no,
                        ra.application_status,
                        COALESCE(ps.submitted_at, ra.applied_at) AS submitted_at,
                        CASE
                            WHEN COALESCE(ra.application_status, '') IN ('returned', '驳回重填') THEN '驳回重填'
                            WHEN COALESCE(ps.submitted_at, ra.applied_at) IS NOT NULL THEN '已填写报名'
                            ELSE '未填写报名'
                        END AS application_form_status
                    FROM dtlms_portal_students ps
                    JOIN dtlms_recruitment_applications ra ON ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                    ORDER BY
                        ps.id,
                        CASE WHEN ra.plan_id = ps.selected_plan_id THEN 0 ELSE 1 END,
                        COALESCE(ra.applied_at, ra.created_at) DESC,
                        ra.id DESC
                )
                SELECT
                    la.student_id,
                    la.student_name,
                    la.application_id,
                    la.candidate_no,
                    la.application_status,
                    la.application_form_status,
                    ps.application_draft,
                    psm.resume_attachment_url,
                    psm.supporting_material_attachment_url
                FROM latest_applications la
                JOIN dtlms_portal_students ps ON ps.id = la.student_id
                JOIN dtlms_portal_application_personal_statements psm ON psm.application_id = la.application_id
                WHERE la.application_form_status IN ('已填写报名', '驳回重填')
                  AND COALESCE(BTRIM(la.candidate_no), '') <> ''
                                    AND (%s::bigint IS NULL OR la.student_id = %s::bigint)
{draft_condition_sql}
{attachment_condition_sql}
                ORDER BY la.student_id ASC, la.application_id ASC
                """
            cur.execute(
                query,
                (student_id, student_id),
            )
            return [dict(row) for row in cur.fetchall()]


def load_english_certificate_rows(
    store: PostgresStateStore,
    database_name: str,
    application_id: int,
) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    exam_name,
                    score_text,
                    certificate_attachment_url,
                    created_at,
                    updated_at
                FROM dtlms_portal_application_english_proficiencies
                WHERE application_id = %s
                  AND COALESCE(BTRIM(certificate_attachment_url), '') = ''
                ORDER BY created_at ASC, updated_at ASC, id ASC
                """,
                (int(application_id),),
            )
            return [dict(row) for row in cur.fetchall()]


def load_application_draft_from_tables(
    store: PostgresStateStore,
    database_name: str,
    student_id: int,
    application_id: int,
) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ps.selected_plan_id,
                    ps.selected_advisor_user_id,
                    ps.selected_advisor_name,
                    ps.submitted_at,
                    ps.signed_agreement,
                    ps.education_experience,
                    ps.practice_experience,
                    ps.family_info,
                    ps.recommendation_notes,
                    ps.personal_statement_text,
                    ra.plan_id,
                    ra.source_channel,
                    ra.source_channel_other,
                    ra.applied_at,
                    ra.application_status,
                    ra.first_choice,
                    ra.second_choice,
                    ra.intended_advisor_user_id,
                    ra.intended_advisor_name,
                    ra.material_list_attachment
                FROM dtlms_portal_students ps
                LEFT JOIN dtlms_recruitment_applications ra ON ra.id = %s AND ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
                WHERE ps.id = %s
                LIMIT 1
                """,
                (int(application_id), int(student_id)),
            )
            base_row = cur.fetchone()
            if not base_row:
                return None

            cur.execute(
                """
                SELECT preference_order, advisor_user_id, advisor_name, is_optional
                FROM dtlms_portal_application_preferences
                WHERE application_id = %s
                ORDER BY preference_order ASC, id ASC
                """,
                (int(application_id),),
            )
            preferences = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT sort_order, education_stage, start_month, end_month, school_name, major_name,
                       average_score, gpa, ranking, verifier_name, verifier_phone,
                       transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                FROM dtlms_portal_application_education_experiences
                WHERE application_id = %s
                ORDER BY sort_order ASC, id ASC
                """,
                (int(application_id),),
            )
            education_experiences = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                       verifier_name, verifier_phone
                FROM dtlms_portal_application_practice_experiences
                WHERE application_id = %s
                ORDER BY id ASC
                """,
                (int(application_id),),
            )
            practice_experiences = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT exam_name, score_text, certificate_attachment_url
                FROM dtlms_portal_application_english_proficiencies
                WHERE application_id = %s
                ORDER BY created_at ASC, updated_at ASC, id ASC
                """,
                (int(application_id),),
            )
            english_proficiencies = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT member_name, relation_type, employer_name, job_title, contact_phone
                FROM dtlms_portal_application_family_members
                WHERE application_id = %s
                ORDER BY id ASC
                """,
                (int(application_id),),
            )
            family_members = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT id, achievement_type, paper_title, author_order, journal_or_conference,
                       publish_or_index_month, achievement_month, award_name, award_rank,
                       award_certificate_attachment_url, awarding_organization, award_level,
                       award_year, description_text, responsibility_text
                FROM dtlms_portal_application_achievement_records
                WHERE application_id = %s
                ORDER BY id ASC
                """,
                (int(application_id),),
            )
            achievement_rows = [dict(item) for item in cur.fetchall()]

            cur.execute(
                """
                SELECT owner_type, owner_id, attachment_category, file_name, file_url
                FROM dtlms_portal_application_attachments
                WHERE application_id = %s
                ORDER BY id ASC
                """,
                (int(application_id),),
            )
            attachment_rows = [dict(item) for item in cur.fetchall()]

            achievement_records: list[dict[str, Any]] = []
            for achievement in achievement_rows:
                achievement_id = int(achievement.get("id") or 0)
                achievement["award_certificate_attachment_name"] = next(
                    (
                        str(item.get("file_name") or "")
                        for item in attachment_rows
                        if str(item.get("owner_type") or "") == "achievement_record"
                        and int(item.get("owner_id") or 0) == achievement_id
                        and str(item.get("attachment_category") or "") == "achievement_award_certificate"
                        and item.get("file_name")
                    ),
                    None,
                )
                achievement.pop("id", None)
                achievement_records.append(achievement)

            personal_statement_row = None
            cur.execute(
                """
                SELECT personal_statement_text, growth_experience_text, program_application_reason_text,
                       career_plan_text, resume_attachment_url, supporting_material_attachment_url,
                       ai_problem_statement, ai_industry_opinion
                FROM dtlms_portal_application_personal_statements
                WHERE application_id = %s
                """,
                (int(application_id),),
            )
            personal_statement_row = cur.fetchone()

            cur.execute(
                """
                SELECT has_read_declaration, declaration_text, progress_snapshot
                FROM dtlms_portal_application_declarations
                WHERE application_id = %s
                """,
                (int(application_id),),
            )
            declaration_row = cur.fetchone()

            personal_statement: dict[str, Any] = dict(personal_statement_row) if personal_statement_row else {}
            if not personal_statement.get("resume_attachment_url"):
                personal_statement["resume_attachment_url"] = next(
                    (
                        str(item.get("file_url") or "")
                        for item in attachment_rows
                        if str(item.get("owner_type") or "") == "personal_statement"
                        and int(item.get("owner_id") or 0) == int(application_id)
                        and str(item.get("attachment_category") or "") == "resume"
                        and item.get("file_url")
                    ),
                    None,
                )
            if not personal_statement.get("supporting_material_attachment_url"):
                personal_statement["supporting_material_attachment_url"] = next(
                    (
                        str(item.get("file_url") or "")
                        for item in attachment_rows
                        if str(item.get("owner_type") or "") == "portal_application"
                        and int(item.get("owner_id") or 0) == int(application_id)
                        and str(item.get("attachment_category") or "") == "materials"
                        and item.get("file_url")
                    ),
                    None,
                )

            return {
                "selected_plan_id": int(base_row.get("plan_id") or base_row.get("selected_plan_id") or 0) or None,
                "source_channel": base_row.get("source_channel"),
                "source_channel_other": base_row.get("source_channel_other"),
                "preferences": preferences,
                "education_experiences": education_experiences,
                "practice_experiences": practice_experiences,
                "english_proficiencies": english_proficiencies,
                "family_members": family_members,
                "achievement_records": achievement_records,
                "personal_statement": personal_statement,
                "declaration": dict(declaration_row) if declaration_row else {"has_read_declaration": bool(base_row.get("signed_agreement"))},
                "submitted_at": None if str(base_row.get("application_status") or "").strip() in {"returned", "驳回重填"} else base_row.get("applied_at") or base_row.get("submitted_at"),
            }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        attachments_root = resolve_attachments_root(args.attachments_root)
    except Exception as exc:
        print(f"[ERROR] Failed to resolve attachments root: {exc}", file=sys.stderr)
        return 1

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        try:
            candidate_rows = load_candidates(store, args.database, args.student_id, args.english_only, args.resume_only)
        except Exception as exc:
            print(f"[ERROR] Failed to load candidate rows: {exc}", file=sys.stderr)
            return 1

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Attachments root: {attachments_root}")
        print(f"[INFO] Candidates to inspect: {len(candidate_rows)}")
        if args.english_only:
            mode_label = "english-only"
        elif args.resume_only:
            mode_label = "resume-only"
        else:
            mode_label = "full"
        print(f"[INFO] Mode: {mode_label}")

        if not candidate_rows:
            print("[INFO] No portal students need resume/supporting-material URL backfill.")
            return 0

        planned_updates: list[dict[str, Any]] = []
        skipped_students = 0

        for row in candidate_rows:
            student_id = int(row["student_id"])
            student_name = str(row.get("student_name") or "")
            application_id = int(row["application_id"])
            current_application_draft = row.get("application_draft") if isinstance(row.get("application_draft"), dict) else None

            resume_url = str(row.get("resume_attachment_url") or "").strip()
            supporting_url = str(row.get("supporting_material_attachment_url") or "").strip()
            resume_file = None if args.english_only else latest_attachment_file(attachments_root, student_id, "resume") if not resume_url else None

            if args.resume_only:
                supporting_file = None
                english_rows: list[dict[str, Any]] = []
                english_files: list[Path] = []
                db_application_draft = None
            else:
                supporting_file = None if args.english_only else latest_attachment_file(attachments_root, student_id, "supporting_material") if not supporting_url else None
                english_rows = load_english_certificate_rows(store, args.database, application_id)
                english_files = list_english_certificate_files(attachments_root, student_id) if english_rows else []
                db_application_draft = load_application_draft_from_tables(store, args.database, student_id, application_id)

            if (not resume_file and not supporting_file and not english_files and db_application_draft is None):
                skipped_students += 1
                if args.summary:
                    print(
                        f"[SKIP] student_id={student_id} application_id={application_id} name={student_name} no files in resume/supporting_material/english_certificate and no draft data"
                    )
                continue

            update_item: dict[str, Any] = {
                "student_id": student_id,
                "student_name": student_name,
                "application_id": application_id,
            }

            if not args.english_only and not resume_url and resume_file is not None:
                update_item["resume_attachment_url"] = build_public_attachment_url(attachments_root, resume_file)
                update_item["resume_file_name"] = resume_file.name

            if not args.english_only and not args.resume_only and not supporting_url and supporting_file is not None:
                update_item["supporting_material_attachment_url"] = build_public_attachment_url(attachments_root, supporting_file)
                update_item["supporting_file_name"] = supporting_file.name

            if not args.resume_only and english_rows and english_files:
                ordered_english_rows = sorted(
                    english_rows,
                    key=lambda english_row: (
                        to_timestamp(english_row.get("created_at")) or to_timestamp(english_row.get("updated_at")) or float("inf"),
                        int(english_row.get("id") or 0),
                    ),
                )
                file_candidates = [
                    (get_file_created_timestamp(file_path), file_path)
                    for file_path in english_files
                ]
                matched_english_urls: list[str | None] = [None] * len(ordered_english_rows)
                english_certificate_updates: list[dict[str, Any]] = []

                for row_index, english_row in enumerate(ordered_english_rows):
                    if not file_candidates:
                        break
                    row_timestamp = to_timestamp(english_row.get("created_at")) or to_timestamp(english_row.get("updated_at")) or file_candidates[0][0]
                    best_index = min(
                        range(len(file_candidates)),
                        key=lambda index: build_file_match_key(file_candidates[index], float(row_timestamp)),
                    )
                    _, file_path = file_candidates.pop(best_index)
                    public_url = build_public_attachment_url(attachments_root, file_path)
                    matched_english_urls[row_index] = public_url
                    english_certificate_updates.append(
                        {
                            "english_proficiency_id": int(english_row["id"]),
                            "certificate_attachment_url": public_url,
                            "file_name": file_path.name,
                        }
                    )

                if english_certificate_updates:
                    update_item["english_certificate_updates"] = english_certificate_updates
                    if db_application_draft is not None:
                        draft_english_rows = db_application_draft.get("english_proficiencies")
                        if isinstance(draft_english_rows, list):
                            for index, public_url in enumerate(matched_english_urls):
                                if public_url and index < len(draft_english_rows) and isinstance(draft_english_rows[index], dict):
                                    draft_english_rows[index]["certificate_attachment_url"] = public_url

            if not args.resume_only and db_application_draft is not None:
                merged_draft = merge_missing_values(current_application_draft or {}, db_application_draft)
                if merged_draft != current_application_draft:
                    update_item["application_draft"] = merged_draft

            if len(update_item) > 3:
                planned_updates.append(update_item)
                if args.summary:
                    print(
                        f"[PLAN] student_id={student_id} application_id={application_id} "
                        f"resume={'yes' if 'resume_attachment_url' in update_item else 'no'} "
                        f"supporting={'yes' if 'supporting_material_attachment_url' in update_item else 'no'} "
                        f"english={'yes' if 'english_certificate_updates' in update_item else 'no'} "
                        f"draft={'yes' if 'application_draft' in update_item else 'no'}"
                    )

        print(f"[INFO] Planned updates: {len(planned_updates)}")
        print(f"[INFO] Skipped students: {skipped_students}")

        if args.dry_run or not args.apply:
            print("[INFO] Dry run completed. No changes were written.")
            if not args.apply:
                print("[INFO] Re-run with --apply to persist updates.")
            return 0

        updated_resume = 0
        updated_supporting = 0
        updated_english = 0
        updated_draft = 0
        with store._connect(args.database) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                for item in planned_updates:
                    application_id = int(item["application_id"])

                    if "resume_attachment_url" in item:
                        cur.execute(
                            """
                            UPDATE dtlms_portal_application_personal_statements
                            SET resume_attachment_url = %s
                            WHERE application_id = %s
                              AND COALESCE(BTRIM(resume_attachment_url), '') = ''
                            """,
                            (item["resume_attachment_url"], application_id),
                        )
                        if cur.rowcount > 0:
                            updated_resume += 1
                            if args.summary:
                                print(
                                    f"[UPDATE] student_id={item['student_id']} application_id={application_id} resume={item['resume_file_name']}"
                                )

                    if "supporting_material_attachment_url" in item:
                        cur.execute(
                            """
                            UPDATE dtlms_portal_application_personal_statements
                            SET supporting_material_attachment_url = %s
                            WHERE application_id = %s
                              AND COALESCE(BTRIM(supporting_material_attachment_url), '') = ''
                            """,
                            (item["supporting_material_attachment_url"], application_id),
                        )
                        if cur.rowcount > 0:
                            updated_supporting += 1
                            if args.summary:
                                print(
                                    f"[UPDATE] student_id={item['student_id']} application_id={application_id} supporting={item['supporting_file_name']}"
                                )

                    for english_update in item.get("english_certificate_updates", []):
                        cur.execute(
                            """
                            UPDATE dtlms_portal_application_english_proficiencies
                            SET certificate_attachment_url = %s
                            WHERE id = %s
                              AND COALESCE(BTRIM(certificate_attachment_url), '') = ''
                            """,
                            (english_update["certificate_attachment_url"], int(english_update["english_proficiency_id"])),
                        )
                        if cur.rowcount > 0:
                            updated_english += 1
                            if args.summary:
                                print(
                                    f"[UPDATE] student_id={item['student_id']} application_id={application_id} english={english_update['file_name']}"
                                )

                    if "application_draft" in item:
                        cur.execute(
                            """
                            UPDATE dtlms_portal_students
                            SET application_draft = %s::jsonb
                            WHERE id = %s
                              AND (
                                  application_draft IS NULL
                                  OR application_draft = '{}'::jsonb
                                  OR NOT (application_draft @> %s::jsonb)
                              )
                            """,
                            (
                                json.dumps(item["application_draft"], ensure_ascii=False, default=json_default),
                                int(item["student_id"]),
                                json.dumps(item["application_draft"], ensure_ascii=False, default=json_default),
                            ),
                        )
                        if cur.rowcount > 0:
                            updated_draft += 1
                            if args.summary:
                                print(f"[UPDATE] student_id={item['student_id']} application_id={application_id} application_draft=merged")

            conn.commit()

        print(f"[INFO] Updated resume rows: {updated_resume}")
        print(f"[INFO] Updated supporting-material rows: {updated_supporting}")
        print(f"[INFO] Updated english-certificate rows: {updated_english}")
        print(f"[INFO] Updated application_draft rows: {updated_draft}")
        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())
