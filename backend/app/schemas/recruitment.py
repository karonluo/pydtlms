from datetime import datetime
from typing import Any, Sequence, TypeVar

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import PaginationResponseBase, SelectOption
from app.schemas.contact import validate_optional_email, validate_optional_phone_number
from app.schemas.identity import validate_china_resident_id_number
from app.schemas.portal import (
    PortalAchievementRecordItem,
    PortalApplicantProfileData,
    PortalApplicationDeclarationData,
    PortalApplicationPreferenceItem,
    PortalEducationExperienceItem,
    PortalEnglishProficiencyItem,
    PortalFamilyMemberItem,
    PortalPersonalStatementData,
    PortalPracticeExperienceItem,
)


def _first_non_empty(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str):
            text = value.strip()
            if text:
                return text
    return None


def _serialize_models(items: Sequence[BaseModel | dict[str, Any]] | None) -> str | None:
    if not items:
        return None
    payload: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, BaseModel):
            payload.append(item.model_dump(mode="json", exclude_none=True))
        elif isinstance(item, dict):
            payload.append({key: value for key, value in item.items() if value is not None})
    return __import__("json").dumps(payload, ensure_ascii=False) if payload else None


def _parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not isinstance(value, str) or not value.strip():
        return []
    try:
        parsed = __import__("json").loads(value)
    except Exception:
        return []
    return parsed if isinstance(parsed, list) else []


TModel = TypeVar("TModel", bound=BaseModel)


def _parse_model_list(value: Any, model_cls: type[TModel]) -> list[TModel]:
    items: list[TModel] = []
    for raw in _parse_json_list(value):
        if not isinstance(raw, dict):
            continue
        try:
            items.append(model_cls.model_validate(raw))
        except Exception:
            continue
    return items


def _fallback_education_experiences(data: dict[str, Any]) -> list[PortalEducationExperienceItem]:
    parsed = _parse_model_list(data.get("education_experience"), PortalEducationExperienceItem)
    if parsed:
        return parsed

    items: list[PortalEducationExperienceItem] = []
    graduation_school = _first_non_empty(data.get("graduation_school"), data.get("undergraduate_school"))
    if graduation_school:
        items.append(
            PortalEducationExperienceItem(
                sort_order=1,
                education_stage=str(data.get("highest_degree") or "本科"),
                school_name=graduation_school,
                major_name=data.get("undergraduate_major"),
                average_score=data.get("undergraduate_average_score"),
                gpa=data.get("undergraduate_gpa"),
                ranking=data.get("undergraduate_rank"),
            )
        )
    graduate_school = _first_non_empty(data.get("graduate_school"), data.get("overseas_master_university_name"))
    if graduate_school:
        items.append(
            PortalEducationExperienceItem(
                sort_order=len(items) + 1,
                education_stage="硕士",
                school_name=graduate_school,
                major_name=data.get("graduate_major"),
                average_score=data.get("graduate_average_score"),
                gpa=data.get("graduate_gpa"),
                ranking=data.get("graduate_rank"),
            )
        )
    return items


class RecruitPlanSummary(BaseModel):
    plan_name: str
    academic_term: str
    plan_description: str | None = None
    application_count: int


class RecruitWorkbench(BaseModel):
    plans: list[RecruitPlanSummary]
    pipeline: list[dict[str, str | int]]
    pending_tasks: list[dict[str, str]]


class RecruitPlanRecord(BaseModel):
    id: int
    plan_name: str
    academic_term: str
    academic_year: str
    semester: str
    application_count: int
    brochure_image_url: str | None = None
    plan_description: str | None = None


class RecruitPlanUpsert(BaseModel):
    plan_name: str
    academic_year: str
    semester: str
    brochure_image_url: str | None = None
    plan_description: str | None = None


class RecruitPlanListResponse(PaginationResponseBase):
    items: list[RecruitPlanRecord]


class BackgroundAssessmentRecord(BaseModel):
    evaluator_user_id: int | None = None
    evaluator_username: str
    evaluator_name: str | None = None
    evaluator_role_code: str
    assessment_result: str
    assessment_comment: str | None = None
    assessed_at: str | None = None


