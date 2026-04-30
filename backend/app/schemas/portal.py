from __future__ import annotations

import json
from typing import Any, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import SelectOption
from app.schemas.contact import validate_email, validate_optional_phone_number, validate_phone_number
from app.schemas.identity import validate_china_resident_id_number


def _first_non_empty(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str):
            text = value.strip()
            if text:
                return text
    return None


def _rewrite_portal_attachment_urls(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _rewrite_portal_attachment_urls(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_rewrite_portal_attachment_urls(item) for item in value]
    if not isinstance(value, str):
        return value

    text = value.strip()
    legacy_prefix = "/portal-attachments/uploads/"
    if text.startswith(legacy_prefix):
        return f"/api/v1/portal/attachments/{text[len(legacy_prefix):]}"
    return value


def _serialize_models(items: Sequence[BaseModel | dict[str, Any]] | None) -> str | None:
    if not items:
        return None
    payload: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, BaseModel):
            payload.append(item.model_dump(mode="json", exclude_none=True))
        elif isinstance(item, dict):
            payload.append({key: value for key, value in item.items() if value is not None})
    return json.dumps(payload, ensure_ascii=False) if payload else None


def _parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not isinstance(value, str) or not value.strip():
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []


def _parse_model_list(value: Any, model_cls: type[BaseModel]) -> list[BaseModel]:
    items: list[BaseModel] = []
    for raw in _parse_json_list(value):
        if not isinstance(raw, dict):
            continue
        try:
            items.append(model_cls.model_validate(raw))
        except Exception:
            continue
    return items


def _normalize_education_items(items: Sequence["PortalEducationExperienceItem"]) -> list["PortalEducationExperienceItem"]:
    normalized = sorted(items, key=lambda item: item.sort_order)
    return [item for item in normalized if _first_non_empty(item.education_stage, item.school_name)]


def _practice_item_has_content(item: "PortalPracticeExperienceItem") -> bool:
    return bool(
        _first_non_empty(
            item.start_month,
            item.end_month,
            item.organization_name,
            item.position_name,
            item.responsibility_text,
            item.verifier_name,
            item.verifier_phone,
        )
    )


def _normalize_practice_items(items: Sequence["PortalPracticeExperienceItem"]) -> list["PortalPracticeExperienceItem"]:
    return [item for item in items if _practice_item_has_content(item)]


def _validate_portal_practice_rules(items: Sequence["PortalPracticeExperienceItem"]) -> None:
    normalized = _normalize_practice_items(items)
    if len(normalized) > 2:
        raise ValueError("实践经历最多填写 2 条")

    for index, item in enumerate(normalized, start=1):
        if not _first_non_empty(item.verifier_name):
            raise ValueError(f"实践经历{index}必须填写证明人姓名")
        if not _first_non_empty(item.verifier_phone):
            raise ValueError(f"实践经历{index}必须填写证明人手机")
        if not _first_non_empty(item.start_month, item.end_month):
            continue

        missing_fields: list[str] = []
        if not _first_non_empty(item.start_month):
            missing_fields.append("开始年月")
        if not _first_non_empty(item.end_month):
            missing_fields.append("结束年月")
        if not _first_non_empty(item.organization_name):
            missing_fields.append("实习实践/工作单位")
        if not _first_non_empty(item.position_name):
            missing_fields.append("岗位")
        if not _first_non_empty(item.verifier_name):
            missing_fields.append("证明人姓名")
        if not _first_non_empty(item.verifier_phone):
            missing_fields.append("证明人手机")
        if missing_fields:
            raise ValueError(
                f"实践经历{index}填写了开始年月或结束年月时，除职责外其余字段均必填：缺少{'、'.join(missing_fields)}"
            )


def _english_item_has_content(item: "PortalEnglishProficiencyItem") -> bool:
    return bool(
        _first_non_empty(
            item.exam_name,
            item.score_text,
            item.certificate_attachment_url,
            item.certificate_attachment_name,
        )
    )


def _normalize_english_items(items: Sequence["PortalEnglishProficiencyItem"]) -> list["PortalEnglishProficiencyItem"]:
    return [item for item in items if _english_item_has_content(item)]


def _validate_portal_english_rules(items: Sequence["PortalEnglishProficiencyItem"], require_at_least_one: bool) -> None:
    normalized = _normalize_english_items(items)
    if require_at_least_one and not normalized:
        raise ValueError("请至少完整填写一条英语能力，并上传英语证明附件")

    for index, item in enumerate(normalized, start=1):
        exam_name = _first_non_empty(item.exam_name)
        if exam_name == "CET-4":
            raise ValueError("英语能力不再支持填写“CET-4”，请改填 CET-6、IELTS、TOEFL 或其他英语考试成绩")
        if not exam_name:
            raise ValueError(f"英语能力{index}请先选择英语考试名称")
        if not _first_non_empty(item.certificate_attachment_url):
            raise ValueError(f"英语能力{index}必须上传英语证明附件")


def _validate_portal_family_rules(items: Sequence["PortalFamilyMemberItem"], require_at_least_one_parent: bool) -> None:
    if not require_at_least_one_parent:
        return

    has_parent = any(
        _first_non_empty(item.relation_type) in {"父亲", "母亲"} and _first_non_empty(item.member_name)
        for item in items
    )
    if not has_parent:
        raise ValueError("父母信息至少填写一方")


