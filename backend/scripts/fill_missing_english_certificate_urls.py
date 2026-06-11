from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import sys
from collections import defaultdict
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fill missing English certificate URLs from frontend/public/portal-attachments/uploads/student-*/english_certificate.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--attachments-root",
        default=str(DEFAULT_ATTACHMENTS_ROOT),
        help=f"Root directory for portal attachments. Default: {DEFAULT_ATTACHMENTS_ROOT}",
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
        "--force-bulk",
        action="store_true",
        help="Allow bulk updates when the planned row count is large.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a short per-student summary while processing.",
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
    return "/api/v1/portal/attachments/" + relative_path.as_posix()


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


def get_file_created_timestamp(file_path: Path) -> float:
    stat_result = file_path.stat()
    birth_time = getattr(stat_result, "st_birthtime", None)
    if birth_time is not None:
        return float(birth_time)
    return float(getattr(stat_result, "st_ctime", stat_result.st_mtime))


def list_english_certificate_files(attachments_root: Path, student_id: int) -> list[Path]:
    student_folder = attachments_root / f"student-{student_id}" / "english_certificate"
    if not student_folder.exists() or not student_folder.is_dir():
        return []
    return sorted(
        (item for item in student_folder.iterdir() if item.is_file()),
        key=lambda item: (get_file_created_timestamp(item), item.name.lower()),
    )


def build_file_match_key(file_candidate: tuple[Any, Path], row_timestamp: float) -> tuple[float, float, str]:
    file_timestamp = float(file_candidate[0])
    file_path = file_candidate[1]
    return abs(file_timestamp - row_timestamp), file_timestamp, file_path.name.lower()


def load_candidates(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH latest_applications AS (
                    SELECT DISTINCT ON (ps.id)
                        ps.id AS student_id,
                        ps.full_name AS student_name,
                        ra.id AS application_id,
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
                    la.application_status,
                    la.application_form_status,
                    ep.id AS english_proficiency_id,
                    ep.exam_name,
                    ep.score_text,
                    ep.certificate_attachment_url,
                    ep.created_at,
                    ep.updated_at
                FROM latest_applications la
                JOIN dtlms_portal_application_english_proficiencies ep ON ep.application_id = la.application_id
                                WHERE la.application_form_status IN ('已填写报名', '驳回重填')
                                    AND COALESCE(BTRIM(ep.certificate_attachment_url), '') = ''
                ORDER BY la.student_id ASC, ep.created_at ASC, ep.updated_at ASC, ep.id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


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
            candidate_rows = load_candidates(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to load candidate rows: {exc}", file=sys.stderr)
            return 1

        if not candidate_rows:
            print(f"[INFO] Database: {args.database}")
            print("[INFO] No portal students need English certificate URL backfill.")
            return 0

        candidates_by_student: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in candidate_rows:
            candidates_by_student[int(row["student_id"])].append(row)

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Attachments root: {attachments_root}")
        print(f"[INFO] Students to inspect: {len(candidates_by_student)}")
        print(f"[INFO] Missing English attachment rows: {len(candidate_rows)}")

        updates: list[tuple[int, int, str]] = []
        skipped_students: list[str] = []

        for student_id, rows in sorted(candidates_by_student.items()):
            student_name = str(rows[0].get("student_name") or "")
            files = list_english_certificate_files(attachments_root, student_id)
            if not files:
                skipped_students.append(f"student_id={student_id} name={student_name} reason=no_files")
                if args.summary:
                    print(f"[SKIP] student_id={student_id} name={student_name} no files in english_certificate")
                continue

            ordered_rows = sorted(
                rows,
                key=lambda row: (
                    (to_timestamp(row.get("created_at")) or to_timestamp(row.get("updated_at")) or float("inf")),
                    int(row.get("english_proficiency_id") or 0),
                ),
            )
            file_candidates = [
                (get_file_created_timestamp(file_path), file_path)
                for file_path in files
            ]
            if len(file_candidates) < len(ordered_rows):
                if args.summary:
                    print(
                        f"[WARN] student_id={student_id} name={student_name} rows={len(ordered_rows)} files={len(file_candidates)} "
                        "will update only matched pairs"
                    )

            for row in ordered_rows:
                if not file_candidates:
                    break
                row_timestamp = row.get("_row_timestamp")
                if not isinstance(row_timestamp, (int, float)):
                    row_timestamp = to_timestamp(row.get("created_at")) or to_timestamp(row.get("updated_at")) or file_candidates[0][0]
                    row["_row_timestamp"] = float(row_timestamp)
                else:
                    row_timestamp = float(row_timestamp)
                match_row_timestamp = float(row_timestamp)
                best_index = min(
                    range(len(file_candidates)),
                    key=lambda index: build_file_match_key(file_candidates[index], match_row_timestamp),
                )
                _, file_path = file_candidates.pop(best_index)
                updates.append((int(row["english_proficiency_id"]), student_id, build_public_attachment_url(attachments_root, file_path)))
                if args.summary:
                    print(
                        f"[PLAN] student_id={student_id} english_id={int(row['english_proficiency_id'])} "
                        f"file={file_path.name}"
                    )

        if args.dry_run:
            print(f"[INFO] Planned updates: {len(updates)}")
            print(f"[INFO] Skipped students: {len(skipped_students)}")
            return 0

        if not args.apply:
            print(f"[INFO] Planned updates: {len(updates)}")
            print(f"[INFO] Skipped students: {len(skipped_students)}")
            print("[INFO] No changes were written. Re-run with --apply to persist updates.")
            return 0

        bulk_threshold = 100
        if len(updates) > bulk_threshold and not args.force_bulk:
            print(
                f"[ERROR] Refusing to write {len(updates)} rows without --force-bulk. "
                f"Use --dry-run first or pass --force-bulk if you really intend a bulk repair.",
                file=sys.stderr,
            )
            return 1

        if not updates:
            print("[INFO] No matching attachment files found. Nothing to update.")
            return 0

        updated_count = 0
        with store._connect(args.database) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                for english_proficiency_id, student_id, certificate_url in updates:
                    cur.execute(
                        """
                        UPDATE dtlms_portal_application_english_proficiencies
                        SET certificate_attachment_url = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                          AND COALESCE(BTRIM(certificate_attachment_url), '') = ''
                        """,
                        (certificate_url, english_proficiency_id),
                    )
                    if cur.rowcount > 0:
                        updated_count += 1
                        if args.summary:
                            print(
                                f"[UPDATE] student_id={student_id} english_id={english_proficiency_id} url={certificate_url}"
                            )

            conn.commit()

        print(f"[INFO] Updated rows: {updated_count}")
        print(f"[INFO] Skipped students: {len(skipped_students)}")
        if skipped_students and args.summary:
            for item in skipped_students:
                print(f"[SKIP] {item}")
        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())