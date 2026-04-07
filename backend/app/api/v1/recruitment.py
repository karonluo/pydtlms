from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.recruitment import (
    RecruitApplicationListResponse,
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
    get_recruitment_application_list,
    get_recruitment_options,
    get_recruitment_plan_list,
    get_recruitment_stats,
    get_recruitment_workbench,
    update_recruitment_application,
    update_recruitment_plan,
)


router = APIRouter(prefix="/recruitment", tags=["recruitment"])


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
    current_stage: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("recruitment:read")),
) -> RecruitPlanListResponse:
    return get_recruitment_plan_list(keyword=keyword, semester=semester, current_stage=current_stage, page=page, page_size=page_size)


@router.post("/plans", response_model=RecruitPlanRecord, status_code=status.HTTP_201_CREATED)
def create_recruitment_plan_record(payload: RecruitPlanUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitPlanRecord:
    return create_recruitment_plan(payload)


@router.put("/plans/{plan_id}", response_model=RecruitPlanRecord)
def update_recruitment_plan_record(plan_id: int, payload: RecruitPlanUpsert, principal: Principal = Depends(require_permissions("recruitment:write"))) -> RecruitPlanRecord:
    try:
        return update_recruitment_plan(plan_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruitment plan not found") from exc


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
