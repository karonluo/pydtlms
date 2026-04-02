from pydantic import BaseModel

from app.schemas.system import SelectOption


class TrainingTask(BaseModel):
    title: str
    owner: str
    due_text: str
    status: str


class TrainingWorkbench(BaseModel):
    open_tasks: list[TrainingTask]
    supervision_rules: list[dict[str, str]]
    outbound_study_status: list[dict[str, str | int]]


class DegreeWorkbench(BaseModel):
    thesis_pipeline: list[dict[str, str | int]]
    committee_tasks: list[TrainingTask]


class TrainingPlanRecord(BaseModel):
    id: int
    student_no: str
    student_name: str
    advisor_name: str
    version_no: str
    report_cycle: str
    plan_status: str
    scientific_goal: str
    assessment_rule: str


class TrainingPlanUpsert(BaseModel):
    student_no: str
    student_name: str
    advisor_name: str
    version_no: str
    report_cycle: str
    plan_status: str
    scientific_goal: str
    assessment_rule: str


class TrainingPlanListResponse(BaseModel):
    items: list[TrainingPlanRecord]
    total: int


class ScientificReportRecord(BaseModel):
    id: int
    student_no: str
    student_name: str
    period_label: str
    report_status: str
    reviewer_name: str | None = None
    review_score: float | None = None
    summary: str


class ScientificReportUpsert(BaseModel):
    student_no: str
    student_name: str
    period_label: str
    report_status: str
    reviewer_name: str | None = None
    review_score: float | None = None
    summary: str


class ScientificReportListResponse(BaseModel):
    items: list[ScientificReportRecord]
    total: int


class OutboundStudyRecord(BaseModel):
    id: int
    student_no: str
    student_name: str
    advisor_name: str
    study_type: str
    destination: str
    start_date: str
    end_date: str
    approval_status: str
    expected_outcome: str | None = None


class OutboundStudyUpsert(BaseModel):
    student_no: str
    student_name: str
    advisor_name: str
    study_type: str
    destination: str
    start_date: str
    end_date: str
    approval_status: str
    expected_outcome: str | None = None


class OutboundStudyListResponse(BaseModel):
    items: list[OutboundStudyRecord]
    total: int


class TrainingStudentOption(BaseModel):
    student_no: str
    student_name: str
    advisor_name: str
    label: str


class TrainingOptionsResponse(BaseModel):
    plan_status_options: list[SelectOption]
    report_cycle_options: list[SelectOption]
    report_status_options: list[SelectOption]
    study_type_options: list[SelectOption]
    approval_status_options: list[SelectOption]
    advisor_options: list[SelectOption]
    reviewer_options: list[SelectOption]
    student_options: list[TrainingStudentOption]


class TrainingStats(BaseModel):
    training_plan_total: int
    pending_confirmation_total: int
    report_pending_total: int
    outbound_active_total: int


class ThesisRecord(BaseModel):
    id: int
    student_no: str
    student_name: str
    advisor_name: str
    title: str
    plagiarism_rate: float | None = None
    thesis_status: str
    blind_review_status: str
    defense_status: str
    degree_status: str


class ThesisUpsert(BaseModel):
    student_no: str
    student_name: str
    advisor_name: str
    title: str
    plagiarism_rate: float | None = None
    thesis_status: str
    blind_review_status: str
    defense_status: str
    degree_status: str


class ThesisListResponse(BaseModel):
    items: list[ThesisRecord]
    total: int


class ThesisReviewRecord(BaseModel):
    id: int
    thesis_id: int
    thesis_title: str
    expert_name: str
    review_score: float | None = None
    review_status: str
    review_comment: str | None = None


class ThesisReviewUpsert(BaseModel):
    thesis_id: int
    thesis_title: str
    expert_name: str
    review_score: float | None = None
    review_status: str
    review_comment: str | None = None


class ThesisReviewListResponse(BaseModel):
    items: list[ThesisReviewRecord]
    total: int


class DegreeOptionsResponse(BaseModel):
    student_options: list[SelectOption]
    advisor_options: list[SelectOption]
    thesis_options: list[SelectOption]
    thesis_status_options: list[SelectOption]
    blind_review_status_options: list[SelectOption]
    defense_status_options: list[SelectOption]
    degree_status_options: list[SelectOption]
    expert_options: list[SelectOption]
    review_status_options: list[SelectOption]


class DegreeStats(BaseModel):
    thesis_total: int
    plagiarism_pending_total: int
    blind_review_pending_total: int
    defense_pending_total: int
    degree_granted_total: int
