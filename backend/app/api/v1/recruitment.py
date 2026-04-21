from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.recruitment import (
    RecruitApplicationListResponse,
    RecruitApplicationImportResult,
    RecruitApplicationRecord,
    RecruitApplicationUpsert,
    RecruitPlanListResponse,
    RecruitPlanRecord,
    RecruitPlanUpsert,
    RecruitmentOptionsResponse,
    RecruitStats,
    RecruitWorkbench,
)
from app.services.dashboard_service import (
    create_recruitment_application,
    create_recruitment_plan,
    delete_recruitment_application,
    export_recruitment_application_blank_template,
    export_recruitment_applications,
    get_recruitment_application_list,
    get_recruitment_options,
    get_recruitment_plan_list,
    get_recruitment_stats,
    get_recruitment_workbench,
    import_recruitment_applications,
    update_recruitment_application,
    update_recruitment_plan,
)
from app.services.recruitment_excel_service import parse_recruitment_template


router = APIRouter(prefix="/recruitment", tags=["recruitment"])
PROJECT_ROOT = Path(__file__).resolve().parents[4]
BROCHURE_UPLOAD_DIR = PROJECT_ROOT / "frontend" / "public" / "portal-brochures" / "uploads"


@router.get("/workbench", response_model=RecruitWorkbench)
def recruitment_workbench(principal: Principal = Depends(require_permissions("recruitment:read"))) -> RecruitWorkbench:
    return get_recruitment_workbench()


@router.get("/stats", response_model=RecruitStats)
def recruitment_stats(principal: Principal = Depends(require_permissions("recruitment:read"))) -> RecruitStats:
    return get_recruitment_stats()


@router.get("/options", response_model=RecruitmentOptionsResponse)
def recruitment_options(principal: Principal = Depends(require_permissions("recruitment:read"))) -> RecruitmentOptionsResponse:
    return get_recruitment_options()


@router.get("/plans", response_model=RecruitPlanListResponse)
def recruitment_plans(
    keyword: str | None = Query(default=None),
    semester: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("recruitment:read")),
) -> RecruitPlanListResponse:
    return get_recruitment_plan_list(keyword=keyword, semester=semester, page=page, page_size=page_size)


@router.post("/plans", response_model=RecruitPlanRecord, status_code=status.HTTP_201_CREATED)
def create_recruitment_plan_record(payload: RecruitPlanUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitPlanRecord:
    return create_recruitment_plan(payload)


@router.put("/plans/{plan_id}", response_model=RecruitPlanRecord)
def update_recruitment_plan_record(plan_id: int, payload: RecruitPlanUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitPlanRecord:
    try:
        return update_recruitment_plan(plan_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruitment plan not found") from exc


@router.post("/plans/brochure-upload")
async def upload_recruitment_brochure_image(
    file: UploadFile = File(...),
    principal: Principal = Depends(require_permissions("recruitment:write")),
) -> dict[str, str]:
    content_type = str(file.content_type or "")
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持上传图片文件")

    suffix = Path(file.filename or "brochure.png").suffix.lower() or ".png"
    if suffix not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="图片格式不受支持")

    BROCHURE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"brochure-{uuid4().hex}{suffix}"
    target = BROCHURE_UPLOAD_DIR / filename
    target.write_bytes(await file.read())
    return {"url": f"/portal-brochures/uploads/{filename}"}


@router.get("/applications", response_model=RecruitApplicationListResponse)
def recruitment_applications(
    keyword: str | None = Query(default=None),
    plan_id: int | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("recruitment:read")),
) -> RecruitApplicationListResponse:
    return get_recruitment_application_list(keyword=keyword, plan_id=plan_id, status=status_filter, page=page, page_size=page_size)


@router.post("/applications", response_model=RecruitApplicationRecord, status_code=status.HTTP_201_CREATED)
def create_recruitment_application_record(payload: RecruitApplicationUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitApplicationRecord:
    return create_recruitment_application(payload, principal=principal)


@router.put("/applications/{application_id}", response_model=RecruitApplicationRecord)
def update_recruitment_application_record(application_id: int, payload: RecruitApplicationUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitApplicationRecord:
    try:
        return update_recruitment_application(application_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruitment application not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recruitment_application_record(application_id: int, principal: Principal = Depends(require_permissions("recruitment:write"))) -> None:
    try:
        delete_recruitment_application(application_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruitment application not found") from exc


@router.post("/applications/import", response_model=RecruitApplicationImportResult)
async def import_recruitment_application_records(
    plan_id: int = Form(...),
    file: UploadFile = File(...),
    principal: Principal = Depends(require_permissions("recruitment:write")),
) -> RecruitApplicationImportResult:
    try:
        rows = parse_recruitment_template(await file.read())
        return import_recruitment_applications(plan_id=plan_id, rows=rows, principal=principal)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/applications/export")
def export_recruitment_application_records(
    keyword: str | None = Query(default=None),
    plan_id: int | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    principal: Principal = Depends(require_permissions("recruitment:read")),
) -> StreamingResponse:
    content = export_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status_filter)
    filename = f"资料审核名单_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    encoded_filename = quote(filename)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
    )


@router.get("/applications/template")
def download_recruitment_application_template(
    principal: Principal = Depends(require_permissions("recruitment:read")),
) -> StreamingResponse:
    content = export_recruitment_application_blank_template()
    filename = "资料审核名单模板.xlsx"
    encoded_filename = quote(filename)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
    )
