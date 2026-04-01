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
