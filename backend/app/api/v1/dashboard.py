from fastapi import APIRouter, Depends, Query

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardUndergraduateSchoolGroupDistributionResponse,
    DashboardUndergraduateSchoolRankingResponse,
    DashboardUndergraduateSchoolStudentListResponse,
)
from app.services.dashboard_service import (
    get_dashboard_overview,
    get_dashboard_undergraduate_school_group_distribution,
    get_dashboard_undergraduate_school_group_students,
    get_dashboard_undergraduate_school_rankings,
    get_dashboard_undergraduate_school_students,
)


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def overview(principal: Principal = Depends(require_permissions("dashboard:read"))) -> DashboardOverview:
    return get_dashboard_overview()


@router.get("/undergraduate-school-rankings", response_model=DashboardUndergraduateSchoolRankingResponse)
def undergraduate_school_rankings(
    limit: int = 20,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolRankingResponse:
    return get_dashboard_undergraduate_school_rankings(limit=limit)


@router.get("/undergraduate-school-group-distribution", response_model=DashboardUndergraduateSchoolGroupDistributionResponse)
def undergraduate_school_group_distribution(
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolGroupDistributionResponse:
    return get_dashboard_undergraduate_school_group_distribution()


@router.get("/undergraduate-school-group-distribution/students", response_model=DashboardUndergraduateSchoolStudentListResponse)
def undergraduate_school_group_students(
    dict_type: str,
    school_name: str | None = None,
    bucket: str | None = Query(default=None),
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolStudentListResponse:
    return get_dashboard_undergraduate_school_group_students(dict_type=dict_type, school_name=school_name, bucket=bucket)


@router.get("/undergraduate-school-rankings/students", response_model=DashboardUndergraduateSchoolStudentListResponse)
def undergraduate_school_students(
    school_name: str,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolStudentListResponse:
    return get_dashboard_undergraduate_school_students(school_name)
