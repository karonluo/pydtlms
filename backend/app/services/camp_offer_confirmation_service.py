from __future__ import annotations

from typing import Any

import psycopg
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
OFFER_CONFIRM_DEADLINE_HOURS = 24


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def _normalize_text(value: Any) -> str:
    return str(value or "").strip()


def _normalize_choice(choice: str) -> bool:
    normalized = _normalize_text(choice).lower()
    if normalized in {"确认", "同意", "accept", "agree", "yes", "true", "1"}:
        return True
    if normalized in {"拒绝", "拒绝参营", "reject", "refuse", "no", "false", "0"}:
        return False
    raise ValueError("请选择确认或拒绝")


def _row_value(row: tuple[Any, ...] | None, index: int) -> Any:
    if row is None or index < 0 or index >= len(row):
        return None
    return row[index]


def submit_camp_offer_confirmation(email: str, password: str, choice: str) -> dict[str, Any]:
    email = _normalize_text(email)
    password = _normalize_text(password)
    choice = _normalize_text(choice)
    if not email:
        raise ValueError("邮箱不能为空")
    if not password:
        raise ValueError("密码不能为空")

    agreed = _normalize_choice(choice)
    with psycopg.connect(_conninfo()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, password_hash, full_name
                FROM dtlms_portal_students
                WHERE email = %s
                LIMIT 1
                """,
                (email,),
            )
            student = cur.fetchone()
            if not student:
                raise ValueError("未找到该学生邮箱对应的账号")

            password_hash = _normalize_text(_row_value(student, 2))
            if not password_hash or not pwd_context.verify(password, password_hash):
                raise ValueError("账号或密码错误")

            cur.execute(
                """
                SELECT id, portal_student_id, candidate_no
                FROM dtlms_recruitment_applications
                WHERE portal_student_id = %s
                  AND is_deleted = FALSE
                ORDER BY id DESC
                LIMIT 1
                """,
                (int(_row_value(student, 0) or 0),),
            )
            application_row = cur.fetchone()
            if not application_row:
                raise ValueError("未找到该学生对应的报名申请")

            candidate_no = _normalize_text(_row_value(application_row, 2))
            if not candidate_no:
                raise ValueError("该报名申请缺少报名号")

            cur.execute(
                """
                SELECT id
                FROM dtlms_recruitment_plans
                ORDER BY id DESC
                LIMIT 1
                """
            )
            plan_row = cur.fetchone()
            resolved_plan_id = int(_row_value(plan_row, 0) or 0)
            if resolved_plan_id <= 0:
                raise ValueError("无法确定最新报名计划")

            cur.execute(
                """
                SELECT id, candidate_no, plan_id, portal_student_id, submitted_at, is_agree, sent_mail_at
                FROM dtlms_plan_offer
                WHERE candidate_no = %s
                  AND plan_id = %s
                ORDER BY id DESC
                LIMIT 1
                FOR UPDATE
                """,
                (candidate_no, resolved_plan_id),
            )
            existing_offer = cur.fetchone()

            if existing_offer is None:
                raise ValueError("当前暂未对您开放邀请")

            existing_portal_student_id = _row_value(existing_offer, 3)
            submitted_at = _row_value(existing_offer, 4)
            offer_id = int(_row_value(existing_offer, 0) or 0)
            offer_sent_mail_at = _row_value(existing_offer, 6)

            if existing_portal_student_id is not None and int(existing_portal_student_id) != int(_row_value(student, 0) or 0):
                raise ValueError("邮箱与该报名号下的入营名单记录不一致")

            if not _normalize_text(_row_value(student, 1)):
                raise ValueError("该报名号下没有邮箱，非要求勿填写，请先补齐再提交")

            if submitted_at is not None:
                raise ValueError("该学生已经提交过确认结果")

            if offer_sent_mail_at is not None:
                cur.execute(
                    """
                    SELECT (CURRENT_TIMESTAMP - %s) > make_interval(hours => %s) AS is_overdue
                    """
                , (offer_sent_mail_at, OFFER_CONFIRM_DEADLINE_HOURS))
                deadline_row = cur.fetchone()
                is_overdue = bool(_row_value(deadline_row, 0)) if deadline_row is not None else False
                if is_overdue:
                    raise ValueError("已经超时无法提交")
            else:
                raise ValueError("邀请邮件尚未发出，请等待邮件通知后再提交")

            cur.execute(
                """
                UPDATE dtlms_plan_offer
                SET
                    is_agree = %s,
                    portal_student_id = %s,
                    submitted_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    agreed,
                    int(_row_value(student, 0) or 0),
                    offer_id,
                ),
            )
            conn.commit()

    return {
        "student_name": _normalize_text(_row_value(student, 3)),
        "email": email,
        "candidate_no": candidate_no,
        "plan_id": resolved_plan_id,
        "is_agree": agreed,
        "updated": True,
        "offer_id": offer_id,
    }
