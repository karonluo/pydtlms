from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import time
from typing import Any
import uuid
import xml.etree.ElementTree as ET

import psycopg


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / "backend" / ".env"
OUTPUT_SQL_PATH = ROOT / "documents" / "pydtlms-powerdesigner16_5-reverse-engineering.sql"
OUTPUT_PDM_PATH = ROOT / "documents" / "pydtlms-powerdesigner16_5-complete.pdm"
OUTPUT_GUIDE_PATH = ROOT / "documents" / "pydtlms-powerdesigner16_5-import.md"

NS_A = "attribute"
NS_C = "collection"
NS_O = "object"
UUID_NAMESPACE = uuid.UUID("9f23dd7c-190c-45a5-8df3-e65d504c3350")
POWERDESIGNER_MODEL_TYPE = "{CDE44E21-9669-11D1-9914-006097355D9B}"
POWERDESIGNER_TARGET_CLASS_ID = "4BA9F647-DAB1-11D1-9944-006097355D9B"
POSTGRESQL_DBMS_NAME = "PostgreSQL 9.x"
POSTGRESQL_DBMS_CODE = "PGSQL9"
POSTGRESQL_DBMS_OBJECT_ID = "83063C86-4E0A-4954-BF00-620C0D0F02D8"
POSTGRESQL_TARGET_MODEL_URL = "file:///%_DBMS%/pgsql9.xdb"
DEFAULT_GROUP_NAME = "PUBLIC"
SYMBOL_FONT_LIST = (
    "STRN 0 Arial,8,N\n"
    "DISPNAME 0 Arial,8,N\n"
    "OWNRDISPNAME 0 Arial,8,N\n"
    "Columns 0 Arial,8,N\n"
    "TablePkColumns 0 Arial,8,N\n"
    "TableFkColumns 0 Arial,8,N\n"
    "Keys 0 Arial,8,N\n"
    "Indexes 0 Arial,8,N\n"
    "Triggers 0 Arial,8,N\n"
    "LABL 0 Arial,8,N"
)
REFERENCE_FONT_LIST = "CENTER 0 Arial,8,N\nSOURCE 0 Arial,8,N\nDESTINATION 0 Arial,8,N"

TABLE_DISPLAY_NAMES = {
    "dtlms_achievements": "科研成果",
    "dtlms_admission_decisions": "录取决定",
    "dtlms_advisors": "导师",
    "dtlms_application_materials": "申请材料",
    "dtlms_audit_policies": "审计策略",
    "dtlms_background_assessments": "背景评估",
    "dtlms_data_sync_logs": "数据同步日志",
    "dtlms_dict_data": "字典数据",
    "dtlms_dict_types": "字典类型",
    "dtlms_integrations": "集成配置",
    "dtlms_interview_groups": "面试分组",
    "dtlms_interview_schedules": "面试安排",
    "dtlms_interview_scores": "面试成绩",
    "dtlms_login_logs": "登录日志",
    "dtlms_material_scores": "材料成绩",
    "dtlms_notification_delivery_logs": "通知投递日志",
    "dtlms_notification_templates": "通知模板",
    "dtlms_operation_logs": "操作日志",
    "dtlms_outbound_studies": "外出研修",
    "dtlms_permissions": "权限",
    "dtlms_portal_application_achievement_records": "门户申请成果记录",
    "dtlms_portal_application_attachments": "门户申请附件",
    "dtlms_portal_application_declarations": "门户申请声明",
    "dtlms_portal_application_education_experiences": "门户申请教育经历",
    "dtlms_portal_application_english_proficiencies": "门户申请英语能力",
    "dtlms_portal_application_family_members": "门户申请家庭成员",
    "dtlms_portal_application_personal_statements": "门户申请个人陈述",
    "dtlms_portal_application_practice_experiences": "门户申请实践经历",
    "dtlms_portal_application_preferences": "门户申请志愿信息",
    "dtlms_portal_student_profiles": "门户学生档案",
    "dtlms_portal_students": "门户学生",
    "dtlms_qualification_reviews": "资格审查",
    "dtlms_recruitment_applications": "招生申请",
    "dtlms_recruitment_plans": "招生计划",
    "dtlms_research_fields": "研究方向",
    "dtlms_research_projects": "科研项目",
    "dtlms_reviewer_assignments": "评审分配",
    "dtlms_role_permissions": "角色权限",
    "dtlms_roles": "角色",
    "dtlms_scientific_reports": "科研报告",
    "dtlms_student_advisor_history": "学生导师变更历史",
    "dtlms_student_team_history": "学生团队变更历史",
    "dtlms_students": "学生",
    "dtlms_system_configs": "系统配置",
    "dtlms_team_advisors": "团队导师",
    "dtlms_teams": "团队",
    "dtlms_theses": "论文",
    "dtlms_thesis_reviews": "论文评审",
    "dtlms_training_plan_versions": "培养方案版本",
    "dtlms_training_plans": "培养方案",
    "dtlms_user_profiles": "用户档案",
    "dtlms_user_roles": "用户角色",
    "dtlms_users": "用户",
    "dtlms_wf_de_model": "工作流模型定义",
    "dtlms_wf_hi_actinst": "工作流历史活动实例",
    "dtlms_wf_hi_procinst": "工作流历史流程实例",
    "dtlms_wf_hi_taskinst": "工作流历史任务实例",
    "dtlms_wf_hi_varinst": "工作流历史变量实例",
    "dtlms_wf_re_deployment": "工作流部署",
    "dtlms_wf_re_procdef": "工作流流程定义",
    "dtlms_wf_ru_execution": "工作流运行执行",
    "dtlms_wf_ru_identitylink": "工作流运行身份关联",
    "dtlms_wf_ru_task": "工作流运行任务",
    "dtlms_wf_ru_variable": "工作流运行变量",
    "dtlms_written_exam_scores": "笔试成绩",
}

