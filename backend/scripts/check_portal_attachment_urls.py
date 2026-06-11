from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DEFAULT_ATTACHMENTS_ROOT = REPO_ROOT / "frontend" / "public" / "portal-attachments" / "uploads"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


STANDARD_ATTACHMENT_PREFIX = "/api/v1/portal/attachments/"
LEGACY_ATTACHMENT_PREFIX = "/portal-attachments/uploads/"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report resume, supporting material, and English certificate attachment URLs for a portal student.",
    )
    parser.add_argument(
        "candidate_no",
        help="Student application number, for example SH20271088.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--attachments-root",
        default=str(DEFAULT_ATTACHMENTS_ROOT),
        help=f"Root directory for portal attachment files. Defaults to: {DEFAULT_ATTACHMENTS_ROOT}",
    )
    return parser


def fetch_latest_application(store: PostgresStateStore, database_name: str, candidate_no: str) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ra.id AS application_id,
                    ra.portal_student_id,
                    ra.candidate_no,
                    ra.application_status,
                    ra.applied_at,
                    ps.full_name AS student_name
                FROM dtlms_recruitment_applications ra
                JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
                WHERE ra.is_deleted = FALSE
                  AND ra.candidate_no = %s
                ORDER BY CASE WHEN ra.plan_id = ps.selected_plan_id THEN 0 ELSE 1 END,
                         COALESCE(ra.applied_at, ra.created_at) DESC,
                         ra.id DESC
                LIMIT 1
                """,
                (candidate_no,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def fetch_personal_statement(store: PostgresStateStore, database_name: str, application_id: int) -> dict[str, Any] | None:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    personal_statement_text,
                    resume_attachment_url,
                    supporting_material_attachment_url
                FROM dtlms_portal_application_personal_statements
                WHERE application_id = %s
                """,
                (application_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def fetch_english_proficiencies(store: PostgresStateStore, database_name: str, application_id: int) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    exam_name,
                    score_text,
                    certificate_attachment_url
                FROM dtlms_portal_application_english_proficiencies
                WHERE application_id = %s
                ORDER BY id ASC
                """,
                (application_id,),
            )
            return [dict(row) for row in cur.fetchall()]


def resolve_attachments_root(raw_value: str) -> Path:
    attachments_root = Path(raw_value).expanduser()
    if not attachments_root.is_absolute():
        attachments_root = (Path.cwd() / attachments_root).resolve()
    else:
        attachments_root = attachments_root.resolve()
    return attachments_root


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


def student_attachment_directory(attachments_root: Path, student_id: int | None, category: str) -> Path | None:
    if student_id is None:
        return None
    return (attachments_root / f"student-{student_id}" / category).resolve()


def url_to_physical_directory(attachments_root: Path, attachment_url: str | None) -> Path | None:
    normalized_url = str(attachment_url or "").strip()
    if not normalized_url:
        return None
    parsed_path = urlsplit(normalized_url).path.strip()
    if parsed_path.startswith(STANDARD_ATTACHMENT_PREFIX):
        relative_path = parsed_path[len(STANDARD_ATTACHMENT_PREFIX):].lstrip("/")
    else:
        if parsed_path.startswith(LEGACY_ATTACHMENT_PREFIX):
            relative_path = parsed_path[len(LEGACY_ATTACHMENT_PREFIX):].lstrip("/")
        else:
            return None
    if not relative_path:
        return None
    return (attachments_root / Path(relative_path).parent).resolve()


def print_physical_file_report(
    label: str,
    attachments_root: Path,
    attachment_url: str | None,
    student_id: int | None,
    category: str,
) -> None:
    physical_directory = url_to_physical_directory(attachments_root, attachment_url)
    directory_source = "url"
    if physical_directory is None:
        physical_directory = student_attachment_directory(attachments_root, student_id, category)
        directory_source = "student_directory"

    if physical_directory is None:
        print(f"- {label}: missing url mapping")
        print("  physical_directory: (unresolved)")
        print("  exists: no")
        print("  latest_file: (empty)")
        print("  directory_files: (none)")
        return

    files = list_files_sorted_by_time(physical_directory)
    latest_file = files[0] if files else None
    print(f"- {label}: {'present' if is_present(attachment_url) else 'missing url; checked student directory'}")
    print(f"  url: {str(attachment_url or '').strip() or '(empty)'}")
    print(f"  directory_source: {directory_source}")
    print(f"  physical_directory: {physical_directory}")
    print(f"  exists: {'yes' if physical_directory.exists() and physical_directory.is_dir() else 'no'}")
    if latest_file is None:
        print("  latest_file: (missing)")
    else:
        print(f"  latest_file: {latest_file.name}")
        print(f"  latest_file_url: {STANDARD_ATTACHMENT_PREFIX}{latest_file.relative_to(attachments_root).as_posix()}")
    if files:
        print("  directory_files:")
        for file_path in files:
            print(f"    - {file_path.name}")
    else:
        print("  directory_files: (none)")


def is_present(value: Any) -> bool:
    return bool(str(value or "").strip())


def print_field(label: str, value: Any) -> None:
    text = str(value or "").strip()
    status = "present" if text else "missing"
    print(f"- {label}: {status}")
    print(f"  value: {text or '(empty)'}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    candidate_no = str(args.candidate_no or "").strip()
    if not candidate_no:
        print("[ERROR] candidate_no is required", file=sys.stderr)
        return 1

    try:
        attachments_root = resolve_attachments_root(args.attachments_root)
    except Exception as exc:
        print(f"[ERROR] Failed to resolve attachments root: {exc}", file=sys.stderr)
        return 1

    original_database = settings.postgres_db
    settings.postgres_db = args.database

    store = PostgresStateStore()
    try:
        try:
            latest_application = fetch_latest_application(store, args.database, candidate_no)
        except Exception as exc:
            print(f"[ERROR] Failed to load latest application: {exc}", file=sys.stderr)
            return 1

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Candidate no: {candidate_no}")
        print(f"[INFO] Attachments root: {attachments_root}")

        if not latest_application:
            print("[WARN] No active recruitment application found for this candidate number.")
            return 0

        application_id = int(latest_application["application_id"])
        print(f"[INFO] Student name: {latest_application.get('student_name') or '(unknown)'}")
        print(f"[INFO] Student id: {latest_application.get('portal_student_id')}")
        print(f"[INFO] Application id: {application_id}")
        print(f"[INFO] Application status: {latest_application.get('application_status') or '(empty)'}")

        try:
            personal_statement = fetch_personal_statement(store, args.database, application_id)
        except Exception as exc:
            print(f"[ERROR] Failed to load personal statement: {exc}", file=sys.stderr)
            return 1

        print("[SECTION] Personal Statement Attachments")
        if personal_statement is None:
            print("- row: missing")
        else:
            print_field("resume_attachment_url", personal_statement.get("resume_attachment_url"))
            print_physical_file_report(
                "resume_attachment_file",
                attachments_root,
                personal_statement.get("resume_attachment_url"),
                int(latest_application.get("portal_student_id") or 0) or None,
                "resume",
            )
            print_field("supporting_material_attachment_url", personal_statement.get("supporting_material_attachment_url"))
            print_physical_file_report(
                "supporting_material_attachment_file",
                attachments_root,
                personal_statement.get("supporting_material_attachment_url"),
                int(latest_application.get("portal_student_id") or 0) or None,
                "supporting_material",
            )

        try:
            english_rows = fetch_english_proficiencies(store, args.database, application_id)
        except Exception as exc:
            print(f"[ERROR] Failed to load English proficiencies: {exc}", file=sys.stderr)
            return 1

        print("[SECTION] English Certificate Attachments")
        if not english_rows:
            print("- row: missing")
        else:
            for row in english_rows:
                exam_name = str(row.get("exam_name") or "").strip() or "(unnamed exam)"
                score_text = str(row.get("score_text") or "").strip() or "(empty)"
                certificate_url = str(row.get("certificate_attachment_url") or "").strip()
                status = "present" if certificate_url else "missing"
                print(f"- english_id={row.get('id')} exam={exam_name} score={score_text}")
                print(f"  certificate_attachment_url: {status}")
                print(f"  value: {certificate_url or '(empty)'}")
                print_physical_file_report(
                    "certificate_attachment_file",
                    attachments_root,
                    row.get("certificate_attachment_url"),
                    int(latest_application.get("portal_student_id") or 0) or None,
                    "english_certificate",
                )

        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())