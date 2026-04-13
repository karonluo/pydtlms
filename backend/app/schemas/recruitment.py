from pydantic import BaseModel

from app.schemas.common import PaginationResponseBase, SelectOption


class RecruitPlanSummary(BaseModel):
    plan_name: str
    academic_term: str
    current_stage: str
    application_count: int
    interview_group_count: int


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
    current_stage: str
    target_quota: int
    application_count: int
    interview_group_count: int
    is_open: bool
    brochure_image_url: str | None = None


class RecruitPlanUpsert(BaseModel):
    plan_name: str
    academic_year: str
    semester: str
    current_stage: str
    target_quota: int
    interview_group_count: int
    is_open: bool
    brochure_image_url: str | None = None


class RecruitPlanListResponse(PaginationResponseBase):
    items: list[RecruitPlanRecord]


class RecruitApplicationRecord(BaseModel):
    id: int
    plan_id: int
    business_key: str
    candidate_no: str | None = None
    review_round: str | None = None
    student_name: str
    first_choice: str | None = None
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
    intended_advisor_name: str | None = None
    discovery_channel: str | None = None
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


class RecruitApplicationUpsert(BaseModel):
    plan_id: int
    business_key: str | None = None
    candidate_no: str | None = None
    review_round: str | None = None
    student_name: str
    first_choice: str | None = None
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
    intended_advisor_name: str | None = None
    discovery_channel: str | None = None
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
