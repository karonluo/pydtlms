from pydantic import BaseModel


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


class RecruitPlanUpsert(BaseModel):
    plan_name: str
    academic_year: str
    semester: str
    current_stage: str
    target_quota: int
    interview_group_count: int
    is_open: bool


class RecruitPlanListResponse(BaseModel):
    items: list[RecruitPlanRecord]
    total: int


class RecruitApplicationRecord(BaseModel):
    id: int
    plan_id: int
    candidate_no: str
    student_name: str
    graduation_school: str
    highest_degree: str
    intended_field: str
    material_status: str
    application_status: str
    reviewer_name: str | None = None
    final_score: float | None = None


class RecruitApplicationUpsert(BaseModel):
    plan_id: int
    candidate_no: str
    student_name: str
    graduation_school: str
    highest_degree: str
    intended_field: str
    material_status: str
    application_status: str
    reviewer_name: str | None = None
    final_score: float | None = None


class RecruitApplicationListResponse(BaseModel):
    items: list[RecruitApplicationRecord]
    total: int


class RecruitStats(BaseModel):
    plan_count: int
    open_plan_count: int
    application_total: int
    pending_review_total: int
    pre_admit_total: int
