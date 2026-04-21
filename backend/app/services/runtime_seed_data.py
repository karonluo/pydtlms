from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any


PERMISSION_GROUPS: dict[str, list[str]] = {
    "platform_admin": ["*"],
    "advisor": ["dashboard:read", "students:read", "training:read", "training:write", "degree:read", "workflow:read", "workflow:write"],
    "secretary": ["dashboard:read", "degree:read", "degree:write", "workflow:read", "workflow:write"],
    "recruit_reviewer": ["dashboard:read", "recruitment:read"],
    "interview_officer": ["dashboard:read", "recruitment:read", "recruitment:write"],
    "hrbp": ["dashboard:read", "students:read", "training:read"],
    "party_affairs": ["dashboard:read", "students:read", "audit:read"],
}


def _fmt_date(value: date) -> str:
    return value.strftime("%Y-%m-%d")


def _fmt_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def build_runtime_seed_state() -> dict[str, Any]:
    now = datetime(2026, 4, 7, 9, 0, 0)

    roles = [
        {"id": 1, "role_code": "platform_admin", "role_name": "平台管理员", "scope_name": "系统治理", "permissions": PERMISSION_GROUPS["platform_admin"]},
        {"id": 2, "role_code": "advisor", "role_name": "导师", "scope_name": "培养与学位", "permissions": PERMISSION_GROUPS["advisor"]},
        {"id": 3, "role_code": "secretary", "role_name": "学位秘书", "scope_name": "学位管理", "permissions": PERMISSION_GROUPS["secretary"]},
        {"id": 4, "role_code": "recruit_reviewer", "role_name": "评分人", "scope_name": "招生管理", "permissions": PERMISSION_GROUPS["recruit_reviewer"]},
        {"id": 5, "role_code": "interview_officer", "role_name": "面试官", "scope_name": "招生管理", "permissions": PERMISSION_GROUPS["interview_officer"]},
        {"id": 6, "role_code": "hrbp", "role_name": "中心HRBP", "scope_name": "跨部门协同", "permissions": PERMISSION_GROUPS["hrbp"]},
        {"id": 7, "role_code": "party_affairs", "role_name": "党群负责人", "scope_name": "学生管理", "permissions": PERMISSION_GROUPS["party_affairs"]},
    ]

    users = [
        {"id": 1, "username": "admin", "full_name": "系统管理员", "role_code": "platform_admin", "department_name": "学科与研究生管理处", "phone_number": "13800000000", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(hours=1))},
        {"id": 2, "username": "liu.ya", "full_name": "刘亚", "role_code": "advisor", "department_name": "智能制造学院", "phone_number": "13800000021", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=1, hours=2))},
        {"id": 3, "username": "yuan.ye", "full_name": "袁野", "role_code": "advisor", "department_name": "工业软件学院", "phone_number": "13800000022", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=1, hours=3))},
        {"id": 4, "username": "xu.sutian", "full_name": "徐素天", "role_code": "advisor", "department_name": "数据智能学院", "phone_number": "13800000023", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=2))},
        {"id": 5, "username": "zhou.qing", "full_name": "周晴", "role_code": "secretary", "department_name": "学位办公室", "phone_number": "13800000024", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(hours=8))},
        {"id": 6, "username": "he.lin", "full_name": "何琳", "role_code": "recruit_reviewer", "department_name": "招生办公室", "phone_number": "13800000025", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=2, hours=4))},
        {"id": 7, "username": "cao.bo", "full_name": "曹博", "role_code": "interview_officer", "department_name": "招生办公室", "phone_number": "13800000026", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=3))},
        {"id": 8, "username": "yang.qin", "full_name": "杨琴", "role_code": "hrbp", "department_name": "人力资源部", "phone_number": "13800000027", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=1, hours=5))},
        {"id": 9, "username": "sun.wei", "full_name": "孙伟", "role_code": "party_affairs", "department_name": "党群工作部", "phone_number": "13800000028", "account_status": "启用", "last_login_at": _fmt_datetime(now - timedelta(days=4))},
    ]

    profiles = {
        item["username"]: {
            "username": item["username"],
            "full_name": item["full_name"],
            "role_name": next(role["role_name"] for role in roles if role["role_code"] == item["role_code"]),
            "department_name": item["department_name"],
            "phone_number": item["phone_number"],
            "email": f"{item['username']}@dtlms.local",
            "theme_color": "#0f4cbd" if item["role_code"] != "advisor" else "#13795b",
        }
        for item in users
    }

    teams = [
        {"id": 1, "team_code": "TEAM-IM-001", "team_name": "智能制造团队", "department_name": "智能制造学院", "discipline_name": "智能制造工程", "lead_advisor_name": "刘亚", "advisor_names": ["刘亚", "何琳"], "research_directions": ["智能制造", "工业互联网", "数字孪生"], "status": "启用", "established_on": "2022-09-01", "description": "面向智能制造、工业互联网与装备数字化方向的人才培养团队。"},
        {"id": 2, "team_code": "TEAM-IS-002", "team_name": "工业软件团队", "department_name": "工业软件学院", "discipline_name": "软件工程", "lead_advisor_name": "袁野", "advisor_names": ["袁野", "曹博"], "research_directions": ["工业软件", "软件工程", "模型驱动开发"], "status": "启用", "established_on": "2021-09-01", "description": "面向工业软件、软件工程与系统架构方向的联合培养团队。"},
        {"id": 3, "team_code": "TEAM-DI-003", "team_name": "数据智能团队", "department_name": "数据智能学院", "discipline_name": "人工智能", "lead_advisor_name": "徐素天", "advisor_names": ["徐素天", "周晴"], "research_directions": ["数据智能", "机器学习", "知识图谱"], "status": "启用", "established_on": "2020-09-01", "description": "面向数据智能、机器学习与知识图谱方向的博士培养团队。"},
        {"id": 4, "team_code": "TEAM-RA-004", "team_name": "机器人应用团队", "department_name": "智能制造学院", "discipline_name": "控制科学与工程", "lead_advisor_name": "刘亚", "advisor_names": ["刘亚"], "research_directions": ["机器人控制", "视觉检测"], "status": "启用", "established_on": "2023-09-01", "description": "聚焦机器人应用与智能检测。"},
        {"id": 5, "team_code": "TEAM-PL-005", "team_name": "平台治理团队", "department_name": "研究生院", "discipline_name": "教育技术", "lead_advisor_name": "袁野", "advisor_names": ["袁野", "周晴"], "research_directions": ["流程治理", "教育数字化"], "status": "筹建", "established_on": "2026-01-10", "description": "聚焦研究生管理平台治理与流程协同。"},
    ]

    student_rows = [
        (1, "D20240001", "陈一鸣", "在校", "刘亚", "智能制造团队", "工程博士", 2024, "13800010001", "中共党员"),
        (2, "D20240002", "林书雅", "在校", "刘亚", "机器人应用团队", "学术博士", 2024, "13800010002", "共青团员"),
        (3, "D20240003", "周启航", "在校", "袁野", "工业软件团队", "工程博士", 2024, "13800010003", "群众"),
        (4, "D20240004", "顾南乔", "在校", "徐素天", "数据智能团队", "学术博士", 2024, "13800010004", "中共预备党员"),
        (5, "D20230005", "赵嘉霖", "实习中", "袁野", "工业软件团队", "工程博士", 2023, "13800010005", "中共党员"),
        (6, "D20230006", "沈知遥", "实习中", "徐素天", "数据智能团队", "工程博士", 2023, "13800010006", "共青团员"),
        (7, "D20230007", "王书宁", "外出研修", "刘亚", "智能制造团队", "学术博士", 2023, "13800010007", "共青团员"),
        (8, "D20230008", "贺景川", "外出研修", "徐素天", "数据智能团队", "工程博士", 2023, "13800010008", "群众"),
        (9, "D20230009", "许安然", "请假中", "袁野", "工业软件团队", "学术博士", 2023, "13800010009", "群众"),
        (10, "D20220010", "张乐之", "学位论文阶段", "袁野", "工业软件团队", "工程博士", 2022, "13800010010", "群众"),
        (11, "D20220011", "赵嘉禾", "学位论文阶段", "徐素天", "数据智能团队", "工程博士", 2022, "13800010011", "中共党员"),
        (12, "D20220012", "顾清越", "学位论文阶段", "刘亚", "机器人应用团队", "学术博士", 2022, "13800010012", "中共预备党员"),
        (13, "D20250013", "宋知行", "在校", "刘亚", "智能制造团队", "工程博士", 2025, "13800010013", "共青团员"),
        (14, "D20250014", "江若溪", "在校", "徐素天", "数据智能团队", "学术博士", 2025, "13800010014", "群众"),
        (15, "D20250015", "孟书恒", "在校", "袁野", "平台治理团队", "工程博士", 2025, "13800010015", "中共党员"),
        (16, "D20250016", "魏知远", "在校", "刘亚", "机器人应用团队", "学术博士", 2025, "13800010016", "共青团员"),
        (17, "D20240017", "韩嘉宁", "在校", "袁野", "工业软件团队", "学术博士", 2024, "13800010017", "群众"),
        (18, "D20240018", "陆承泽", "在校", "徐素天", "数据智能团队", "工程博士", 2024, "13800010018", "中共党员"),
    ]
    students = [
        {"id": row[0], "student_no": row[1], "full_name": row[2], "status": row[3], "advisor_name": row[4], "team_name": row[5], "degree_type": row[6], "enrollment_year": row[7], "phone_number": row[8], "political_status": row[9]}
        for row in student_rows
    ]

    recruitment_plans = [
        {"id": 1, "plan_name": "2026 秋季博士招生", "academic_year": "2026", "semester": "秋", "plan_description": "面向学术型博士申请人，重点关注基础研究能力与科研潜力。", "current_stage": "报名配置", "target_quota": 0, "interview_group_count": 0, "is_open": True, "brochure_image_url": "/portal-brochures/doctoral-fall.svg"},
        {"id": 2, "plan_name": "2026 工程博士专项", "academic_year": "2026", "semester": "秋", "plan_description": "面向工程实践与产业问题导向申请人，强调场景落地与交叉协同。", "current_stage": "报名配置", "target_quota": 0, "interview_group_count": 0, "is_open": True, "brochure_image_url": "/portal-brochures/engineering-track.svg"},
        {"id": 3, "plan_name": "2026 智能制造联合培养", "academic_year": "2026", "semester": "秋", "plan_description": "聚焦智能制造方向联合培养，适合具备制造业、自动化、AI 背景的申请人。", "current_stage": "报名配置", "target_quota": 0, "interview_group_count": 0, "is_open": True, "brochure_image_url": "/portal-brochures/intelligent-manufacturing.svg"},
        {"id": 4, "plan_name": "2025 春季补录", "academic_year": "2025", "semester": "春", "plan_description": "针对上一轮缺口进行补录，适合已具备完整材料并可快速进入复核的申请人。", "current_stage": "报名配置", "target_quota": 0, "interview_group_count": 0, "is_open": True, "brochure_image_url": "/portal-brochures/spring-supplement.svg"},
    ]

    application_rows = [
        (1, 1, "ZSLQSP202604070001", "吴启程", "东南大学", "硕士", "智能制造", "材料齐全", "同意录取", "何琳", 91.0),
        (2, 1, "ZSLQSP202604070002", "沈清禾", "同济大学", "硕士", "机器人控制", "材料齐全", "预录取", "何琳", 88.5),
        (3, 1, "ZSLQSP202604070003", "顾明睿", "华中科技大学", "硕士", "工业互联网", "材料齐全", "面试完成", "何琳", 85.0),
        (4, 1, "ZSLQSP202604070004", "周亦凡", "哈尔滨工业大学", "硕士", "视觉检测", "材料齐全", "面试待安排", "曹博", None),
        (5, 1, "ZSLQSP202604070005", "李静姝", "浙江大学", "硕士", "数据智能", "材料齐全", "材料评分中", "何琳", 82.0),
        (6, 1, "ZSLQSP202604070006", "陈思远", "北京航空航天大学", "硕士", "数字孪生", "待补材料", "报名已提交", None, None),
        (7, 2, "ZSLQSP202604070007", "赵安歌", "南京大学", "硕士", "工业软件", "材料齐全", "资格审核通过", "何琳", None),
        (8, 2, "ZSLQSP202604070008", "林知夏", "上海交通大学", "硕士", "软件工程", "材料齐全", "同意录取", "何琳", 93.0),
        (9, 2, "ZSLQSP202604070009", "钱北辰", "西安交通大学", "硕士", "模型驱动开发", "材料齐全", "不录取", "曹博", 73.0),
        (10, 2, "ZSLQSP202604070010", "韩知遇", "天津大学", "硕士", "工业数据治理", "材料齐全", "预录取", "何琳", 86.0),
        (11, 3, "ZSLQSP202604070011", "朱安宁", "武汉大学", "硕士", "知识图谱", "材料齐全", "面试待安排", "曹博", None),
        (12, 3, "ZSLQSP202604070012", "谢明远", "北京理工大学", "硕士", "机器学习", "已退回修改", "报名已提交", None, None),
    ]
    recruitment_applications = [
        {"id": row[0], "plan_id": row[1], "business_key": row[2], "candidate_no": row[2], "student_name": row[3], "graduation_school": row[4], "highest_degree": row[5], "intended_field": row[6], "material_status": row[7], "application_status": row[8], "reviewer_name": row[9], "final_score": row[10]}
        for row in application_rows
    ]
    second_choice_values = [
        "机器学习",
        "工业互联网",
        "知识图谱",
        "数据智能",
        "数字孪生",
        "软件工程",
        "工业数据治理",
        "机器人控制",
        "视觉检测",
        "模型驱动开发",
        "智能制造",
        "大模型应用",
    ]
    political_values = ["中共党员", "共青团员", "群众", "中共预备党员"]
    for index, item in enumerate(recruitment_applications, start=1):
        item.update(
            {
                "review_round": "2026 秋季第一轮" if item["plan_id"] in {1, 2} else "2026 秋季第二轮",
                "first_choice": item["intended_field"],
                "second_choice": second_choice_values[(index - 1) % len(second_choice_values)],
                "gender": "男" if index % 2 else "女",
                "political_status": political_values[(index - 1) % len(political_values)],
                "marital_status": "未婚",
                "religious_belief": "无",
                "native_place": ["江苏南京", "上海浦东", "湖北武汉", "浙江杭州"][index % 4],
                "phone_number": f"1390002{index:04d}",
                "email": f"candidate{index:02d}@mail.example.com",
                "mailing_address": f"上海市浦东新区临港大道 {100 + index} 号",
                "id_type": "居民身份证",
                "id_number": f"31010119950{index:02d}1234",
                "undergraduate_school": item["graduation_school"],
                "accept_adjustment": "是" if index % 3 else "否",
                "undergraduate_average_score": f"{85 + index % 8}",
                "undergraduate_gpa": f"{3.2 + (index % 5) * 0.1:.1f}",
                "undergraduate_rank": f"{index}/{40 + index}",
                "undergraduate_major": item["intended_field"],
                "graduate_average_score": f"{86 + index % 7}",
                "graduate_gpa": f"{3.3 + (index % 4) * 0.1:.1f}",
                "graduate_rank": f"{index}/{24 + index}",
                "graduate_major": item["intended_field"],
                "intended_advisor_name": ["刘亚", "袁野", "徐素天"][index % 3],
                "discovery_channel": "实验室官网 / 学术宣讲会",
                "graduate_school": ["上海交通大学", "同济大学", "浙江大学", "南京大学"][index % 4],
                "overseas_university_name": None,
                "overseas_master_university_name": None,
                "self_evaluation": "具备较强的科研热情、工程实现能力和跨团队协作意识。",
                "applied_at": _fmt_datetime(now - timedelta(days=index, hours=2)),
                "research_problem": "希望围绕通用人工智能在垂直领域中的可靠落地问题开展研究。",
                "research_status_analysis": "当前研究已在通用能力上取得突破，但在可解释性、数据效率和行业适配方面仍有明显局限。",
                "research_impact": "若问题得到解决，将显著提升 AI 技术普及效率并降低行业智能化成本。",
                "ai_society_impact": "AI 将优先在知识密集型决策支持、教育科研和工业协同场景中持续改变社会运行方式。",
                "dissenting_view": "不同意“更大参数规模一定带来更强行业效果”的绝对化判断。",
                "family_info": "家庭成员支持继续深造，具备稳定异地学习条件。",
                "education_experience": "本科与硕士阶段均围绕人工智能、自动化或软件工程方向系统学习。",
                "practice_experience": "参与过科研项目、企业实习和算法系统原型开发。",
                "personal_statement_text": "希望在博士阶段系统推进基础研究与场景化应用结合。",
                "student_activity_experience": "担任过学生干部并组织学术交流活动。",
                "personal_statement_attachment": f"/attachments/recruitment/{item['candidate_no']}/personal-statement.pdf",
                "material_list_attachment": f"/attachments/recruitment/{item['candidate_no']}/materials.zip",
                "supplementary_profile": "具备持续学习与自我驱动能力。",
            }
        )

    training_plans = []
    for student in students:
        training_plans.append(
            {
                "id": student["id"],
                "student_no": student["student_no"],
                "student_name": student["full_name"],
                "advisor_name": student["advisor_name"],
                "version_no": "v1.0" if student["enrollment_year"] >= 2024 else "v2.0",
                "report_cycle": "月度" if student["enrollment_year"] >= 2024 else "季度",
                "plan_status": "执行中" if student["status"] != "请假中" else "待学生确认",
                "scientific_goal": f"围绕{student['team_name']}承担课题，形成阶段性论文与系统原型。",
                "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。",
            }
        )

    report_rows = [
        (1, "KYBGSY202604070001", "D20240001", "陈一鸣", "2026Q1", "已通过", "刘亚", 92.0, "完成产线调度算法优化与仿真验证。"),
        (2, "KYBGSY202604070002", "D20240002", "林书雅", "2026Q1", "待导师审阅", "刘亚", None, "完成机器人视觉检测数据采集。"),
        (3, "KYBGSY202604070003", "D20240003", "周启航", "2026Q1", "已通过", "袁野", 88.0, "完成工业软件模块设计与接口联调。"),
        (4, "KYBGSY202604070004", "D20240004", "顾南乔", "2026Q1", "退回修改", "徐素天", 76.0, "实验结果不足，需要补充对比分析。"),
        (5, "KYBGSY202604070005", "D20230005", "赵嘉霖", "2026Q1", "已通过", "袁野", 90.0, "完成企业实习阶段需求分析与文档输出。"),
        (6, "KYBGSY202604070006", "D20230006", "沈知遥", "2026Q1", "待导师审阅", "徐素天", None, "完成知识图谱抽取规则验证。"),
        (7, "KYBGSY202604070007", "D20250013", "宋知行", "2026Q1", "待导师审阅", "刘亚", None, "完成入组初期课题调研和综述整理。"),
        (8, "KYBGSY202604070008", "D20250014", "江若溪", "2026Q1", "已通过", "徐素天", 89.0, "完成大模型辅助标注流程验证。"),
    ]
    scientific_reports = [
        {"id": row[0], "business_key": row[1], "student_no": row[2], "student_name": row[3], "period_label": row[4], "report_status": row[5], "reviewer_name": row[6], "review_score": row[7], "summary": row[8]}
        for row in report_rows
    ]

    outbound_rows = [
        (1, "WCYXSP202604070001", "D20230007", "王书宁", "刘亚", "联合培养", "新加坡国立大学", "2026-03-01", "2026-08-31", "已批准", "完成联合培养课题与月度交流汇报。"),
        (2, "WCYXSP202604070002", "D20230008", "贺景川", "徐素天", "访学交流", "香港科技大学", "2026-02-15", "2026-07-30", "审批中", "完成知识图谱跨语种研究。"),
        (3, "WCYXSP202604070003", "D20240003", "周启航", "袁野", "企业研修", "中控技术研究院", "2026-05-01", "2026-07-31", "已驳回", "研修目标与阶段任务需进一步明确。"),
        (4, "WCYXSP202604070004", "D20250015", "孟书恒", "袁野", "学术会议", "深圳", "2026-05-18", "2026-05-22", "审批中", "参加流程治理与数字教育论坛。"),
    ]
    outbound_studies = [
        {"id": row[0], "business_key": row[1], "student_no": row[2], "student_name": row[3], "advisor_name": row[4], "study_type": row[5], "destination": row[6], "start_date": row[7], "end_date": row[8], "approval_status": row[9], "expected_outcome": row[10]}
        for row in outbound_rows
    ]

    thesis_rows = [
        (1, "SWSQSP202604070001", "D20220010", "张乐之", "袁野", "面向工业软件的流程协同引擎设计与实现", 12.5, "盲审通过", "已通过", "正式答辩完成", "待正式答辩"),
        (2, "SWSQSP202604070002", "D20220011", "赵嘉禾", "徐素天", "知识图谱驱动的科研过程智能分析方法研究", 15.2, "查重通过", "进行中", "待安排", "授位审批中"),
        (3, "SWSQSP202604070003", "D20220012", "顾清越", "刘亚", "机器人视觉检测中的多模态融合方法研究", 18.0, "退回修改", "未通过", "未进入", "未授位"),
        (4, "SWSQSP202604070004", "D20230006", "沈知遥", "徐素天", "面向教育场景的大模型知识对齐与应用研究", 9.8, "待查重", "未送审", "未进入", "待申请"),
    ]
    theses = [
        {"id": row[0], "business_key": row[1], "student_no": row[2], "student_name": row[3], "advisor_name": row[4], "title": row[5], "plagiarism_rate": row[6], "thesis_status": row[7], "blind_review_status": row[8], "defense_status": row[9], "degree_status": row[10]}
        for row in thesis_rows
    ]

    thesis_reviews = [
        {"id": 1, "thesis_id": 1, "thesis_title": thesis_rows[0][5], "expert_name": "何振华", "review_score": 86.0, "review_status": "已通过", "review_comment": "研究目标明确，工程实现完整。"},
        {"id": 2, "thesis_id": 1, "thesis_title": thesis_rows[0][5], "expert_name": "潘雪松", "review_score": 88.0, "review_status": "已通过", "review_comment": "实验设计充分，建议补充性能对比。"},
        {"id": 3, "thesis_id": 2, "thesis_title": thesis_rows[1][5], "expert_name": "杨知行", "review_score": None, "review_status": "待反馈", "review_comment": None},
        {"id": 4, "thesis_id": 3, "thesis_title": thesis_rows[2][5], "expert_name": "陈明哲", "review_score": 70.0, "review_status": "需修改", "review_comment": "理论分析不充分，需要补强实验结果。"},
    ]

    audit_policies = [
        {"id": 1, "item": "登录与鉴权审计", "policy": "记录登录成功、失败、退出与令牌刷新。", "status": "启用"},
        {"id": 2, "item": "流程审批留痕", "policy": "所有流程动作、意见、节点变更必须留痕。", "status": "启用"},
        {"id": 3, "item": "主数据变更审计", "policy": "学生、团队、角色与字典变更需记录操作日志。", "status": "启用"},
        {"id": 4, "item": "敏感数据导出控制", "policy": "导出包含联系方式与身份信息时需保留审计记录。", "status": "启用"},
    ]

    integrations = [
        {"id": 1, "name": "招生系统主数据同步", "direction": "主数据导入 / 录取回传", "cadence": "实时 + 每日对账", "status": "正常", "owner": "系统管理员"},
        {"id": 2, "name": "实验室 OA 事件同步", "direction": "考勤 / 门禁 / 请假同步", "cadence": "实时事件 + 定时补偿", "status": "正常", "owner": "杨琴"},
        {"id": 3, "name": "飞书待办推送", "direction": "待办通知 / 审批提醒 / 回执", "cadence": "实时", "status": "告警", "owner": "周晴"},
    ]

    operation_logs = [
        {"id": 1, "operated_at": _fmt_datetime(now - timedelta(days=1)), "operator_username": "admin", "module_name": "系统治理", "entity_name": "角色权限", "entity_id": "role-2", "action": "授权", "result": "success", "summary": "为导师角色补充流程处理权限。"},
        {"id": 2, "operated_at": _fmt_datetime(now - timedelta(hours=10)), "operator_username": "liu.ya", "module_name": "培养管理", "entity_name": "科研报告", "entity_id": "KYBGSY202604070001", "action": "审阅通过", "result": "success", "summary": "导师完成陈一鸣科研报告审阅。"},
        {"id": 3, "operated_at": _fmt_datetime(now - timedelta(hours=6)), "operator_username": "zhou.qing", "module_name": "学位管理", "entity_name": "论文主档", "entity_id": "SWSQSP202604070002", "action": "复核", "result": "success", "summary": "学位秘书推进论文送审流程。"},
    ]

    sync_logs = [
        {"id": 1, "source_system": "招生系统", "target_system": "DTLMS", "sync_status": "success", "record_count": 36, "executed_at": _fmt_datetime(now - timedelta(hours=4)), "failure_reason": None},
        {"id": 2, "source_system": "飞书", "target_system": "DTLMS", "sync_status": "failed", "record_count": 4, "executed_at": _fmt_datetime(now - timedelta(hours=3)), "failure_reason": "回执接口超时，等待补偿重试。"},
        {"id": 3, "source_system": "实验室OA", "target_system": "DTLMS", "sync_status": "success", "record_count": 58, "executed_at": _fmt_datetime(now - timedelta(hours=2)), "failure_reason": None},
    ]

    counters = {
        "students": len(students),
        "recruitment_plans": len(recruitment_plans),
        "recruitment_applications": len(recruitment_applications),
        "training_plans": len(training_plans),
        "scientific_reports": len(scientific_reports),
        "outbound_studies": len(outbound_studies),
        "theses": len(theses),
        "thesis_reviews": len(thesis_reviews),
        "roles": len(roles),
        "system_users": len(users),
        "audit_policies": len(audit_policies),
        "integrations": len(integrations),
        "operation_logs": len(operation_logs),
        "sync_logs": len(sync_logs),
        "workflow_tasks": 0,
        "teams": len(teams),
        "portal_students": 0,
    }

    return {
        "counters": counters,
        "profiles": profiles,
        "students": students,
        "teams": teams,
        "recruitment_plans": recruitment_plans,
        "recruitment_applications": recruitment_applications,
        "training_plans": training_plans,
        "scientific_reports": scientific_reports,
        "outbound_studies": outbound_studies,
        "theses": theses,
        "thesis_reviews": thesis_reviews,
        "roles": roles,
        "system_users": users,
        "audit_policies": audit_policies,
        "integrations": integrations,
        "operation_logs": operation_logs,
        "sync_logs": sync_logs,
        "workflow_tasks": [],
        "portal_students": [],
    }
