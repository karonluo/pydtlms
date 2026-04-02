from app.schemas.auth import UserProfile, UserProfileUpdate
from app.schemas.dashboard import DashboardOverview
from app.schemas.recruitment import RecruitApplicationListResponse, RecruitPlanListResponse, RecruitStats, RecruitWorkbench
from app.schemas.student import StudentLifecycleBoard, StudentManagementResponse, StudentStats, StudentUpsert
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyUpsert,
    BulkActionResponse,
    IntegrationListResponse,
    IntegrationUpsert,
    OperationLogListResponse,
    PermissionCatalogResponse,
    RoleListResponse,
    RoleUpsert,
    SyncLogListResponse,
    SystemArchitecture,
    SystemOptionsResponse,
    SystemStats,
    SystemUserListResponse,
    SystemUserUpsert,
)
from app.schemas.training import (
    DegreeStats,
    DegreeWorkbench,
    OutboundStudyListResponse,
    OutboundStudyUpsert,
    ScientificReportListResponse,
    ScientificReportUpsert,
    ThesisListResponse,
    ThesisReviewListResponse,
    ThesisReviewUpsert,
    ThesisUpsert,
    TrainingOptionsResponse,
    TrainingPlanListResponse,
    TrainingPlanUpsert,
    TrainingStats,
    TrainingWorkbench,
)
from app.schemas.workflow import WorkflowStats, WorkflowTaskListResponse, WorkflowTaskUpsert
from app.services.management_service import store


def get_dashboard_overview() -> DashboardOverview:
    return store.get_dashboard_overview()


def get_recruitment_workbench() -> RecruitWorkbench:
    return store.get_recruitment_workbench()


def get_student_lifecycle_board() -> StudentLifecycleBoard:
    return store.get_student_board()


def get_training_workbench() -> TrainingWorkbench:
    return store.get_training_workbench()


def get_degree_workbench() -> DegreeWorkbench:
    return store.get_degree_workbench()


def get_audit_policies() -> list[dict[str, str]]:
    return [item.model_dump() for item in store.get_audit_policy_records().items]


def get_student_management_list(keyword: str | None = None, status: str | None = None, advisor_name: str | None = None) -> StudentManagementResponse:
    return store.get_students(keyword=keyword, status=status, advisor_name=advisor_name)


def get_student_stats() -> StudentStats:
    return store.get_student_stats()


def create_student(payload: StudentUpsert):
    return store.create_student(payload)


def update_student(student_id: int, payload: StudentUpsert):
    return store.update_student(student_id, payload)


def delete_student(student_id: int) -> None:
    store.delete_student(student_id)


def get_recruitment_plan_list() -> RecruitPlanListResponse:
    return store.get_recruitment_plans()


def create_recruitment_plan(payload):
    return store.create_recruitment_plan(payload)


def update_recruitment_plan(plan_id: int, payload):
    return store.update_recruitment_plan(plan_id, payload)


def get_recruitment_application_list(keyword: str | None = None, plan_id: int | None = None, status: str | None = None) -> RecruitApplicationListResponse:
    return store.get_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status)


def create_recruitment_application(payload):
    return store.create_recruitment_application(payload)


def update_recruitment_application(application_id: int, payload):
    return store.update_recruitment_application(application_id, payload)


def delete_recruitment_application(application_id: int) -> None:
    store.delete_recruitment_application(application_id)


def get_recruitment_stats() -> RecruitStats:
    return store.get_recruitment_stats()


def get_training_plan_list(
    keyword: str | None = None,
    plan_status: str | None = None,
    advisor_name: str | None = None,
    report_cycle: str | None = None,
) -> TrainingPlanListResponse:
    return store.get_training_plans(keyword=keyword, plan_status=plan_status, advisor_name=advisor_name, report_cycle=report_cycle)


def create_training_plan(payload: TrainingPlanUpsert):
    return store.create_training_plan(payload)


def update_training_plan(plan_id: int, payload: TrainingPlanUpsert):
    return store.update_training_plan(plan_id, payload)


def delete_training_plan(plan_id: int) -> None:
    store.delete_training_plan(plan_id)


def delete_training_plans(plan_ids: list[int]) -> BulkActionResponse:
    return store.delete_training_plans(plan_ids)


def get_scientific_report_list(
    keyword: str | None = None,
    status: str | None = None,
    reviewer_name: str | None = None,
) -> ScientificReportListResponse:
    return store.get_scientific_reports(keyword=keyword, status=status, reviewer_name=reviewer_name)


def create_scientific_report(payload: ScientificReportUpsert):
    return store.create_scientific_report(payload)


def update_scientific_report(report_id: int, payload: ScientificReportUpsert):
    return store.update_scientific_report(report_id, payload)


def delete_scientific_report(report_id: int) -> None:
    store.delete_scientific_report(report_id)


def delete_scientific_reports(report_ids: list[int]) -> BulkActionResponse:
    return store.delete_scientific_reports(report_ids)


def get_outbound_study_list(
    keyword: str | None = None,
    status: str | None = None,
    study_type: str | None = None,
    advisor_name: str | None = None,
) -> OutboundStudyListResponse:
    return store.get_outbound_studies(keyword=keyword, status=status, study_type=study_type, advisor_name=advisor_name)


def create_outbound_study(payload: OutboundStudyUpsert):
    return store.create_outbound_study(payload)


def update_outbound_study(study_id: int, payload: OutboundStudyUpsert):
    return store.update_outbound_study(study_id, payload)


