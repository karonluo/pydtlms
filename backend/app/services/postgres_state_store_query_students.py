"""Student and portal student PostgreSQL query mixin.

This module contains student master data, portal student, and center queries.
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

class PostgresStateStoreQueryStudentsMixin:
    """Query mixin extracted by functional module."""

    def load_team_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_team_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        t.id,
                        t.team_code,
                        t.team_name,
                        COALESCE(t.department_name, '') AS department_name,
                        COALESCE(t.discipline_name, '') AS discipline_name,
                        t.lead_user_id,
                        COALESCE(lead.full_name, '') AS lead_user_name,
                        COALESCE(advisor_names.advisor_names, ARRAY[]::text[]) AS advisor_names,
                        COALESCE(team_leaders.director_ids, ARRAY[]::bigint[]) AS director_ids,
                        COALESCE(team_leaders.directors_json, '[]'::jsonb) AS directors,
                        COALESCE(advisor_names.advisor_user_ids, ARRAY[]::bigint[]) AS advisor_ids,
                        COALESCE(advisor_names.advisor_relation_ids, ARRAY[]::bigint[]) AS advisor_relation_ids,
                        t.research_directions,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS established_on,
                        t.description
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_users lead ON lead.id = t.lead_user_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT
                            array_agg(tl.user_id ORDER BY u.full_name, tl.user_id) AS director_ids,
                            COALESCE(jsonb_agg(jsonb_build_object('user_id', tl.user_id, 'full_name', u.full_name) ORDER BY u.full_name, tl.user_id), '[]'::jsonb) AS directors_json
                        FROM dtlms_team_leaders tl
                        JOIN dtlms_users u ON u.id = tl.user_id AND u.is_deleted = FALSE
                        WHERE tl.team_id = t.id
                    ) team_leaders ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            array_agg(advisor_rows.advisor_name ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_names,
                            array_agg(advisor_rows.advisor_user_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_user_ids,
                            array_agg(advisor_rows.relation_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_relation_ids
                        FROM (
                            SELECT DISTINCT
                                ta.id AS relation_id,
                                ta.advisor_user_id,
                                COALESCE(advisor.full_name, '') AS advisor_name,
                                1 AS sort_role
                            FROM dtlms_team_advisors ta
                            JOIN dtlms_users advisor ON advisor.id = ta.advisor_user_id AND advisor.is_deleted = FALSE
                            WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                        ) advisor_rows
                    ) advisor_names ON TRUE
                    WHERE t.is_deleted = FALSE
                    ORDER BY t.id DESC
                    """
                )
                rows = cur.fetchall()

        return [
            {
                "id": int(row["id"]),
                "director_ids": [int(item) for item in (row.get("director_ids") or []) if item is not None],
                "directors": [dict(item) for item in (row.get("directors") or []) if item is not None],
                "team_code": row["team_code"],
                "team_name": row["team_name"],
                "discipline_name": row["discipline_name"],
                "lead_user_id": int(row.get("lead_user_id") or 0) or None,
                "lead_user_name": row["lead_user_name"] or None,
                "advisor_names": list(row["advisor_names"] or []),
                "advisor_ids": [int(item) for item in (row.get("advisor_ids") or []) if item is not None],
                "advisor_relation_ids": [int(item) for item in (row.get("advisor_relation_ids") or []) if item is not None],
                "research_directions": self._split_delimited_values(row["research_directions"]),
                "status": self._team_status_label(row["team_status"]),
                "established_on": row["established_on"],
                "description": row["description"],
            }
            for row in rows
        ]

    def load_student_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_student_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        s.id,
                        s.portal_student_id,
                        s.student_no,
                        s.full_name,
                        s.current_status,
                        COALESCE(a.full_name, '') AS advisor_name,
                        COALESCE(t.team_name, '') AS team_name,
                        s.degree_type,
                        s.enrollment_year,
                        s.phone_number,
                        s.political_status
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id AND a.is_deleted = FALSE
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id AND t.is_deleted = FALSE
                    WHERE s.is_deleted = FALSE
                    ORDER BY s.id DESC
                    """
                )
                rows = cur.fetchall()

        return [
            {
                "id": int(row["id"]),
                "portal_student_id": int(row.get("portal_student_id") or 0) or None,
                "student_no": str(row.get("student_no") or ""),
                "full_name": str(row.get("full_name") or ""),
                "status": self._student_status_label(row.get("current_status")),
                "advisor_name": str(row.get("advisor_name") or ""),
                "team_name": str(row.get("team_name") or ""),
                "degree_type": str(row.get("degree_type") or ""),
                "enrollment_year": int(row.get("enrollment_year") or 0),
                "phone_number": row.get("phone_number"),
                "political_status": row.get("political_status"),
            }
            for row in rows
        ]

    def load_portal_student_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_portal_student_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ps.id,
                        ps.full_name,
                        ps.phone_number,
                        ps.email,
                        ps.id_number,
                        ps.account_status,
                        ps.password_hash,
                        ps.gender,
                        ps.birth_date,
                        ps.ethnic_group,
                        ps.native_place,
                        ps.marital_status,
                        ps.religious_belief,
                        ps.id_type,
                        ps.mailing_address,
                        ps.graduation_school,
                        ps.highest_degree,
                        ps.intended_field,
                        ps.political_status,
                        ps.english_level,
                        ps.family_info,
                        ps.education_experience,
                        ps.practice_experience,
                        ps.personal_profile,
                        ps.recommendation_notes,
                        ps.personal_statement_text,
                        ps.signed_agreement,
                        ps.selected_plan_id,
                        ps.selected_team_id,
                        ps.selected_team_name,
                        ps.selected_advisor_user_id,
                        ps.selected_advisor_name,
                        ps.self_evaluation,
                        ps.submitted_at,
                        ps.created_at,
                        ps.updated_at,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone,
                        latest_application.id AS recruitment_application_id,
                        latest_application.business_key AS business_key,
                        latest_application.candidate_no AS candidate_no,
                        latest_application.application_status AS recruitment_application_status,
                        latest_application.applied_at AS recruitment_application_applied_at,
                        COALESCE(resume_attachment.resume_attachment_url, psm.resume_attachment_url) AS resume_attachment_url,
                        resume_attachment.resume_attachment_name,
                        COALESCE(supporting_material_attachment.supporting_material_attachment_url, psm.supporting_material_attachment_url) AS supporting_material_attachment_url,
                        supporting_material_attachment.supporting_material_attachment_name
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    LEFT JOIN LATERAL (
                        SELECT
                            ra.id,
                            ra.business_key,
                            ra.candidate_no,
                            ra.application_status,
                            ra.applied_at
                        FROM dtlms_recruitment_applications ra
                        WHERE ra.is_deleted = FALSE
                          AND ra.portal_student_id = ps.id
                        ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC,
                                 ra.id DESC
                        LIMIT 1
                    ) latest_application ON TRUE
                    LEFT JOIN dtlms_portal_application_personal_statements psm ON psm.application_id = latest_application.id
                    LEFT JOIN LATERAL (
                        SELECT
                            attachment.file_url AS resume_attachment_url,
                            attachment.file_name AS resume_attachment_name
                        FROM dtlms_portal_application_attachments attachment
                        WHERE latest_application.id IS NOT NULL
                          AND attachment.application_id = latest_application.id
                          AND attachment.owner_type = 'personal_statement'
                          AND attachment.owner_id = latest_application.id
                          AND attachment.attachment_category = 'resume'
                          AND COALESCE(NULLIF(BTRIM(attachment.file_url), ''), NULL) IS NOT NULL
                        ORDER BY attachment.id DESC
                        LIMIT 1
                    ) resume_attachment ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            attachment.file_url AS supporting_material_attachment_url,
                            attachment.file_name AS supporting_material_attachment_name
                        FROM dtlms_portal_application_attachments attachment
                        WHERE latest_application.id IS NOT NULL
                          AND attachment.application_id = latest_application.id
                          AND attachment.owner_type = 'portal_application'
                          AND attachment.owner_id = latest_application.id
                          AND attachment.attachment_category = 'materials'
                          AND COALESCE(NULLIF(BTRIM(attachment.file_url), ''), NULL) IS NOT NULL
                        ORDER BY attachment.id DESC
                        LIMIT 1
                    ) supporting_material_attachment ON TRUE
                    ORDER BY ps.id DESC
                    """
                )
                rows = cur.fetchall()

        results: list[dict[str, Any]] = []
        for row in rows:
            student = dict(row)
            profile = self._derive_portal_profile(student)
            if profile is not None:
                student["profile"] = profile
            student.pop("application_draft", None)
            results.append(student)
        return results

    def _build_portal_application_draft_from_tables(self, student: dict[str, Any], application: dict[str, Any] | None) -> dict[str, Any] | None:
        draft: dict[str, Any] = {
            "selected_plan_id": int((application or {}).get("plan_id") or student.get("selected_plan_id") or 0) or None,
            "source_channel": (application or {}).get("source_channel"),
            "source_channel_other": (application or {}).get("source_channel_other"),
            "preferences": [],
            "education_experiences": self._parse_json_list(student.get("education_experience")),
            "practice_experiences": self._parse_json_list(student.get("practice_experience")),
            "english_proficiencies": self._parse_json_list(student.get("english_level")),
            "family_members": self._parse_json_list(student.get("family_info")),
            "achievement_records": self._parse_json_list(student.get("recommendation_notes")),
            "personal_statement": {
                "personal_statement_text": student.get("personal_statement_text"),
                "ai_problem_statement": student.get("research_problem"),
                "ai_industry_opinion": student.get("dissenting_view"),
                "growth_experience_text": student.get("personal_statement_text"),
                "program_application_reason_text": student.get("research_problem"),
                "career_plan_text": student.get("dissenting_view"),
                "resume_attachment_url": None,
                "resume_attachment_name": None,
                "supporting_material_attachment_url": student.get("material_list_attachment"),
                "supporting_material_attachment_name": None,
            },
            "declaration": {
                "has_read_declaration": bool(student.get("signed_agreement")),
            },
            "submitted_at": student.get("submitted_at"),
        }
        has_content = any(value not in (None, "", [], {}) for key, value in draft.items() if key != "selected_plan_id") or draft.get("selected_plan_id") is not None
        return draft if has_content else None

    def get_portal_student_detail(self, student_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_portal_student_detail`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ps.*,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.id_card_collage_url,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    WHERE ps.id = %s
                    """,
                    (int(student_id),),
                )
                row = cur.fetchone()
                if not row:
                    return None
                student = dict(row)
                profile = self._derive_portal_profile(student)
                if profile is not None:
                    student["profile"] = profile
                existing_application_draft = student.get("application_draft") if isinstance(student.get("application_draft"), dict) else None

                selected_plan_id = student.get("selected_plan_id")
                cur.execute(
                    """
                    SELECT id, plan_id, business_key, candidate_no, source_channel, source_channel_other,
                              intended_advisor_name, application_status, applied_at,
                           advisor_screening_status, advisor_screening_round,
                           initial_screening_status, initial_screening_result,
                              first_choice, second_choice,
                                        intended_advisor_user_id
                    FROM dtlms_recruitment_applications
                    WHERE is_deleted = FALSE AND portal_student_id = %s
                    ORDER BY CASE WHEN plan_id = %s THEN 0 ELSE 1 END,
                             COALESCE(applied_at, created_at) DESC,
                             id DESC
                    LIMIT 1
                    """,
                    (int(student_id), int(selected_plan_id) if selected_plan_id is not None else -1),
                )
                application = cur.fetchone()
                if not application:
                    tables_draft = self._build_portal_application_draft_from_tables(student, None)
                    if tables_draft is not None:
                        student["application_draft"] = (
                            self._merge_portal_application_draft(tables_draft, existing_application_draft)
                            or tables_draft
                        )
                    elif existing_application_draft is not None:
                        student["application_draft"] = existing_application_draft
                    return student

                application_id = int(application["id"])
                student["recruitment_application_id"] = application_id
                student["recruitment_application_business_key"] = application.get("business_key")
                student["recruitment_application_candidate_no"] = application.get("candidate_no")
                student["recruitment_application_status"] = application.get("application_status")
                student["recruitment_application_applied_at"] = application.get("applied_at")
                student["first_choice"] = application.get("first_choice")
                student["second_choice"] = application.get("second_choice")
                student["intended_advisor_user_id"] = application.get("intended_advisor_user_id")
                student["intended_advisor_name"] = application.get("intended_advisor_name")
                cur.execute(
                    """
                    SELECT preference_order, advisor_user_id, advisor_name, is_optional
                    FROM dtlms_portal_application_preferences
                    WHERE application_id = %s
                    ORDER BY preference_order ASC, id ASC
                    """,
                    (application_id,),
                )
                preferences = [dict(item) for item in cur.fetchall()]
                if not preferences:
                    first_choice_name = str(application.get("first_choice") or "").strip()
                    second_choice_name = str(application.get("second_choice") or "").strip()
                    if first_choice_name:
                        preferences.append(
                            {
                                "preference_order": 1,
                                "advisor_user_id": application.get("intended_advisor_user_id"),
                                "advisor_name": first_choice_name,
                                "is_optional": False,
                            }
                        )
                    if second_choice_name:
                        preferences.append(
                            {
                                "preference_order": 2,
                                "advisor_user_id": None,
                                "advisor_name": second_choice_name,
                                "is_optional": True,
                            }
                        )
                cur.execute(
                    """
                    SELECT sort_order, education_stage, start_month, end_month, school_name, major_name,
                           average_score, gpa, ranking, verifier_name, verifier_phone,
                              transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                    FROM dtlms_portal_application_education_experiences
                    WHERE application_id = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (application_id,),
                )
                education_experiences = [dict(item) for item in cur.fetchall()]
                student["education_experiences"] = education_experiences
                if not student.get("education_experience") and education_experiences:
                    student["education_experience"] = self._json_payload(education_experiences)
                cur.execute(
                    """
                    SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                           verifier_name, verifier_phone
                    FROM dtlms_portal_application_practice_experiences
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                practice_experiences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT exam_name, score_text, certificate_attachment_url
                    FROM dtlms_portal_application_english_proficiencies
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                english_proficiencies = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT member_name, relation_type, employer_name, job_title, contact_phone
                    FROM dtlms_portal_application_family_members
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
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
                    (application_id,),
                )
                achievement_rows = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT owner_type, owner_id, attachment_category, file_name, file_url
                    FROM dtlms_portal_application_attachments
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                attachment_rows = [dict(item) for item in cur.fetchall()]
                achievement_records = []
                for achievement in achievement_rows:
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
                    (application_id,),
                )
                personal_statement_row = cur.fetchone()
                cur.execute(
                    """
                    SELECT has_read_declaration, declaration_text, progress_snapshot
                    FROM dtlms_portal_application_declarations
                    WHERE application_id = %s
                    """,
                    (application_id,),
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
                    (application_id,),
                )
                background_assessments = [
                    {
                        **dict(item),
                        "assessed_at": self._stringify_datetime(item.get("assessed_at")),
                    }
                    for item in cur.fetchall()
                ]
                application_draft = {
                    "selected_plan_id": int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None,
                    "source_channel": application.get("source_channel"),
                    "source_channel_other": application.get("source_channel_other"),
                    "preferences": preferences,
                    "education_experiences": education_experiences,
                    "practice_experiences": practice_experiences,
                    "english_proficiencies": english_proficiencies,
                    "family_members": family_members,
                    "achievement_records": achievement_records,
                    "personal_statement": dict(personal_statement_row) if personal_statement_row else {},
                    "declaration": dict(declaration_row) if declaration_row else {"has_read_declaration": bool(student.get("signed_agreement"))},
                    "submitted_at": None if self._portal_resubmittable_application_status(application.get("application_status")) else self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at"),
                }
                if self._portal_resubmittable_application_status(application.get("application_status")):
                    merged_application_draft = self._merge_portal_application_draft(application_draft, existing_application_draft)
                else:
                    merged_application_draft = self._merge_portal_application_draft(existing_application_draft, application_draft)
                student["application_draft"] = merged_application_draft or application_draft

                personal_statement = student["application_draft"]["personal_statement"]
                if not personal_statement.get("resume_attachment_url"):
                    personal_statement["resume_attachment_url"] = next(
                        (
                            str(item.get("file_url") or "")
                            for item in attachment_rows
                            if str(item.get("owner_type") or "") == "personal_statement"
                            and int(item.get("owner_id") or 0) == application_id
                            and str(item.get("attachment_category") or "") == "resume"
                            and item.get("file_url")
                        ),
                        None,
                    )
                if not personal_statement.get("supporting_material_attachment_url"):
                    personal_statement["supporting_material_attachment_url"] = next(
                        (
                            str(item.get("file_url") or "")
                            for item in attachment_rows
                            if str(item.get("owner_type") or "") == "portal_application"
                            and int(item.get("owner_id") or 0) == application_id
                            and str(item.get("attachment_category") or "") == "materials"
                            and item.get("file_url")
                        ),
                        None,
                    )
                personal_statement["resume_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "personal_statement",
                    application_id,
                    "resume",
                    personal_statement.get("resume_attachment_url"),
                )
                personal_statement["supporting_material_attachment_name"] = self._resolve_attachment_name(
                    attachment_rows,
                    "portal_application",
                    application_id,
                    "materials",
                    personal_statement.get("supporting_material_attachment_url") or application.get("material_list_attachment"),
                )
                if personal_statement and not personal_statement.get("supporting_material_attachment_url"):
                    personal_statement["supporting_material_attachment_url"] = application.get("material_list_attachment")
                student["business_key"] = application.get("business_key")
                student["candidate_no"] = application.get("candidate_no")
                student["recruitment_application_status"] = self._application_status_label(application.get("application_status"))
                student["advisor_screening_status"] = application.get("advisor_screening_status")
                student["advisor_screening_round"] = application.get("advisor_screening_round")
                student["initial_screening_status"] = application.get("initial_screening_status")
                student["initial_screening_result"] = application.get("initial_screening_result")
                student["background_assessments"] = background_assessments
                if preferences:
                    student["selected_advisor_user_id"] = int(preferences[0].get("advisor_user_id") or application.get("intended_advisor_user_id") or student.get("selected_advisor_user_id") or 0) or None
                    student["selected_advisor_name"] = preferences[0].get("advisor_name") or application.get("intended_advisor_name") or student.get("selected_advisor_name")
                student["selected_plan_id"] = int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None
                student["submitted_at"] = None if self._portal_resubmittable_application_status(application.get("application_status")) else self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at")
                return student

    def list_students_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        advisor_name: str | None = None,
        center_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_students_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["s.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    s.student_no ILIKE %s
                    OR s.full_name ILIKE %s
                    OR COALESCE(t.team_name, '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if status:
            where_clauses.append("s.current_status = %s")
            params.append(self._map_student_status(status))
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if center_name:
            where_clauses.append("COALESCE(t.team_name, '') = %s")
            params.append(center_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        s.id,
                        s.student_no,
                        s.full_name,
                        s.current_status,
                        s.primary_advisor_id AS advisor_id,
                        COALESCE(a.full_name, '') AS advisor_name,
                        COALESCE(t.team_name, '') AS team_name,
                        s.degree_type,
                        s.enrollment_year,
                        s.phone_number,
                        s.political_status
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                    ORDER BY s.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_student_row(dict(row)) for row in cur.fetchall()], total

    def list_registered_portal_students_page(
        self,
        keyword: str | None = None,
        application_form_status: str | None = None,
        recruitment_application_status: str | None = None,
        exclude_background_assessed_username: str | None = None,
        advisor_names: list[str] | None = None,
        first_choice_advisor_names: list[str] | None = None,
        second_choice_advisor_names: list[str] | None = None,
        first_choice_center_names: list[str] | None = None,
        second_choice_center_names: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_registered_portal_students_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    ps.full_name ILIKE %s
                    OR ps.phone_number ILIKE %s
                    OR ps.email ILIKE %s
                    OR ps.id_number ILIKE %s
                    OR COALESCE(rp.plan_name, '') ILIKE %s
                    OR COALESCE(ps.selected_advisor_name, '') ILIKE %s
                    OR COALESCE(ps.selected_team_name, '') ILIKE %s
                    OR COALESCE(latest_application.candidate_no, '') ILIKE %s
                    OR COALESCE(latest_application.business_key, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 9)

        normalized_status = str(application_form_status or "").strip()
        if normalized_status == "已填写报名":
            where_clauses.append("COALESCE(latest_application.application_status, '') <> 'returned'")
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NOT NULL")
        elif normalized_status == "驳回重填":
            where_clauses.append("COALESCE(latest_application.application_status, '') = 'returned'")
        elif normalized_status == "未填写报名":
            where_clauses.append("COALESCE(latest_application.application_status, '') <> 'returned'")
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NULL")

        normalized_recruitment_status = str(recruitment_application_status or "").strip()
        if normalized_recruitment_status:
            candidate_statuses = [normalized_recruitment_status]
            mapped_recruitment_status = self._map_application_status(normalized_recruitment_status)
            if mapped_recruitment_status != normalized_recruitment_status and self._application_status_label(mapped_recruitment_status) == normalized_recruitment_status:
                candidate_statuses.append(mapped_recruitment_status)
            where_clauses.append("COALESCE(latest_application.application_status, '') = ANY(%s)")
            params.append(candidate_statuses)

        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if normalized_advisor_names:
            where_clauses.append("COALESCE(ps.selected_advisor_name, '') = ANY(%s)")
            params.append(normalized_advisor_names)

        normalized_first_choice_advisor_names = [str(item).strip() for item in (first_choice_advisor_names or []) if str(item).strip()]
        if normalized_first_choice_advisor_names:
            where_clauses.append("COALESCE(latest_application.first_choice, '') = ANY(%s)")
            params.append(normalized_first_choice_advisor_names)

        normalized_second_choice_advisor_names = [str(item).strip() for item in (second_choice_advisor_names or []) if str(item).strip()]
        if normalized_second_choice_advisor_names:
            where_clauses.append("COALESCE(latest_application.second_choice, '') = ANY(%s)")
            params.append(normalized_second_choice_advisor_names)

        normalized_first_choice_center_names = [str(item).strip() for item in (first_choice_center_names or []) if str(item).strip()]
        if normalized_first_choice_center_names:
            where_clauses.append("COALESCE(latest_application.first_choice_center_name, '') = ANY(%s)")
            params.append(normalized_first_choice_center_names)

        normalized_second_choice_center_names = [str(item).strip() for item in (second_choice_center_names or []) if str(item).strip()]
        if normalized_second_choice_center_names:
            where_clauses.append("COALESCE(latest_application.second_choice_center_name, '') = ANY(%s)")
            params.append(normalized_second_choice_center_names)

        normalized_background_assessed_username = str(exclude_background_assessed_username or "").strip()
        if normalized_background_assessed_username:
            where_clauses.append(
                """
                (
                    COALESCE(latest_application.application_status, '') <> 'background_review'
                    OR NOT EXISTS (
                        SELECT 1
                        FROM dtlms_background_assessments ba
                        WHERE ba.application_id = latest_application.id
                          AND COALESCE(ba.evaluator_username, '') = %s
                    )
                )
                """
            )
            params.append(normalized_background_assessed_username)

        where_sql = " AND ".join(where_clauses)
        latest_application_sql = """
            LEFT JOIN LATERAL (
                SELECT
                    app.id,
                    app.business_key,
                    app.candidate_no,
                    app.application_status,
                    app.applied_at,
                    app.first_choice,
                    app.second_choice,
                    app.first_choice_screening_score,
                    app.second_choice_screening_score,
                    fc.center_name AS first_choice_center_name,
                    sc.center_name AS second_choice_center_name
                FROM (
                    SELECT
                        ra.id,
                        ra.business_key,
                        ra.candidate_no,
                        ra.application_status,
                        ra.applied_at,
                        ra.first_choice_screening_score,
                        ra.second_choice_screening_score,
                        COALESCE(NULLIF(BTRIM(pref1.advisor_name), ''), NULLIF(BTRIM(ra.first_choice), '')) AS first_choice,
                        COALESCE(NULLIF(BTRIM(pref2.advisor_name), ''), NULLIF(BTRIM(ra.second_choice), '')) AS second_choice
                    FROM dtlms_recruitment_applications ra
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
                    WHERE ra.is_deleted = FALSE AND ra.portal_student_id = ps.id
                    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC,
                             ra.id DESC
                    LIMIT 1
                ) app
                LEFT JOIN LATERAL (
                    SELECT t.team_name AS center_name
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    JOIN dtlms_team_advisors ta ON ta.advisor_user_id = u.id AND ta.is_deleted = FALSE
                    JOIN dtlms_teams t ON t.id = ta.team_id AND t.is_deleted = FALSE
                    WHERE u.full_name = app.first_choice
                      AND u.is_deleted = FALSE
                      AND r.role_code = 'advisor'
                    ORDER BY t.id DESC
                    LIMIT 1
                ) fc ON TRUE
                LEFT JOIN LATERAL (
                    SELECT t.team_name AS center_name
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    JOIN dtlms_team_advisors ta ON ta.advisor_user_id = u.id AND ta.is_deleted = FALSE
                    JOIN dtlms_teams t ON t.id = ta.team_id AND t.is_deleted = FALSE
                    WHERE u.full_name = app.second_choice
                      AND u.is_deleted = FALSE
                      AND r.role_code = 'advisor'
                    ORDER BY t.id DESC
                    LIMIT 1
                ) sc ON TRUE
            ) latest_application ON TRUE
        """

        normalized_sort_by = str(sort_by or "").strip()
        normalized_sort_order = "ASC" if str(sort_order or "").strip().lower() == "asc" else "DESC"
        order_sql = "ORDER BY ps.created_at DESC, ps.id DESC"
        if normalized_sort_by == "first_choice_screening_score":
            order_sql = f"ORDER BY latest_application.first_choice_screening_score {normalized_sort_order} NULLS LAST, ps.created_at DESC, ps.id DESC"
        elif normalized_sort_by == "second_choice_screening_score":
            order_sql = f"ORDER BY latest_application.second_choice_screening_score {normalized_sort_order} NULLS LAST, ps.created_at DESC, ps.id DESC"

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        ps.id,
                        ps.full_name,
                        ps.phone_number,
                        ps.email,
                        ps.id_number,
                        ps.account_status,
                        rp.plan_name AS selected_plan_name,
                        ps.selected_team_name,
                        ps.selected_advisor_name,
                        latest_application.first_choice,
                        latest_application.second_choice,
                        ps.created_at,
                        ps.submitted_at,
                        latest_application.id AS recruitment_application_id,
                        latest_application.candidate_no AS recruitment_application_candidate_no,
                        latest_application.business_key AS recruitment_application_business_key,
                        latest_application.application_status,
                        latest_application.applied_at,
                        latest_application.first_choice,
                        latest_application.second_choice,
                        latest_application.first_choice_center_name,
                        latest_application.second_choice_center_name,
                        latest_application.first_choice_screening_score,
                        latest_application.second_choice_screening_score
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                    {order_sql}
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_registered_portal_student_row(dict(row)) for row in cur.fetchall()], total

    def list_centers_page(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        # 旧入参 director_id（单值）保留以兼容老调用方，新代码请使用 director_ids（多值）
        director_id: int | None = None,
        director_ids: list[int] | None = None,
        principal: Any | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_centers_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        # 兼容处理：director_id（单值）合并进 director_ids（多值）；director_ids 优先
        _filter_director_ids: list[int] = list(director_ids or [])
        if director_id and int(director_id) not in _filter_director_ids:
            _filter_director_ids.append(int(director_id))

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.team_name ILIKE %s
                    OR COALESCE(lead.full_name, '') ILIKE %s
                    OR EXISTS (
                        SELECT 1
                        FROM dtlms_team_advisors ta_keyword
                        JOIN dtlms_users advisor_keyword ON advisor_keyword.id = ta_keyword.advisor_user_id AND advisor_keyword.is_deleted = FALSE
                        WHERE ta_keyword.team_id = t.id
                          AND ta_keyword.is_deleted = FALSE
                          AND advisor_keyword.full_name ILIKE %s
                    )
                )
                """
            )
            params.extend([keyword_like] * 3)
        if is_enabled is not None:
            where_clauses.append("t.team_status = %s" if is_enabled else "t.team_status <> %s")
            params.append("active")
        # 旧：COALESCE(t.lead_user_id, lead.id, 0) = %s  (单值)
        # 新：EXISTS 查 dtlms_team_leaders 拿多值
        if _filter_director_ids:
            where_clauses.append(
                "EXISTS (SELECT 1 FROM dtlms_team_leaders tl WHERE tl.team_id = t.id AND tl.user_id = ANY(%s::bigint[]))"
            )
            params.append([int(v) for v in _filter_director_ids if int(v or 0) > 0])
            if not username:
                return [], 0
            where_clauses.append(
                """
                (
                    EXISTS (
                        SELECT 1
                        FROM dtlms_team_leaders tl_scope
                        JOIN dtlms_users u_scope ON u_scope.id = tl_scope.user_id
                        WHERE tl_scope.team_id = t.id
                          AND u_scope.username = %s
                          AND u_scope.is_deleted = FALSE
                    )
                    OR EXISTS (
                        SELECT 1
                        FROM dtlms_team_advisors ta_scope
                        JOIN dtlms_users advisor_scope ON advisor_scope.id = ta_scope.advisor_user_id AND advisor_scope.is_deleted = FALSE
                        WHERE ta_scope.team_id = t.id
                          AND ta_scope.is_deleted = FALSE
                          AND advisor_scope.username = %s
                          AND advisor_scope.is_deleted = FALSE
                    )
                )
                """
            )
            params.extend([username, username])

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_users lead ON lead.id = t.lead_user_id AND lead.is_deleted = FALSE
                    WHERE {where_sql}
                """
                self._execute_dynamic(cur, count_sql, params)
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        t.id,
                        t.team_name,
                        t.lead_user_id AS director_id,
                        COALESCE(lead.full_name, '') AS director_name,
                        COALESCE(team_leaders.director_ids, ARRAY[]::bigint[]) AS director_ids,
                        COALESCE(team_leaders.directors_json, '[]'::jsonb) AS directors,
                        COALESCE(advisor_names.advisor_names, '') AS advisor_names,
                        COALESCE(advisor_names.advisor_ids, ARRAY[]::bigint[]) AS advisor_ids,
                        COALESCE(advisor_names.advisor_relation_ids, ARRAY[]::bigint[]) AS advisor_relation_ids,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS created_date,
                        COALESCE(student_stats.member_student_count, 0) AS member_student_count,
                        COALESCE(student_stats.active_student_count, 0) AS active_student_count,
                        COALESCE(student_stats.student_count, 0) AS student_count
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_users lead ON lead.id = t.lead_user_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT
                            array_agg(tl.user_id ORDER BY u.full_name, tl.user_id) AS director_ids,
                            COALESCE(jsonb_agg(jsonb_build_object('user_id', tl.user_id, 'full_name', u.full_name) ORDER BY u.full_name, tl.user_id), '[]'::jsonb) AS directors_json
                        FROM dtlms_team_leaders tl
                        JOIN dtlms_users u ON u.id = tl.user_id AND u.is_deleted = FALSE
                        WHERE tl.team_id = t.id
                    ) team_leaders ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            string_agg(advisor_rows.advisor_name, '、' ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_names,
                            COALESCE(array_agg(advisor_rows.advisor_name ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id), ARRAY[]::text[]) AS advisor_names_arr,
                            array_agg(advisor_rows.advisor_user_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_ids,
                            array_agg(advisor_rows.relation_id ORDER BY advisor_rows.sort_role, advisor_rows.advisor_name, advisor_rows.relation_id) AS advisor_relation_ids
                        FROM (
                            SELECT DISTINCT
                                ta.id AS relation_id,
                                ta.advisor_user_id AS advisor_user_id,
                                advisor.full_name AS advisor_name,
                                1 AS sort_role
                            FROM dtlms_team_advisors ta
                            JOIN dtlms_users advisor ON advisor.id = ta.advisor_user_id AND advisor.is_deleted = FALSE
                            WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                        ) advisor_rows
                    ) advisor_names ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            COUNT(*) AS member_student_count,
                            COUNT(*) FILTER (WHERE s.current_status IN ('enrolled', 'internship', 'outbound', 'thesis')) AS active_student_count,
                            (
                                SELECT COUNT(DISTINCT offer.candidate_no)
                                FROM dtlms_plan_offer offer
                                JOIN dtlms_recruitment_applications app
                                    ON app.candidate_no = offer.candidate_no
                                       AND app.is_deleted = FALSE
                                WHERE offer.submitted_at IS NOT NULL
                                  AND offer.is_agree = TRUE
                                  AND (
                                        (app.first_choice_screening_score >= 80
                                            AND app.first_choice = ANY (advisor_names.advisor_names_arr))
                                     OR (app.second_choice_screening_score >= 80
                                            AND app.second_choice = ANY (advisor_names.advisor_names_arr))
                                  )
                            ) AS student_count
                        FROM dtlms_students s
                        WHERE s.team_id = t.id AND s.is_deleted = FALSE
                    ) student_stats ON TRUE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                """
                self._execute_dynamic(cur, page_sql, [*params, page_size, offset])
                return [self._normalize_center_row(dict(row)) for row in cur.fetchall()], total

    def list_active_advisors(self) -> list[dict[str, Any]]:
        """Execute query logic for `list_active_advisors`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                                        SELECT
                                                u.id,
                                                u.full_name,
                                                advisor_match.advisor_no,
                                                COALESCE(advisor_match.organization_name, NULLIF(u.department_name, ''), '未分配单位') AS organization_name,
                                                NULLIF(up.introduction, '') AS introduction
                                        FROM dtlms_users u
                                        JOIN dtlms_user_roles ur ON ur.user_id = u.id
                                        JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                                        LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                                        LEFT JOIN LATERAL (
                                                SELECT a.advisor_no, a.organization_name
                                                FROM dtlms_advisors a
                                                WHERE a.is_deleted = FALSE
                                                    AND a.user_id = u.id
                                                ORDER BY a.id
                                                LIMIT 1
                                        ) advisor_match ON TRUE
                                        WHERE u.is_deleted = FALSE
                                            AND u.is_active = TRUE
                                            AND r.role_code = 'advisor'
                                        ORDER BY u.full_name ASC, u.id ASC
                    """
                )
                rows = [dict(row) for row in cur.fetchall()]
                if not rows:
                    cur.execute(
                        """
                                                SELECT id, full_name, NULL::varchar AS advisor_no, department_name AS organization_name, NULL::text AS introduction
                                                FROM dtlms_users
                                                WHERE is_deleted = FALSE
                                                    AND is_active = TRUE
                                                ORDER BY full_name ASC, id ASC
                        """
                    )
                    rows = [dict(row) for row in cur.fetchall()]
                return rows