def _achievement_item_has_content(item: "PortalAchievementRecordItem") -> bool:
    return bool(
        _first_non_empty(
            item.achievement_type,
            item.achievement_month,
            item.paper_title,
            item.author_order,
            item.journal_or_conference,
            item.publish_or_index_month,
            item.award_name,
            item.award_rank,
            item.award_certificate_attachment_url,
            item.awarding_organization,
            item.award_level,
            item.award_year,
            item.description_text,
            item.responsibility_text,
        )
    )


def _normalize_achievement_items(items: Sequence["PortalAchievementRecordItem"]) -> list["PortalAchievementRecordItem"]:
    return [item for item in items if _achievement_item_has_content(item)]


def _populate_achievement_legacy_fields(items: Sequence["PortalAchievementRecordItem"]) -> list["PortalAchievementRecordItem"]:
    normalized = _normalize_achievement_items(items)
    for item in normalized:
        achievement_month = _first_non_empty(item.achievement_month, item.publish_or_index_month)
        description_text = _first_non_empty(item.description_text, item.responsibility_text)
        award_rank = _first_non_empty(item.award_rank, item.award_level)

        item.achievement_month = achievement_month
        item.publish_or_index_month = achievement_month
        item.description_text = description_text
        item.responsibility_text = description_text
        item.award_rank = award_rank
        item.award_level = award_rank
        if achievement_month and not _first_non_empty(item.award_year):
            item.award_year = achievement_month[:4]
    return normalized


def _validate_portal_achievement_rules(items: Sequence["PortalAchievementRecordItem"]) -> None:
    normalized = _normalize_achievement_items(items)
    if len(normalized) > 4:
        raise ValueError("成果经历最多填写 4 条")

    for index, item in enumerate(normalized, start=1):
        achievement_type = _first_non_empty(item.achievement_type)
        if achievement_type not in {"论文发表", "获奖经历"}:
            raise ValueError(f"成果经历{index}仅支持填写“论文发表”或“获奖经历”")

        achievement_month = _first_non_empty(item.achievement_month, item.publish_or_index_month)
        description_text = _first_non_empty(item.description_text, item.responsibility_text)

        if achievement_type == "论文发表":
            missing_fields: list[str] = []
            if not achievement_month:
                missing_fields.append("日期")
            if not _first_non_empty(item.paper_title):
                missing_fields.append("论文名称")
            if not _first_non_empty(item.author_order):
                missing_fields.append("作者序位")
            if not _first_non_empty(item.journal_or_conference):
                missing_fields.append("期刊名称")
            if not description_text:
                missing_fields.append("描述")
            if missing_fields:
                raise ValueError(f"成果经历{index}为论文发表时，以下字段必填：{'、'.join(missing_fields)}")

        if achievement_type == "获奖经历":
            missing_fields = []
            if not achievement_month:
                missing_fields.append("日期")
            if not _first_non_empty(item.award_name):
                missing_fields.append("奖项名称")
            if not _first_non_empty(item.award_rank, item.award_level):
                missing_fields.append("获奖名次")
            if not _first_non_empty(item.award_certificate_attachment_url):
                missing_fields.append("获奖证明")
            if not description_text:
                missing_fields.append("描述")
            if missing_fields:
                raise ValueError(f"成果经历{index}为获奖经历时，以下字段必填：{'、'.join(missing_fields)}")