class QualificationReviewHistoryRecord(BaseModel):
    reviewer_username: str
    reviewer_name: str | None = None
    reviewer_role_code: str | None = None
    action: str
    action_label: str
    review_comment: str | None = None
    reviewed_at: str | None = None


class RecruitApplicationRecord(BaseModel):
    id: int
    plan_id: int
    business_key: str
    portal_student_id: int | None = None
    account_status: str | None = None
    selected_plan_name: str | None = None
    registered_at: str | None = None
    candidate_no: str | None = None
    review_round: str | None = None
    student_name: str
    first_choice: str | None = None
    second_choice: str | None = None
    first_choice_id: int | None = None
    second_choice_id: int | None = None
    gender: str | None = None
    political_status: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    native_place: str | None = None
    phone_number: str | None = None
    email: str | None = None
    mailing_address: str | None = None
    id_type: str | None = None
    id_number: str | None = None
    graduation_school: str
    undergraduate_school: str | None = None
    accept_adjustment: str | None = None
    undergraduate_average_score: str | None = None
    undergraduate_gpa: str | None = None
    undergraduate_rank: str | None = None
    undergraduate_major: str | None = None
    graduate_average_score: str | None = None
    graduate_gpa: str | None = None
    graduate_rank: str | None = None
    graduate_major: str | None = None
    highest_degree: str
    intended_field: str | None = None
    intended_advisor_user_id: int | None = None
    intended_advisor_name: str | None = None
    discovery_channel: str | None = None
    source_channel: str | None = None
    source_channel_other: str | None = None
    graduate_school: str | None = None
    overseas_university_name: str | None = None
    overseas_master_university_name: str | None = None
    self_evaluation: str | None = None
    applied_at: str | None = None
    research_problem: str | None = None
    research_status_analysis: str | None = None
    research_impact: str | None = None
    ai_society_impact: str | None = None
    dissenting_view: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_statement_text: str | None = None
    student_activity_experience: str | None = None
    personal_statement_attachment: str | None = None
    material_list_attachment: str | None = None
    material_list_attachment_name: str | None = None
    supplementary_profile: str | None = None
    material_status: str
    application_status: str
    advisor_screening_status: str | None = None
    advisor_screening_round: str | None = None
    advisor_screening_submitted_at: str | None = None
    advisor_signature_base64: str | None = None
    first_choice_screening_batch_id: int | None = None
    second_choice_screening_batch_id: int | None = None
    first_choice_screening_submitted_at: str | None = None
    second_choice_screening_submitted_at: str | None = None
    first_choice_screening_score: float | None = None
    second_choice_screening_score: float | None = None
    initial_screening_status: str | None = None
    initial_screening_result: str | None = None
    initial_screening_confirmed_at: str | None = None
    initial_screening_confirmer_username: str | None = None
    initial_screening_confirmer_name: str | None = None
    initial_screening_notification_status: str | None = None
    initial_screening_notification_sent_at: str | None = None
    next_stage_name: str | None = None
    reviewer_name: str | None = None
    final_score: float | None = None
    background_assessments: list[BackgroundAssessmentRecord] = Field(default_factory=list)
    qualification_review_history: list[QualificationReviewHistoryRecord] = Field(default_factory=list)
    profile: PortalApplicantProfileData | None = None
    preferences: list[PortalApplicationPreferenceItem] = Field(default_factory=list)
    education_experiences: list[PortalEducationExperienceItem] = Field(default_factory=list)
    practice_experiences: list[PortalPracticeExperienceItem] = Field(default_factory=list)
    english_proficiencies: list[PortalEnglishProficiencyItem] = Field(default_factory=list)
    family_members: list[PortalFamilyMemberItem] = Field(default_factory=list)
    achievement_records: list[PortalAchievementRecordItem] = Field(default_factory=list)
    personal_statement: PortalPersonalStatementData | None = None
    declaration: PortalApplicationDeclarationData | None = None

    @model_validator(mode="before")
    @classmethod
    def populate_structured_sections(cls, raw_value: Any) -> Any:
        if not isinstance(raw_value, dict):
            return raw_value
        data = dict(raw_value)
        if data.get("profile") is None:
            profile_payload = {
                "full_name_pinyin": data.get("full_name_pinyin"),
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
                "emergency_contact_name": data.get("emergency_contact_name"),
                "emergency_contact_phone": data.get("emergency_contact_phone"),
            }
            if any(value is not None for value in profile_payload.values()):
                data["profile"] = profile_payload

        if not data.get("preferences"):
            preferences: list[dict[str, Any]] = []
            if _first_non_empty(data.get("first_choice")):
                preferences.append(
                    {
                        "preference_order": 1,
                        "advisor_user_id": data.get("intended_advisor_user_id"),
                        "advisor_name": data.get("intended_advisor_name"),
                        "is_optional": False,
                    }
                )
            if _first_non_empty(data.get("second_choice")):
                preferences.append(
                    {
                        "preference_order": 2,
                        "advisor_name": None,
                        "is_optional": True,
                    }
                )
            data["preferences"] = preferences

        if not data.get("education_experiences"):
            data["education_experiences"] = _fallback_education_experiences(data)
        if not data.get("practice_experiences"):
            data["practice_experiences"] = _parse_model_list(data.get("practice_experience"), PortalPracticeExperienceItem)
        if not data.get("english_proficiencies"):
            data["english_proficiencies"] = _parse_model_list(data.get("english_level"), PortalEnglishProficiencyItem)
        if not data.get("family_members"):
            data["family_members"] = _parse_model_list(data.get("family_info"), PortalFamilyMemberItem)
        if not data.get("achievement_records"):
            data["achievement_records"] = _parse_model_list(data.get("recommendation_notes"), PortalAchievementRecordItem)
        if data.get("personal_statement") is None:
            data["personal_statement"] = PortalPersonalStatementData(
                personal_statement_text=data.get("personal_statement_text"),
                ai_problem_statement=data.get("research_problem"),
                ai_industry_opinion=data.get("dissenting_view"),
                resume_attachment_url=data.get("personal_statement_attachment"),
                supporting_material_attachment_url=data.get("material_list_attachment"),
            )
        if data.get("declaration") is None:
            data["declaration"] = PortalApplicationDeclarationData(has_read_declaration=False)
        return data