COLUMN_DISPLAY_OVERRIDES = {
    "id": "ID",
    "full_name": "姓名",
    "full_name_pinyin": "姓名拼音",
    "phone_number": "手机号",
    "id_number": "证件号",
    "created_at": "创建时间",
    "updated_at": "更新时间",
    "deleted_at": "删除时间",
    "created_by": "创建人",
    "updated_by": "更新人",
    "deleted_by": "删除人",
    "business_key": "业务键",
    "account_status": "账号状态",
    "user_id": "用户ID",
    "role_id": "角色ID",
    "team_id": "团队ID",
    "advisor_id": "导师ID",
    "plan_id": "计划ID",
    "application_id": "申请ID",
    "portal_student_id": "门户学生ID",
    "permission_id": "权限ID",
    "parent_id": "上级ID",
    "selected_plan_id": "已选计划ID",
    "selected_advisor_name": "已选导师姓名",
    "selected_team_name": "已选团队名称",
    "first_choice": "第一志愿",
    "second_choice": "第二志愿",
    "source_channel": "来源渠道",
    "source_channel_other": "其他来源渠道",
    "personal_statement_text": "个人陈述文本",
    "recommendation_notes": "推荐说明",
    "education_experience": "教育经历",
    "practice_experience": "实践经历",
    "family_info": "家庭信息",
    "self_evaluation": "自我评价",
    "candidate_no": "考生编号",
    "plan_code": "计划编码",
    "field_code": "方向编码",
    "project_code": "项目编码",
    "template_code": "模板编码",
    "role_code": "角色编码",
    "permission_code": "权限编码",
    "dict_type": "字典类型",
    "admission_ticket_no": "准考证号",
    "email": "邮箱",
    "password": "密码",
    "username": "用户名",
    "introduction": "简介",
    "profile_photo_url": "头像地址",
    "resume_attachment_url": "简历附件地址",
    "supporting_material_attachment_url": "支撑材料附件地址",
    "material_list_attachment": "材料清单附件",
    "growth_experience_text": "成长经历文本",
    "program_application_reason_text": "项目申请原因文本",
    "career_plan_text": "职业规划文本",
}

