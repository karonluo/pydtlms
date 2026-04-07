from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.student import (
    StudentLifecycleBoard,
    StudentManagementResponse,
    StudentOptionsResponse,
    StudentRecord,
    StudentStats,
    StudentUpsert,
    TeamListResponse,
    TeamRecord,
    TeamUpsert,
)
from app.schemas.system import BulkActionResponse, BulkDeleteRequest
from app.services.dashboard_service import (
    create_team,
    create_student,
    delete_team,
    delete_teams,
    delete_student,
    get_student_lifecycle_board,
    get_student_management_list,
    get_student_options,
    get_student_stats,
    get_team_list,
    update_team,
    update_student,
)


router = APIRouter(prefix="/students", tags=["students"])


@router.get("/lifecycle", response_model=StudentLifecycleBoard)
def student_lifecycle(principal: Principal = Depends(require_permissions("students:read"))) -> StudentLifecycleBoard:
    return get_student_lifecycle_board()


@router.get("/management", response_model=StudentManagementResponse)
def student_management_list(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    advisor_name: str | None = Query(default=None),
    team_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("students:read")),
) -> StudentManagementResponse:
    return get_student_management_list(keyword=keyword, status=status_filter, advisor_name=advisor_name, team_name=team_name, page=page, page_size=page_size)


@router.get("/options", response_model=StudentOptionsResponse)
def student_options(principal: Principal = Depends(require_permissions("students:read"))) -> StudentOptionsResponse:
    return get_student_options()


@router.get("/management/stats", response_model=StudentStats)
def student_management_stats(principal: Principal = Depends(require_permissions("students:read"))) -> StudentStats:
    return get_student_stats()


@router.post("/management", response_model=StudentRecord, status_code=status.HTTP_201_CREATED)
def create_student_record(payload: StudentUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> StudentRecord:
    return create_student(payload)


@router.put("/management/{student_id}", response_model=StudentRecord)
def update_student_record(student_id: int, payload: StudentUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> StudentRecord:
    try:
        return update_student(student_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found") from exc


@router.delete("/management/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_record(student_id: int, principal: Principal = Depends(require_permissions("students:write"))) -> None:
    try:
        delete_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found") from exc


@router.get("/teams", response_model=TeamListResponse)
def team_list(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    department_name: str | None = Query(default=None),
    lead_advisor_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("students:read")),
) -> TeamListResponse:
    return get_team_list(
        keyword=keyword,
        status=status_filter,
        department_name=department_name,
        lead_advisor_name=lead_advisor_name,
        page=page,
        page_size=page_size,
    )


@router.post("/teams", response_model=TeamRecord, status_code=status.HTTP_201_CREATED)
def create_team_record(payload: TeamUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> TeamRecord:
    try:
        return create_team(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/teams/{team_id}", response_model=TeamRecord)
def update_team_record(team_id: int, payload: TeamUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> TeamRecord:
    try:
        return update_team(team_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_record(team_id: int, principal: Principal = Depends(require_permissions("students:write"))) -> None:
    try:
        delete_team(team_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/teams/batch-delete", response_model=BulkActionResponse)
def batch_delete_team_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("students:write"))) -> BulkActionResponse:
    try:
        return delete_teams(payload.ids)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
