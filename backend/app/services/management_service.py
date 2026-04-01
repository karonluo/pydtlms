from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any

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
    RecruitStats,
    RecruitWorkbench,
)
from app.schemas.student import (
    StudentLifecycleBoard,
    StudentManagementResponse,
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
    IntegrationListResponse,
    IntegrationRecord,
    IntegrationUpsert,
    OperationLogListResponse,
    OperationLogRecord,
    RoleListResponse,
    RoleRecord,
    RoleUpsert,
    SyncLogListResponse,
    SyncLogRecord,
    SystemArchitecture,
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
    TrainingPlanListResponse,
    TrainingPlanRecord,
    TrainingPlanUpsert,
    TrainingStats,
    TrainingTask,
    TrainingWorkbench,
)
from app.schemas.workflow import WorkflowStats, WorkflowTaskListResponse, WorkflowTaskRecord, WorkflowTaskUpsert


class DemoManagementStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._data_path = Path(__file__).resolve().parents[2] / "data" / "demo_store.json"
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()
        self._counters = self.state.setdefault("counters", {})

    def _seed_state(self) -> dict[str, Any]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "counters": {
                "students": 1000,
                "recruitment_plans": 100,
                "recruitment_applications": 5000,
                "training_plans": 300,
                "scientific_reports": 800,
                "outbound_studies": 120,
                "theses": 400,
                "thesis_reviews": 900,
                "roles": 30,
                "system_users": 300,
                "audit_policies": 60,
                "integrations": 40,
                "operation_logs": 10000,
                "sync_logs": 600,
                "workflow_tasks": 2000,
            },
            "profiles": {
                "admin": {
                    "username": "admin",
                    "full_name": "系统管理员",
                    "role_name": "平台管理员",
                    "department_name": "学科与研究生管理处",
                    "phone_number": "13800000000",
                    "email": "admin@dtlms.local",
                    "theme_color": "#0f4cbd",
                },
                "mentor.demo": {
                    "username": "mentor.demo",
                    "full_name": "导师示例账号",
                    "role_name": "导师",
                    "department_name": "智能制造学院",
                    "phone_number": "13800000088",
                    "email": "mentor.demo@dtlms.local",
                    "theme_color": "#13795b",
                },
            },
            "students": [
                {"id": 1, "student_no": "D20240001", "full_name": "陈一鸣", "status": "在校", "advisor_name": "刘亚", "team_name": "智能制造团队", "degree_type": "工程博士", "enrollment_year": 2024, "phone_number": "13800000001", "political_status": "中共党员"},
                {"id": 2, "student_no": "D20240007", "full_name": "王书宁", "status": "外出研修", "advisor_name": "刘亚", "team_name": "智能制造团队", "degree_type": "学术博士", "enrollment_year": 2024, "phone_number": "13800000007", "political_status": "共青团员"},
                {"id": 3, "student_no": "D20230018", "full_name": "张乐之", "status": "学位论文阶段", "advisor_name": "袁野", "team_name": "数据智能团队", "degree_type": "工程博士", "enrollment_year": 2023, "phone_number": "13800000018", "political_status": "群众"},
                {"id": 4, "student_no": "D20220009", "full_name": "赵嘉霖", "status": "实习中", "advisor_name": "徐素天", "team_name": "工业软件团队", "degree_type": "工程博士", "enrollment_year": 2022, "phone_number": "13800000009", "political_status": "中共预备党员"}
            ],
            "recruitment_plans": [
                {"id": 1, "plan_name": "2026 学术交流周", "academic_year": "2026", "semester": "秋", "current_stage": "资格审核", "target_quota": 120, "interview_group_count": 8, "is_open": True},
                {"id": 2, "plan_name": "2026 工程博士专项", "academic_year": "2026", "semester": "秋", "current_stage": "评分推荐", "target_quota": 80, "interview_group_count": 6, "is_open": True},
                {"id": 3, "plan_name": "2026 秋季招生", "academic_year": "2026", "semester": "秋", "current_stage": "预录取", "target_quota": 32, "interview_group_count": 4, "is_open": False}
            ],
            "recruitment_applications": [
                {"id": 1, "plan_id": 1, "candidate_no": "A20260001", "student_name": "李书航", "graduation_school": "东南大学", "highest_degree": "硕士", "intended_field": "智能制造", "material_status": "材料齐全", "application_status": "资格审核通过", "reviewer_name": "王天舒", "final_score": None},
                {"id": 2, "plan_id": 1, "candidate_no": "A20260002", "student_name": "周亦凡", "graduation_school": "同济大学", "highest_degree": "硕士", "intended_field": "控制科学", "material_status": "待补材料", "application_status": "报名已提交", "reviewer_name": None, "final_score": None},
                {"id": 3, "plan_id": 2, "candidate_no": "A20261018", "student_name": "陈思语", "graduation_school": "哈尔滨工业大学", "highest_degree": "硕士", "intended_field": "机器人", "material_status": "材料齐全", "application_status": "材料评分中", "reviewer_name": "刘亚", "final_score": 86.5},
                {"id": 4, "plan_id": 3, "candidate_no": "A20262021", "student_name": "吴启程", "graduation_school": "华中科技大学", "highest_degree": "硕士", "intended_field": "工业软件", "material_status": "材料齐全", "application_status": "预录取", "reviewer_name": "袁野", "final_score": 92.0}
            ],
            "training_plans": [
                {"id": 1, "student_no": "D20240001", "student_name": "陈一鸣", "advisor_name": "刘亚", "version_no": "v1.0", "report_cycle": "季度", "plan_status": "待学生确认", "scientific_goal": "完成智能制造调度知识图谱构建与实验验证", "assessment_rule": "每季度提交科研报告，年度中期考核"},
                {"id": 2, "student_no": "D20240007", "student_name": "王书宁", "advisor_name": "刘亚", "version_no": "v1.1", "report_cycle": "双月", "plan_status": "执行中", "scientific_goal": "完成控制科学方向仿真平台与论文投稿", "assessment_rule": "双月例会 + 阶段性成果复盘"},
                {"id": 3, "student_no": "D20230018", "student_name": "张乐之", "advisor_name": "袁野", "version_no": "v2.0", "report_cycle": "月度", "plan_status": "执行中", "scientific_goal": "完成论文定稿和学位前成果归档", "assessment_rule": "月度报告 + 论文节点检查"}
            ],
            "scientific_reports": [
                {"id": 1, "student_no": "D20240001", "student_name": "陈一鸣", "period_label": "2026Q1", "report_status": "待导师审阅", "reviewer_name": "刘亚", "review_score": None, "summary": "已完成知识图谱本体建模与基础规则整理。"},
                {"id": 2, "student_no": "D20240007", "student_name": "王书宁", "period_label": "2026-02", "report_status": "已通过", "reviewer_name": "刘亚", "review_score": 90.0, "summary": "已完成控制算法仿真验证。"},
                {"id": 3, "student_no": "D20230018", "student_name": "张乐之", "period_label": "2026-03", "report_status": "退回修改", "reviewer_name": "袁野", "review_score": 78.0, "summary": "论文实验部分需要补充对照组。"}
            ],
            "outbound_studies": [
                {"id": 1, "student_no": "D20240007", "student_name": "王书宁", "advisor_name": "刘亚", "study_type": "联合培养", "destination": "新加坡国立大学", "start_date": "2026-04-15", "end_date": "2026-10-15", "approval_status": "审批中", "expected_outcome": "完成联合课题实验与论文合作"},
                {"id": 2, "student_no": "D20220009", "student_name": "赵嘉霖", "advisor_name": "徐素天", "study_type": "企业研修", "destination": "无锡厚德自动化仪表有限公司", "start_date": "2026-03-01", "end_date": "2026-06-30", "approval_status": "研修中", "expected_outcome": "完成工业软件接口适配与案例沉淀"}
            ],
            "theses": [
                {"id": 1, "student_no": "D20230018", "student_name": "张乐之", "advisor_name": "袁野", "title": "高校博士生培养过程指标预测模型", "plagiarism_rate": 22.3, "thesis_status": "退回修改", "blind_review_status": "未送审", "defense_status": "未进入", "degree_status": "待申请"},
                {"id": 2, "student_no": "D20240001", "student_name": "陈一鸣", "advisor_name": "刘亚", "title": "智能制造知识图谱驱动调度研究", "plagiarism_rate": 18.4, "thesis_status": "查重通过", "blind_review_status": "进行中", "defense_status": "待安排", "degree_status": "授位审批中"},
                {"id": 3, "student_no": "D20220009", "student_name": "赵嘉霖", "advisor_name": "徐素天", "title": "多源日志语义融合与审计异常检测", "plagiarism_rate": 12.7, "thesis_status": "盲审通过", "blind_review_status": "已通过", "defense_status": "预答辩完成", "degree_status": "待正式答辩"}
            ],
            "thesis_reviews": [
                {"id": 1, "thesis_id": 2, "thesis_title": "智能制造知识图谱驱动调度研究", "expert_name": "专家A", "review_score": 88.0, "review_status": "已提交", "review_comment": "选题较好，建议补充案例。"},
                {"id": 2, "thesis_id": 3, "thesis_title": "多源日志语义融合与审计异常检测", "expert_name": "专家B", "review_score": 92.0, "review_status": "已通过", "review_comment": "结构完整，可进入答辩。"}
            ],
            "roles": [
                {"id": 1, "role_code": "platform_admin", "role_name": "平台管理员", "scope_name": "系统治理", "permissions": ["dashboard:read", "recruitment:read", "recruitment:write", "students:read", "students:write", "training:read", "training:write", "degree:read", "degree:write", "audit:read", "audit:write", "system:read", "system:write", "workflow:read", "workflow:write"]},
                {"id": 2, "role_code": "advisor", "role_name": "导师", "scope_name": "培养与学位", "permissions": ["dashboard:read", "students:read", "training:read", "training:write", "degree:read", "degree:write", "workflow:read"]},
                {"id": 3, "role_code": "secretary", "role_name": "学位秘书", "scope_name": "学位管理", "permissions": ["degree:read", "degree:write", "workflow:read", "workflow:write"]}
            ],
            "system_users": [
                {"id": 1, "username": "admin", "full_name": "系统管理员", "role_code": "platform_admin", "department_name": "学科与研究生管理处", "phone_number": "13800000000", "account_status": "启用"},
                {"id": 2, "username": "mentor.demo", "full_name": "导师示例账号", "role_code": "advisor", "department_name": "智能制造学院", "phone_number": "13800000088", "account_status": "启用"},
                {"id": 3, "username": "secretary.demo", "full_name": "学位秘书示例账号", "role_code": "secretary", "department_name": "学位办公室", "phone_number": "13800000066", "account_status": "启用"}
            ],
            "audit_policies": [
                {"id": 1, "item": "登录日志", "policy": "成功、失败、锁定、异地登录均留痕，保留 5 年。"},
                {"id": 2, "item": "操作日志", "policy": "关键实体的增删改审必须记录前后值、IP、设备和结果。"},
                {"id": 3, "item": "同步日志", "policy": "外部系统同步需记录总量、成功量、失败量和失败原因。"},
                {"id": 4, "item": "权限治理", "policy": "职责分离，禁止录入、评分、审批同人闭环完成。"}
            ],
            "integrations": [
                {"id": 1, "name": "招生系统", "direction": "主数据导入 / 录取回传", "cadence": "实时 + 每日对账", "status": "正常", "owner": "招生办公室"},
                {"id": 2, "name": "实验室 OA", "direction": "考勤 / 门禁 / 请假同步", "cadence": "实时事件 + 定时补偿", "status": "正常", "owner": "学院办公室"},
                {"id": 3, "name": "飞书", "direction": "待办通知 / 审批提醒 / 回执", "cadence": "实时", "status": "告警", "owner": "学合管理员"}
            ],
            "operation_logs": [
                {"id": 1, "operated_at": now, "operator_username": "admin", "module_name": "招生管理", "entity_name": "报名申请", "entity_id": "4", "action": "预录取确认", "result": "success", "summary": "确认吴启程进入预录取池。"},
                {"id": 2, "operated_at": now, "operator_username": "admin", "module_name": "培养管理", "entity_name": "培养方案", "entity_id": "2", "action": "发布版本", "result": "success", "summary": "王书宁培养方案版本发布为 v1.1。"}
            ],
            "sync_logs": [
                {"id": 1, "source_system": "招生系统", "target_system": "DTLMS", "sync_status": "success", "record_count": 120, "executed_at": now, "failure_reason": None},
                {"id": 2, "source_system": "DTLMS", "target_system": "飞书", "sync_status": "failed", "record_count": 4, "executed_at": now, "failure_reason": "回执接口超时"}
            ],
            "workflow_tasks": [
                {"id": 1, "workflow_name": "外出研修审批", "business_module": "培养管理", "business_key": "OUT-1", "title": "王书宁联合培养申请", "applicant_name": "王书宁", "current_handler": "刘亚", "current_node": "导师审核", "priority": "高", "status": "处理中", "created_at": now, "due_at": "2026-04-05 18:00:00", "form_summary": "研修地点：新加坡国立大学；周期：6个月", "latest_comment": "待导师确认联合培养计划。"},
                {"id": 2, "workflow_name": "学位申请审批", "business_module": "学位管理", "business_key": "DEG-2", "title": "陈一鸣授位审批", "applicant_name": "陈一鸣", "current_handler": "学位秘书", "current_node": "材料复核", "priority": "中", "status": "待处理", "created_at": now, "due_at": "2026-04-03 12:00:00", "form_summary": "论文查重通过，盲审进行中。", "latest_comment": "待核验盲审回执。"},
                {"id": 3, "workflow_name": "导师变更审批", "business_module": "学生管理", "business_key": "ADV-3", "title": "赵嘉霖导师变更申请", "applicant_name": "赵嘉霖", "current_handler": "学合管理员", "current_node": "管理员统筹", "priority": "中", "status": "已通过", "created_at": now, "due_at": "2026-03-20 17:00:00", "form_summary": "原导师：刘亚，新导师：徐素天", "latest_comment": "已完成权限级联刷新。"}
            ]
        }

    def _load_state(self) -> dict[str, Any]:
        if not self._data_path.exists():
            state = self._seed_state()
            self._write_state(state)
            return state
        return json.loads(self._data_path.read_text(encoding="utf-8"))

    def _write_state(self, state: dict[str, Any] | None = None) -> None:
        payload = state or self.state
        self._data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

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

    def get_students(self, keyword: str | None = None, status: str | None = None, advisor_name: str | None = None) -> StudentManagementResponse:
        items = list(self._list("students"))
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["full_name"].lower() or term in item["team_name"].lower()]
        if status:
            items = [item for item in items if item["status"] == status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        return StudentManagementResponse(items=[StudentRecord(**item) for item in items], total=len(items))

    def get_student_stats(self) -> StudentStats:
        distribution = Counter(item["status"] for item in self._list("students"))
        return StudentStats(
            total_students=len(self._list("students")),
            active_students=distribution.get("在校", 0) + distribution.get("实习中", 0),
            outbound_students=distribution.get("外出研修", 0),
            thesis_students=distribution.get("学位论文阶段", 0),
            advisor_count=len({item["advisor_name"] for item in self._list("students")}),
        )

    def create_student(self, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("students")
            self._list("students").insert(0, item)
            self._record_operation("学生管理", "学生主档", str(item["id"]), "新增", f'新增学生 {item["full_name"]}')
            self._save()
            return StudentRecord(**item)

    def update_student(self, student_id: int, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
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

    def get_training_plans(self) -> TrainingPlanListResponse:
        items = [TrainingPlanRecord(**item) for item in self._list("training_plans")]
        return TrainingPlanListResponse(items=items, total=len(items))

    def create_training_plan(self, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("training_plans")
            self._list("training_plans").insert(0, item)
            self._record_operation("培养管理", "培养方案", str(item["id"]), "新增", f'新增培养方案 {item["student_name"]}')
            self._save()
            return TrainingPlanRecord(**item)

    def update_training_plan(self, plan_id: int, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("training_plans")[index] = updated
            self._record_operation("培养管理", "培养方案", str(plan_id), "编辑", f'更新培养方案 {updated["student_name"]}')
            self._save()
            return TrainingPlanRecord(**updated)

    def get_scientific_reports(self, keyword: str | None = None, status: str | None = None) -> ScientificReportListResponse:
        items = list(self._list("scientific_reports"))
        if status:
            items = [item for item in items if item["report_status"] == status]
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["student_name"].lower() or term in item["period_label"].lower()]
        return ScientificReportListResponse(items=[ScientificReportRecord(**item) for item in items], total=len(items))

    def create_scientific_report(self, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("scientific_reports")
            self._list("scientific_reports").insert(0, item)
            self._record_operation("培养管理", "科研报告", str(item["id"]), "新增", f'新增科研报告 {item["student_name"]}')
            self._save()
            return ScientificReportRecord(**item)

    def update_scientific_report(self, report_id: int, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            updated = {**item, **payload.model_dump(), "id": report_id}
            self._list("scientific_reports")[index] = updated
            self._record_operation("培养管理", "科研报告", str(report_id), "编辑", f'更新科研报告 {updated["student_name"]}')
            self._save()
            return ScientificReportRecord(**updated)

    def get_outbound_studies(self, keyword: str | None = None, status: str | None = None) -> OutboundStudyListResponse:
        items = list(self._list("outbound_studies"))
        if status:
            items = [item for item in items if item["approval_status"] == status]
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["student_name"].lower() or term in item["destination"].lower()]
        return OutboundStudyListResponse(items=[OutboundStudyRecord(**item) for item in items], total=len(items))

    def create_outbound_study(self, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("outbound_studies")
            self._list("outbound_studies").insert(0, item)
            self._record_operation("培养管理", "外出研修", str(item["id"]), "新增", f'新增外出研修 {item["student_name"]}')
            self._save()
            return OutboundStudyRecord(**item)

    def update_outbound_study(self, study_id: int, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            updated = {**item, **payload.model_dump(), "id": study_id}
            self._list("outbound_studies")[index] = updated
            self._record_operation("培养管理", "外出研修", str(study_id), "编辑", f'更新外出研修 {updated["student_name"]}')
            self._save()
            return OutboundStudyRecord(**updated)

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

    def get_roles(self) -> RoleListResponse:
        items = [RoleRecord(**item) for item in self._list("roles")]
        return RoleListResponse(items=items, total=len(items))

    def create_role(self, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("roles")
            self._list("roles").insert(0, item)
            self._record_operation("系统治理", "角色", str(item["id"]), "新增", f'新增角色 {item["role_name"]}')
            self._save()
            return RoleRecord(**item)

    def update_role(self, role_id: int, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            updated = {**item, **payload.model_dump(), "id": role_id}
            self._list("roles")[index] = updated
            self._record_operation("系统治理", "角色", str(role_id), "编辑", f'更新角色 {updated["role_name"]}')
            self._save()
            return RoleRecord(**updated)

    def get_system_users(self) -> SystemUserListResponse:
        items = [SystemUserRecord(**item) for item in self._list("system_users")]
        return SystemUserListResponse(items=items, total=len(items))

    def create_system_user(self, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("system_users")
            self._list("system_users").insert(0, item)
            self._record_operation("系统治理", "系统用户", str(item["id"]), "新增", f'新增系统用户 {item["full_name"]}')
            self._save()
            return SystemUserRecord(**item)

    def update_system_user(self, user_id: int, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            updated = {**item, **payload.model_dump(), "id": user_id}
            self._list("system_users")[index] = updated
            self._record_operation("系统治理", "系统用户", str(user_id), "编辑", f'更新系统用户 {updated["full_name"]}')
            self._save()
            return SystemUserRecord(**updated)

    def get_audit_policy_records(self) -> AuditPolicyListResponse:
        items = [AuditPolicyRecord(**item) for item in self._list("audit_policies")]
        return AuditPolicyListResponse(items=items, total=len(items))

    def create_audit_policy(self, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("audit_policies")
            self._list("audit_policies").insert(0, item)
            self._record_operation("系统治理", "审计策略", str(item["id"]), "新增", f'新增审计策略 {item["item"]}')
            self._save()
            return AuditPolicyRecord(**item)

    def update_audit_policy(self, policy_id: int, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            updated = {**item, **payload.model_dump(), "id": policy_id}
            self._list("audit_policies")[index] = updated
            self._record_operation("系统治理", "审计策略", str(policy_id), "编辑", f'更新审计策略 {updated["item"]}')
            self._save()
            return AuditPolicyRecord(**updated)

    def get_integrations(self) -> IntegrationListResponse:
        items = [IntegrationRecord(**item) for item in self._list("integrations")]
        return IntegrationListResponse(items=items, total=len(items))

    def create_integration(self, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("integrations")
            self._list("integrations").insert(0, item)
            self._record_operation("系统治理", "集成链路", str(item["id"]), "新增", f'新增集成链路 {item["name"]}')
            self._save()
            return IntegrationRecord(**item)

    def update_integration(self, integration_id: int, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            updated = {**item, **payload.model_dump(), "id": integration_id}
            self._list("integrations")[index] = updated
            self._record_operation("系统治理", "集成链路", str(integration_id), "编辑", f'更新集成链路 {updated["name"]}')
            self._save()
            return IntegrationRecord(**updated)

    def get_operation_logs(self) -> OperationLogListResponse:
        items = [OperationLogRecord(**item) for item in self._list("operation_logs")]
        return OperationLogListResponse(items=items, total=len(items))

    def get_sync_logs(self) -> SyncLogListResponse:
        items = [SyncLogRecord(**item) for item in self._list("sync_logs")]
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
            profile = {
                "username": fallback["username"],
                "full_name": fallback["full_name"],
                "role_name": fallback["role_code"],
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
