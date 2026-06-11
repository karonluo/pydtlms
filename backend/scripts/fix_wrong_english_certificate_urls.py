from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlsplit

from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


OLD_PREFIX = "/portal-attachments/uploads/"
NEW_PREFIX = "/api/v1/portal/attachments/"
SITE_ROOT_URL = settings.normalized_site_root_url
STANDARD_ABSOLUTE_PREFIX = settings.build_absolute_site_url(NEW_PREFIX) or NEW_PREFIX
LEGACY_ABSOLUTE_PREFIX = settings.build_absolute_site_url(OLD_PREFIX) or OLD_PREFIX
DEFAULT_BULK_THRESHOLD = 100


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fix incorrect English certificate attachment URLs by replacing the legacy portal-attachments path with the API path.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show how many rows would be updated and print a few samples.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually update the rows in PostgreSQL.",
    )
    parser.add_argument(
        "--force-bulk",
        action="store_true",
        help="Allow large updates when the affected row count exceeds the safety threshold.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print per-row before/after samples while processing.",
    )
    return parser


def load_candidates(store: PostgresStateStore, database_name: str) -> list[dict[str, object]]:
    with store._connect(database_name) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    ep.id,
                    ep.application_id,
                    ps.id AS student_id,
                    ps.full_name AS student_name,
                    ep.certificate_attachment_url
                FROM dtlms_portal_application_english_proficiencies ep
                JOIN dtlms_recruitment_applications ra ON ra.id = ep.application_id
                JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
                WHERE ep.certificate_attachment_url IS NOT NULL
                  AND BTRIM(ep.certificate_attachment_url) <> ''
                ORDER BY ps.id ASC, ep.id ASC
                """,
            )
            return [dict(row) for row in cur.fetchall()]


def is_standard_url(url: str) -> bool:
    normalized_url = url.strip()
    return normalized_url.startswith(NEW_PREFIX)


def normalize_url(url: str) -> str | None:
    normalized_url = url.strip()
    if not normalized_url:
        return None

    if normalized_url.startswith(NEW_PREFIX):
        return normalized_url

    if normalized_url.startswith(STANDARD_ABSOLUTE_PREFIX):
        return NEW_PREFIX + normalized_url[len(STANDARD_ABSOLUTE_PREFIX):]

    if normalized_url.startswith(LEGACY_ABSOLUTE_PREFIX):
        return NEW_PREFIX + normalized_url[len(LEGACY_ABSOLUTE_PREFIX):]

    if normalized_url.startswith(OLD_PREFIX):
        return NEW_PREFIX + normalized_url[len(OLD_PREFIX):]

    if normalized_url.startswith(("http://", "https://")):
        parsed = urlsplit(normalized_url)
        if parsed.path.startswith(NEW_PREFIX):
            return parsed.path
        if parsed.path.startswith(OLD_PREFIX):
            return NEW_PREFIX + parsed.path[len(OLD_PREFIX):]

    return None


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        try:
            candidates = load_candidates(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to load candidate rows: {exc}", file=sys.stderr)
            return 1

        print(f"[INFO] Database: {args.database}")
        print(f"[INFO] Legacy prefix: {LEGACY_ABSOLUTE_PREFIX}")
        print(f"[INFO] Standard prefix: {NEW_PREFIX}")

        updates: list[dict[str, object]] = []
        skipped_standard = 0
        skipped_unknown = 0
        for candidate in candidates:
            old_url = str(candidate.get("certificate_attachment_url") or "")
            if is_standard_url(old_url):
                skipped_standard += 1
                continue
            new_url = normalize_url(old_url)
            if new_url is None or new_url == old_url:
                skipped_unknown += 1
                continue
            candidate["normalized_certificate_attachment_url"] = new_url
            updates.append(candidate)

        print(f"[INFO] Total non-empty English certificate URLs: {len(candidates)}")
        print(f"[INFO] Already standard URLs skipped: {skipped_standard}")
        print(f"[INFO] Fixable wrong URLs: {len(updates)}")
        print(f"[INFO] Unrecognized URLs skipped: {skipped_unknown}")

        if updates:
            for sample in updates[:10]:
                old_url = str(sample.get("certificate_attachment_url") or "")
                new_url = str(sample.get("normalized_certificate_attachment_url") or "")
                print(
                    f"[SAMPLE] student_id={sample.get('student_id')} english_id={sample.get('id')}\n"
                    f"         old={old_url}\n"
                    f"         new={new_url}"
                )

        if args.dry_run:
            print("[INFO] Dry run completed. No changes were written.")
            return 0

        if not args.apply:
            print("[INFO] No changes were written. Re-run with --apply to persist updates.")
            return 0

        if len(updates) > DEFAULT_BULK_THRESHOLD and not args.force_bulk:
            print(
                f"[ERROR] Refusing to update {len(updates)} rows without --force-bulk. "
                f"Use --dry-run first or pass --force-bulk if this bulk correction is expected.",
                file=sys.stderr,
            )
            return 1

        updated_count = 0
        with store._connect(args.database) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                for candidate in updates:
                    old_url = str(candidate.get("certificate_attachment_url") or "")
                    new_url = str(candidate.get("normalized_certificate_attachment_url") or "")
                    if new_url == old_url:
                        continue
                    cur.execute(
                        """
                        UPDATE dtlms_portal_application_english_proficiencies
                        SET certificate_attachment_url = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                          AND certificate_attachment_url = %s
                          AND certificate_attachment_url <> %s
                        """,
                        (new_url, int(candidate["id"]), old_url, new_url),
                    )
                    if cur.rowcount > 0:
                        updated_count += 1
                        if args.summary:
                            print(
                                f"[UPDATE] student_id={candidate.get('student_id')} english_id={candidate.get('id')}"
                            )

            conn.commit()

        print(f"[INFO] Updated rows: {updated_count}")
        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())