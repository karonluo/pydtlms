from pydantic import BaseModel


class MetricCard(BaseModel):
    label: str
    value: str
    target: str | None = None
    trend: str | None = None
    status: str


class DashboardAlert(BaseModel):
    level: str
    title: str
    owner: str
    due_text: str


class DashboardOverview(BaseModel):
    lifecycle_coverage: list[MetricCard]
    recruitment_metrics: list[MetricCard]
    training_metrics: list[MetricCard]
    degree_metrics: list[MetricCard]
    alerts: list[DashboardAlert]
    workflow_metrics: list[MetricCard]


class DashboardRecruitmentApplicationStatusItem(BaseModel):
    application_status_state: str
    count: int


class DashboardRecruitmentApplicationStatusResponse(BaseModel):
    items: list[DashboardRecruitmentApplicationStatusItem]


class DashboardRecruitmentFirstChoicePendingGradingItem(BaseModel):
    advisor_name: str
    student_count: int


class DashboardRecruitmentFirstChoicePendingGradingResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[DashboardRecruitmentFirstChoicePendingGradingItem]


class DashboardRecruitmentSecondChoicePendingGradingItem(BaseModel):
    advisor_name: str
    student_count: int


class DashboardRecruitmentSecondChoicePendingGradingResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[DashboardRecruitmentSecondChoicePendingGradingItem]


class DashboardRecruitmentFirstChoicePendingStudentItem(BaseModel):
    application_id: int
    candidate_no: str
    student_name: str


class DashboardRecruitmentFirstChoicePendingStudentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[DashboardRecruitmentFirstChoicePendingStudentItem]


class DashboardRecruitmentSecondChoicePendingStudentItem(BaseModel):
    application_id: int
    candidate_no: str
    student_name: str


class DashboardRecruitmentSecondChoicePendingStudentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[DashboardRecruitmentSecondChoicePendingStudentItem]


class DashboardUndergraduateSchoolRankingItem(BaseModel):
    school_name: str
    student_count: int


class DashboardUndergraduateSchoolRankingResponse(BaseModel):
    items: list[DashboardUndergraduateSchoolRankingItem]


class DashboardUndergraduateSchoolGroupItem(BaseModel):
    school_name: str
    student_count: int
    percentage: float


class DashboardUndergraduateSchoolGroupDistribution(BaseModel):
    group_name: str
    dict_type: str
    total: int
    items: list[DashboardUndergraduateSchoolGroupItem]


class DashboardUndergraduateSchoolGroupDistributionResponse(BaseModel):
    total_applications: int
    groups: list[DashboardUndergraduateSchoolGroupDistribution]


class DashboardRecruitmentAdvisorChoiceItem(BaseModel):
    advisor_name: str
    student_count: int
    percentage: float


class DashboardRecruitmentAdvisorChoiceDistribution(BaseModel):
    choice_round: str
    choice_name: str
    total: int
    items: list[DashboardRecruitmentAdvisorChoiceItem]


class DashboardRecruitmentAdvisorChoiceDistributionResponse(BaseModel):
    choices: list[DashboardRecruitmentAdvisorChoiceDistribution]


class DashboardUndergraduateSchoolStudentItem(BaseModel):
    recruitment_application_id: int
    student_name: str
    choice_round: str | None = None
    advisor_name: str | None = None
    school_name: str | None = None
    candidate_no: str | None = None
    registered_at: str | None = None
    phone_number: str | None = None
    email: str | None = None


class DashboardUndergraduateSchoolStudentListResponse(BaseModel):
    school_name: str
    total: int
    items: list[DashboardUndergraduateSchoolStudentItem]
