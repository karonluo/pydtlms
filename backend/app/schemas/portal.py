from pydantic import BaseModel, Field


class PortalRegistrationRequest(BaseModel):
    phone_number: str
    email: str
    full_name: str
    id_number: str
    password: str


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


class PortalStudentRecord(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    id_number: str
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


class PortalSessionResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: PortalStudentRecord


class PortalPlanRecord(BaseModel):
    id: int
    plan_name: str
    academic_term: str
    current_stage: str
    target_quota: int
    interview_group_count: int
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


class PortalApplicationUpsert(BaseModel):
    plan_id: int
    gender: str | None = None
    birth_date: str | None = None
    ethnic_group: str | None = None
    native_place: str | None = None
    marital_status: str | None = None
    religious_belief: str | None = None
    id_type: str | None = None
    mailing_address: str | None = None
    graduation_school: str
    highest_degree: str
    intended_field: str
    political_status: str | None = None
    english_level: str | None = None
    family_info: str | None = None
    education_experience: str | None = None
    practice_experience: str | None = None
    personal_profile: str | None = None
    recommendation_notes: str | None = None
    personal_statement_text: str | None = None
    signed_agreement: bool = False
    selected_team_name: str
    selected_advisor_name: str | None = None
    self_evaluation: str | None = None


class PortalApplicationSubmissionResponse(BaseModel):
    student: PortalStudentRecord
    application_business_key: str
    application_status: str