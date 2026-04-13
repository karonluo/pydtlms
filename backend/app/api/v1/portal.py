from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.portal_security import create_portal_access_token, portal_bearer, resolve_portal_student_id
from app.schemas.portal import (
    PortalApplicationSubmissionResponse,
    PortalApplicationUpsert,
    PortalLoginRequest,
    PortalPlanListResponse,
    PortalPasswordResetRequest,
    PortalRegistrationRequest,
    PortalRegistrationResponse,
    PortalSessionResponse,
    PortalStudentRecord,
    PortalTeamListResponse,
)
from app.services.dashboard_service import (
    get_portal_student,
    get_public_recruitment_plans,
    get_public_teams,
    login_portal_student,
    register_portal_student,
    reset_portal_student_password,
    submit_portal_application,
)


router = APIRouter(prefix="/portal", tags=["portal"])


def get_current_portal_student_id(credentials: HTTPAuthorizationCredentials | None = Depends(portal_bearer)) -> int:
    return resolve_portal_student_id(credentials)


@router.post("/register", response_model=PortalRegistrationResponse, status_code=status.HTTP_201_CREATED)
def portal_register(payload: PortalRegistrationRequest) -> PortalRegistrationResponse:
    try:
        return register_portal_student(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=PortalSessionResponse)
def portal_login(payload: PortalLoginRequest) -> PortalSessionResponse:
    try:
        student = login_portal_student(payload)
        return PortalSessionResponse(
            access_token=create_portal_access_token(student_id=student.id, full_name=student.full_name),
            student=student,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/forgot-password")
def portal_forgot_password(payload: PortalPasswordResetRequest) -> dict[str, str]:
    try:
        reset_portal_student_password(payload)
        return {"message": "密码已重置，请重新登录"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/me", response_model=PortalStudentRecord)
def portal_me(student_id: int = Depends(get_current_portal_student_id)) -> PortalStudentRecord:
    try:
        return get_portal_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc


@router.get("/plans", response_model=PortalPlanListResponse)
def portal_plans(student_id: int = Depends(get_current_portal_student_id)) -> PortalPlanListResponse:
    return get_public_recruitment_plans()


@router.get("/teams", response_model=PortalTeamListResponse)
def portal_teams(student_id: int = Depends(get_current_portal_student_id)) -> PortalTeamListResponse:
    return get_public_teams()


@router.post("/applications", response_model=PortalApplicationSubmissionResponse)
def portal_submit_application(
    payload: PortalApplicationUpsert,
    student_id: int = Depends(get_current_portal_student_id),
) -> PortalApplicationSubmissionResponse:
    try:
        return submit_portal_application(student_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
