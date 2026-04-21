from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.student import (
    CenterListResponse,
    CenterRecord,
    CenterUpsert,
    RegisteredPortalStudentActionResponse,
    RegisteredPortalStudentEmailRequest,
    RegisteredPortalStudentListResponse,
    StudentLifecycleBoard,
    StudentManagementResponse,
    StudentOptionsResponse,
    StudentRecord,
    StudentStats,
    StudentUpsert,
)
from app.schemas.system import BulkActionResponse, BulkDeleteRequest
from app.services.dashboard_service import (
    activate_registered_portal_student,
    create_center,
    create_student,
    deactivate_registered_portal_student,
    delete_center,
    delete_centers,
    delete_student,
    get_student_lifecycle_board,
    get_center_list,
    get_registered_portal_student_list,
    get_student_management_list,
    get_student_options,
    get_student_stats,
    reset_registered_portal_student_password,
    send_registered_portal_student_email,
    update_center,
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
    center_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("students:read")),
) -> StudentManagementResponse:
    return get_student_management_list(keyword=keyword, status=status_filter, advisor_name=advisor_name, center_name=center_name, page=page, page_size=page_size)


@router.get("/portal-registrations", response_model=RegisteredPortalStudentListResponse)
def registered_portal_student_list(
    keyword: str | None = Query(default=None),
    application_form_status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("students:read")),
) -> RegisteredPortalStudentListResponse:
    return get_registered_portal_student_list(
        keyword=keyword,
        application_form_status=application_form_status,
        page=page,
        page_size=page_size,
    )


@router.post("/portal-registrations/{student_id}/deactivate", response_model=RegisteredPortalStudentActionResponse)
def deactivate_registered_portal_student_record(
    student_id: int,
    principal: Principal = Depends(require_permissions("students:write")),
) -> RegisteredPortalStudentActionResponse:
    try:
        return deactivate_registered_portal_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/portal-registrations/{student_id}/activate", response_model=RegisteredPortalStudentActionResponse)
def activate_registered_portal_student_record(
    student_id: int,
    principal: Principal = Depends(require_permissions("students:write")),
) -> RegisteredPortalStudentActionResponse:
    try:
        return activate_registered_portal_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/portal-registrations/{student_id}/reset-password", response_model=RegisteredPortalStudentActionResponse)
def reset_registered_portal_student_password_record(
    student_id: int,
    principal: Principal = Depends(require_permissions("students:write")),
) -> RegisteredPortalStudentActionResponse:
    try:
        return reset_registered_portal_student_password(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/portal-registrations/{student_id}/send-email", response_model=RegisteredPortalStudentActionResponse)
def send_registered_portal_student_email_record(
    student_id: int,
    payload: RegisteredPortalStudentEmailRequest,
    principal: Principal = Depends(require_permissions("students:write")),
) -> RegisteredPortalStudentActionResponse:
    try:
        return send_registered_portal_student_email(student_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


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


@router.get("/centers", response_model=CenterListResponse)
@router.get("/teams", response_model=CenterListResponse, include_in_schema=False)
def center_list(
    keyword: str | None = Query(default=None),
    is_enabled: bool | None = Query(default=None),
    director_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("students:read")),
) -> CenterListResponse:
    return get_center_list(
        keyword=keyword,
        is_enabled=is_enabled,
        director_name=director_name,
        page=page,
        page_size=page_size,
    )


@router.post("/centers", response_model=CenterRecord, status_code=status.HTTP_201_CREATED)
@router.post("/teams", response_model=CenterRecord, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_center_record(payload: CenterUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> CenterRecord:
    try:
        return create_center(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/centers/{center_id}", response_model=CenterRecord)
@router.put("/teams/{center_id}", response_model=CenterRecord, include_in_schema=False)
def update_center_record(center_id: int, payload: CenterUpsert, principal: Principal = Depends(require_permissions("students:write"))) -> CenterRecord:
    try:
        return update_center(center_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Center not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/centers/{center_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/teams/{center_id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_center_record(center_id: int, principal: Principal = Depends(require_permissions("students:write"))) -> None:
    try:
        delete_center(center_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Center not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/centers/batch-delete", response_model=BulkActionResponse)
@router.post("/teams/batch-delete", response_model=BulkActionResponse, include_in_schema=False)
def batch_delete_center_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("students:write"))) -> BulkActionResponse:
    try:
        return delete_centers(payload.ids)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Center not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
