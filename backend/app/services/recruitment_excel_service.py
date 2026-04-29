from __future__ import annotations

from io import BytesIO
from typing import Any

from openpyxl import Workbook, load_workbook


RECRUITMENT_TEMPLATE_COLUMNS: list[tuple[str, str]] = [
    ("review_round", "轮次"),
    ("student_name", "全名"),
    ("first_choice", "第一志愿"),
    ("second_choice", "第二志愿"),
    ("gender", "性别"),
    ("political_status", "政治面貌"),
    ("marital_status", "婚否"),
    ("religious_belief", "宗教信仰"),
    ("native_place", "籍贯"),
    ("phone_number", "电话"),
    ("email", "邮箱"),
    ("mailing_address", "联系地址"),
    ("id_type", "证件类型"),
    ("id_number", "证件号码"),
    ("material_status", "资料审核"),
    ("graduation_school", "本科院校"),
    ("accept_adjustment", "是否接受调剂"),
    ("undergraduate_average_score", "本科期间平均成绩"),
    ("undergraduate_gpa", "本科期间绩点"),
    ("undergraduate_rank", "本科平均成绩排名"),
    ("undergraduate_major", "本科专业"),
    ("graduate_average_score", "硕士期间平均成绩"),
    ("graduate_gpa", "硕士期间绩点"),
    ("graduate_rank", "硕士平均成绩排名"),
    ("graduate_major", "硕士专业"),
    ("intended_advisor_name", "意向导师姓名"),
    ("discovery_channel", "了解上海人工智能实验室联合培养博士生的方式"),
    ("graduate_school", "硕士院校"),
    ("overseas_university_name", "就读境外大学名称"),
    ("overseas_master_university_name", "就读境外硕士大学名称"),
    ("self_evaluation", "本人自我评价"),
    ("applied_at", "申请时间"),
    ("research_problem", "你认为目前AI技术发展过程中还未被解决的，且你未来希望去作为科研目标解决的最重要问题是什么？"),
    ("research_status_analysis", "上述问题现在全球科研界完成到了什么阶段以及有什么局限性？你觉得是否有新方法可以解决？"),
    ("research_impact", "上述问题如果解决了，对于技术进步、技术普及（e.g.成本大幅降低）、以及日常生活会带来什么影响？"),
    ("ai_society_impact", "你认为AI未来最能在什么环节或者场景影响/改变/优化/威胁人类社会？"),
    ("dissenting_view", "请陈述一个目前AI行业基本形成共识，但你不同意的观点，可以适当展开（选填）。"),
    ("family_info", "家庭情况"),
    ("education_experience", "教育经历"),
    ("practice_experience", "实践经历"),
    ("personal_statement_text", "个人成长经历、自我个性描述、为何申报本项目或本专业以及未来职业发展规划等"),
    ("student_activity_experience", "学生活动经历"),
    ("personal_statement_attachment", "个人陈述附件"),
    ("material_list_attachment", "材料清单附件"),
    ("supplementary_profile", "个人简介"),
]


def _normalize_header(value: Any) -> str:
    return str(value or "").replace(" ", "").replace("\n", "").strip()


def _normalize_cell(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_recruitment_template(file_bytes: bytes) -> list[dict[str, Any]]:
    workbook = load_workbook(BytesIO(file_bytes), data_only=True)
    worksheet = workbook.active
    rows = list(worksheet.iter_rows(values_only=True))
    if not rows:
        return []

    header_row = rows[0]
    normalized_headers = [_normalize_header(item) for item in header_row]
    expected_headers = [_normalize_header(label) for _, label in RECRUITMENT_TEMPLATE_COLUMNS]
    if normalized_headers[: len(expected_headers)] != expected_headers:
        raise ValueError("导入文件表头与资料审核名单模板不一致")

    result: list[dict[str, Any]] = []
    for row in rows[1:]:
        values = list(row[: len(RECRUITMENT_TEMPLATE_COLUMNS)])
        if not any(value not in (None, "") for value in values):
            continue
        item = {
            field: _normalize_cell(value)
            for (field, _), value in zip(RECRUITMENT_TEMPLATE_COLUMNS, values, strict=False)
        }
        item["intended_field"] = item.get("first_choice") or item.get("second_choice") or "待分配方向"
        item["undergraduate_school"] = item.get("graduation_school") or item.get("undergraduate_school")
        result.append(item)
    return result


def build_recruitment_template(records: list[dict[str, Any]]) -> bytes:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Worksheet"
    worksheet.append([label for _, label in RECRUITMENT_TEMPLATE_COLUMNS])
    for record in records:
        worksheet.append([record.get(field) for field, _ in RECRUITMENT_TEMPLATE_COLUMNS])
    stream = BytesIO()
    workbook.save(stream)
    return stream.getvalue()
