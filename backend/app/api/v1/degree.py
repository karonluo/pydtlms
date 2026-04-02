from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.training import (
    DegreeOptionsResponse,
    DegreeStats,
    DegreeWorkbench,
    ThesisListResponse,
    ThesisRecord,
    ThesisReviewListResponse,
    ThesisReviewRecord,
    ThesisReviewUpsert,
    ThesisUpsert,
)
from app.services.dashboard_service import (
    create_thesis,
    create_thesis_review,
    get_degree_options,
    get_degree_stats,
    get_degree_workbench,
    get_thesis_list,
    get_thesis_review_list,
    update_thesis,
    update_thesis_review,
)


router = APIRouter(prefix="/degree", tags=["degree"])


@router.get("/workbench", response_model=DegreeWorkbench)
def degree_workbench(principal: Principal = Depends(require_permissions("degree:read"))) -> DegreeWorkbench:
    return get_degree_workbench()


@router.get("/stats", response_model=DegreeStats)
def degree_stats(principal: Principal = Depends(require_permissions("degree:read"))) -> DegreeStats:
    return get_degree_stats()


@router.get("/options", response_model=DegreeOptionsResponse)
def degree_options(principal: Principal = Depends(require_permissions("degree:read"))) -> DegreeOptionsResponse:
    return get_degree_options()


@router.get("/theses", response_model=ThesisListResponse)
def theses(
    keyword: str | None = Query(default=None),
    degree_status: str | None = Query(default=None),
    principal: Principal = Depends(require_permissions("degree:read")),
) -> ThesisListResponse:
    return get_thesis_list(keyword=keyword, degree_status=degree_status)


@router.post("/theses", response_model=ThesisRecord, status_code=status.HTTP_201_CREATED)
def create_thesis_record(payload: ThesisUpsert, principal: Principal = Depends(require_permissions("degree:write"))) -> ThesisRecord:
    return create_thesis(payload)


@router.put("/theses/{thesis_id}", response_model=ThesisRecord)
def update_thesis_record(thesis_id: int, payload: ThesisUpsert, principal: Principal = Depends(require_permissions("degree:write"))) -> ThesisRecord:
    try:
        return update_thesis(thesis_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thesis not found") from exc


@router.get("/reviews", response_model=ThesisReviewListResponse)
def thesis_reviews(thesis_id: int | None = Query(default=None), principal: Principal = Depends(require_permissions("degree:read"))) -> ThesisReviewListResponse:
    return get_thesis_review_list(thesis_id=thesis_id)


@router.post("/reviews", response_model=ThesisReviewRecord, status_code=status.HTTP_201_CREATED)
def create_thesis_review_record(payload: ThesisReviewUpsert, principal: Principal = Depends(require_permissions("degree:write"))) -> ThesisReviewRecord:
    return create_thesis_review(payload)


@router.put("/reviews/{review_id}", response_model=ThesisReviewRecord)
def update_thesis_review_record(review_id: int, payload: ThesisReviewUpsert, principal: Principal = Depends(require_permissions("degree:write"))) -> ThesisReviewRecord:
    try:
        return update_thesis_review(review_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thesis review not found") from exc
