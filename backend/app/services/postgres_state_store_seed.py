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


class PostgresStateStoreSeedMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    @staticmethod
    def _execute_dynamic(
        cur: psycopg.Cursor[Any],
        query: str,
        params: Any | None = None,
    ) -> None:
        cur.execute(cast(Any, query), params)

    @staticmethod
    def _require_scalar_row(row: Any, context: str) -> Any:
        if row is None:
            raise RuntimeError(f"Expected row for {context}")
        return row

    def _seed_relational_tables(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        self._seed_users_and_roles(cur, state)
        advisor_map = self._seed_advisors(cur, state)
        team_map = self._seed_teams(cur, state, advisor_map)
        student_map = self._seed_students(cur, state, advisor_map, team_map)
        plan_map, field_map, group_ids = self._seed_recruitment(cur, state)
        training_plan_map = self._seed_training(cur, state, student_map, advisor_map)
        self._seed_portal_students(cur, state, plan_map)
        self._seed_recruitment_applications(cur, state, plan_map, field_map, group_ids)
        self._seed_portal_application_structures(cur, state)
        thesis_map = self._seed_degree(cur, state, student_map, advisor_map)
        self._seed_operation_logs(cur, state)
        self._seed_sync_logs(cur, state)
        self._seed_notification_delivery_logs(cur, state)
        self._seed_system_configs(cur, state)
        self._seed_training_plan_versions(cur, state, training_plan_map)
        self._seed_admission_decisions(cur, state, plan_map)
        self._seed_thesis_reviews(cur, state, thesis_map)
        self._seed_workflow_engine(cur, state)

    def _seed_users_and_roles(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        from app.core.security import get_password_hash

        cur.execute("TRUNCATE TABLE dtlms_user_roles, dtlms_users RESTART IDENTITY CASCADE")
        users = state.get("system_users", [])
        profiles = state.get("profiles", {})
        role_id_map = self._fetch_map(cur, "SELECT id, role_code AS key FROM dtlms_roles")

        for item in users:
            profile = profiles.get(item["username"], {})
            password_hash = item.get("password_hash") or get_password_hash("ChangeMe@123456")
            cur.execute(
                """
                INSERT INTO dtlms_users (id, username, full_name, email, password_hash, is_active, is_deleted)
                VALUES (%s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["username"],
                    item["full_name"],
                    profile.get("email"),
                    password_hash,
                    item.get("account_status") == "启用",
                ),
            )
            role_id = role_id_map.get(item["role_code"])
            if role_id:
                cur.execute(
                    "INSERT INTO dtlms_user_roles (user_id, role_id, grant_source) VALUES (%s, %s, %s)",
                    (int(item["id"]), int(role_id), "runtime_seed"),
                )

    def _seed_advisors(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_student_advisor_history, dtlms_advisors RESTART IDENTITY CASCADE")
        names: list[str] = []
        for dataset in ("students", "training_plans", "outbound_studies", "theses"):
            for item in state.get(dataset, []):
                advisor_name = item.get("advisor_name")
                if advisor_name and advisor_name not in names:
                    names.append(advisor_name)

        advisor_map: dict[str, int] = {}
        for index, name in enumerate(names, start=1):
            title = "教授" if index % 2 else "副教授"
            organization = "智能制造学院" if name in {"刘亚", "袁野"} else "工业软件学院"
            direction = "博士生培养与过程治理" if name == "袁野" else "智能制造与工业互联网"
            cur.execute(
                """
                INSERT INTO dtlms_advisors (id, advisor_no, full_name, title, organization_name, research_direction, annual_quota, is_deleted)
                VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (index, f"ADV{index:03d}", name, title, organization, direction, 6 + index),
            )
            advisor_map[name] = index
        return advisor_map

    def _seed_teams(self, cur: psycopg.Cursor[Any], state: dict[str, Any], advisor_map: dict[str, int]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_student_team_history, dtlms_team_advisors, dtlms_teams RESTART IDENTITY CASCADE")
        team_map: dict[str, int] = {}
        for item in state.get("teams", []):
            team_id = int(item["id"])
            lead_advisor_name = item.get("lead_advisor_name")
            lead_advisor_id = advisor_map.get(lead_advisor_name) if lead_advisor_name else None
            cur.execute(
                """
                INSERT INTO dtlms_teams (
                    id, team_code, team_name, department_name, discipline_name, lead_advisor_id,
                    research_directions, team_status, established_on, description, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    team_id,
                    item["team_code"],
                    item["team_name"],
                    item.get("department_name") or "未分配院系",
                    item.get("discipline_name"),
                    lead_advisor_id,
                    self._normalize_research_directions(item.get("research_directions")),
                    self._map_team_status(item.get("status", "启用")),
                    item.get("established_on"),
                    item.get("description"),
                ),
            )
            team_map[item["team_name"]] = team_id

            advisor_names = self._normalize_name_list(item.get("advisor_names"))
            if lead_advisor_name and lead_advisor_name not in advisor_names:
                advisor_names.insert(0, lead_advisor_name)

            inserted_advisors: set[int] = set()
            for advisor_name in advisor_names:
                advisor_id = advisor_map.get(advisor_name)
                if not advisor_id or advisor_id in inserted_advisors:
                    continue
                inserted_advisors.add(advisor_id)
                advisor_role = "lead" if advisor_name == lead_advisor_name else "member"
                cur.execute(
                    """
                    INSERT INTO dtlms_team_advisors (
                        team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted
                    ) VALUES (%s, %s, %s, %s, NULL, FALSE)
                    """,
                    (team_id, advisor_id, advisor_role, item.get("established_on")),
                )
        return team_map

    def _seed_students(self, cur: psycopg.Cursor[Any], state: dict[str, Any], advisor_map: dict[str, int], team_map: dict[str, int]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_students RESTART IDENTITY CASCADE")
        student_map: dict[str, int] = {}
        for item in state.get("students", []):
            status = self._map_student_status(item.get("status", "在校"))
            team_id = team_map.get(item.get("team_name")) if item.get("team_name") else None
            cur.execute(
                """
                INSERT INTO dtlms_students (
                    id, portal_student_id, student_no, full_name, gender, political_status, phone_number, identity_no,
                    enrollment_year, degree_type, team_id, current_status, primary_advisor_id, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    int(item.get("portal_student_id") or 0) or None,
                    item["student_no"],
                    item["full_name"],
                    "未知",
                    item.get("political_status"),
                    item.get("phone_number"),
                    f"ID-{item['student_no']}",
                    int(item["enrollment_year"]),
                    item["degree_type"],
                    team_id,
                    status,
                    advisor_map.get(item.get("advisor_name")),
                ),
            )
            student_map[item["student_no"]] = int(item["id"])
            if team_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_student_team_history (student_id, team_id, start_date, end_date, change_reason)
                    VALUES (%s, %s, %s, NULL, %s)
                    """,
                    (int(item["id"]), team_id, f"{item['enrollment_year']}-09-01", "初始化导入"),
                )
            advisor_id = advisor_map.get(item.get("advisor_name"))
            if advisor_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_student_advisor_history (student_id, advisor_id, relation_type, start_date, end_date, change_reason)
                    VALUES (%s, %s, 'primary', %s, NULL, %s)
                    """,
                    (int(item["id"]), advisor_id, f"{item['enrollment_year']}-09-01", "初始化导入"),
                )
        return student_map

    def _seed_recruitment(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> tuple[dict[int, int], dict[str, int], dict[str, Any]]:
        cur.execute(
            "TRUNCATE TABLE dtlms_admission_decisions, dtlms_written_exam_scores, dtlms_interview_scores, "
            "dtlms_interview_schedules, dtlms_interview_groups, dtlms_material_scores, dtlms_reviewer_assignments, "
            "dtlms_qualification_reviews, dtlms_application_materials, dtlms_recruitment_applications, "
            "dtlms_research_fields, dtlms_recruitment_plans RESTART IDENTITY CASCADE"
        )

        field_names = sorted({item["intended_field"] for item in state.get("recruitment_applications", []) if item.get("intended_field")})
        field_map: dict[str, int] = {}
        for index, field_name in enumerate(field_names, start=1):
            cur.execute(
                "INSERT INTO dtlms_research_fields (id, field_code, field_name, description, is_deleted) VALUES (%s, %s, %s, %s, FALSE)",
                (index, f"FIELD{index:03d}", field_name, f"{field_name}方向"),
            )
            field_map[field_name] = index

        plan_map: dict[int, int] = {}
        for item in state.get("recruitment_plans", []):
            plan_status = self._map_plan_status(item.get("current_stage", "资格审核"), item.get("is_open", True))
            academic_year_start = self._normalize_academic_year_start(item.get("academic_year"))
            cur.execute(
                """
                INSERT INTO dtlms_recruitment_plans (
                    id, plan_code, plan_name, academic_year, semester, plan_description, start_date, end_date, target_quota, plan_status, brochure_image_url, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    f"PLAN-{item['id']:03d}",
                    item["plan_name"],
                    item["academic_year"],
                    item["semester"],
                    item.get("plan_description"),
                    f"{academic_year_start}-03-01 08:00:00+08",
                    f"{academic_year_start}-10-31 18:00:00+08",
                    int(item["target_quota"]),
                    plan_status,
                    item.get("brochure_image_url"),
                ),
            )
            plan_map[int(item["id"])] = int(item["id"])

            for group_index in range(1, int(item.get("interview_group_count", 0)) + 1):
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_groups (plan_id, group_code, group_name, interview_mode, is_deleted)
                    VALUES (%s, %s, %s, %s, FALSE)
                    """,
                    (int(item["id"]), f"G{group_index:02d}", f"第{group_index}面试组", "offline"),
                )

        group_ids = self._fetch_map(cur, "SELECT id, (plan_id::text || ':' || group_code) AS key FROM dtlms_interview_groups")
        return plan_map, field_map, group_ids

    def _seed_recruitment_applications(
        self,
        cur: psycopg.Cursor[Any],
        state: dict[str, Any],
        plan_map: dict[int, int],
        field_map: dict[str, int],
        group_ids: dict[str, Any],
    ) -> None:
        application_rows = state.get("recruitment_applications", [])
        portal_students = state.get("portal_students", [])
        for item in application_rows:
            matched_student = next(
                (
                    student for student in portal_students
                    if int(student.get("id") or 0) == int(item.get("portal_student_id") or 0)
                ),
                None,
            )
            if matched_student is None:
                matched_student = next(
                    (
                        student for student in portal_students
                        if int(student.get("selected_plan_id") or 0) == int(item.get("plan_id") or 0)
                        and (
                            (student.get("phone_number") and student.get("phone_number") == item.get("phone_number"))
                            or (student.get("email") and student.get("email") == item.get("email"))
                            or (student.get("id_number") and student.get("id_number") == item.get("id_number"))
                        )
                    ),
                    None,
                )
            draft = self._derive_portal_application_draft(matched_student) if matched_student else None
            application_status = self._map_application_status(item.get("application_status", "报名已提交"))
            application_columns = [
                "id",
                "plan_id",
                "portal_student_id",
                "business_key",
                "student_name",
                "candidate_no",
                "gender",
                "graduation_school",
                "highest_degree",
                "intended_field_id",
                "application_status",
                "review_round",
                "first_choice",
                "second_choice",
                "political_status",
                "marital_status",
                "religious_belief",
                "native_place",
                "phone_number",
                "email",
                "mailing_address",
                "id_type",
                "id_number",
                "undergraduate_school",
                "accept_adjustment",
                "undergraduate_average_score",
                "undergraduate_gpa",
                "undergraduate_rank",
                "undergraduate_major",
                "graduate_average_score",
                "graduate_gpa",
                "graduate_rank",
                "graduate_major",
                "intended_advisor_name",
                "discovery_channel",
                "source_channel",
                "source_channel_other",
                "graduate_school",
                "overseas_university_name",
                "overseas_master_university_name",
                "self_evaluation",
                "applied_at",
                "research_problem",
                "research_status_analysis",
                "research_impact",
                "ai_society_impact",
                "dissenting_view",
                "family_info",
                "education_experience",
                "practice_experience",
                "personal_statement_text",
                "student_activity_experience",
                "personal_statement_attachment",
                "material_list_attachment",
                "supplementary_profile",
            ]
            application_values = (
                int(item["id"]),
                plan_map[int(item["plan_id"])],
                int(item.get("portal_student_id") or (matched_student.get("id") if matched_student else 0) or 0)
                if matched_student or item.get("portal_student_id")
                else None,
                item.get("business_key") or item["candidate_no"],
                item["student_name"],
                item["candidate_no"],
                item.get("gender") or "未知",
                item.get("graduation_school"),
                item.get("highest_degree"),
                field_map.get(item.get("intended_field")),
                application_status,
                item.get("review_round"),
                item.get("first_choice"),
                item.get("second_choice"),
                item.get("political_status"),
                item.get("marital_status"),
                item.get("religious_belief"),
                item.get("native_place"),
                item.get("phone_number"),
                item.get("email"),
                item.get("mailing_address"),
                item.get("id_type"),
                item.get("id_number"),
                item.get("undergraduate_school"),
                item.get("accept_adjustment"),
                item.get("undergraduate_average_score"),
                item.get("undergraduate_gpa"),
                item.get("undergraduate_rank"),
                item.get("undergraduate_major"),
                item.get("graduate_average_score"),
                item.get("graduate_gpa"),
                item.get("graduate_rank"),
                item.get("graduate_major"),
                item.get("intended_advisor_name"),
                item.get("discovery_channel"),
                item.get("source_channel") or (draft or {}).get("source_channel"),
                item.get("source_channel_other") or (draft or {}).get("source_channel_other"),
                item.get("graduate_school"),
                item.get("overseas_university_name"),
                item.get("overseas_master_university_name"),
                item.get("self_evaluation"),
                item.get("applied_at"),
                item.get("research_problem"),
                item.get("research_status_analysis"),
                item.get("research_impact"),
                item.get("ai_society_impact"),
                item.get("dissenting_view"),
                item.get("family_info"),
                item.get("education_experience"),
                item.get("practice_experience"),
                item.get("personal_statement_text"),
                item.get("student_activity_experience"),
                item.get("personal_statement_attachment"),
                item.get("material_list_attachment"),
                item.get("supplementary_profile"),
            )
            self._execute_dynamic(
                cur,
                f"INSERT INTO dtlms_recruitment_applications ({', '.join(application_columns)}, is_deleted) VALUES ({', '.join(['%s'] * len(application_columns))}, FALSE)",
                application_values,
            )
            cur.execute(
                "INSERT INTO dtlms_application_materials (application_id, material_type, material_status, file_url, is_deleted) VALUES (%s, %s, %s, %s, FALSE)",
                (
                    int(item["id"]),
                    "报名材料",
                    self._map_material_status(item.get("material_status", "待补材料")),
                    item.get("material_list_attachment") or f"/materials/{item['candidate_no']}.zip",
                ),
            )
            reviewer = item.get("reviewer_name") or "system.auto"
            cur.execute(
                "INSERT INTO dtlms_qualification_reviews (application_id, reviewer_username, review_status, review_comment) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), reviewer, self._map_review_status(application_status), f"导入状态：{item.get('application_status') or '报名已提交'}"),
            )
            cur.execute(
                "INSERT INTO dtlms_reviewer_assignments (application_id, reviewer_username, reviewer_role, assignment_status) VALUES (%s, %s, %s, %s) RETURNING id",
                (int(item["id"]), reviewer, "reviewer", "assigned"),
            )
            reviewer_assignment_row = self._require_scalar_row(cur.fetchone(), "reviewer assignment id")
            reviewer_assignment_id = int(reviewer_assignment_row[0])
            cur.execute(
                "INSERT INTO dtlms_material_scores (application_id, reviewer_assignment_id, material_score, recommendation_text) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), reviewer_assignment_id, item.get("final_score"), "按模拟数据导入"),
            )
            group_key = f"{item['plan_id']}:G01"
            interview_group_id = group_ids.get(group_key)
            if interview_group_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_schedules (
                        application_id, interview_group_id, admission_ticket_no, starts_at, ends_at, schedule_status
                    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (
                        int(item["id"]),
                        int(interview_group_id),
                        f"TKT-{item['candidate_no']}",
                        "2026-04-18 09:00:00+08",
                        "2026-04-18 09:30:00+08",
                        "completed" if item.get("final_score") is not None else "scheduled",
                    ),
                )
                schedule_row = self._require_scalar_row(cur.fetchone(), "interview schedule id")
                schedule_id = int(schedule_row[0])
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_scores (
                        schedule_id, evaluator_username, single_choice_score, fill_blank_score, coding_score,
                        interview_score, ideological_score
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (schedule_id, reviewer, None, None, None, item.get("final_score"), 95.0),
                )
            cur.execute(
                "INSERT INTO dtlms_written_exam_scores (application_id, exam_date, exam_score, import_batch_no) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), "2026-03-20", item.get("final_score"), "SIM-2026-01"),
            )

    def _seed_portal_students(self, cur: psycopg.Cursor[Any], state: dict[str, Any], plan_map: dict[int, int]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_portal_students RESTART IDENTITY CASCADE")
        for item in state.get("portal_students", []):
            selected_plan_id = item.get("selected_plan_id")
            cur.execute(
                """
                INSERT INTO dtlms_portal_students (
                    id, full_name, phone_number, email, id_number, password_hash, gender, birth_date,
                    ethnic_group, native_place, marital_status, religious_belief, id_type, mailing_address,
                    graduation_school, highest_degree, intended_field, political_status, english_level,
                    family_info, education_experience, practice_experience, personal_profile,
                    recommendation_notes, personal_statement_text, signed_agreement, selected_plan_id,
                    selected_team_name, selected_advisor_name, self_evaluation, application_draft, submitted_at, account_status, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(item["id"]),
                    item["full_name"],
                    item["phone_number"],
                    item["email"],
                    item["id_number"],
                    item.get("password_hash"),
                    item.get("gender"),
                    item.get("birth_date"),
                    item.get("ethnic_group"),
                    item.get("native_place"),
                    item.get("marital_status"),
                    item.get("religious_belief"),
                    item.get("id_type"),
                    item.get("mailing_address"),
                    item.get("graduation_school"),
                    item.get("highest_degree"),
                    item.get("intended_field"),
                    item.get("political_status"),
                    item.get("english_level"),
                    item.get("family_info"),
                    item.get("education_experience"),
                    item.get("practice_experience"),
                    item.get("personal_profile"),
                    item.get("recommendation_notes"),
                    item.get("personal_statement_text"),
                    bool(item.get("signed_agreement")),
                    plan_map.get(int(selected_plan_id)) if selected_plan_id else None,
                    item.get("selected_team_name"),
                    item.get("selected_advisor_name"),
                    item.get("self_evaluation"),
                    self._json_payload(item.get("application_draft")) if item.get("application_draft") else None,
                    item.get("submitted_at"),
                    self._normalize_portal_account_status(item.get("account_status")),
                    item.get("created_at"),
                    item.get("updated_at"),
                ),
            )

    def _seed_portal_application_structures(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        application_rows = state.get("recruitment_applications", [])
        for student in state.get("portal_students", []):
            profile = self._derive_portal_profile(student)
            if profile is not None:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_student_profiles (
                        portal_student_id, full_name_pinyin, gender, birth_date, ethnic_group, native_place,
                        political_status, marital_status, religious_belief, id_type, mailing_address,
                        profile_photo_url, id_card_collage_url,
                        emergency_contact_name, emergency_contact_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(student["id"]),
                        profile.get("full_name_pinyin"),
                        profile.get("gender"),
                        profile.get("birth_date"),
                        profile.get("ethnic_group"),
                        profile.get("native_place"),
                        profile.get("political_status"),
                        profile.get("marital_status"),
                        profile.get("religious_belief"),
                        profile.get("id_type"),
                        profile.get("mailing_address"),
                        profile.get("profile_photo_url"),
                        profile.get("id_card_collage_url"),
                        profile.get("emergency_contact_name"),
                        profile.get("emergency_contact_phone"),
                    ),
                )

            draft = self._derive_portal_application_draft(student)
            matched_application = self._match_portal_application(student, application_rows)
            if draft is None or matched_application is None:
                continue
            application_id = int(matched_application["id"])

            def insert_attachment(
                owner_type: str,
                owner_id: int | None,
                category: str,
                file_url: str | None,
                file_name: str | None = None,
            ) -> None:
                if not file_url:
                    return
                attachment_name = str(file_name or "").strip() or str(file_url).rstrip("/").split("/")[-1] or f"{category}.dat"
                file_suffix = Path(attachment_name).suffix.lower().lstrip(".") or None
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_attachments (
                        portal_student_id, application_id, owner_type, owner_id, attachment_category,
                        file_name, file_url, file_type
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (int(student["id"]), application_id, owner_type, owner_id, category, attachment_name, file_url, file_suffix),
                )

            for preference in draft.get("preferences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_preferences (
                        application_id, preference_order, research_center_name, advisor_name, is_optional
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        int(preference.get("preference_order") or 1),
                        preference.get("research_center_name"),
                        preference.get("advisor_name"),
                        bool(preference.get("is_optional")),
                    ),
                )

            for education in draft.get("education_experiences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_education_experiences (
                        application_id, sort_order, education_stage, start_month, end_month, school_name,
                        major_name, average_score, gpa, ranking, verifier_name, verifier_phone,
                        transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        application_id,
                        int(education.get("sort_order") or 1),
                        education.get("education_stage"),
                        education.get("start_month"),
                        education.get("end_month"),
                        education.get("school_name"),
                        education.get("major_name"),
                        education.get("average_score"),
                        education.get("gpa"),
                        education.get("ranking"),
                        education.get("verifier_name"),
                        education.get("verifier_phone"),
                        education.get("transcript_attachment_url"),
                        education.get("degree_certificate_attachment_url"),
                        education.get("graduation_certificate_attachment_url"),
                    ),
                )
                education_row = cur.fetchone()
                education_id = int(education_row[0]) if education_row else None
                insert_attachment(
                    "education_experience",
                    education_id,
                    "transcript",
                    education.get("transcript_attachment_url"),
                    education.get("transcript_attachment_name"),
                )
                insert_attachment(
                    "education_experience",
                    education_id,
                    "degree_certificate",
                    education.get("degree_certificate_attachment_url"),
                    education.get("degree_certificate_attachment_name"),
                )
                insert_attachment(
                    "education_experience",
                    education_id,
                    "graduation_certificate",
                    education.get("graduation_certificate_attachment_url"),
                    education.get("graduation_certificate_attachment_name"),
                )

            for practice in draft.get("practice_experiences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_practice_experiences (
                        application_id, start_month, end_month, organization_name, position_name,
                        responsibility_text, verifier_name, verifier_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        practice.get("start_month"),
                        practice.get("end_month"),
                        practice.get("organization_name"),
                        practice.get("position_name"),
                        practice.get("responsibility_text"),
                        practice.get("verifier_name"),
                        practice.get("verifier_phone"),
                    ),
                )

            for english in draft.get("english_proficiencies", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_english_proficiencies (
                        application_id, exam_name, score_text, certificate_attachment_url
                    ) VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        application_id,
                        english.get("exam_name"),
                        english.get("score_text") or "",
                        english.get("certificate_attachment_url"),
                    ),
                )
                english_row = cur.fetchone()
                english_id = int(english_row[0]) if english_row else None
                insert_attachment(
                    "english_proficiency",
                    english_id,
                    "english_certificate",
                    english.get("certificate_attachment_url"),
                    english.get("certificate_attachment_name"),
                )

            for member in draft.get("family_members", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_family_members (
                        application_id, member_name, relation_type, employer_name, job_title, contact_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        member.get("member_name"),
                        member.get("relation_type"),
                        member.get("employer_name"),
                        member.get("job_title"),
                        member.get("contact_phone"),
                    ),
                )

            for achievement in draft.get("achievement_records", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_achievement_records (
                        application_id, achievement_type, paper_title, author_order, journal_or_conference,
                        publish_or_index_month, achievement_month, award_name, award_rank,
                        award_certificate_attachment_url, awarding_organization, award_level,
                        award_year, description_text, responsibility_text
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        application_id,
                        achievement.get("achievement_type"),
                        achievement.get("paper_title"),
                        achievement.get("author_order"),
                        achievement.get("journal_or_conference"),
                        achievement.get("publish_or_index_month"),
                        achievement.get("achievement_month"),
                        achievement.get("award_name"),
                        achievement.get("award_rank"),
                        achievement.get("award_certificate_attachment_url"),
                        achievement.get("awarding_organization"),
                        achievement.get("award_level"),
                        achievement.get("award_year"),
                        achievement.get("description_text"),
                        achievement.get("responsibility_text"),
                    ),
                )
                achievement_row = cur.fetchone()
                achievement_id = int(achievement_row[0]) if achievement_row else None
                insert_attachment(
                    "achievement_record",
                    achievement_id,
                    "achievement_award_certificate",
                    achievement.get("award_certificate_attachment_url"),
                    achievement.get("award_certificate_attachment_name"),
                )

            personal_statement = draft.get("personal_statement") if isinstance(draft.get("personal_statement"), dict) else {}
            if personal_statement:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_personal_statements (
                        application_id,
                        personal_statement_text,
                        growth_experience_text,
                        program_application_reason_text,
                        career_plan_text,
                        resume_attachment_url,
                        supporting_material_attachment_url,
                        ai_problem_statement,
                        ai_industry_opinion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        personal_statement.get("personal_statement_text"),
                        personal_statement.get("growth_experience_text"),
                        personal_statement.get("program_application_reason_text"),
                        personal_statement.get("career_plan_text"),
                        personal_statement.get("resume_attachment_url"),
                        personal_statement.get("supporting_material_attachment_url"),
                        personal_statement.get("ai_problem_statement"),
                        personal_statement.get("ai_industry_opinion"),
                    ),
                )
                insert_attachment(
                    "personal_statement",
                    application_id,
                    "resume",
                    personal_statement.get("resume_attachment_url"),
                    personal_statement.get("resume_attachment_name"),
                )

            declaration = draft.get("declaration") if isinstance(draft.get("declaration"), dict) else {}
            if declaration:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_declarations (
                        application_id, has_read_declaration, declaration_text, progress_snapshot
                    ) VALUES (%s, %s, %s, %s::jsonb)
                    """,
                    (
                        application_id,
                        bool(declaration.get("has_read_declaration")),
                        declaration.get("declaration_text"),
                        json.dumps(declaration.get("progress_snapshot")) if declaration.get("progress_snapshot") is not None else None,
                    ),
                )

            legacy_personal_statement_attachment = matched_application.get("personal_statement_attachment")
            if legacy_personal_statement_attachment and legacy_personal_statement_attachment != personal_statement.get("resume_attachment_url"):
                insert_attachment("portal_application", application_id, "personal_statement", legacy_personal_statement_attachment)
            insert_attachment("portal_application", application_id, "materials", matched_application.get("material_list_attachment"))

    def _seed_training(self, cur: psycopg.Cursor[Any], state: dict[str, Any], student_map: dict[str, int], advisor_map: dict[str, int]) -> dict[int, int]:
        cur.execute(
            "TRUNCATE TABLE dtlms_training_plan_versions, dtlms_scientific_reports, dtlms_outbound_studies, dtlms_training_plans RESTART IDENTITY CASCADE"
        )
        training_plan_map: dict[int, int] = {}
        for item in state.get("training_plans", []):
            cur.execute(
                """
                INSERT INTO dtlms_training_plans (
                    id, student_id, advisor_id, version_no, report_cycle, plan_status, scientific_goal, assessment_rule, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["version_no"],
                    item["report_cycle"],
                    self._map_training_plan_status(item.get("plan_status", "待学生确认")),
                    item["scientific_goal"],
                    item["assessment_rule"],
                ),
            )
            training_plan_map[int(item["id"])] = int(item["id"])

        training_plan_by_student = {item["student_no"]: int(item["id"]) for item in state.get("training_plans", [])}
        for item in state.get("scientific_reports", []):
            cur.execute(
                """
                INSERT INTO dtlms_scientific_reports (
                    id, business_key, student_id, training_plan_id, period_label, report_status, summary,
                    attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
                    student_map[item["student_no"]],
                    training_plan_by_student[item["student_no"]],
                    item["period_label"],
                    self._map_report_status(item.get("report_status", "待导师审阅")),
                    item["summary"],
                    f"/reports/{item['student_no']}/{item['period_label']}.pdf",
                    advisor_map.get(item.get("reviewer_name")) if item.get("reviewer_name") else None,
                    item.get("review_score"),
                    f"导入状态：{item.get('report_status')}",
                ),
            )

        for item in state.get("outbound_studies", []):
            cur.execute(
                """
                INSERT INTO dtlms_outbound_studies (
                    id, business_key, student_id, advisor_id, study_type, destination, start_date, end_date,
                    approval_status, expected_outcome, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["study_type"],
                    item["destination"],
                    item["start_date"],
                    item["end_date"],
                    self._map_outbound_status(item.get("approval_status", "审批中")),
                    item.get("expected_outcome"),
                ),
            )
        return training_plan_map

    def _seed_degree(self, cur: psycopg.Cursor[Any], state: dict[str, Any], student_map: dict[str, int], advisor_map: dict[str, int]) -> dict[int, int]:
        cur.execute("TRUNCATE TABLE dtlms_thesis_reviews, dtlms_theses RESTART IDENTITY CASCADE")
        thesis_map: dict[int, int] = {}
        for item in state.get("theses", []):
            cur.execute(
                """
                INSERT INTO dtlms_theses (
                    id, business_key, student_id, advisor_id, title, plagiarism_rate, thesis_status,
                    blind_review_status, defense_date, degree_granted, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["title"],
                    item.get("plagiarism_rate"),
                    self._map_thesis_status(item.get("thesis_status", "待提交")),
                    self._map_blind_review_status(item.get("blind_review_status", "未送审")),
                    self._map_defense_date(item.get("defense_status", "未进入")),
                    self._map_degree_status(item.get("degree_status", "待申请")),
                ),
            )
            thesis_map[int(item["id"])] = int(item["id"])
        return thesis_map

    def _seed_training_plan_versions(self, cur: psycopg.Cursor[Any], state: dict[str, Any], training_plan_map: dict[int, int]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_training_plan_versions RESTART IDENTITY CASCADE")
        for item in state.get("training_plans", []):
            cur.execute(
                "INSERT INTO dtlms_training_plan_versions (training_plan_id, version_no, change_reason, plan_snapshot) VALUES (%s, %s, %s, %s)",
                (training_plan_map[int(item["id"])], item["version_no"], "初始化导入", item["scientific_goal"]),
            )

    def _seed_admission_decisions(self, cur: psycopg.Cursor[Any], state: dict[str, Any], plan_map: dict[int, int]) -> None:
        application_ids = {int(item["id"]): item for item in state.get("recruitment_applications", [])}
        cur.execute("SELECT id FROM dtlms_recruitment_applications")
        existing_application_ids = {int(row[0]) for row in cur.fetchall()}
        for application_id, item in application_ids.items():
            if application_id not in existing_application_ids:
                logger.warning("Skip admission decision seed because recruitment application %s does not exist", application_id)
                continue
            decision_status = self._map_decision_status(item.get("application_status", "报名已提交"))
            cur.execute(
                "INSERT INTO dtlms_admission_decisions (application_id, decision_status, rank_no, final_score, transfer_option, decision_comment) VALUES (%s, %s, %s, %s, %s, %s)",
                (application_id, decision_status, application_id, item.get("final_score"), None, f"来源计划 {plan_map[int(item['plan_id'])]}"),
            )

    def _seed_thesis_reviews(self, cur: psycopg.Cursor[Any], state: dict[str, Any], thesis_map: dict[int, int]) -> None:
        for item in state.get("thesis_reviews", []):
            cur.execute(
                "INSERT INTO dtlms_thesis_reviews (id, thesis_id, expert_name, review_score, review_status, review_comment) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    int(item["id"]),
                    thesis_map[int(item["thesis_id"])],
                    item["expert_name"],
                    item.get("review_score"),
                    self._map_review_progress(item.get("review_status", "待提交")),
                    item.get("review_comment"),
                ),
            )

    def _seed_operation_logs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_operation_logs RESTART IDENTITY CASCADE")
        for item in state.get("operation_logs", []):
            cur.execute(
                """
                INSERT INTO dtlms_operation_logs (
                    id, operator_username, operator_role, module_name, entity_name, entity_id,
                    action, old_value, new_value, request_ip, result, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s::jsonb, %s, %s, %s, %s)
                """,
                (
                    int(item["id"]),
                    item["operator_username"],
                    "runtime_seed",
                    item["module_name"],
                    item["entity_name"],
                    item["entity_id"],
                    item["action"],
                    self._json_payload({"summary": item.get("summary")}),
                    "127.0.0.1",
                    item.get("result", "success"),
                    item["operated_at"],
                    item["operated_at"],
                ),
            )

    def _seed_sync_logs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_data_sync_logs RESTART IDENTITY CASCADE")
        for item in state.get("sync_logs", []):
            cur.execute(
                "INSERT INTO dtlms_data_sync_logs (id, source_system, target_system, sync_status, record_count, failure_reason, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    int(item["id"]),
                    item["source_system"],
                    item["target_system"],
                    item["sync_status"],
                    int(item["record_count"]),
                    item.get("failure_reason"),
                    item["executed_at"],
                    item["executed_at"],
                ),
            )

    def _seed_notification_delivery_logs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_notification_delivery_logs RESTART IDENTITY CASCADE")
        for item in state.get("notification_delivery_logs", []):
            cur.execute(
                """
                INSERT INTO dtlms_notification_delivery_logs (
                    id, channel, template_code, recipient, subject, send_status,
                    failure_reason, business_key, triggered_by, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(item["id"]),
                    item["channel"],
                    item.get("template_code"),
                    item["recipient"],
                    item["subject"],
                    item["send_status"],
                    item.get("failure_reason"),
                    item.get("business_key"),
                    item.get("triggered_by"),
                    item["sent_at"],
                    item["sent_at"],
                ),
            )

    def _seed_system_configs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        for item in state.get("audit_policies", []):
            cur.execute(
                """
                INSERT INTO dtlms_system_configs (config_key, config_value, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value, description = EXCLUDED.description, updated_at = CURRENT_TIMESTAMP
                """,
                (f"audit.policy.{int(item['id'])}", item["policy"], item["item"]),
            )
        for item in state.get("integrations", []):
            cur.execute(
                """
                INSERT INTO dtlms_system_configs (config_key, config_value, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value, description = EXCLUDED.description, updated_at = CURRENT_TIMESTAMP
                """,
                (
                    f"integration.{int(item['id'])}.{item['name']}",
                    f"{item['direction']}|{item['cadence']}|{item['status']}|{item['owner']}",
                    "外部集成概览",
                ),
            )

    def _seed_workflow_engine(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute(
            "TRUNCATE TABLE "
            "dtlms_wf_ru_identitylink, dtlms_wf_ru_variable, dtlms_wf_ru_task, dtlms_wf_ru_execution, "
            "dtlms_wf_hi_varinst, dtlms_wf_hi_actinst, dtlms_wf_hi_taskinst, dtlms_wf_hi_procinst, "
            "dtlms_wf_re_procdef, dtlms_wf_re_deployment, dtlms_wf_de_model"
        )
        tasks = list(state.get("workflow_tasks", []))
        inserted_models: set[str] = set()
        inserted_deployments: set[str] = set()
        inserted_procdefs: set[str] = set()
        inserted_procinsts: set[str] = set()
        inserted_variables: set[str] = set()

        for task in tasks:
            process_definition_key = str(task.get("process_definition_key") or task.get("flow_code") or "adhoc_workflow")
            task_definition_key = str(task.get("task_definition_key") or task.get("node_key") or "manual_task")
            business_key = str(task.get("business_key") or task.get("id") or "0")
            process_definition_id = str(task.get("process_definition_id") or self._workflow_process_definition_id(process_definition_key))
            deployment_id = str(task.get("deployment_id") or self._workflow_deployment_id(process_definition_key))
            process_instance_id = str(task.get("process_instance_id") or self._workflow_process_instance_id(process_definition_key, business_key))
            execution_id = str(task.get("execution_id") or self._workflow_execution_id(process_instance_id, task_definition_key))
            workflow_name = str(task.get("workflow_name") or "未命名流程")
            resource_name = f"{process_definition_key}.bpmn20.xml"
            terminal = self._is_workflow_terminal(task)
            start_time = str(task.get("created_at") or "")
            end_time = self._workflow_end_time(task) if terminal else None
            duration_ms = self._workflow_duration_millis(start_time, end_time)
            candidate_groups = self._normalize_name_list(task.get("candidate_groups"))

            if process_definition_key not in inserted_models:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_de_model (
                        id_, name_, key_, category_, version_, model_type_, description_, meta_info_,
                        created_, last_updated_, deployment_id_, resource_name_, editor_source_extra_value_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s::jsonb)
                    """,
                    (
                        f"MODEL-{process_definition_key}",
                        workflow_name,
                        process_definition_key,
                        task.get("business_module") or "流程中心",
                        int(task.get("process_definition_version") or 1),
                        0,
                        f"{workflow_name} 流程模型",
                        self._json_payload({"source": "runtime_seed", "workflow_name": workflow_name}),
                        start_time,
                        end_time or start_time,
                        deployment_id,
                        resource_name,
                        self._json_payload({"business_module": task.get("business_module"), "flow_code": task.get("flow_code")}),
                    ),
                )
                inserted_models.add(process_definition_key)

            if deployment_id not in inserted_deployments:
                cur.execute(
                    "INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_) VALUES (%s, %s, %s, %s, %s)",
                    (deployment_id, workflow_name, task.get("business_module") or "流程中心", process_definition_key, start_time),
                )
                inserted_deployments.add(deployment_id)

            if process_definition_id not in inserted_procdefs:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_re_procdef (
                        id_, key_, version_, deployment_id_, resource_name_, diagram_resource_name_, name_, category_, description_, suspension_state_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        process_definition_id,
                        process_definition_key,
                        int(task.get("process_definition_version") or 1),
                        deployment_id,
                        resource_name,
                        f"{process_definition_key}.png",
                        workflow_name,
                        task.get("business_module") or "流程中心",
                        f"{workflow_name} 定义",
                        1,
                    ),
                )
                inserted_procdefs.add(process_definition_id)

            if process_instance_id not in inserted_procinsts:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_hi_procinst (
                        id_, proc_inst_id_, business_key_, proc_def_id_, start_time_, end_time_, duration_ms_,
                        start_user_id_, end_act_id_, delete_reason_, start_act_id_, state_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        process_instance_id,
                        process_instance_id,
                        business_key,
                        process_definition_id,
                        start_time,
                        end_time,
                        duration_ms,
                        None,
                        None if not terminal else task_definition_key,
                        "rejected" if str(task.get("status") or "") == "已驳回" else None,
                        "startEvent",
                        "COMPLETED" if terminal else "ACTIVE",
                    ),
                )
                inserted_procinsts.add(process_instance_id)

            cur.execute(
                """
                INSERT INTO dtlms_wf_hi_taskinst (
                    id_, task_def_key_, proc_def_id_, proc_inst_id_, exec_id_, name_, business_key_, assignee_, owner_,
                    start_time_, claim_time_, end_time_, duration_ms_, due_date_, delete_reason_, priority_, category_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    f"TASK-{int(task['id'])}",
                    task_definition_key,
                    process_definition_id,
                    process_instance_id,
                    execution_id,
                    task.get("title") or workflow_name,
                    business_key,
                    None,
                    None,
                    start_time,
                    None,
                    end_time,
                    duration_ms,
                    task.get("due_at"),
                    "rejected" if str(task.get("status") or "") == "已驳回" else None,
                    int(self._workflow_priority_value(task.get("priority"))),
                    task.get("business_module") or "流程中心",
                ),
            )

            self._insert_workflow_history_activities(
                cur,
                task=task,
                process_definition_id=process_definition_id,
                process_instance_id=process_instance_id,
                execution_id=execution_id,
                task_definition_key=task_definition_key,
            )

            self._insert_workflow_history_variables(
                cur,
                task=task,
                process_instance_id=process_instance_id,
                execution_id=execution_id,
                inserted_variables=inserted_variables,
            )

            if terminal:
                continue

            cur.execute(
                """
                INSERT INTO dtlms_wf_ru_execution (
                    id_, proc_inst_id_, proc_def_id_, business_key_, parent_id_, act_id_, is_active_, is_concurrent_, is_scope_, start_time_, start_user_id_
                ) VALUES (%s, %s, %s, %s, NULL, %s, TRUE, FALSE, TRUE, %s, %s)
                """,
                (execution_id, process_instance_id, process_definition_id, business_key, task_definition_key, start_time, None),
            )
            cur.execute(
                """
                INSERT INTO dtlms_wf_ru_task (
                    id_, exec_id_, proc_inst_id_, proc_def_id_, task_def_key_, name_, business_key_, assignee_, owner_,
                    create_time_, due_date_, claim_time_, priority_, suspension_state_, form_key_, description_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s, %s)
                """,
                (
                    f"TASK-{int(task['id'])}",
                    execution_id,
                    process_instance_id,
                    process_definition_id,
                    task_definition_key,
                    task.get("title") or workflow_name,
                    business_key,
                    None,
                    None,
                    start_time,
                    task.get("due_at"),
                    int(self._workflow_priority_value(task.get("priority"))),
                    1,
                    business_key,
                    task.get("form_summary"),
                ),
            )
            for group_id in candidate_groups:
                cur.execute(
                    "INSERT INTO dtlms_wf_ru_identitylink (task_id_, proc_inst_id_, user_id_, group_id_, link_type_) VALUES (%s, %s, NULL, %s, %s)",
                    (f"TASK-{int(task['id'])}", process_instance_id, group_id, "candidate"),
                )
            self._insert_workflow_runtime_variables(cur, task=task, process_instance_id=process_instance_id, execution_id=execution_id)
