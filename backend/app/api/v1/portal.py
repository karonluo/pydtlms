from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.portal_security import create_portal_access_token, portal_bearer, resolve_portal_student_id
from app.core.config import settings
from app.schemas.portal import (
    PortalApplicationDraftSaveResponse,
    PortalApplicationDraftUpsert,
    PortalAttachmentUploadResponse,
    PortalEmailCodeLoginRequest,
    PortalLoginEmailCodeRequest,
    PortalPublicConfigResponse,
    PortalApplicationSubmissionResponse,
    PortalApplicationUpsert,
    PortalLoginRequest,
    PortalPasswordChangeRequest,
    PortalPlanListResponse,
    PortalProfileOptionsResponse,
    PortalPasswordResetRequest,
    PortalRegistrationEmailCodeRequest,
    PortalRegistrationEmailCodeResponse,
    PortalRegistrationRequest,
    PortalRegistrationResponse,
    PortalSessionResponse,
    PortalStudentRecord,
    PortalTeamListResponse,
)
from app.services.dashboard_service import (
    change_portal_student_password,
    get_portal_profile_options,
    get_portal_student,
    get_public_recruitment_plans,
    get_public_teams,
    login_portal_student,
    login_portal_student_by_email_code,
    clear_portal_registration_email_code,
    register_portal_student,
    reset_portal_student_password,
    save_portal_application_draft,
    send_portal_login_email_code,
    send_portal_registration_email_code,
    submit_portal_application,
    validate_portal_registration_email_code,
)


router = APIRouter(prefix="/portal", tags=["portal"])
PROJECT_ROOT = Path(__file__).resolve().parents[4]
PORTAL_ATTACHMENT_UPLOAD_DIR = PROJECT_ROOT / "frontend" / "public" / "portal-attachments" / "uploads"
PORTAL_ATTACHMENT_EXTENSIONS: dict[str, set[str]] = {
    "education_transcript": {".pdf", ".png", ".jpg", ".jpeg", ".webp"},
    "education_degree_certificate": {".pdf", ".png", ".jpg", ".jpeg", ".webp"},
    "education_graduation_certificate": {".pdf", ".png", ".jpg", ".jpeg", ".webp"},
    "english_certificate": {".pdf", ".png", ".jpg", ".jpeg", ".webp"},
    "achievement_award_certificate": {".pdf", ".png", ".jpg", ".jpeg", ".webp"},
    "profile_photo": {".png", ".jpg", ".jpeg", ".webp"},
    "id_card_collage": {".jpg", ".jpeg"},
    "resume": {".pdf", ".doc", ".docx"},
    "supporting_material": {".zip", ".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".webp"},
}
PORTAL_ATTACHMENT_CONTENT_TYPES: dict[str, tuple[str, ...]] = {
    "education_transcript": ("application/pdf", "image/"),
    "education_degree_certificate": ("application/pdf", "image/"),
    "education_graduation_certificate": ("application/pdf", "image/"),
    "english_certificate": ("application/pdf", "image/"),
    "achievement_award_certificate": ("application/pdf", "image/"),
    "profile_photo": ("image/",),
    "id_card_collage": ("image/",),
    "resume": (
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ),
    "supporting_material": (
        "application/pdf",
        "application/zip",
        "application/x-zip-compressed",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/",
    ),
}
PORTAL_ATTACHMENT_MAX_SIZES: dict[str, int] = {
    "profile_photo": 1 * 1024 * 1024,
    "id_card_collage": 5 * 1024 * 1024,
}
PORTAL_ATTACHMENT_DEFAULT_MAX_SIZE = 20 * 1024 * 1024
PORTAL_ATTACHMENT_GENERIC_CONTENT_TYPES = {
    "application/octet-stream",
    "binary/octet-stream",
    "application/x-msdownload",
    "application/unknown",
}


def get_current_portal_student_id(credentials: HTTPAuthorizationCredentials | None = Depends(portal_bearer)) -> int:
    return resolve_portal_student_id(credentials)


def get_current_active_portal_student_id(student_id: int = Depends(get_current_portal_student_id)) -> int:
    try:
        student = get_portal_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc
    if student.account_status != "启用":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账号已停用，请联系管理员")
    return student_id


def ensure_portal_application_v2_available() -> None:
    if settings.portal_application_v2_blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=settings.portal_application_v2_block_message,
        )


def _validate_portal_attachment(file: UploadFile, category: str) -> str:
    allowed_extensions = PORTAL_ATTACHMENT_EXTENSIONS.get(category)
    if not allowed_extensions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不支持的附件分类")

    suffix = Path(file.filename or "attachment.dat").suffix.lower()
    if suffix not in allowed_extensions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="附件格式不受支持")

    content_type = str(file.content_type or "")
    allowed_content_types = PORTAL_ATTACHMENT_CONTENT_TYPES.get(category, ())
    if content_type and content_type not in PORTAL_ATTACHMENT_GENERIC_CONTENT_TYPES:
        matched = any(content_type.startswith(prefix) for prefix in allowed_content_types)
        if not matched:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="附件类型不受支持")

    return suffix


