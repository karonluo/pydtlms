from __future__ import annotations

from typing import Any

from psycopg.rows import dict_row

from app.core.config import settings
from app.schemas.auth import Principal
from app.schemas.recruitment import AdvisorScreeningScoreUpdateRequest, RecruitApplicationRecord

from .postgres_state_store import PostgresStateStore


query_store = PostgresStateStore()


def _resolve_screening_score_column(choice_name: str) -> tuple[str, str]:
    normalized_choice_name = str(choice_name or "").strip()
    if normalized_choice_name == "第一志愿":
        return "first_choice", "first_choice_screening_score"
    if normalized_choice_name == "第二志愿":
        return "second_choice", "second_choice_screening_score"
    raise ValueError("choice_name 只能是 第一志愿 或 第二志愿")


def update_advisor_screening_score(
    payload: AdvisorScreeningScoreUpdateRequest,
    *,
    principal: Principal,
) -> RecruitApplicationRecord:
    del principal
    screening_round, score_column = _resolve_screening_score_column(payload.choice_name)
    score = float(payload.advisor_score)
    candidate_no = str(payload.candidate_no or "").strip()
    application_id = int(payload.application_id)

    query_store.ensure_schema()
    with query_store._connect(settings.postgres_db) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    id,
                    candidate_no,
                    application_status,
                    advisor_screening_round,
                    first_choice_screening_submitted_at,
                    second_choice_screening_submitted_at
                FROM dtlms_recruitment_applications
                WHERE id = %s
                  AND is_deleted = FALSE
                """,
                (application_id,),
            )
            application_row = cur.fetchone()
            if application_row is None:
                raise KeyError("Recruitment application not found")

            stored_candidate_no = str(application_row.get("candidate_no") or "").strip()
            if stored_candidate_no and stored_candidate_no != candidate_no:
                raise ValueError("报名号与申请记录不一致，无法保存评分")

            current_round = str(application_row.get("advisor_screening_round") or "").strip()
            current_status = str(application_row.get("application_status") or "").strip()
            if current_round and current_round not in {screening_round, ""}:
                raise ValueError("当前申请不属于该轮次导师初筛")
            if current_status and current_status not in {"initial_screening_first", "initial_screening_second", "待导师初筛-第一志愿", "待导师初筛-第二志愿"}:
                raise ValueError("当前申请不在导师初筛待提交状态")

            cur.execute(
                f"""
                UPDATE dtlms_recruitment_applications
                SET {score_column} = %s,
                    advisor_screening_round = COALESCE(advisor_screening_round, %s),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND candidate_no = %s
                  AND is_deleted = FALSE
                """,
                (
                    score,
                    screening_round,
                    application_id,
                    candidate_no,
                ),
            )
            if cur.rowcount != 1:
                raise KeyError("Recruitment application not found")
        conn.commit()

    application_detail = query_store.get_recruitment_application_detail(application_id)
    if application_detail is None:
        raise KeyError("Recruitment application not found")
    return RecruitApplicationRecord(**application_detail)
