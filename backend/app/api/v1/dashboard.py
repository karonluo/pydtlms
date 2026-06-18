from fastapi import APIRouter, Depends, Query

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardRecruitmentFirstChoicePendingStudentListResponse,
    DashboardRecruitmentSecondChoicePendingGradingResponse,
    DashboardRecruitmentSecondChoicePendingStudentListResponse,
    DashboardRecruitmentFirstChoicePendingGradingResponse,
    DashboardRecruitmentApplicationStatusResponse,
    DashboardRecruitmentAdvisorChoiceDistributionResponse,
    DashboardUndergraduateSchoolStudentListResponse,
    DashboardUndergraduateSchoolGroupDistributionResponse,
    DashboardUndergraduateSchoolRankingResponse,
)
from app.services.dashboard_service import (
    get_dashboard_overview,
    get_dashboard_first_choice_pending_student_list,
    get_dashboard_second_choice_pending_grading_statistics,
    get_dashboard_second_choice_pending_student_list,
    get_dashboard_first_choice_pending_grading_statistics,
    get_dashboard_recruitment_application_status_stats,
    get_dashboard_recruitment_advisor_choice_students,
    get_dashboard_recruitment_advisor_choice_distribution,
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


@router.get("/recruitment-advisor-choice-distribution", response_model=DashboardRecruitmentAdvisorChoiceDistributionResponse)
def recruitment_advisor_choice_distribution(
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentAdvisorChoiceDistributionResponse:
    return get_dashboard_recruitment_advisor_choice_distribution()


@router.get("/recruitment-advisor-choice-distribution/students", response_model=DashboardUndergraduateSchoolStudentListResponse)
def recruitment_advisor_choice_students(
    choice_round: str,
    advisor_name: str | None = None,
    bucket: str | None = Query(default=None),
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolStudentListResponse:
    return get_dashboard_recruitment_advisor_choice_students(choice_round=choice_round, advisor_name=advisor_name, bucket=bucket)


@router.get("/recruitment-application-status-stats", response_model=DashboardRecruitmentApplicationStatusResponse)
def recruitment_application_status_stats(
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentApplicationStatusResponse:
    return get_dashboard_recruitment_application_status_stats()


@router.get("/recruitment-first-choice-pending-grading-statistics", response_model=DashboardRecruitmentFirstChoicePendingGradingResponse)
def recruitment_first_choice_pending_grading_statistics(
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentFirstChoicePendingGradingResponse:
    return get_dashboard_first_choice_pending_grading_statistics(page=page, page_size=page_size, advisor_name=advisor_name)


@router.get("/recruitment-first-choice-pending-students", response_model=DashboardRecruitmentFirstChoicePendingStudentListResponse)
def recruitment_first_choice_pending_students(
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    advisor_id: str | None = None,
    keyword: str | None = None,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentFirstChoicePendingStudentListResponse:
    return get_dashboard_first_choice_pending_student_list(
        page=page,
        page_size=page_size,
        advisor_name=advisor_name,
        advisor_id=advisor_id,
        keyword=keyword,
    )


@router.get("/recruitment-second-choice-pending-grading-statistics", response_model=DashboardRecruitmentSecondChoicePendingGradingResponse)
def recruitment_second_choice_pending_grading_statistics(
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentSecondChoicePendingGradingResponse:
    return get_dashboard_second_choice_pending_grading_statistics(page=page, page_size=page_size, advisor_name=advisor_name)


@router.get("/recruitment-second-choice-pending-students", response_model=DashboardRecruitmentSecondChoicePendingStudentListResponse)
def recruitment_second_choice_pending_students(
    page: int = 1,
    page_size: int = 10,
    advisor_name: str | None = None,
    advisor_id: str | None = None,
    keyword: str | None = None,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardRecruitmentSecondChoicePendingStudentListResponse:
    return get_dashboard_second_choice_pending_student_list(
        page=page,
        page_size=page_size,
        advisor_name=advisor_name,
        advisor_id=advisor_id,
        keyword=keyword,
    )


@router.get("/undergraduate-school-rankings/students", response_model=DashboardUndergraduateSchoolStudentListResponse)
def undergraduate_school_students(
    school_name: str,
    principal: Principal = Depends(require_permissions("dashboard:read")),
) -> DashboardUndergraduateSchoolStudentListResponse:
    return get_dashboard_undergraduate_school_students(school_name)
