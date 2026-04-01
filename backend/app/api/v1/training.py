from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.training import (
    OutboundStudyListResponse,
    OutboundStudyRecord,
    OutboundStudyUpsert,
    ScientificReportListResponse,
    ScientificReportRecord,
    ScientificReportUpsert,
    TrainingPlanListResponse,
    TrainingPlanRecord,
    TrainingPlanUpsert,
    TrainingStats,
    TrainingWorkbench,
)
from app.services.dashboard_service import (
    create_outbound_study,
    create_scientific_report,
    create_training_plan,
    get_outbound_study_list,
    get_scientific_report_list,
    get_training_plan_list,
    get_training_stats,
    get_training_workbench,
    update_outbound_study,
    update_scientific_report,
    update_training_plan,
)


router = APIRouter(prefix="/training", tags=["training"])


@router.get("/workbench", response_model=TrainingWorkbench)
def training_workbench(principal: Principal = Depends(require_permissions("training:read"))) -> TrainingWorkbench:
    return get_training_workbench()


@router.get("/stats", response_model=TrainingStats)
def training_stats(principal: Principal = Depends(require_permissions("training:read"))) -> TrainingStats:
    return get_training_stats()


@router.get("/plans", response_model=TrainingPlanListResponse)
def training_plans(principal: Principal = Depends(require_permissions("training:read"))) -> TrainingPlanListResponse:
    return get_training_plan_list()


@router.post("/plans", response_model=TrainingPlanRecord, status_code=status.HTTP_201_CREATED)
def create_training_plan_record(payload: TrainingPlanUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> TrainingPlanRecord:
    return create_training_plan(payload)


@router.put("/plans/{plan_id}", response_model=TrainingPlanRecord)
def update_training_plan_record(plan_id: int, payload: TrainingPlanUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> TrainingPlanRecord:
    try:
        return update_training_plan(plan_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found") from exc


@router.get("/reports", response_model=ScientificReportListResponse)
def scientific_reports(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    principal: Principal = Depends(require_permissions("training:read")),
) -> ScientificReportListResponse:
    return get_scientific_report_list(keyword=keyword, status=status_filter)


@router.post("/reports", response_model=ScientificReportRecord, status_code=status.HTTP_201_CREATED)
def create_scientific_report_record(payload: ScientificReportUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> ScientificReportRecord:
    return create_scientific_report(payload)


@router.put("/reports/{report_id}", response_model=ScientificReportRecord)
def update_scientific_report_record(report_id: int, payload: ScientificReportUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> ScientificReportRecord:
    try:
        return update_scientific_report(report_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scientific report not found") from exc


@router.get("/outbound-studies", response_model=OutboundStudyListResponse)
def outbound_studies(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    principal: Principal = Depends(require_permissions("training:read")),
) -> OutboundStudyListResponse:
    return get_outbound_study_list(keyword=keyword, status=status_filter)


@router.post("/outbound-studies", response_model=OutboundStudyRecord, status_code=status.HTTP_201_CREATED)
def create_outbound_study_record(payload: OutboundStudyUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> OutboundStudyRecord:
    return create_outbound_study(payload)


@router.put("/outbound-studies/{study_id}", response_model=OutboundStudyRecord)
def update_outbound_study_record(study_id: int, payload: OutboundStudyUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> OutboundStudyRecord:
    try:
        return update_outbound_study(study_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outbound study not found") from exc