def _validate_portal_education_rules(items: Sequence["PortalEducationExperienceItem"], require_minimum_two: bool) -> None:
    if not items:
        return

    ordered = sorted(items, key=lambda item: item.sort_order)
    first_item = ordered[0] if ordered else None
    if first_item is None or _first_non_empty(first_item.education_stage) != "高中毕业":
        raise ValueError("教育经历1的教育阶段必须为“高中毕业”")

    second_item = ordered[1] if len(ordered) > 1 else None
    if second_item is None or not _first_non_empty(second_item.education_stage) or not _first_non_empty(second_item.school_name):
        raise ValueError("教育经历2必须完整填写，且教育阶段应为“本科在读”或“本科毕业”")
    if _first_non_empty(second_item.education_stage) not in {"本科在读", "本科毕业"}:
        raise ValueError("教育经历2必须完整填写，且教育阶段应为“本科在读”或“本科毕业”")

    third_item = ordered[2] if len(ordered) > 2 else None
    third_item_started = third_item is not None and bool(
        _first_non_empty(third_item.education_stage)
        or _first_non_empty(third_item.school_name)
        or _first_non_empty(third_item.start_month)
        or _first_non_empty(third_item.end_month)
    )
    if third_item_started:
        if _first_non_empty(second_item.education_stage) != "本科毕业":
            raise ValueError("填写教育经历3前，教育经历2的教育阶段应为“本科毕业”")
        if _first_non_empty(third_item.education_stage) not in {"硕士在读", "硕士毕业"}:
            raise ValueError("教育经历3的教育阶段应为“硕士在读”或“硕士毕业”")

    normalized = _normalize_education_items(items)
    completed = [item for item in normalized if _first_non_empty(item.education_stage) and _first_non_empty(item.school_name)]
    stage_selected = [item for item in normalized if _first_non_empty(item.education_stage)]

    if len(normalized) > 3:
        raise ValueError("教育经历最多填写 3 条")
    if require_minimum_two and len(completed) < 2:
        raise ValueError("请至少完整填写两条教育经历")

    for index, item in enumerate(ordered, start=1):
        stage = _first_non_empty(item.education_stage)
        if not stage:
            continue
        missing_fields: list[str] = []
        if not _first_non_empty(item.start_month):
            missing_fields.append("开始年月")
        if not stage.endswith("在读") and not _first_non_empty(item.end_month):
            missing_fields.append("结束年月")
        if not _first_non_empty(item.school_name):
            missing_fields.append("就读学校")
        if not _first_non_empty(item.verifier_name):
            missing_fields.append("证明人姓名")
        if not _first_non_empty(item.verifier_phone):
            missing_fields.append("证明人手机")
        if stage != "高中毕业":
            if not _first_non_empty(item.major_name):
                missing_fields.append("就读专业")
            if not _first_non_empty(item.average_score):
                missing_fields.append("期间平均成绩")
            if not _first_non_empty(item.gpa):
                missing_fields.append("期间绩点")
            if not _first_non_empty(item.ranking):
                missing_fields.append("成绩排名")
            if not _first_non_empty(item.transcript_attachment_url):
                missing_fields.append("成绩单附件")
            if stage.endswith("毕业"):
                if not _first_non_empty(item.degree_certificate_attachment_url):
                    missing_fields.append("学位证附件")
                if not _first_non_empty(item.graduation_certificate_attachment_url):
                    missing_fields.append("毕业证附件")
        if missing_fields:
            raise ValueError(f"教育经历{index}以下字段必填：{'、'.join(missing_fields)}")

    stages = {_first_non_empty(item.education_stage) for item in stage_selected}
    if "本科毕业" in stages and not ({"硕士在读", "硕士毕业"} & stages):
        raise ValueError("填写“本科毕业”时，必须同时填写“硕士在读”或“硕士毕业”教育经历")
    if "本科在读" in stages and ({"硕士在读", "硕士毕业"} & stages):
        raise ValueError("填写“本科在读”时，不能同时填写“硕士在读”或“硕士毕业”教育经历")


def _build_personal_statement_summary(personal_statement: "PortalPersonalStatementData") -> str | None:
    return _first_non_empty(personal_statement.personal_statement_text)


def _populate_personal_statement_legacy_fields(personal_statement: "PortalPersonalStatementData") -> "PortalPersonalStatementData":
    personal_statement.growth_experience_text = _first_non_empty(
        personal_statement.growth_experience_text,
        personal_statement.personal_statement_text,
    )
    personal_statement.program_application_reason_text = _first_non_empty(
        personal_statement.program_application_reason_text,
        personal_statement.ai_problem_statement,
    )
    personal_statement.career_plan_text = _first_non_empty(
        personal_statement.career_plan_text,
        personal_statement.ai_industry_opinion,
    )
    personal_statement.personal_statement_text = _first_non_empty(
        personal_statement.personal_statement_text,
        _build_personal_statement_summary(personal_statement),
    )
    personal_statement.ai_problem_statement = _first_non_empty(
        personal_statement.ai_problem_statement,
        personal_statement.program_application_reason_text,
    )
    personal_statement.ai_industry_opinion = _first_non_empty(
        personal_statement.ai_industry_opinion,
        personal_statement.career_plan_text,
    )
    return personal_statement


def _validate_portal_personal_statement_rules(
    personal_statement: "PortalPersonalStatementData | None",
    require_complete: bool,
) -> None:
    if personal_statement is None:
        if require_complete:
            raise ValueError("请填写个人陈述")
        return

    statement_text = _first_non_empty(personal_statement.personal_statement_text)
    resume_attachment_url = _first_non_empty(personal_statement.resume_attachment_url)

    has_any_content = bool(
        statement_text
        or _first_non_empty(personal_statement.ai_problem_statement)
        or _first_non_empty(personal_statement.ai_industry_opinion)
        or _first_non_empty(personal_statement.growth_experience_text)
        or _first_non_empty(personal_statement.program_application_reason_text)
        or _first_non_empty(personal_statement.career_plan_text)
        or resume_attachment_url
        or _first_non_empty(personal_statement.supporting_material_attachment_url)
    )
    if not has_any_content:
        if require_complete:
            raise ValueError("请填写个人陈述")
        return

    if not require_complete:
        return

    if statement_text and len(statement_text) > 1200:
        raise ValueError("个人陈述需控制在 1200 字以内")

    if not statement_text:
        raise ValueError("请填写个人陈述并上传简历。")

    if not resume_attachment_url:
        raise ValueError("请填写个人陈述并上传简历。")