class RecruitPortalApplicationDetail(BaseModel):
    application_id: int
    plan_id: int
    business_key: str
    candidate_no: str | None = None
    student_name: str
    phone_number: str | None = None
    email: str | None = None
    id_number: str | None = None
    application_status: str
    material_status: str
    reviewer_name: str | None = None
    submitted_at: str | None = None
    advisor_screening_status: str | None = None
    advisor_screening_round: str | None = None
    advisor_screening_submitted_at: str | None = None
    advisor_signature_base64: str | None = None
    first_choice: str | None = None
    second_choice: str | None = None
    first_choice_id: int | None = None
    second_choice_id: int | None = None
    first_choice_screening_score: float | None = None
    second_choice_screening_score: float | None = None
    initial_screening_status: str | None = None
    initial_screening_result: str | None = None
    next_stage_name: str | None = None
    background_assessments: list[BackgroundAssessmentRecord] = Field(default_factory=list)
    qualification_review_history: list[QualificationReviewHistoryRecord] = Field(default_factory=list)
    profile: PortalApplicantProfileData | None = None
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


class RecruitApplicationUpsert(BaseModel):
    plan_id: int
    portal_student_id: int | None = None
    business_key: str | None = None
    candidate_no: str | None = None
    review_round: str | None = None
    student_name: str
    first_choice: str | None = None
    second_choice: str | None = None
    first_choice_id: int | None = None
    second_choice_id: int | None = None
    gender: str | None = None
    political_status: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    native_place: str | None = None
    phone_number: str | None = None
    email: str | None = None
    mailing_address: str | None = None
    id_type: str | None = None
    id_number: str | None = None
    graduation_school: str
    undergraduate_school: str | None = None
    accept_adjustment: str | None = None
    undergraduate_average_score: str | None = None
    undergraduate_gpa: str | None = None
    undergraduate_rank: str | None = None
    undergraduate_major: str | None = None
    graduate_average_score: str | None = None
    graduate_gpa: str | None = None
    graduate_rank: str | None = None
    graduate_major: str | None = None
    highest_degree: str
    intended_field: str
    intended_advisor_user_id: int | None = None
    intended_advisor_name: str | None = None
    discovery_channel: str | None = None
    source_channel: str | None = None
    source_channel_other: str | None = None
    graduate_school: str | None = None
    overseas_university_name: str | None = None
    overseas_master_university_name: str | None = None
    self_evaluation: str | None = None
    applied_at: str | None = None
    research_problem: str | None = None
    research_status_analysis: str | None = None
    research_impact: str | None = None
    ai_society_impact: str | None = None
    dissenting_view: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_statement_text: str | None = None
    student_activity_experience: str | None = None
    personal_statement_attachment: str | None = None
    material_list_attachment: str | None = None
    supplementary_profile: str | None = None
    material_status: str
    application_status: str
    advisor_screening_status: str | None = None
    advisor_screening_round: str | None = None
    advisor_screening_submitted_at: str | None = None
    advisor_signature_base64: str | None = None
    first_choice_screening_batch_id: int | None = None
    second_choice_screening_batch_id: int | None = None
    first_choice_screening_submitted_at: str | None = None
    second_choice_screening_submitted_at: str | None = None
    first_choice_screening_score: float | None = None
    second_choice_screening_score: float | None = None
    initial_screening_status: str | None = None
    initial_screening_result: str | None = None
    initial_screening_confirmed_at: str | None = None
    initial_screening_confirmer_username: str | None = None
    initial_screening_confirmer_name: str | None = None
    initial_screening_notification_status: str | None = None
    initial_screening_notification_sent_at: str | None = None
    next_stage_name: str | None = None
    reviewer_name: str | None = None
    final_score: float | None = None
    profile: PortalApplicantProfileData | None = None
    preferences: list[PortalApplicationPreferenceItem] = Field(default_factory=list)
    education_experiences: list[PortalEducationExperienceItem] = Field(default_factory=list)
    practice_experiences: list[PortalPracticeExperienceItem] = Field(default_factory=list)
    family_members: list[PortalFamilyMemberItem] = Field(default_factory=list)
    personal_statement: PortalPersonalStatementData | None = None
    declaration: PortalApplicationDeclarationData | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str | None) -> str | None:
        return validate_optional_phone_number(value)

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str | None) -> str | None:
        return validate_optional_email(value)

    @model_validator(mode="after")
    def populate_legacy_fields(self) -> "RecruitApplicationUpsert":
        if self.profile is not None:
            self.gender = self.gender or self.profile.gender
            self.native_place = self.native_place or self.profile.native_place
            self.political_status = self.political_status or self.profile.political_status
            self.marital_status = self.marital_status or self.profile.marital_status
            self.religious_belief = self.religious_belief or self.profile.religious_belief
            self.id_type = self.id_type or self.profile.id_type
            self.mailing_address = self.mailing_address or self.profile.mailing_address

        preferences = sorted(self.preferences, key=lambda item: item.preference_order)
        if preferences:
            self.first_choice = self.first_choice or preferences[0].advisor_name
            self.intended_advisor_user_id = self.intended_advisor_user_id or preferences[0].advisor_user_id
            self.intended_advisor_name = self.intended_advisor_name or preferences[0].advisor_name
            if len(preferences) > 1:
                self.second_choice = self.second_choice or preferences[1].advisor_name

        if self.source_channel or self.source_channel_other:
            self.discovery_channel = self.discovery_channel or self.source_channel_other or self.source_channel

        ordered_education = sorted(self.education_experiences, key=lambda item: item.sort_order)
        if ordered_education:
            primary_education = ordered_education[0]
            self.graduation_school = self.graduation_school or primary_education.school_name
            self.highest_degree = self.highest_degree or primary_education.education_stage
            self.undergraduate_major = self.undergraduate_major or primary_education.major_name
            self.undergraduate_average_score = self.undergraduate_average_score or primary_education.average_score
            self.undergraduate_gpa = self.undergraduate_gpa or primary_education.gpa
            self.undergraduate_rank = self.undergraduate_rank or primary_education.ranking
            if len(ordered_education) > 1:
                secondary_education = ordered_education[1]
                self.graduate_school = self.graduate_school or secondary_education.school_name
                self.graduate_major = self.graduate_major or secondary_education.major_name
                self.graduate_average_score = self.graduate_average_score or secondary_education.average_score
                self.graduate_gpa = self.graduate_gpa or secondary_education.gpa
                self.graduate_rank = self.graduate_rank or secondary_education.ranking
            self.education_experience = self.education_experience or _serialize_models(self.education_experiences)

        if self.practice_experiences and not self.practice_experience:
            self.practice_experience = _serialize_models(self.practice_experiences)
        if self.family_members and not self.family_info:
            self.family_info = _serialize_models(self.family_members)

        if self.personal_statement is not None:
            self.personal_statement_text = self.personal_statement_text or self.personal_statement.personal_statement_text
            self.research_problem = self.research_problem or self.personal_statement.ai_problem_statement
            self.dissenting_view = self.dissenting_view or self.personal_statement.ai_industry_opinion
            self.personal_statement_attachment = self.personal_statement_attachment or self.personal_statement.resume_attachment_url

        if not _first_non_empty(self.graduation_school):
            raise ValueError("缺少毕业院校/就读学校信息")
        if not _first_non_empty(self.highest_degree):
            raise ValueError("缺少最高学历/教育阶段信息")
        return self


class InitialScreeningConfirmationApplicationRecord(BaseModel):
    application_id: int
    student_id: int
    plan_id: int
    candidate_no: str
    business_key: str | None = None
    full_name: str
    first_choice: str | None = None
    first_choice_screening_score: float | None = None
    second_choice: str | None = None
    second_choice_screening_score: float | None = None
    first_choice_screening_submitted_at: datetime | None = None
    second_choice_screening_submitted_at: datetime | None = None
    choice_score: float | None = None
    is_passed: str | None = None
    choice_name: str | None = None
    application_status: str
    intended_advisor_name: str | None = None

class InitialScreeningConfirmationApplicationListResponse(PaginationResponseBase):
    items: list[InitialScreeningConfirmationApplicationRecord]

class RecruitApplicationListResponse(PaginationResponseBase):
    items: list[RecruitApplicationRecord]


class AdvisorScreeningSubmitItem(BaseModel):
    application_id: int
    advisor_score: float

    @field_validator("advisor_score")
    @classmethod
    def validate_advisor_score(cls, value: float) -> float:
        score = float(value)
        if score < 0 or score > 100:
            raise ValueError("导师初筛分数必须在 0 到 100 之间")
        return score


class AdvisorScreeningScoreUpdateRequest(BaseModel):
    application_id: int
    candidate_no: str
    choice_name: str
    advisor_score: float

    @field_validator("candidate_no", "choice_name", mode="before")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        return str(value or "").strip()

    @field_validator("choice_name")
    @classmethod
    def validate_choice_name(cls, value: str) -> str:
        if value not in {"第一志愿", "第二志愿"}:
            raise ValueError("choice_name 只能是 第一志愿 或 第二志愿")
        return value

    @field_validator("candidate_no")
    @classmethod
    def validate_candidate_no(cls, value: str) -> str:
        if not value:
            raise ValueError("candidate_no 不能为空")
        return value

    @field_validator("advisor_score")
    @classmethod
    def validate_advisor_score(cls, value: float) -> float:
        score = float(value)
        if score < 0 or score > 100:
            raise ValueError("导师初筛分数必须在 0 到 100 之间")
        return score


