from __future__ import annotations

import json
from typing import Any, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import SelectOption
from app.schemas.contact import validate_email, validate_phone_number
from app.schemas.identity import validate_china_resident_id_number


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


class PortalApplicantProfileData(BaseModel):
    full_name_pinyin: str | None = None
    profile_photo_url: str | None = None
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


class PortalApplicationPreferenceItem(BaseModel):
    preference_order: int = 1
    research_center_name: str
    advisor_name: str | None = None
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
    paper_title: str | None = None
    author_order: str | None = None
    journal_or_conference: str | None = None
    publish_or_index_month: str | None = None
    award_name: str | None = None
    awarding_organization: str | None = None
    award_level: str | None = None
    award_year: str | None = None
    responsibility_text: str | None = None


class PortalPersonalStatementData(BaseModel):
    personal_statement_text: str | None = None
    ai_problem_statement: str | None = None
    ai_industry_opinion: str | None = None
    resume_attachment_url: str | None = None
    resume_attachment_name: str | None = None


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
    selected_team_name: str | None = None
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

        data = dict(raw_value)
        if data.get("profile") is None:
            profile_payload = {
                "profile_photo_url": data.get("profile_photo_url"),
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
                        "research_center_name": data.get("selected_team_name"),
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
    lead_advisor_name: str
    advisor_names: list[str] = Field(default_factory=list)
    department_name: str
    discipline_name: str
    research_directions: list[str] = Field(default_factory=list)
    description: str | None = None


class PortalTeamListResponse(BaseModel):
    items: list[PortalTeamRecord] = Field(default_factory=list)


class PortalProfileOptionsResponse(BaseModel):
    political_status_options: list[SelectOption] = Field(default_factory=list)
    ethnic_group_options: list[SelectOption] = Field(default_factory=list)


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
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_team_name: str | None = None
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None

    @model_validator(mode="after")
    def populate_legacy_fields(self) -> "PortalApplicationUpsert":
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
            self.selected_team_name = self.selected_team_name or primary_preference.research_center_name
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

        if self.declaration is not None:
            self.signed_agreement = self.signed_agreement or self.declaration.has_read_declaration

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
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_team_name: str | None = None
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None

    @model_validator(mode="after")
    def populate_legacy_fields(self) -> "PortalApplicationDraftUpsert":
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
            self.selected_team_name = self.selected_team_name or primary_preference.research_center_name
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

        if self.declaration is not None:
            self.signed_agreement = self.signed_agreement or self.declaration.has_read_declaration

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