def _validate_portal_basic_profile_rules(
    profile: "PortalApplicantProfileData | None",
    *,
    gender: str | None,
    ethnic_group: str | None,
    political_status: str | None,
    mailing_address: str | None,
    require_complete: bool,
) -> None:
    emergency_contact_phone = profile.emergency_contact_phone if profile is not None else None
    if emergency_contact_phone:
        validate_phone_number(emergency_contact_phone, "紧急联系人手机")

    if not require_complete:
        return

    missing_fields: list[str] = []
    required_fields = [
        ("姓名拼音", profile.full_name_pinyin if profile is not None else None),
        ("个人照片", profile.profile_photo_url if profile is not None else None),
        ("身份证拼图", profile.id_card_collage_url if profile is not None else None),
        ("性别", gender),
        ("民族", ethnic_group),
        ("政治面貌", political_status),
        ("紧急联系人姓名", profile.emergency_contact_name if profile is not None else None),
        ("紧急联系人手机", emergency_contact_phone),
        ("通讯地址", mailing_address),
    ]
    for field_label, value in required_fields:
        if not _first_non_empty(value):
            missing_fields.append(field_label)

    if missing_fields:
        raise ValueError(f"基本信息以下字段必填：{'、'.join(missing_fields)}")


def _validate_portal_source_channel_rules(source_channel: str | None, source_channel_other: str | None) -> None:
    if not _first_non_empty(source_channel):
        raise ValueError("请选择了解项目方式")

    if _first_non_empty(source_channel) == "其他" and not _first_non_empty(source_channel_other):
        raise ValueError("选择“其他”来源时，请补充说明")


def _validate_portal_declaration_rules(signed_agreement: bool) -> None:
    if not signed_agreement:
        raise ValueError("请先确认提交声明")


def _validate_portal_draft_rules_by_section(payload: "PortalApplicationDraftUpsert") -> None:
    section_id = _first_non_empty(payload.validation_section_id)
    if not section_id:
        return

    if section_id == "basic-section":
        _validate_portal_basic_profile_rules(
            payload.profile,
            gender=payload.gender,
            ethnic_group=payload.ethnic_group,
            political_status=payload.political_status,
            mailing_address=payload.mailing_address,
            require_complete=True,
        )
        return

    if section_id == "application-section":
        _validate_portal_source_channel_rules(payload.source_channel, payload.source_channel_other)
        if not _first_non_empty(payload.selected_team_name):
            raise ValueError("缺少第一志愿研究中心信息")
        return

    if section_id == "education-section":
        _validate_portal_education_rules(payload.education_experiences, require_minimum_two=True)
        return

    if section_id == "practice-section":
        _validate_portal_practice_rules(payload.practice_experiences)
        return

    if section_id == "english-section":
        _validate_portal_english_rules(payload.english_proficiencies, require_at_least_one=True)
        return

    if section_id == "family-section":
        _validate_portal_family_rules(payload.family_members, require_at_least_one_parent=True)
        return

    if section_id == "achievement-section":
        _validate_portal_achievement_rules(payload.achievement_records)
        return

    if section_id == "statement-section":
        _validate_portal_personal_statement_rules(payload.personal_statement, require_complete=True)
        return


class PortalApplicantProfileData(BaseModel):
    full_name_pinyin: str | None = None
    profile_photo_url: str | None = None
    id_card_collage_url: str | None = None
    gender: str | None = None
    birth_date: str | None = None
    ethnic_group: str | None = None
    native_place: str | None = None
    political_status: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    id_type: str | None = None
    mailing_address: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

    @field_validator("emergency_contact_phone")
    @classmethod
    def validate_emergency_contact_phone_field(cls, value: str | None) -> str | None:
        return validate_optional_phone_number(value, "紧急联系人手机")


class PortalApplicationPreferenceItem(BaseModel):
    preference_order: int = 1
    research_center_name: str | None = None
    team_id: int | None = None
    advisor_name: str | None = None
    advisor_user_id: int | None = None
    is_optional: bool = False


class PortalEducationExperienceItem(BaseModel):
    sort_order: int = 1
    education_stage: str
    start_month: str | None = None
    end_month: str | None = None
    school_name: str
    major_name: str | None = None
    average_score: str | None = None
    gpa: str | None = None
    ranking: str | None = None
    verifier_name: str | None = None
    verifier_phone: str | None = None
    transcript_attachment_url: str | None = None
    transcript_attachment_name: str | None = None
    degree_certificate_attachment_url: str | None = None
    degree_certificate_attachment_name: str | None = None
    graduation_certificate_attachment_url: str | None = None
    graduation_certificate_attachment_name: str | None = None


class PortalPracticeExperienceItem(BaseModel):
    start_month: str | None = None
    end_month: str | None = None
    organization_name: str
    position_name: str | None = None
    responsibility_text: str | None = None
    verifier_name: str | None = None
    verifier_phone: str | None = None


class PortalEnglishProficiencyItem(BaseModel):
    exam_name: str
    score_text: str | None = None
    certificate_attachment_url: str | None = None
    certificate_attachment_name: str | None = None


class PortalFamilyMemberItem(BaseModel):
    member_name: str
    relation_type: str
    employer_name: str | None = None
    job_title: str | None = None
    contact_phone: str | None = None


