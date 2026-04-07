from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.system import BulkActionResponse, BulkDeleteRequest
from app.schemas.training import (
    OutboundStudyListResponse,
    OutboundStudyRecord,
    OutboundStudyUpsert,
    ScientificReportListResponse,
    ScientificReportRecord,
    ScientificReportUpsert,
    TrainingOptionsResponse,
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
    delete_outbound_studies,
    delete_outbound_study,
    delete_scientific_report,
    delete_scientific_reports,
    delete_training_plan,
    delete_training_plans,
    get_outbound_study_list,
    get_scientific_report_list,
    get_training_options,
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


@router.get("/options", response_model=TrainingOptionsResponse)
def training_options(principal: Principal = Depends(require_permissions("training:read"))) -> TrainingOptionsResponse:
    return get_training_options()


@router.get("/plans", response_model=TrainingPlanListResponse)
def training_plans(
    keyword: str | None = Query(default=None),
    plan_status: str | None = Query(default=None),
    advisor_name: str | None = Query(default=None),
    report_cycle: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("training:read")),
) -> TrainingPlanListResponse:
    return get_training_plan_list(keyword=keyword, plan_status=plan_status, advisor_name=advisor_name, report_cycle=report_cycle, page=page, page_size=page_size)


@router.post("/plans", response_model=TrainingPlanRecord, status_code=status.HTTP_201_CREATED)
def create_training_plan_record(payload: TrainingPlanUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> TrainingPlanRecord:
    return create_training_plan(payload)


@router.post("/plans/batch-delete", response_model=BulkActionResponse)
def batch_delete_training_plan_records(
    payload: BulkDeleteRequest,
    principal: Principal = Depends(require_permissions("training:write")),
) -> BulkActionResponse:
    return delete_training_plans(payload.ids)


@router.put("/plans/{plan_id}", response_model=TrainingPlanRecord)
def update_training_plan_record(plan_id: int, payload: TrainingPlanUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> TrainingPlanRecord:
    try:
        return update_training_plan(plan_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found") from exc


@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training_plan_record(plan_id: int, principal: Principal = Depends(require_permissions("training:write"))) -> None:
    try:
        delete_training_plan(plan_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training plan not found") from exc


@router.get("/reports", response_model=ScientificReportListResponse)
def scientific_reports(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    reviewer_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("training:read")),
) -> ScientificReportListResponse:
    return get_scientific_report_list(keyword=keyword, status=status_filter, reviewer_name=reviewer_name, page=page, page_size=page_size)


@router.post("/reports", response_model=ScientificReportRecord, status_code=status.HTTP_201_CREATED)
def create_scientific_report_record(payload: ScientificReportUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> ScientificReportRecord:
    return create_scientific_report(payload, principal=principal)


@router.post("/reports/batch-delete", response_model=BulkActionResponse)
def batch_delete_scientific_report_records(
    payload: BulkDeleteRequest,
    principal: Principal = Depends(require_permissions("training:write")),
) -> BulkActionResponse:
    return delete_scientific_reports(payload.ids)


@router.put("/reports/{report_id}", response_model=ScientificReportRecord)
def update_scientific_report_record(report_id: int, payload: ScientificReportUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> ScientificReportRecord:
    try:
        return update_scientific_report(report_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scientific report not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/reports/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scientific_report_record(report_id: int, principal: Principal = Depends(require_permissions("training:write"))) -> None:
    try:
        delete_scientific_report(report_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scientific report not found") from exc


@router.get("/outbound-studies", response_model=OutboundStudyListResponse)
def outbound_studies(
    keyword: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    study_type: str | None = Query(default=None),
    advisor_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=1000),
    principal: Principal = Depends(require_permissions("training:read")),
) -> OutboundStudyListResponse:
    return get_outbound_study_list(keyword=keyword, status=status_filter, study_type=study_type, advisor_name=advisor_name, page=page, page_size=page_size)


@router.post("/outbound-studies", response_model=OutboundStudyRecord, status_code=status.HTTP_201_CREATED)
def create_outbound_study_record(payload: OutboundStudyUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> OutboundStudyRecord:
    return create_outbound_study(payload, principal=principal)


@router.post("/outbound-studies/batch-delete", response_model=BulkActionResponse)
def batch_delete_outbound_study_records(
    payload: BulkDeleteRequest,
    principal: Principal = Depends(require_permissions("training:write")),
) -> BulkActionResponse:
    return delete_outbound_studies(payload.ids)


@router.put("/outbound-studies/{study_id}", response_model=OutboundStudyRecord)
def update_outbound_study_record(study_id: int, payload: OutboundStudyUpsert, principal: Principal = Depends(require_permissions("training:write"))) -> OutboundStudyRecord:
    try:
        return update_outbound_study(study_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outbound study not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/outbound-studies/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_outbound_study_record(study_id: int, principal: Principal = Depends(require_permissions("training:write"))) -> None:
    try:
        delete_outbound_study(study_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outbound study not found") from exc