@router.post("/register", response_model=PortalRegistrationResponse, status_code=status.HTTP_201_CREATED)
def portal_register(payload: PortalRegistrationRequest) -> PortalRegistrationResponse:
    if not payload.email_verification_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="请先填写邮件验证码")
    try:
        validate_portal_registration_email_code(payload.email, payload.email_verification_code)
        response = register_portal_student(payload)
        clear_portal_registration_email_code(payload.email)
        return response
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.post("/register/email-code", response_model=PortalRegistrationEmailCodeResponse)
def portal_send_registration_email_code(payload: PortalRegistrationEmailCodeRequest) -> PortalRegistrationEmailCodeResponse:
    try:
        return send_portal_registration_email_code(payload.email)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.post("/login/email-code/send", response_model=PortalRegistrationEmailCodeResponse)
def portal_send_login_email_code(payload: PortalLoginEmailCodeRequest) -> PortalRegistrationEmailCodeResponse:
    try:
        return send_portal_login_email_code(payload.email)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


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


@router.post("/login/email-code", response_model=PortalSessionResponse)
def portal_login_by_email_code(payload: PortalEmailCodeLoginRequest) -> PortalSessionResponse:
    try:
        student = login_portal_student_by_email_code(payload.email, payload.email_verification_code)
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
def portal_me(student_id: int = Depends(get_current_active_portal_student_id)) -> PortalStudentRecord:
    try:
        return get_portal_student(student_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portal student not found") from exc


@router.get("/profile-options", response_model=PortalProfileOptionsResponse)
def portal_profile_options(student_id: int = Depends(get_current_active_portal_student_id)) -> PortalProfileOptionsResponse:
    return get_portal_profile_options()


@router.post("/change-password")
def portal_change_password(
    payload: PortalPasswordChangeRequest,
    student_id: int = Depends(get_current_active_portal_student_id),
) -> dict[str, str]:
    try:
        change_portal_student_password(student_id, payload)
        return {"message": "密码修改成功，请使用新密码继续登录"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/plans", response_model=PortalPlanListResponse)
def portal_plans(student_id: int = Depends(get_current_active_portal_student_id)) -> PortalPlanListResponse:
    return get_public_recruitment_plans()


@router.get("/teams", response_model=PortalTeamListResponse)
def portal_teams(student_id: int = Depends(get_current_active_portal_student_id)) -> PortalTeamListResponse:
    return get_public_teams()


@router.get("/public-config", response_model=PortalPublicConfigResponse)
def portal_public_config(student_id: int = Depends(get_current_active_portal_student_id)) -> PortalPublicConfigResponse:
    del student_id
    return PortalPublicConfigResponse(
        portal_admissions_info_url=settings.portal_admissions_info_url,
        portal_application_v2_blocked=settings.portal_application_v2_blocked,
        portal_application_v2_block_message=settings.portal_application_v2_block_message,
    )


@router.post("/attachments/upload", response_model=PortalAttachmentUploadResponse)
async def portal_upload_attachment(
    category: str = Form(...),
    file: UploadFile = File(...),
    student_id: int = Depends(get_current_active_portal_student_id),
) -> PortalAttachmentUploadResponse:
    suffix = _validate_portal_attachment(file, category)
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="附件内容不能为空")
    max_size = PORTAL_ATTACHMENT_MAX_SIZES.get(category, PORTAL_ATTACHMENT_DEFAULT_MAX_SIZE)
    if len(content) > max_size:
        detail = "照片大小不能超过 1MB" if category == "profile_photo" else "附件大小不能超过 20MB"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    target_dir = PORTAL_ATTACHMENT_UPLOAD_DIR / f"student-{student_id}" / category
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{category}-{uuid4().hex}{suffix}"
    target = target_dir / filename
    target.write_bytes(content)

    original_name = Path(file.filename or filename).name or filename
    return PortalAttachmentUploadResponse(
        category=category,
        file_name=original_name,
        file_type=str(file.content_type or "") or None,
        file_size=len(content),
        url=f"/portal-attachments/uploads/student-{student_id}/{category}/{filename}",
    )


@router.post("/applications", response_model=PortalApplicationSubmissionResponse)
def portal_submit_application(
    payload: PortalApplicationUpsert,
    student_id: int = Depends(get_current_active_portal_student_id),
) -> PortalApplicationSubmissionResponse:
    ensure_portal_application_v2_available()
    try:
        return submit_portal_application(student_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/applications/draft", response_model=PortalApplicationDraftSaveResponse)
def portal_save_application_draft(
    payload: PortalApplicationDraftUpsert,
    student_id: int = Depends(get_current_active_portal_student_id),
) -> PortalApplicationDraftSaveResponse:
    ensure_portal_application_v2_available()
    try:
        student = save_portal_application_draft(student_id, payload)
        return PortalApplicationDraftSaveResponse(message="草稿已保存", student=student)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
