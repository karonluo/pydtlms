from pydantic import BaseModel

from app.schemas.common import PaginationResponseBase, SelectOption


class WorkflowActionOption(BaseModel):
    action: str
    label: str


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
    available_actions: list[WorkflowActionOption] = []
    process_definition_key: str | None = None
    process_definition_id: str | None = None
    process_instance_id: str | None = None
    execution_id: str | None = None
    task_definition_key: str | None = None


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
    process_definition_key: str | None = None
    process_definition_id: str | None = None
    process_instance_id: str | None = None
    execution_id: str | None = None
    task_definition_key: str | None = None


class WorkflowTaskListResponse(PaginationResponseBase):
    items: list[WorkflowTaskRecord]


class WorkflowTaskActionRequest(BaseModel):
    action: str
    comment: str | None = None


class WorkflowTaskActionLog(BaseModel):
    operated_at: str
    operator_username: str
    operator_full_name: str
    action: str
    action_label: str
    from_node: str
    to_node: str | None = None
    result_status: str
    comment: str | None = None


class WorkflowTaskDetailResponse(BaseModel):
    task: WorkflowTaskRecord
    history: list[WorkflowTaskActionLog]


class WorkflowStats(BaseModel):
    todo_total: int
    in_progress_total: int
    approved_total: int
    rejected_total: int
    overdue_total: int


class WorkflowOptionsResponse(BaseModel):
    workflow_name_options: list[SelectOption]
    business_module_options: list[SelectOption]
    applicant_options: list[SelectOption]
    handler_options: list[SelectOption]
    current_node_options: list[SelectOption]
    priority_options: list[SelectOption]
    status_options: list[SelectOption]