class PortalAchievementRecordItem(BaseModel):
    achievement_type: str
    achievement_month: str | None = None
    paper_title: str | None = None
    author_order: str | None = None
    journal_or_conference: str | None = None
    publish_or_index_month: str | None = None
    award_name: str | None = None
    award_rank: str | None = None
    award_certificate_attachment_url: str | None = None
    award_certificate_attachment_name: str | None = None
    awarding_organization: str | None = None
    award_level: str | None = None
    award_year: str | None = None
    description_text: str | None = None
    responsibility_text: str | None = None


class PortalPersonalStatementData(BaseModel):
    personal_statement_text: str | None = None
    ai_problem_statement: str | None = None
    ai_industry_opinion: str | None = None
    growth_experience_text: str | None = None
    program_application_reason_text: str | None = None
    career_plan_text: str | None = None
    resume_attachment_url: str | None = None
    resume_attachment_name: str | None = None
    supporting_material_attachment_url: str | None = None
    supporting_material_attachment_name: str | None = None


class PortalApplicationDeclarationData(BaseModel):
    has_read_declaration: bool = False
    declaration_text: str | None = None
    progress_snapshot: dict[str, Any] | None = None


class PortalApplicationDraftRecord(BaseModel):
    selected_plan_id: int | None = None
    source_channel: str | None = None
    source_channel_other: str | None = None
    preferences: list[PortalApplicationPreferenceItem] = Field(default_factory=list)
    education_experiences: list[PortalEducationExperienceItem] = Field(default_factory=list)
    practice_experiences: list[PortalPracticeExperienceItem] = Field(default_factory=list)
    english_proficiencies: list[PortalEnglishProficiencyItem] = Field(default_factory=list)
    family_members: list[PortalFamilyMemberItem] = Field(default_factory=list)
    achievement_records: list[PortalAchievementRecordItem] = Field(default_factory=list)
    personal_statement: PortalPersonalStatementData = Field(default_factory=PortalPersonalStatementData)
    declaration: PortalApplicationDeclarationData = Field(default_factory=PortalApplicationDeclarationData)
    submitted_at: str | None = None


class PortalRegistrationEmailCodeRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str) -> str:
        return validate_email(value)


class PortalRegistrationEmailCodeResponse(BaseModel):
    message: str
    expires_in_seconds: int
    cooldown_seconds: int


class PortalLoginEmailCodeRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str) -> str:
        return validate_email(value)


