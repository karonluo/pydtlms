from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
import hashlib
import json
import logging
from time import perf_counter
import secrets
import string
from threading import Lock, RLock
from typing import Any, TypeVar

from passlib.context import CryptContext

from app.core.cache import build_cache_key, get_cache_client
from app.core.exceptions import DatabaseUnavailableError
from app.schemas.contact import validate_email, validate_optional_email, validate_optional_phone_number, validate_phone_number
from app.schemas.auth import Principal, UserProfile, UserProfileUpdate
from app.schemas.portal import (
    PortalAdvisorRecord,
    PortalApplicationSubmissionResponse,
    PortalApplicationDraftUpsert,
    PortalApplicationUpsert,
    PortalWorkflowProgressSummary,
    PortalWorkflowStageItem,
    PortalLoginRequest,
    PortalImpersonationLaunchResponse,
    PortalPasswordChangeRequest,
    PortalPlanListResponse,
    PortalPlanRecord,
    PortalProfileOptionsResponse,
    PortalPasswordResetRequest,
    PortalRegistrationEmailCodeResponse,
    PortalRegistrationRequest,
    PortalRegistrationResponse,
    PortalSessionResponse,
    PortalStudentRecord,
    PortalTeamListResponse,
    PortalTeamRecord,
)
from app.schemas.dashboard import (
    DashboardAlert,
    DashboardOverview,
    DashboardUndergraduateSchoolGroupDistribution,
    DashboardUndergraduateSchoolGroupDistributionResponse,
    DashboardUndergraduateSchoolGroupItem,
    DashboardUndergraduateSchoolRankingItem,
    DashboardUndergraduateSchoolStudentItem,
    DashboardUndergraduateSchoolStudentListResponse,
    MetricCard,
)
from app.schemas.recruitment import (
    AdvisorScreeningBatchSubmitRequest,
    AdvisorScreeningBatchSubmitResponse,
    InitialScreeningConfirmationRequest,
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
    CenterDirector,
    CenterListResponse,
    CenterRecord,
    CenterUpsert,
    RegisteredPortalStudentActionResponse,
    RegisteredPortalStudentExportJobCreateResponse,
    RegisteredPortalStudentExportJobListResponse,
    RegisteredPortalStudentExportJobRecord,
    RegisteredPortalStudentExportRequest,
    RegisteredPortalStudentEmailRequest,
    RegisteredPortalStudentRollbackStageRequest,
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
    NotificationDeliveryLogListResponse,
    NotificationDeliveryLogRecord,
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
    SystemUserImportIssue,
    SystemUserImportResult,
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


PASSWORD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
ListItemT = TypeVar("ListItemT")
logger = logging.getLogger(__name__)
FINAL_WORKFLOW_STATUSES = {"已通过", "已驳回"}
PORTAL_RESUBMITTABLE_APPLICATION_STATUSES = {"驳回重填", "不录取"}
ADMITTED_RECRUITMENT_APPLICATION_STATUSES = {"材料评分中", "面试待安排", "面试完成", "预录取", "同意录取"}
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
PORTAL_POLITICAL_STATUS_PRIORITY = {
    "中共党员": 10,
    "中共预备党员": 20,
    "共青团员": 30,
    "群众": 31,
}
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
CACHE_NULL_SENTINEL_KEY = "__cached_null__"
CACHE_NULL_TTL_SECONDS = 60
CACHE_TTL_JITTER_SECONDS = 30
SYSTEM_USER_AUTH_CACHE_TTL_SECONDS = 120
SYSTEM_USER_LIST_CACHE_TTL_SECONDS = 60
USER_PROFILE_CACHE_TTL_SECONDS = 300
CACHE_REBUILD_LOCKS: dict[str, Lock] = {}
CACHE_REBUILD_LOCKS_GUARD = Lock()
ROLE_DISPLAY_NAMES = {
    "platform_admin": "平台管理员",
    "AILABMGT": "书院管理员",
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
        "business_key_prefix": "SH",
        "managed_fields": ("application_status",),
        "initial_field_values": {"application_status": "报名已提交"},
        "nodes": {
            "qualification_review": {
                "label": "资格审核",
                "handler_roles": ["AILABMGT"],
                "due_days": 1,
                "actions": {
                    "approve": {
                        "label": "审核通过",
                        "next_node": "background_assessment",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "待背景评估"},
                    },
                    "reject": {
                        "label": "审核不通过",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "驳回重填"},
                    },
                },
            },
            "background_assessment": {
                "label": "背景评估",
                "handler_roles": ["AILABMGT"],
                "due_days": 2,
                "actions": {
                    "approve": {
                        "label": "评估通过",
                        "next_node": "advisor_screening",
                        "task_status": "处理中",
                        "field_updates": {"application_status": "待导师初筛-第一志愿"},
                    },
                    "reject": {
                        "label": "评估不通过",
                        "next_node": None,
                        "task_status": "已驳回",
                        "field_updates": {"application_status": "报名终止"},
                    },
                },
            },
            "advisor_screening": {
                "label": "导师初筛",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {},
            },
            "initial_screening_confirmation": {
                "label": "初筛确认",
                "handler_roles": ["AILABMGT"],
                "due_days": 2,
                "actions": {},
            },
            "camp_interview": {
                "label": "入营面试",
                "handler_roles": ["AILABMGT"],
                "due_days": 2,
                "actions": {},
            },
            "result_publish": {
                "label": "结果公布",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {},
            },
            "pre_admission": {
                "label": "预录取",
                "handler_roles": ["advisor"],
                "due_days": 2,
                "actions": {},
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
    "qin.rao": "QinRao@2026",
    "yuan.ye": "YuanYe@2026",
    "xu.sutian": "XuSutian@2026",
    "zhou.qing": "ZhouQing@2026",
    "he.lin": "HeLin@2026",
    "cao.bo": "CaoBo@2026",
    "yang.qin": "YangQin@2026",
    "sun.wei": "SunWei@2026",
}
PERMISSION_CATALOG: list[dict[str, str]] = [
    {"code": "dashboard:read", "name": "查看经营总览", "module_name": "工作台", "description": "查看工作台下的经营总览、预警和统计看板。"},
    {"code": "workflow_center_menu:read", "name": "查看流程待办菜单", "module_name": "工作台", "description": "查看工作台下的流程待办入口。"},
    {"code": "recruitment:read", "name": "查看招生业务", "module_name": "招生管理", "description": "查看招生计划、报名申请和过程数据。"},
    {"code": "recruitment:write", "name": "维护招生业务", "module_name": "招生管理", "description": "新建、编辑和推进招生业务流程。"},
    {"code": "news_management:read", "name": "查看新闻管理菜单", "module_name": "招生管理", "description": "查看招生管理下的新闻管理入口。"},
    {"code": "recruitment_plan:read", "name": "查看招生计划菜单", "module_name": "招生管理", "description": "查看招生管理下的招生计划入口。"},
    {"code": "recruitment_registered_students:read", "name": "查看注册学生菜单", "module_name": "招生管理", "description": "查看招生管理下的注册学生入口。"},
    {"code": "recruitment_registered_students:write", "name": "退回注册学生环节", "module_name": "招生管理", "description": "允许在注册学生页面退回报名申请到指定流程环节。"},
    {"code": "research_center:read", "name": "查看研究中心菜单", "module_name": "学生管理", "description": "查看学生管理下的研究中心入口与中心数据。"},
    {"code": "research_center:write", "name": "维护研究中心数据", "module_name": "学生管理", "description": "维护研究中心资料、负责人和导师团队。"},
    {"code": "recruitment_advisor_screening:read", "name": "查看导师初筛菜单", "module_name": "招生管理", "description": "查看招生管理下的导师初筛入口。"},
    {"code": "recruitment_camp_offer:read", "name": "查看入营名单菜单", "module_name": "招生管理", "description": "查看招生管理下的入营名单入口。"},
    {"code": "recruitment_camp_offer:write", "name": "维护入营名单数据", "module_name": "招生管理", "description": "新建、编辑、删除和导入入营名单，发送通知邮件并维护邮件模板。"},
    {"code": "recruitment_initial_screening_confirmation:read", "name": "查看初筛确认菜单", "module_name": "招生管理", "description": "查看招生管理下的初筛确认入口。"},
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
    {"code": "workflow:read", "name": "查看流程处理数据", "module_name": "流程处理", "description": "查看流程详情、候选动作和状态数据，供各业务菜单内处理流程时使用。"},
    {"code": "workflow:write", "name": "处理流程任务", "module_name": "流程处理", "description": "在各业务菜单内处理流程任务和推进流程节点。"},
]
