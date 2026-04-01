from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.workflow import WorkflowStats, WorkflowTaskListResponse, WorkflowTaskRecord, WorkflowTaskUpsert
from app.services.dashboard_service import (
    create_workflow_task,
    delete_workflow_task,
    get_workflow_stats,
    get_workflow_task_list,
    update_workflow_task,
)


router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.get("/stats", response_model=WorkflowStats)
def workflow_stats(principal: Principal = Depends(require_permissions("workflow:read"))) -> WorkflowStats:
    return get_workflow_stats()


@router.get("/tasks", response_model=WorkflowTaskListResponse)
def workflow_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    module: str | None = Query(default=None),
    principal: Principal = Depends(require_permissions("workflow:read")),
) -> WorkflowTaskListResponse:
    return get_workflow_task_list(status=status_filter, module=module)


@router.post("/tasks", response_model=WorkflowTaskRecord, status_code=status.HTTP_201_CREATED)
def create_workflow_task_record(payload: WorkflowTaskUpsert, principal: Principal = Depends(require_permissions("workflow:write"))) -> WorkflowTaskRecord:
    return create_workflow_task(payload)


@router.put("/tasks/{task_id}", response_model=WorkflowTaskRecord)
def update_workflow_task_record(task_id: int, payload: WorkflowTaskUpsert, principal: Principal = Depends(require_permissions("workflow:write"))) -> WorkflowTaskRecord:
    try:
        return update_workflow_task(task_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow_task_record(task_id: int, principal: Principal = Depends(require_permissions("workflow:write"))) -> None:
    try:
        delete_workflow_task(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc