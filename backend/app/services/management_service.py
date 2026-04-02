from __future__ import annotations

from collections import Counter
from datetime import datetime
from threading import Lock
from typing import Any

from passlib.context import CryptContext

from app.schemas.auth import UserProfile, UserProfileUpdate
from app.schemas.dashboard import DashboardAlert, DashboardOverview, MetricCard
from app.schemas.recruitment import (
    RecruitApplicationListResponse,
    RecruitApplicationRecord,
    RecruitApplicationUpsert,
    RecruitPlanListResponse,
    RecruitPlanRecord,
    RecruitPlanSummary,
    RecruitPlanUpsert,
    RecruitmentOptionsResponse,
    RecruitStats,
    RecruitWorkbench,
)
from app.schemas.student import (
    StudentLifecycleBoard,
    StudentManagementResponse,
    StudentOptionsResponse,
    StudentRecord,
    StudentStateItem,
    StudentStats,
    StudentSummary,
    StudentUpsert,
    TeamAdvisorMapItem,
    TeamListResponse,
    TeamRecord,
    TeamUpsert,
)
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyRecord,
    AuditPolicyUpsert,
    BulkActionResponse,
    DictDataListResponse,
    DictDataRecord,
    DictDataUpsert,
    DictTypeListResponse,
    DictTypeRecord,
    DictTypeUpsert,
    IntegrationListResponse,
    IntegrationRecord,
    IntegrationUpsert,
    OperationLogListResponse,
    OperationLogRecord,
    PermissionCatalogResponse,
    PermissionOption,
    RoleListResponse,
    RoleRecord,
    RoleUpsert,
    SelectOption,
    SyncLogListResponse,
    SyncLogRecord,
    SystemArchitecture,
    SystemOptionsResponse,
    SystemStats,
    SystemUserListResponse,
    SystemUserRecord,
    SystemUserUpsert,
)
from app.schemas.training import (
    DegreeStats,
    DegreeWorkbench,
    OutboundStudyListResponse,
    OutboundStudyRecord,
    OutboundStudyUpsert,
    ScientificReportListResponse,
    ScientificReportRecord,
    ScientificReportUpsert,
    ThesisListResponse,
    ThesisRecord,
    ThesisReviewListResponse,
    ThesisReviewRecord,
    ThesisReviewUpsert,
    ThesisUpsert,
    DegreeOptionsResponse,
    TrainingStudentOption,
    TrainingOptionsResponse,
    TrainingPlanListResponse,
    TrainingPlanRecord,
    TrainingPlanUpsert,
    TrainingStats,
    TrainingTask,
    TrainingWorkbench,
)
from app.schemas.workflow import WorkflowOptionsResponse, WorkflowStats, WorkflowTaskListResponse, WorkflowTaskRecord, WorkflowTaskUpsert
from app.services.postgres_state_store import PostgresStateStore


PASSWORD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
DEFAULT_USER_PASSWORD = "ChangeMe@123"
DEFAULT_PASSWORD_BY_USERNAME = {
    "admin": "Admin@123456",
    "mentor.demo": "Mentor@123456",
    "secretary.demo": "Secretary@123456",
}
PERMISSION_CATALOG: list[dict[str, str]] = [
    {"code": "dashboard:read", "name": "查看驾驶舱", "module_name": "驾驶舱", "description": "查看系统总览、预警和统计看板。"},
    {"code": "recruitment:read", "name": "查看招生业务", "module_name": "招生管理", "description": "查看招生计划、报名申请和过程数据。"},
    {"code": "recruitment:write", "name": "维护招生业务", "module_name": "招生管理", "description": "新建、编辑和推进招生业务流程。"},
    {"code": "students:read", "name": "查看学生主档", "module_name": "学生管理", "description": "查看学生档案、状态和导师信息。"},
    {"code": "students:write", "name": "维护学生主档", "module_name": "学生管理", "description": "维护学生信息、导师和团队关系。"},
    {"code": "training:read", "name": "查看培养业务", "module_name": "培养管理", "description": "查看培养方案、科研汇报和研修安排。"},
    {"code": "training:write", "name": "维护培养业务", "module_name": "培养管理", "description": "维护培养方案、汇报审核和研修流程。"},
    {"code": "degree:read", "name": "查看学位业务", "module_name": "学位管理", "description": "查看论文、盲审和答辩进度。"},
    {"code": "degree:write", "name": "维护学位业务", "module_name": "学位管理", "description": "维护论文节点、送审和授位流程。"},
    {"code": "audit:read", "name": "查看审计日志", "module_name": "审计治理", "description": "查看审计策略、操作日志和同步日志。"},
    {"code": "audit:write", "name": "维护审计治理", "module_name": "审计治理", "description": "维护审计策略和审计治理配置。"},
    {"code": "system:read", "name": "查看系统治理", "module_name": "系统管理", "description": "查看系统用户、角色、权限和集成信息。"},
    {"code": "system:write", "name": "维护系统治理", "module_name": "系统管理", "description": "维护系统用户、角色、权限和集成配置。"},
    {"code": "workflow:read", "name": "查看流程任务", "module_name": "流程中心", "description": "查看审批任务和流程状态。"},
    {"code": "workflow:write", "name": "处理流程任务", "module_name": "流程中心", "description": "处理审批任务和推进流程节点。"},
]


class DemoManagementStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._postgres_store = PostgresStateStore()
        self.state = self._load_state()
        self._counters = self.state.setdefault("counters", {})
        if self._migrate_state():
            self._save()

    def _load_state(self) -> dict[str, Any]:
        postgres_state = self._postgres_store.load_state()
        if postgres_state:
            return postgres_state
        raise RuntimeError("PostgreSQL runtime state is required. Initialize and sync PostgreSQL before starting the application.")

    def _write_state(self, state: dict[str, Any] | None = None) -> None:
        payload = state or self.state
        self._postgres_store.save_state(payload)

    def _migrate_state(self) -> bool:
        changed = False
        role_lookup = {item["role_code"]: item for item in self.state.setdefault("roles", [])}
        profiles = self.state.setdefault("profiles", {})
        if "teams" not in self.state:
            self.state["teams"] = self._bootstrap_teams_from_students()
            changed = True
        self._counters.setdefault("teams", max([item.get("id", 0) for item in self.state.setdefault("teams", [])], default=0))

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
                        "description": "由历史学生主档自动迁移生成的团队记录。",
                    }
                )
                changed = True

        return changed

    def _next_id(self, key: str) -> int:
        self._counters[key] = int(self._counters.get(key, 0)) + 1
        return self._counters[key]

    def _record_operation(self, module_name: str, entity_name: str, entity_id: str, action: str, summary: str, operator_username: str = "admin") -> None:
        entry = {
            "id": self._next_id("operation_logs"),
            "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator_username": operator_username,
            "module_name": module_name,
            "entity_name": entity_name,
            "entity_id": entity_id,
            "action": action,
            "result": "success",
            "summary": summary,
        }
        self.state["operation_logs"].insert(0, entry)

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
                    "description": "由历史学生主档自动生成的团队记录。",
                },
            )
            current["advisor_names"] = self._normalize_name_list(current.get("advisor_names", []), item.get("advisor_name"))
        return list(grouped.values())

    def _advisor_name_values(self) -> list[str]:
        values = {
            *[item.get("lead_advisor_name") for item in self._list("teams") if item.get("lead_advisor_name")],
            *[advisor for item in self._list("teams") for advisor in item.get("advisor_names", []) if advisor],
            *[item.get("advisor_name") for item in self._list("students") if item.get("advisor_name")],
            *[item.get("advisor_name") for item in self._list("training_plans") if item.get("advisor_name")],
            *[item.get("advisor_name") for item in self._list("outbound_studies") if item.get("advisor_name")],
            *[item.get("advisor_name") for item in self._list("theses") if item.get("advisor_name")],
        }
        return sorted(str(item).strip() for item in values if str(item or "").strip())

    def _system_user_name_values(self) -> list[str]:
        values = {item.get("full_name") for item in self._list("system_users") if item.get("full_name")}
        return sorted(str(item).strip() for item in values if str(item or "").strip())

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

    def _build_team_record(self, item: dict[str, Any]) -> TeamRecord:
        members = [student for student in self._list("students") if student.get("team_name") == item["team_name"]]
        active_statuses = {"在校", "实习中", "外出研修", "请假中", "学位论文阶段"}
        return TeamRecord(
            id=item["id"],
            team_code=item["team_code"],
            team_name=item["team_name"],
            department_name=item["department_name"],
            discipline_name=item["discipline_name"],
            lead_advisor_name=item["lead_advisor_name"],
            advisor_names=self._normalize_name_list(item.get("advisor_names", []), item.get("lead_advisor_name")),
            research_directions=self._normalize_name_list(item.get("research_directions", [])),
            status=item["status"],
            established_on=item.get("established_on"),
            description=item.get("description"),
            member_student_count=len(members),
            active_student_count=len([student for student in members if student.get("status") in active_statuses]),
        )

    def _ensure_team_exists(self, team_name: str) -> dict[str, Any]:
        team = self._team_lookup_by_name().get(team_name)
        if not team:
            raise ValueError("Selected team not found")
        return team

    def _validate_student_payload(self, payload: StudentUpsert, current_student_id: int | None = None) -> None:
        for item in self._list("students"):
            if item["student_no"] == payload.student_no and item["id"] != current_student_id:
                raise ValueError("Student number already exists")
        team = self._ensure_team_exists(payload.team_name)
        team_advisors = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
        if payload.advisor_name not in team_advisors:
            raise ValueError("Selected advisor does not belong to the selected team")

    def _validate_team_payload(self, payload: TeamUpsert, current_team_id: int | None = None) -> dict[str, Any]:
        for item in self._list("teams"):
            if item["team_code"] == payload.team_code and item["id"] != current_team_id:
                raise ValueError("Team code already exists")
            if item["team_name"] == payload.team_name and item["id"] != current_team_id:
                raise ValueError("Team name already exists")
        advisor_names = self._normalize_name_list(payload.advisor_names, payload.lead_advisor_name)
        if not advisor_names:
            raise ValueError("Team must contain at least one advisor")
        return {
            **payload.model_dump(),
            "advisor_names": advisor_names,
            "research_directions": self._normalize_name_list(payload.research_directions),
        }

    def _role_lookup(self) -> dict[str, dict[str, Any]]:
        return {item["role_code"]: item for item in self._list("roles")}

    def _build_role_record(self, item: dict[str, Any]) -> RoleRecord:
        user_count = len([user for user in self._list("system_users") if user["role_code"] == item["role_code"]])
        return RoleRecord(**item, user_count=user_count)

    def _build_system_user_record(self, item: dict[str, Any]) -> SystemUserRecord:
        role = self._role_lookup().get(item["role_code"])
        return SystemUserRecord(
            id=item["id"],
            username=item["username"],
            full_name=item["full_name"],
            role_code=item["role_code"],
            role_name=role["role_name"] if role else item["role_code"],
            department_name=item["department_name"],
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
        teams = [self._build_team_record(item) for item in self._list("teams")]
        advisor_values = self._advisor_name_values()
        department_values = {item.department_name for item in teams if item.department_name}
        discipline_values = {item.discipline_name for item in teams if item.discipline_name}
        political_values = {
            *self._dict_option_values("student_political_status"),
            *[item.get("political_status") for item in self._list("students") if item.get("political_status")],
        }
        return StudentOptionsResponse(
            status_options=self._dict_options("student_status"),
            degree_options=self._dict_options("student_degree_type"),
            advisor_options=[SelectOption(label=item, value=item) for item in advisor_values],
            team_options=[SelectOption(label=item.team_name, value=item.team_name) for item in teams if item.status != "停用"],
            team_status_options=self._dict_options("student_team_status"),
            political_status_options=self._select_options_from_values(political_values),
            department_options=self._select_options_from_values(department_values),
            discipline_options=self._select_options_from_values(discipline_values),
            team_advisor_map=[
                TeamAdvisorMapItem(
                    team_name=item.team_name,
                    advisors=[SelectOption(label=advisor, value=advisor) for advisor in item.advisor_names],
                )
                for item in teams
            ],
        )

    def authenticate_system_user(self, username: str, password: str) -> dict[str, Any] | None:
        candidate = next((item for item in self._list("system_users") if item["username"] == username), None)
        if not candidate:
            return None
        if candidate["account_status"] != "启用":
            return None
        password_hash = candidate.get("password_hash")
        if not password_hash or not PASSWORD_CONTEXT.verify(password, password_hash):
            return None
        return self.get_principal_context(username)

    def get_principal_context(self, username: str) -> dict[str, Any]:
        user = next((item for item in self._list("system_users") if item["username"] == username), None)
        if not user or user["account_status"] != "启用":
            raise KeyError(username)
        role = self._ensure_role_exists(user["role_code"])
        return {
            "username": user["username"],
            "full_name": user["full_name"],
            "roles": [role["role_code"]],
            "permissions": role.get("permissions", []),
        }

    def touch_last_login(self, username: str) -> None:
        with self._lock:
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    self._list("system_users")[index] = {**item, "last_login_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    self._save()
                    return
            raise KeyError(username)

    def update_user_password(self, username: str, new_password: str) -> None:
        with self._lock:
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    self._list("system_users")[index] = {**item, "password_hash": PASSWORD_CONTEXT.hash(new_password)}
                    self._record_operation("系统治理", "系统用户", username, "重置密码", f"更新账号 {username} 的登录密码", operator_username=username)
                    self._save()
                    return
            raise KeyError(username)

    def sync_to_postgres(self) -> None:
        self._postgres_store.save_state(self.state)

    def _build_recruit_plan_record(self, item: dict[str, Any]) -> RecruitPlanRecord:
        application_count = len([application for application in self._list("recruitment_applications") if application["plan_id"] == item["id"]])
        return RecruitPlanRecord(
            id=item["id"],
            plan_name=item["plan_name"],
            academic_term=f'{item["academic_year"]} {item["semester"]}',
            academic_year=item["academic_year"],
            semester=item["semester"],
            current_stage=item["current_stage"],
            target_quota=item["target_quota"],
            application_count=application_count,
            interview_group_count=item["interview_group_count"],
            is_open=item["is_open"],
        )

    def get_dashboard_overview(self) -> DashboardOverview:
        recruitment_stats = self.get_recruitment_stats()
        student_stats = self.get_student_stats()
        training_stats = self.get_training_stats()
        degree_stats = self.get_degree_stats()
        workflow_stats = self.get_workflow_stats()
        return DashboardOverview(
            lifecycle_coverage=[
                MetricCard(label="学生总量", value=str(student_stats.total_students), target="主数据", trend="招生到毕业全周期", status="healthy"),
                MetricCard(label="开放招生计划", value=str(recruitment_stats.open_plan_count), target="年度滚动", trend=f'累计 {recruitment_stats.application_total} 份申请', status="healthy"),
                MetricCard(label="在途审批", value=str(workflow_stats.todo_total + workflow_stats.in_progress_total), target="流程中心", trend="覆盖导师变更/外出研修/授位", status="attention"),
            ],
            recruitment_metrics=[
                MetricCard(label="招生计划", value=str(recruitment_stats.plan_count), target="年度批次", trend=f'开放 {recruitment_stats.open_plan_count} 个', status="healthy"),
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

    def get_recruitment_workbench(self) -> RecruitWorkbench:
        status_counter = Counter(item["application_status"] for item in self._list("recruitment_applications"))
        return RecruitWorkbench(
            plans=[
                RecruitPlanSummary(
                    plan_name=plan.plan_name,
                    academic_term=plan.academic_term,
                    current_stage=plan.current_stage,
                    application_count=plan.application_count,
                    interview_group_count=plan.interview_group_count,
                )
                for plan in self.get_recruitment_plans().items
            ],
            pipeline=[
                {"stage": "报名已提交", "count": status_counter.get("报名已提交", 0), "status": "active"},
                {"stage": "资格审核通过", "count": status_counter.get("资格审核通过", 0), "status": "active"},
                {"stage": "材料评分中", "count": status_counter.get("材料评分中", 0), "status": "active"},
                {"stage": "面试完成", "count": status_counter.get("面试完成", 0), "status": "active"},
                {"stage": "预录取", "count": status_counter.get("预录取", 0) + status_counter.get("同意录取", 0), "status": "attention"},
            ],
            pending_tasks=[
                {"title": "资格审核待处理", "owner": "管理员", "due_text": "今日 18:00"},
                {"title": "评分人分配确认", "owner": "招生秘书", "due_text": "明日 12:00"},
                {"title": "面试组自动分配复核", "owner": "面试组织岗", "due_text": "两日内"},
            ],
        )

    def get_recruitment_plans(self) -> RecruitPlanListResponse:
        items = [self._build_recruit_plan_record(item) for item in self._list("recruitment_plans")]
        return RecruitPlanListResponse(items=items, total=len(items))

    def create_recruitment_plan(self, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("recruitment_plans")
            self._list("recruitment_plans").insert(0, item)
            self._record_operation("招生管理", "招生计划", str(item["id"]), "新增", f'新增招生计划 {item["plan_name"]}')
            self._save()
            return self._build_recruit_plan_record(item)

    def update_recruitment_plan(self, plan_id: int, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            index, item = self._find_required("recruitment_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("recruitment_plans")[index] = updated
            self._record_operation("招生管理", "招生计划", str(plan_id), "编辑", f'更新招生计划 {updated["plan_name"]}')
            self._save()
            return self._build_recruit_plan_record(updated)

    def get_recruitment_applications(self, keyword: str | None = None, plan_id: int | None = None, status: str | None = None) -> RecruitApplicationListResponse:
        items = list(self._list("recruitment_applications"))
        if plan_id is not None:
            items = [item for item in items if item["plan_id"] == plan_id]
        if status:
            items = [item for item in items if item["application_status"] == status]
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["candidate_no"].lower() or term in item["student_name"].lower() or term in item["graduation_school"].lower() or term in item["intended_field"].lower()]
        return RecruitApplicationListResponse(items=[RecruitApplicationRecord(**item) for item in items], total=len(items))

    def create_recruitment_application(self, payload: RecruitApplicationUpsert) -> RecruitApplicationRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("recruitment_applications")
            self._list("recruitment_applications").insert(0, item)
            self._record_operation("招生管理", "报名申请", str(item["id"]), "新增", f'新增报名申请 {item["student_name"]}')
            self._save()
            return RecruitApplicationRecord(**item)

    def update_recruitment_application(self, application_id: int, payload: RecruitApplicationUpsert) -> RecruitApplicationRecord:
        with self._lock:
            index, item = self._find_required("recruitment_applications", application_id)
            updated = {**item, **payload.model_dump(), "id": application_id}
            self._list("recruitment_applications")[index] = updated
            self._record_operation("招生管理", "报名申请", str(application_id), "编辑", f'更新报名申请 {updated["student_name"]}')
            self._save()
            return RecruitApplicationRecord(**updated)

    def delete_recruitment_application(self, application_id: int) -> None:
        with self._lock:
            index, item = self._find_required("recruitment_applications", application_id)
            self._list("recruitment_applications").pop(index)
            self._record_operation("招生管理", "报名申请", str(application_id), "删除", f'删除报名申请 {item["student_name"]}')
            self._save()

    def get_recruitment_stats(self) -> RecruitStats:
        plans = self._list("recruitment_plans")
        applications = self._list("recruitment_applications")
        return RecruitStats(
            plan_count=len(plans),
            open_plan_count=len([item for item in plans if item["is_open"]]),
            application_total=len(applications),
            pending_review_total=len([item for item in applications if item["application_status"] in {"报名已提交", "资格审核通过", "材料评分中", "面试待安排"}]),
            pre_admit_total=len([item for item in applications if item["application_status"] in {"预录取", "同意录取"}]),
        )

    def get_student_board(self) -> StudentLifecycleBoard:
        distribution = Counter(item["status"] for item in self._list("students"))
        return StudentLifecycleBoard(
            summary=[StudentSummary(student_no=item["student_no"], full_name=item["full_name"], status=item["status"], advisor_name=item["advisor_name"], team_name=item["team_name"]) for item in self._list("students")[:8]],
            state_distribution=[StudentStateItem(label=label, count=count) for label, count in distribution.items()],
        )

    def get_students(
        self,
        keyword: str | None = None,
        status: str | None = None,
        advisor_name: str | None = None,
        team_name: str | None = None,
    ) -> StudentManagementResponse:
        items = list(self._list("students"))
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["full_name"].lower() or term in item["team_name"].lower()]
        if status:
            items = [item for item in items if item["status"] == status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if team_name:
            items = [item for item in items if item["team_name"] == team_name]
        return StudentManagementResponse(items=[StudentRecord(**item) for item in items], total=len(items))

    def get_teams(
        self,
        keyword: str | None = None,
        status: str | None = None,
        department_name: str | None = None,
        lead_advisor_name: str | None = None,
    ) -> TeamListResponse:
        items = list(self._list("teams"))
        if keyword:
            items = [
                item for item in items
                if self._matches_keyword(
                    item.get("team_code"),
                    item.get("team_name"),
                    item.get("department_name"),
                    item.get("discipline_name"),
                    item.get("lead_advisor_name"),
                    *(item.get("research_directions") or []),
                    keyword=keyword,
                )
            ]
        if status:
            items = [item for item in items if item["status"] == status]
        if department_name:
            items = [item for item in items if item["department_name"] == department_name]
        if lead_advisor_name:
            items = [item for item in items if item["lead_advisor_name"] == lead_advisor_name]
        records = [self._build_team_record(item) for item in items]
        return TeamListResponse(items=records, total=len(records))

    def get_student_stats(self) -> StudentStats:
        distribution = Counter(item["status"] for item in self._list("students"))
        teams = self._list("teams")
        return StudentStats(
            total_students=len(self._list("students")),
            active_students=distribution.get("在校", 0) + distribution.get("实习中", 0),
            outbound_students=distribution.get("外出研修", 0),
            thesis_students=distribution.get("学位论文阶段", 0),
            advisor_count=len({item["advisor_name"] for item in self._list("students")}),
            team_total=len(teams),
            active_team_total=len([item for item in teams if item.get("status") == "启用"]),
        )

    def create_student(self, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            self._validate_student_payload(payload)
            item = payload.model_dump()
            item["id"] = self._next_id("students")
            self._list("students").insert(0, item)
            self._record_operation("学生管理", "学生主档", str(item["id"]), "新增", f'新增学生 {item["full_name"]}')
            self._save()
            return StudentRecord(**item)

    def update_student(self, student_id: int, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            self._validate_student_payload(payload, current_student_id=student_id)
            index, item = self._find_required("students", student_id)
            updated = {**item, **payload.model_dump(), "id": student_id}
            self._list("students")[index] = updated
            self._record_operation("学生管理", "学生主档", str(student_id), "编辑", f'更新学生 {updated["full_name"]}')
            self._save()
            return StudentRecord(**updated)

    def delete_student(self, student_id: int) -> None:
        with self._lock:
            index, item = self._find_required("students", student_id)
            self._list("students").pop(index)
            self._record_operation("学生管理", "学生主档", str(student_id), "删除", f'删除学生 {item["full_name"]}')
            self._save()

    def create_team(self, payload: TeamUpsert) -> TeamRecord:
        with self._lock:
            item = self._validate_team_payload(payload)
            item["id"] = self._next_id("teams")
            self._list("teams").insert(0, item)
            self._record_operation("学生管理", "团队主数据", str(item["id"]), "新增团队", f'新增团队 {item["team_name"]}')
            self._save()
            return self._build_team_record(item)

    def update_team(self, team_id: int, payload: TeamUpsert) -> TeamRecord:
        with self._lock:
            index, current = self._find_required("teams", team_id)
            validated = self._validate_team_payload(payload, current_team_id=team_id)
            if current["team_name"] != validated["team_name"]:
                for student in self._list("students"):
                    if student.get("team_name") == current["team_name"]:
                        student["team_name"] = validated["team_name"]
            if any(student.get("team_name") == validated["team_name"] and student.get("advisor_name") not in validated["advisor_names"] for student in self._list("students")):
                raise ValueError("Current team members contain advisors outside the selected advisor set")
            updated = {**current, **validated, "id": team_id}
            self._list("teams")[index] = updated
            self._record_operation("学生管理", "团队主数据", str(team_id), "编辑团队", f'更新团队 {updated["team_name"]}')
            self._save()
            return self._build_team_record(updated)

    def delete_team(self, team_id: int) -> None:
        with self._lock:
            index, item = self._find_required("teams", team_id)
            if any(student.get("team_name") == item["team_name"] for student in self._list("students")):
                raise ValueError("Team still has assigned students and cannot be deleted")
            self._list("teams").pop(index)
            self._record_operation("学生管理", "团队主数据", str(team_id), "删除团队", f'删除团队 {item["team_name"]}')
            self._save()

    def delete_teams(self, team_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for team_id in team_ids:
            self.delete_team(team_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_training_workbench(self) -> TrainingWorkbench:
        outbound_counter = Counter(item["approval_status"] for item in self._list("outbound_studies"))
        return TrainingWorkbench(
            open_tasks=[
                TrainingTask(title="培养方案待学生确认", owner="导师", due_text="剩余 2 天", status="pending"),
                TrainingTask(title="科研报告待审阅", owner="导师", due_text="剩余 1 天", status="warning"),
                TrainingTask(title="外出研修超期未归提醒", owner="学合管理员", due_text="需要今日处置", status="critical"),
            ],
            supervision_rules=[
                {"rule": "入学 15 日内制定培养方案", "owner": "导师", "trigger": "自动待办"},
                {"rule": "学生 7 日内确认培养方案", "owner": "学生", "trigger": "站内信提醒"},
                {"rule": "科研报告逾期 7 日提醒导师", "owner": "系统控制", "trigger": "升级提醒"},
                {"rule": "外出研修需导师和学合管理员双节点审批", "owner": "审批中心", "trigger": "严格串行"},
            ],
            outbound_study_status=[
                {"status": label, "count": count} for label, count in outbound_counter.items()
            ],
        )

    def get_training_plans(
        self,
        keyword: str | None = None,
        plan_status: str | None = None,
        advisor_name: str | None = None,
        report_cycle: str | None = None,
    ) -> TrainingPlanListResponse:
        items = list(self._list("training_plans"))
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item["student_no"], item["student_name"], item["scientific_goal"], keyword=keyword)
            ]
        if plan_status:
            items = [item for item in items if item["plan_status"] == plan_status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if report_cycle:
            items = [item for item in items if item["report_cycle"] == report_cycle]
        items = [TrainingPlanRecord(**item) for item in items]
        return TrainingPlanListResponse(items=items, total=len(items))

    def create_training_plan(self, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("training_plans")
            self._list("training_plans").insert(0, item)
            self._record_operation("培养管理", "培养方案", str(item["id"]), "登记方案", f'登记培养方案 {item["student_name"]}')
            self._save()
            return TrainingPlanRecord(**item)

    def update_training_plan(self, plan_id: int, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("training_plans")[index] = updated
            self._record_operation("培养管理", "培养方案", str(plan_id), "维护方案", f'维护培养方案 {updated["student_name"]}')
            self._save()
            return TrainingPlanRecord(**updated)

    def delete_training_plan(self, plan_id: int) -> None:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            self._list("training_plans").pop(index)
            self._record_operation("培养管理", "培养方案", str(plan_id), "删除方案", f'删除培养方案 {item["student_name"]}')
            self._save()

    def delete_training_plans(self, plan_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for plan_id in plan_ids:
            self.delete_training_plan(plan_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_scientific_reports(
        self,
        keyword: str | None = None,
        status: str | None = None,
        reviewer_name: str | None = None,
    ) -> ScientificReportListResponse:
        items = list(self._list("scientific_reports"))
        if status:
            items = [item for item in items if item["report_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item["student_no"], item["student_name"], item["period_label"], item["summary"], keyword=keyword)
            ]
        if reviewer_name:
            items = [item for item in items if item.get("reviewer_name") == reviewer_name]
        return ScientificReportListResponse(items=[ScientificReportRecord(**item) for item in items], total=len(items))

    def create_scientific_report(self, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("scientific_reports")
            self._list("scientific_reports").insert(0, item)
            self._record_operation("培养管理", "科研报告", str(item["id"]), "登记报告", f'登记科研报告 {item["student_name"]}')
            self._save()
            return ScientificReportRecord(**item)

    def update_scientific_report(self, report_id: int, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            updated = {**item, **payload.model_dump(), "id": report_id}
            self._list("scientific_reports")[index] = updated
            self._record_operation("培养管理", "科研报告", str(report_id), "维护报告", f'维护科研报告 {updated["student_name"]}')
            self._save()
            return ScientificReportRecord(**updated)

    def delete_scientific_report(self, report_id: int) -> None:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            self._list("scientific_reports").pop(index)
            self._record_operation("培养管理", "科研报告", str(report_id), "删除报告", f'删除科研报告 {item["student_name"]}')
            self._save()

    def delete_scientific_reports(self, report_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for report_id in report_ids:
            self.delete_scientific_report(report_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_outbound_studies(
        self,
        keyword: str | None = None,
        status: str | None = None,
        study_type: str | None = None,
        advisor_name: str | None = None,
    ) -> OutboundStudyListResponse:
        items = list(self._list("outbound_studies"))
        if status:
            items = [item for item in items if item["approval_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item["student_no"], item["student_name"], item["destination"], item.get("expected_outcome"), keyword=keyword)
            ]
        if study_type:
            items = [item for item in items if item["study_type"] == study_type]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        return OutboundStudyListResponse(items=[OutboundStudyRecord(**item) for item in items], total=len(items))

    def create_outbound_study(self, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("outbound_studies")
            self._list("outbound_studies").insert(0, item)
            self._record_operation("培养管理", "外出研修", str(item["id"]), "发起研修", f'发起外出研修 {item["student_name"]}')
            self._save()
            return OutboundStudyRecord(**item)

    def update_outbound_study(self, study_id: int, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            updated = {**item, **payload.model_dump(), "id": study_id}
            self._list("outbound_studies")[index] = updated
            self._record_operation("培养管理", "外出研修", str(study_id), "维护研修", f'维护外出研修 {updated["student_name"]}')
            self._save()
            return OutboundStudyRecord(**updated)

    def delete_outbound_study(self, study_id: int) -> None:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            self._list("outbound_studies").pop(index)
            self._record_operation("培养管理", "外出研修", str(study_id), "删除研修", f'删除外出研修 {item["student_name"]}')
            self._save()

    def delete_outbound_studies(self, study_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for study_id in study_ids:
            self.delete_outbound_study(study_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_training_stats(self) -> TrainingStats:
        return TrainingStats(
            training_plan_total=len(self._list("training_plans")),
            pending_confirmation_total=len([item for item in self._list("training_plans") if item["plan_status"] == "待学生确认"]),
            report_pending_total=len([item for item in self._list("scientific_reports") if item["report_status"] in {"待导师审阅", "退回修改"}]),
            outbound_active_total=len([item for item in self._list("outbound_studies") if item["approval_status"] in {"审批中", "研修中"}]),
        )

    def get_degree_workbench(self) -> DegreeWorkbench:
        status_counter = Counter(item["degree_status"] for item in self._list("theses"))
        return DegreeWorkbench(
            thesis_pipeline=[
                {"stage": "查重中", "count": len([item for item in self._list("theses") if item["thesis_status"] in {"待查重", "查重中"}])},
                {"stage": "盲审中", "count": len([item for item in self._list("theses") if item["blind_review_status"] == "进行中"])},
                {"stage": "预答辩待安排", "count": len([item for item in self._list("theses") if item["defense_status"] == "待安排"])},
                {"stage": "正式答辩待安排", "count": len([item for item in self._list("theses") if item["degree_status"] == "待正式答辩"])},
                {"stage": "授位审批", "count": status_counter.get("授位审批中", 0)},
            ],
            committee_tasks=[
                TrainingTask(title="指派盲审专家", owner="学位秘书", due_text="本周内", status="pending"),
                TrainingTask(title="组织预答辩会议", owner="导师", due_text="剩余 5 天", status="warning"),
                TrainingTask(title="学位委员会审议", owner="委员会秘书", due_text="答辩后 7 日内", status="pending"),
            ],
        )

    def get_theses(self, keyword: str | None = None, degree_status: str | None = None) -> ThesisListResponse:
        items = list(self._list("theses"))
        if degree_status:
            items = [item for item in items if item["degree_status"] == degree_status]
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["student_name"].lower() or term in item["title"].lower()]
        return ThesisListResponse(items=[ThesisRecord(**item) for item in items], total=len(items))

    def create_thesis(self, payload: ThesisUpsert) -> ThesisRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("theses")
            self._list("theses").insert(0, item)
            self._record_operation("学位管理", "论文主档", str(item["id"]), "新增", f'新增论文 {item["student_name"]}')
            self._save()
            return ThesisRecord(**item)

    def update_thesis(self, thesis_id: int, payload: ThesisUpsert) -> ThesisRecord:
        with self._lock:
            index, item = self._find_required("theses", thesis_id)
            updated = {**item, **payload.model_dump(), "id": thesis_id}
            self._list("theses")[index] = updated
            self._record_operation("学位管理", "论文主档", str(thesis_id), "编辑", f'更新论文 {updated["student_name"]}')
            self._save()
            return ThesisRecord(**updated)

    def get_thesis_reviews(self, thesis_id: int | None = None) -> ThesisReviewListResponse:
        items = list(self._list("thesis_reviews"))
        if thesis_id is not None:
            items = [item for item in items if item["thesis_id"] == thesis_id]
        return ThesisReviewListResponse(items=[ThesisReviewRecord(**item) for item in items], total=len(items))

    def create_thesis_review(self, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("thesis_reviews")
            self._list("thesis_reviews").insert(0, item)
            self._record_operation("学位管理", "盲审意见", str(item["id"]), "新增", f'新增盲审意见 {item["expert_name"]}')
            self._save()
            return ThesisReviewRecord(**item)

    def update_thesis_review(self, review_id: int, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            index, item = self._find_required("thesis_reviews", review_id)
            updated = {**item, **payload.model_dump(), "id": review_id}
            self._list("thesis_reviews")[index] = updated
            self._record_operation("学位管理", "盲审意见", str(review_id), "编辑", f'更新盲审意见 {updated["expert_name"]}')
            self._save()
            return ThesisReviewRecord(**updated)

    def get_degree_stats(self) -> DegreeStats:
        return DegreeStats(
            thesis_total=len(self._list("theses")),
            plagiarism_pending_total=len([item for item in self._list("theses") if item["thesis_status"] in {"待查重", "查重中"}]),
            blind_review_pending_total=len([item for item in self._list("theses") if item["blind_review_status"] in {"进行中", "未送审"}]),
            defense_pending_total=len([item for item in self._list("theses") if item["defense_status"] in {"待安排", "未进入"}]),
            degree_granted_total=len([item for item in self._list("theses") if item["degree_status"] == "已授位"]),
        )

    def get_workflow_options(self) -> WorkflowOptionsResponse:
        applicants = {
            *[item.get("applicant_name") for item in self._list("workflow_tasks") if item.get("applicant_name")],
            *[item.get("full_name") for item in self._list("students") if item.get("full_name")],
        }
        handlers = {
            *[item.get("current_handler") for item in self._list("workflow_tasks") if item.get("current_handler")],
            *self._advisor_name_values(),
            *self._system_user_name_values(),
        }
        return WorkflowOptionsResponse(
            workflow_name_options=self._select_options_from_values([item.get("workflow_name") for item in self._list("workflow_tasks")]),
            business_module_options=self._select_options_from_values([item.get("business_module") for item in self._list("workflow_tasks")]),
            applicant_options=self._select_options_from_values(applicants),
            handler_options=self._select_options_from_values(handlers),
            current_node_options=self._select_options_from_values([item.get("current_node") for item in self._list("workflow_tasks")]),
            priority_options=self._dict_options("workflow_priority"),
            status_options=self._dict_options("workflow_status"),
        )

    def get_dict_types(self, keyword: str | None = None, status: str | None = None) -> DictTypeListResponse:
        records = self._postgres_store.list_dict_types(keyword=keyword, status=status)
        return DictTypeListResponse(items=[DictTypeRecord(**item) for item in records], total=len(records))

    def create_dict_type(self, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.create_dict_type(payload.model_dump())
        return DictTypeRecord(**record)

    def update_dict_type(self, dict_type_id: int, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.update_dict_type(dict_type_id, payload.model_dump())
        return DictTypeRecord(**record)

    def delete_dict_type(self, dict_type_id: int) -> None:
        self._postgres_store.delete_dict_type(dict_type_id)

    def get_dict_data(self, keyword: str | None = None, dict_type: str | None = None, status: str | None = None) -> DictDataListResponse:
        records = self._postgres_store.list_dict_data(keyword=keyword, dict_type=dict_type, status=status)
        return DictDataListResponse(items=[DictDataRecord(**item) for item in records], total=len(records))

    def create_dict_data(self, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.create_dict_data(payload.model_dump())
        return DictDataRecord(**record)

    def update_dict_data(self, dict_data_id: int, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.update_dict_data(dict_data_id, payload.model_dump())
        return DictDataRecord(**record)

    def delete_dict_data(self, dict_data_id: int) -> None:
        self._postgres_store.delete_dict_data(dict_data_id)

    def get_roles(self, keyword: str | None = None, scope_name: str | None = None, permission: str | None = None) -> RoleListResponse:
        items = list(self._list("roles"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["role_code"], item["role_name"], item["scope_name"], keyword=keyword)]
        if scope_name:
            items = [item for item in items if item["scope_name"] == scope_name]
        if permission:
            items = [item for item in items if permission in item.get("permissions", [])]
        items = [self._build_role_record(item) for item in items]
        return RoleListResponse(items=items, total=len(items))

    def create_role(self, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            item = payload.model_dump()
            if any(role["role_code"] == item["role_code"] for role in self._list("roles")):
                raise ValueError("Role code already exists")
            item["permissions"] = self._validate_permissions(item.get("permissions", []))
            item["id"] = self._next_id("roles")
            self._list("roles").insert(0, item)
            self._record_operation("系统治理", "角色", str(item["id"]), "新建角色", f'新建角色 {item["role_name"]}')
            self._save()
            return self._build_role_record(item)

    def update_role(self, role_id: int, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            new_values = payload.model_dump()
            if any(role["role_code"] == new_values["role_code"] and role["id"] != role_id for role in self._list("roles")):
                raise ValueError("Role code already exists")
            new_values["permissions"] = self._validate_permissions(new_values.get("permissions", []))
            updated = {**item, **new_values, "id": role_id}
            self._list("roles")[index] = updated
            if item["role_code"] != updated["role_code"]:
                for user_index, user in enumerate(self._list("system_users")):
                    if user["role_code"] == item["role_code"]:
                        self._list("system_users")[user_index] = {**user, "role_code": updated["role_code"]}
                for username, profile in self.state.setdefault("profiles", {}).items():
                    if profile.get("role_name") in {item["role_name"], item["role_code"]}:
                        self.state["profiles"][username] = {**profile, "role_name": updated["role_name"]}
            self._record_operation("系统治理", "角色", str(role_id), "调整权限", f'更新角色 {updated["role_name"]} 的权限配置')
            self._save()
            return self._build_role_record(updated)

    def delete_role(self, role_id: int) -> None:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            in_use = next((user for user in self._list("system_users") if user["role_code"] == item["role_code"]), None)
            if in_use:
                raise ValueError("Role is assigned to users")
            self._list("roles").pop(index)
            self._record_operation("系统治理", "角色", str(role_id), "删除角色", f'删除角色 {item["role_name"]}')
            self._save()

    def delete_roles(self, role_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for role_id in role_ids:
            self.delete_role(role_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_system_users(
        self,
        keyword: str | None = None,
        role_code: str | None = None,
        account_status: str | None = None,
        department_name: str | None = None,
    ) -> SystemUserListResponse:
        items = list(self._list("system_users"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["username"], item["full_name"], item["department_name"], keyword=keyword)]
        if role_code:
            items = [item for item in items if item["role_code"] == role_code]
        if account_status:
            items = [item for item in items if item["account_status"] == account_status]
        if department_name:
            items = [item for item in items if department_name in item["department_name"]]
        items = [self._build_system_user_record(item) for item in items]
        return SystemUserListResponse(items=items, total=len(items))

    def create_system_user(self, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            item = payload.model_dump()
            if any(user["username"] == item["username"] for user in self._list("system_users")):
                raise ValueError("Username already exists")
            role = self._ensure_role_exists(item["role_code"])
            item["id"] = self._next_id("system_users")
            item["password_hash"] = PASSWORD_CONTEXT.hash(item.pop("password") or DEFAULT_USER_PASSWORD)
            item["last_login_at"] = None
            self._list("system_users").insert(0, item)
            self.state.setdefault("profiles", {})[item["username"]] = {
                "username": item["username"],
                "full_name": item["full_name"],
                "role_name": role["role_name"],
                "department_name": item["department_name"],
                "phone_number": item.get("phone_number"),
                "email": None,
                "theme_color": "#0f4cbd",
            }
            self._record_operation("系统治理", "系统用户", str(item["id"]), "新建账号", f'新建系统账号 {item["full_name"]}')
            self._save()
            return self._build_system_user_record(item)

    def update_system_user(self, user_id: int, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            new_values = payload.model_dump()
            if any(user["username"] == new_values["username"] and user["id"] != user_id for user in self._list("system_users")):
                raise ValueError("Username already exists")
            role = self._ensure_role_exists(new_values["role_code"])
            password = new_values.pop("password")
            updated = {**item, **new_values, "id": user_id}
            if password:
                updated["password_hash"] = PASSWORD_CONTEXT.hash(password)
            self._list("system_users")[index] = updated
            profile = self.state.setdefault("profiles", {}).get(updated["username"], {})
            self.state["profiles"][updated["username"]] = {
                "username": updated["username"],
                "full_name": updated["full_name"],
                "role_name": role["role_name"],
                "department_name": updated["department_name"],
                "phone_number": updated.get("phone_number"),
                "email": profile.get("email"),
                "theme_color": profile.get("theme_color", "#0f4cbd"),
            }
            if item["username"] != updated["username"]:
                old_profile = self.state.setdefault("profiles", {}).pop(item["username"], None)
                if old_profile:
                    self.state["profiles"][updated["username"]] = {**old_profile, "username": updated["username"]}
            action_name = "停用账号" if updated["account_status"] != "启用" and item.get("account_status") == "启用" else "维护账号"
            self._record_operation("系统治理", "系统用户", str(user_id), action_name, f'更新系统账号 {updated["full_name"]}')
            self._save()
            return self._build_system_user_record(updated)

    def delete_system_user(self, user_id: int, current_username: str | None = None) -> None:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            if current_username and item["username"] == current_username:
                raise ValueError("Cannot delete current user")
            self._list("system_users").pop(index)
            self.state.setdefault("profiles", {}).pop(item["username"], None)
            self._record_operation("系统治理", "系统用户", str(user_id), "删除账号", f'删除系统账号 {item["full_name"]}')
            self._save()

    def delete_system_users(self, user_ids: list[int], current_username: str | None = None) -> BulkActionResponse:
        success_count = 0
        for user_id in user_ids:
            self.delete_system_user(user_id, current_username=current_username)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_audit_policy_records(self, keyword: str | None = None, status: str | None = None) -> AuditPolicyListResponse:
        items = list(self._list("audit_policies"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["item"], item["policy"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        items = [AuditPolicyRecord(**item) for item in items]
        return AuditPolicyListResponse(items=items, total=len(items))

    def create_audit_policy(self, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("audit_policies")
            self._list("audit_policies").insert(0, item)
            self._record_operation("系统治理", "审计策略", str(item["id"]), "新建策略", f'新建审计策略 {item["item"]}')
            self._save()
            return AuditPolicyRecord(**item)

    def update_audit_policy(self, policy_id: int, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            updated = {**item, **payload.model_dump(), "id": policy_id}
            self._list("audit_policies")[index] = updated
            self._record_operation("系统治理", "审计策略", str(policy_id), "维护策略", f'更新审计策略 {updated["item"]}')
            self._save()
            return AuditPolicyRecord(**updated)

    def delete_audit_policy(self, policy_id: int) -> None:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            self._list("audit_policies").pop(index)
            self._record_operation("系统治理", "审计策略", str(policy_id), "删除策略", f'删除审计策略 {item["item"]}')
            self._save()

    def delete_audit_policies(self, policy_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for policy_id in policy_ids:
            self.delete_audit_policy(policy_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_integrations(self, keyword: str | None = None, status: str | None = None, direction: str | None = None) -> IntegrationListResponse:
        items = list(self._list("integrations"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["name"], item["owner"], item["direction"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        if direction:
            items = [item for item in items if item["direction"] == direction]
        items = [IntegrationRecord(**item) for item in items]
        return IntegrationListResponse(items=items, total=len(items))

    def create_integration(self, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("integrations")
            self._list("integrations").insert(0, item)
            self._record_operation("系统治理", "集成链路", str(item["id"]), "新建链路", f'新建集成链路 {item["name"]}')
            self._save()
            return IntegrationRecord(**item)

    def update_integration(self, integration_id: int, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            updated = {**item, **payload.model_dump(), "id": integration_id}
            self._list("integrations")[index] = updated
            self._record_operation("系统治理", "集成链路", str(integration_id), "维护链路", f'更新集成链路 {updated["name"]}')
            self._save()
            return IntegrationRecord(**updated)

    def delete_integration(self, integration_id: int) -> None:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            self._list("integrations").pop(index)
            self._record_operation("系统治理", "集成链路", str(integration_id), "删除链路", f'删除集成链路 {item["name"]}')
            self._save()

    def delete_integrations(self, integration_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for integration_id in integration_ids:
            self.delete_integration(integration_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_operation_logs(self, keyword: str | None = None, module_name: str | None = None, result: str | None = None) -> OperationLogListResponse:
        items = list(self._list("operation_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["operator_username"], item["entity_name"], item["summary"], keyword=keyword)]
        if module_name:
            items = [item for item in items if item["module_name"] == module_name]
        if result:
            items = [item for item in items if item["result"] == result]
        items = [OperationLogRecord(**item) for item in items]
        return OperationLogListResponse(items=items, total=len(items))

    def get_sync_logs(self, keyword: str | None = None, sync_status: str | None = None, source_system: str | None = None) -> SyncLogListResponse:
        items = list(self._list("sync_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["source_system"], item["target_system"], item.get("failure_reason"), keyword=keyword)]
        if sync_status:
            items = [item for item in items if item["sync_status"] == sync_status]
        if source_system:
            items = [item for item in items if item["source_system"] == source_system]
        items = [SyncLogRecord(**item) for item in items]
        return SyncLogListResponse(items=items, total=len(items))

    def get_system_architecture(self) -> SystemArchitecture:
        return SystemArchitecture(
            authentication="JWT + RBAC",
            database="PostgreSQL 17-",
            cache="Redis Sentinel",
            audit=["login_logs", "operation_logs", "data_sync_logs"],
            integrations=[item["name"] for item in self._list("integrations")],
        )

    def get_system_stats(self) -> SystemStats:
        return SystemStats(
            integration_total=len(self._list("integrations")),
            active_integration_total=len([item for item in self._list("integrations") if item["status"] == "正常"]),
            operation_log_total=len(self._list("operation_logs")),
            sync_failure_total=len([item for item in self._list("sync_logs") if item["sync_status"] != "success"]),
            user_total=len(self._list("system_users")),
            role_total=len(self._list("roles")),
        )

    def get_workflow_tasks(self, status: str | None = None, module: str | None = None) -> WorkflowTaskListResponse:
        items = list(self._list("workflow_tasks"))
        if status:
            items = [item for item in items if item["status"] == status]
        if module:
            items = [item for item in items if item["business_module"] == module]
        return WorkflowTaskListResponse(items=[WorkflowTaskRecord(**item) for item in items], total=len(items))

    def create_workflow_task(self, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("workflow_tasks")
            self._list("workflow_tasks").insert(0, item)
            self._record_operation("审批中心", "审批任务", str(item["id"]), "新增", f'新增审批任务 {item["title"]}')
            self._save()
            return WorkflowTaskRecord(**item)

    def update_workflow_task(self, task_id: int, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            updated = {**item, **payload.model_dump(), "id": task_id}
            self._list("workflow_tasks")[index] = updated
            self._record_operation("审批中心", "审批任务", str(task_id), "编辑", f'更新审批任务 {updated["title"]}')
            self._save()
            return WorkflowTaskRecord(**updated)

    def delete_workflow_task(self, task_id: int) -> None:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            self._list("workflow_tasks").pop(index)
            self._record_operation("审批中心", "审批任务", str(task_id), "删除", f'删除审批任务 {item["title"]}')
            self._save()

    def get_workflow_stats(self) -> WorkflowStats:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = self._list("workflow_tasks")
        overdue_total = len([item for item in items if item["status"] in {"待处理", "处理中"} and item["due_at"] < now])
        return WorkflowStats(
            todo_total=len([item for item in items if item["status"] == "待处理"]),
            in_progress_total=len([item for item in items if item["status"] == "处理中"]),
            approved_total=len([item for item in items if item["status"] == "已通过"]),
            rejected_total=len([item for item in items if item["status"] == "已驳回"]),
            overdue_total=overdue_total,
        )

    def get_profile(self, username: str) -> UserProfile:
        profile = self.state.setdefault("profiles", {}).get(username)
        if not profile:
            fallback = next((item for item in self._list("system_users") if item["username"] == username), None)
            if not fallback:
                raise KeyError(username)
            role = self._role_lookup().get(fallback["role_code"])
            profile = {
                "username": fallback["username"],
                "full_name": fallback["full_name"],
                "role_name": role["role_name"] if role else fallback["role_code"],
                "department_name": fallback["department_name"],
                "phone_number": fallback.get("phone_number"),
                "email": None,
                "theme_color": "#0f4cbd",
            }
            self.state.setdefault("profiles", {})[username] = profile
            self._save()
        return UserProfile(**profile)

    def update_profile(self, username: str, payload: UserProfileUpdate) -> UserProfile:
        with self._lock:
            current = self.get_profile(username).model_dump()
            updated = {**current, **payload.model_dump(), "username": username}
            self.state.setdefault("profiles", {})[username] = updated
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    self._list("system_users")[index] = {**item, "full_name": updated["full_name"], "phone_number": updated.get("phone_number")}
                    break
            self._record_operation("个人空间", "个人资料", username, "编辑", f'更新个人资料 {updated["full_name"]}', operator_username=username)
            self._save()
            return UserProfile(**updated)


store = DemoManagementStore()
