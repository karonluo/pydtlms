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


class DashboardUndergraduateSchoolStudentItem(BaseModel):
    recruitment_application_id: int
    student_name: str
    school_name: str | None = None
    candidate_no: str | None = None
    registered_at: str | None = None
    phone_number: str | None = None
    email: str | None = None


class DashboardUndergraduateSchoolStudentListResponse(BaseModel):
    school_name: str
    total: int
    items: list[DashboardUndergraduateSchoolStudentItem]
