"""Query the list of students rejected by 2 background-assessment votes on a given date.

Usage examples:
  # Single date (Asia/Shanghai, default), all time-of-day rows
  python -m backend.scripts.query_bg_assessment_2_reject --date 2026-05-14

  # Date range (inclusive)
  python -m backend.scripts.query_bg_assessment_2_reject --from 2026-05-01 --to 2026-05-31

  # Override the assessment timestamp column and time zone
  python -m backend.scripts.query_bg_assessment_2_reject --date 2026-05-14 \\
      --column assessed_at --tz Asia/Shanghai

  # Show summary statistics and export CSV
  python -m backend.scripts.query_bg_assessment_2_reject --date 2026-05-14 \\
      --summary --export-csv out/rejected_2026-05-14.csv

The script targets the PostgreSQL connection configured in `backend/.env` and
treats ``assessed_at`` as the canonical "background-assessment action time".
It only counts rows whose ``assessment_result`` is "不通过" (``reject``) and
only includes applications whose total reject count reaches 2 within the
filter window (the second reject must fall inside the window, and the final
total reject count must be >= 2 to make it a "2-vote rejection").
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import psycopg
from psycopg.rows import dict_row


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings  # noqa: E402


ASSESSMENT_RESULT_REJECT = "不通过"
REJECT_THRESHOLD = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "List students whose background assessment received >=2 reject votes, "
            "with the second reject happening on the given date/range."
        ),
        epilog="Example: python -m backend.scripts.query_bg_assessment_2_reject --date 2026-05-14 --summary",
    )
    parser.add_argument(
        "--date",
        type=_parse_iso_date,
        help="Single date in YYYY-MM-DD (Asia/Shanghai by default).",
    )
    parser.add_argument(
        "--from",
        dest="date_from",
        type=_parse_iso_date,
        help="Range start date (inclusive, YYYY-MM-DD).",
    )
    parser.add_argument(
        "--to",
        dest="date_to",
        type=_parse_iso_date,
        help="Range end date (inclusive, YYYY-MM-DD).",
    )
    parser.add_argument(
        "--tz",
        default="Asia/Shanghai",
        help="IANA timezone name for interpreting --date/--from/--to (default: Asia/Shanghai).",
    )
    parser.add_argument(
        "--column",
        default="assessed_at",
        help="Background-assessment timestamp column to filter on (default: assessed_at).",
    )
    parser.add_argument(
        "--result-value",
        default=ASSESSMENT_RESULT_REJECT,
        help="Background-assessment value that counts as a reject vote (default: 不通过).",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=REJECT_THRESHOLD,
        help="Reject vote count threshold (default: 2).",
    )
    parser.add_argument(
        "--include-deleted",
        action="store_true",
        help="Include soft-deleted recruitment applications in the result.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics along with the detailed rows.",
    )
    parser.add_argument(
        "--export-csv",
        type=Path,
        help="Optional path to also export the result rows as CSV.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit the number of returned students (0 = no limit).",
    )
    return parser


def _parse_iso_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}', expected YYYY-MM-DD: {exc}") from exc


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def _resolve_window(args: argparse.Namespace) -> tuple[datetime, datetime, str]:
    if args.date and (args.date_from or args.date_to):
        raise SystemExit("[ERROR] --date cannot be combined with --from/--to")
    if not args.date and not (args.date_from and args.date_to):
        raise SystemExit("[ERROR] Provide either --date or both --from and --to")

    try:
        from zoneinfo import ZoneInfo
    except ImportError as exc:  # pragma: no cover - Python 3.9+
        raise SystemExit("[ERROR] zoneinfo is required (Python 3.9+)") from exc

    try:
        tz = ZoneInfo(args.tz)
    except Exception as exc:
        raise SystemExit(f"[ERROR] Invalid timezone '{args.tz}': {exc}") from exc

    if args.date:
        start_local = datetime.combine(args.date, time.min, tzinfo=tz)
        end_local = datetime.combine(args.date, time.max, tzinfo=tz)
    else:
        if args.date_from > args.date_to:
            raise SystemExit("[ERROR] --from must be <= --to")
        start_local = datetime.combine(args.date_from, time.min, tzinfo=tz)
        # end-of-day inclusive: include the whole day of `date_to`
        end_local = datetime.combine(args.date_to, time.max, tzinfo=tz)

    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)
    label = f"{start_local.date().isoformat()} ~ {end_local.date().isoformat()} ({args.tz})"
    return start_utc, end_utc, label


def _candidate_query(
    column: str,
    threshold: int,
    include_deleted: bool,
    reject_value: str,
) -> str:
    if not column.replace("_", "").isalnum():
        raise SystemExit(f"[ERROR] Unsafe column name: {column!r}")

    deleted_clause = "" if include_deleted else "AND ra.is_deleted = FALSE"
    return f"""
    WITH windowed_rejects AS (
        SELECT
            ba.application_id,
            ba.assessed_at,
            ba.evaluator_username,
            ba.evaluator_name,
            ba.evaluator_role_code,
            ba.assessment_result,
            ba.assessment_comment
        FROM dtlms_background_assessments ba
        WHERE ba.assessment_result = %s
          AND ba.assessed_at >= %s
          AND ba.assessed_at <= %s
    ),
    rejects_in_window AS (
        SELECT
            wr.application_id,
            COUNT(*)::int AS window_reject_count,
            MIN(wr.assessed_at) AS first_window_reject_at,
            MAX(wr.assessed_at) AS second_window_reject_at
        FROM windowed_rejects wr
        GROUP BY wr.application_id
        HAVING COUNT(*) >= %s
    ),
    total_reject_counts AS (
        SELECT
            ba.application_id,
            COUNT(*)::int AS total_reject_count,
            COUNT(*) FILTER (WHERE ba.assessed_at <= %s)::int AS reject_count_up_to_end
        FROM dtlms_background_assessments ba
        WHERE ba.assessment_result = %s
        GROUP BY ba.application_id
    )
    SELECT
        riw.application_id,
        ra.portal_student_id,
        stu.full_name,
        stu.phone_number,
        stu.email,
        stu.id_number,
        stu.candidate_no AS portal_candidate_no,
        ra.candidate_no AS application_candidate_no,
        ra.business_key,
        ra.plan_id,
        ra.application_status,
        ra.initial_screening_status,
        ra.initial_screening_result,
        ra.first_choice,
        ra.first_choice_id,
        ra.second_choice,
        ra.second_choice_id,
        ra.updated_at AS application_updated_at,
        riw.window_reject_count,
        riw.first_window_reject_at,
        riw.second_window_reject_at,
        trc.total_reject_count,
        trc.reject_count_up_to_end
    FROM rejects_in_window riw
    JOIN total_reject_counts trc ON trc.application_id = riw.application_id
    JOIN dtlms_recruitment_applications ra ON ra.id = riw.application_id
    LEFT JOIN dtlms_portal_students stu ON stu.id = ra.portal_student_id
    WHERE trc.reject_count_up_to_end >= %s
      {deleted_clause}
    ORDER BY riw.second_window_reject_at ASC, riw.application_id ASC
    """


def _assessment_query() -> str:
    return """
    SELECT
        application_id,
        assessed_at,
        evaluator_username,
        evaluator_name,
        evaluator_role_code,
        assessment_result,
        assessment_comment
    FROM dtlms_background_assessments
    WHERE application_id = ANY(%s)
    ORDER BY application_id ASC, assessed_at ASC, id ASC
    """


def _fetch_rows(
    start_utc: datetime,
    end_utc: datetime,
    column: str,
    threshold: int,
    reject_value: str,
    include_deleted: bool,
    limit: int,
) -> list[dict[str, Any]]:
    sql = _candidate_query(column=column, threshold=threshold, include_deleted=include_deleted, reject_value=reject_value)
    params: list[Any] = [
        reject_value,
        start_utc,
        end_utc,
        threshold,
        end_utc,
        reject_value,
        threshold,
    ]
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = [dict(item) for item in cur.fetchall()]

    if limit > 0:
        rows = rows[:limit]
    return rows


def _fetch_assessments(application_ids: Iterable[int]) -> dict[int, list[dict[str, Any]]]:
    ids = [int(item) for item in application_ids]
    if not ids:
        return {}

    sql = _assessment_query()
    with psycopg.connect(_conninfo()) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql, (ids,))
            rows = [dict(item) for item in cur.fetchall()]

    grouped: dict[int, list[dict[str, Any]]] = {}
    for item in rows:
        grouped.setdefault(int(item["application_id"]), []).append(item)
    return grouped


def _build_assessment_payload(
    assessments: list[dict[str, Any]],
    second_window_reject_at: datetime,
) -> dict[str, Any]:
    reject_votes = []
    other_votes = []
    for item in assessments:
        bucket = reject_votes if item.get("assessment_result") == "不通过" else other_votes
        bucket.append(
            {
                "assessed_at": item.get("assessed_at"),
                "evaluator_username": item.get("evaluator_username"),
                "evaluator_name": item.get("evaluator_name"),
                "evaluator_role_code": item.get("evaluator_role_code"),
                "assessment_result": item.get("assessment_result"),
                "assessment_comment": item.get("assessment_comment"),
            }
        )
    second_window_reject_at_naive = second_window_reject_at.replace(tzinfo=None) if second_window_reject_at.tzinfo else second_window_reject_at
    second_window_reject_votes = [
        item
        for item in reject_votes
        if item["assessed_at"] is not None
        and (item["assessed_at"].replace(tzinfo=None) if item["assessed_at"].tzinfo else item["assessed_at"])
        <= second_window_reject_at_naive
    ]
    return {
        "reject_votes": reject_votes,
        "other_votes": other_votes,
        "second_reject_vote": second_window_reject_votes[-1] if second_window_reject_votes else None,
    }


def _row_to_payload(row: dict[str, Any], assessments: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    application_id = int(row["application_id"])
    assessment_payload = _build_assessment_payload(
        assessments.get(application_id, []),
        row["second_window_reject_at"],
    )
    return {
        "application_id": application_id,
        "portal_student_id": row.get("portal_student_id"),
        "full_name": row.get("full_name"),
        "phone_number": row.get("phone_number"),
        "email": row.get("email"),
        "id_number": row.get("id_number"),
        "candidate_no_application": row.get("application_candidate_no"),
        "candidate_no_portal": row.get("portal_candidate_no"),
        "business_key": row.get("business_key"),
        "plan_id": row.get("plan_id"),
        "application_status": row.get("application_status"),
        "initial_screening_status": row.get("initial_screening_status"),
        "initial_screening_result": row.get("initial_screening_result"),
        "first_choice": row.get("first_choice"),
        "first_choice_id": row.get("first_choice_id"),
        "second_choice": row.get("second_choice"),
        "second_choice_id": row.get("second_choice_id"),
        "application_updated_at": row.get("application_updated_at"),
        "reject_vote_count_in_window": row.get("window_reject_count"),
        "first_reject_at_in_window": row.get("first_window_reject_at"),
        "second_reject_at_in_window": row.get("second_window_reject_at"),
        "reject_vote_count_total": row.get("total_reject_count"),
        "reject_vote_count_up_to_window_end": row.get("reject_count_up_to_end"),
        "second_reject_vote_detail": assessment_payload["second_reject_vote"],
        "background_assessment_history": assessment_payload["reject_votes"] + assessment_payload["other_votes"],
    }


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    status_counter: Counter[str] = Counter()
    role_counter: Counter[str] = Counter()
    plan_counter: Counter[Any] = Counter()
    for row in rows:
        status_counter[str(row.get("application_status") or "<null>")] += 1
        detail = row.get("second_reject_vote_detail") or {}
        role_counter[str(detail.get("evaluator_role_code") or "<null>")] += 1
        plan_counter[row.get("plan_id")] += 1
    return {
        "total_matched": len(rows),
        "application_status_counter": dict(status_counter),
        "second_reject_role_counter": dict(role_counter),
        "plan_id_counter": {str(k): v for k, v in plan_counter.items()},
    }


def _export_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "application_id",
        "portal_student_id",
        "full_name",
        "phone_number",
        "email",
        "id_number",
        "candidate_no_application",
        "candidate_no_portal",
        "business_key",
        "plan_id",
        "application_status",
        "first_choice",
        "second_choice",
        "reject_vote_count_in_window",
        "first_reject_at_in_window",
        "second_reject_at_in_window",
        "reject_vote_count_total",
        "reject_vote_count_up_to_window_end",
        "second_reject_evaluator_username",
        "second_reject_evaluator_name",
        "second_reject_evaluator_role_code",
        "second_reject_comment",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            detail = row.get("second_reject_vote_detail") or {}
            writer.writerow(
                {
                    "application_id": row.get("application_id"),
                    "portal_student_id": row.get("portal_student_id"),
                    "full_name": row.get("full_name"),
                    "phone_number": row.get("phone_number"),
                    "email": row.get("email"),
                    "id_number": row.get("id_number"),
                    "candidate_no_application": row.get("candidate_no_application"),
                    "candidate_no_portal": row.get("candidate_no_portal"),
                    "business_key": row.get("business_key"),
                    "plan_id": row.get("plan_id"),
                    "application_status": row.get("application_status"),
                    "first_choice": row.get("first_choice"),
                    "second_choice": row.get("second_choice"),
                    "reject_vote_count_in_window": row.get("reject_vote_count_in_window"),
                    "first_reject_at_in_window": row.get("first_reject_at_in_window"),
                    "second_reject_at_in_window": row.get("second_reject_at_in_window"),
                    "reject_vote_count_total": row.get("reject_vote_count_total"),
                    "reject_vote_count_up_to_window_end": row.get("reject_vote_count_up_to_window_end"),
                    "second_reject_evaluator_username": detail.get("evaluator_username"),
                    "second_reject_evaluator_name": detail.get("evaluator_name"),
                    "second_reject_evaluator_role_code": detail.get("evaluator_role_code"),
                    "second_reject_comment": detail.get("assessment_comment"),
                }
            )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    start_utc, end_utc, label = _resolve_window(args)

    try:
        candidate_rows = _fetch_rows(
            start_utc=start_utc,
            end_utc=end_utc,
            column=args.column,
            threshold=args.threshold,
            reject_value=args.result_value,
            include_deleted=args.include_deleted,
            limit=args.limit,
        )
    except Exception as exc:
        print(f"[ERROR] Query failed: {exc}", file=sys.stderr)
        return 1

    assessments_by_application = _fetch_assessments(int(row["application_id"]) for row in candidate_rows)
    payload_rows = [_row_to_payload(row, assessments_by_application) for row in candidate_rows]

    print(f"[INFO] Date window: {label}")
    print(f"[INFO] UTC window : {start_utc.isoformat()} ~ {end_utc.isoformat()}")
    print(f"[INFO] Matched applications: {len(payload_rows)}")
    print(json.dumps(payload_rows, ensure_ascii=False, indent=2, default=str))

    if args.summary:
        print(json.dumps(_summary(payload_rows), ensure_ascii=False, indent=2, default=str))

    if args.export_csv:
        try:
            _export_csv(args.export_csv, payload_rows)
        except Exception as exc:
            print(f"[ERROR] CSV export failed: {exc}", file=sys.stderr)
            return 1
        print(f"[INFO] CSV exported to: {args.export_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
