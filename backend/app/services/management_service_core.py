from __future__ import annotations

from typing import TYPE_CHECKING

from .management_service_shared import *


class RuntimeManagementStoreCoreMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _create_postgres_store(self):
        raise NotImplementedError

    def _create_email_service(self):
        raise NotImplementedError

    def _get_cache_client(self):
        raise NotImplementedError

    def __init__(self) -> None:
        self._lock = RLock()
        self._postgres_store = self._create_postgres_store()
        self._email_service = self._create_email_service()
        self._loaded_state_from_postgres = False
        self._hydrated_state_from_postgres = False
        self._migrated_workflow_task_ids: set[int] = set()
        self.state = self._load_state()
        self._counters = self.state.setdefault("counters", {})
        state_changed = self._migrate_state()
        if (self._loaded_state_from_postgres or self._hydrated_state_from_postgres) and state_changed:
            try:
                self._persist_migrated_workflow_tasks()
            except Exception as exc:
                logger.warning("Persist migrated runtime state to PostgreSQL failed: %s", exc)

    def _load_state(self) -> dict[str, Any]:
        postgres_state = self._postgres_store.load_state()
        if postgres_state is not None:
            self._loaded_state_from_postgres = True
            return postgres_state
        return {"counters": {}}

    def _write_state(self, state: dict[str, Any] | None = None) -> None:
        payload = state or self.state
        self._postgres_store.save_state(payload)

    def _migrate_state(self) -> bool:
        changed = False
        if "teams" not in self.state:
            self.state["teams"] = self._bootstrap_teams_from_students()
            changed = True
        postgres_roles = self._load_roles_from_postgres()
        if postgres_roles is not None and self.state.setdefault("roles", []) != postgres_roles:
            self.state["roles"] = postgres_roles
            changed = True
        postgres_system_users = self._load_system_users_from_postgres()
        if postgres_system_users is not None and self.state.setdefault("system_users", []) != postgres_system_users:
            self.state["system_users"] = postgres_system_users
            changed = True
        postgres_profiles = self._load_profiles_from_postgres()
        if postgres_profiles is not None and self.state.setdefault("profiles", {}) != postgres_profiles:
            self.state["profiles"] = postgres_profiles
            changed = True
        postgres_audit_policies = self._load_audit_policies_from_postgres()
        if postgres_audit_policies is not None and self.state.setdefault("audit_policies", []) != postgres_audit_policies:
            self.state["audit_policies"] = postgres_audit_policies
            changed = True
        postgres_integrations = self._load_integrations_from_postgres()
        if postgres_integrations is not None and self.state.setdefault("integrations", []) != postgres_integrations:
            self.state["integrations"] = postgres_integrations
            changed = True
        postgres_students = self._load_students_from_postgres()
        if postgres_students is not None:
            state_student_ids = {int(item.get("id", 0)) for item in self.state.setdefault("students", [])}
            postgres_student_ids = {int(item.get("id", 0)) for item in postgres_students}
            if state_student_ids != postgres_student_ids:
                self.state["students"] = postgres_students
                changed = True
        postgres_teams = self._load_teams_from_postgres()
        if postgres_teams is not None:
            state_team_ids = {int(item.get("id", 0)) for item in self.state.setdefault("teams", [])}
            postgres_team_ids = {int(item.get("id", 0)) for item in postgres_teams}
            if state_team_ids != postgres_team_ids:
                self.state["teams"] = postgres_teams
                changed = True
        postgres_recruitment_plans = self._load_recruitment_plans_from_postgres()
        if postgres_recruitment_plans is not None:
            state_plan_ids = {int(item.get("id", 0)) for item in self.state.setdefault("recruitment_plans", [])}
            postgres_plan_ids = {int(item.get("id", 0)) for item in postgres_recruitment_plans}
            if state_plan_ids != postgres_plan_ids:
                self.state["recruitment_plans"] = postgres_recruitment_plans
                changed = True
        postgres_portal_students = self._load_portal_students_from_postgres()
        if postgres_portal_students is not None:
            state_portal_student_ids = {int(item.get("id", 0)) for item in self.state.setdefault("portal_students", [])}
            postgres_portal_student_ids = {int(item.get("id", 0)) for item in postgres_portal_students}
            if state_portal_student_ids != postgres_portal_student_ids:
                self.state["portal_students"] = postgres_portal_students
                changed = True
        postgres_recruitment_applications = self._load_recruitment_applications_from_postgres()
        if postgres_recruitment_applications is not None:
            state_application_ids = {int(item.get("id", 0)) for item in self.state.setdefault("recruitment_applications", [])}
            postgres_application_ids = {int(item.get("id", 0)) for item in postgres_recruitment_applications}
            if state_application_ids != postgres_application_ids:
                self.state["recruitment_applications"] = postgres_recruitment_applications
                changed = True
        postgres_workflow_tasks = self._load_workflow_tasks_from_postgres()
        if postgres_workflow_tasks is not None:
            state_task_ids = {int(item.get("id", 0)) for item in self.state.setdefault("workflow_tasks", [])}
            postgres_task_ids = {int(item.get("id", 0)) for item in postgres_workflow_tasks}
            if state_task_ids != postgres_task_ids:
                self.state["workflow_tasks"] = postgres_workflow_tasks
                changed = True
        self._counters["teams"] = max(
            int(self._counters.get("teams", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("teams", [])], default=0),
        )
        self._counters["roles"] = max(
            int(self._counters.get("roles", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("roles", [])], default=0),
        )
        self._counters["system_users"] = max(
            int(self._counters.get("system_users", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("system_users", [])], default=0),
        )
        self._counters["audit_policies"] = max(
            int(self._counters.get("audit_policies", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("audit_policies", [])], default=0),
        )
        self._counters["integrations"] = max(
            int(self._counters.get("integrations", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("integrations", [])], default=0),
        )
        self._counters["recruitment_plans"] = max(
            int(self._counters.get("recruitment_plans", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("recruitment_plans", [])], default=0),
        )
        self.state.setdefault("portal_students", [])
        self._counters["portal_students"] = max(
            int(self._counters.get("portal_students", 0)),
            max([item.get("id", 0) for item in self.state["portal_students"]], default=0),
        )
        self._counters["recruitment_applications"] = max(
            int(self._counters.get("recruitment_applications", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("recruitment_applications", [])], default=0),
        )
        self._counters["workflow_tasks"] = max(
            int(self._counters.get("workflow_tasks", 0)),
            max([item.get("id", 0) for item in self.state.setdefault("workflow_tasks", [])], default=0),
        )
        for portal_student in self.state["portal_students"]:
            portal_student["account_status"] = self._normalize_portal_account_status(portal_student.get("account_status"))
            portal_student.setdefault("password_hash", None)
            portal_student.setdefault("gender", None)
            portal_student.setdefault("birth_date", None)
            portal_student.setdefault("ethnic_group", None)
            portal_student.setdefault("native_place", None)
            portal_student.setdefault("marital_status", None)
            portal_student.setdefault("religious_belief", None)
            portal_student.setdefault("id_type", "居民身份证")
            portal_student.setdefault("mailing_address", None)
            portal_student.setdefault("english_level", None)
            portal_student.setdefault("family_info", None)
            portal_student.setdefault("education_experience", None)
            portal_student.setdefault("practice_experience", None)
            portal_student.setdefault("personal_profile", None)
            portal_student.setdefault("recommendation_notes", None)
            portal_student.setdefault("personal_statement_text", None)
            portal_student.setdefault("signed_agreement", False)
            portal_student.setdefault("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            portal_student.setdefault("updated_at", portal_student.get("created_at"))

        role_lookup = {item["role_code"]: item for item in self.state.setdefault("roles", [])}
        profiles = self.state.setdefault("profiles", {})
        for user in self.state.setdefault("system_users", []):
            if not user.get("password_hash"):
                default_password = DEFAULT_PASSWORD_BY_USERNAME.get(user.get("username"), DEFAULT_USER_PASSWORD)
                user["password_hash"] = PASSWORD_CONTEXT.hash(default_password)
                changed = True
            if "last_login_at" not in user:
                user["last_login_at"] = None
                changed = True
            profile = profiles.get(user["username"])
            role = role_lookup.get(user.get("role_code"))
            if not profile:
                profiles[user["username"]] = {
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "role_name": role["role_name"] if role else user["role_code"],
                    "department_name": user["department_name"],
                    "phone_number": user.get("phone_number"),
                    "email": None,
                    "theme_color": "#0f4cbd",
                }
                changed = True
            elif role and profile.get("role_name") in {None, user.get("role_code")}:
                profile["role_name"] = role["role_name"]
                changed = True

        for policy in self.state.setdefault("audit_policies", []):
            if not policy.get("status"):
                policy["status"] = "启用"
                changed = True

        for plan in self.state.setdefault("recruitment_plans", []):
            if "brochure_image_url" not in plan:
                plan["brochure_image_url"] = None
                changed = True
            if "plan_description" not in plan:
                plan["plan_description"] = None
                changed = True
            if "current_stage" not in plan:
                plan["current_stage"] = "报名配置"
                changed = True
            if "target_quota" not in plan:
                plan["target_quota"] = 0
                changed = True
            if "interview_group_count" not in plan:
                plan["interview_group_count"] = 0
                changed = True
            if "is_open" not in plan:
                plan["is_open"] = True
                changed = True

        team_lookup = {item["team_name"]: item for item in self.state.setdefault("teams", [])}
        for team in self.state.setdefault("teams", []):
            team.setdefault("team_code", f"TEAM-{team['id']:03d}")
            team.setdefault("department_name", "未分配院系")
            team.setdefault("discipline_name", "未分配学科")
            team.setdefault("lead_advisor_name", (team.get("advisor_names") or [""])[0])
            team["advisor_names"] = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
            team["research_directions"] = self._normalize_name_list(team.get("research_directions", []))
            team.setdefault("status", "启用")
            team.setdefault("established_on", None)
            team.setdefault("created_on", team.get("established_on"))
            team.setdefault("description", None)
        for student in self.state.setdefault("students", []):
            if student.get("team_name") and student["team_name"] not in team_lookup:
                next_team_id = max([item.get("id", 0) for item in self.state["teams"]], default=0) + 1
                self.state["teams"].append(
                    {
                        "id": next_team_id,
                        "team_code": f"TEAM-AUTO-{next_team_id:03d}",
                        "team_name": student["team_name"],
                        "department_name": "未分配院系",
                        "discipline_name": "未分配学科",
                        "lead_advisor_name": student.get("advisor_name", ""),
                        "advisor_names": self._normalize_name_list([student.get("advisor_name", "")]),
                        "research_directions": [],
                        "status": "启用",
                        "established_on": None,
                        "created_on": datetime.now().strftime("%Y-%m-%d"),
                        "description": "由历史学生主档自动迁移生成的团队记录。",
                    }
                )
                changed = True

        if self._normalize_legacy_workflow_tasks():
            changed = True

        if self._migrate_workflow_runtime():
            changed = True

        if self._normalize_recruitment_application_profiles():
            changed = True

        return changed

    def _load_students_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_student_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load students from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_teams_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_team_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load teams from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_recruitment_plans_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_recruitment_plan_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load recruitment plans from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_portal_students_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_portal_student_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load portal students from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_recruitment_applications_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_recruitment_application_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load recruitment applications from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_workflow_tasks_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_workflow_task_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load workflow tasks from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_roles_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_role_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load roles from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_system_users_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_system_user_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load system users from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_profiles_from_postgres(self) -> dict[str, dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_user_profile_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load user profiles from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_audit_policies_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_audit_policy_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load audit policies from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _load_integrations_from_postgres(self) -> list[dict[str, Any]] | None:
        try:
            rows = self._postgres_store.load_integration_state()
            if rows is not None:
                self._hydrated_state_from_postgres = True
            return rows
        except Exception as exc:
            logger.warning("Load integrations from PostgreSQL failed, current state will stay database-only/empty: %s", exc)
            return None

    def _refresh_students_from_postgres(self) -> None:
        postgres_students = self._load_students_from_postgres()
        if postgres_students is not None:
            self.state["students"] = postgres_students
            self._counters["students"] = max([item.get("id", 0) for item in postgres_students], default=0)

    def _refresh_teams_from_postgres(self) -> None:
        postgres_teams = self._load_teams_from_postgres()
        if postgres_teams is not None:
            self.state["teams"] = postgres_teams
            self._counters["teams"] = max([item.get("id", 0) for item in postgres_teams], default=0)

    def _normalize_recruitment_application_profiles(self) -> bool:
        changed = False
        fallback_second_choices = [
            "机器学习",
            "工业互联网",
            "知识图谱",
            "数据智能",
            "数字孪生",
            "软件工程",
        ]
        fallback_political_statuses = ["中共党员", "共青团员", "群众", "中共预备党员"]
        for index, item in enumerate(self.state.setdefault("recruitment_applications", []), start=1):
            defaults = {
                "review_round": f'{item.get("plan_id") or 0}轮次' if item.get("plan_id") else "默认轮次",
                "first_choice": item.get("intended_field"),
                "second_choice": fallback_second_choices[(index - 1) % len(fallback_second_choices)],
                "gender": "未知",
                "political_status": fallback_political_statuses[(index - 1) % len(fallback_political_statuses)],
                "marital_status": "未婚",
                "religious_belief": "无",
                "native_place": "待补充",
                "phone_number": f'1390002{index:04d}',
                "email": f'candidate{index:02d}@mail.example.com',
                "mailing_address": "待补充",
                "id_type": "居民身份证",
                "id_number": None,
                "undergraduate_school": item.get("graduation_school"),
                "accept_adjustment": "是",
                "undergraduate_average_score": None,
                "undergraduate_gpa": None,
                "undergraduate_rank": None,
                "undergraduate_major": item.get("intended_field"),
                "graduate_average_score": None,
                "graduate_gpa": None,
                "graduate_rank": None,
                "graduate_major": item.get("intended_field"),
                "intended_advisor_name": item.get("reviewer_name"),
                "discovery_channel": None,
                "graduate_school": None,
                "overseas_university_name": None,
                "overseas_master_university_name": None,
                "self_evaluation": None,
                "applied_at": None,
                "research_problem": None,
                "research_status_analysis": None,
                "research_impact": None,
                "ai_society_impact": None,
                "dissenting_view": None,
                "family_info": None,
                "education_experience": None,
                "practice_experience": None,
                "personal_statement_text": None,
                "student_activity_experience": None,
                "personal_statement_attachment": None,
                "material_list_attachment": None,
                "supplementary_profile": None,
            }
            for key, value in defaults.items():
                if key not in item:
                    item[key] = value
                    changed = True
        return changed

    def _next_id(self, key: str) -> int:
        self._counters[key] = int(self._counters.get(key, 0)) + 1
        return self._counters[key]

    def _record_operation(
        self,
        module_name: str,
        entity_name: str,
        entity_id: str,
        action: str,
        summary: str,
        operator_username: str = "admin",
        *,
        result: str = "success",
    ) -> dict[str, Any]:
        entry = {
            "id": self._next_id("operation_logs"),
            "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator_username": operator_username,
            "module_name": module_name,
            "entity_name": entity_name,
            "entity_id": entity_id,
            "action": action,
            "result": result,
            "summary": summary,
        }
        self._list("operation_logs").insert(0, entry)
        return entry

    def _persist_operation_log(self, operation_log: dict[str, Any]) -> None:
        try:
            self._postgres_store.sync_operation_log(
                operation_log,
                counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
            )
        except Exception as exc:
            logger.warning("Persist operation log failed: %s", exc)

    def record_operation_event(
        self,
        module_name: str,
        entity_name: str,
        entity_id: str,
        action: str,
        summary: str,
        operator_username: str = "admin",
        *,
        result: str = "success",
    ) -> dict[str, Any]:
        operation_log = self._record_operation(
            module_name,
            entity_name,
            entity_id,
            action,
            summary,
            operator_username=operator_username,
            result=result,
        )
        self._persist_operation_log(operation_log)
        return operation_log

    def _record_notification_delivery_log(
        self,
        *,
        channel: str,
        recipient: str,
        subject: str,
        send_status: str,
        template_code: str | None = None,
        failure_reason: str | None = None,
        business_key: str | None = None,
        triggered_by: str | None = None,
    ) -> dict[str, Any]:
        entry = {
            "id": self._next_id("notification_delivery_logs"),
            "channel": channel,
            "template_code": template_code,
            "recipient": recipient,
            "subject": subject,
            "send_status": send_status,
            "failure_reason": failure_reason,
            "business_key": business_key,
            "triggered_by": triggered_by or "system",
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._list("notification_delivery_logs").insert(0, entry)
        try:
            self._postgres_store.sync_notification_delivery_log(
                entry,
                counters={"notification_delivery_logs": int(self._counters.get("notification_delivery_logs", 0))},
            )
        except Exception as exc:
            logger.warning("Persist notification delivery log failed: %s", exc)
        return entry

    def _list(self, name: str) -> list[dict[str, Any]]:
        return self.state.setdefault(name, [])

    def _find_required(self, name: str, item_id: int) -> tuple[int, dict[str, Any]]:
        for index, item in enumerate(self._list(name)):
            if item["id"] == item_id:
                return index, item
        raise KeyError(item_id)

    def _save(self) -> None:
        self._write_state()

    def _matches_keyword(self, *values: Any, keyword: str | None = None) -> bool:
        if not keyword:
            return True
        needle = str(keyword).strip().lower()
        haystack = " ".join(str(value or "") for value in values).lower()
        return needle in haystack

    def _normalize_name_list(self, values: list[str] | tuple[str, ...] | set[str] | None, *extra_values: str | None) -> list[str]:
        merged = [*(values or []), *extra_values]
        return list(dict.fromkeys(str(item).strip() for item in merged if str(item or "").strip()))

    def _paginate_items(self, items: list[ListItemT], page: int, page_size: int) -> tuple[list[ListItemT], int]:
        total = len(items)
        start_index = max(page - 1, 0) * page_size
        end_index = start_index + page_size
        return items[start_index:end_index], total

    def _bootstrap_teams_from_students(self) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, Any]] = {}
        for item in self.state.get("students", []):
            team_name = str(item.get("team_name") or "").strip()
            if not team_name:
                continue
            current = grouped.setdefault(
                team_name,
                {
                    "id": len(grouped) + 1,
                    "team_code": f"TEAM-AUTO-{len(grouped) + 1:03d}",
                    "team_name": team_name,
                    "department_name": "未分配院系",
                    "discipline_name": "未分配学科",
                    "lead_advisor_name": item.get("advisor_name", ""),
                    "advisor_names": [],
                    "research_directions": [],
                    "status": "启用",
                    "established_on": None,
                    "created_on": datetime.now().strftime("%Y-%m-%d"),
                    "description": "由历史学生主档自动生成的团队记录。",
                },
            )
            current["advisor_names"] = self._normalize_name_list(current.get("advisor_names", []), item.get("advisor_name"))
        return list(grouped.values())

    def _advisor_name_values(self) -> list[str]:
        return sorted(
            {
                str(item.get("full_name") or "").strip()
                for item in self._list("system_users")
                if str(item.get("role_code") or "").strip() == "advisor"
                and str(item.get("account_status") or "").strip() == "启用"
                and str(item.get("full_name") or "").strip()
            }
        )

    def _system_user_name_values(self) -> list[str]:
        values = {item.get("full_name") for item in self._list("system_users") if item.get("full_name")}
        return sorted(str(item).strip() for item in values if str(item or "").strip())

    def _active_advisor_directory(self) -> list[dict[str, Any]]:
        try:
            return self._postgres_store.list_active_advisors()
        except Exception as exc:
            logger.warning("Load active advisors from PostgreSQL failed, fallback to advisor names only: %s", exc)
            return [{"id": None, "full_name": name, "advisor_no": None, "organization_name": None} for name in self._advisor_name_values()]

    @staticmethod
    def _build_advisor_option_label(item: dict[str, Any]) -> str:
        full_name = str(item.get("full_name") or "").strip()
        advisor_no = str(item.get("advisor_no") or "").strip()
        return f"{full_name}（{advisor_no}）" if advisor_no else full_name

    def _advisor_select_options(self) -> list[SelectOption]:
        options: list[SelectOption] = []
        for item in self._active_advisor_directory():
            full_name = str(item.get("full_name") or "").strip()
            if not full_name:
                continue
            advisor_id = item.get("id")
            options.append(SelectOption(label=self._build_advisor_option_label(item), value=str(advisor_id) if advisor_id is not None else full_name))
        return options

    def _resolve_advisor_name(self, advisor_id: int | None = None, advisor_name: str | None = None) -> str:
        if advisor_id is not None:
            for item in self._active_advisor_directory():
                if int(item.get("id") or 0) == int(advisor_id):
                    full_name = str(item.get("full_name") or "").strip()
                    if full_name:
                        return full_name
            raise ValueError("Selected advisor not found")
        normalized_name = str(advisor_name or "").strip()
        if normalized_name:
            return normalized_name
        raise ValueError("Selected advisor not found")

    def _advisor_name_by_id(self, advisor_id: int | None) -> str | None:
        if advisor_id is None:
            return None
        try:
            return self._resolve_advisor_name(advisor_id=advisor_id)
        except ValueError:
            return None

    def _resolve_advisor_names(self, advisor_ids: list[int] | None = None, advisor_names: list[str] | None = None) -> list[str]:
        resolved_names = [self._resolve_advisor_name(advisor_id=item) for item in (advisor_ids or []) if item is not None]
        if resolved_names:
            return self._normalize_name_list(resolved_names)
        return self._normalize_name_list(advisor_names or [])

    def _best_effort_advisor_ids(self, advisor_names: list[str]) -> list[int]:
        name_to_ids: dict[str, list[int]] = {}
        for item in self._active_advisor_directory():
            full_name = str(item.get("full_name") or "").strip()
            advisor_id = int(item.get("id") or 0) or None
            if not full_name or advisor_id is None:
                continue
            name_to_ids.setdefault(full_name, []).append(advisor_id)
        resolved: list[int] = []
        for name in advisor_names:
            advisor_ids = name_to_ids.get(name) or []
            if advisor_ids:
                resolved.append(advisor_ids[0])
        return resolved

    def _student_option_values(self) -> list[SelectOption]:
        items = sorted(self._list("students"), key=lambda item: str(item.get("student_no") or ""))
        return [SelectOption(label=f'{item["full_name"]}（{item["student_no"]}）', value=item["student_no"]) for item in items]

    def _training_student_options(self) -> list[TrainingStudentOption]:
        items = sorted(self._list("students"), key=lambda item: str(item.get("student_no") or ""))
        return [
            TrainingStudentOption(
                student_no=item["student_no"],
                student_name=item["full_name"],
                advisor_name=item["advisor_name"],
                label=f'{item["full_name"]}（{item["student_no"]}）',
            )
            for item in items
        ]

    def _select_options_from_values(self, values: list[str | None] | set[str | None] | tuple[str | None, ...]) -> list[SelectOption]:
        return [SelectOption(label=item, value=item) for item in sorted({str(value).strip() for value in values if str(value or "").strip()})]

    def _team_lookup_by_name(self) -> dict[str, dict[str, Any]]:
        return {item["team_name"]: item for item in self._list("teams")}

    def _team_lookup_by_id(self) -> dict[int, dict[str, Any]]:
        return {int(item["id"]): item for item in self._list("teams")}

    def _team_advisor_options(self, team: dict[str, Any]) -> list[dict[str, Any]]:
        advisor_names = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
        advisor_ids = [int(value) for value in (team.get("advisor_ids") or self._best_effort_advisor_ids(advisor_names)) if value is not None]
        advisor_relation_ids = [int(value) for value in (team.get("advisor_relation_ids") or []) if value is not None]
        lead_user_id = int(team.get("director_id") or team.get("lead_user_id") or 0) or None
        lead_name = self._resolve_center_director_name(team, advisor_names)
        options: list[dict[str, Any]] = []

        for index, advisor_name in enumerate(advisor_names):
            advisor_user_id = advisor_ids[index] if index < len(advisor_ids) else None
            advisor_relation_id = advisor_relation_ids[index] if index < len(advisor_relation_ids) else None
            options.append(
                {
                    "relation_id": advisor_relation_id,
                    "user_id": advisor_user_id,
                    "full_name": advisor_name,
                    "is_lead": lead_user_id is not None and advisor_user_id == lead_user_id,
                }
            )

        if lead_name and not any(
            option["full_name"] == lead_name and (lead_user_id is None or option.get("user_id") == lead_user_id)
            for option in options
        ):
            options.insert(
                0,
                {
                    "relation_id": None,
                    "user_id": lead_user_id,
                    "full_name": lead_name,
                    "is_lead": True,
                },
            )

        deduplicated: list[dict[str, Any]] = []
        seen_keys: set[tuple[int | None, str, int | None]] = set()
        for option in options:
            key = (
                int(option.get("user_id") or 0) or None,
                str(option.get("full_name") or "").strip(),
                int(option.get("relation_id") or 0) or None,
            )
            if key in seen_keys:
                continue
            seen_keys.add(key)
            deduplicated.append(option)
        return deduplicated

    def _resolve_center_director_name(self, item: dict[str, Any], advisor_names: list[str] | None = None) -> str:
        resolved_by_id = self._advisor_name_by_id(int(item.get("director_id") or 0) or None)
        if resolved_by_id:
            return resolved_by_id
        normalized_advisors = advisor_names or self._normalize_name_list(item.get("advisor_names", []), item.get("lead_advisor_name"))
        return str(item.get("lead_advisor_name") or "").strip() or (normalized_advisors[0] if normalized_advisors else "")

    def _build_center_record(self, item: dict[str, Any]) -> CenterRecord:
        members = [student for student in self._list("students") if student.get("team_name") == item["team_name"]]
        active_statuses = {"在校", "实习中", "外出研修", "请假中", "学位论文阶段"}
        advisor_names = self._normalize_name_list(item.get("advisor_names", []), item.get("lead_advisor_name"))
        return CenterRecord(
            id=item["id"],
            center_name=item["team_name"],
            director_name=self._resolve_center_director_name(item, advisor_names),
            director_id=int(item.get("director_id") or 0) or None,
            advisor_names=advisor_names,
            advisor_ids=[int(value) for value in (item.get("advisor_ids") or self._best_effort_advisor_ids(advisor_names)) if value is not None],
            advisor_relation_ids=[int(value) for value in (item.get("advisor_relation_ids") or []) if value is not None],
            is_enabled=item.get("status") == "启用",
            created_date=item.get("created_on") or item.get("established_on"),
            member_student_count=len(members),
            active_student_count=len([student for student in members if student.get("status") in active_statuses]),
        )

    def _ensure_team_exists(self, team_name: str | None = None, team_id: int | None = None) -> dict[str, Any]:
        team = None
        if team_id is not None:
            team = self._team_lookup_by_id().get(int(team_id))
        if team is None and team_name:
            team = self._team_lookup_by_name().get(team_name)
        if not team:
            raise ValueError("Selected team not found")
        return team

    def _resolve_portal_team_and_advisor(
        self,
        selected_team_id: int | None,
        selected_team_name: str | None,
        selected_advisor_user_id: int | None,
        selected_advisor_name: str | None,
        *,
        require_advisor: bool = True,
    ) -> dict[str, Any]:
        team = self._ensure_team_exists(team_name=selected_team_name, team_id=selected_team_id)
        advisor_options = self._team_advisor_options(team)
        option_by_user_id = {
            int(option["user_id"]): option
            for option in advisor_options
            if int(option.get("user_id") or 0) > 0
        }
        option_by_name: dict[str, list[dict[str, Any]]] = {}
        for option in advisor_options:
            full_name = str(option.get("full_name") or "").strip()
            if not full_name:
                continue
            option_by_name.setdefault(full_name, []).append(option)

        advisor_option: dict[str, Any] | None = None
        if selected_advisor_user_id is not None:
            advisor_option = option_by_user_id.get(int(selected_advisor_user_id))
            if advisor_option is None:
                raise ValueError("所选导师不属于当前团队")
        elif str(selected_advisor_name or "").strip():
            matched_options = option_by_name.get(str(selected_advisor_name).strip(), [])
            if not matched_options:
                raise ValueError("所选导师不属于当前团队")
            if len(matched_options) > 1:
                raise ValueError("当前团队存在同名导师，请按导师ID选择")
            advisor_option = matched_options[0]
        elif require_advisor:
            lead_user_id = int(team.get("director_id") or team.get("lead_user_id") or 0) or None
            if lead_user_id is not None and lead_user_id in option_by_user_id:
                advisor_option = option_by_user_id[lead_user_id]
            elif advisor_options:
                advisor_option = advisor_options[0]

        if require_advisor and advisor_option is None:
            raise ValueError("当前团队缺少可选导师")

        return {
            "team": team,
            "team_id": int(team.get("id") or 0),
            "team_name": str(team.get("team_name") or "").strip(),
            "advisor_user_id": int(advisor_option.get("user_id") or 0) or None if advisor_option else None,
            "advisor_name": str(advisor_option.get("full_name") or "").strip() or None if advisor_option else None,
        }

    def _validate_student_payload(self, payload: StudentUpsert, current_student_id: int | None = None) -> str:
        for item in self._list("students"):
            if item["student_no"] == payload.student_no and item["id"] != current_student_id:
                raise ValueError("Student number already exists")
        team = self._ensure_team_exists(team_name=payload.center_name)
        team_advisors = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
        advisor_name = self._resolve_advisor_name(payload.advisor_id, payload.advisor_name)
        if advisor_name not in team_advisors:
            raise ValueError("Selected advisor does not belong to the selected center")
        return advisor_name

    def _generate_admitted_student_no(self, enrollment_year: int) -> str:
        prefix = f"D{enrollment_year}"
        next_sequence = 1
        for item in self._list("students"):
            student_no = str(item.get("student_no") or "").strip()
            if not student_no.startswith(prefix):
                continue
            suffix = student_no[len(prefix):]
            if suffix.isdigit():
                next_sequence = max(next_sequence, int(suffix) + 1)
        return f"{prefix}{next_sequence:04d}"

    def _find_student_for_recruitment_application(self, application: dict[str, Any], phone_number: str | None = None) -> dict[str, Any] | None:
        portal_student_id = int(application.get("portal_student_id") or 0)
        full_name = str(application.get("student_name") or application.get("full_name") or "").strip()
        phone_value = str(phone_number or application.get("phone_number") or "").strip()
        for item in self._list("students"):
            if portal_student_id > 0 and int(item.get("portal_student_id") or 0) == portal_student_id:
                return item
            if phone_value and str(item.get("phone_number") or "").strip() == phone_value:
                return item
            if full_name and str(item.get("full_name") or "").strip() == full_name:
                return item
        return None

    def _sync_student_master_from_recruitment_application(self, application: dict[str, Any]) -> StudentRecord | None:
        status = str(application.get("application_status") or "").strip()
        if status not in ADMITTED_RECRUITMENT_APPLICATION_STATUSES:
            return None

        portal_student_id = int(application.get("portal_student_id") or 0)
        portal_student = next((item for item in self._list("portal_students") if int(item.get("id") or 0) == portal_student_id), None)
        center_name = str(
            (portal_student or {}).get("selected_team_name")
            or application.get("first_choice")
            or application.get("intended_field")
            or ""
        ).strip()
        if not center_name:
            return None

        center = next((item for item in self._list("teams") if str(item.get("team_name") or "").strip() == center_name), None)
        if center is None:
            return None

        advisor_candidates = self._normalize_name_list(center.get("advisor_names", []), center.get("lead_advisor_name"))
        advisor_name = str(
            (portal_student or {}).get("selected_advisor_name")
            or application.get("intended_advisor_name")
            or center.get("lead_advisor_name")
            or (advisor_candidates[0] if advisor_candidates else "")
        ).strip()
        if advisor_candidates and advisor_name not in advisor_candidates:
            advisor_name = advisor_candidates[0]
        if not advisor_name:
            return None

        applied_at = str(application.get("applied_at") or application.get("created_at") or "").strip()
        enrollment_year = int(applied_at[:4]) if len(applied_at) >= 4 and applied_at[:4].isdigit() else datetime.now().year
        full_name = str(application.get("student_name") or application.get("full_name") or (portal_student or {}).get("full_name") or "").strip()
        phone_value = str((portal_student or {}).get("phone_number") or application.get("phone_number") or "").strip() or None
        political_status = str((portal_student or {}).get("political_status") or application.get("political_status") or "").strip() or None
        existing_student = self._find_student_for_recruitment_application(application, phone_number=phone_value)
        payload = StudentUpsert(
            portal_student_id=portal_student_id or None,
            student_no=str(existing_student.get("student_no") or "").strip() if existing_student else self._generate_admitted_student_no(enrollment_year),
            full_name=full_name,
            status="在校",
            advisor_name=advisor_name,
            center_name=center_name,
            degree_type="工程博士",
            enrollment_year=enrollment_year,
            phone_number=phone_value,
            political_status=political_status,
        )
        if existing_student is not None:
            return self.update_student(int(existing_student["id"]), payload)
        return self.create_student(payload)

    def _validate_center_payload(self, payload: CenterUpsert, current_center_id: int | None = None) -> dict[str, Any]:
        for item in self._list("teams"):
            if item["team_name"] == payload.center_name and item["id"] != current_center_id:
                raise ValueError("Center name already exists")
        director_name = self._resolve_advisor_name(payload.director_id, payload.director_name)
        advisor_names = self._normalize_name_list(self._resolve_advisor_names(payload.advisor_ids, payload.advisor_names), director_name)
        if not advisor_names:
            raise ValueError("Center must contain at least one advisor")
        return {
            "team_name": payload.center_name,
            "lead_advisor_name": director_name,
            "director_id": payload.director_id,
            "advisor_names": advisor_names,
            "advisor_ids": [int(item) for item in (payload.advisor_ids or self._best_effort_advisor_ids(advisor_names)) if item is not None],
            "advisor_relation_ids": [int(item) for item in payload.advisor_relation_ids if item is not None],
            "status": "启用" if payload.is_enabled else "停用",
            "created_on": payload.created_date or datetime.now().strftime("%Y-%m-%d"),
        }

    def _role_lookup(self) -> dict[str, dict[str, Any]]:
        return {item["role_code"]: item for item in self._list("roles")}

    def _build_role_record(self, item: dict[str, Any]) -> RoleRecord:
        user_count = len([user for user in self._list("system_users") if user["role_code"] == item["role_code"]])
        normalized = {key: value for key, value in item.items() if key != "user_count"}
        return RoleRecord(**normalized, user_count=user_count)

    def _build_system_user_record(self, item: dict[str, Any]) -> SystemUserRecord:
        role = self._role_lookup().get(item["role_code"])
        profile = self.state.setdefault("profiles", {}).get(item["username"], {})
        return SystemUserRecord(
            id=item["id"],
            username=item["username"],
            full_name=item["full_name"],
            role_code=item["role_code"],
            role_name=role["role_name"] if role else item["role_code"],
            department_name=item["department_name"],
            introduction=item.get("introduction") or profile.get("introduction"),
            email=item.get("email") or profile.get("email"),
            phone_number=item.get("phone_number"),
            account_status=item["account_status"],
            last_login_at=item.get("last_login_at"),
        )

    def _ensure_role_exists(self, role_code: str) -> dict[str, Any]:
        role = self._role_lookup().get(role_code)
        if not role:
            raise ValueError("Role not found")
        return role

    def _validate_permissions(self, permissions: list[str]) -> list[str]:
        allowed_codes = {item["code"] for item in PERMISSION_CATALOG}
        invalid = [code for code in permissions if code not in allowed_codes]
        if invalid:
            raise ValueError(f"Invalid permissions: {', '.join(invalid)}")
        return list(dict.fromkeys(permissions))

    def _expand_granted_permissions(self, permissions: list[str]) -> list[str]:
        normalized_permissions = [str(item) for item in permissions if str(item).strip()]
        if "*" in normalized_permissions:
            return ["*"]
        expanded_permissions = list(dict.fromkeys(normalized_permissions))
        for permission in list(expanded_permissions):
            module_name, separator, action_name = permission.partition(":")
            if separator and action_name == "write":
                read_permission = f"{module_name}:read"
                if read_permission not in expanded_permissions:
                    expanded_permissions.append(read_permission)
        return expanded_permissions

    def get_permission_catalog(self) -> PermissionCatalogResponse:
        return PermissionCatalogResponse(items=[PermissionOption(**item) for item in PERMISSION_CATALOG])

    def _dict_options(self, dict_type: str) -> list[SelectOption]:
        return [
            SelectOption(
                label=item["label"],
                value=item["value"],
                color_type=item.get("color_type"),
                css_class=item.get("css_class"),
            )
            for item in self._postgres_store.list_dict_options(dict_type)
        ]

    def _dict_option_values(self, dict_type: str) -> list[str]:
        return [item.value for item in self._dict_options(dict_type)]

    def _reorder_portal_political_status_options(self, options: list[SelectOption]) -> list[SelectOption]:
        return sorted(
            options,
            key=lambda item: (
                PORTAL_POLITICAL_STATUS_PRIORITY.get(str(item.value or item.label), 1000),
                str(item.label or item.value),
            ),
        )

    def get_portal_profile_options(self) -> PortalProfileOptionsResponse:
        political_status_options = self._dict_options("student_political_status")
        ethnic_group_options = self._dict_options("student_ethnic_group")
        if not political_status_options:
            political_status_options = self._select_options_from_values(DEFAULT_PORTAL_POLITICAL_STATUS_VALUES)
        political_status_options = self._reorder_portal_political_status_options(political_status_options)
        if not ethnic_group_options:
            ethnic_group_options = self._select_options_from_values(DEFAULT_PORTAL_ETHNIC_GROUP_VALUES)
        return PortalProfileOptionsResponse(
            political_status_options=political_status_options,
            ethnic_group_options=ethnic_group_options,
        )

    def get_system_options(self) -> SystemOptionsResponse:
        return SystemOptionsResponse(
            account_status_options=self._dict_options("system_account_status"),
            role_scope_options=self._dict_options("system_role_scope"),
            integration_direction_options=self._dict_options("system_integration_direction"),
            integration_cadence_options=self._dict_options("system_integration_cadence"),
            integration_status_options=self._dict_options("system_integration_status"),
            audit_status_options=self._dict_options("system_audit_status"),
            operation_result_options=self._dict_options("system_operation_result"),
            sync_status_options=self._dict_options("system_sync_status"),
        )

    def get_training_options(self) -> TrainingOptionsResponse:
        advisor_values = sorted(
            {
                *[item["advisor_name"] for item in self._list("training_plans") if item.get("advisor_name")],
                *[item["advisor_name"] for item in self._list("outbound_studies") if item.get("advisor_name")],
                *[item["advisor_name"] for item in self._list("students") if item.get("advisor_name")],
            }
        )
        reviewer_values = sorted(
            {
                *[item["reviewer_name"] for item in self._list("scientific_reports") if item.get("reviewer_name")],
                *advisor_values,
            }
        )
        return TrainingOptionsResponse(
            plan_status_options=self._dict_options("training_plan_status"),
            report_cycle_options=self._dict_options("training_report_cycle"),
            report_status_options=self._dict_options("training_report_status"),
            study_type_options=self._dict_options("training_outbound_study_type"),
            approval_status_options=self._dict_options("training_outbound_approval_status"),
            advisor_options=[SelectOption(label=item, value=item) for item in advisor_values],
            reviewer_options=[SelectOption(label=item, value=item) for item in reviewer_values],
            student_options=self._training_student_options(),
        )

    def get_degree_options(self) -> DegreeOptionsResponse:
        advisor_values = self._advisor_name_values()
        expert_values = {
            *[item.get("expert_name") for item in self._list("thesis_reviews") if item.get("expert_name")],
            *advisor_values,
            *self._system_user_name_values(),
        }
        thesis_options = [
            SelectOption(label=f'{item["title"]}｜{item["student_name"]}', value=str(item["id"]))
            for item in sorted(self._list("theses"), key=lambda thesis: thesis["id"])
        ]
        return DegreeOptionsResponse(
            student_options=self._student_option_values(),
            advisor_options=[SelectOption(label=item, value=item) for item in advisor_values],
            thesis_options=thesis_options,
            thesis_status_options=self._dict_options("degree_thesis_status"),
            blind_review_status_options=self._dict_options("degree_blind_review_status"),
            defense_status_options=self._dict_options("degree_defense_status"),
            degree_status_options=self._dict_options("degree_status"),
            expert_options=self._select_options_from_values(expert_values),
            review_status_options=self._dict_options("degree_review_status"),
        )

    def get_recruitment_options(self) -> RecruitmentOptionsResponse:
        intended_fields = {
            *[field for team in self._list("teams") for field in team.get("research_directions", []) if field],
            *[item.get("intended_field") for item in self._list("recruitment_applications") if item.get("intended_field")],
        }
        graduation_schools = {item.get("graduation_school") for item in self._list("recruitment_applications") if item.get("graduation_school")}
        reviewers = {
            *[item.get("reviewer_name") for item in self._list("recruitment_applications") if item.get("reviewer_name")],
            *self._advisor_name_values(),
            *self._system_user_name_values(),
        }
        return RecruitmentOptionsResponse(
            semester_options=self._dict_options("recruitment_semester"),
            plan_stage_options=self._dict_options("recruitment_plan_stage"),
            degree_options=self._dict_options("recruitment_degree"),
            material_status_options=self._dict_options("recruitment_material_status"),
            application_status_options=self._dict_options("recruitment_application_status"),
            intended_field_options=self._select_options_from_values(intended_fields),
            reviewer_options=self._select_options_from_values(reviewers),
            graduation_school_options=self._select_options_from_values(graduation_schools),
        )

    def get_student_options(self) -> StudentOptionsResponse:
        advisor_options = self._advisor_select_options()
        advisor_option_map = {item.value: item for item in advisor_options}
        centers = self.get_centers(page=1, page_size=1000).items
        political_values = {
            *self._dict_option_values("student_political_status"),
            *[item.get("political_status") for item in self._list("students") if item.get("political_status")],
        }
        return StudentOptionsResponse(
            status_options=self._dict_options("student_status"),
            degree_options=self._dict_options("student_degree_type"),
            advisor_options=advisor_options,
            center_options=[SelectOption(label=item.center_name, value=item.center_name) for item in centers if item.is_enabled],
            political_status_options=self._select_options_from_values(political_values),
            center_advisor_map=[
                CenterAdvisorMapItem(
                    center_name=item.center_name,
                    advisors=[advisor_option_map[str(advisor_id)] for advisor_id in item.advisor_ids if str(advisor_id) in advisor_option_map],
                )
                for item in centers
            ],
        )

    def authenticate_system_user(self, username: str, password: str) -> dict[str, Any] | None:
        candidate = self._load_system_user_auth_context(username)
        if not candidate:
            return None
        if candidate["account_status"] != "启用":
            return None
        password_hash = candidate.get("password_hash")
        if not password_hash or not PASSWORD_CONTEXT.verify(password, password_hash):
            return None
        return self.get_principal_context(username)

    def get_principal_context(self, username: str) -> dict[str, Any]:
        user = self._load_system_user_auth_context(username)
        if not user or user["account_status"] != "启用":
            raise KeyError(username)
        return {
            "username": user["username"],
            "full_name": user["full_name"],
            "roles": [user["role_code"]],
            "permissions": self._expand_granted_permissions(user.get("permissions", [])),
        }

    def touch_last_login(self, username: str) -> None:
        with self._lock:
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    updated_user = {**item, "last_login_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    self._list("system_users")[index] = updated_user
                    self._postgres_store.update_runtime_system_user(int(updated_user["id"]), updated_user)
                    self._bump_system_user_list_cache_version()
                    return
            raise KeyError(username)

    def update_user_password(self, username: str, new_password: str) -> None:
        with self._lock:
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    updated_user = {**item, "password_hash": PASSWORD_CONTEXT.hash(new_password)}
                    self._list("system_users")[index] = updated_user
                    operation_log = self._record_operation("系统治理", "系统用户", username, "重置密码", f"更新账号 {username} 的登录密码", operator_username=username)
                    try:
                        self._postgres_store.update_runtime_system_user(int(updated_user["id"]), updated_user)
                        self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                        self._postgres_store.insert_runtime_operation_log(operation_log)
                    except Exception:
                        self._save()
                    self._delete_cache_keys(self._system_user_auth_cache_key(username))
                    return
            raise KeyError(username)

    def sync_to_postgres(self) -> None:
        self._postgres_store.save_state(self.state)

    def get_dashboard_overview(self) -> DashboardOverview:
        recruitment_stats = self.get_recruitment_stats()
        student_stats = self.get_student_stats()
        training_stats = self.get_training_stats()
        degree_stats = self.get_degree_stats()
        workflow_stats = self.get_workflow_stats()
        return DashboardOverview(
            lifecycle_coverage=[
                MetricCard(label="学生总量", value=str(student_stats.total_students), target="主数据", trend="招生到毕业全周期", status="healthy"),
                MetricCard(label="招生计划", value=str(recruitment_stats.plan_count), target="年度滚动", trend=f'累计 {recruitment_stats.application_total} 份申请', status="healthy"),
                MetricCard(label="在途审批", value=str(workflow_stats.todo_total + workflow_stats.in_progress_total), target="流程中心", trend="覆盖导师变更/外出研修/授位", status="attention"),
            ],
            recruitment_metrics=[
                MetricCard(label="招生计划", value=str(recruitment_stats.plan_count), target="年度批次", trend=f'累计申请 {recruitment_stats.application_total} 份', status="healthy"),
                MetricCard(label="待审核申请", value=str(recruitment_stats.pending_review_total), target="及时清零", trend="资格审核与材料评分中", status="attention"),
                MetricCard(label="预录取池", value=str(recruitment_stats.pre_admit_total), target="录取决策", trend="可下钻到候补与确认", status="healthy"),
            ],
            training_metrics=[
                MetricCard(label="培养方案", value=str(training_stats.training_plan_total), target="全部建档", trend=f'待确认 {training_stats.pending_confirmation_total} 份', status="healthy"),
                MetricCard(label="科研报告待审", value=str(training_stats.report_pending_total), target="按期审阅", trend="逾期自动升级提醒", status="attention"),
                MetricCard(label="外出研修在途", value=str(training_stats.outbound_active_total), target="过程闭环", trend="关联审批和成果归档", status="warning"),
            ],
            degree_metrics=[
                MetricCard(label="论文总量", value=str(degree_stats.thesis_total), target="学位季", trend="覆盖查重、盲审、答辩", status="healthy"),
                MetricCard(label="盲审待办", value=str(degree_stats.blind_review_pending_total), target="及时分派", trend="专家回执自动跟踪", status="attention"),
                MetricCard(label="待答辩", value=str(degree_stats.defense_pending_total), target="排期协调", trend="预答辩与正式答辩分开管理", status="warning"),
            ],
            workflow_metrics=[
                MetricCard(label="待处理审批", value=str(workflow_stats.todo_total), target="流程中心", trend="需及时分派", status="attention"),
                MetricCard(label="处理中审批", value=str(workflow_stats.in_progress_total), target="节点推进", trend="全程留痕", status="healthy"),
                MetricCard(label="超期审批", value=str(workflow_stats.overdue_total), target="0", trend="需要升级提醒", status="warning"),
            ],
            alerts=[
                DashboardAlert(level="high", title="科研报告待审阅", owner="培养管理", due_text=f'当前 {training_stats.report_pending_total} 份待审阅'),
                DashboardAlert(level="medium", title="预录取待确认", owner="招生管理", due_text=f'当前 {recruitment_stats.pre_admit_total} 人处于预录取池'),
                DashboardAlert(level="medium", title="审批超期待处理", owner="审批中心", due_text=f'当前 {workflow_stats.overdue_total} 项已超期'),
            ],
        )
