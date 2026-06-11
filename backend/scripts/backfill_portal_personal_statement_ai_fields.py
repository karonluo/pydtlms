from __future__ import annotations

from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore


def main() -> int:
    store = PostgresStateStore()

    with store._connect(settings.postgres_db) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH source_rows AS (
                    SELECT
                        ra.id AS application_id,
                        NULLIF(BTRIM(s.application_draft -> 'personal_statement' ->> 'ai_problem_statement'), '') AS ai_problem_statement,
                        NULLIF(BTRIM(s.application_draft -> 'personal_statement' ->> 'ai_industry_opinion'), '') AS ai_industry_opinion
                    FROM dtlms_portal_students AS s
                    JOIN dtlms_recruitment_applications AS ra
                      ON ra.portal_student_id = s.id
                     AND ra.is_deleted = FALSE
                )
                UPDATE dtlms_recruitment_applications AS ra
                SET research_problem = COALESCE(NULLIF(BTRIM(ra.research_problem), ''), source_rows.ai_problem_statement),
                    dissenting_view = COALESCE(NULLIF(BTRIM(ra.dissenting_view), ''), source_rows.ai_industry_opinion),
                    updated_at = CURRENT_TIMESTAMP
                FROM source_rows
                WHERE ra.id = source_rows.application_id
                  AND (
                        (NULLIF(BTRIM(ra.research_problem), '') IS NULL AND source_rows.ai_problem_statement IS NOT NULL)
                     OR (NULLIF(BTRIM(ra.dissenting_view), '') IS NULL AND source_rows.ai_industry_opinion IS NOT NULL)
                  )
                RETURNING ra.id
                """
            )
            recruitment_rows = cur.fetchall()

            cur.execute(
                """
                WITH source_rows AS (
                    SELECT
                        ra.id AS application_id,
                        NULLIF(BTRIM(s.application_draft -> 'personal_statement' ->> 'ai_problem_statement'), '') AS ai_problem_statement,
                        NULLIF(BTRIM(s.application_draft -> 'personal_statement' ->> 'ai_industry_opinion'), '') AS ai_industry_opinion
                    FROM dtlms_portal_students AS s
                    JOIN dtlms_recruitment_applications AS ra
                      ON ra.portal_student_id = s.id
                     AND ra.is_deleted = FALSE
                )
                UPDATE dtlms_portal_application_personal_statements AS ps
                SET ai_problem_statement = COALESCE(NULLIF(BTRIM(ps.ai_problem_statement), ''), source_rows.ai_problem_statement),
                    ai_industry_opinion = COALESCE(NULLIF(BTRIM(ps.ai_industry_opinion), ''), source_rows.ai_industry_opinion),
                    updated_at = CURRENT_TIMESTAMP
                FROM source_rows
                WHERE ps.application_id = source_rows.application_id
                  AND (
                        (NULLIF(BTRIM(ps.ai_problem_statement), '') IS NULL AND source_rows.ai_problem_statement IS NOT NULL)
                     OR (NULLIF(BTRIM(ps.ai_industry_opinion), '') IS NULL AND source_rows.ai_industry_opinion IS NOT NULL)
                  )
                RETURNING ps.application_id
                """
            )
            personal_statement_rows = cur.fetchall()

        conn.commit()

    print(f"Updated recruitment applications: {len(recruitment_rows)}")
    print(f"Updated personal statement rows: {len(personal_statement_rows)}")
    print(f"Total updated rows: {len(recruitment_rows) + len(personal_statement_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())