def delete_outbound_study(study_id: int) -> None:
    store.delete_outbound_study(study_id)


def delete_outbound_studies(study_ids: list[int]) -> BulkActionResponse:
    return store.delete_outbound_studies(study_ids)


def get_training_stats() -> TrainingStats:
    return store.get_training_stats()


def get_training_options() -> TrainingOptionsResponse:
    return store.get_training_options()


def get_thesis_list(keyword: str | None = None, degree_status: str | None = None) -> ThesisListResponse:
    return store.get_theses(keyword=keyword, degree_status=degree_status)


def create_thesis(payload: ThesisUpsert):
    return store.create_thesis(payload)


def update_thesis(thesis_id: int, payload: ThesisUpsert):
    return store.update_thesis(thesis_id, payload)


def get_thesis_review_list(thesis_id: int | None = None) -> ThesisReviewListResponse:
    return store.get_thesis_reviews(thesis_id=thesis_id)


def create_thesis_review(payload: ThesisReviewUpsert):
    return store.create_thesis_review(payload)


def update_thesis_review(review_id: int, payload: ThesisReviewUpsert):
    return store.update_thesis_review(review_id, payload)


def get_degree_stats() -> DegreeStats:
    return store.get_degree_stats()


def get_role_list(keyword: str | None = None, scope_name: str | None = None, permission: str | None = None) -> RoleListResponse:
    return store.get_roles(keyword=keyword, scope_name=scope_name, permission=permission)


def create_role(payload: RoleUpsert):
    return store.create_role(payload)


def update_role(role_id: int, payload: RoleUpsert):
    return store.update_role(role_id, payload)


def delete_role(role_id: int) -> None:
    store.delete_role(role_id)


def delete_roles(role_ids: list[int]) -> BulkActionResponse:
    return store.delete_roles(role_ids)


def get_system_user_list(
    keyword: str | None = None,
    role_code: str | None = None,
    account_status: str | None = None,
    department_name: str | None = None,
) -> SystemUserListResponse:
    return store.get_system_users(
        keyword=keyword,
        role_code=role_code,
        account_status=account_status,
        department_name=department_name,
    )


def create_system_user(payload: SystemUserUpsert):
    return store.create_system_user(payload)


def update_system_user(user_id: int, payload: SystemUserUpsert):
    return store.update_system_user(user_id, payload)


def delete_system_user(user_id: int, current_username: str | None = None) -> None:
    store.delete_system_user(user_id, current_username=current_username)


def delete_system_users(user_ids: list[int], current_username: str | None = None) -> BulkActionResponse:
    return store.delete_system_users(user_ids, current_username=current_username)


def get_audit_policy_list(keyword: str | None = None, status: str | None = None) -> AuditPolicyListResponse:
    return store.get_audit_policy_records(keyword=keyword, status=status)


def create_audit_policy(payload: AuditPolicyUpsert):
    return store.create_audit_policy(payload)


def update_audit_policy(policy_id: int, payload: AuditPolicyUpsert):
    return store.update_audit_policy(policy_id, payload)


def delete_audit_policy(policy_id: int) -> None:
    store.delete_audit_policy(policy_id)


def delete_audit_policies(policy_ids: list[int]) -> BulkActionResponse:
    return store.delete_audit_policies(policy_ids)


def get_integration_list(keyword: str | None = None, status: str | None = None, direction: str | None = None) -> IntegrationListResponse:
    return store.get_integrations(keyword=keyword, status=status, direction=direction)


def create_integration(payload: IntegrationUpsert):
    return store.create_integration(payload)


def update_integration(integration_id: int, payload: IntegrationUpsert):
    return store.update_integration(integration_id, payload)


def delete_integration(integration_id: int) -> None:
    store.delete_integration(integration_id)


def delete_integrations(integration_ids: list[int]) -> BulkActionResponse:
    return store.delete_integrations(integration_ids)


def get_operation_log_list(keyword: str | None = None, module_name: str | None = None, result: str | None = None) -> OperationLogListResponse:
    return store.get_operation_logs(keyword=keyword, module_name=module_name, result=result)


def get_sync_log_list(keyword: str | None = None, sync_status: str | None = None, source_system: str | None = None) -> SyncLogListResponse:
    return store.get_sync_logs(keyword=keyword, sync_status=sync_status, source_system=source_system)


def get_system_permission_catalog() -> PermissionCatalogResponse:
    return store.get_permission_catalog()


def get_system_options() -> SystemOptionsResponse:
    return store.get_system_options()


def get_system_architecture() -> SystemArchitecture:
    return store.get_system_architecture()


def get_system_stats() -> SystemStats:
    return store.get_system_stats()


def get_workflow_task_list(status: str | None = None, module: str | None = None) -> WorkflowTaskListResponse:
    return store.get_workflow_tasks(status=status, module=module)


def create_workflow_task(payload: WorkflowTaskUpsert):
    return store.create_workflow_task(payload)


def update_workflow_task(task_id: int, payload: WorkflowTaskUpsert):
    return store.update_workflow_task(task_id, payload)


def delete_workflow_task(task_id: int) -> None:
    store.delete_workflow_task(task_id)


def get_workflow_stats() -> WorkflowStats:
    return store.get_workflow_stats()


def get_user_profile(username: str) -> UserProfile:
    return store.get_profile(username)


def update_user_profile(username: str, payload: UserProfileUpdate) -> UserProfile:
    return store.update_profile(username, payload)