class PortalEmailCodeLoginRequest(BaseModel):
    email: str
    email_verification_code: str

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str) -> str:
        return validate_email(value)

    @field_validator("email_verification_code")
    @classmethod
    def validate_email_verification_code_field(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if len(normalized) != 6 or not normalized.isdigit():
            raise ValueError("邮件验证码格式不正确，请输入 6 位数字验证码")
        return normalized


class PortalRegistrationRequest(BaseModel):
    phone_number: str
    email: str
    full_name: str
    id_number: str
    password: str
    email_verification_code: str = ""

    @field_validator("id_number")
    @classmethod
    def validate_id_number(cls, value: str) -> str:
        return validate_china_resident_id_number(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str) -> str:
        return validate_phone_number(value)

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str) -> str:
        return validate_email(value)

    @field_validator("email_verification_code")
    @classmethod
    def validate_email_verification_code_field(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            return ""
        if len(normalized) != 6 or not normalized.isdigit():
            raise ValueError("邮件验证码格式不正确，请输入 6 位数字验证码")
        return normalized


class PortalRegistrationResponse(BaseModel):
    message: str
    student: "PortalStudentRecord"


class PortalLoginRequest(BaseModel):
    account: str
    password: str


class PortalPasswordResetRequest(BaseModel):
    account: str
    id_number: str
    new_password: str

    @field_validator("id_number")
    @classmethod
    def validate_id_number(cls, value: str) -> str:
        return validate_china_resident_id_number(value)


class PortalPasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class PortalStudentRecord(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    id_number: str
    business_key: str | None = None
    candidate_no: str | None = None
    account_status: str = "启用"
    gender: str | None = None
    birth_date: str | None = None
    ethnic_group: str | None = None
    native_place: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    id_type: str | None = None
    mailing_address: str | None = None
    graduation_school: str | None = None
    highest_degree: str | None = None
    intended_field: str | None = None
    political_status: str | None = None
    english_level: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_profile: str | None = None
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_plan_id: int | None = None
    selected_team_id: int | None = None
    selected_team_name: str | None = None
    selected_advisor_user_id: int | None = None
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None
    submitted_at: str | None = None
    profile: PortalApplicantProfileData | None = None
    application_draft: PortalApplicationDraftRecord | None = None

    @model_validator(mode="before")
    @classmethod
    def populate_structured_sections(cls, raw_value: Any) -> Any:
        if not isinstance(raw_value, dict):
            return raw_value

        data = _rewrite_portal_attachment_urls(dict(raw_value))
        if data.get("profile") is None:
            profile_payload = {
                "profile_photo_url": data.get("profile_photo_url"),
                "id_card_collage_url": data.get("id_card_collage_url"),
                "gender": data.get("gender"),
                "birth_date": data.get("birth_date"),
                "ethnic_group": data.get("ethnic_group"),
                "native_place": data.get("native_place"),
                "political_status": data.get("political_status"),
                "marital_status": data.get("marital_status"),
                "religious_belief": data.get("religious_belief"),
                "id_type": data.get("id_type"),
                "mailing_address": data.get("mailing_address"),
            }
            if any(value is not None for value in profile_payload.values()):
                data["profile"] = profile_payload

        if data.get("application_draft") is None:
            preferences: list[dict[str, Any]] = []
            if _first_non_empty(data.get("selected_team_name")):
                preferences.append(
                    {
                        "preference_order": 1,
                        "team_id": data.get("selected_team_id"),
                        "research_center_name": data.get("selected_team_name"),
                        "advisor_user_id": data.get("selected_advisor_user_id"),
                        "advisor_name": data.get("selected_advisor_name"),
                        "is_optional": False,
                    }
                )
            education_experiences = _parse_model_list(data.get("education_experience"), PortalEducationExperienceItem)
            practice_experiences = _parse_model_list(data.get("practice_experience"), PortalPracticeExperienceItem)
            family_members = _parse_model_list(data.get("family_info"), PortalFamilyMemberItem)
            english_proficiencies = _parse_model_list(data.get("english_level"), PortalEnglishProficiencyItem)
            achievement_records = _parse_model_list(data.get("recommendation_notes"), PortalAchievementRecordItem)
            personal_statement = PortalPersonalStatementData(
                personal_statement_text=data.get("personal_statement_text"),
            )
            declaration = PortalApplicationDeclarationData(
                has_read_declaration=bool(data.get("signed_agreement")),
            )
            if (
                data.get("selected_plan_id") is not None
                or preferences
                or education_experiences
                or practice_experiences
                or family_members
                or english_proficiencies
                or achievement_records
                or personal_statement.personal_statement_text
                or declaration.has_read_declaration
                or data.get("submitted_at") is not None
            ):
                data["application_draft"] = {
                    "selected_plan_id": data.get("selected_plan_id"),
                    "preferences": preferences,
                    "education_experiences": education_experiences,
                    "practice_experiences": practice_experiences,
                    "family_members": family_members,
                    "english_proficiencies": english_proficiencies,
                    "achievement_records": achievement_records,
                    "personal_statement": personal_statement,
                    "declaration": declaration,
                    "submitted_at": data.get("submitted_at"),
                }
        return data


class PortalSessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: PortalStudentRecord


class PortalPlanRecord(BaseModel):
    id: int
    plan_name: str
    academic_term: str
    brochure_image_url: str | None = None
    summary: str | None = None


class PortalPlanListResponse(BaseModel):
    items: list[PortalPlanRecord] = Field(default_factory=list)


class PortalTeamRecord(BaseModel):
    id: int
    team_name: str
    lead_user_id: int | None = None
    lead_advisor_name: str
    advisor_names: list[str] = Field(default_factory=list)
    advisor_ids: list[int] = Field(default_factory=list)
    advisor_relation_ids: list[int] = Field(default_factory=list)
    department_name: str
    discipline_name: str
    research_directions: list[str] = Field(default_factory=list)
    description: str | None = None


class PortalTeamListResponse(BaseModel):
    items: list[PortalTeamRecord] = Field(default_factory=list)


class PortalProfileOptionsResponse(BaseModel):
    political_status_options: list[SelectOption] = Field(default_factory=list)
    ethnic_group_options: list[SelectOption] = Field(default_factory=list)


class PortalPublicConfigResponse(BaseModel):
    portal_admissions_info_url: str = "https://www.shlab.org.cn"


class PortalApplicationUpsert(BaseModel):
    plan_id: int
    profile: PortalApplicantProfileData | None = None
    source_channel: str | None = None
    source_channel_other: str | None = None
    preferences: list[PortalApplicationPreferenceItem] = Field(default_factory=list)
    education_experiences: list[PortalEducationExperienceItem] = Field(default_factory=list)
    practice_experiences: list[PortalPracticeExperienceItem] = Field(default_factory=list)
    english_proficiencies: list[PortalEnglishProficiencyItem] = Field(default_factory=list)
    family_members: list[PortalFamilyMemberItem] = Field(default_factory=list)
    achievement_records: list[PortalAchievementRecordItem] = Field(default_factory=list)
    personal_statement: PortalPersonalStatementData | None = None
    declaration: PortalApplicationDeclarationData | None = None
    gender: str | None = None
    birth_date: str | None = None
    ethnic_group: str | None = None
    native_place: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    id_type: str | None = None
    mailing_address: str | None = None
    graduation_school: str | None = None
    highest_degree: str | None = None
    intended_field: str | None = None
    political_status: str | None = None
    english_level: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_profile: str | None = None
    material_list_attachment: str | None = None
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_team_id: int | None = None
    selected_team_name: str | None = None
    selected_advisor_user_id: int | None = None
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None

    @model_validator(mode="after")
    def populate_legacy_fields(self) -> "PortalApplicationUpsert":
        self.practice_experiences = _normalize_practice_items(self.practice_experiences)
        self.english_proficiencies = _normalize_english_items(self.english_proficiencies)
        self.achievement_records = _populate_achievement_legacy_fields(self.achievement_records)
        if self.personal_statement is not None:
            self.personal_statement = _populate_personal_statement_legacy_fields(self.personal_statement)

        if self.profile is not None:
            self.gender = self.gender or self.profile.gender
            self.birth_date = self.birth_date or self.profile.birth_date
            self.ethnic_group = self.ethnic_group or self.profile.ethnic_group
            self.native_place = self.native_place or self.profile.native_place
            self.marital_status = self.marital_status or self.profile.marital_status
            self.religious_belief = self.religious_belief or self.profile.religious_belief
            self.id_type = self.id_type or self.profile.id_type
            self.mailing_address = self.mailing_address or self.profile.mailing_address
            self.political_status = self.political_status or self.profile.political_status

        preferences = sorted(self.preferences, key=lambda item: item.preference_order)
        if preferences:
            primary_preference = preferences[0]
            self.selected_team_id = self.selected_team_id or primary_preference.team_id
            self.selected_team_name = self.selected_team_name or primary_preference.research_center_name
            self.selected_advisor_user_id = self.selected_advisor_user_id or primary_preference.advisor_user_id
            self.selected_advisor_name = self.selected_advisor_name or primary_preference.advisor_name
            self.intended_field = self.intended_field or primary_preference.research_center_name

        ordered_education = sorted(self.education_experiences, key=lambda item: item.sort_order)
        if ordered_education:
            primary_education = ordered_education[0]
            self.graduation_school = self.graduation_school or primary_education.school_name
            self.highest_degree = self.highest_degree or primary_education.education_stage

        if self.english_proficiencies and not self.english_level:
            primary_english = self.english_proficiencies[0]
            self.english_level = _first_non_empty(
                f"{primary_english.exam_name}:{primary_english.score_text}" if primary_english.score_text else None,
                primary_english.exam_name,
            )

        if self.family_members and not self.family_info:
            self.family_info = _serialize_models(self.family_members)
        if self.education_experiences and not self.education_experience:
            self.education_experience = _serialize_models(self.education_experiences)
        if self.practice_experiences and not self.practice_experience:
            self.practice_experience = _serialize_models(self.practice_experiences)
        if self.achievement_records and not self.recommendation_notes:
            self.recommendation_notes = _serialize_models(self.achievement_records)

        if self.personal_statement is not None:
            self.personal_statement_text = self.personal_statement_text or self.personal_statement.personal_statement_text
            self.material_list_attachment = self.material_list_attachment or self.personal_statement.supporting_material_attachment_url

        if self.personal_statement is not None and not self.personal_profile:
            self.personal_profile = self.personal_statement.growth_experience_text

        if self.personal_statement is not None and not self.self_evaluation:
            self.self_evaluation = self.personal_statement.career_plan_text

        if self.declaration is not None:
            self.signed_agreement = self.signed_agreement or self.declaration.has_read_declaration

        _validate_portal_education_rules(
            self.education_experiences,
            require_minimum_two=bool(self.education_experiences),
        )
        _validate_portal_practice_rules(self.practice_experiences)
        _validate_portal_english_rules(self.english_proficiencies, require_at_least_one=True)
        _validate_portal_family_rules(self.family_members, require_at_least_one_parent=True)
        _validate_portal_achievement_rules(self.achievement_records)
        _validate_portal_personal_statement_rules(self.personal_statement, require_complete=True)
        _validate_portal_basic_profile_rules(
            self.profile,
            gender=self.gender,
            ethnic_group=self.ethnic_group,
            political_status=self.political_status,
            mailing_address=self.mailing_address,
            require_complete=True,
        )
        _validate_portal_source_channel_rules(self.source_channel, self.source_channel_other)
        _validate_portal_declaration_rules(self.signed_agreement)

        if not _first_non_empty(self.graduation_school):
            raise ValueError("缺少毕业院校/就读学校信息")
        if not _first_non_empty(self.highest_degree):
            raise ValueError("缺少最高学历/教育阶段信息")
        if not _first_non_empty(self.selected_team_name):
            raise ValueError("缺少第一志愿研究中心信息")
        if not _first_non_empty(self.intended_field):
            self.intended_field = self.selected_team_name
        return self


class PortalApplicationDraftUpsert(BaseModel):
    plan_id: int = 0
    validation_section_id: str | None = None
    profile: PortalApplicantProfileData | None = None
    source_channel: str | None = None
    source_channel_other: str | None = None
    preferences: list[PortalApplicationPreferenceItem] = Field(default_factory=list)
    education_experiences: list[PortalEducationExperienceItem] = Field(default_factory=list)
    practice_experiences: list[PortalPracticeExperienceItem] = Field(default_factory=list)
    english_proficiencies: list[PortalEnglishProficiencyItem] = Field(default_factory=list)
    family_members: list[PortalFamilyMemberItem] = Field(default_factory=list)
    achievement_records: list[PortalAchievementRecordItem] = Field(default_factory=list)
    personal_statement: PortalPersonalStatementData | None = None
    declaration: PortalApplicationDeclarationData | None = None
    gender: str | None = None
    birth_date: str | None = None
    ethnic_group: str | None = None
    native_place: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    id_type: str | None = None
    mailing_address: str | None = None
    graduation_school: str | None = None
    highest_degree: str | None = None
    intended_field: str | None = None
    political_status: str | None = None
    english_level: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_profile: str | None = None
    material_list_attachment: str | None = None
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_team_id: int | None = None
    selected_team_name: str | None = None
    selected_advisor_user_id: int | None = None
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None

    @model_validator(mode="after")
    def populate_legacy_fields(self) -> "PortalApplicationDraftUpsert":
        self.practice_experiences = _normalize_practice_items(self.practice_experiences)
        self.english_proficiencies = _normalize_english_items(self.english_proficiencies)
        self.achievement_records = _populate_achievement_legacy_fields(self.achievement_records)
        if self.personal_statement is not None:
            self.personal_statement = _populate_personal_statement_legacy_fields(self.personal_statement)

        if self.profile is not None:
            self.gender = self.gender or self.profile.gender
            self.birth_date = self.birth_date or self.profile.birth_date
            self.ethnic_group = self.ethnic_group or self.profile.ethnic_group
            self.native_place = self.native_place or self.profile.native_place
            self.marital_status = self.marital_status or self.profile.marital_status
            self.religious_belief = self.religious_belief or self.profile.religious_belief
            self.id_type = self.id_type or self.profile.id_type
            self.mailing_address = self.mailing_address or self.profile.mailing_address
            self.political_status = self.political_status or self.profile.political_status

        preferences = sorted(self.preferences, key=lambda item: item.preference_order)
        if preferences:
            primary_preference = preferences[0]
            self.selected_team_id = self.selected_team_id or primary_preference.team_id
            self.selected_team_name = self.selected_team_name or primary_preference.research_center_name
            self.selected_advisor_user_id = self.selected_advisor_user_id or primary_preference.advisor_user_id
            self.selected_advisor_name = self.selected_advisor_name or primary_preference.advisor_name
            self.intended_field = self.intended_field or primary_preference.research_center_name

        ordered_education = sorted(self.education_experiences, key=lambda item: item.sort_order)
        if ordered_education:
            primary_education = ordered_education[0]
            self.graduation_school = self.graduation_school or primary_education.school_name
            self.highest_degree = self.highest_degree or primary_education.education_stage

        if self.english_proficiencies and not self.english_level:
            primary_english = self.english_proficiencies[0]
            self.english_level = _first_non_empty(
                f"{primary_english.exam_name}:{primary_english.score_text}" if primary_english.score_text else None,
                primary_english.exam_name,
            )

        if self.family_members and not self.family_info:
            self.family_info = _serialize_models(self.family_members)
        if self.education_experiences and not self.education_experience:
            self.education_experience = _serialize_models(self.education_experiences)
        if self.practice_experiences and not self.practice_experience:
            self.practice_experience = _serialize_models(self.practice_experiences)
        if self.achievement_records and not self.recommendation_notes:
            self.recommendation_notes = _serialize_models(self.achievement_records)

        if self.personal_statement is not None:
            self.personal_statement_text = self.personal_statement_text or self.personal_statement.personal_statement_text
            self.material_list_attachment = self.material_list_attachment or self.personal_statement.supporting_material_attachment_url

        if self.personal_statement is not None and not self.personal_profile:
            self.personal_profile = self.personal_statement.growth_experience_text

        if self.personal_statement is not None and not self.self_evaluation:
            self.self_evaluation = self.personal_statement.career_plan_text

        if self.declaration is not None:
            self.signed_agreement = self.signed_agreement or self.declaration.has_read_declaration

        if _first_non_empty(self.validation_section_id):
            _validate_portal_draft_rules_by_section(self)
            if not _first_non_empty(self.intended_field):
                self.intended_field = self.selected_team_name
            return self

        _validate_portal_education_rules(
            self.education_experiences,
            require_minimum_two=bool(self.education_experiences),
        )
        _validate_portal_practice_rules(self.practice_experiences)
        _validate_portal_english_rules(self.english_proficiencies, require_at_least_one=True)
        _validate_portal_family_rules(self.family_members, require_at_least_one_parent=True)
        _validate_portal_achievement_rules(self.achievement_records)
        _validate_portal_personal_statement_rules(self.personal_statement, require_complete=True)
        _validate_portal_basic_profile_rules(
            self.profile,
            gender=self.gender,
            ethnic_group=self.ethnic_group,
            political_status=self.political_status,
            mailing_address=self.mailing_address,
            require_complete=True,
        )
        _validate_portal_source_channel_rules(self.source_channel, self.source_channel_other)
        _validate_portal_declaration_rules(self.signed_agreement)

        if not _first_non_empty(self.graduation_school):
            raise ValueError("缺少毕业院校/就读学校信息")
        if not _first_non_empty(self.highest_degree):
            raise ValueError("缺少最高学历/教育阶段信息")
        if not _first_non_empty(self.selected_team_name):
            raise ValueError("缺少第一志愿研究中心信息")
        if not _first_non_empty(self.intended_field):
            self.intended_field = self.selected_team_name

        return self


class PortalApplicationSubmissionResponse(BaseModel):
    student: PortalStudentRecord
    application_business_key: str
    application_status: str


class PortalApplicationDraftSaveResponse(BaseModel):
    message: str
    student: PortalStudentRecord


class PortalAttachmentUploadResponse(BaseModel):
    category: str
    file_name: str
    file_type: str | None = None
    file_size: int
    url: str
