"""Recruitment PostgreSQL query mixin.

This module contains recruitment plan, application, and advisor-choice queries.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)

class PostgresStateStoreQueryRecruitmentMixin:
    """Query mixin extracted by functional module."""

    def _advisor_user_id_by_username(self, username: str | None) -> int | None:
        normalized_username = str(username or "").strip()
        if not normalized_username:
            return None
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM dtlms_users WHERE username = %s AND is_deleted = FALSE LIMIT 1",
                    (normalized_username,),
                )
                row = cur.fetchone()
        if row is None:
            return None
        return int(row["id"] or 0) or None

    def get_recruitment_application_detail(self, application_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_recruitment_application_detail`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ra.*,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.gender,
                        pp.birth_date,
                        pp.ethnic_group,
                        pp.native_place,
                        pp.political_status,
                        pp.marital_status,
                        pp.religious_belief,
                        pp.id_type,
                        pp.mailing_address,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone,
                        rf.field_name AS intended_field,
                        am.material_status,
                        qr.reviewer_username AS reviewer_name,
                        ad.final_score
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT material_status
                        FROM dtlms_application_materials
                        WHERE application_id = ra.id AND is_deleted = FALSE
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) am ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT reviewer_username
                        FROM dtlms_qualification_reviews
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) qr ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT final_score
                        FROM dtlms_admission_decisions
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) ad ON TRUE
                    WHERE ra.id = %s AND ra.is_deleted = FALSE
                    """,
                    (int(application_id),),
                )
                application_row = cur.fetchone()
                if application_row is None:
                    return None

                cur.execute(
                    """
                    SELECT owner_type, owner_id, attachment_category, file_name, file_url
                    FROM dtlms_portal_application_attachments
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                attachment_rows = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT preference_order, advisor_name, is_optional
                    FROM dtlms_portal_application_preferences
                    WHERE application_id = %s
                    ORDER BY preference_order ASC, id ASC
                    """,
                    (int(application_id),),
                )
                preferences = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, sort_order, education_stage, start_month, end_month, school_name, major_name,
                           average_score, gpa, ranking, verifier_name, verifier_phone,
                              transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                    FROM dtlms_portal_application_education_experiences
                    WHERE application_id = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (int(application_id),),
                )
                education_experiences: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    education = dict(item)
                    education_id = int(education.get("id") or 0)
                    transcript_url = education.get("transcript_attachment_url")
                    degree_url = education.get("degree_certificate_attachment_url")
                    graduation_url = education.get("graduation_certificate_attachment_url")
                    education["transcript_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "transcript", transcript_url
                    )
                    education["degree_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "degree_certificate", degree_url
                    )
                    education["graduation_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows, "education_experience", education_id, "graduation_certificate", graduation_url
                    )
                    education.pop("id", None)
                    education_experiences.append(education)

                cur.execute(
                    """
                    SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                           verifier_name, verifier_phone
                    FROM dtlms_portal_application_practice_experiences
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                practice_experiences = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, exam_name, score_text, certificate_attachment_url
                    FROM dtlms_portal_application_english_proficiencies
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                english_proficiencies: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    english = dict(item)
                    english_id = int(english.get("id") or 0)
                    english["certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows,
                        "english_proficiency",
                        english_id,
                        "english_certificate",
                        english.get("certificate_attachment_url"),
                    )
                    english.pop("id", None)
                    english_proficiencies.append(english)

                cur.execute(
                    """
                    SELECT member_name, relation_type, employer_name, job_title, contact_phone
                    FROM dtlms_portal_application_family_members
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                family_members = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT id, achievement_type, paper_title, author_order, journal_or_conference,
                           publish_or_index_month, achievement_month, award_name, award_rank,
                           award_certificate_attachment_url, awarding_organization, award_level,
                           award_year, description_text, responsibility_text
                    FROM dtlms_portal_application_achievement_records
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (int(application_id),),
                )
                achievement_records: list[dict[str, Any]] = []
                for item in cur.fetchall():
                    achievement = dict(item)
                    achievement_id = int(achievement.get("id") or 0)
                    achievement["award_certificate_attachment_name"] = self._resolve_attachment_name(
                        attachment_rows,
                        "achievement_record",
                        achievement_id,
                        "achievement_award_certificate",
                        achievement.get("award_certificate_attachment_url"),
                    )
                    achievement.pop("id", None)
                    achievement_records.append(achievement)

                cur.execute(
                    """
                    SELECT
                        personal_statement_text,
                        growth_experience_text,
                        program_application_reason_text,
                        career_plan_text,
                        resume_attachment_url,
                        supporting_material_attachment_url,
                        ai_problem_statement,
                        ai_industry_opinion
                    FROM dtlms_portal_application_personal_statements
                    WHERE application_id = %s
                    """,
                    (int(application_id),),
                )
                personal_statement_row = cur.fetchone()
                personal_statement = dict(personal_statement_row) if personal_statement_row else {}
                personal_statement["resume_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "personal_statement",
                    int(application_id),
                    "resume",
                    personal_statement.get("resume_attachment_url") if personal_statement else None,
                )
                personal_statement["supporting_material_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    int(application_id),
                    "materials",
                    (
                        personal_statement.get("supporting_material_attachment_url")
                        if personal_statement
                        else application_row.get("material_list_attachment")
                    )
                    or application_row.get("material_list_attachment"),
                )
                if personal_statement and not personal_statement.get("supporting_material_attachment_url"):
                    personal_statement["supporting_material_attachment_url"] = application_row.get("material_list_attachment")

                cur.execute(
                    """
                    SELECT has_read_declaration, declaration_text, progress_snapshot
                    FROM dtlms_portal_application_declarations
                    WHERE application_id = %s
                    """,
                    (int(application_id),),
                )
                declaration_row = cur.fetchone()

                cur.execute(
                    """
                    SELECT
                        evaluator_user_id,
                        evaluator_username,
                        evaluator_name,
                        evaluator_role_code,
                        assessment_result,
                        assessment_comment,
                        assessed_at
                    FROM dtlms_background_assessments
                    WHERE application_id = %s
                    ORDER BY assessed_at ASC, id ASC
                    """,
                    (int(application_id),),
                )
                background_assessments = [dict(item) for item in cur.fetchall()]

                cur.execute(
                    """
                    SELECT
                        reviewer_username,
                        reviewer_name,
                        reviewer_role_code,
                        action,
                        action_label,
                        review_comment,
                        reviewed_at
                    FROM dtlms_qualification_review_logs
                    WHERE application_id = %s
                    ORDER BY reviewed_at DESC, id DESC
                    """,
                    (int(application_id),),
                )
                qualification_review_history = [dict(item) for item in cur.fetchall()]

                screening_round = str(application_row.get("advisor_screening_round") or "").strip()
                current_screening_batch_id = (
                    int(application_row.get("second_choice_screening_batch_id") or 0)
                    if screening_round == "second_choice"
                    else int(application_row.get("first_choice_screening_batch_id") or 0)
                ) or None
                if current_screening_batch_id is None:
                    current_screening_batch_id = int(application_row.get("first_choice_screening_batch_id") or 0) or int(application_row.get("second_choice_screening_batch_id") or 0) or None

                advisor_screening_batch: dict[str, Any] = {}
                if current_screening_batch_id is not None:
                    cur.execute(
                        """
                        SELECT signature_base64, submitted_at
                        FROM dtlms_advisor_screening_batches
                        WHERE id = %s
                        LIMIT 1
                        """,
                        (int(current_screening_batch_id),),
                    )
                    advisor_screening_batch_row = cur.fetchone()
                    if advisor_screening_batch_row is not None:
                        advisor_screening_batch = dict(advisor_screening_batch_row)

                application = self._normalize_recruitment_application_row(dict(application_row))
                profile = self._derive_portal_profile(dict(application_row))
                if profile is not None:
                    application["profile"] = profile
                application["background_assessments"] = [
                    {
                        **item,
                        "assessed_at": self._stringify_datetime(item.get("assessed_at")),
                    }
                    for item in background_assessments
                ]
                application["qualification_review_history"] = [
                    {
                        **item,
                        "reviewed_at": self._stringify_datetime(item.get("reviewed_at")),
                    }
                    for item in qualification_review_history
                ]
                application["preferences"] = preferences
                application["education_experiences"] = education_experiences
                application["practice_experiences"] = practice_experiences
                application["english_proficiencies"] = english_proficiencies
                application["family_members"] = family_members
                application["achievement_records"] = achievement_records
                application["personal_statement"] = personal_statement
                application["declaration"] = dict(declaration_row) if declaration_row else {"has_read_declaration": False}
                application["advisor_signature_base64"] = advisor_screening_batch.get("signature_base64")
                application["advisor_screening_submitted_at"] = self._stringify_datetime(
                    advisor_screening_batch.get("submitted_at")
                    or application.get("second_choice_screening_submitted_at")
                    or application.get("first_choice_screening_submitted_at")
                )
                application["material_list_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    int(application_id),
                    "materials",
                    application.get("material_list_attachment"),
                )
                return application

    def load_recruitment_plan_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_recruitment_plan_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        rp.id,
                        rp.plan_name,
                        rp.academic_year,
                        rp.semester,
                        rp.brochure_image_url,
                        rp.plan_description,
                        rp.plan_status,
                        rp.target_quota,
                        COUNT(ra.id) FILTER (WHERE ra.is_deleted = FALSE) AS application_count
                    FROM dtlms_recruitment_plans rp
                    LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id
                    WHERE rp.is_deleted = FALSE
                    GROUP BY rp.id, rp.plan_name, rp.academic_year, rp.semester, rp.brochure_image_url, rp.plan_description, rp.plan_status, rp.target_quota
                    ORDER BY rp.id DESC
                    """
                )
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for row in rows:
            normalized = self._normalize_recruitment_plan_row(dict(row))
            normalized["current_stage"] = str(row.get("plan_status") or "报名配置")
            normalized["target_quota"] = int(row.get("target_quota") or 0)
            normalized["interview_group_count"] = 0
            normalized["is_open"] = True
            results.append(normalized)
        return results

    def load_recruitment_application_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_recruitment_application_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ra.*, 
                        rf.field_name AS intended_field
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id
                    WHERE ra.is_deleted = FALSE
                    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    """
                )
                rows = cur.fetchall()
        return [self._normalize_recruitment_application_row(dict(row)) for row in rows]

    def list_recruitment_plans_page(
        self,
        keyword: str | None = None,
        semester: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_recruitment_plans_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["rp.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    rp.plan_name ILIKE %s
                    OR CONCAT_WS(' ', COALESCE(rp.academic_year, ''), COALESCE(rp.semester, '')) ILIKE %s
                    OR COALESCE(rp.plan_description, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if semester:
            where_clauses.append("rp.semester = %s")
            params.append(semester)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_recruitment_plans rp
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        rp.id,
                        rp.plan_name,
                        rp.academic_year,
                        rp.semester,
                        rp.brochure_image_url,
                        rp.plan_description,
                        COUNT(ra.id) FILTER (WHERE ra.is_deleted = FALSE) AS application_count
                    FROM dtlms_recruitment_plans rp
                    LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id
                    WHERE {where_sql}
                    GROUP BY rp.id, rp.plan_name, rp.academic_year, rp.semester, rp.brochure_image_url, rp.plan_description
                    ORDER BY rp.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_recruitment_plan_row(dict(row)) for row in cur.fetchall()], total

    def list_recruitment_applications_page(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        portal_student_only: bool = False,
        advisor_name: str | None = None,
        advisor_names: list[str] | None = None,
        advisor_user_id: int | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_recruitment_applications_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["app.is_deleted = FALSE"]
        params: list[Any] = []

        if plan_id is not None:
            where_clauses.append("app.plan_id = %s")
            params.append(int(plan_id))
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                "(stu.full_name ILIKE %s OR app.candidate_no ILIKE %s OR app.business_key ILIKE %s)"
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        normalized_status = str(status or "").strip()
        if normalized_status:
            if normalized_status == "advisor_screening_pending":
                where_clauses.append("app.application_status LIKE %s")
                params.append("initial_screening_%")
                where_clauses.append("app.application_status <> 'initial_screening_confirmation'")
                where_clauses.append("app.advisor_screening_status = 'pending'")
            elif normalized_status == "initial_screening_confirmation":
                where_clauses.append("app.application_status = 'initial_screening_confirmation'")
                where_clauses.append("(app.first_choice_screening_score >= 80 OR app.second_choice_screening_score >= 80)")
                where_clauses.append(
                    "(app.first_choice_screening_submitted_at IS NOT NULL OR app.second_choice_screening_submitted_at IS NOT NULL)"
                )
            else:
                status_values = [item.strip() for item in normalized_status.split(",") if item.strip()]
                if len(status_values) > 1:
                    where_clauses.append("app.application_status = ANY(%s)")
                    params.append(status_values)
                else:
                    where_clauses.append("app.application_status = %s")
                    params.append(status_values[0] if status_values else normalized_status)

        effective_advisor_user_id = advisor_user_id
        if effective_advisor_user_id is None:
            effective_advisor_user_id = self._advisor_user_id_by_username(advisor_name)
        if effective_advisor_user_id is not None:
            normalized_advisor_name = str(advisor_name or "").strip()
            if normalized_advisor_name:
                where_clauses.append(
                    "(app.intended_advisor_name = %s OR app.intended_advisor_user_id = %s)"
                )
                params.extend([normalized_advisor_name, int(effective_advisor_user_id)])
            else:
                where_clauses.append("app.intended_advisor_user_id = %s")
                params.append(int(effective_advisor_user_id))
        elif advisor_name and str(advisor_name).strip():
            normalized_advisor_name = str(advisor_name).strip()
            where_clauses.append("app.intended_advisor_name = %s")
            params.append(normalized_advisor_name)

        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if normalized_advisor_names:
            where_clauses.append("app.intended_advisor_name = ANY(%s)")
            params.append(normalized_advisor_names)
        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_recruitment_applications app
                    LEFT JOIN dtlms_portal_students stu ON stu.id = app.portal_student_id
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        app.*
                    FROM dtlms_recruitment_applications app
                    LEFT JOIN dtlms_portal_students stu ON stu.id = app.portal_student_id
                    WHERE {where_sql}
                    ORDER BY app.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_recruitment_application_row(dict(row)) for row in cur.fetchall()], total

    def _normalize_camp_offer_row(self, row: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(row)
        normalized["candidate_no"] = str(normalized.get("candidate_no") or "").strip()
        normalized["plan_id"] = int(normalized.get("plan_id") or 0)
        normalized["is_sent_mail"] = bool(normalized.get("is_sent_mail") or False)
        normalized["is_agree"] = normalized.get("is_agree")
        normalized["reason"] = str(normalized.get("reason") or "").strip() or None
        normalized["student_name"] = str(normalized.get("student_name") or "").strip() or None
        normalized["student_email"] = str(normalized.get("student_email") or "").strip() or None
        normalized["student_phone"] = str(normalized.get("student_phone") or "").strip() or None
        normalized["first_choice_advisor_name"] = str(normalized.get("first_choice_advisor_name") or "").strip() or None
        normalized["first_choice_advisor_team_name"] = str(normalized.get("first_choice_advisor_team_name") or "").strip() or None
        normalized["first_choice_screening_score"] = self._to_optional_float(normalized.get("first_choice_screening_score"))
        normalized["second_choice_advisor_name"] = str(normalized.get("second_choice_advisor_name") or "").strip() or None
        normalized["second_choice_advisor_team_name"] = str(normalized.get("second_choice_advisor_team_name") or "").strip() or None
        normalized["second_choice_screening_score"] = self._to_optional_float(normalized.get("second_choice_screening_score"))
        normalized["created_at"] = self._stringify_datetime(normalized.get("created_at"))
        normalized["student_offer_submitted_at"] = self._stringify_datetime(normalized.get("student_offer_submitted_at"))
        return normalized

    def get_latest_recruitment_plan_id(self) -> int | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id
                    FROM dtlms_recruitment_plans
                    WHERE is_deleted = FALSE
                    ORDER BY id DESC
                    LIMIT 1
                    """
                )
                row = cur.fetchone()
        if row is None:
            return None
        return int(row["id"] or 0) or None

    def list_camp_offers_page(
        self,
        *,
        keyword: str | None = None,
        plan_id: int | None = None,
        is_sent_mail: bool | None = None,
        is_agree: bool | None = None,
        first_choice_advisor: str | None = None,
        first_choice_team: str | None = None,
        first_choice_score_op: str | None = None,
        first_choice_score: float | None = None,
        second_choice_advisor: str | None = None,
        second_choice_team: str | None = None,
        second_choice_score_op: str | None = None,
        second_choice_score: float | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1=1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(offer.candidate_no ILIKE %s OR COALESCE(app.student_name, '') ILIKE %s)")
            params.extend([keyword_like, keyword_like])
        if plan_id is not None:
            where_clauses.append("offer.plan_id = %s")
            params.append(int(plan_id))
        if is_sent_mail is not None:
            where_clauses.append("COALESCE(offer.is_sent_mail, FALSE) = %s")
            params.append(bool(is_sent_mail))
        if is_agree is not None:
            where_clauses.append("offer.is_agree = %s")
            params.append(bool(is_agree))
        if first_choice_advisor and str(first_choice_advisor).strip():
            where_clauses.append("app.first_choice ILIKE %s")
            params.append("%" + str(first_choice_advisor).strip() + "%")
        if first_choice_team and str(first_choice_team).strip():
            where_clauses.append("first_team.team_names ILIKE %s")
            params.append("%" + str(first_choice_team).strip() + "%")
        _score_ops = { "eq": "=", "ne": "<>", "gt": ">", "ge": ">=", "lt": "<", "le": "<=" }
        if first_choice_score is not None and first_choice_score_op in _score_ops:
            where_clauses.append("app.first_choice_screening_score " + _score_ops[first_choice_score_op] + " %s")
            params.append(float(first_choice_score))
        if second_choice_advisor and str(second_choice_advisor).strip():
            where_clauses.append("app.second_choice ILIKE %s")
            params.append("%" + str(second_choice_advisor).strip() + "%")
        if second_choice_team and str(second_choice_team).strip():
            where_clauses.append("second_team.team_names ILIKE %s")
            params.append("%" + str(second_choice_team).strip() + "%")
        if second_choice_score is not None and second_choice_score_op in _score_ops:
            where_clauses.append("app.second_choice_screening_score " + _score_ops[second_choice_score_op] + " %s")
            params.append(float(second_choice_score))

        where_sql = " AND ".join(where_clauses)

        normalized_sort_by = str(sort_by or "").strip()
        normalized_sort_order = "ASC" if str(sort_order or "").strip().lower() == "asc" else "DESC"
        order_sql = "ORDER BY offer.created_at DESC NULLS LAST, offer.id DESC"
        if normalized_sort_by == "first_choice_screening_score":
            order_sql = f"ORDER BY app.first_choice_screening_score {normalized_sort_order} NULLS LAST, offer.created_at DESC NULLS LAST, offer.id DESC"
        elif normalized_sort_by == "second_choice_screening_score":
            order_sql = f"ORDER BY app.second_choice_screening_score {normalized_sort_order} NULLS LAST, offer.created_at DESC NULLS LAST, offer.id DESC"

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_plan_offer offer
                    LEFT JOIN dtlms_recruitment_applications app ON app.candidate_no = offer.candidate_no AND app.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.first_choice
                    ) first_team ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.second_choice
                    ) second_team ON TRUE
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        offer.id,
                        offer.candidate_no,
                        offer.plan_id,
                        plan.plan_name,
                        COALESCE(offer.is_sent_mail, FALSE) AS is_sent_mail,
                        offer.is_agree,
                        COALESCE(offer.reson, '') AS reason,
                        app.student_name,
                        ps.email AS student_email,
                        ps.phone_number AS student_phone,
                        app.first_choice AS first_choice_advisor_name,
                        first_team.team_names AS first_choice_advisor_team_name,
                        app.first_choice_screening_score,
                        app.second_choice AS second_choice_advisor_name,
                        second_team.team_names AS second_choice_advisor_team_name,
                        app.second_choice_screening_score,
                        offer.created_at,
                        offer.submitted_at AS student_offer_submitted_at
                    FROM dtlms_plan_offer offer
                    LEFT JOIN dtlms_recruitment_plans plan ON plan.id = offer.plan_id
                    LEFT JOIN LATERAL (
                        SELECT
                            student_name,
                            portal_student_id,
                            first_choice,
                            first_choice_screening_score,
                            second_choice,
                            second_choice_screening_score
                        FROM dtlms_recruitment_applications app2
                        WHERE app2.candidate_no = offer.candidate_no AND app2.is_deleted = FALSE
                        ORDER BY app2.id DESC
                        LIMIT 1
                    ) app ON TRUE
                    LEFT JOIN dtlms_portal_students ps ON ps.id = app.portal_student_id
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.first_choice
                    ) first_team ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.second_choice
                    ) second_team ON TRUE
                    WHERE {where_sql}
                    {order_sql}
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                rows = [self._normalize_camp_offer_row(dict(row)) for row in cur.fetchall()]
                return rows, total

    def get_camp_offer_detail(self, offer_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        offer.id,
                        offer.candidate_no,
                        offer.plan_id,
                        plan.plan_name,
                        COALESCE(offer.is_sent_mail, FALSE) AS is_sent_mail,
                        offer.is_agree,
                        COALESCE(offer.reson, '') AS reason,
                        app.student_name,
                        ps.email AS student_email,
                        ps.phone_number AS student_phone,
                        app.first_choice AS first_choice_advisor_name,
                        first_team.team_names AS first_choice_advisor_team_name,
                        app.first_choice_screening_score,
                        app.second_choice AS second_choice_advisor_name,
                        second_team.team_names AS second_choice_advisor_team_name,
                        app.second_choice_screening_score,
                        offer.created_at,
                        offer.submitted_at AS student_offer_submitted_at
                    FROM dtlms_plan_offer offer
                    LEFT JOIN dtlms_recruitment_plans plan ON plan.id = offer.plan_id
                    LEFT JOIN LATERAL (
                        SELECT
                            student_name,
                            portal_student_id,
                            first_choice,
                            first_choice_screening_score,
                            second_choice,
                            second_choice_screening_score
                        FROM dtlms_recruitment_applications app2
                        WHERE app2.candidate_no = offer.candidate_no AND app2.is_deleted = FALSE
                        ORDER BY app2.id DESC
                        LIMIT 1
                    ) app ON TRUE
                    LEFT JOIN dtlms_portal_students ps ON ps.id = app.portal_student_id
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.first_choice
                    ) first_team ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT string_agg(team.team_name, ',') AS team_names
                        FROM dtlms_team_advisors adv
                        LEFT JOIN dtlms_users u ON adv.advisor_user_id = u.id
                        LEFT JOIN dtlms_teams team ON adv.team_id = team.id
                        WHERE u.full_name = app.second_choice
                    ) second_team ON TRUE
                    WHERE offer.id = %s
                    LIMIT 1
                    """,
                    (int(offer_id),),
                )
                row = cur.fetchone()
        if row is None:
            return None
        return self._normalize_camp_offer_row(dict(row))

    def find_camp_offer_by_candidate_plan(self, *, candidate_no: str, plan_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        normalized_candidate_no = str(candidate_no or "").strip()
        if not normalized_candidate_no:
            return None
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id
                    FROM dtlms_plan_offer
                    WHERE candidate_no = %s AND plan_id = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (normalized_candidate_no, int(plan_id)),
                )
                row = cur.fetchone()
        return dict(row) if row else None

    def list_background_assessments(self, application_id: int) -> list[dict[str, Any]]:
        """Execute query logic for `list_background_assessments`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        application_id,
                        evaluator_user_id,
                        evaluator_username,
                        evaluator_name,
                        evaluator_role_code,
                        assessment_result,
                        assessment_comment,
                        assessed_at,
                        created_at,
                        updated_at
                    FROM dtlms_background_assessments
                    WHERE application_id = %s
                    ORDER BY assessed_at ASC, id ASC
                    """,
                    (int(application_id),),
                )
                rows = [dict(item) for item in cur.fetchall()]
        return [
            {
                **row,
                "assessed_at": self._stringify_datetime(row.get("assessed_at")),
                "created_at": self._stringify_datetime(row.get("created_at")),
                "updated_at": self._stringify_datetime(row.get("updated_at")),
            }
            for row in rows
        ]

    def list_dashboard_recruitment_advisor_choice_distribution(self) -> dict[str, Any]:
        """Execute query logic for `list_dashboard_recruitment_advisor_choice_distribution`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT
                            ps.id AS portal_student_id,
                            ra.id AS recruitment_application_id
                        FROM dtlms_portal_students ps
                        LEFT JOIN LATERAL (
                            SELECT ra.id, ra.intended_advisor_name, ra.application_status, ra.applied_at
                            FROM dtlms_recruitment_applications ra
                            WHERE ra.portal_student_id = ps.id
                              AND ra.is_deleted = FALSE
                                                        ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC,
                                     ra.id DESC
                            LIMIT 1
                        ) ra ON TRUE
                        WHERE (
                            COALESCE(ra.application_status, '') IN ('returned', '驳回重填')
                            OR (
                                COALESCE(ra.application_status, '') NOT IN ('returned', '驳回重填')
                                AND COALESCE(ps.submitted_at, ra.applied_at) IS NOT NULL
                            )
                        )
                    ),
                    choice_rows AS (
                        SELECT
                            'first_choice' AS choice_round,
                            NULLIF(BTRIM(pref1.advisor_name), '') AS advisor_name
                        FROM latest_application
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = latest_application.recruitment_application_id
                              AND pref.preference_order = 1
                            LIMIT 1
                        ) pref1 ON TRUE
                        UNION ALL
                        SELECT
                            'second_choice' AS choice_round,
                            NULLIF(BTRIM(pref2.advisor_name), '') AS advisor_name
                        FROM latest_application
                        LEFT JOIN LATERAL (
                            SELECT NULLIF(BTRIM(pref.advisor_name), '') AS advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = latest_application.recruitment_application_id
                              AND pref.preference_order = 2
                            LIMIT 1
                        ) pref2 ON TRUE
                    ),
                    choice_counts AS (
                        SELECT choice_round, advisor_name, COUNT(*)::int AS student_count
                        FROM choice_rows
                        WHERE advisor_name IS NOT NULL AND BTRIM(advisor_name) <> ''
                        GROUP BY choice_round, advisor_name
                    ),
                    ranked_counts AS (
                        SELECT
                            choice_round,
                            advisor_name,
                            student_count,
                            ROW_NUMBER() OVER (PARTITION BY choice_round ORDER BY student_count DESC, advisor_name ASC)::int AS advisor_rank,
                            SUM(student_count) OVER (PARTITION BY choice_round)::int AS total
                        FROM choice_counts
                    ),
                    bucketed_counts AS (
                        SELECT
                            choice_round,
                            CASE WHEN advisor_rank <= 10 THEN advisor_name ELSE '其他导师' END AS advisor_name,
                            CASE WHEN advisor_rank <= 10 THEN advisor_rank ELSE 11 END AS bucket_order,
                            SUM(student_count)::int AS student_count,
                            MAX(total)::int AS total
                        FROM ranked_counts
                        GROUP BY choice_round, CASE WHEN advisor_rank <= 10 THEN advisor_name ELSE '其他导师' END, CASE WHEN advisor_rank <= 10 THEN advisor_rank ELSE 11 END
                    )
                    SELECT
                        choice_round,
                        CASE choice_round
                            WHEN 'first_choice' THEN '第一志愿导师'
                            WHEN 'second_choice' THEN '第二志愿导师'
                            ELSE choice_round
                        END AS choice_name,
                        total,
                        advisor_name,
                        student_count,
                        ROUND(student_count * 100.0 / NULLIF(total, 0), 2)::float AS percentage,
                        bucket_order
                    FROM bucketed_counts
                    ORDER BY CASE choice_round WHEN 'first_choice' THEN 1 WHEN 'second_choice' THEN 2 ELSE 3 END, bucket_order ASC, advisor_name ASC
                    """
                )
                choices: dict[str, dict[str, Any]] = {
                    "first_choice": {"choice_round": "first_choice", "choice_name": "第一志愿导师", "total": 0, "items": []},
                    "second_choice": {"choice_round": "second_choice", "choice_name": "第二志愿导师", "total": 0, "items": []},
                }
                for row in cur.fetchall():
                    choice_round = str(row.get("choice_round") or "")
                    if choice_round not in choices:
                        continue
                    total = int(row.get("total") or 0)
                    student_count = int(row.get("student_count") or 0)
                    choices[choice_round]["total"] = total
                    choices[choice_round]["items"].append(
                        {
                            "advisor_name": str(row.get("advisor_name") or ""),
                            "student_count": student_count,
                            "percentage": float(row.get("percentage") or 0),
                        }
                    )

                return {"choices": [choices["first_choice"], choices["second_choice"]]}

    def list_dashboard_recruitment_advisor_choice_students(
        self,
        *,
        choice_round: str,
        advisor_name: str | None = None,
        bucket: str | None = None,
    ) -> list[dict[str, Any]]:
        """Execute query logic for `list_dashboard_recruitment_advisor_choice_students`."""
        self.ensure_schema()
        normalized_choice_round = str(choice_round or "").strip()
        normalized_advisor_name = str(advisor_name or "").strip()
        normalized_bucket = str(bucket or "").strip().lower()
        if normalized_choice_round not in {"first_choice", "second_choice"}:
            return []

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    WITH latest_application AS (
                        SELECT
                            ps.id AS portal_student_id,
                            ps.full_name AS student_name,
                            ps.phone_number,
                            ps.email,
                            ps.created_at AS registered_at,
                            ra.id AS recruitment_application_id,
                            ra.candidate_no,
                            NULLIF(BTRIM(ra.undergraduate_school), '') AS school_name,
                            NULLIF(BTRIM(ps.selected_advisor_name), '') AS selected_advisor_name,
                            NULLIF(BTRIM(ra.intended_advisor_name), '') AS intended_advisor_name,
                            NULLIF(BTRIM(pref1.advisor_name), '') AS first_choice_advisor_name,
                            NULLIF(BTRIM(pref2.advisor_name), '') AS second_choice_advisor_name
                        FROM dtlms_portal_students ps
                        LEFT JOIN LATERAL (
                                                        SELECT ra.id, ra.candidate_no, ra.undergraduate_school, ra.intended_advisor_name, ra.application_status, ra.applied_at
                            FROM dtlms_recruitment_applications ra
                            WHERE ra.portal_student_id = ps.id
                              AND ra.is_deleted = FALSE
                                                        ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC,
                                     ra.id DESC
                            LIMIT 1
                        ) ra ON TRUE
                        LEFT JOIN LATERAL (
                            SELECT pref.advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = ra.id
                              AND pref.preference_order = 1
                            ORDER BY pref.id ASC
                            LIMIT 1
                        ) pref1 ON TRUE
                        LEFT JOIN LATERAL (
                            SELECT pref.advisor_name
                            FROM dtlms_portal_application_preferences pref
                            WHERE pref.application_id = ra.id
                              AND pref.preference_order = 2
                            ORDER BY pref.id ASC
                            LIMIT 1
                        ) pref2 ON TRUE
                        WHERE (
                            COALESCE(ra.application_status, '') IN ('returned', '驳回重填')
                            OR (
                                COALESCE(ra.application_status, '') NOT IN ('returned', '驳回重填')
                                AND COALESCE(ps.submitted_at, ra.applied_at) IS NOT NULL
                            )
                        )
                    ),
                    choice_rows AS (
                        SELECT
                            recruitment_application_id,
                            student_name,
                            phone_number,
                            email,
                            registered_at,
                            candidate_no,
                            school_name,
                            'first_choice' AS choice_round,
                            first_choice_advisor_name AS advisor_name
                        FROM latest_application
                        UNION ALL
                        SELECT
                            recruitment_application_id,
                            student_name,
                            phone_number,
                            email,
                            registered_at,
                            candidate_no,
                            school_name,
                            'second_choice' AS choice_round,
                            second_choice_advisor_name AS advisor_name
                        FROM latest_application
                    ),
                    choice_counts AS (
                        SELECT choice_round, advisor_name, COUNT(*)::int AS student_count
                        FROM choice_rows
                        WHERE advisor_name IS NOT NULL AND BTRIM(advisor_name) <> ''
                        GROUP BY choice_round, advisor_name
                    ),
                    ranked_counts AS (
                        SELECT
                            choice_round,
                            advisor_name,
                            ROW_NUMBER() OVER (PARTITION BY choice_round ORDER BY student_count DESC, advisor_name ASC)::int AS advisor_rank
                        FROM choice_counts
                    ),
                    selected_advisors AS (
                        SELECT advisor_name
                        FROM ranked_counts
                        WHERE choice_round = %s
                          AND (
                              (%s = 'other' AND advisor_rank > 10)
                              OR (%s <> 'other' AND advisor_name = %s)
                          )
                    )
                    SELECT
                        cr.recruitment_application_id,
                        cr.student_name,
                        cr.choice_round,
                        cr.advisor_name,
                        cr.school_name,
                        cr.candidate_no,
                        cr.registered_at,
                        cr.phone_number,
                        cr.email
                    FROM choice_rows cr
                    JOIN selected_advisors sa ON sa.advisor_name = cr.advisor_name
                    WHERE cr.choice_round = %s
                    ORDER BY cr.registered_at DESC NULLS LAST, cr.recruitment_application_id DESC
                    """,
                    (
                        normalized_choice_round,
                        normalized_bucket,
                        normalized_bucket,
                        normalized_advisor_name,
                        normalized_choice_round,
                    ),
                )
                return [
                    {
                        "recruitment_application_id": int(row.get("recruitment_application_id") or 0),
                        "student_name": str(row.get("student_name") or ""),
                        "choice_round": str(row.get("choice_round") or ""),
                        "advisor_name": row.get("advisor_name"),
                        "school_name": row.get("school_name"),
                        "candidate_no": row.get("candidate_no"),
                        "registered_at": self._stringify_datetime(row.get("registered_at")),
                        "phone_number": row.get("phone_number"),
                        "email": row.get("email"),
                    }
                    for row in cur.fetchall()
                ]
