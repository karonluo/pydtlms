from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.student import StudentLifecycleBoard, StudentManagementResponse, StudentRecord, StudentStats, StudentUpsert
from app.services.dashboard_service import (
    create_student,
    delete_student,
    get_student_lifecycle_board,
    get_student_management_list,
    get_student_stats,
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
    principal: Principal = Depends(require_permissions("students:read")),
) -> StudentManagementResponse:
    return get_student_management_list(keyword=keyword, status=status_filter, advisor_name=advisor_name)


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
