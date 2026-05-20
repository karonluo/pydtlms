from typing import Any

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


def _serialize_models(items: list[BaseModel] | list[dict[str, Any]] | None) -> str | None:
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


class RecruitApplicationRecord(BaseModel):
    id: int
    plan_id: int
    business_key: str
    portal_student_id: int | None = None
    candidate_no: str | None = None
    review_round: str | None = None
    student_name: str
    first_choice_team_id: int | None = None
    first_choice: str | None = None
    second_choice_team_id: int | None = None
    second_choice: str | None = None
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
    reviewer_name: str | None = None
    final_score: float | None = None
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
                        "team_id": data.get("first_choice_team_id"),
                        "research_center_name": data.get("first_choice"),
                        "advisor_user_id": data.get("intended_advisor_user_id"),
                        "advisor_name": data.get("intended_advisor_name"),
                        "is_optional": False,
                    }
                )
            if _first_non_empty(data.get("second_choice")):
                preferences.append(
                    {
                        "preference_order": 2,
                        "team_id": data.get("second_choice_team_id"),
                        "research_center_name": data.get("second_choice"),
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
    first_choice_team_id: int | None = None
    first_choice: str | None = None
    second_choice_team_id: int | None = None
    second_choice: str | None = None
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
            self.first_choice_team_id = self.first_choice_team_id or preferences[0].team_id
            self.first_choice = self.first_choice or preferences[0].research_center_name
            self.intended_advisor_user_id = self.intended_advisor_user_id or preferences[0].advisor_user_id
            self.intended_advisor_name = self.intended_advisor_name or preferences[0].advisor_name
            self.intended_field = self.intended_field or preferences[0].research_center_name
            if len(preferences) > 1:
                self.second_choice_team_id = self.second_choice_team_id or preferences[1].team_id
                self.second_choice = self.second_choice or preferences[1].research_center_name

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

    @model_validator(mode="after")
    def validate_resident_id_number(self) -> "RecruitApplicationUpsert":
        id_number = _first_non_empty(self.id_number)
        if not id_number:
            return self
        id_type = _first_non_empty(self.id_type, self.profile.id_type if self.profile else None)
        if id_type and "身份证" not in id_type:
            return self
        self.id_number = validate_china_resident_id_number(id_number, "居民身份证号码")
        return self


class RecruitApplicationListResponse(PaginationResponseBase):
    items: list[RecruitApplicationRecord]


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


class RecruitmentOptionsResponse(BaseModel):
    semester_options: list[SelectOption]
    plan_stage_options: list[SelectOption]
    degree_options: list[SelectOption]
    material_status_options: list[SelectOption]
    application_status_options: list[SelectOption]
    intended_field_options: list[SelectOption]
    reviewer_options: list[SelectOption]
    graduation_school_options: list[SelectOption]


class RecruitStats(BaseModel):
    plan_count: int
    open_plan_count: int
    application_total: int
    pending_review_total: int
    pre_admit_total: int