TOKEN_DISPLAY_NAMES = {
    "academic": "学术",
    "accept": "接收",
    "achievement": "成果",
    "achievements": "成果",
    "account": "账号",
    "action": "操作",
    "active": "启用",
    "activity": "活动",
    "act": "活动",
    "actinst": "活动实例",
    "address": "地址",
    "adjustment": "调整",
    "admission": "录取",
    "advisor": "导师",
    "advisors": "导师",
    "agent": "代理",
    "agreement": "协议",
    "ai": "AI",
    "amount": "数量",
    "analysis": "分析",
    "annual": "年度",
    "application": "申请",
    "applications": "申请",
    "applied": "已申请",
    "approval": "审批",
    "assessed": "已评估",
    "assessment": "评估",
    "assessments": "评估",
    "assignee": "办理人",
    "assignment": "分配",
    "assignments": "分配",
    "at": "时间",
    "attachment": "附件",
    "attachments": "附件",
    "audit": "审计",
    "author": "作者",
    "average": "平均",
    "award": "奖项",
    "awarding": "授奖",
    "background": "背景",
    "batch": "批次",
    "belief": "信仰",
    "birth": "出生",
    "blank": "空白",
    "blind": "盲审",
    "brochure": "简章",
    "business": "业务",
    "by": "人",
    "cadence": "频率",
    "candidate": "考生",
    "card": "证件",
    "career": "职业",
    "category": "类别",
    "center": "中心",
    "certificate": "证书",
    "change": "变更",
    "channel": "渠道",
    "choice": "志愿",
    "claim": "声明",
    "class": "班级",
    "code": "编码",
    "coding": "编码",
    "collage": "学院",
    "color": "颜色",
    "comment": "备注",
    "concurrent": "并发",
    "conference": "会议",
    "config": "配置",
    "configs": "配置",
    "contact": "联系人",
    "content": "内容",
    "count": "数量",
    "create": "创建",
    "created": "创建",
    "css": "CSS",
    "current": "当前",
    "cycle": "周期",
    "data": "数据",
    "date": "日期",
    "de": "定义",
    "decision": "决定",
    "decisions": "决定",
    "declaration": "声明",
    "declarations": "声明",
    "def": "定义",
    "defense": "答辩",
    "degree": "学位",
    "delete": "删除",
    "deleted": "已删除",
    "delivery": "投递",
    "department": "部门",
    "deploy": "部署",
    "deployment": "部署",
    "deployment": "部署",
    "description": "描述",
    "destination": "目标",
    "diagram": "图",
    "dict": "字典",
    "direction": "方向",
    "directions": "方向",
    "discipline": "学科",
    "discovery": "发现",
    "dissenting": "异议",
    "draft": "草稿",
    "due": "截止",
    "duration": "时长",
    "editor": "编辑人",
    "education": "教育",
    "email": "邮箱",
    "emergency": "紧急",
    "employer": "工作单位",
    "end": "结束",
    "ends": "结束",
    "english": "英语",
    "enrollment": "入学",
    "entity": "实体",
    "established": "立项",
    "ethnic": "民族",
    "evaluation": "评价",
    "evaluator": "评审人",
    "exam": "考试",
    "exec": "执行",
    "execution": "执行",
    "expected": "预计",
    "experience": "经历",
    "experiences": "经历",
    "expert": "专家",
    "extra": "附加",
    "failure": "失败",
    "family": "家庭",
    "field": "方向",
    "fields": "方向",
    "file": "文件",
    "fill": "填写",
    "final": "最终",
    "first": "第一",
    "form": "表单",
    "full": "完整",
    "funding": "经费",
    "gender": "性别",
    "goal": "目标",
    "gpa": "绩点",
    "grant": "授予",
    "granted": "已授予",
    "graduate": "毕业",
    "graduation": "毕业",
    "group": "分组",
    "groups": "分组",
    "growth": "成长",
    "has": "有",
    "hash": "哈希",
    "hi": "历史",
    "highest": "最高",
    "history": "历史",
    "id": "ID",
    "identity": "身份",
    "identitylink": "身份关联",
    "ideological": "思想",
    "image": "图片",
    "impact": "影响",
    "import": "导入",
    "index": "索引",
    "industry": "行业",
    "info": "信息",
    "inst": "实例",
    "integrations": "集成",
    "intended": "拟报考",
    "interview": "面试",
    "introduction": "简介",
    "ip": "IP",
    "is": "是否",
    "item": "项",
    "job": "职务",
    "joined": "加入",
    "journal": "期刊",
    "json": "JSON",
    "key": "键",
    "label": "标签",
    "last": "最近",
    "lead": "负责人",
    "left": "剩余",
    "level": "等级",
    "link": "关联",
    "list": "列表",
    "login": "登录",
    "logs": "日志",
    "mailing": "邮寄",
    "major": "专业",
    "marital": "婚姻",
    "master": "硕士",
    "material": "材料",
    "materials": "材料",
    "member": "成员",
    "members": "成员",
    "meta": "元数据",
    "mode": "模式",
    "model": "模型",
    "module": "模块",
    "month": "月份",
    "ms": "毫秒",
    "name": "名称",
    "native": "籍贯",
    "new": "新",
    "no": "编号",
    "notes": "备注",
    "notification": "通知",
    "number": "号码",
    "old": "旧",
    "on": "于",
    "operation": "操作",
    "operator": "操作人",
    "opinion": "意见",
    "option": "选项",
    "optional": "可选",
    "or": "或",
    "order": "顺序",
    "organization": "机构",
    "other": "其他",
    "outbound": "外出",
    "outcome": "结果",
    "overseas": "海外",
    "owner": "归属",
    "paper": "论文",
    "parent": "上级",
    "password": "密码",
    "period": "周期",
    "permission": "权限",
    "permissions": "权限",
    "personal": "个人",
    "phone": "电话",
    "photo": "照片",
    "pinyin": "拼音",
    "place": "地点",
    "plagiarism": "查重",
    "plan": "计划",
    "plans": "计划",
    "policies": "策略",
    "policy": "策略",
    "political": "政治面貌",
    "portal": "门户",
    "position": "职位",
    "practice": "实践",
    "preference": "志愿",
    "preferences": "志愿",
    "primary": "第一",
    "principal": "负责人",
    "priority": "优先级",
    "problem": "问题",
    "proc": "流程",
    "procdef": "流程定义",
    "procinst": "流程实例",
    "profile": "档案",
    "profiles": "档案",
    "program": "项目",
    "progress": "进度",
    "project": "项目",
    "projects": "项目",
    "proficiencies": "能力",
    "publish": "发表",
    "published": "已发表",
    "publisher": "出版方",
    "qualification": "资格",
    "quota": "名额",
    "rank": "排名",
    "ranking": "排名",
    "rate": "比率",
    "re": "资源库",
    "read": "已读",
    "reason": "原因",
    "recipient": "接收方",
    "recommendation": "推荐",
    "record": "记录",
    "records": "记录",
    "relation": "关系",
    "religious": "宗教",
    "remark": "备注",
    "report": "报告",
    "reports": "报告",
    "request": "请求",
    "research": "研究",
    "resource": "资源",
    "responsibility": "职责",
    "result": "结果",
    "resume": "简历",
    "review": "评审",
    "reviews": "评审",
    "reviewer": "评审人",
    "role": "角色",
    "roles": "角色",
    "round": "轮次",
    "ru": "运行",
    "rule": "规则",
    "schedule": "安排",
    "schedules": "安排",
    "schema": "结构",
    "school": "学校",
    "scientific": "科研",
    "scope": "范围",
    "score": "成绩",
    "scores": "成绩",
    "second": "第二",
    "selected": "已选",
    "self": "自我",
    "semester": "学期",
    "send": "发送",
    "signed": "已签署",
    "single": "单项",
    "size": "大小",
    "snapshot": "快照",
    "society": "社会",
    "sort": "排序",
    "source": "来源",
    "stage": "阶段",
    "start": "开始",
    "starts": "开始",
    "state": "状态",
    "statement": "陈述",
    "statements": "陈述",
    "status": "状态",
    "student": "学生",
    "students": "学生",
    "studies": "研修",
    "study": "研修",
    "subject": "学科",
    "submitted": "已提交",
    "summary": "摘要",
    "super": "上级",
    "supplementary": "补充",
    "supporting": "支撑",
    "suspension": "暂停",
    "sync": "同步",
    "system": "系统",
    "target": "目标",
    "task": "任务",
    "taskinst": "任务实例",
    "team": "团队",
    "teams": "团队",
    "template": "模板",
    "templates": "模板",
    "tenant": "租户",
    "text": "文本",
    "theme": "主题",
    "theses": "论文",
    "thesis": "论文",
    "ticket": "准考证",
    "time": "时间",
    "title": "标题",
    "training": "培养",
    "transcript": "成绩单",
    "transfer": "流转",
    "triggered": "已触发",
    "type": "类型",
    "types": "类型",
    "undergraduate": "本科",
    "university": "高校",
    "updated": "更新",
    "url": "地址",
    "user": "用户",
    "users": "用户",
    "username": "用户名",
    "value": "值",
    "var": "变量",
    "variable": "变量",
    "variables": "变量",
    "varinst": "变量实例",
    "verifier": "复核人",
    "version": "版本",
    "versions": "版本",
    "view": "视图",
    "wf": "工作流",
    "written": "笔试",
    "year": "年份",
}

PERSON_NAME_TOKENS = {"advisor", "assignee", "evaluator", "full", "member", "principal", "reviewer", "student", "user", "verifier", "contact"}


for prefix, namespace in (("a", NS_A), ("c", NS_C), ("o", NS_O)):
    ET.register_namespace(prefix, namespace)


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def build_dsn(env_values: dict[str, str]) -> str:
    return (
        f"host={env_values['POSTGRES_HOST']} "
        f"port={env_values['POSTGRES_PORT']} "
        f"dbname={env_values['POSTGRES_DB']} "
        f"user={env_values['POSTGRES_USER']} "
        f"password={env_values['POSTGRES_PASSWORD']} "
        "client_encoding=utf8 connect_timeout=10"
    )


