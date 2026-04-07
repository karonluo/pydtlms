from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import get_current_principal, require_permissions
from app.schemas.auth import Principal
from app.schemas.workflow import (
    WorkflowOptionsResponse,
    WorkflowStats,
    WorkflowTaskActionRequest,
    WorkflowTaskDetailResponse,
    WorkflowTaskListResponse,
    WorkflowTaskRecord,
    WorkflowTaskUpsert,
)
from app.services.dashboard_service import (
    create_workflow_task,
    delete_workflow_task,
    execute_workflow_task_action,
    get_workflow_options,
    get_workflow_stats,
    get_workflow_task_detail,
    get_workflow_task_list,
    update_workflow_task,
)


router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.get("/stats", response_model=WorkflowStats)
def workflow_stats(principal: Principal = Depends(require_permissions("workflow:read"))) -> WorkflowStats:
    return get_workflow_stats()


@router.get("/options", response_model=WorkflowOptionsResponse)
def workflow_options(principal: Principal = Depends(require_permissions("workflow:read"))) -> WorkflowOptionsResponse:
    return get_workflow_options()


@router.get("/tasks", response_model=WorkflowTaskListResponse)
def workflow_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    module: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("workflow:read")),
) -> WorkflowTaskListResponse:
    return get_workflow_task_list(status=status_filter, module=module, keyword=keyword, page=page, page_size=page_size, principal=principal)


@router.post("/tasks", response_model=WorkflowTaskRecord, status_code=status.HTTP_201_CREATED)
def create_workflow_task_record(payload: WorkflowTaskUpsert, principal: Principal = Depends(require_permissions("workflow:write"))) -> WorkflowTaskRecord:
    return create_workflow_task(payload)


@router.get("/tasks/{task_id}", response_model=WorkflowTaskDetailResponse)
def workflow_task_detail(task_id: int, principal: Principal = Depends(require_permissions("workflow:read"))) -> WorkflowTaskDetailResponse:
    try:
        return get_workflow_task_detail(task_id, principal=principal)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc


@router.put("/tasks/{task_id}", response_model=WorkflowTaskRecord)
def update_workflow_task_record(task_id: int, payload: WorkflowTaskUpsert, principal: Principal = Depends(require_permissions("workflow:write"))) -> WorkflowTaskRecord:
    try:
        return update_workflow_task(task_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/tasks/{task_id}/actions", response_model=WorkflowTaskDetailResponse)
def execute_workflow_task_record_action(
    task_id: int,
    payload: WorkflowTaskActionRequest,
    principal: Principal = Depends(get_current_principal),
) -> WorkflowTaskDetailResponse:
    try:
        return execute_workflow_task_action(task_id, payload, principal=principal)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow_task_record(task_id: int, principal: Principal = Depends(require_permissions("workflow:write"))) -> None:
    try:
        delete_workflow_task(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow task not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc