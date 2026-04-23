from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
import logging
import secrets
import string
from threading import Lock, RLock
from typing import Any, TypeVar

from passlib.context import CryptContext

from app.core.cache import build_cache_key, get_cache_client
from app.schemas.auth import UserProfile, UserProfileUpdate
from app.schemas.portal import (
    PortalApplicationSubmissionResponse,
    PortalApplicationDraftUpsert,
    PortalApplicationUpsert,
    PortalLoginRequest,
    PortalPasswordChangeRequest,
    PortalPlanListResponse,
    PortalPlanRecord,
    PortalProfileOptionsResponse,
    PortalPasswordResetRequest,
    PortalRegistrationEmailCodeResponse,
    PortalRegistrationRequest,
    PortalRegistrationResponse,
    PortalStudentRecord,
    PortalTeamListResponse,
    PortalTeamRecord,
)
from app.schemas.dashboard import DashboardAlert, DashboardOverview, MetricCard
from app.schemas.recruitment import (
    RecruitApplicationImportIssue,
    RecruitApplicationImportResult,
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
    CenterAdvisorMapItem,
    CenterListResponse,
    CenterRecord,
    CenterUpsert,
    RegisteredPortalStudentActionResponse,
    RegisteredPortalStudentEmailRequest,
    RegisteredPortalStudentListResponse,
    RegisteredPortalStudentRecord,
    StudentLifecycleBoard,
    StudentManagementResponse,
    StudentOptionsResponse,
    StudentRecord,
    StudentStateItem,
    StudentStats,
    StudentSummary,
    StudentUpsert,
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
from app.services.email_service import NotificationEmailService
from app.services.postgres_state_store import PostgresStateStore
from app.services.recruitment_excel_service import build_recruitment_template
from app.services.runtime_seed_data import build_runtime_seed_state


PASSWORD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
ListItemT = TypeVar("ListItemT")
logger = logging.getLogger(__name__)
FINAL_WORKFLOW_STATUSES = {"已通过", "已驳回"}
PORTAL_REGISTRATION_EMAIL_CODE_LENGTH = 6
PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS = 10 * 60
PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS = 60
DEFAULT_PORTAL_POLITICAL_STATUS_VALUES = (
    "中共党员",
    "中共预备党员",
    "共青团员",
    "民革党员",
    "民盟盟员",
    "民建会员",
    "民进会员",
    "农工党党员",
    "致公党党员",
    "九三学社社员",
    "台盟盟员",
    "无党派人士",
    "群众",
)
DEFAULT_PORTAL_ETHNIC_GROUP_VALUES = (
    "汉族",
    "蒙古族",
    "回族",
    "藏族",
    "维吾尔族",
    "苗族",
    "彝族",
    "壮族",
    "布依族",
    "朝鲜族",
    "满族",
    "侗族",
    "瑶族",
    "白族",
    "土家族",
    "哈尼族",
    "哈萨克族",
    "傣族",
    "黎族",
    "傈僳族",
    "佤族",
    "畲族",
    "高山族",
    "拉祜族",
    "水族",
    "东乡族",
    "纳西族",
    "景颇族",
    "柯尔克孜族",
    "土族",
    "达斡尔族",
    "仫佬族",
    "羌族",
    "布朗族",
    "撒拉族",
    "毛南族",
    "仡佬族",
    "锡伯族",
    "阿昌族",
    "普米族",
    "塔吉克族",
    "怒族",
    "乌孜别克族",
    "俄罗斯族",
    "鄂温克族",
    "德昂族",
    "保安族",
    "裕固族",
    "京族",
    "塔塔尔族",
    "独龙族",
    "鄂伦春族",
    "赫哲族",
    "门巴族",
    "珞巴族",
    "基诺族",
)
ROLE_DISPLAY_NAMES = {
    "platform_admin": "学合管理员",
    "advisor": "导师",
    "secretary": "学位秘书",
}
WORKFLOW_NAME_INITIALS_MAP = {
    "招生录取审批": "ZSLQSP",
    "科研报告审阅": "KYBGSY",
    "外出研修审批": "WCYXSP",
    "学位申请审批": "SWSQSP",
    "导师变更审批": "DSBGSP",
}
MANAGED_WORKFLOW_DEFINITIONS: dict[str, dict[str, Any]] = {
    "recruitment_application": {
        "workflow_name": "招生录取审批",
        "business_module": "招生管理",
        "business_dataset": "recruitment_applications",
        "business_entity": "报名申请",
        "business_key_prefix": "REC",
        "managed_fields": ("application_status",),
        "initial_field_values": {"application_status": "报名已提交"},
        "nodes": {
            "qualification_review": {
                "label": "资格审核",
                "handler_roles": ["platform_admin"],
                "due_days": 1,
                "actions": {
                    "approve": {
                        "label": "资格通过",
                        "next_node": "qualification_passed",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "资格审核通过"},
                    },
                    "reject": {
                        "label": "审核不通过",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "不录取"},
                    },
                },
            },
            "qualification_passed": {
                "label": "评分准备",
                "handler_roles": ["platform_admin"],
                "due_days": 1,
                "actions": {
                    "start_scoring": {
                        "label": "启动评分",
                        "next_node": "interview_arrangement",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "材料评分中"},
                    },
                    "reject": {
                        "label": "取消申请",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "不录取"},
                    },
                },
            },
            "interview_arrangement": {
                "label": "面试安排",
                "handler_roles": ["platform_admin"],
                "due_days": 2,
                "actions": {
                    "schedule_interview": {
                        "label": "完成面试安排",
                        "next_node": "admission_decision",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "面试待安排"},
                    },
                    "reject": {
                        "label": "终止流程",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "不录取"},
                    },
                },
            },
            "admission_decision": {
                "label": "录取决策",
                "handler_roles": ["platform_admin"],
                "due_days": 2,
                "actions": {
                    "record_interview": {
                        "label": "录入面试结果",
                        "next_node": "admission_confirmation",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "面试完成"},
                    },
                    "reject": {
                        "label": "不录取",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "不录取"},
                    },
                },
            },
            "admission_confirmation": {
                "label": "录取确认",
                "handler_roles": ["platform_admin"],
                "due_days": 2,
                "actions": {
                    "pre_admit": {
                        "label": "预录取",
                        "next_node": None,
                        "task_status": "已通过",
                        "field_updates": {"application_status": "预录取"},
                    },
                    "admit": {
                        "label": "同意录取",
                        "next_node": None,
                        "task_status": "已通过",
                        "field_updates": {"application_status": "同意录取"},
                    },
                    "reject": {
                        "label": "不录取",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "不录取"},
                    },
                },
            },
        },
    },
    "scientific_report": {
        "workflow_name": "科研报告审阅",
        "business_module": "培养管理",
        "business_dataset": "scientific_reports",
        "business_entity": "科研报告",
        "business_key_prefix": "REP",
        "managed_fields": ("report_status",),
        "initial_field_values": {"report_status": "待导师审阅"},
        "nodes": {
            "advisor_review": {
                "label": "导师审阅",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {
                    "approve": {
                        "label": "审阅通过",
                        "next_node": None,
                        "task_status": "已通过",
                        "field_updates": {"report_status": "已通过"},
                    },
                    "request_revision": {
                        "label": "退回修改",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"report_status": "退回修改"},
                    },
                },
            },
        },
    },
    "outbound_study": {
        "workflow_name": "外出研修审批",
        "business_module": "培养管理",
        "business_dataset": "outbound_studies",
        "business_entity": "外出研修",
        "business_key_prefix": "OUT",
        "managed_fields": ("approval_status",),
        "initial_field_values": {"approval_status": "审批中"},
        "nodes": {
            "advisor_review": {
                "label": "导师审核",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {
                    "approve": {
                        "label": "导师同意",
                        "next_node": "office_review",
                        "task_status": "处理中",
                        "field_updates": {"approval_status": "审批中"},
                    },
                    "reject": {
                        "label": "导师驳回",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"approval_status": "已驳回"},
                    },
                },
            },
            "office_review": {
                "label": "学合审核",
                "handler_roles": ["platform_admin"],
                "due_days": 2,
                "actions": {
                    "approve": {
                        "label": "审批通过",
                        "next_node": None,
                        "task_status": "已通过",
                        "field_updates": {"approval_status": "已批准"},
                    },
                    "reject": {
                        "label": "审批驳回",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"approval_status": "已驳回"},
                    },
                },
            },
        },
    },
    "thesis": {
        "workflow_name": "学位申请审批",
        "business_module": "学位管理",
        "business_dataset": "theses",
        "business_entity": "论文主档",
        "business_key_prefix": "DEG",
        "managed_fields": ("thesis_status", "blind_review_status", "degree_status"),
        "initial_field_values": {
            "thesis_status": "待查重",
            "blind_review_status": "未送审",
            "degree_status": "待申请",
        },
        "nodes": {
            "advisor_precheck": {
                "label": "导师预审",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {
                    "submit_review": {
                        "label": "提交送审",
                        "next_node": "secretary_review",
                        "task_status": "处理中",
                        "field_updates": {
                            "thesis_status": "查重通过",
                            "blind_review_status": "进行中",
                            "degree_status": "授位审批中",
                        },
                    },
                    "request_revision": {
                        "label": "退回修改",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {
                            "thesis_status": "退回修改",
                            "blind_review_status": "未通过",
                            "degree_status": "未授位",
                        },
                    },
                },
            },
            "secretary_review": {
                "label": "材料复核",
                "handler_roles": ["secretary"],
                "due_days": 2,
                "actions": {
                    "approve": {
                        "label": "复核通过",
                        "next_node": None,
                        "task_status": "已通过",
                        "field_updates": {
                            "thesis_status": "盲审通过",
                            "blind_review_status": "已通过",
                            "degree_status": "待正式答辩",
                        },
                    },
                    "reject": {
                        "label": "复核驳回",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {
                            "thesis_status": "退回修改",
                            "blind_review_status": "未通过",
                            "degree_status": "未授位",
                        },
                    },
                },
            },
        },
    },
}
WORKFLOW_DATASET_TO_FLOW = {
    definition["business_dataset"]: flow_code for flow_code, definition in MANAGED_WORKFLOW_DEFINITIONS.items()
}
DEFAULT_USER_PASSWORD = "ChangeMe@123"
DEFAULT_PASSWORD_BY_USERNAME = {
    "admin": "Admin@123456",
    "liu.ya": "LiuYa@2026",
    "yuan.ye": "YuanYe@2026",
    "xu.sutian": "XuSutian@2026",
    "zhou.qing": "ZhouQing@2026",
    "he.lin": "HeLin@2026",
    "cao.bo": "CaoBo@2026",
    "yang.qin": "YangQin@2026",
    "sun.wei": "SunWei@2026",
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


class RuntimeManagementStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._postgres_store = PostgresStateStore()
        self._email_service = NotificationEmailService()
        self.state = self._load_state()
        self._counters = self.state.setdefault("counters", {})
        self._migrate_state()

    def _load_state(self) -> dict[str, Any]:
        postgres_state = self._postgres_store.load_state()
        if postgres_state:
            return postgres_state
        return build_runtime_seed_state()

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
        postgres_teams = self._load_teams_from_postgres()
        if postgres_teams:
            state_team_ids = {int(item.get("id", 0)) for item in self.state.setdefault("teams", [])}
            postgres_team_ids = {int(item.get("id", 0)) for item in postgres_teams}
            if state_team_ids != postgres_team_ids:
                self.state["teams"] = postgres_teams
                changed = True
        self._counters.setdefault("teams", max([item.get("id", 0) for item in self.state.setdefault("teams", [])], default=0))
        self.state.setdefault("portal_students", [])
        self._counters.setdefault("portal_students", max([item.get("id", 0) for item in self.state["portal_students"]], default=0))
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

    def _load_teams_from_postgres(self) -> list[dict[str, Any]]:
        try:
            return self._postgres_store.load_team_state()
        except Exception as exc:
            logger.warning("Load teams from PostgreSQL failed, fallback to current runtime state: %s", exc)
            return []

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

    def _record_operation(self, module_name: str, entity_name: str, entity_id: str, action: str, summary: str, operator_username: str = "admin") -> dict[str, Any]:
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

    def _build_center_record(self, item: dict[str, Any]) -> CenterRecord:
        members = [student for student in self._list("students") if student.get("team_name") == item["team_name"]]
        active_statuses = {"在校", "实习中", "外出研修", "请假中", "学位论文阶段"}
        return CenterRecord(
            id=item["id"],
            center_name=item["team_name"],
            director_name=item["lead_advisor_name"],
            advisor_names=self._normalize_name_list(item.get("advisor_names", []), item.get("lead_advisor_name")),
            is_enabled=item.get("status") == "启用",
            created_date=item.get("created_on") or item.get("established_on"),
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
        team = self._ensure_team_exists(payload.center_name)
        team_advisors = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
        if payload.advisor_name not in team_advisors:
            raise ValueError("Selected advisor does not belong to the selected center")

    def _validate_center_payload(self, payload: CenterUpsert, current_center_id: int | None = None) -> dict[str, Any]:
        for item in self._list("teams"):
            if item["team_name"] == payload.center_name and item["id"] != current_center_id:
                raise ValueError("Center name already exists")
        advisor_names = self._normalize_name_list(payload.advisor_names, payload.director_name)
        if not advisor_names:
            raise ValueError("Center must contain at least one advisor")
        return {
            "team_name": payload.center_name,
            "lead_advisor_name": payload.director_name,
            "advisor_names": advisor_names,
            "status": "启用" if payload.is_enabled else "停用",
            "created_on": payload.created_date or datetime.now().strftime("%Y-%m-%d"),
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

    def get_portal_profile_options(self) -> PortalProfileOptionsResponse:
        political_status_options = self._dict_options("student_political_status")
        ethnic_group_options = self._dict_options("student_ethnic_group")
        if not political_status_options:
            political_status_options = self._select_options_from_values(DEFAULT_PORTAL_POLITICAL_STATUS_VALUES)
        if not ethnic_group_options:
            ethnic_group_options = self._select_options_from_values(DEFAULT_PORTAL_ETHNIC_GROUP_VALUES)
        return PortalProfileOptionsResponse(
            political_status_options=political_status_options,
            ethnic_group_options=ethnic_group_options,
        )

    def _workflow_definition(self, flow_code: str) -> dict[str, Any]:
        definition = MANAGED_WORKFLOW_DEFINITIONS.get(flow_code)
        if not definition:
            raise ValueError(f"Unsupported workflow flow: {flow_code}")
        return definition

    def _workflow_name_code(self, workflow_name: str) -> str:
        normalized = str(workflow_name or "").strip()
        if normalized in WORKFLOW_NAME_INITIALS_MAP:
            return WORKFLOW_NAME_INITIALS_MAP[normalized]
        ascii_code = "".join(char for char in normalized.upper() if "A" <= char <= "Z")
        if ascii_code:
            return ascii_code
        return "YWLC"

    @staticmethod
    def _workflow_id_slug(value: str | None, max_length: int) -> str:
        normalized = "".join(character.lower() for character in str(value or "") if character.isalnum())
        if not normalized:
            normalized = "x"
        return normalized[:max_length]

    @staticmethod
    def _workflow_id_hash(*parts: Any, length: int = 10) -> str:
        raw_value = "::".join(str(part or "") for part in parts)
        return hashlib.sha1(raw_value.encode("utf-8")).hexdigest()[:length]

    def _workflow_business_key_date(self, created_at: str | None = None) -> str:
        text = str(created_at or "").strip()
        if len(text) >= 10:
            date_part = text[:10].replace("-", "")
            if len(date_part) == 8 and date_part.isdigit():
                return date_part
        return datetime.now().strftime("%Y%m%d")

    def _next_workflow_business_sequence(self, workflow_code: str, business_date: str) -> int:
        cache_key = build_cache_key("workflow", "business-key", workflow_code, business_date)
        try:
            client = get_cache_client()
            sequence = int(client.incr(cache_key))
            if sequence == 1:
                client.expire(cache_key, 3 * 24 * 60 * 60)
            return sequence
        except Exception:
            fallback_key = f'workflow_business_key:{workflow_code}:{business_date}'
            self._counters[fallback_key] = int(self._counters.get(fallback_key, 0)) + 1
            return int(self._counters[fallback_key])

    def _workflow_business_key_exists(self, business_key: str) -> bool:
        for task in self._list("workflow_tasks"):
            if str(task.get("business_key") or "") == business_key:
                return True
        for definition in MANAGED_WORKFLOW_DEFINITIONS.values():
            for item in self._list(definition["business_dataset"]):
                if str(item.get("business_key") or item.get("candidate_no") or "") == business_key:
                    return True
        return False

    def _generate_workflow_business_key(self, workflow_name: str, created_at: str | None = None) -> str:
        workflow_code = self._workflow_name_code(workflow_name)
        business_date = self._workflow_business_key_date(created_at)
        while True:
            sequence = self._next_workflow_business_sequence(workflow_code, business_date)
            business_key = f"{workflow_code}{business_date}{sequence:04d}"
            if not self._workflow_business_key_exists(business_key):
                return business_key

    @staticmethod
    def _portal_registration_email_cache_token(email: str) -> str:
        normalized = str(email or "").strip().lower()
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:24]

    def _portal_registration_email_code_key(self, email: str) -> str:
        return build_cache_key("portal", "register", "email-code", self._portal_registration_email_cache_token(email))

    def _portal_registration_email_cooldown_key(self, email: str) -> str:
        return build_cache_key("portal", "register", "email-cooldown", self._portal_registration_email_cache_token(email))

    def send_portal_registration_email_code(self, email: str) -> PortalRegistrationEmailCodeResponse:
        normalized_email = str(email or "").strip()
        with self._lock:
            if any(item.get("email") == normalized_email for item in self._list("portal_students")):
                raise ValueError("该邮箱已注册，请直接登录")

        if not self._email_service.enabled():
            raise RuntimeError("邮件服务未启用，暂无法发送邮箱验证码")

        try:
            client = get_cache_client()
            cooldown_key = self._portal_registration_email_cooldown_key(normalized_email)
            if client.exists(cooldown_key):
                remaining_seconds = int(client.ttl(cooldown_key) or 0)
                if remaining_seconds <= 0:
                    remaining_seconds = PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS
                raise ValueError(f"验证码已发送，请{remaining_seconds}秒后重试")

            verification_code = "".join(
                secrets.choice(string.digits) for _ in range(PORTAL_REGISTRATION_EMAIL_CODE_LENGTH)
            )
            client.set(
                self._portal_registration_email_code_key(normalized_email),
                verification_code,
                ex=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            )
            client.set(cooldown_key, "1", ex=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS)
        except ValueError:
            raise
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        self._email_service.send_portal_registration_verification_code(normalized_email, verification_code)
        return PortalRegistrationEmailCodeResponse(
            message="邮件验证码已发送，请查收邮箱",
            expires_in_seconds=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            cooldown_seconds=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS,
        )

    def validate_portal_registration_email_code(self, email: str, verification_code: str) -> None:
        normalized_email = str(email or "").strip()
        normalized_code = str(verification_code or "").strip()
        try:
            client = get_cache_client()
            cached_code = client.get(self._portal_registration_email_code_key(normalized_email))
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        if not isinstance(cached_code, (str, bytes, bytearray)):
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if isinstance(cached_code, (bytes, bytearray)):
            cached_text = cached_code.decode("utf-8", errors="ignore").strip()
        else:
            cached_text = cached_code.strip()
        if not cached_text:
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if cached_text != normalized_code:
            raise ValueError("邮件验证码不正确")

    def clear_portal_registration_email_code(self, email: str) -> None:
        normalized_email = str(email or "").strip()
        try:
            client = get_cache_client()
            client.delete(
                self._portal_registration_email_code_key(normalized_email),
                self._portal_registration_email_cooldown_key(normalized_email),
            )
        except Exception as exc:
            logger.warning("Clear portal registration email code failed: %s", exc)

    def _workflow_business_key(self, flow_code: str, entity_id: int, existing_key: str | None = None, created_at: str | None = None) -> str:
        if existing_key:
            return str(existing_key)
        del entity_id
        definition = self._workflow_definition(flow_code)
        return self._generate_workflow_business_key(definition["workflow_name"], created_at=created_at)

    def _workflow_process_definition_key(self, flow_code: str | None, workflow_name: str | None) -> str:
        normalized_flow_code = str(flow_code or "").strip()
        if normalized_flow_code:
            return normalized_flow_code.lower()
        return self._workflow_name_code(str(workflow_name or "未命名流程")).lower()

    @staticmethod
    def _workflow_deployment_id(process_definition_key: str) -> str:
        return (
            f"dep-{RuntimeManagementStore._workflow_id_slug(process_definition_key, 24)}-"
            f"{RuntimeManagementStore._workflow_id_hash(process_definition_key, 'deployment', length=8)}"
        )

    @staticmethod
    def _workflow_process_definition_id(process_definition_key: str) -> str:
        return (
            f"procdef-{RuntimeManagementStore._workflow_id_slug(process_definition_key, 20)}-v1-"
            f"{RuntimeManagementStore._workflow_id_hash(process_definition_key, 'process-definition', length=8)}"
        )

    @staticmethod
    def _workflow_process_instance_id(process_definition_key: str, business_key: str) -> str:
        return (
            f"procinst-{RuntimeManagementStore._workflow_id_slug(process_definition_key, 16)}-"
            f"{RuntimeManagementStore._workflow_id_slug(business_key, 18)}-"
            f"{RuntimeManagementStore._workflow_id_hash(process_definition_key, business_key, 'process-instance', length=10)}"
        )

    @staticmethod
    def _workflow_task_definition_key(node_key: str | None, current_node: str | None) -> str:
        normalized_node_key = str(node_key or "").strip()
        if normalized_node_key:
            return normalized_node_key
        normalized_node = str(current_node or "").strip()
        return normalized_node or "manual_task"

    @staticmethod
    def _workflow_execution_id(process_instance_id: str, task_definition_key: str) -> str:
        return (
            f"exec-{RuntimeManagementStore._workflow_id_slug(task_definition_key, 18)}-"
            f"{RuntimeManagementStore._workflow_id_hash(process_instance_id, task_definition_key, 'execution', length=10)}"
        )

    def _workflow_candidate_groups(self, flow_code: str | None, node_key: str | None) -> list[str]:
        normalized_flow_code = str(flow_code or "").strip()
        normalized_node_key = str(node_key or "").strip()
        if not normalized_flow_code or not normalized_node_key:
            return []
        node = self._workflow_definition(normalized_flow_code)["nodes"].get(normalized_node_key)
        if not node:
            return []
        return [str(role) for role in node.get("handler_roles", []) if str(role).strip()]

    def _ensure_workflow_engine_metadata(self, task: dict[str, Any]) -> bool:
        process_definition_key = self._workflow_process_definition_key(task.get("flow_code"), task.get("workflow_name"))
        task_definition_key = self._workflow_task_definition_key(task.get("node_key"), task.get("current_node"))
        business_key = str(task.get("business_key") or "")
        process_instance_id = self._workflow_process_instance_id(process_definition_key, business_key or f'TASK-{task.get("id") or "0"}')
        execution_id = self._workflow_execution_id(process_instance_id, task_definition_key)
        metadata_updates = {
            "deployment_id": task.get("deployment_id") or self._workflow_deployment_id(process_definition_key),
            "process_definition_key": process_definition_key,
            "process_definition_id": task.get("process_definition_id") or self._workflow_process_definition_id(process_definition_key),
            "process_definition_version": int(task.get("process_definition_version") or 1),
            "process_instance_id": process_instance_id,
            "execution_id": execution_id,
            "task_definition_key": task_definition_key,
            "candidate_groups": self._workflow_candidate_groups(task.get("flow_code"), task.get("node_key")),
        }
        changed = False
        for key, value in metadata_updates.items():
            if task.get(key) != value:
                task[key] = value
                changed = True
        return changed

    def _workflow_task_index_by_entity(self, flow_code: str, entity_id: int) -> tuple[int, dict[str, Any]] | None:
        for index, item in enumerate(self._list("workflow_tasks")):
            if item.get("flow_code") == flow_code and int(item.get("entity_id") or 0) == entity_id:
                return index, item
        return None

    def _ensure_managed_business_key(self, flow_code: str, item: dict[str, Any], existing_key: str | None = None, created_at: str | None = None) -> tuple[str, bool]:
        candidate_key = existing_key or item.get("business_key")
        if not candidate_key and flow_code == "recruitment_application":
            candidate_key = item.get("candidate_no")
        business_key = self._workflow_business_key(
            flow_code,
            int(item.get("id") or 0),
            existing_key=str(candidate_key) if candidate_key else None,
            created_at=created_at,
        )
        changed = False
        if item.get("business_key") != business_key:
            item["business_key"] = business_key
            changed = True
        if flow_code == "recruitment_application" and item.get("candidate_no") != business_key:
            item["candidate_no"] = business_key
            changed = True
        return business_key, changed

    def _workflow_initial_node_key(self, flow_code: str) -> str:
        return next(iter(self._workflow_definition(flow_code)["nodes"]))

    def _workflow_due_at(self, flow_code: str, node_key: str) -> str:
        definition = self._workflow_definition(flow_code)
        due_days = int(definition["nodes"][node_key].get("due_days", 2))
        return (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d %H:%M:%S")

    def _workflow_handler_display(self, flow_code: str, node_key: str, item: dict[str, Any]) -> str:
        roles = self._workflow_definition(flow_code)["nodes"][node_key]["handler_roles"]
        if roles == ["advisor"] and item.get("advisor_name"):
            return str(item["advisor_name"])
        return " / ".join(ROLE_DISPLAY_NAMES.get(role, role) for role in roles)

    def _workflow_title(self, flow_code: str, item: dict[str, Any]) -> str:
        if flow_code == "recruitment_application":
            return f'{item["student_name"]}报名审核'
        if flow_code == "scientific_report":
            return f'{item["student_name"]}科研报告审阅'
        if flow_code == "outbound_study":
            return f'{item["student_name"]}外出研修申请'
        if flow_code == "thesis":
            return f'{item["student_name"]}授位审批'
        return str(item.get("student_name") or item.get("title") or "流程任务")

    def _workflow_form_summary(self, flow_code: str, item: dict[str, Any]) -> str:
        if flow_code == "recruitment_application":
            return f'业务编号：{item.get("business_key") or item.get("candidate_no") or "-"}；研究方向：{item["intended_field"]}；材料状态：{item["material_status"]}'
        if flow_code == "scientific_report":
            reviewer_name = item.get("reviewer_name") or "待分配"
            return f'周期：{item["period_label"]}；审阅人：{reviewer_name}'
        if flow_code == "outbound_study":
            return f'研修地点：{item["destination"]}；起止：{item["start_date"]} 至 {item["end_date"]}'
        if flow_code == "thesis":
            return f'论文题目：{item["title"]}；盲审状态：{item["blind_review_status"]}'
        return str(item.get("title") or item.get("student_name") or "")

    def _workflow_applicant_name(self, flow_code: str, item: dict[str, Any]) -> str:
        del flow_code
        return str(item.get("student_name") or item.get("full_name") or item.get("business_key") or item.get("candidate_no") or "未知申请人")

    def _principal_summary(self, principal: Any) -> dict[str, Any]:
        if hasattr(principal, "model_dump"):
            payload = principal.model_dump()
        elif isinstance(principal, dict):
            payload = principal
        else:
            payload = {
                "username": getattr(principal, "username", "system"),
                "full_name": getattr(principal, "full_name", getattr(principal, "username", "system")),
                "roles": list(getattr(principal, "roles", [])),
            }
        return {
            "username": payload.get("username", "system"),
            "full_name": payload.get("full_name", payload.get("username", "system")),
            "roles": list(payload.get("roles", [])),
        }

    def _workflow_action_options(self, task: dict[str, Any], principal_roles: list[str] | None = None) -> list[dict[str, str]]:
        flow_code = task.get("flow_code")
        node_key = task.get("node_key")
        if not flow_code or not node_key:
            return []
        node = self._workflow_definition(flow_code)["nodes"].get(node_key)
        if not node:
            return []
        if principal_roles and not set(node["handler_roles"]).intersection(principal_roles):
            return []
        return [{"action": action_code, "label": action_config["label"]} for action_code, action_config in node["actions"].items()]

    def _fallback_workflow_due_at(self, task: dict[str, Any]) -> str:
        due_at = task.get("due_at")
        if due_at:
            return str(due_at)
        created_at = str(task.get("created_at") or "").strip()
        if created_at:
            return created_at
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _build_workflow_task_record(self, task: dict[str, Any], principal_roles: list[str] | None = None) -> WorkflowTaskRecord:
        return WorkflowTaskRecord(
            id=int(task["id"]),
            workflow_name=str(task.get("workflow_name") or "未命名流程"),
            business_module=str(task.get("business_module") or "流程中心"),
            business_key=str(task.get("business_key") or f'TASK-{task["id"]}'),
            title=str(task.get("title") or "未命名任务"),
            applicant_name=str(task.get("applicant_name") or "未知申请人"),
            current_handler=str(task.get("current_handler") or "待分派"),
            current_node=str(task.get("current_node") or "待处理"),
            priority=str(task.get("priority") or "中"),
            status=str(task.get("status") or "待处理"),
            created_at=str(task.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            due_at=self._fallback_workflow_due_at(task),
            form_summary=str(task.get("form_summary") or ""),
            latest_comment=task.get("latest_comment"),
            available_actions=self._workflow_action_options(task, principal_roles=principal_roles),
            process_definition_key=task.get("process_definition_key"),
            process_definition_id=task.get("process_definition_id"),
            process_instance_id=task.get("process_instance_id"),
            execution_id=task.get("execution_id"),
            task_definition_key=task.get("task_definition_key"),
        )

    def _build_workflow_history_record(self, entry: dict[str, Any]) -> dict[str, Any]:
        return {
            "operated_at": entry["operated_at"],
            "operator_username": entry["operator_username"],
            "operator_full_name": entry["operator_full_name"],
            "action": entry["action"],
            "action_label": entry["action_label"],
            "from_node": entry["from_node"],
            "to_node": entry.get("to_node"),
            "result_status": entry["result_status"],
            "comment": entry.get("comment"),
        }

    def _workflow_task_index_by_business_key(self, business_key: str) -> tuple[int, dict[str, Any]] | None:
        for index, item in enumerate(self._list("workflow_tasks")):
            if item.get("business_key") == business_key:
                return index, item
        return None

    def _normalize_legacy_workflow_tasks(self) -> bool:
        changed = False
        for index, task in enumerate(self._list("workflow_tasks")):
            updated = dict(task)
            row_changed = False
            defaults = {
                "workflow_name": updated.get("workflow_name") or "未命名流程",
                "business_module": updated.get("business_module") or "流程中心",
                "business_key": updated.get("business_key") or self._generate_workflow_business_key(
                    str(updated.get("workflow_name") or "未命名流程"),
                    created_at=str(updated.get("created_at") or ""),
                ),
                "title": updated.get("title") or "未命名任务",
                "applicant_name": updated.get("applicant_name") or "未知申请人",
                "current_handler": updated.get("current_handler") or "待分派",
                "current_node": updated.get("current_node") or "待处理",
                "priority": updated.get("priority") or "中",
                "status": updated.get("status") or "待处理",
                "created_at": updated.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "due_at": self._fallback_workflow_due_at(updated),
                "form_summary": updated.get("form_summary") or "",
                "history": updated.get("history") or [],
            }
            for key, value in defaults.items():
                if updated.get(key) != value:
                    updated[key] = value
                    row_changed = True
            if self._ensure_workflow_engine_metadata(updated):
                row_changed = True
            if row_changed:
                self._list("workflow_tasks")[index] = updated
                changed = True
        return changed

    def _workflow_initial_item(self, flow_code: str, item: dict[str, Any]) -> dict[str, Any]:
        definition = self._workflow_definition(flow_code)
        initial_item = {**item, **definition.get("initial_field_values", {})}
        self._ensure_managed_business_key(flow_code, initial_item)
        return initial_item

    def _ensure_managed_status_fields_unchanged(self, dataset: str, current: dict[str, Any], incoming: dict[str, Any]) -> None:
        flow_code = WORKFLOW_DATASET_TO_FLOW.get(dataset)
        if not flow_code:
            return
        definition = self._workflow_definition(flow_code)
        changed_fields = [field for field in definition["managed_fields"] if current.get(field) != incoming.get(field)]
        if changed_fields:
            raise ValueError(f'字段 {", ".join(changed_fields)} 为流程托管状态，请通过审批流程活动变更')

    def _infer_workflow_runtime(self, flow_code: str, item: dict[str, Any]) -> dict[str, Any]:
        if flow_code == "recruitment_application":
            mapping = {
                "报名已提交": ("qualification_review", "待处理"),
                "资格审核通过": ("qualification_passed", "处理中"),
                "材料评分中": ("interview_arrangement", "处理中"),
                "面试待安排": ("admission_decision", "处理中"),
                "面试完成": ("admission_confirmation", "处理中"),
                "预录取": (None, "已通过"),
                "同意录取": (None, "已通过"),
                "不录取": (None, "已驳回"),
            }
            node_key, task_status = mapping.get(item.get("application_status"), ("qualification_review", "待处理"))
            return {"node_key": node_key, "task_status": task_status}
        if flow_code == "scientific_report":
            if item.get("report_status") == "已通过":
                return {"node_key": None, "task_status": "已通过"}
            if item.get("report_status") == "退回修改":
                return {"node_key": None, "task_status": "已驳回"}
            return {"node_key": "advisor_review", "task_status": "待处理"}
        if flow_code == "outbound_study":
            if item.get("approval_status") in {"已批准", "研修中", "已结束"}:
                return {"node_key": None, "task_status": "已通过"}
            if item.get("approval_status") == "已驳回":
                return {"node_key": None, "task_status": "已驳回"}
            return {"node_key": "advisor_review", "task_status": "待处理"}
        if flow_code == "thesis":
            if item.get("degree_status") == "待正式答辩" or item.get("blind_review_status") == "已通过":
                return {"node_key": None, "task_status": "已通过"}
            if item.get("degree_status") == "未授位" or item.get("blind_review_status") == "未通过" or item.get("thesis_status") == "退回修改":
                return {"node_key": None, "task_status": "已驳回"}
            if item.get("degree_status") == "授位审批中" or item.get("blind_review_status") == "进行中":
                return {"node_key": "secretary_review", "task_status": "处理中"}
            return {"node_key": "advisor_precheck", "task_status": "待处理"}
        raise ValueError(f"Unsupported workflow flow: {flow_code}")

    def _sync_managed_workflow_task(self, flow_code: str, item: dict[str, Any], existing_task: dict[str, Any] | None = None) -> tuple[dict[str, Any], bool]:
        definition = self._workflow_definition(flow_code)
        runtime = self._infer_workflow_runtime(flow_code, item)
        node_key = runtime["node_key"]
        task_status = runtime["task_status"]
        task = dict(existing_task or {})
        changed = False
        if not existing_task:
            task["id"] = self._next_id("workflow_tasks")
            task["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["history"] = []
            changed = True
        if "history" not in task:
            task["history"] = []
            changed = True
        item_business_key, item_key_changed = self._ensure_managed_business_key(
            flow_code,
            item,
            existing_key=task.get("business_key"),
            created_at=str(task.get("created_at") or ""),
        )
        if item_key_changed:
            changed = True
        task_updates = {
            "workflow_name": definition["workflow_name"],
            "business_module": definition["business_module"],
            "business_key": item_business_key,
            "title": self._workflow_title(flow_code, item),
            "applicant_name": self._workflow_applicant_name(flow_code, item),
            "priority": task.get("priority") or "中",
            "status": task_status,
            "current_node": definition["nodes"][node_key]["label"] if node_key else "流程结束",
            "current_handler": self._workflow_handler_display(flow_code, node_key, item) if node_key else "流程结束",
            "due_at": task.get("due_at") if not node_key else task.get("due_at") or self._workflow_due_at(flow_code, node_key),
            "form_summary": self._workflow_form_summary(flow_code, item),
            "latest_comment": task.get("latest_comment"),
            "flow_code": flow_code,
            "business_dataset": definition["business_dataset"],
            "entity_id": int(item["id"]),
            "node_key": node_key,
        }
        for key, value in task_updates.items():
            if task.get(key) != value:
                task[key] = value
                changed = True
        if self._ensure_workflow_engine_metadata(task):
            changed = True
        return task, changed

    def _migrate_workflow_runtime(self) -> bool:
        changed = False
        for flow_code, definition in MANAGED_WORKFLOW_DEFINITIONS.items():
            for item in self._list(definition["business_dataset"]):
                existing_business_key = str(item.get("business_key") or item.get("candidate_no") or "").strip() or None
                if existing_business_key:
                    _, item_changed = self._ensure_managed_business_key(flow_code, item, existing_key=existing_business_key)
                    if item_changed:
                        changed = True
                located = None
                if item.get("business_key"):
                    located = self._workflow_task_index_by_business_key(str(item["business_key"]))
                if located is None:
                    located = self._workflow_task_index_by_entity(flow_code, int(item["id"]))
                existing_task = located[1] if located else None
                task, task_changed = self._sync_managed_workflow_task(flow_code, item, existing_task=existing_task)
                if located is None:
                    self._list("workflow_tasks").insert(0, task)
                    changed = True
                elif task_changed:
                    self._list("workflow_tasks")[located[0]] = task
                    changed = True
        return changed

    def _start_managed_workflow(self, flow_code: str, item: dict[str, Any], operator_username: str) -> None:
        task, _ = self._sync_managed_workflow_task(flow_code, item)
        task["latest_comment"] = "流程已发起，等待节点处理。"
        task["history"] = [
            {
                "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator_username": operator_username,
                "operator_full_name": operator_username,
                "action": "start",
                "action_label": "发起流程",
                "from_node": "开始",
                "to_node": task["current_node"],
                "result_status": task["status"],
                "comment": task["latest_comment"],
            }
        ]
        self._list("workflow_tasks").insert(0, task)

    def _update_runtime_managed_entity(self, dataset_name: str, entity_id: int, payload: dict[str, Any]) -> None:
        if dataset_name == "recruitment_applications":
            self._postgres_store.update_runtime_recruitment_application(entity_id, payload)
            return
        if dataset_name == "scientific_reports":
            self._postgres_store.update_runtime_scientific_report(entity_id, payload)
            return
        if dataset_name == "outbound_studies":
            self._postgres_store.update_runtime_outbound_study(entity_id, payload)
            return
        if dataset_name == "theses":
            self._postgres_store.update_runtime_thesis(entity_id, payload)
            return
        raise ValueError(f"Unsupported managed dataset: {dataset_name}")

    def _persist_portal_student_change(
        self,
        student: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        update_student_counter: bool = False,
    ) -> None:
        self._postgres_store.update_runtime_portal_student(int(student["id"]), student)
        if update_student_counter:
            self._postgres_store.update_runtime_counter("portal_students", int(self._counters.get("portal_students", 0)))
        self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
        self._postgres_store.insert_runtime_operation_log(operation_log)

    def _persist_portal_application_submission(
        self,
        student: dict[str, Any],
        application: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        workflow_task: dict[str, Any] | None = None,
        created_application: bool = False,
        created_workflow_task: bool = False,
    ) -> None:
        counters = {"operation_logs": int(self._counters.get("operation_logs", 0))}
        if created_application:
            counters["recruitment_applications"] = int(self._counters.get("recruitment_applications", 0))
        if created_workflow_task:
            counters["workflow_tasks"] = int(self._counters.get("workflow_tasks", 0))
        self._postgres_store.sync_portal_application_submission(
            student,
            application,
            operation_log,
            workflow_task=workflow_task,
            counters=counters,
        )

    def _persist_student_change(
        self,
        student: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        created: bool = False,
    ) -> None:
        counters = {
            "students": int(self._counters.get("students", 0)),
            "operation_logs": int(self._counters.get("operation_logs", 0)),
        }
        if created:
            self._postgres_store.sync_created_student(student, operation_log=operation_log, counters=counters)
            return
        self._postgres_store.sync_updated_student(student, operation_log=operation_log, counters=counters)

    def _persist_recruitment_application_change(
        self,
        application: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        workflow_task: dict[str, Any] | None = None,
        portal_student: dict[str, Any] | None = None,
        update_application_counter: bool = False,
        update_workflow_counter: bool = False,
    ) -> None:
        del application, operation_log, workflow_task, portal_student, update_application_counter, update_workflow_counter
        # Recruitment application edits affect both the formal relational tables
        # and the runtime mirror. Persist the full state so refreshes read back the
        # same data that was just saved.
        self._save()

    def get_workflow_task_detail(self, task_id: int, principal: Any) -> dict[str, Any]:
        principal_summary = self._principal_summary(principal)
        _, task = self._find_required("workflow_tasks", task_id)
        return {
            "task": self._build_workflow_task_record(task, principal_roles=principal_summary["roles"]),
            "history": [self._build_workflow_history_record(item) for item in task.get("history", [])],
        }

    def execute_workflow_action(self, task_id: int, action: str, comment: str | None, principal: Any) -> dict[str, Any]:
        principal_summary = self._principal_summary(principal)
        notification_payload: dict[str, str] | None = None
        with self._lock:
            index, task = self._find_required("workflow_tasks", task_id)
            flow_code = task.get("flow_code")
            node_key = task.get("node_key")
            if not flow_code or not node_key:
                raise ValueError("当前任务不是流程驱动任务，不能执行流程动作")
            definition = self._workflow_definition(flow_code)
            node = definition["nodes"][node_key]
            if not set(node["handler_roles"]).intersection(principal_summary["roles"]):
                raise PermissionError("当前角色无权执行该流程活动")
            action_definition = node["actions"].get(action)
            if not action_definition:
                raise ValueError("当前节点不支持该流程动作")
            entity_index, entity = self._find_required(definition["business_dataset"], int(task["entity_id"]))
            updated_entity = {**entity, **action_definition.get("field_updates", {})}
            self._list(definition["business_dataset"])[entity_index] = updated_entity

            next_node = action_definition.get("next_node")
            updated_task = dict(task)
            updated_task["status"] = action_definition["task_status"]
            updated_task["latest_comment"] = comment or action_definition["label"]
            updated_task["form_summary"] = self._workflow_form_summary(flow_code, updated_entity)
            updated_task["node_key"] = next_node
            updated_task["current_node"] = definition["nodes"][next_node]["label"] if next_node else "流程结束"
            updated_task["current_handler"] = self._workflow_handler_display(flow_code, next_node, updated_entity) if next_node else "流程结束"
            updated_task["due_at"] = self._workflow_due_at(flow_code, next_node) if next_node else updated_task["due_at"]
            updated_task.setdefault("history", []).append(
                {
                    "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "operator_username": principal_summary["username"],
                    "operator_full_name": principal_summary["full_name"],
                    "action": action,
                    "action_label": action_definition["label"],
                    "from_node": node["label"],
                    "to_node": definition["nodes"][next_node]["label"] if next_node else "流程结束",
                    "result_status": updated_task["status"],
                    "comment": updated_task["latest_comment"],
                }
            )
            self._ensure_workflow_engine_metadata(updated_task)
            self._list("workflow_tasks")[index] = updated_task
            operation_log = self._record_operation(
                "流程中心",
                definition["business_entity"],
                task["business_key"],
                action_definition["label"],
                f'{principal_summary["full_name"]} 执行 {definition["workflow_name"]} - {action_definition["label"]}',
                operator_username=principal_summary["username"],
            )
            try:
                self._update_runtime_managed_entity(definition["business_dataset"], int(task["entity_id"]), updated_entity)
                self._postgres_store.update_runtime_workflow_task(int(updated_task["id"]), updated_task)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            if flow_code == "recruitment_application":
                notification_payload = self._build_recruitment_email_notification(updated_entity)
            result = {
                "task": self._build_workflow_task_record(updated_task, principal_roles=principal_summary["roles"]),
                "history": [self._build_workflow_history_record(item) for item in updated_task.get("history", [])],
            }

        if notification_payload is not None and self._email_service.enabled():
            self._email_service.send_recruitment_status_update(**notification_payload)
        return result

    def _build_recruitment_email_notification(self, application: dict[str, Any]) -> dict[str, str] | None:
        status = str(application.get("application_status") or "").strip()
        if status not in {"资格审核通过", "预录取", "同意录取"}:
            return None

        email = str(application.get("email") or "").strip()
        if not email:
            return None

        plan_name = ""
        plan_id = application.get("plan_id")
        if plan_id is not None:
            matched_plan = next((item for item in self._list("recruitment_plans") if int(item.get("id") or 0) == int(plan_id)), None)
            if matched_plan is not None:
                plan_name = str(matched_plan.get("plan_name") or "")

        return {
            "student_name": str(application.get("student_name") or "同学"),
            "email": email,
            "business_key": str(application.get("business_key") or ""),
            "application_status": status,
            "plan_name": plan_name,
        }

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
        centers = [self._build_center_record(item) for item in self._list("teams")]
        advisor_values = self._advisor_name_values()
        political_values = {
            *self._dict_option_values("student_political_status"),
            *[item.get("political_status") for item in self._list("students") if item.get("political_status")],
        }
        return StudentOptionsResponse(
            status_options=self._dict_options("student_status"),
            degree_options=self._dict_options("student_degree_type"),
            advisor_options=[SelectOption(label=item, value=item) for item in advisor_values],
            center_options=[SelectOption(label=item.center_name, value=item.center_name) for item in centers if item.is_enabled],
            political_status_options=self._select_options_from_values(political_values),
            center_advisor_map=[
                CenterAdvisorMapItem(
                    center_name=item.center_name,
                    advisors=[SelectOption(label=advisor, value=advisor) for advisor in item.advisor_names],
                )
                for item in centers
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
                    updated_user = {**item, "last_login_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    self._list("system_users")[index] = updated_user
                    self._postgres_store.update_runtime_system_user(int(updated_user["id"]), updated_user)
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
            application_count=application_count,
            brochure_image_url=item.get("brochure_image_url"),
            plan_description=item.get("plan_description"),
        )

    @staticmethod
    def _portal_plan_sort_key(item: dict[str, Any]) -> tuple[int, int, int]:
        year_text = str(item.get("academic_year") or "").strip()
        try:
            academic_year = int(year_text)
        except ValueError:
            academic_year = 0
        semester_order = {"春": 1, "夏": 2, "秋": 3, "冬": 4}.get(str(item.get("semester") or "").strip(), 0)
        return academic_year, semester_order, int(item.get("id") or 0)

    def _build_portal_student_record(self, item: dict[str, Any]) -> PortalStudentRecord:
        normalized = dict(item)
        normalized["account_status"] = self._normalize_portal_account_status(normalized.get("account_status"))
        if not normalized.get("business_key") and not normalized.get("candidate_no"):
            student_id = normalized.get("id")
            selected_plan_id = normalized.get("selected_plan_id")
            applications = [
                application for application in self._list("recruitment_applications")
                if int(application.get("portal_student_id") or 0) == int(student_id or 0)
            ]
            if applications:
                def _sort_key(application: dict[str, Any]) -> tuple[int, str, int]:
                    same_plan = 0
                    if selected_plan_id is not None and int(application.get("plan_id") or 0) == int(selected_plan_id):
                        same_plan = 1
                    timestamp = str(application.get("applied_at") or application.get("created_at") or "")
                    return (same_plan, timestamp, int(application.get("id") or 0))

                latest_application = max(applications, key=_sort_key)
                normalized["business_key"] = latest_application.get("business_key")
                normalized["candidate_no"] = latest_application.get("candidate_no")
        return PortalStudentRecord(**normalized)

    @staticmethod
    def _generate_portal_temporary_password(length: int = 10) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def _normalize_portal_account_status(value: Any) -> str:
        text = str(value or "").strip()
        if text in {"已注销", "停用"}:
            return "停用"
        return "启用"

    def _build_portal_profile_payload(self, payload: Any) -> dict[str, Any] | None:
        profile = payload.profile.model_dump(exclude_none=True) if payload.profile is not None else {}
        fallback_profile = {
            "gender": payload.gender,
            "birth_date": payload.birth_date,
            "ethnic_group": payload.ethnic_group,
            "native_place": payload.native_place,
            "political_status": payload.political_status,
            "marital_status": payload.marital_status,
            "religious_belief": payload.religious_belief,
            "id_type": payload.id_type,
            "mailing_address": payload.mailing_address,
        }
        for key, value in fallback_profile.items():
            profile.setdefault(key, value)
        return profile or None

    def _build_portal_application_draft_payload(
        self,
        payload: Any,
        advisor_name: str | None,
        submitted_at: str | None,
    ) -> dict[str, Any]:
        preferences = [item.model_dump() for item in payload.preferences]
        if not preferences and payload.selected_team_name:
            preferences = [
                {
                    "preference_order": 1,
                    "research_center_name": payload.selected_team_name,
                    "advisor_name": advisor_name,
                    "is_optional": False,
                }
            ]
        personal_statement = payload.personal_statement.model_dump(exclude_none=True) if payload.personal_statement is not None else {}
        if payload.personal_statement_text and not personal_statement.get("personal_statement_text"):
            personal_statement["personal_statement_text"] = payload.personal_statement_text
        declaration = payload.declaration.model_dump(exclude_none=True) if payload.declaration is not None else {}
        declaration.setdefault("has_read_declaration", bool(payload.signed_agreement))
        return {
            "selected_plan_id": payload.plan_id,
            "source_channel": payload.source_channel,
            "source_channel_other": payload.source_channel_other,
            "preferences": preferences,
            "education_experiences": [item.model_dump() for item in payload.education_experiences],
            "practice_experiences": [item.model_dump() for item in payload.practice_experiences],
            "english_proficiencies": [item.model_dump() for item in payload.english_proficiencies],
            "family_members": [item.model_dump() for item in payload.family_members],
            "achievement_records": [item.model_dump() for item in payload.achievement_records],
            "personal_statement": personal_statement,
            "declaration": declaration,
            "submitted_at": submitted_at,
        }

    def save_portal_application_draft(self, student_id: int, payload: PortalApplicationDraftUpsert) -> PortalStudentRecord:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法保存草稿")

            selected_team_name = payload.selected_team_name
            advisor_name = payload.selected_advisor_name
            if selected_team_name:
                team = self._ensure_team_exists(selected_team_name)
                advisor_names = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
                if advisor_name and advisor_name not in advisor_names:
                    raise ValueError("所选导师不属于当前团队")
                if not advisor_name:
                    advisor_name = team.get("lead_advisor_name")

            now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            profile_payload = self._build_portal_profile_payload(payload)
            application_draft = self._build_portal_application_draft_payload(payload, advisor_name, student.get("submitted_at"))

            student.update(
                {
                    "gender": payload.gender,
                    "birth_date": payload.birth_date,
                    "ethnic_group": payload.ethnic_group,
                    "native_place": payload.native_place,
                    "marital_status": payload.marital_status,
                    "religious_belief": payload.religious_belief,
                    "id_type": payload.id_type,
                    "mailing_address": payload.mailing_address,
                    "graduation_school": payload.graduation_school,
                    "highest_degree": payload.highest_degree,
                    "intended_field": payload.intended_field,
                    "political_status": payload.political_status,
                    "english_level": payload.english_level,
                    "family_info": payload.family_info,
                    "education_experience": payload.education_experience,
                    "practice_experience": payload.practice_experience,
                    "personal_profile": payload.personal_profile,
                    "recommendation_notes": payload.recommendation_notes,
                    "personal_statement_text": payload.personal_statement_text,
                    "signed_agreement": payload.signed_agreement,
                    "selected_plan_id": payload.plan_id or student.get("selected_plan_id"),
                    "selected_team_name": selected_team_name,
                    "selected_advisor_name": advisor_name,
                    "self_evaluation": payload.self_evaluation,
                    "updated_at": now_text,
                    "profile": profile_payload,
                    "application_draft": application_draft,
                }
            )
            operation_log = self._record_operation("学生门户", "申请草稿", str(student_id), "保存草稿", f'学生 {student["full_name"]} 保存报名草稿', operator_username=student["phone_number"])
            try:
                self._persist_portal_student_change(student, operation_log)
            except Exception:
                self._save()
            return self._build_portal_student_record(student)

    def _build_portal_plan_record(self, item: dict[str, Any]) -> PortalPlanRecord:
        plan = self._build_recruit_plan_record(item)
        return PortalPlanRecord(
            id=plan.id,
            plan_name=plan.plan_name,
            academic_term=plan.academic_term,
            brochure_image_url=plan.brochure_image_url,
            summary=plan.plan_description,
        )

    def _build_portal_team_record(self, item: dict[str, Any]) -> PortalTeamRecord:
        team = self._build_center_record(item)
        return PortalTeamRecord(
            id=team.id,
            team_name=team.center_name,
            lead_advisor_name=team.director_name,
            advisor_names=team.advisor_names,
            department_name="",
            discipline_name="",
            research_directions=[],
            description=None,
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

    def get_recruitment_workbench(self) -> RecruitWorkbench:
        status_counter = Counter(item["application_status"] for item in self._list("recruitment_applications"))
        return RecruitWorkbench(
            plans=[
                RecruitPlanSummary(
                    plan_name=plan.plan_name,
                    academic_term=plan.academic_term,
                    plan_description=plan.plan_description,
                    application_count=plan.application_count,
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

    def get_recruitment_plans(
        self,
        keyword: str | None = None,
        semester: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RecruitPlanListResponse:
        try:
            items, total = self._postgres_store.list_recruitment_plans_page(
                keyword=keyword,
                semester=semester,
                page=page,
                page_size=page_size,
            )
            records = [RecruitPlanRecord(**item) for item in items]
            return RecruitPlanListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query recruitment plans from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = [self._build_recruit_plan_record(item) for item in self._list("recruitment_plans")]
        if keyword:
            items = [item for item in items if self._matches_keyword(item.plan_name, item.academic_term, item.plan_description, keyword=keyword)]
        if semester:
            items = [item for item in items if item.semester == semester]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return RecruitPlanListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_recruitment_plan(self, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item.setdefault("current_stage", "报名配置")
            item.setdefault("target_quota", 0)
            item.setdefault("interview_group_count", 0)
            item.setdefault("is_open", True)
            item["id"] = self._next_id("recruitment_plans")
            self._list("recruitment_plans").insert(0, item)
            operation_log = self._record_operation("招生管理", "招生计划", str(item["id"]), "新增", f'新增招生计划 {item["plan_name"]}')
            try:
                self._postgres_store.update_runtime_recruitment_plan(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("recruitment_plans", int(self._counters.get("recruitment_plans", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return self._build_recruit_plan_record(item)

    def update_recruitment_plan(self, plan_id: int, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            index, item = self._find_required("recruitment_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("recruitment_plans")[index] = updated
            operation_log = self._record_operation("招生管理", "招生计划", str(plan_id), "编辑", f'更新招生计划 {updated["plan_name"]}')
            try:
                self._postgres_store.update_runtime_recruitment_plan(int(plan_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return self._build_recruit_plan_record(updated)

    def delete_recruitment_plan(self, plan_id: int) -> None:
        with self._lock:
            index, item = self._find_required("recruitment_plans", plan_id)
            has_applications = any(int(application.get("plan_id") or 0) == int(plan_id) for application in self._list("recruitment_applications"))
            if has_applications:
                raise ValueError("当前招生计划下仍有报名申请，不能删除")
            self._list("recruitment_plans").pop(index)
            operation_log = self._record_operation("招生管理", "招生计划", str(plan_id), "删除", f'删除招生计划 {item["plan_name"]}')
            try:
                self._postgres_store.delete_recruitment_plan(int(plan_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def get_recruitment_applications(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RecruitApplicationListResponse:
        try:
            items, total = self._postgres_store.list_recruitment_applications_page(
                keyword=keyword,
                plan_id=plan_id,
                status=status,
                page=page,
                page_size=page_size,
            )
            records = [RecruitApplicationRecord(**item) for item in items]
            return RecruitApplicationListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query recruitment applications from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("recruitment_applications"))
        if plan_id is not None:
            items = [item for item in items if item["plan_id"] == plan_id]
        if status:
            items = [item for item in items if item["application_status"] == status]
        if keyword:
            term = keyword.lower()
            items = [
                item
                for item in items
                if term in str(item.get("business_key") or "").lower()
                or term in str(item.get("candidate_no") or "").lower()
                or term in item["student_name"].lower()
                or term in str(item.get("graduation_school") or "").lower()
                or term in str(item.get("graduate_school") or "").lower()
                or term in str(item.get("intended_field") or "").lower()
                or term in str(item.get("first_choice") or "").lower()
                or term in str(item.get("second_choice") or "").lower()
                or term in str(item.get("intended_advisor_name") or "").lower()
                or term in str(item.get("phone_number") or "").lower()
                or term in str(item.get("email") or "").lower()
            ]
        records = [RecruitApplicationRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RecruitApplicationListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_recruitment_application_detail(self, application_id: int) -> RecruitApplicationRecord:
        try:
            item = self._postgres_store.get_recruitment_application_detail(application_id)
            if item is not None:
                return RecruitApplicationRecord(**item)
        except Exception as exc:
            logger.warning("Query recruitment application detail from PostgreSQL failed, fallback to in-memory data: %s", exc)

        _, item = self._find_required("recruitment_applications", application_id)
        return RecruitApplicationRecord(**item)

    def create_recruitment_application(self, payload: RecruitApplicationUpsert, principal: Any | None = None) -> RecruitApplicationRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("recruitment_application", payload.model_dump())
            item["id"] = self._next_id("recruitment_applications")
            self._list("recruitment_applications").insert(0, item)
            self._start_managed_workflow("recruitment_application", item, operator_username=operator["username"])
            workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("招生管理", "报名申请", str(item["id"]), "新增", f'新增报名申请 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._persist_recruitment_application_change(
                    item,
                    operation_log,
                    workflow_task=workflow_located[1] if workflow_located is not None else None,
                    update_application_counter=True,
                    update_workflow_counter=workflow_located is not None,
                )
            except Exception:
                self._save()
            return RecruitApplicationRecord(**item)

    def import_recruitment_applications(
        self,
        plan_id: int,
        rows: list[dict[str, Any]],
        principal: Any | None = None,
    ) -> RecruitApplicationImportResult:
        with self._lock:
            self._find_required("recruitment_plans", plan_id)
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            imported_business_keys: list[str] = []
            issues: list[RecruitApplicationImportIssue] = []
            for row_number, row in enumerate(rows, start=2):
                student_name = str(row.get("student_name") or "").strip()
                if not student_name:
                    issues.append(RecruitApplicationImportIssue(row_number=row_number, student_name=None, reason="姓名为空，已跳过"))
                    continue

                duplicated = next(
                    (
                        item
                        for item in self._list("recruitment_applications")
                        if int(item.get("plan_id") or 0) == int(plan_id)
                        and str(item.get("student_name") or "").strip() == student_name
                        and (
                            (row.get("phone_number") and item.get("phone_number") == row.get("phone_number"))
                            or (row.get("email") and item.get("email") == row.get("email"))
                        )
                    ),
                    None,
                )
                if duplicated:
                    issues.append(
                        RecruitApplicationImportIssue(
                            row_number=row_number,
                            student_name=student_name,
                            reason=f'检测到重复报名申请，已跳过：{duplicated.get("business_key")}',
                        )
                    )
                    continue

                payload_data = {
                    **row,
                    "plan_id": int(plan_id),
                    "business_key": None,
                    "candidate_no": None,
                    "graduation_school": row.get("graduation_school") or row.get("undergraduate_school") or "待补充",
                    "highest_degree": row.get("highest_degree") or "硕士",
                    "intended_field": row.get("intended_field") or row.get("first_choice") or row.get("second_choice") or "待分配方向",
                    "material_status": row.get("material_status") or "待审核",
                    "application_status": row.get("application_status") or "报名已提交",
                    "reviewer_name": row.get("reviewer_name") or None,
                    "final_score": None,
                }
                item = self._workflow_initial_item("recruitment_application", RecruitApplicationUpsert(**payload_data).model_dump())
                item["id"] = self._next_id("recruitment_applications")
                self._list("recruitment_applications").insert(0, item)
                self._start_managed_workflow("recruitment_application", item, operator_username=operator["username"])
                workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
                operation_log = self._record_operation("招生管理", "报名申请", str(item["id"]), "导入", f'导入报名申请 {item["student_name"]}', operator_username=operator["username"])
                try:
                    self._persist_recruitment_application_change(
                        item,
                        operation_log,
                        workflow_task=workflow_located[1] if workflow_located is not None else None,
                        update_application_counter=True,
                        update_workflow_counter=workflow_located is not None,
                    )
                except Exception:
                    self._save()
                imported_business_keys.append(str(item["business_key"]))

            return RecruitApplicationImportResult(
                imported_count=len(imported_business_keys),
                skipped_count=len(issues),
                plan_id=int(plan_id),
                imported_business_keys=imported_business_keys,
                issues=issues,
            )

    def export_recruitment_applications(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
    ) -> bytes:
        records = self.get_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status, page=1, page_size=10000).items
        return build_recruitment_template([record.model_dump() for record in records])

    def export_recruitment_application_blank_template(self) -> bytes:
        return build_recruitment_template([])

    def register_portal_student(self, payload: PortalRegistrationRequest) -> PortalRegistrationResponse:
        with self._lock:
            now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if any(item.get("phone_number") == payload.phone_number for item in self._list("portal_students")):
                raise ValueError("该手机号已注册，请直接登录")
            if any(item.get("email") == payload.email for item in self._list("portal_students")):
                raise ValueError("该邮箱已注册，请直接登录")
            if any(item.get("id_number") == payload.id_number for item in self._list("portal_students")):
                raise ValueError("该身份证号已注册，请使用找回密码")

            item = payload.model_dump()
            password = item.pop("password")
            item.update(
                {
                    "id": self._next_id("portal_students"),
                    "account_status": "启用",
                    "password_hash": PASSWORD_CONTEXT.hash(password),
                    "gender": None,
                    "birth_date": None,
                    "ethnic_group": None,
                    "native_place": None,
                    "marital_status": None,
                    "religious_belief": None,
                    "id_type": "居民身份证",
                    "mailing_address": None,
                    "graduation_school": None,
                    "highest_degree": None,
                    "intended_field": None,
                    "political_status": None,
                    "english_level": None,
                    "family_info": None,
                    "education_experience": None,
                    "practice_experience": None,
                    "personal_profile": None,
                    "recommendation_notes": None,
                    "personal_statement_text": None,
                    "signed_agreement": False,
                    "selected_plan_id": None,
                    "selected_team_name": None,
                    "selected_advisor_name": None,
                    "self_evaluation": None,
                    "submitted_at": None,
                    "created_at": now_text,
                    "updated_at": now_text,
                }
            )
            self._list("portal_students").insert(0, item)
            operation_log = self._record_operation("学生门户", "门户注册", str(item["id"]), "注册", f'学生 {item["full_name"]} 完成门户注册', operator_username=item["phone_number"])
            try:
                self._persist_portal_student_change(item, operation_log, update_student_counter=True)
            except Exception:
                self._save()
            response = PortalRegistrationResponse(message="注册成功，请使用手机号或邮箱登录", student=self._build_portal_student_record(item))

        if self._email_service.enabled():
            self._email_service.send_portal_registration_success(item["full_name"], item["email"])
        return response

    def login_portal_student(self, payload: PortalLoginRequest) -> PortalStudentRecord:
        account = payload.account.strip()
        with self._lock:
            student = next(
                (
                    item for item in self._list("portal_students")
                    if item.get("phone_number") == account or item.get("email") == account
                ),
                None,
            )
            if not student:
                raise ValueError("账号不存在")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")
            password_hash = student.get("password_hash")
            if not password_hash or not PASSWORD_CONTEXT.verify(payload.password, password_hash):
                raise ValueError("账号或密码错误")
            return self._build_portal_student_record(student)

    def reset_portal_student_password(self, payload: PortalPasswordResetRequest) -> None:
        account = payload.account.strip()
        id_number = payload.id_number.strip()
        with self._lock:
            student = next(
                (
                    item for item in self._list("portal_students")
                    if item.get("phone_number") == account or item.get("email") == account
                ),
                None,
            )
            if not student:
                raise ValueError("账号不存在")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")
            if str(student.get("id_number") or "").strip() != id_number:
                raise ValueError("身份证号校验失败")
            student["password_hash"] = PASSWORD_CONTEXT.hash(payload.new_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation(
                "学生门户",
                "找回密码",
                str(student["id"]),
                "重置密码",
                f'学生 {student["full_name"]} 重置门户密码',
                operator_username=student["phone_number"],
            )
            try:
                self._postgres_store.update_runtime_portal_student(int(student["id"]), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        if self._email_service.enabled():
            self._email_service.send_portal_password_reset_success(student["full_name"], student["email"], account)

    def change_portal_student_password(self, student_id: int, payload: PortalPasswordChangeRequest) -> None:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法修改密码")
            password_hash = student.get("password_hash")
            if not password_hash or not PASSWORD_CONTEXT.verify(payload.current_password, password_hash):
                raise ValueError("当前密码不正确")
            student["password_hash"] = PASSWORD_CONTEXT.hash(payload.new_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation(
                "学生门户",
                "个人空间",
                str(student_id),
                "修改密码",
                f'学生 {student["full_name"]} 在个人空间修改密码',
                operator_username=student["phone_number"],
            )
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def get_portal_student(self, student_id: int) -> PortalStudentRecord:
        try:
            _, item = self._find_required("portal_students", student_id)
            return self._build_portal_student_record(item)
        except KeyError:
            postgres_item = self._postgres_store.get_portal_student_detail(student_id)
            if postgres_item is not None:
                return self._build_portal_student_record(postgres_item)
            raise

    def get_public_recruitment_plans(self) -> PortalPlanListResponse:
        source_items = sorted(self._list("recruitment_plans"), key=self._portal_plan_sort_key, reverse=True)
        items = [self._build_portal_plan_record(item) for item in source_items]
        return PortalPlanListResponse(items=items)

    def get_public_teams(self) -> PortalTeamListResponse:
        items = [self._build_portal_team_record(item) for item in self._list("teams") if item.get("status") != "停用"]
        return PortalTeamListResponse(items=items)

    def submit_portal_application(self, student_id: int, payload: PortalApplicationUpsert) -> PortalApplicationSubmissionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法提交报名")
            _, plan = self._find_required("recruitment_plans", payload.plan_id)
            selected_team_name = payload.selected_team_name
            if not selected_team_name:
                raise ValueError("缺少第一志愿研究中心信息")
            graduation_school = payload.graduation_school
            if not graduation_school:
                raise ValueError("缺少毕业院校/就读学校信息")
            highest_degree = payload.highest_degree
            if not highest_degree:
                raise ValueError("缺少最高学历/教育阶段信息")
            intended_field = payload.intended_field or selected_team_name
            team = self._ensure_team_exists(selected_team_name)
            advisor_names = self._normalize_name_list(team.get("advisor_names", []), team.get("lead_advisor_name"))
            advisor_name = payload.selected_advisor_name or team.get("lead_advisor_name")
            if advisor_name not in advisor_names:
                raise ValueError("所选导师不属于当前团队")
            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            profile_payload = self._build_portal_profile_payload(payload)
            application_draft = self._build_portal_application_draft_payload(payload, advisor_name, submitted_at)
            preference_names = [item.get("research_center_name") for item in application_draft.get("preferences", []) if item.get("research_center_name")]
            second_choice = preference_names[1] if len(preference_names) > 1 else None

            student.update(
                {
                    "gender": payload.gender,
                    "birth_date": payload.birth_date,
                    "ethnic_group": payload.ethnic_group,
                    "native_place": payload.native_place,
                    "marital_status": payload.marital_status,
                    "religious_belief": payload.religious_belief,
                    "id_type": payload.id_type,
                    "mailing_address": payload.mailing_address,
                    "graduation_school": graduation_school,
                    "highest_degree": highest_degree,
                    "intended_field": intended_field,
                    "political_status": payload.political_status,
                    "english_level": payload.english_level,
                    "family_info": payload.family_info,
                    "education_experience": payload.education_experience,
                    "practice_experience": payload.practice_experience,
                    "personal_profile": payload.personal_profile,
                    "recommendation_notes": payload.recommendation_notes,
                    "personal_statement_text": payload.personal_statement_text,
                    "signed_agreement": payload.signed_agreement,
                    "selected_plan_id": payload.plan_id,
                    "selected_team_name": selected_team_name,
                    "selected_advisor_name": advisor_name,
                    "self_evaluation": payload.self_evaluation,
                    "submitted_at": submitted_at,
                    "updated_at": submitted_at,
                    "profile": profile_payload,
                    "application_draft": application_draft,
                }
            )

            existing_application = next(
                (
                    item for item in self._list("recruitment_applications")
                    if int(item.get("plan_id") or 0) == int(payload.plan_id)
                    and item.get("phone_number") == student.get("phone_number")
                    and item.get("email") == student.get("email")
                ),
                None,
            )
            created_application = False
            created_workflow_task = False
            if existing_application:
                existing_application.update(
                    {
                        "student_name": student["full_name"],
                        "gender": payload.gender,
                        "graduation_school": graduation_school,
                        "highest_degree": highest_degree,
                        "intended_field": intended_field,
                        "first_choice": intended_field,
                        "second_choice": second_choice,
                        "political_status": payload.political_status,
                        "marital_status": payload.marital_status,
                        "religious_belief": payload.religious_belief,
                        "native_place": payload.native_place,
                        "mailing_address": payload.mailing_address,
                        "id_type": payload.id_type,
                        "intended_advisor_name": advisor_name,
                        "phone_number": student["phone_number"],
                        "email": student["email"],
                        "id_number": student["id_number"],
                        "family_info": payload.family_info,
                        "education_experience": payload.education_experience,
                        "practice_experience": payload.practice_experience,
                        "personal_statement_text": payload.personal_statement_text,
                        "personal_statement_attachment": (payload.personal_statement.resume_attachment_url if payload.personal_statement else None),
                        "supplementary_profile": payload.personal_profile,
                        "self_evaluation": payload.self_evaluation,
                        "discovery_channel": payload.source_channel_other or payload.source_channel,
                        "source_channel": payload.source_channel,
                        "source_channel_other": payload.source_channel_other,
                        "portal_student_id": student_id,
                        "applied_at": submitted_at,
                    }
                )
                workflow_located = self._workflow_task_index_by_business_key(str(existing_application.get("business_key") or ""))
                workflow_task = None
                if workflow_located is not None:
                    workflow_task, task_changed = self._sync_managed_workflow_task("recruitment_application", existing_application, existing_task=workflow_located[1])
                    if task_changed:
                        self._list("workflow_tasks")[workflow_located[0]] = workflow_task
                else:
                    self._start_managed_workflow("recruitment_application", existing_application, operator_username=student["phone_number"])
                    workflow_located = self._workflow_task_index_by_business_key(str(existing_application.get("business_key") or ""))
                    workflow_task = workflow_located[1] if workflow_located is not None else None
                    created_workflow_task = workflow_located is not None
                business_key = str(existing_application["business_key"])
                application_status = str(existing_application["application_status"])
                persisted_application = existing_application
            else:
                persisted_application = self._workflow_initial_item(
                    "recruitment_application",
                    RecruitApplicationUpsert(
                        plan_id=payload.plan_id,
                        student_name=student["full_name"],
                        gender=payload.gender,
                        graduation_school=graduation_school,
                        highest_degree=highest_degree,
                        intended_field=intended_field,
                        first_choice=intended_field,
                        second_choice=second_choice,
                        political_status=payload.political_status,
                        marital_status=payload.marital_status,
                        religious_belief=payload.religious_belief,
                        native_place=payload.native_place,
                        mailing_address=payload.mailing_address,
                        id_type=payload.id_type,
                        phone_number=student["phone_number"],
                        email=student["email"],
                        id_number=student["id_number"],
                        intended_advisor_name=advisor_name,
                        family_info=payload.family_info,
                        education_experience=payload.education_experience,
                        practice_experience=payload.practice_experience,
                        personal_statement_text=payload.personal_statement_text,
                        personal_statement_attachment=(payload.personal_statement.resume_attachment_url if payload.personal_statement else None),
                        supplementary_profile=payload.personal_profile,
                        self_evaluation=payload.self_evaluation,
                        discovery_channel=payload.source_channel_other or payload.source_channel,
                        source_channel=payload.source_channel,
                        source_channel_other=payload.source_channel_other,
                        portal_student_id=student_id,
                        applied_at=submitted_at,
                        material_status="待审核",
                        application_status="报名已提交",
                    ).model_dump(),
                )
                persisted_application["id"] = self._next_id("recruitment_applications")
                self._list("recruitment_applications").insert(0, persisted_application)
                self._start_managed_workflow("recruitment_application", persisted_application, operator_username=student["phone_number"])
                workflow_located = self._workflow_task_index_by_business_key(str(persisted_application.get("business_key") or ""))
                workflow_task = workflow_located[1] if workflow_located is not None else None
                created_application = True
                created_workflow_task = workflow_located is not None
                business_key = str(persisted_application["business_key"])
                application_status = str(persisted_application["application_status"])

            operation_log = self._record_operation("学生门户", "报名提交", str(student_id), "提交报名", f'学生 {student["full_name"]} 提交报名申请', operator_username=student["phone_number"])
            try:
                if persisted_application is not None:
                    self._persist_portal_application_submission(
                        student,
                        persisted_application,
                        operation_log,
                        workflow_task=workflow_task,
                        created_application=created_application,
                        created_workflow_task=created_workflow_task,
                    )
                else:
                    self._persist_portal_student_change(student, operation_log)
            except Exception:
                self._save()
            return PortalApplicationSubmissionResponse(
                student=self.get_portal_student(student_id),
                application_business_key=business_key,
                application_status=application_status,
            )

    def deactivate_registered_portal_student(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) == "停用":
                return RegisteredPortalStudentActionResponse(message="该注册学生账号已停用", account_status="停用")

            student["account_status"] = "停用"
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "停用账号", f'停用注册学生账号 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return RegisteredPortalStudentActionResponse(message="注册学生账号已停用", account_status="停用")

    def activate_registered_portal_student(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) == "启用":
                return RegisteredPortalStudentActionResponse(message="该注册学生账号已启用", account_status="启用")

            student["account_status"] = "启用"
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "启用账号", f'启用注册学生账号 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return RegisteredPortalStudentActionResponse(message="注册学生账号已启用", account_status="启用")

    def reset_registered_portal_student_password(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("已停用账号不可重置密码")

            temporary_password = self._generate_portal_temporary_password()
            student["password_hash"] = PASSWORD_CONTEXT.hash(temporary_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "重置密码", f'重置注册学生密码 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        email_sent = False
        if self._email_service.enabled():
            self._email_service.send_portal_admin_password_reset(
                str(student.get("full_name") or ""),
                str(student.get("email") or ""),
                temporary_password,
            )
            email_sent = True

        return RegisteredPortalStudentActionResponse(
            message="注册学生密码已重置",
            account_status=self._normalize_portal_account_status(student.get("account_status")),
            email_sent=email_sent,
            temporary_password=temporary_password,
        )

    def send_registered_portal_student_email(self, student_id: int, payload: RegisteredPortalStudentEmailRequest) -> RegisteredPortalStudentActionResponse:
        subject = payload.subject.strip()
        content = payload.content.strip()
        if not subject:
            raise ValueError("邮件主题不能为空")
        if not content:
            raise ValueError("邮件内容不能为空")

        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "发送邮件", f'向注册学生发送邮件 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        email_sent = False
        if self._email_service.enabled():
            self._email_service.send_message(to_email=str(student.get("email") or ""), subject=subject, text_body=content)
            email_sent = True

        return RegisteredPortalStudentActionResponse(
            message="邮件发送请求已处理",
            account_status=self._normalize_portal_account_status(student.get("account_status")),
            email_sent=email_sent,
        )

    def update_recruitment_application(self, application_id: int, payload: RecruitApplicationUpsert) -> RecruitApplicationRecord:
        with self._lock:
            index, item = self._find_required("recruitment_applications", application_id)
            incoming = {**item, **payload.model_dump(), "id": application_id}
            self._ensure_managed_status_fields_unchanged("recruitment_applications", item, incoming)
            updated = incoming
            workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            workflow_task = None
            if workflow_located is not None:
                workflow_task, task_changed = self._sync_managed_workflow_task("recruitment_application", updated, existing_task=workflow_located[1])
                if task_changed:
                    self._list("workflow_tasks")[workflow_located[0]] = workflow_task
            self._list("recruitment_applications")[index] = updated
            operation_log = self._record_operation("招生管理", "报名申请", str(application_id), "编辑", f'更新报名申请 {updated["student_name"]}')
            try:
                self._persist_recruitment_application_change(updated, operation_log, workflow_task=workflow_task)
            except Exception:
                self._save()
            return RecruitApplicationRecord(**updated)

    def delete_recruitment_application(self, application_id: int) -> None:
        with self._lock:
            list_items = self._list("recruitment_applications")
            index = next((item_index for item_index, item in enumerate(list_items) if int(item.get("id") or 0) == int(application_id)), None)
            item = list_items.pop(index) if index is not None else None
            try:
                deleted_record = self._postgres_store.delete_recruitment_application(int(application_id))
                if deleted_record is None and item is None:
                    raise KeyError(application_id)
                deleted_name = str((item or deleted_record or {}).get("student_name") or application_id)
                operation_log = self._record_operation("招生管理", "报名申请", str(application_id), "删除", f"删除报名申请 {deleted_name}")
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
                if item is None and deleted_record is not None:
                    self.state["recruitment_applications"] = [
                        existing for existing in list_items if int(existing.get("id") or 0) != int(application_id)
                    ]
            except KeyError:
                raise
            except Exception:
                self._save()

    def get_recruitment_stats(self) -> RecruitStats:
        plans = self._list("recruitment_plans")
        applications = self._list("recruitment_applications")
        return RecruitStats(
            plan_count=len(plans),
            open_plan_count=len(plans),
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
        center_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> StudentManagementResponse:
        try:
            items, total = self._postgres_store.list_students_page(
                keyword=keyword,
                status=status,
                advisor_name=advisor_name,
                center_name=center_name,
                page=page,
                page_size=page_size,
            )
            records = [StudentRecord(**item) for item in items]
            return StudentManagementResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query students from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("students"))
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["full_name"].lower() or term in item["team_name"].lower()]
        if status:
            items = [item for item in items if item["status"] == status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if center_name:
            items = [item for item in items if item["team_name"] == center_name]
        records = [
            StudentRecord(
                id=item["id"],
                student_no=item["student_no"],
                full_name=item["full_name"],
                status=item["status"],
                advisor_name=item["advisor_name"],
                center_name=item["team_name"],
                degree_type=item["degree_type"],
                enrollment_year=item["enrollment_year"],
                phone_number=item.get("phone_number"),
                political_status=item.get("political_status"),
            )
            for item in items
        ]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return StudentManagementResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_centers(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        director_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CenterListResponse:
        try:
            items, total = self._postgres_store.list_centers_page(
                keyword=keyword,
                is_enabled=is_enabled,
                director_name=director_name,
                page=page,
                page_size=page_size,
            )
            records = [CenterRecord(**item) for item in items]
            return CenterListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query centers from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("teams"))
        if keyword:
            items = [
                item for item in items
                if self._matches_keyword(
                    item.get("team_name"),
                    item.get("lead_advisor_name"),
                    *(item.get("advisor_names") or []),
                    keyword=keyword,
                )
            ]
        if is_enabled is not None:
            items = [item for item in items if (item.get("status") == "启用") == is_enabled]
        if director_name:
            items = [item for item in items if item["lead_advisor_name"] == director_name]
        records = [self._build_center_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return CenterListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_registered_portal_students(
        self,
        keyword: str | None = None,
        application_form_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RegisteredPortalStudentListResponse:
        try:
            items, total = self._postgres_store.list_registered_portal_students_page(
                keyword=keyword,
                application_form_status=application_form_status,
                page=page,
                page_size=page_size,
            )
            records = [RegisteredPortalStudentRecord(**item) for item in items]
            return RegisteredPortalStudentListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query registered portal students from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        portal_students = list(self._list("portal_students"))
        applications = list(self._list("recruitment_applications"))
        plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}

        latest_application_map: dict[int, dict[str, Any]] = {}
        for application in applications:
            portal_student_id = int(application.get("portal_student_id") or 0)
            if portal_student_id <= 0:
                continue
            previous = latest_application_map.get(portal_student_id)
            current_sort_key = str(application.get("applied_at") or application.get("created_at") or "")
            previous_sort_key = str(previous.get("applied_at") or previous.get("created_at") or "") if previous else ""
            if previous is None or current_sort_key >= previous_sort_key:
                latest_application_map[portal_student_id] = application

        records = []
        for student in portal_students:
            student_id = int(student.get("id") or 0)
            latest_application = latest_application_map.get(student_id)
            submitted_at = str(student.get("submitted_at") or latest_application.get("applied_at") or "").strip() if latest_application else str(student.get("submitted_at") or "").strip()
            application_status = str(latest_application.get("application_status") or "").strip() if latest_application else ""
            plan_id = student.get("selected_plan_id") or (latest_application.get("plan_id") if latest_application else None)
            record = RegisteredPortalStudentRecord(
                id=student_id,
                full_name=str(student.get("full_name") or ""),
                phone_number=str(student.get("phone_number") or ""),
                email=str(student.get("email") or ""),
                id_number=str(student.get("id_number") or ""),
                account_status=self._normalize_portal_account_status(student.get("account_status")),
                application_form_status="已填写报名" if submitted_at else "未填写报名",
                selected_plan_name=plan_name_map.get(int(plan_id or 0)) if plan_id is not None else None,
                selected_center_name=str(student.get("selected_team_name") or "") or None,
                selected_advisor_name=str(student.get("selected_advisor_name") or "") or None,
                recruitment_application_status=application_status or None,
                registered_at=str(student.get("created_at") or "") or None,
                submitted_at=submitted_at or None,
            )
            records.append(record)

        if keyword:
            records = [
                record for record in records
                if self._matches_keyword(
                    record.full_name,
                    record.phone_number,
                    record.email,
                    record.id_number,
                    record.selected_plan_name,
                    record.selected_center_name,
                    record.selected_advisor_name,
                    keyword=keyword,
                )
            ]
        if application_form_status:
            records = [record for record in records if record.application_form_status == application_form_status]

        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RegisteredPortalStudentListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_student_stats(self) -> StudentStats:
        distribution = Counter(item["status"] for item in self._list("students"))
        teams = self._list("teams")
        portal_students = self._list("portal_students")
        portal_submitted_total = len([item for item in portal_students if item.get("submitted_at")])
        return StudentStats(
            total_students=len(self._list("students")),
            active_students=distribution.get("在校", 0) + distribution.get("实习中", 0),
            outbound_students=distribution.get("外出研修", 0),
            thesis_students=distribution.get("学位论文阶段", 0),
            advisor_count=len({item["advisor_name"] for item in self._list("students")}),
            center_total=len(teams),
            enabled_center_total=len([item for item in teams if item.get("status") == "启用"]),
            registered_portal_total=len(portal_students),
            portal_submitted_total=portal_submitted_total,
            portal_unsubmitted_total=max(len(portal_students) - portal_submitted_total, 0),
        )

    def create_student(self, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            self._validate_student_payload(payload)
            item = {**payload.model_dump(exclude={"center_name"}), "team_name": payload.center_name}
            item["id"] = self._next_id("students")
            self._list("students").insert(0, item)
            operation_log = self._record_operation("学生管理", "学生主档", str(item["id"]), "新增", f'新增学生 {item["full_name"]}')
            try:
                self._persist_student_change(item, operation_log, created=True)
            except Exception as exc:
                logger.warning("Incremental student create sync failed, fallback to full state save: %s", exc)
                self._save()
            return StudentRecord(center_name=item["team_name"], **{key: value for key, value in item.items() if key != "team_name"})

    def update_student(self, student_id: int, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            self._validate_student_payload(payload, current_student_id=student_id)
            index, item = self._find_required("students", student_id)
            updated = {**item, **payload.model_dump(exclude={"center_name"}), "team_name": payload.center_name, "id": student_id}
            self._list("students")[index] = updated
            operation_log = self._record_operation("学生管理", "学生主档", str(student_id), "编辑", f'更新学生 {updated["full_name"]}')
            try:
                self._persist_student_change(updated, operation_log)
            except Exception as exc:
                logger.warning("Incremental student update sync failed, fallback to full state save: %s", exc)
                self._save()
            return StudentRecord(center_name=updated["team_name"], **{key: value for key, value in updated.items() if key != "team_name"})

    def delete_student(self, student_id: int) -> None:
        with self._lock:
            index, item = self._find_required("students", student_id)
            self._list("students").pop(index)
            operation_log = self._record_operation("学生管理", "学生主档", str(student_id), "删除", f'删除学生 {item["full_name"]}')
            try:
                self._postgres_store.sync_deleted_student(
                    student_id,
                    operation_log=operation_log,
                    counters={
                        "students": int(self._counters.get("students", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception as exc:
                logger.warning("Incremental student delete sync failed, fallback to full state save: %s", exc)
                self._save()

    def create_center(self, payload: CenterUpsert) -> CenterRecord:
        with self._lock:
            item = self._validate_center_payload(payload)
            item["id"] = self._next_id("teams")
            item["team_code"] = f"CENTER-{item['id']:03d}"
            item.setdefault("department_name", "")
            item.setdefault("discipline_name", "")
            item.setdefault("research_directions", [])
            item.setdefault("established_on", item.get("created_on"))
            item.setdefault("description", None)
            self._list("teams").insert(0, item)
            self._record_operation("学生管理", "研究中心主数据", str(item["id"]), "新增研究中心", f'新增研究中心 {item["team_name"]}')
            try:
                self._postgres_store.sync_created_center(
                    item,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception as exc:
                logger.warning("Incremental center create sync failed, fallback to full state save: %s", exc)
                self._save()
            return self._build_center_record(item)

    def update_center(self, center_id: int, payload: CenterUpsert) -> CenterRecord:
        with self._lock:
            postgres_teams = self._load_teams_from_postgres()
            if postgres_teams:
                self.state["teams"] = postgres_teams
                self._counters["teams"] = max([item.get("id", 0) for item in postgres_teams], default=0)
            index, current = self._find_required("teams", center_id)
            validated = self._validate_center_payload(payload, current_center_id=center_id)
            affected_students: list[dict[str, Any]] = []
            if current["team_name"] != validated["team_name"]:
                for student in self._list("students"):
                    if student.get("team_name") == current["team_name"]:
                        student["team_name"] = validated["team_name"]
                        affected_students.append(student)
            if any(student.get("team_name") == validated["team_name"] and student.get("advisor_name") not in validated["advisor_names"] for student in self._list("students")):
                raise ValueError("Current center members contain advisors outside the selected advisor set")
            updated = {**current, **validated, "id": center_id}
            self._list("teams")[index] = updated
            self._record_operation("学生管理", "研究中心主数据", str(center_id), "编辑研究中心", f'更新研究中心 {updated["team_name"]}')
            try:
                self._postgres_store.sync_updated_center(
                    updated,
                    affected_students=affected_students,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception as exc:
                logger.warning("Incremental center sync failed, fallback to full state save: %s", exc)
                self._save()
            return self._build_center_record(updated)

    def delete_center(self, center_id: int) -> None:
        with self._lock:
            index, item = self._find_required("teams", center_id)
            if any(student.get("team_name") == item["team_name"] for student in self._list("students")):
                raise ValueError("Center still has assigned students and cannot be deleted")
            self._list("teams").pop(index)
            self._record_operation("学生管理", "研究中心主数据", str(center_id), "删除研究中心", f'删除研究中心 {item["team_name"]}')
            try:
                self._postgres_store.sync_deleted_center(
                    center_id,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception as exc:
                logger.warning("Incremental center delete sync failed, fallback to full state save: %s", exc)
                self._save()

    def delete_centers(self, center_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for center_id in center_ids:
            self.delete_center(center_id)
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
        page: int = 1,
        page_size: int = 10,
    ) -> TrainingPlanListResponse:
        try:
            items, total = self._postgres_store.list_training_plans_page(
                keyword=keyword,
                plan_status=plan_status,
                advisor_name=advisor_name,
                report_cycle=report_cycle,
                page=page,
                page_size=page_size,
            )
            records = [TrainingPlanRecord(**item) for item in items]
            return TrainingPlanListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query training plans from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

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
        records = [TrainingPlanRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return TrainingPlanListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_training_plan(self, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("training_plans")
            self._list("training_plans").insert(0, item)
            operation_log = self._record_operation("培养管理", "培养方案", str(item["id"]), "登记方案", f'登记培养方案 {item["student_name"]}')
            try:
                self._postgres_store.update_runtime_training_plan(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("training_plans", int(self._counters.get("training_plans", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return TrainingPlanRecord(**item)

    def update_training_plan(self, plan_id: int, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("training_plans")[index] = updated
            operation_log = self._record_operation("培养管理", "培养方案", str(plan_id), "维护方案", f'维护培养方案 {updated["student_name"]}')
            try:
                self._postgres_store.update_runtime_training_plan(int(plan_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return TrainingPlanRecord(**updated)

    def delete_training_plan(self, plan_id: int) -> None:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            self._list("training_plans").pop(index)
            operation_log = self._record_operation("培养管理", "培养方案", str(plan_id), "删除方案", f'删除培养方案 {item["student_name"]}')
            try:
                self._postgres_store.delete_runtime_training_plan(int(plan_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
        page: int = 1,
        page_size: int = 10,
    ) -> ScientificReportListResponse:
        try:
            items, total = self._postgres_store.list_scientific_reports_page(
                keyword=keyword,
                status=status,
                reviewer_name=reviewer_name,
                page=page,
                page_size=page_size,
            )
            records = [ScientificReportRecord(**item) for item in items]
            return ScientificReportListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query scientific reports from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("scientific_reports"))
        if status:
            items = [item for item in items if item["report_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item.get("business_key"), item["student_no"], item["student_name"], item["period_label"], item["summary"], keyword=keyword)
            ]
        if reviewer_name:
            items = [item for item in items if item.get("reviewer_name") == reviewer_name]
        records = [ScientificReportRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ScientificReportListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_scientific_report(self, payload: ScientificReportUpsert, principal: Any | None = None) -> ScientificReportRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("scientific_report", payload.model_dump())
            item["id"] = self._next_id("scientific_reports")
            self._list("scientific_reports").insert(0, item)
            self._start_managed_workflow("scientific_report", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("培养管理", "科研报告", str(item["id"]), "登记报告", f'登记科研报告 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.update_runtime_scientific_report(int(item["id"]), item)
                if task_located is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task_located[1]["id"]), task_located[1])
                    self._postgres_store.update_runtime_counter("workflow_tasks", int(self._counters.get("workflow_tasks", 0)))
                self._postgres_store.update_runtime_counter("scientific_reports", int(self._counters.get("scientific_reports", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return ScientificReportRecord(**item)

    def update_scientific_report(self, report_id: int, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            incoming = {**item, **payload.model_dump(), "id": report_id}
            self._ensure_managed_status_fields_unchanged("scientific_reports", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("scientific_report", report_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("scientific_report", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("scientific_reports")[index] = updated
            operation_log = self._record_operation("培养管理", "科研报告", str(report_id), "维护报告", f'维护科研报告 {updated["student_name"]}')
            try:
                self._postgres_store.update_runtime_scientific_report(int(report_id), updated)
                if task is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task["id"]), task)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return ScientificReportRecord(**updated)

    def delete_scientific_report(self, report_id: int) -> None:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            self._list("scientific_reports").pop(index)
            operation_log = self._record_operation("培养管理", "科研报告", str(report_id), "删除报告", f'删除科研报告 {item["student_name"]}')
            try:
                self._postgres_store.delete_runtime_scientific_report(int(report_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
        page: int = 1,
        page_size: int = 10,
    ) -> OutboundStudyListResponse:
        try:
            items, total = self._postgres_store.list_outbound_studies_page(
                keyword=keyword,
                status=status,
                study_type=study_type,
                advisor_name=advisor_name,
                page=page,
                page_size=page_size,
            )
            records = [OutboundStudyRecord(**item) for item in items]
            return OutboundStudyListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query outbound studies from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("outbound_studies"))
        if status:
            items = [item for item in items if item["approval_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item.get("business_key"), item["student_no"], item["student_name"], item["destination"], item.get("expected_outcome"), keyword=keyword)
            ]
        if study_type:
            items = [item for item in items if item["study_type"] == study_type]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        records = [OutboundStudyRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return OutboundStudyListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_outbound_study(self, payload: OutboundStudyUpsert, principal: Any | None = None) -> OutboundStudyRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("outbound_study", payload.model_dump())
            item["id"] = self._next_id("outbound_studies")
            self._list("outbound_studies").insert(0, item)
            self._start_managed_workflow("outbound_study", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("培养管理", "外出研修", str(item["id"]), "发起研修", f'发起外出研修 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.update_runtime_outbound_study(int(item["id"]), item)
                if task_located is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task_located[1]["id"]), task_located[1])
                    self._postgres_store.update_runtime_counter("workflow_tasks", int(self._counters.get("workflow_tasks", 0)))
                self._postgres_store.update_runtime_counter("outbound_studies", int(self._counters.get("outbound_studies", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return OutboundStudyRecord(**item)

    def update_outbound_study(self, study_id: int, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            incoming = {**item, **payload.model_dump(), "id": study_id}
            self._ensure_managed_status_fields_unchanged("outbound_studies", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("outbound_study", study_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("outbound_study", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("outbound_studies")[index] = updated
            operation_log = self._record_operation("培养管理", "外出研修", str(study_id), "维护研修", f'维护外出研修 {updated["student_name"]}')
            try:
                self._postgres_store.update_runtime_outbound_study(int(study_id), updated)
                if task is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task["id"]), task)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return OutboundStudyRecord(**updated)

    def delete_outbound_study(self, study_id: int) -> None:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            self._list("outbound_studies").pop(index)
            operation_log = self._record_operation("培养管理", "外出研修", str(study_id), "删除研修", f'删除外出研修 {item["student_name"]}')
            try:
                self._postgres_store.delete_runtime_outbound_study(int(study_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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

    def get_theses(
        self,
        keyword: str | None = None,
        degree_status: str | None = None,
        advisor_name: str | None = None,
        thesis_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ThesisListResponse:
        items = list(self._list("theses"))
        if degree_status:
            items = [item for item in items if item["degree_status"] == degree_status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if thesis_status:
            items = [item for item in items if item["thesis_status"] == thesis_status]
        if keyword:
            term = keyword.lower()
            items = [
                item
                for item in items
                if term in str(item.get("business_key") or "").lower()
                or term in item["student_no"].lower()
                or term in item["student_name"].lower()
                or term in item["title"].lower()
            ]
        records = [ThesisRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ThesisListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_thesis(self, payload: ThesisUpsert, principal: Any | None = None) -> ThesisRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("thesis", payload.model_dump())
            item["id"] = self._next_id("theses")
            self._list("theses").insert(0, item)
            self._start_managed_workflow("thesis", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("学位管理", "论文主档", str(item["id"]), "新增", f'新增论文 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.update_runtime_thesis(int(item["id"]), item)
                if task_located is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task_located[1]["id"]), task_located[1])
                    self._postgres_store.update_runtime_counter("workflow_tasks", int(self._counters.get("workflow_tasks", 0)))
                self._postgres_store.update_runtime_counter("theses", int(self._counters.get("theses", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return ThesisRecord(**item)

    def update_thesis(self, thesis_id: int, payload: ThesisUpsert) -> ThesisRecord:
        with self._lock:
            index, item = self._find_required("theses", thesis_id)
            incoming = {**item, **payload.model_dump(), "id": thesis_id}
            self._ensure_managed_status_fields_unchanged("theses", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("thesis", thesis_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("thesis", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("theses")[index] = updated
            operation_log = self._record_operation("学位管理", "论文主档", str(thesis_id), "编辑", f'更新论文 {updated["student_name"]}')
            try:
                self._postgres_store.update_runtime_thesis(int(thesis_id), updated)
                if task is not None:
                    self._postgres_store.update_runtime_workflow_task(int(task["id"]), task)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return ThesisRecord(**updated)

    def delete_thesis(self, thesis_id: int) -> None:
        with self._lock:
            index, item = self._find_required("theses", thesis_id)
            self._list("theses").pop(index)
            operation_log = self._record_operation("学位管理", "论文主档", str(thesis_id), "删除", f'删除论文 {item["student_name"]}')
            try:
                self._postgres_store.delete_runtime_thesis(int(thesis_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def get_thesis_reviews(
        self,
        thesis_id: int | None = None,
        keyword: str | None = None,
        expert_name: str | None = None,
        review_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ThesisReviewListResponse:
        items = list(self._list("thesis_reviews"))
        if thesis_id is not None:
            items = [item for item in items if item["thesis_id"] == thesis_id]
        if expert_name:
            items = [item for item in items if item["expert_name"] == expert_name]
        if review_status:
            items = [item for item in items if item["review_status"] == review_status]
        if keyword:
            items = [item for item in items if self._matches_keyword(item["thesis_title"], item["expert_name"], item.get("review_comment"), keyword=keyword)]
        records = [ThesisReviewRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ThesisReviewListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_thesis_review(self, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("thesis_reviews")
            self._list("thesis_reviews").insert(0, item)
            operation_log = self._record_operation("学位管理", "盲审意见", str(item["id"]), "新增", f'新增盲审意见 {item["expert_name"]}')
            try:
                self._postgres_store.update_runtime_thesis_review(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("thesis_reviews", int(self._counters.get("thesis_reviews", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return ThesisReviewRecord(**item)

    def update_thesis_review(self, review_id: int, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            index, item = self._find_required("thesis_reviews", review_id)
            updated = {**item, **payload.model_dump(), "id": review_id}
            self._list("thesis_reviews")[index] = updated
            operation_log = self._record_operation("学位管理", "盲审意见", str(review_id), "编辑", f'更新盲审意见 {updated["expert_name"]}')
            try:
                self._postgres_store.update_runtime_thesis_review(int(review_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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

    def get_dict_types(self, keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> DictTypeListResponse:
        records = self._postgres_store.list_dict_types(keyword=keyword, status=status)
        items = [DictTypeRecord(**item) for item in records]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return DictTypeListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_dict_type(self, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.create_dict_type(payload.model_dump())
        return DictTypeRecord(**record)

    def update_dict_type(self, dict_type_id: int, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.update_dict_type(dict_type_id, payload.model_dump())
        return DictTypeRecord(**record)

    def delete_dict_type(self, dict_type_id: int) -> None:
        self._postgres_store.delete_dict_type(dict_type_id)

    def get_dict_data(
        self,
        keyword: str | None = None,
        dict_type: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> DictDataListResponse:
        records = self._postgres_store.list_dict_data(keyword=keyword, dict_type=dict_type, status=status)
        items = [DictDataRecord(**item) for item in records]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return DictDataListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_dict_data(self, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.create_dict_data(payload.model_dump())
        return DictDataRecord(**record)

    def update_dict_data(self, dict_data_id: int, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.update_dict_data(dict_data_id, payload.model_dump())
        return DictDataRecord(**record)

    def delete_dict_data(self, dict_data_id: int) -> None:
        self._postgres_store.delete_dict_data(dict_data_id)

    def get_roles(
        self,
        keyword: str | None = None,
        scope_name: str | None = None,
        permission: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RoleListResponse:
        items = list(self._list("roles"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["role_code"], item["role_name"], item["scope_name"], keyword=keyword)]
        if scope_name:
            items = [item for item in items if item["scope_name"] == scope_name]
        if permission:
            items = [item for item in items if permission in item.get("permissions", [])]
        records = [self._build_role_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RoleListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_role(self, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            item = payload.model_dump()
            if any(role["role_code"] == item["role_code"] for role in self._list("roles")):
                raise ValueError("Role code already exists")
            item["permissions"] = self._validate_permissions(item.get("permissions", []))
            item["id"] = self._next_id("roles")
            self._list("roles").insert(0, item)
            operation_log = self._record_operation("系统治理", "角色", str(item["id"]), "新建角色", f'新建角色 {item["role_name"]}')
            try:
                self._postgres_store.update_runtime_role(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("roles", int(self._counters.get("roles", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
            affected_users: list[dict[str, Any]] = []
            affected_profiles: list[tuple[str, dict[str, Any]]] = []
            if item["role_code"] != updated["role_code"]:
                for user_index, user in enumerate(self._list("system_users")):
                    if user["role_code"] == item["role_code"]:
                        updated_user = {**user, "role_code": updated["role_code"]}
                        self._list("system_users")[user_index] = updated_user
                        affected_users.append(updated_user)
                for username, profile in self.state.setdefault("profiles", {}).items():
                    if profile.get("role_name") in {item["role_name"], item["role_code"]}:
                        updated_profile = {**profile, "role_name": updated["role_name"]}
                        self.state["profiles"][username] = updated_profile
                        affected_profiles.append((username, updated_profile))
            elif item["role_name"] != updated["role_name"]:
                for username, profile in self.state.setdefault("profiles", {}).items():
                    if profile.get("role_name") == item["role_name"]:
                        updated_profile = {**profile, "role_name": updated["role_name"]}
                        self.state["profiles"][username] = updated_profile
                        affected_profiles.append((username, updated_profile))
            operation_log = self._record_operation("系统治理", "角色", str(role_id), "调整权限", f'更新角色 {updated["role_name"]} 的权限配置')
            try:
                self._postgres_store.update_runtime_role(int(role_id), updated)
                for affected_user in affected_users:
                    self._postgres_store.update_runtime_system_user(int(affected_user["id"]), affected_user)
                for username, affected_profile in affected_profiles:
                    self._postgres_store.update_runtime_profile(username, affected_profile)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return self._build_role_record(updated)

    def delete_role(self, role_id: int) -> None:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            in_use = next((user for user in self._list("system_users") if user["role_code"] == item["role_code"]), None)
            if in_use:
                raise ValueError("Role is assigned to users")
            self._list("roles").pop(index)
            operation_log = self._record_operation("系统治理", "角色", str(role_id), "删除角色", f'删除角色 {item["role_name"]}')
            try:
                self._postgres_store.delete_runtime_role(int(role_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
        page: int = 1,
        page_size: int = 10,
    ) -> SystemUserListResponse:
        try:
            items, total = self._postgres_store.list_system_users_page(
                keyword=keyword,
                role_code=role_code,
                account_status=account_status,
                department_name=department_name,
                page=page,
                page_size=page_size,
            )
            records = [SystemUserRecord(**item) for item in items]
            return SystemUserListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query system users from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("system_users"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["username"], item["full_name"], item["department_name"], keyword=keyword)]
        if role_code:
            items = [item for item in items if item["role_code"] == role_code]
        if account_status:
            items = [item for item in items if item["account_status"] == account_status]
        if department_name:
            items = [item for item in items if department_name in item["department_name"]]
        records = [self._build_system_user_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return SystemUserListResponse(items=paged_items, total=total, page=page, page_size=page_size)

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
            profile = self.state["profiles"][item["username"]]
            operation_log = self._record_operation("系统治理", "系统用户", str(item["id"]), "新建账号", f'新建系统账号 {item["full_name"]}')
            try:
                self._postgres_store.update_runtime_system_user(int(item["id"]), item)
                self._postgres_store.update_runtime_profile(item["username"], profile)
                self._postgres_store.update_runtime_counter("system_users", int(self._counters.get("system_users", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
            current_profile = self.state["profiles"][updated["username"]]
            operation_log = self._record_operation("系统治理", "系统用户", str(user_id), action_name, f'更新系统账号 {updated["full_name"]}')
            try:
                self._postgres_store.update_runtime_system_user(int(user_id), updated)
                self._postgres_store.update_runtime_profile(updated["username"], current_profile)
                if item["username"] != updated["username"]:
                    self._postgres_store.delete_runtime_profile(item["username"])
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return self._build_system_user_record(updated)

    def delete_system_user(self, user_id: int, current_username: str | None = None) -> None:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            if current_username and item["username"] == current_username:
                raise ValueError("Cannot delete current user")
            self._list("system_users").pop(index)
            self.state.setdefault("profiles", {}).pop(item["username"], None)
            operation_log = self._record_operation("系统治理", "系统用户", str(user_id), "删除账号", f'删除系统账号 {item["full_name"]}')
            try:
                self._postgres_store.delete_runtime_system_user(int(user_id))
                self._postgres_store.delete_runtime_profile(item["username"])
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def delete_system_users(self, user_ids: list[int], current_username: str | None = None) -> BulkActionResponse:
        success_count = 0
        for user_id in user_ids:
            self.delete_system_user(user_id, current_username=current_username)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_audit_policy_records(self, keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> AuditPolicyListResponse:
        items = list(self._list("audit_policies"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["item"], item["policy"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        records = [AuditPolicyRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return AuditPolicyListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_audit_policy(self, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("audit_policies")
            self._list("audit_policies").insert(0, item)
            operation_log = self._record_operation("系统治理", "审计策略", str(item["id"]), "新建策略", f'新建审计策略 {item["item"]}')
            try:
                self._postgres_store.update_runtime_audit_policy(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("audit_policies", int(self._counters.get("audit_policies", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return AuditPolicyRecord(**item)

    def update_audit_policy(self, policy_id: int, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            updated = {**item, **payload.model_dump(), "id": policy_id}
            self._list("audit_policies")[index] = updated
            operation_log = self._record_operation("系统治理", "审计策略", str(policy_id), "维护策略", f'更新审计策略 {updated["item"]}')
            try:
                self._postgres_store.update_runtime_audit_policy(int(policy_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return AuditPolicyRecord(**updated)

    def delete_audit_policy(self, policy_id: int) -> None:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            self._list("audit_policies").pop(index)
            operation_log = self._record_operation("系统治理", "审计策略", str(policy_id), "删除策略", f'删除审计策略 {item["item"]}')
            try:
                self._postgres_store.delete_runtime_audit_policy(int(policy_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def delete_audit_policies(self, policy_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for policy_id in policy_ids:
            self.delete_audit_policy(policy_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_integrations(
        self,
        keyword: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> IntegrationListResponse:
        items = list(self._list("integrations"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["name"], item["owner"], item["direction"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        if direction:
            items = [item for item in items if item["direction"] == direction]
        records = [IntegrationRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return IntegrationListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_integration(self, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("integrations")
            self._list("integrations").insert(0, item)
            operation_log = self._record_operation("系统治理", "集成链路", str(item["id"]), "新建链路", f'新建集成链路 {item["name"]}')
            try:
                self._postgres_store.update_runtime_integration(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("integrations", int(self._counters.get("integrations", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return IntegrationRecord(**item)

    def update_integration(self, integration_id: int, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            updated = {**item, **payload.model_dump(), "id": integration_id}
            self._list("integrations")[index] = updated
            operation_log = self._record_operation("系统治理", "集成链路", str(integration_id), "维护链路", f'更新集成链路 {updated["name"]}')
            try:
                self._postgres_store.update_runtime_integration(int(integration_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return IntegrationRecord(**updated)

    def delete_integration(self, integration_id: int) -> None:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            self._list("integrations").pop(index)
            operation_log = self._record_operation("系统治理", "集成链路", str(integration_id), "删除链路", f'删除集成链路 {item["name"]}')
            try:
                self._postgres_store.delete_runtime_integration(int(integration_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def delete_integrations(self, integration_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for integration_id in integration_ids:
            self.delete_integration(integration_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_operation_logs(
        self,
        keyword: str | None = None,
        module_name: str | None = None,
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> OperationLogListResponse:
        try:
            items, total = self._postgres_store.list_operation_logs_page(
                keyword=keyword,
                module_name=module_name,
                result=result,
                page=page,
                page_size=page_size,
            )
            records = [OperationLogRecord(**item) for item in items]
            return OperationLogListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query operation logs from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("operation_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["operator_username"], item["entity_name"], item["summary"], keyword=keyword)]
        if module_name:
            items = [item for item in items if item["module_name"] == module_name]
        if result:
            items = [item for item in items if item["result"] == result]
        records = [OperationLogRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return OperationLogListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_sync_logs(
        self,
        keyword: str | None = None,
        sync_status: str | None = None,
        source_system: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> SyncLogListResponse:
        try:
            items, total = self._postgres_store.list_sync_logs_page(
                keyword=keyword,
                sync_status=sync_status,
                source_system=source_system,
                page=page,
                page_size=page_size,
            )
            records = [SyncLogRecord(**item) for item in items]
            return SyncLogListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query sync logs from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("sync_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["source_system"], item["target_system"], item.get("failure_reason"), keyword=keyword)]
        if sync_status:
            items = [item for item in items if item["sync_status"] == sync_status]
        if source_system:
            items = [item for item in items if item["source_system"] == source_system]
        records = [SyncLogRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return SyncLogListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_system_architecture(self) -> SystemArchitecture:
        return SystemArchitecture(
            authentication="JWT + RBAC",
            database="PostgreSQL 17-",
            cache="Redis（单机/哨兵）",
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

    def get_workflow_tasks(
        self,
        status: str | None = None,
        module: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        page_size: int = 10,
        principal: Any | None = None,
    ) -> WorkflowTaskListResponse:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": []})
        try:
            items, total = self._postgres_store.list_workflow_tasks_page(
                status=status,
                module=module,
                keyword=keyword,
                page=page,
                page_size=page_size,
            )
            records = [self._build_workflow_task_record(item, principal_roles=principal_summary["roles"]) for item in items]
            return WorkflowTaskListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query workflow tasks from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("workflow_tasks"))
        if status:
            items = [item for item in items if item["status"] == status]
        if module:
            items = [item for item in items if item["business_module"] == module]
        if keyword:
            items = [item for item in items if self._matches_keyword(item["workflow_name"], item["business_key"], item["title"], item["applicant_name"], item["current_handler"], keyword=keyword)]
        records = [self._build_workflow_task_record(item, principal_roles=principal_summary["roles"]) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return WorkflowTaskListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_workflow_task(self, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("workflow_tasks")
            item["created_at"] = item.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["business_key"] = self._generate_workflow_business_key(item.get("workflow_name") or "未命名流程", created_at=item["created_at"])
            self._ensure_workflow_engine_metadata(item)
            self._list("workflow_tasks").insert(0, item)
            operation_log = self._record_operation("审批中心", "审批任务", str(item["id"]), "新增", f'新增审批任务 {item["title"]}')
            try:
                self._postgres_store.update_runtime_workflow_task(int(item["id"]), item)
                self._postgres_store.update_runtime_counter("workflow_tasks", int(self._counters.get("workflow_tasks", 0)))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return WorkflowTaskRecord(**item)

    def update_workflow_task(self, task_id: int, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            if item.get("flow_code"):
                raise ValueError("流程驱动任务不允许手工编辑，请通过流程动作推进")
            updated = {**item, **payload.model_dump(), "id": task_id, "business_key": item.get("business_key")}
            self._ensure_workflow_engine_metadata(updated)
            self._list("workflow_tasks")[index] = updated
            operation_log = self._record_operation("审批中心", "审批任务", str(task_id), "编辑", f'更新审批任务 {updated["title"]}')
            try:
                self._postgres_store.update_runtime_workflow_task(int(task_id), updated)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return WorkflowTaskRecord(**updated)

    def delete_workflow_task(self, task_id: int) -> None:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            if item.get("flow_code"):
                raise ValueError("流程驱动任务不允许手工删除")
            self._list("workflow_tasks").pop(index)
            operation_log = self._record_operation("审批中心", "审批任务", str(task_id), "删除", f'删除审批任务 {item["title"]}')
            try:
                self._postgres_store.delete_runtime_workflow_task(int(task_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
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
            try:
                self._postgres_store.update_runtime_profile(username, profile)
            except Exception as exc:
                logger.warning("Profile fallback runtime sync failed for %s: %s", username, exc)
        return UserProfile(**profile)

    def update_profile(self, username: str, payload: UserProfileUpdate) -> UserProfile:
        with self._lock:
            current = self.get_profile(username).model_dump()
            updated = {**current, **payload.model_dump(), "username": username}
            self.state.setdefault("profiles", {})[username] = updated
            updated_user: dict[str, Any] | None = None
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    updated_user = {**item, "full_name": updated["full_name"], "phone_number": updated.get("phone_number")}
                    self._list("system_users")[index] = updated_user
                    break
            operation_log = self._record_operation("个人空间", "个人资料", username, "编辑", f'更新个人资料 {updated["full_name"]}', operator_username=username)
            try:
                self._postgres_store.update_runtime_profile(username, updated)
                if updated_user is not None:
                    self._postgres_store.update_runtime_system_user(int(updated_user["id"]), updated_user)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return UserProfile(**updated)


class LazyRuntimeManagementStore:
    def __init__(self) -> None:
        self._instance: RuntimeManagementStore | None = None
        self._instance_lock = Lock()

    def _get_instance(self) -> RuntimeManagementStore:
        if self._instance is None:
            with self._instance_lock:
                if self._instance is None:
                    self._instance = RuntimeManagementStore()
        return self._instance

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_instance(), name)


store = LazyRuntimeManagementStore()
