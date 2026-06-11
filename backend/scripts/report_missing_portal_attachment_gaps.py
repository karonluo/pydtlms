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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report portal students with a candidate number whose resume URL, personal-statement optional questions, or English certificate URL are missing.",
    )
    parser.add_argument(
        "--database",
        default=settings.postgres_db,
        help=f"Target database name. Defaults to current config value: {settings.postgres_db}",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a compact summary block at the end.",
    )
    return parser


def load_resume_candidates(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
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
                        ra.candidate_no,
                        ra.application_status,
                        COALESCE(ra.applied_at, ra.created_at) AS applied_at
                    FROM dtlms_portal_students AS ps
                    JOIN dtlms_recruitment_applications AS ra
                      ON ra.portal_student_id = ps.id
                     AND ra.is_deleted = FALSE
                    WHERE COALESCE(BTRIM(ra.candidate_no), '') <> ''
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
                    psm.resume_attachment_url,
                    psm.ai_problem_statement,
                    psm.ai_industry_opinion
                FROM latest_applications AS la
                LEFT JOIN dtlms_portal_application_personal_statements AS psm
                  ON psm.application_id = la.application_id
                WHERE COALESCE(BTRIM(psm.resume_attachment_url), '') = ''
                ORDER BY la.student_id ASC, la.application_id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def load_personal_statement_candidates(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
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
                        ra.candidate_no,
                        ra.application_status,
                        COALESCE(ra.applied_at, ra.created_at) AS applied_at
                    FROM dtlms_portal_students AS ps
                    JOIN dtlms_recruitment_applications AS ra
                      ON ra.portal_student_id = ps.id
                     AND ra.is_deleted = FALSE
                    WHERE COALESCE(BTRIM(ra.candidate_no), '') <> ''
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
                    psm.ai_problem_statement,
                    psm.ai_industry_opinion
                FROM latest_applications AS la
                LEFT JOIN dtlms_portal_application_personal_statements AS psm
                  ON psm.application_id = la.application_id
                WHERE COALESCE(BTRIM(psm.ai_problem_statement), '') = ''
                   OR COALESCE(BTRIM(psm.ai_industry_opinion), '') = ''
                ORDER BY la.student_id ASC, la.application_id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def load_english_certificate_candidates(store: PostgresStateStore, database_name: str) -> list[dict[str, Any]]:
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
                        ra.candidate_no,
                        ra.application_status,
                        COALESCE(ra.applied_at, ra.created_at) AS applied_at
                    FROM dtlms_portal_students AS ps
                    JOIN dtlms_recruitment_applications AS ra
                      ON ra.portal_student_id = ps.id
                     AND ra.is_deleted = FALSE
                    WHERE COALESCE(BTRIM(ra.candidate_no), '') <> ''
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
                    ep.id AS english_proficiency_id,
                    ep.exam_name,
                    ep.score_text,
                    ep.certificate_attachment_url
                FROM latest_applications AS la
                JOIN dtlms_portal_application_english_proficiencies AS ep
                  ON ep.application_id = la.application_id
                WHERE COALESCE(BTRIM(ep.certificate_attachment_url), '') = ''
                ORDER BY la.student_id ASC, la.application_id ASC, ep.id ASC
                """
            )
            return [dict(row) for row in cur.fetchall()]


def print_section(title: str, rows: list[dict[str, Any]], formatter) -> None:
    print(f"\n[{title}] {len(rows)}")
    if not rows:
        print("- 无")
        return

    for row in rows:
        print(formatter(row))


def fmt_text(value: Any) -> str:
    text = str(value or "").strip()
    return text if text else "(empty)"


def format_resume_row(row: dict[str, Any]) -> str:
    return (
        f"- student_id={row.get('student_id')} candidate_no={fmt_text(row.get('candidate_no'))} "
        f"name={fmt_text(row.get('student_name'))} application_id={row.get('application_id')} "
        f"status={fmt_text(row.get('application_status'))} resume_url={fmt_text(row.get('resume_attachment_url'))}"
    )


def format_personal_statement_row(row: dict[str, Any]) -> str:
    return (
        f"- student_id={row.get('student_id')} candidate_no={fmt_text(row.get('candidate_no'))} "
        f"name={fmt_text(row.get('student_name'))} application_id={row.get('application_id')} "
        f"status={fmt_text(row.get('application_status'))} "
        f"ai_problem_statement={fmt_text(row.get('ai_problem_statement'))} "
        f"ai_industry_opinion={fmt_text(row.get('ai_industry_opinion'))}"
    )


def format_english_row(row: dict[str, Any]) -> str:
    return (
        f"- student_id={row.get('student_id')} candidate_no={fmt_text(row.get('candidate_no'))} "
        f"name={fmt_text(row.get('student_name'))} application_id={row.get('application_id')} "
        f"status={fmt_text(row.get('application_status'))} english_id={row.get('english_proficiency_id')} "
        f"exam_name={fmt_text(row.get('exam_name'))} score_text={fmt_text(row.get('score_text'))} "
        f"certificate_url={fmt_text(row.get('certificate_attachment_url'))}"
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = PostgresStateStore()
    original_database = settings.postgres_db
    settings.postgres_db = args.database

    try:
        try:
            resume_rows = load_resume_candidates(store, args.database)
            personal_statement_rows = load_personal_statement_candidates(store, args.database)
            english_rows = load_english_certificate_candidates(store, args.database)
        except Exception as exc:
            print(f"[ERROR] Failed to query portal data: {exc}", file=sys.stderr)
            return 1

        print(f"[INFO] Database: {args.database}")
        print("[INFO] Scope: portal students with non-empty candidate_no and active applications")

        print_section("简历附件URL为空", resume_rows, format_resume_row)
        print_section("个人陈述两个选填问题为空", personal_statement_rows, format_personal_statement_row)
        print_section("英文成绩单附件URL为空", english_rows, format_english_row)

        if args.summary:
            print("\n[SUMMARY]")
            print(f"- resume_url_empty_rows={len(resume_rows)}")
            print(f"- personal_statement_optional_empty_rows={len(personal_statement_rows)}")
            print(f"- english_certificate_empty_rows={len(english_rows)}")

        return 0
    finally:
        settings.postgres_db = original_database


if __name__ == "__main__":
    raise SystemExit(main())