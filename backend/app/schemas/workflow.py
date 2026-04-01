from pydantic import BaseModel


class WorkflowTaskRecord(BaseModel):
    id: int
    workflow_name: str
    business_module: str
    business_key: str
    title: str
    applicant_name: str
    current_handler: str
    current_node: str
    priority: str
    status: str
    created_at: str
    due_at: str
    form_summary: str
    latest_comment: str | None = None


class WorkflowTaskUpsert(BaseModel):
    workflow_name: str
    business_module: str
    business_key: str
    title: str
    applicant_name: str
    current_handler: str
    current_node: str
    priority: str
    status: str
    created_at: str
    due_at: str
    form_summary: str
    latest_comment: str | None = None


class WorkflowTaskListResponse(BaseModel):
    items: list[WorkflowTaskRecord]
    total: int


class WorkflowStats(BaseModel):
    todo_total: int
    in_progress_total: int
    approved_total: int
    rejected_total: int
    overdue_total: int