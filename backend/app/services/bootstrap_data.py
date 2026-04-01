from app.schemas.dashboard import DashboardAlert, DashboardOverview, MetricCard
from app.schemas.recruitment import RecruitPlanSummary, RecruitWorkbench
from app.schemas.student import StudentLifecycleBoard, StudentSummary
from app.schemas.training import DegreeWorkbench, TrainingTask, TrainingWorkbench


def build_dashboard_overview() -> DashboardOverview:
    return DashboardOverview(
        lifecycle_coverage=[
            MetricCard(label="生命周期覆盖", value="招生-毕业-就业", target="全流程", trend="闭环完成", status="healthy"),
            MetricCard(label="角色体系", value="8类角色", target="RBAC", trend="含评分人/面试官", status="healthy"),
            MetricCard(label="集成系统", value="6个外部系统", target="招生/OA/飞书", trend="双向同步", status="attention"),
        ],
        recruitment_metrics=[
            MetricCard(label="进行中计划", value="4", target="年内滚动", trend="预录取阶段2个", status="healthy"),
            MetricCard(label="资格审核通过率", value="79%", target=">=75%", trend="较上期+6%", status="healthy"),
            MetricCard(label="面试安排及时率", value="92%", target=">=95%", trend="需补强", status="attention"),
        ],
        training_metrics=[
            MetricCard(label="培养方案生效率", value="100%", target="100%", trend="导师确认完成", status="healthy"),
            MetricCard(label="科研报告提交率", value="94%", target=">=95%", trend="月底冲刺", status="attention"),
            MetricCard(label="导师审阅及时率", value="87%", target=">=90%", trend="需提醒", status="warning"),
        ],
        degree_metrics=[
            MetricCard(label="答辩流程中", value="34", target="学位季", trend="盲审待办8人", status="healthy"),
            MetricCard(label="查重一次通过", value="91%", target=">=90%", trend="维持高位", status="healthy"),
            MetricCard(label="正式授位通过率", value="96%", target=">=95%", trend="稳态运行", status="healthy"),
        ],
        alerts=[
            DashboardAlert(level="high", title="导师超期未审科研报告", owner="培养管理", due_text="3名导师超过14天"),
            DashboardAlert(level="medium", title="学位论文查重失败待修改", owner="学位管理", due_text="2篇论文待回修"),
            DashboardAlert(level="medium", title="导师关系待确认", owner="学生主数据", due_text="12条记录超过3天"),
        ],
    )


def build_recruitment_workbench() -> RecruitWorkbench:
    return RecruitWorkbench(
        plans=[
            RecruitPlanSummary(plan_name="2026 学术交流周", academic_term="2026 秋", current_stage="资格审核", application_count=1082, interview_group_count=8),
            RecruitPlanSummary(plan_name="2026 工程博士专项", academic_term="2026 秋", current_stage="评分推荐", application_count=744, interview_group_count=6),
            RecruitPlanSummary(plan_name="2026 秋季招生", academic_term="2026 秋", current_stage="预录取", application_count=121, interview_group_count=4),
        ],
        pipeline=[
            {"stage": "报名列表", "count": 1082, "status": "active"},
            {"stage": "资格审核", "count": 1055, "status": "active"},
            {"stage": "材料评分", "count": 744, "status": "active"},
            {"stage": "面试安排", "count": 337, "status": "active"},
            {"stage": "预录取", "count": 121, "status": "attention"},
        ],
        pending_tasks=[
            {"title": "资格审核待处理", "owner": "管理员", "due_text": "今日 18:00"},
            {"title": "评分人分配确认", "owner": "招生秘书", "due_text": "明日 12:00"},
            {"title": "面试组自动分配复核", "owner": "面试组织岗", "due_text": "两日内"},
        ],
    )


def build_student_board() -> StudentLifecycleBoard:
    return StudentLifecycleBoard(
        summary=[
            StudentSummary(student_no="D20240001", full_name="陈一鸣", status="在校", advisor_name="刘亚", team_name="智能制造团队"),
            StudentSummary(student_no="D20240007", full_name="王书宁", status="外出研修", advisor_name="刘亚", team_name="智能制造团队"),
            StudentSummary(student_no="D20230018", full_name="张乐之", status="学位论文阶段", advisor_name="袁野", team_name="数据智能团队"),
        ],
        state_distribution=[
            {"label": "在校", "count": 182},
            {"label": "实习中", "count": 43},
            {"label": "请假中", "count": 8},
            {"label": "答辩阶段", "count": 34},
        ],
    )


def build_training_board() -> TrainingWorkbench:
    return TrainingWorkbench(
        open_tasks=[
            TrainingTask(title="培养方案待学生确认", owner="导师", due_text="剩余 2 天", status="pending"),
            TrainingTask(title="科研报告待审阅", owner="导师", due_text="剩余 1 天", status="warning"),
            TrainingTask(title="外出研修超期未归提醒", owner="学合管理员", due_text="需要今日处置", status="critical"),
        ],
        supervision_rules=[
            {"rule": "入学 15 日内制定培养方案", "owner": "导师", "trigger": "自动待办"},
            {"rule": "学生 7 日内确认培养方案", "owner": "学生", "trigger": "短信+站内信"},
            {"rule": "每学年最多修改 3 次", "owner": "系统控制", "trigger": "规则校验"},
            {"rule": "科研报告逾期 7 日提醒导师", "owner": "系统控制", "trigger": "定时任务"},
        ],
        outbound_study_status=[
            {"status": "审批中", "count": 5},
            {"status": "研修中", "count": 14},
            {"status": "待评估", "count": 3},
        ],
    )


def build_degree_board() -> DegreeWorkbench:
    return DegreeWorkbench(
        thesis_pipeline=[
            {"stage": "查重中", "count": 9},
            {"stage": "盲审中", "count": 8},
            {"stage": "预答辩待安排", "count": 6},
            {"stage": "正式答辩待安排", "count": 11},
            {"stage": "授位审批", "count": 4},
        ],
        committee_tasks=[
            TrainingTask(title="指派 3 位盲审专家", owner="学位秘书", due_text="本周内", status="pending"),
            TrainingTask(title="组织预答辩会议", owner="导师", due_text="剩余 5 天", status="warning"),
            TrainingTask(title="学位委员会审议", owner="委员会秘书", due_text="答辩后 7 日内", status="pending"),
        ],
    )


def build_audit_policies() -> list[dict[str, str]]:
    return [
        {"module": "登录日志", "scope": "登录成功/失败/锁定/异地登录", "retention": "5年"},
        {"module": "操作日志", "scope": "关键实体新增、修改、审批、导出", "retention": "5年"},
        {"module": "同步日志", "scope": "招生/OA/飞书/科研系统同步结果", "retention": "2年"},
        {"module": "通知留痕", "scope": "站内信、短信、邮件、飞书发送回执", "retention": "2年"},
    ]