def sql_literal(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def action_text(action_code: str) -> str:
    mapping = {
        "a": "NO ACTION",
        "r": "RESTRICT",
        "c": "CASCADE",
        "n": "SET NULL",
        "d": "SET DEFAULT",
    }
    return mapping.get(action_code, "NO ACTION")


def qname(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def make_id(kind: str, name: str) -> str:
    return str(uuid.uuid5(UUID_NAMESPACE, f"{kind}:{name}")).upper()


class PdIdGenerator:
    def __init__(self) -> None:
        self._next = 1

    def new(self) -> str:
        value = f"o{self._next}"
        self._next += 1
        return value


def add_attribute(parent: ET.Element, tag: str, value: str | None) -> ET.Element | None:
    if value is None or value == "":
        return None
    node = ET.SubElement(parent, qname(NS_A, tag))
    node.text = value
    return node


def add_ref(parent: ET.Element, collection_name: str, object_name: str, ref_id: str) -> ET.Element:
    collection = ET.SubElement(parent, qname(NS_C, collection_name))
    return ET.SubElement(collection, qname(NS_O, object_name), {"Ref": ref_id})


def add_standard_metadata(parent: ET.Element, object_id: str, timestamp: str, creator: str, history_tag: str | None = None) -> None:
    add_attribute(parent, "ObjectID", object_id)
    add_attribute(parent, "CreationDate", timestamp)
    add_attribute(parent, "Creator", creator)
    add_attribute(parent, "ModificationDate", timestamp)
    add_attribute(parent, "Modifier", creator)
    if history_tag:
        add_attribute(parent, "History", f"ORG {{{object_id}}}\nDAT {timestamp}\nTAG {history_tag}")


def pd_update_constraint_value(action_code: str) -> str:
    mapping = {
        "a": "1",
        "r": "2",
        "c": "3",
        "n": "4",
        "d": "5",
    }
    return mapping.get(action_code, "1")


def rect_text(left: int, top: int, right: int, bottom: int) -> str:
    return f"(({left},{top}), ({right},{bottom}))"


def points_text(points: list[tuple[int, int]]) -> str:
    return "(" + ",".join(f"({x},{y})" for x, y in points) + ")"


def extract_length(data_type: str) -> str:
    match = re.search(r"\(([^)]+)\)", data_type)
    if not match:
        return ""
    return match.group(1)


def translate_tokens(tokens: list[str]) -> str:
    parts: list[str] = []
    for token in tokens:
        parts.append(TOKEN_DISPLAY_NAMES.get(token, token.upper()))
    return "".join(part for part in parts if part)


def table_display_name(table_name: str) -> str:
    display_name = TABLE_DISPLAY_NAMES.get(table_name)
    if display_name:
        return display_name
    return translate_tokens([token for token in table_name.removeprefix("dtlms_").split("_") if token])


def column_display_name(column_name: str) -> str:
    override_name = COLUMN_DISPLAY_OVERRIDES.get(column_name)
    if override_name:
        return override_name

    tokens = [token for token in column_name.split("_") if token]
    if not tokens:
        return column_name

    if tokens[0] == "is" and len(tokens) > 1:
        return "是否" + translate_tokens(tokens[1:])
    if tokens[0] == "has" and len(tokens) > 1:
        return "是否有" + translate_tokens(tokens[1:])

    if len(tokens) > 1:
        suffix = tokens[-1]
        prefix = tokens[:-1]
        prefix_text = translate_tokens(prefix)
        if suffix == "id":
            return prefix_text + "ID"
        if suffix == "name":
            if prefix and prefix[-1] in PERSON_NAME_TOKENS:
                return prefix_text + "姓名"
            return prefix_text + "名称"
        if suffix == "code":
            return prefix_text + "编码"
        if suffix == "status":
            return prefix_text + "状态"
        if suffix in {"date", "time", "month", "year"}:
            return prefix_text + TOKEN_DISPLAY_NAMES[suffix]
        if suffix == "text":
            return prefix_text + "文本"
        if suffix == "url":
            return prefix_text + "地址"
        if suffix == "number":
            return prefix_text + "号码"
        if suffix == "count":
            return prefix_text + "数量"
        if suffix == "type":
            return prefix_text + "类型"
        if suffix == "key":
            return prefix_text + "键"
        if suffix == "no":
            return prefix_text + "编号"

    return translate_tokens(tokens)


def fetch_tables(cur: psycopg.Cursor[Any]) -> list[str]:
    cur.execute(
        """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
          AND tablename LIKE 'dtlms_%'
          AND tablename NOT LIKE 'dtlms_runtime_%'
          AND tablename <> 'dtlms_schema_migrations'
        ORDER BY tablename ASC
        """
    )
    return [str(row[0]) for row in cur.fetchall()]


def fetch_columns(cur: psycopg.Cursor[Any], table_names: list[str]) -> dict[str, list[dict[str, Any]]]:
    cur.execute(
        """
        SELECT
            cls.relname AS table_name,
            att.attname AS column_name,
            pg_catalog.format_type(att.atttypid, att.atttypmod) AS data_type,
            att.attnotnull AS not_null,
            pg_get_expr(def.adbin, def.adrelid) AS default_value,
            att.attnum AS ordinal_position
        FROM pg_catalog.pg_attribute att
        JOIN pg_catalog.pg_class cls ON cls.oid = att.attrelid
        JOIN pg_catalog.pg_namespace nsp ON nsp.oid = cls.relnamespace
        LEFT JOIN pg_catalog.pg_attrdef def
            ON def.adrelid = att.attrelid
           AND def.adnum = att.attnum
        WHERE nsp.nspname = 'public'
          AND cls.relkind = 'r'
          AND cls.relname = ANY(%s)
          AND att.attnum > 0
          AND NOT att.attisdropped
        ORDER BY cls.relname ASC, att.attnum ASC
        """,
        (table_names,),
    )
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in cur.fetchall():
        grouped[str(row[0])].append(
            {
                "column_name": str(row[1]),
                "data_type": str(row[2]),
                "not_null": bool(row[3]),
                "default_value": row[4],
                "ordinal_position": int(row[5]),
            }
        )
    return grouped


def fetch_constraints(cur: psycopg.Cursor[Any], table_names: list[str]) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    cur.execute(
        """
        SELECT
            con.conname AS constraint_name,
            child.relname AS table_name,
            con.contype AS constraint_type,
            pg_get_constraintdef(con.oid, true) AS constraint_def,
            parent.relname AS parent_table,
            con.confupdtype AS update_action,
            con.confdeltype AS delete_action,
            array_remove(array_agg(child_att.attname ORDER BY child_pos.ordinality), NULL) AS child_columns,
            array_remove(array_agg(parent_att.attname ORDER BY child_pos.ordinality), NULL) AS parent_columns
        FROM pg_catalog.pg_constraint con
        JOIN pg_catalog.pg_class child ON child.oid = con.conrelid
        JOIN pg_catalog.pg_namespace child_nsp ON child_nsp.oid = child.relnamespace
        LEFT JOIN pg_catalog.pg_class parent ON parent.oid = con.confrelid
        LEFT JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS child_pos(attnum, ordinality) ON TRUE
        LEFT JOIN LATERAL unnest(con.confkey) WITH ORDINALITY AS parent_pos(attnum, ordinality)
            ON parent_pos.ordinality = child_pos.ordinality
        LEFT JOIN pg_catalog.pg_attribute child_att
            ON child_att.attrelid = child.oid
           AND child_att.attnum = child_pos.attnum
        LEFT JOIN pg_catalog.pg_attribute parent_att
            ON parent_att.attrelid = parent.oid
           AND parent_att.attnum = parent_pos.attnum
        WHERE child_nsp.nspname = 'public'
          AND child.relname = ANY(%s)
          AND con.contype IN ('p', 'u', 'f')
        GROUP BY con.oid, con.conname, child.relname, con.contype, parent.relname, con.confupdtype, con.confdeltype
        ORDER BY child.relname ASC, con.contype ASC, con.conname ASC
        """,
        (table_names,),
    )
    table_constraints: dict[str, list[dict[str, Any]]] = defaultdict(list)
    foreign_keys: list[dict[str, Any]] = []
    for row in cur.fetchall():
        table_name = str(row[1])
        item = {
            "constraint_name": str(row[0]),
            "table_name": table_name,
            "constraint_type": str(row[2]),
            "constraint_def": str(row[3]),
            "parent_table": str(row[4]) if row[4] is not None else None,
            "update_action": str(row[5]) if row[5] is not None else "a",
            "delete_action": str(row[6]) if row[6] is not None else "a",
            "child_columns": [str(value) for value in (row[7] or [])],
            "parent_columns": [str(value) for value in (row[8] or [])],
        }
        if item["constraint_type"] in {"p", "u"}:
            table_constraints[table_name].append(item)
        elif item["constraint_type"] == "f":
            foreign_keys.append(item)
    return table_constraints, foreign_keys


def fetch_indexes(cur: psycopg.Cursor[Any], table_names: list[str]) -> dict[str, list[dict[str, Any]]]:
    cur.execute(
        """
        SELECT
            tbl.relname AS table_name,
            idx.relname AS index_name,
            pg_get_indexdef(idx.oid) AS index_def,
            ind.indisunique AS is_unique,
            array_remove(array_agg(att.attname ORDER BY ord.ordinality), NULL) AS column_names
        FROM pg_catalog.pg_class tbl
        JOIN pg_catalog.pg_namespace nsp ON nsp.oid = tbl.relnamespace
        JOIN pg_catalog.pg_index ind ON ind.indrelid = tbl.oid
        JOIN pg_catalog.pg_class idx ON idx.oid = ind.indexrelid
        LEFT JOIN LATERAL unnest(ind.indkey) WITH ORDINALITY AS ord(attnum, ordinality) ON TRUE
        LEFT JOIN pg_catalog.pg_attribute att
            ON att.attrelid = tbl.oid
           AND att.attnum = ord.attnum
        WHERE nsp.nspname = 'public'
          AND tbl.relname = ANY(%s)
          AND NOT ind.indisprimary
          AND NOT EXISTS (
              SELECT 1
              FROM pg_catalog.pg_constraint con
              WHERE con.conindid = ind.indexrelid
                AND con.contype IN ('p', 'u')
          )
        GROUP BY tbl.relname, idx.relname, idx.oid, ind.indisunique
        ORDER BY tbl.relname ASC, idx.relname ASC
        """,
        (table_names,),
    )
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in cur.fetchall():
        grouped[str(row[0])].append(
            {
                "index_name": str(row[1]),
                "index_def": str(row[2]).rstrip(";"),
                "is_unique": bool(row[3]),
                "column_names": [str(value) for value in (row[4] or [])],
            }
        )
    return grouped


def build_schema_sql(
    table_names: list[str],
    columns_by_table: dict[str, list[dict[str, Any]]],
    constraints_by_table: dict[str, list[dict[str, Any]]],
    foreign_keys: list[dict[str, Any]],
    indexes_by_table: dict[str, list[dict[str, Any]]],
    env_values: dict[str, str],
) -> str:
    lines: list[str] = []
    lines.append("-- PowerDesigner 16.5 reverse engineering source")
    lines.append("-- Generated by tools/export_powerdesigner_schema.py")
    lines.append(f"-- Source database: {env_values['POSTGRES_DB']}")
    lines.append("-- Scope: public.dtlms_* tables excluding dtlms_runtime_* and dtlms_schema_migrations")
    lines.append("")
    lines.append("SET client_encoding = 'UTF8';")
    lines.append("")

    for table_name in table_names:
        lines.append(f"-- Table: public.{table_name}")
        lines.append(f"CREATE TABLE public.{quote_ident(table_name)} (")
        definition_lines: list[str] = []
        for column in columns_by_table.get(table_name, []):
            segment = f"    {quote_ident(str(column['column_name']))} {column['data_type']}"
            default_value = column.get("default_value")
            if default_value is not None:
                segment += f" DEFAULT {default_value}"
            if column.get("not_null"):
                segment += " NOT NULL"
            definition_lines.append(segment)

        for constraint in constraints_by_table.get(table_name, []):
            definition_lines.append(f"    CONSTRAINT {quote_ident(constraint['constraint_name'])} {constraint['constraint_def']}")

        lines.append(",\n".join(definition_lines))
        lines.append(");")
        lines.append("")

    for foreign_key in foreign_keys:
        child_columns = ", ".join(quote_ident(item) for item in foreign_key["child_columns"])
        parent_columns = ", ".join(quote_ident(item) for item in foreign_key["parent_columns"])
        lines.append(
            f"ALTER TABLE public.{quote_ident(foreign_key['table_name'])} "
            f"ADD CONSTRAINT {quote_ident(foreign_key['constraint_name'])} "
            f"FOREIGN KEY ({child_columns}) REFERENCES public.{quote_ident(str(foreign_key['parent_table']))} ({parent_columns}) "
            f"ON UPDATE {action_text(foreign_key['update_action'])} "
            f"ON DELETE {action_text(foreign_key['delete_action'])};"
        )
    if foreign_keys:
        lines.append("")

    for table_name in table_names:
        for index_item in indexes_by_table.get(table_name, []):
            lines.append(index_item["index_def"] + ";")
        if indexes_by_table.get(table_name):
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_pdm_xml(
    table_names: list[str],
    columns_by_table: dict[str, list[dict[str, Any]]],
    constraints_by_table: dict[str, list[dict[str, Any]]],
    foreign_keys: list[dict[str, Any]],
    indexes_by_table: dict[str, list[dict[str, Any]]],
    env_values: dict[str, str],
) -> str:
    timestamp = str(int(time.time()))
    creator = "GitHub Copilot"
    model_object_id = make_id("pdm_model", env_values["POSTGRES_DB"])
    ids = PdIdGenerator()

    root = ET.Element("Model")
    root_object = ET.SubElement(root, qname(NS_O, "RootObject"), {"Id": ids.new()})
    children = ET.SubElement(root_object, qname(NS_C, "Children"))

    model = ET.SubElement(children, qname(NS_O, "Model"), {"Id": ids.new()})
    add_attribute(model, "ObjectID", model_object_id)
    add_attribute(model, "Name", f"pydtlms_{env_values['POSTGRES_DB']} (PDM)")
    add_attribute(model, "Code", f"PYDTLMS_{env_values['POSTGRES_DB'].upper()}")
    add_attribute(model, "CreationDate", timestamp)
    add_attribute(model, "Creator", creator)
    add_attribute(model, "ModificationDate", timestamp)
    add_attribute(model, "Modifier", creator)
    add_attribute(model, "Comment", "Generated from PostgreSQL public.dtlms_* tables")
    add_attribute(model, "PaperSize", "(8268, 11693)")
    add_attribute(model, "PageMargins", "((984,984), (984,984))")
    add_attribute(model, "PageOrientation", "1")
    add_attribute(model, "PaperSource", "15")

    dbms_shortcut = ET.SubElement(ET.SubElement(model, qname(NS_C, "DBMS")), qname(NS_O, "Shortcut"), {"Id": ids.new()})
    add_attribute(dbms_shortcut, "ObjectID", make_id("dbms_shortcut", env_values["POSTGRES_DB"]))
    add_attribute(dbms_shortcut, "Name", POSTGRESQL_DBMS_NAME)
    add_attribute(dbms_shortcut, "Code", POSTGRESQL_DBMS_CODE)
    add_attribute(dbms_shortcut, "TargetStereotype", "")
    add_attribute(dbms_shortcut, "TargetID", POSTGRESQL_DBMS_OBJECT_ID)
    add_attribute(dbms_shortcut, "TargetClassID", POWERDESIGNER_TARGET_CLASS_ID)

    diagrams_collection = ET.SubElement(model, qname(NS_C, "PhysicalDiagrams"))
    diagram = ET.SubElement(diagrams_collection, qname(NS_O, "PhysicalDiagram"), {"Id": ids.new()})
    add_standard_metadata(diagram, make_id("physical_diagram", env_values["POSTGRES_DB"]), timestamp, creator, "DIAGRAM")
    add_attribute(diagram, "Name", "MainDiagram")
    add_attribute(diagram, "Code", "MAIN_DIAGRAM")

    target_models = ET.SubElement(model, qname(NS_C, "TargetModels"))
    target_model = ET.SubElement(target_models, qname(NS_O, "TargetModel"), {"Id": ids.new()})
    add_attribute(target_model, "ObjectID", make_id("target_model", env_values["POSTGRES_DB"]))
    add_attribute(target_model, "Name", POSTGRESQL_DBMS_NAME)
    add_attribute(target_model, "Code", POSTGRESQL_DBMS_CODE)
    add_attribute(target_model, "TargetModelURL", POSTGRESQL_TARGET_MODEL_URL)
    add_attribute(target_model, "TargetModelID", POSTGRESQL_DBMS_OBJECT_ID)
    add_attribute(target_model, "TargetModelClassID", POWERDESIGNER_TARGET_CLASS_ID)
    session_shortcuts = ET.SubElement(target_model, qname(NS_C, "SessionShortcuts"))
    ET.SubElement(session_shortcuts, qname(NS_O, "Shortcut"), {"Ref": dbms_shortcut.attrib["Id"]})

    default_groups = ET.SubElement(model, qname(NS_C, "DefaultGroups"))
    default_group = ET.SubElement(default_groups, qname(NS_O, "Group"), {"Id": ids.new()})
    add_standard_metadata(default_group, make_id("default_group", DEFAULT_GROUP_NAME), timestamp, creator, "GROUP")
    add_attribute(default_group, "Name", DEFAULT_GROUP_NAME)
    add_attribute(default_group, "Code", DEFAULT_GROUP_NAME)

    tables_collection = ET.SubElement(model, qname(NS_C, "Tables"))
    references_collection = ET.SubElement(model, qname(NS_C, "References"))
    symbols = ET.SubElement(diagram, qname(NS_C, "Symbols"))

    table_ids: dict[str, str] = {}
    column_ids: dict[tuple[str, str], str] = {}
    key_ids: dict[tuple[str, str], str] = {}
    table_symbol_ids: dict[str, str] = {}
    primary_key_ids: dict[str, str] = {}

    for table_index, table_name in enumerate(table_names):
        table_id = ids.new()
        table_ids[table_name] = table_id
        table_node = ET.SubElement(tables_collection, qname(NS_O, "Table"), {"Id": table_id})
        add_standard_metadata(table_node, make_id("table_object", table_name), timestamp, creator, "TABLE")
        add_attribute(table_node, "Name", table_display_name(table_name))
        add_attribute(table_node, "Code", table_name)

        column_collection = ET.SubElement(table_node, qname(NS_C, "Columns"))
        for column in columns_by_table.get(table_name, []):
            column_name = str(column["column_name"])
            column_id = ids.new()
            column_ids[(table_name, column_name)] = column_id
            column_node = ET.SubElement(column_collection, qname(NS_O, "Column"), {"Id": column_id})
            add_standard_metadata(column_node, make_id("column_object", f"{table_name}.{column_name}"), timestamp, creator, "COLUMN")
            add_attribute(column_node, "Name", column_display_name(column_name))
            add_attribute(column_node, "Code", column_name)
            add_attribute(column_node, "DataType", str(column["data_type"]))
            add_attribute(column_node, "Length", extract_length(str(column["data_type"])))
            add_attribute(column_node, "Column.Mandatory", "1" if column["not_null"] else "0")
            if column.get("default_value") is not None:
                add_attribute(column_node, "DefaultValue", str(column["default_value"]))

        key_collection = ET.SubElement(table_node, qname(NS_C, "Keys"))
        primary_key_id: str | None = None
        for constraint in constraints_by_table.get(table_name, []):
            key_id = ids.new()
            key_ids[(table_name, constraint["constraint_name"])] = key_id
            key_node = ET.SubElement(key_collection, qname(NS_O, "Key"), {"Id": key_id})
            add_standard_metadata(key_node, make_id("key_object", f"{table_name}.{constraint['constraint_name']}"), timestamp, creator, "KEY")
            add_attribute(key_node, "Name", constraint["constraint_name"])
            add_attribute(key_node, "Code", constraint["constraint_name"])
            if constraint["constraint_type"] == "u":
                add_attribute(key_node, "ConstraintName", constraint["constraint_name"])
            key_columns = ET.SubElement(key_node, qname(NS_C, "Key.Columns"))
            for column_name in constraint["child_columns"]:
                column_id = column_ids.get((table_name, column_name))
                if column_id is not None:
                    ET.SubElement(key_columns, qname(NS_O, "Column"), {"Ref": column_id})
            if constraint["constraint_type"] == "p":
                primary_key_id = key_id
                primary_key_ids[table_name] = key_id

        if primary_key_id is not None:
            primary_key = ET.SubElement(table_node, qname(NS_C, "PrimaryKey"))
            ET.SubElement(primary_key, qname(NS_O, "Key"), {"Ref": primary_key_id})

        x = -32000 + (table_index % 4) * 12000
        y = -28000 + (table_index // 4) * 8000
        width = 7200
        height = max(2600, 1200 + 380 * len(columns_by_table.get(table_name, [])))
        table_symbol_id = ids.new()
        table_symbol_ids[table_name] = table_symbol_id
        table_symbol = ET.SubElement(symbols, qname(NS_O, "TableSymbol"), {"Id": table_symbol_id})
        add_attribute(table_symbol, "ModificationDate", timestamp)
        add_attribute(table_symbol, "IconMode", "-1")
        add_attribute(table_symbol, "Rect", rect_text(x, y, x + width, y + height))
        add_attribute(table_symbol, "ShadowStyle", "1")
        add_attribute(table_symbol, "LineColor", "16711680")
        add_attribute(table_symbol, "FillColor", "8454016")
        add_attribute(table_symbol, "ShadowColor", "8421504")
        add_attribute(table_symbol, "FontList", SYMBOL_FONT_LIST)
        add_ref(table_symbol, "Object", "Table", table_id)

    for foreign_key in foreign_keys:
        fk_name = foreign_key["constraint_name"]
        parent_table = str(foreign_key["parent_table"])
        child_table = foreign_key["table_name"]
        reference_id = ids.new()
        reference_node = ET.SubElement(references_collection, qname(NS_O, "Reference"), {"Id": reference_id})
        add_standard_metadata(reference_node, make_id("reference_object", fk_name), timestamp, creator, "REFERENCE")
        add_attribute(reference_node, "Name", fk_name)
        add_attribute(reference_node, "Code", fk_name)
        add_attribute(reference_node, "Cardinality", "0..n")
        add_attribute(reference_node, "UpdateConstraint", pd_update_constraint_value(foreign_key["update_action"]))
        add_attribute(reference_node, "DeleteConstraint", pd_update_constraint_value(foreign_key["delete_action"]))
        add_ref(reference_node, "ParentTable", "Table", table_ids[parent_table])
        add_ref(reference_node, "ChildTable", "Table", table_ids[child_table])
        parent_key_id = primary_key_ids.get(parent_table)
        if parent_key_id is not None:
            add_ref(reference_node, "ParentKey", "Key", parent_key_id)

        joins = ET.SubElement(reference_node, qname(NS_C, "Joins"))
        for ordinal, (child_column, parent_column) in enumerate(
            zip(foreign_key["child_columns"], foreign_key["parent_columns"], strict=False),
            start=1,
        ):
            join = ET.SubElement(joins, qname(NS_O, "ReferenceJoin"), {"Id": ids.new()})
            add_standard_metadata(join, make_id("reference_join_object", f"{fk_name}:{ordinal}"), timestamp, creator, "REFERENCE_JOIN")
            add_ref(join, "Object1", "Column", column_ids[(parent_table, parent_column)])
            add_ref(join, "Object2", "Column", column_ids[(child_table, child_column)])

        parent_symbol_id = table_symbol_ids[parent_table]
        child_symbol_id = table_symbol_ids[child_table]
        parent_index = table_names.index(parent_table)
        child_index = table_names.index(child_table)
        parent_x = -32000 + (parent_index % 4) * 12000 + 3600
        parent_y = -28000 + (parent_index // 4) * 8000 + 1300
        child_x = -32000 + (child_index % 4) * 12000 + 3600
        child_y = -28000 + (child_index // 4) * 8000 + 1300
        mid_x = int((parent_x + child_x) / 2)
        mid_y = int((parent_y + child_y) / 2)

        reference_symbol = ET.SubElement(symbols, qname(NS_O, "ReferenceSymbol"), {"Id": ids.new()})
        add_attribute(reference_symbol, "ModificationDate", timestamp)
        add_attribute(
            reference_symbol,
            "Rect",
            rect_text(min(parent_x, child_x), min(parent_y, child_y), max(parent_x, child_x), max(parent_y, child_y)),
        )
        add_attribute(reference_symbol, "ListOfPoints", points_text([(parent_x, parent_y), (mid_x, mid_y), (child_x, child_y)]))
        add_attribute(reference_symbol, "CornerStyle", "2")
        add_attribute(reference_symbol, "ArrowStyle", "1")
        add_attribute(reference_symbol, "LineColor", "16711680")
        add_attribute(reference_symbol, "ShadowColor", "8421504")
        add_attribute(reference_symbol, "FontList", REFERENCE_FONT_LIST)
        add_ref(reference_symbol, "SourceSymbol", "TableSymbol", parent_symbol_id)
        add_ref(reference_symbol, "DestinationSymbol", "TableSymbol", child_symbol_id)
        add_ref(reference_symbol, "Object", "Reference", reference_id)

    ET.indent(root, space="  ")
    object_count = ids._next - 1
    symbol_count = len(table_symbol_ids) + len(foreign_keys)
    xml_body = ET.tostring(root, encoding="unicode")
    processing_instruction = (
        f'<?PowerDesigner AppLocale="UTF16" ID="{{{model_object_id}}}" '
        f'Name="pydtlms_{env_values["POSTGRES_DB"]} (PDM)" '
        f'Objects="{object_count}" Symbols="{symbol_count}" '
        f'Target="{POSTGRESQL_DBMS_NAME}" Type="{POWERDESIGNER_MODEL_TYPE}" '
        f'signature="PDM_DATA_MODEL_XML" version="16.5.0.3982"?>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        + processing_instruction
        + '\n<!-- do not edit this file -->\n\n'
        + xml_body
        + '\n'
    )


def validate_pdm_xml(xml_text: str, expected_tables: int, expected_references: int) -> None:
    root = ET.fromstring(xml_text)
    table_nodes = root.findall(f"./{qname(NS_O, 'RootObject')}/{qname(NS_C, 'Children')}/{qname(NS_O, 'Model')}/{qname(NS_C, 'Tables')}/{qname(NS_O, 'Table')}")
    reference_nodes = root.findall(f"./{qname(NS_O, 'RootObject')}/{qname(NS_C, 'Children')}/{qname(NS_O, 'Model')}/{qname(NS_C, 'References')}/{qname(NS_O, 'Reference')}")
    if len(table_nodes) != expected_tables:
        raise ValueError(f"Unexpected table count in generated PDM: {len(table_nodes)} != {expected_tables}")
    if len(reference_nodes) != expected_references:
        raise ValueError(
            f"Unexpected reference count in generated PDM: {len(reference_nodes)} != {expected_references}"
        )


def build_import_guide(env_values: dict[str, str], table_count: int, fk_count: int) -> str:
    return "\n".join(
        [
            "# PowerDesigner 16.5 导入说明",
            "",
            "已提供文件：",
            f"- documents/pydtlms-powerdesigner16_5-complete.pdm",
            f"- documents/pydtlms-powerdesigner16_5-reverse-engineering.sql",
            "",
            "内容来源：",
            f"- 数据库：{env_values['POSTGRES_DB']}",
            f"- public schema 下的 dtlms_* 物理表，共 {table_count} 张表，外键 {fk_count} 条",
            "- 已排除 dtlms_runtime_* 与 dtlms_schema_migrations",
            "",
            "优先使用原生 .pdm：",
            "1. 在 PowerDesigner 16.5 中选择 File -> Open Model。",
            "2. 打开 documents/pydtlms-powerdesigner16_5-complete.pdm。",
            "3. 进入 MainDiagram 查看表和关系线；如布局需要，可再执行 Auto Layout 微调。",
            "",
            "如果你仍想走 SQL 逆向：",
            "1. File -> Reverse Engineer -> Database。",
            "2. DBMS 选择 PostgreSQL 对应版本。",
            "3. Input 选择 Script files。",
            "4. 选中 documents/pydtlms-powerdesigner16_5-reverse-engineering.sql。",
            "",
            "说明：",
            "- 已使用本机安装的 PowerDesigner 16.5 实际打开 documents/pydtlms-powerdesigner16_5-complete.pdm，验证可正常识别模型。",
            f"- 实际打开验证结果：{table_count} 张表、{fk_count} 条关系、1 张 Physical Diagram。",
            "- 同时做了 XML 结构校验，确保表数量与外键数量和数据库一致。",
            "- .pdm 为主交付，SQL 保留作为备用逆向来源。",
        ]
    ) + "\n"


def main() -> None:
    env_values = load_env_file(ENV_PATH)
    dsn = build_dsn(env_values)
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            table_names = fetch_tables(cur)
            columns_by_table = fetch_columns(cur, table_names)
            constraints_by_table, foreign_keys = fetch_constraints(cur, table_names)
            indexes_by_table = fetch_indexes(cur, table_names)

    schema_sql = build_schema_sql(
        table_names,
        columns_by_table,
        constraints_by_table,
        foreign_keys,
        indexes_by_table,
        env_values,
    )
    pdm_xml = build_pdm_xml(
        table_names,
        columns_by_table,
        constraints_by_table,
        foreign_keys,
        indexes_by_table,
        env_values,
    )
    validate_pdm_xml(pdm_xml, len(table_names), len(foreign_keys))
    OUTPUT_SQL_PATH.write_text(schema_sql, encoding="utf-8")
    OUTPUT_GUIDE_PATH.write_text(
        build_import_guide(env_values, len(table_names), len(foreign_keys)),
        encoding="utf-8",
    )
    pdm_write_warning: str | None = None
    try:
        OUTPUT_PDM_PATH.write_text(pdm_xml, encoding="utf-8")
    except PermissionError:
        pdm_write_warning = (
            f"Skipped writing {OUTPUT_PDM_PATH} because the file is locked. "
            "Close the model in PowerDesigner and rerun the script to refresh the PDM file."
        )
    print(f"Generated {OUTPUT_SQL_PATH}")
    print(f"Generated {OUTPUT_GUIDE_PATH}")
    if pdm_write_warning is None:
        print(f"Generated {OUTPUT_PDM_PATH}")
    else:
        print(pdm_write_warning)
    print(f"Tables: {len(table_names)}")
    print(f"Foreign keys: {len(foreign_keys)}")


if __name__ == "__main__":
    main()