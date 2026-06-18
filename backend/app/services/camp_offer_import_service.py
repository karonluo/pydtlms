from __future__ import annotations

import re
from datetime import date, datetime
from io import BytesIO
from typing import Any

import psycopg
from openpyxl import load_workbook

from app.core.config import settings
from app.schemas.recruitment import CampOfferImportIssue, CampOfferImportResult


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def _normalize_header(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    if not text:
        return ""
    return re.sub(r"[\s\-_—–()（）\[\]【】{}<>《》:：,，.。/\\]+", "", text)


def _normalize_cell(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        text = value.strip()
        return text or None
    return value


def _parse_bool(value: Any) -> bool | None:
    normalized = _normalize_cell(value)
    if normalized is None:
        return None
    if isinstance(normalized, bool):
        return normalized
    if isinstance(normalized, (int, float)):
        if normalized == 1:
            return True
        if normalized == 0:
            return False
        return None
    text = str(normalized).strip().lower()
    if text in {"true", "1", "yes", "y", "是", "同意"}:
        return True
    if text in {"false", "0", "no", "n", "否", "不同意"}:
        return False
    return None


def _parse_datetime(value: Any) -> datetime | date | None:
    value = _normalize_cell(value)
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value
    if isinstance(value, str):
        text = value.replace("T", " ").strip()
        for parser in (
            datetime.fromisoformat,
            lambda item: datetime.strptime(item, "%Y-%m-%d %H:%M:%S"),
            lambda item: datetime.strptime(item, "%Y-%m-%d %H:%M"),
            lambda item: datetime.strptime(item, "%Y/%m/%d %H:%M:%S"),
            lambda item: datetime.strptime(item, "%Y/%m/%d %H:%M"),
            lambda item: datetime.strptime(item, "%Y-%m-%d"),
        ):
            try:
                parsed = parser(text)
            except Exception:
                continue
            if isinstance(parsed, datetime):
                return parsed
            return datetime.combine(parsed, datetime.min.time())
    return None


def _resolve_header_field(header: str) -> str | None:
    if not header:
        return None
    if header == "candidate_no" or ("报名号" in header and "candidate_no" in header):
        return "candidate_no"
    if header in {"报名号", "candidateno"}:
        return "candidate_no"
    if header in {"planid", "plan_id", "计划id"}:
        return "plan_id"
    if header in {"isagree", "is_agree", "是否同意"}:
        return "is_agree"
    if header in {"reason", "原因", "reson"}:
        return "reason"
    if header in {"issentmail", "is_sent_mail", "是否已发邮件"}:
        return "is_sent_mail"
    if header in {"studentoffersubmittedat", "student_offer_submitted_at", "学生提交日期", "submited"}:
        return "student_offer_submitted_at"
    return None


def _load_import_rows(file_bytes: bytes) -> list[dict[str, Any]]:
    workbook = load_workbook(BytesIO(file_bytes), data_only=True)
    worksheet = workbook.active
    if worksheet is None:
        return []
    rows = list(worksheet.iter_rows(values_only=True))
    if not rows:
        return []

    normalized_header_row = [_normalize_header(value) for value in rows[0]]
    header_index: dict[str, int] = {}
    for index, header in enumerate(normalized_header_row):
        field_name = _resolve_header_field(header)
        if field_name:
            header_index[field_name] = index

    if "candidate_no" not in header_index:
        raise ValueError("导入文件必须包含报名号（candidate_no）列")

    result: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if not any(value not in (None, "") for value in row):
            continue
        item: dict[str, Any] = {"row_number": row_number}
        for field_name, index in header_index.items():
            item[field_name] = _normalize_cell(row[index] if index < len(row) else None)
        result.append(item)
    return result


def _resolve_plan_id(
    raw_plan_id: Any,
    fallback_plan_id: int | None,
    latest_plan_id: int | None,
) -> int | None:
    text = _normalize_cell(raw_plan_id)
    if text not in (None, ""):
        try:
            return int(text)
        except (TypeError, ValueError):
            return None
    if fallback_plan_id is not None:
        return int(fallback_plan_id)
    if latest_plan_id is not None:
        return int(latest_plan_id)
    return None


def _load_latest_plan_id(cur: Any) -> int | None:
    cur.execute(
        """
        SELECT id
        FROM dtlms_recruitment_plans
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    return int(row[0]) if row else None


def _load_existing_candidates(cur: Any, candidate_nos: list[str]) -> set[str]:
    if not candidate_nos:
        return set()
    cur.execute(
        """
        SELECT candidate_no
        FROM dtlms_recruitment_applications
        WHERE is_deleted = FALSE
          AND candidate_no = ANY(%s)
        """,
        (candidate_nos,),
    )
    return {str(row[0]).strip() for row in cur.fetchall() if row and row[0]}


def _load_existing_plan_ids(cur: Any, plan_ids: list[int]) -> set[int]:
    if not plan_ids:
        return set()
    cur.execute(
        """
        SELECT id
        FROM dtlms_recruitment_plans
        WHERE id = ANY(%s)
        """,
        (plan_ids,),
    )
    return {int(row[0]) for row in cur.fetchall() if row and row[0] is not None}


def _load_existing_offer_keys(cur: Any, candidate_nos: list[str], plan_ids: list[int]) -> set[tuple[str, int]]:
    if not candidate_nos or not plan_ids:
        return set()
    cur.execute(
        """
        SELECT candidate_no, plan_id
        FROM dtlms_plan_offer
        WHERE candidate_no = ANY(%s)
          AND plan_id = ANY(%s)
        """,
        (candidate_nos, plan_ids),
    )
    return {(str(row[0]).strip(), int(row[1])) for row in cur.fetchall() if row and row[0] is not None and row[1] is not None}


def import_camp_offers_from_excel(file_bytes: bytes, *, plan_id: int | None = None) -> CampOfferImportResult:
    rows = _load_import_rows(file_bytes)
    if not rows:
        return CampOfferImportResult(
            imported_count=0,
            skipped_count=0,
            plan_id=int(plan_id or 0),
            imported_ids=[],
            issues=[],
        )

    issues: list[CampOfferImportIssue] = []
    latest_plan_id = int(plan_id or 0)
    with psycopg.connect(_conninfo()) as conn:
        with conn.cursor() as cur:
            latest_plan_id = _load_latest_plan_id(cur)
            prepared_rows: list[dict[str, Any]] = []
            candidate_nos: list[str] = []
            plan_ids: list[int] = []
            seen_keys: set[tuple[str, int]] = set()

            for row in rows:
                row_number = int(row["row_number"])
                candidate_no = str(row.get("candidate_no") or "").strip()
                if not candidate_no:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            reason="报名号不能为空",
                        )
                    )
                    continue

                resolved_plan_id = _resolve_plan_id(row.get("plan_id"), plan_id, latest_plan_id)
                if resolved_plan_id is None:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="未找到可用的计划编号",
                        )
                    )
                    continue

                is_sent_mail = _parse_bool(row.get("is_sent_mail"))
                if row.get("is_sent_mail") not in (None, "") and is_sent_mail is None:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="是否已发邮件格式无法识别",
                        )
                    )
                    continue

                is_agree = _parse_bool(row.get("is_agree"))
                if row.get("is_agree") not in (None, "") and is_agree is None:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="是否同意格式无法识别",
                        )
                    )
                    continue

                submitted_at = _parse_datetime(row.get("student_offer_submitted_at"))
                if row.get("student_offer_submitted_at") not in (None, "") and submitted_at is None:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="学生提交日期格式无法识别",
                        )
                    )
                    continue

                key = (candidate_no, int(resolved_plan_id))
                if key in seen_keys:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="文件中重复的报名号和计划编号组合",
                        )
                    )
                    continue
                seen_keys.add(key)
                prepared_rows.append(
                    {
                        "row_number": row_number,
                        "candidate_no": candidate_no,
                        "plan_id": int(resolved_plan_id),
                        "is_sent_mail": is_sent_mail,
                        "is_agree": is_agree,
                        "reason": _normalize_cell(row.get("reason")),
                        "student_offer_submitted_at": submitted_at,
                    }
                )
                candidate_nos.append(candidate_no)
                plan_ids.append(int(resolved_plan_id))

            if not prepared_rows:
                return CampOfferImportResult(
                    imported_count=0,
                    skipped_count=len(rows),
                    plan_id=int(plan_id or latest_plan_id or 0),
                    imported_ids=[],
                    issues=issues,
                )

            existing_candidates = _load_existing_candidates(cur, candidate_nos)
            existing_plan_ids = _load_existing_plan_ids(cur, sorted(set(plan_ids)))
            existing_offer_keys = _load_existing_offer_keys(cur, candidate_nos, sorted(set(plan_ids)))

            valid_rows: list[dict[str, Any]] = []
            for row in prepared_rows:
                row_number = int(row["row_number"])
                candidate_no = str(row["candidate_no"])
                resolved_plan_id = int(row["plan_id"])
                key = (candidate_no, resolved_plan_id)
                if resolved_plan_id not in existing_plan_ids:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason=f"计划编号 {resolved_plan_id} 不存在",
                        )
                    )
                    continue
                if candidate_no not in existing_candidates:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="报名号在招生报名表中不存在",
                        )
                    )
                    continue
                if key in existing_offer_keys:
                    issues.append(
                        CampOfferImportIssue(
                            row_number=row_number,
                            candidate_no=candidate_no,
                            reason="该报名号和计划编号的入营名单已存在",
                        )
                    )
                    continue
                valid_rows.append(row)

            if not valid_rows:
                conn.commit()
                return CampOfferImportResult(
                    imported_count=0,
                    skipped_count=len(rows),
                    plan_id=int(plan_id or latest_plan_id or 0),
                    imported_ids=[],
                    issues=issues,
                )

            cur.execute(
                """
                INSERT INTO dtlms_plan_offer (
                    candidate_no,
                    plan_id,
                    is_sent_mail,
                    is_agree,
                    reson,
                    submitted_at,
                    created_at,
                    updated_at
                )
                SELECT
                    data.candidate_no,
                    data.plan_id,
                    data.is_sent_mail,
                    data.is_agree,
                    data.reson,
                    data.submitted_at,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                FROM UNNEST(
                    %s::text[],
                    %s::bigint[],
                    %s::boolean[],
                    %s::boolean[],
                    %s::text[],
                    %s::timestamptz[]
                ) AS data(candidate_no, plan_id, is_sent_mail, is_agree, reson, submitted_at)
                RETURNING id
                """,
                (
                    [str(row["candidate_no"]) for row in valid_rows],
                    [int(row["plan_id"]) for row in valid_rows],
                    [bool(row["is_sent_mail"]) for row in valid_rows],
                    [row["is_agree"] for row in valid_rows],
                    [row["reason"] for row in valid_rows],
                    [row["student_offer_submitted_at"] for row in valid_rows],
                ),
            )
            imported_ids = [int(item[0]) for item in cur.fetchall()]
            conn.commit()

    skipped_count = len(rows) - len(imported_ids)
    return CampOfferImportResult(
        imported_count=len(imported_ids),
        skipped_count=skipped_count,
        plan_id=int(plan_id or latest_plan_id or 0),
        imported_ids=imported_ids,
        issues=issues,
    )
