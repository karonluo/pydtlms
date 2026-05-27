from __future__ import annotations

import argparse
import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize recruitment application business keys and sync matching Flowable-compatible business keys.",
        epilog=(
            "Example: python backend/scripts/normalize_recruitment_application_business_keys.py --apply"
        ),
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute the repair. Without this flag the script only prints the target and exits.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate the configured target and print what would run without executing updates.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.apply and args.dry_run:
        print("[ERROR] --apply and --dry-run cannot be used together.", file=sys.stderr)
        return 1

    print("[INFO] Repair: normalize recruitment application business keys")
    print(f"[INFO] Database: {settings.postgres_db}")
    print(f"[INFO] Host: {settings.postgres_host}:{settings.postgres_port}")
    print("[INFO] Scope: dtlms_recruitment_applications and Flowable-compatible workflow business keys")

    if args.dry_run or not args.apply:
        print("[INFO] Dry run completed. No database updates were executed.")
        if not args.apply and not args.dry_run:
            print("[INFO] Re-run with --apply to execute the repair.")
        return 0

    store = PostgresStateStore()
    try:
        changed_count = store.normalize_recruitment_application_business_keys()
    except Exception as exc:
        print(f"[ERROR] Repair failed: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Repair completed. Renamed recruitment application keys: {changed_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())