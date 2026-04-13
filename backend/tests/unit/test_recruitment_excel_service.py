from io import BytesIO

from openpyxl import load_workbook

from app.services.recruitment_excel_service import build_recruitment_template, parse_recruitment_template


def test_parse_recruitment_template_reads_template_rows() -> None:
    content = build_recruitment_template(
        [
            {
                "review_round": "第一轮",
                "student_name": "张三",
                "first_choice": "人工智能",
                "second_choice": "计算机视觉",
                "gender": "男",
                "phone_number": "13900001111",
                "email": "zhangsan@example.com",
                "graduation_school": "复旦大学",
                "material_status": "材料齐全",
            }
        ]
    )

    rows = parse_recruitment_template(content)

    assert len(rows) == 1
    assert rows[0]["student_name"] == "张三"
    assert rows[0]["first_choice"] == "人工智能"
    assert rows[0]["intended_field"] == "人工智能"
    assert rows[0]["undergraduate_school"] == "复旦大学"


def test_build_recruitment_template_preserves_duplicate_profile_columns() -> None:
    content = build_recruitment_template(
        [
            {
                "student_name": "李四",
                "personal_statement_text": "第一段个人简介",
                "supplementary_profile": "第二段个人简介",
            }
        ]
    )

    workbook = load_workbook(BytesIO(content), data_only=True)
    worksheet = workbook.active
    headers = [cell.value for cell in worksheet[1]]
    values = [cell.value for cell in worksheet[2]]
    profile_indexes = [index for index, header in enumerate(headers) if header == "个人简介"]

    assert len(profile_indexes) == 2
    assert values[profile_indexes[0]] == "第一段个人简介"
    assert values[profile_indexes[1]] == "第二段个人简介"