class AdvisorScreeningBatchSubmitRequest(BaseModel):
    signature_base64: str | None = None
    items: list[AdvisorScreeningSubmitItem] = Field(default_factory=list)

    @field_validator("signature_base64", mode="before")
    @classmethod
    def validate_signature_base64(cls, value: str | None) -> str | None:
        normalized = str(value or "").strip()
        return normalized or None

    @model_validator(mode="after")
    def validate_items(self) -> "AdvisorScreeningBatchSubmitRequest":
        if not self.items:
            raise ValueError("至少需要提交一条导师初筛记录")
        return self


class AdvisorScreeningBatchSubmitResponse(BaseModel):
    batch_id: int
    screening_round: str
    submitted_count: int
    applications: list[RecruitApplicationRecord] = Field(default_factory=list)


class InitialScreeningConfirmationRequest(BaseModel):
    result: str
    comment: str | None = None

    @field_validator("result")
    @classmethod
    def validate_result(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if normalized not in {"passed", "rejected"}:
            raise ValueError("初筛确认结果只能是 passed 或 rejected")
        return normalized


class RecruitApplicationImportIssue(BaseModel):
    row_number: int
    student_name: str | None = None
    reason: str


class RecruitApplicationImportResult(BaseModel):
    imported_count: int
    skipped_count: int
    plan_id: int
    imported_business_keys: list[str]
    issues: list[RecruitApplicationImportIssue]


class CampOfferRecord(BaseModel):
    id: int
    candidate_no: str
    plan_id: int
    plan_name: str | None = None
    is_sent_mail: bool = False
    is_agree: bool | None = None
    reason: str | None = None
    # 关联的报名记录 id（用于跳转到 /recruitment/registered-students 的同款填报详情弹窗）
    recruitment_application_id: int | None = None
    student_name: str | None = None
    student_email: str | None = None
    student_phone: str | None = None
    first_choice_advisor_name: str | None = None
    first_choice_advisor_team_name: str | None = None
    first_choice_screening_score: float | None = None
    second_choice_advisor_name: str | None = None
    second_choice_advisor_team_name: str | None = None
    second_choice_screening_score: float | None = None
    created_at: str | None = None
    student_offer_submitted_at: str | None = None
    # 黑客松夏令营专用字段 (2026-06-30 新增)
    hackathon_score: float | None = None
    hackathon_comments: str | None = None
    accepted: str | None = None  # 黑客松入取状态(字典: hackathon_accepted_status)
    # 2026-07-03: 当前登录用户能否对该行执行 [录取/不录取/待定] 操作
    # 规则与列表可见性一致(导师/中心负责人 + 分数>=80 + 流转判断)
    can_change_accepted: bool = False
    # 2026-07-06: 录取学校 (来自 dtlms_plan_offer.admission_offered_school varchar(64))
    admission_offered_school: str | None = None


# 黑客松入取状态允许的字典值(对应数据库 dtlms_dict_data.hackathon_accepted_status)
# value 为空字符串 '' 代表 NULL (待录取)
HACKATHON_ACCEPTED_VALUES: set[str] = {
    "declined",
    "pending",
    "accepted_pending_send",
    "accepted_sent",
    "accepted_confirmed",
    "accepted_rejected",
}

class CampOfferUpsert(BaseModel):
    candidate_no: str
    plan_id: int | None = None
    is_sent_mail: bool = False
    is_agree: bool | None = None
    reason: str | None = None
    student_offer_submitted_at: str | None = None
    # 黑客松夏令营专用字段 (2026-06-30 新增)
    hackathon_score: float | None = None
    hackathon_comments: str | None = None
    accepted: str | None = None  # 黑客松入取状态(字典: hackathon_accepted_status)
    # 2026-07-03: 当前登录用户能否对该行执行 [录取/不录取/待定] 操作
    # 规则与列表可见性一致(导师/中心负责人 + 分数>=80 + 流转判断)
    can_change_accepted: bool = False
    # 2026-07-06: 录取学校 (来自 dtlms_plan_offer.admission_offered_school varchar(64))
    admission_offered_school: str | None = None

    @field_validator("candidate_no", mode="before")
    @classmethod
    def validate_candidate_no(cls, value: Any) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValueError("candidate_no 不能为空")
        return text

    @field_validator("reason", mode="before")
    @classmethod
    def validate_reason(cls, value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    @field_validator("student_offer_submitted_at", mode="before")
    @classmethod
    def validate_student_offer_submitted_at(cls, value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    @field_validator("hackathon_score", mode="before")
    @classmethod
    def validate_hackathon_score(cls, value: Any) -> float | None:
        if value is None or value == "":
            return None
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("夏令营评分必须为数字") from exc
        if score < 0 or score > 100:
            raise ValueError("夏令营评分必须在 0~100 之间")
        return round(score, 2)

    @field_validator("hackathon_comments", mode="before")
    @classmethod
    def validate_hackathon_comments(cls, value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    @field_validator("accepted", mode="before")
    @classmethod
    def validate_accepted(cls, value: Any) -> str | None:
        if value is None or value == "":
            return None
        text = str(value).strip()
        if not text:
            return None
        if text not in HACKATHON_ACCEPTED_VALUES:
            allowed = "、".join(sorted(HACKATHON_ACCEPTED_VALUES))
            raise ValueError(f"入取状态 accepted 必须是字典 hackathon_accepted_status 中的有效值(允许: {allowed})")
        return text

    @field_validator("admission_offered_school", mode="before")
    @classmethod
    def validate_admission_offered_school(cls, value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        if not text:
            return None
        if len(text) > 64:
            text = text[:64]
        return text


class CampOfferListResponse(PaginationResponseBase):
    items: list[CampOfferRecord]


class CampOfferStats(BaseModel):
    """Headline counts for the camp-offer workbench.

    * ``sent_mail``: rows with ``is_sent_mail = true`` (operator already
      sent the notification email).
    * ``agreed``: rows with ``is_agree = true`` (student confirmed).
    * ``declined``: rows with ``is_agree = false`` (student declined).
    * ``unsigned``: rows with no ``student_offer_submitted_at`` (student
      has not submitted the offer-confirmation form yet).
    * ``total``: total rows considered (after applying the same filters
      as the list endpoint, minus pagination).
    """

    sent_mail: int = 0
    agreed: int = 0
    declined: int = 0
    unsigned: int = 0
    total: int = 0


class CampOfferImportIssue(BaseModel):
    row_number: int
    candidate_no: str | None = None
    reason: str


class CampOfferImportResult(BaseModel):
    imported_count: int
    skipped_count: int
    plan_id: int
    imported_ids: list[int]
    issues: list[CampOfferImportIssue]


# 2026-07-03: 黑客松夏令营「评分导入」专用结果
# 与 CampOfferImportResult 不同:
#   - 通过 手机号 + 邮箱 联合匹配入营名单记录
#   - 只更新 hackathon_score / hackathon_comments 两个字段 (Q4: 无条件覆盖)
#   - 匹配不到的记录 (Q3: A 跳过并在结果中报告) 不算失败, 仅记录
class HackathonScoreImportIssue(BaseModel):
    row_number: int
    phone: str | None = None
    email: str | None = None
    reason: str


class HackathonScoreImportResult(BaseModel):
    """黑客松评分导入结果。

    字段说明:
        - total_rows:    Excel 中非空数据行总数
        - matched_count: 成功匹配到入营名单并已 UPDATE 的行数
        - unmatched_count: 手机号+邮箱联合匹配不到入营名单的行数 (Q3: 跳过)
        - updated_ids:   被更新的入营名单主键 id 列表
        - issues:        失败/未匹配行的明细
    """
    total_rows: int = 0
    matched_count: int = 0
    unmatched_count: int = 0
    updated_ids: list[int] = []
    issues: list[HackathonScoreImportIssue] = []

# 2026-07-06: 录取学校导入 (Excel -> 仅更新 admission_offered_school)
# 区别于 CampOfferImportResult / HackathonScoreImportResult:
#   - 通过 手机号 + 邮箱 联合匹配入营名单
#   - 仅更新 admission_offered_school (dtlms_plan_offer.admission_offered_school varchar(64))
#   - 匹配不到 -> 跳过并在 issues 中报告 (不抛错)
class AdmissionOfferedSchoolImportIssue(BaseModel):
    row_number: int
    phone: str | None = None
    email: str | None = None
    school: str | None = None
    reason: str


class AdmissionOfferedSchoolImportResult(BaseModel):
    u"录取学校导入结果。"

    u"字段说明:"
    u"        - total_rows:    Excel 中非空数据行总数"
    u"        - matched_count: 成功匹配到入营名单并已 UPDATE 的行数"
    u"        - unmatched_count: 手机号+邮箱联合匹配不到入营名单的行数 (跳过)"
    u"        - updated_ids:   被更新的入营名单主键 id 列表"
    u"        - issues:        失败/未匹配行的明细"
    total_rows: int = 0
    matched_count: int = 0
    unmatched_count: int = 0
    updated_ids: list[int] = []
    issues: list[AdmissionOfferedSchoolImportIssue] = []


class RecruitmentOptionsResponse(BaseModel):
    semester_options: list[SelectOption]
    plan_stage_options: list[SelectOption]
    degree_options: list[SelectOption]
    material_status_options: list[SelectOption]
    application_status_options: list[SelectOption]
    intended_field_options: list[SelectOption]
    advisor_options: list[SelectOption]
    reviewer_options: list[SelectOption]
    graduation_school_options: list[SelectOption]


class RecruitStats(BaseModel):
    plan_count: int
    open_plan_count: int
    application_total: int
    pending_review_total: int
    pre_admit_total: int



class CampOfferNotificationSendRequest(BaseModel):
    candidate_nos: list[str] = Field(default_factory=list)
    choice: str = Field(default="first")
    template_id: str | int | None = None
    simulate: bool = False
    simulate_recipient: str | None = None

    @field_validator("candidate_nos", mode="before")
    @classmethod
    def validate_candidate_nos(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            value = [item for item in value.split(",")]
        if not isinstance(value, list):
            raise ValueError("candidate_nos 必须是字符串列表")
        cleaned: list[str] = []
        for item in value:
            text = str(item or "").strip()
            if text and text not in cleaned:
                cleaned.append(text)
        return cleaned

    @field_validator("choice", mode="before")
    @classmethod
    def validate_choice(cls, value: Any) -> str:
        if value is None:
            return "first"
        text = str(value or "").strip().lower()
        if text not in {"first", "second"}:
            raise ValueError("choice 只能是 first 或 second")
        return text

    @field_validator("template_id", mode="before")
    @classmethod
    def validate_template_id(cls, value: Any) -> str | int | None:
        if value is None or value == "":
            return None
        if isinstance(value, bool):
            raise ValueError("template_id 必须是字符串或数字")
        if isinstance(value, int):
            return value
        text = str(value).strip()
        if not text:
            return None
        if text.lower() in {"first", "second"}:
            return text.lower()
        # Uploaded templates are identified by a free-form alphanumeric
        # token (e.g. uuid4 hex or a numeric id) produced by the
        # /recruitment/camp-offers/templates upload endpoint. Accept any
        # safe slug; the service layer is responsible for resolving the
        # id back to a concrete file on disk.
        if all(ch.isalnum() or ch in {"-", "_"} for ch in text) and len(text) <= 128:
            return text
        raise ValueError("template_id 必须是 first / second 或字母数字组合")

    @field_validator("simulate_recipient", mode="before")
    @classmethod
    def validate_simulate_recipient(cls, value: Any) -> str | None:
        text = str(value or "").strip()
        return text or None

    @model_validator(mode="after")
    def validate_request(self) -> "CampOfferNotificationSendRequest":
        if not self.candidate_nos:
            raise ValueError("candidate_nos 至少需要一个报名号")
        if self.simulate and not self.simulate_recipient:
            raise ValueError("模拟发送时必须填写 simulate_recipient")
        return self


class CampOfferNotificationSendResultItem(BaseModel):
    candidate_no: str
    email: str = ""
    status: str
    error: str = ""


class CampOfferNotificationSendResponse(BaseModel):
    message: str
    choice: str
    simulate: bool
    simulate_recipient: str | None = None
    template_path: str | None = None
    success_count: int = 0
    failure_count: int = 0
    results: list[CampOfferNotificationSendResultItem] = Field(default_factory=list)


class OfferTemplateRecord(BaseModel):
    """A single offer-mail template entry (system builtin or user-uploaded)."""

    id: str | int
    filename: str
    display_name: str
    size_bytes: int = 0
    uploaded_at: str | None = None
    uploaded_by: str | None = None
    is_builtin: bool = False
    source: str = Field(default="uploaded")
    builtin_key: str | None = None

    @field_validator("source", mode="before")
    @classmethod
    def validate_source(cls, value: Any) -> str:
        text = str(value or "").strip().lower()
        if text not in {"builtin", "uploaded"}:
            raise ValueError("source 只能是 builtin 或 uploaded")
        return text


class OfferTemplateListResponse(BaseModel):
    items: list[OfferTemplateRecord] = Field(default_factory=list)


