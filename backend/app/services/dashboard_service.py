from typing import Any

from app.schemas.auth import UserProfile, UserProfileUpdate
from app.schemas.dashboard import DashboardOverview
from app.schemas.portal import (
    PortalApplicationDraftUpsert,
    PortalApplicationSubmissionResponse,
    PortalApplicationUpsert,
    PortalLoginRequest,
    PortalPasswordChangeRequest,
    PortalPlanListResponse,
    PortalProfileOptionsResponse,
    PortalPasswordResetRequest,
    PortalRegistrationEmailCodeResponse,
    PortalRegistrationResponse,
    PortalSessionResponse,
    PortalStudentRecord,
    PortalRegistrationRequest,
    PortalTeamListResponse,
)
from app.schemas.recruitment import RecruitApplicationListResponse, RecruitPlanListResponse, RecruitmentOptionsResponse, RecruitStats, RecruitWorkbench
from app.schemas.recruitment import RecruitApplicationImportResult
from app.schemas.student import (
    CenterListResponse,
    CenterUpsert,
    RegisteredPortalStudentActionResponse,
    RegisteredPortalStudentEmailRequest,
    RegisteredPortalStudentListResponse,
    StudentLifecycleBoard,
    StudentManagementResponse,
    StudentOptionsResponse,
    StudentStats,
    StudentUpsert,
)
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyUpsert,
    BulkActionResponse,
    DictDataListResponse,
    DictDataUpsert,
    DictTypeListResponse,
    DictTypeUpsert,
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
    DegreeOptionsResponse,
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
from app.schemas.auth import Principal
from app.schemas.workflow import WorkflowOptionsResponse, WorkflowStats, WorkflowTaskActionRequest, WorkflowTaskDetailResponse, WorkflowTaskListResponse, WorkflowTaskUpsert
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


def get_student_management_list(
    keyword: str | None = None,
    status: str | None = None,
    advisor_name: str | None = None,
    center_name: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> StudentManagementResponse:
    return store.get_students(keyword=keyword, status=status, advisor_name=advisor_name, center_name=center_name, page=page, page_size=page_size)


def get_registered_portal_student_list(
    keyword: str | None = None,
    application_form_status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> RegisteredPortalStudentListResponse:
    return store.get_registered_portal_students(
        keyword=keyword,
        application_form_status=application_form_status,
        page=page,
        page_size=page_size,
    )


def deactivate_registered_portal_student(student_id: int) -> RegisteredPortalStudentActionResponse:
    return store.deactivate_registered_portal_student(student_id)


def activate_registered_portal_student(student_id: int) -> RegisteredPortalStudentActionResponse:
    return store.activate_registered_portal_student(student_id)


def reset_registered_portal_student_password(student_id: int) -> RegisteredPortalStudentActionResponse:
    return store.reset_registered_portal_student_password(student_id)


def send_registered_portal_student_email(student_id: int, payload: RegisteredPortalStudentEmailRequest) -> RegisteredPortalStudentActionResponse:
    return store.send_registered_portal_student_email(student_id, payload)


def get_student_options() -> StudentOptionsResponse:
    return store.get_student_options()


def get_center_list(
    keyword: str | None = None,
    is_enabled: bool | None = None,
    director_id: int | None = None,
    page: int = 1,
    page_size: int = 10,
) -> CenterListResponse:
    return store.get_centers(
        keyword=keyword,
        is_enabled=is_enabled,
        director_id=director_id,
        page=page,
        page_size=page_size,
    )


def get_student_stats() -> StudentStats:
    return store.get_student_stats()


def create_student(payload: StudentUpsert):
    return store.create_student(payload)


def update_student(student_id: int, payload: StudentUpsert):
    return store.update_student(student_id, payload)


def delete_student(student_id: int) -> None:
    store.delete_student(student_id)


def create_center(payload: CenterUpsert):
    return store.create_center(payload)


def update_center(center_id: int, payload: CenterUpsert):
    return store.update_center(center_id, payload)


def delete_center(center_id: int) -> None:
    store.delete_center(center_id)


def delete_centers(center_ids: list[int]):
    return store.delete_centers(center_ids)


def get_recruitment_plan_list(
    keyword: str | None = None,
    semester: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> RecruitPlanListResponse:
    return store.get_recruitment_plans(keyword=keyword, semester=semester, page=page, page_size=page_size)


def create_recruitment_plan(payload):
    return store.create_recruitment_plan(payload)


def update_recruitment_plan(plan_id: int, payload):
    return store.update_recruitment_plan(plan_id, payload)


def delete_recruitment_plan(plan_id: int) -> None:
    store.delete_recruitment_plan(plan_id)


def get_recruitment_application_list(
    keyword: str | None = None,
    plan_id: int | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> RecruitApplicationListResponse:
    return store.get_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status, page=page, page_size=page_size)


def get_recruitment_application_detail(application_id: int):
    return store.get_recruitment_application_detail(application_id)


def create_recruitment_application(payload, principal: Principal | None = None):
    return store.create_recruitment_application(payload, principal=principal)


def update_recruitment_application(application_id: int, payload):
    return store.update_recruitment_application(application_id, payload)


def delete_recruitment_application(application_id: int) -> None:
    store.delete_recruitment_application(application_id)


def import_recruitment_applications(plan_id: int, rows: list[dict[str, Any]], principal: Principal | None = None) -> RecruitApplicationImportResult:
    return store.import_recruitment_applications(plan_id=plan_id, rows=rows, principal=principal)


def export_recruitment_applications(keyword: str | None = None, plan_id: int | None = None, status: str | None = None) -> bytes:
    return store.export_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status)


def export_recruitment_application_blank_template() -> bytes:
    return store.export_recruitment_application_blank_template()


def send_portal_registration_email_code(email: str) -> PortalRegistrationEmailCodeResponse:
    return store.send_portal_registration_email_code(email)


def send_portal_login_email_code(email: str) -> PortalRegistrationEmailCodeResponse:
    return store.send_portal_login_email_code(email)


def validate_portal_registration_email_code(email: str, verification_code: str) -> None:
    store.validate_portal_registration_email_code(email, verification_code)


def clear_portal_registration_email_code(email: str) -> None:
    store.clear_portal_registration_email_code(email)


def register_portal_student(payload: PortalRegistrationRequest) -> PortalRegistrationResponse:
    return store.register_portal_student(payload)


def login_portal_student(payload: PortalLoginRequest) -> PortalStudentRecord:
    return store.login_portal_student(payload)


def login_portal_student_by_email_code(email: str, verification_code: str) -> PortalStudentRecord:
    return store.login_portal_student_by_email_code(email, verification_code)


def reset_portal_student_password(payload: PortalPasswordResetRequest) -> None:
    store.reset_portal_student_password(payload)


def change_portal_student_password(student_id: int, payload: PortalPasswordChangeRequest) -> None:
    store.change_portal_student_password(student_id, payload)


def get_portal_student(student_id: int) -> PortalStudentRecord:
    return store.get_portal_student(student_id)


def get_portal_profile_options() -> PortalProfileOptionsResponse:
    return store.get_portal_profile_options()


def get_public_recruitment_plans() -> PortalPlanListResponse:
    return store.get_public_recruitment_plans()


def get_public_teams() -> PortalTeamListResponse:
    return store.get_public_teams()


def submit_portal_application(student_id: int, payload: PortalApplicationUpsert) -> PortalApplicationSubmissionResponse:
    return store.submit_portal_application(student_id, payload)


def save_portal_application_draft(student_id: int, payload: PortalApplicationDraftUpsert) -> PortalStudentRecord:
    return store.save_portal_application_draft(student_id, payload)


def get_recruitment_stats() -> RecruitStats:
    return store.get_recruitment_stats()


def get_recruitment_options() -> RecruitmentOptionsResponse:
    return store.get_recruitment_options()


def get_training_plan_list(
    keyword: str | None = None,
    plan_status: str | None = None,
    advisor_name: str | None = None,
    report_cycle: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> TrainingPlanListResponse:
    return store.get_training_plans(keyword=keyword, plan_status=plan_status, advisor_name=advisor_name, report_cycle=report_cycle, page=page, page_size=page_size)


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
    page: int = 1,
    page_size: int = 10,
) -> ScientificReportListResponse:
    return store.get_scientific_reports(keyword=keyword, status=status, reviewer_name=reviewer_name, page=page, page_size=page_size)


def create_scientific_report(payload: ScientificReportUpsert, principal: Principal | None = None):
    return store.create_scientific_report(payload, principal=principal)


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
    page: int = 1,
    page_size: int = 10,
) -> OutboundStudyListResponse:
    return store.get_outbound_studies(keyword=keyword, status=status, study_type=study_type, advisor_name=advisor_name, page=page, page_size=page_size)


def create_outbound_study(payload: OutboundStudyUpsert, principal: Principal | None = None):
    return store.create_outbound_study(payload, principal=principal)


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


def get_thesis_list(
    keyword: str | None = None,
    degree_status: str | None = None,
    advisor_name: str | None = None,
    thesis_status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> ThesisListResponse:
    return store.get_theses(keyword=keyword, degree_status=degree_status, advisor_name=advisor_name, thesis_status=thesis_status, page=page, page_size=page_size)


def create_thesis(payload: ThesisUpsert, principal: Principal | None = None):
    return store.create_thesis(payload, principal=principal)


def update_thesis(thesis_id: int, payload: ThesisUpsert):
    return store.update_thesis(thesis_id, payload)


def get_thesis_review_list(
    thesis_id: int | None = None,
    keyword: str | None = None,
    expert_name: str | None = None,
    review_status: str | None = None,
    page: int = 1,
    page_size: int = 10,
) -> ThesisReviewListResponse:
    return store.get_thesis_reviews(thesis_id=thesis_id, keyword=keyword, expert_name=expert_name, review_status=review_status, page=page, page_size=page_size)


def create_thesis_review(payload: ThesisReviewUpsert):
    return store.create_thesis_review(payload)


def update_thesis_review(review_id: int, payload: ThesisReviewUpsert):
    return store.update_thesis_review(review_id, payload)


def get_degree_stats() -> DegreeStats:
    return store.get_degree_stats()


def get_degree_options() -> DegreeOptionsResponse:
    return store.get_degree_options()


def get_role_list(keyword: str | None = None, scope_name: str | None = None, permission: str | None = None, page: int = 1, page_size: int = 10) -> RoleListResponse:
    return store.get_roles(keyword=keyword, scope_name=scope_name, permission=permission, page=page, page_size=page_size)


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
    page: int = 1,
    page_size: int = 10,
) -> SystemUserListResponse:
    return store.get_system_users(
        keyword=keyword,
        role_code=role_code,
        account_status=account_status,
        department_name=department_name,
        page=page,
        page_size=page_size,
    )


def create_system_user(payload: SystemUserUpsert):
    return store.create_system_user(payload)


def update_system_user(user_id: int, payload: SystemUserUpsert):
    return store.update_system_user(user_id, payload)


def delete_system_user(user_id: int, current_username: str | None = None) -> None:
    store.delete_system_user(user_id, current_username=current_username)


def delete_system_users(user_ids: list[int], current_username: str | None = None) -> BulkActionResponse:
    return store.delete_system_users(user_ids, current_username=current_username)


def get_audit_policy_list(keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> AuditPolicyListResponse:
    return store.get_audit_policy_records(keyword=keyword, status=status, page=page, page_size=page_size)


def create_audit_policy(payload: AuditPolicyUpsert):
    return store.create_audit_policy(payload)


def update_audit_policy(policy_id: int, payload: AuditPolicyUpsert):
    return store.update_audit_policy(policy_id, payload)


def delete_audit_policy(policy_id: int) -> None:
    store.delete_audit_policy(policy_id)


def delete_audit_policies(policy_ids: list[int]) -> BulkActionResponse:
    return store.delete_audit_policies(policy_ids)


def get_integration_list(keyword: str | None = None, status: str | None = None, direction: str | None = None, page: int = 1, page_size: int = 10) -> IntegrationListResponse:
    return store.get_integrations(keyword=keyword, status=status, direction=direction, page=page, page_size=page_size)


def create_integration(payload: IntegrationUpsert):
    return store.create_integration(payload)


def update_integration(integration_id: int, payload: IntegrationUpsert):
    return store.update_integration(integration_id, payload)


def delete_integration(integration_id: int) -> None:
    store.delete_integration(integration_id)


def delete_integrations(integration_ids: list[int]) -> BulkActionResponse:
    return store.delete_integrations(integration_ids)


def get_operation_log_list(keyword: str | None = None, module_name: str | None = None, result: str | None = None, page: int = 1, page_size: int = 10) -> OperationLogListResponse:
    return store.get_operation_logs(keyword=keyword, module_name=module_name, result=result, page=page, page_size=page_size)


def get_sync_log_list(keyword: str | None = None, sync_status: str | None = None, source_system: str | None = None, page: int = 1, page_size: int = 10) -> SyncLogListResponse:
    return store.get_sync_logs(keyword=keyword, sync_status=sync_status, source_system=source_system, page=page, page_size=page_size)


def get_system_permission_catalog() -> PermissionCatalogResponse:
    return store.get_permission_catalog()


def get_dict_type_list(keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> DictTypeListResponse:
    return store.get_dict_types(keyword=keyword, status=status, page=page, page_size=page_size)


def create_dict_type(payload: DictTypeUpsert):
    return store.create_dict_type(payload)


def update_dict_type(dict_type_id: int, payload: DictTypeUpsert):
    return store.update_dict_type(dict_type_id, payload)


def delete_dict_type(dict_type_id: int) -> None:
    store.delete_dict_type(dict_type_id)


def get_dict_data_list(keyword: str | None = None, dict_type: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> DictDataListResponse:
    return store.get_dict_data(keyword=keyword, dict_type=dict_type, status=status, page=page, page_size=page_size)


def create_dict_data(payload: DictDataUpsert):
    return store.create_dict_data(payload)


def update_dict_data(dict_data_id: int, payload: DictDataUpsert):
    return store.update_dict_data(dict_data_id, payload)


def delete_dict_data(dict_data_id: int) -> None:
    store.delete_dict_data(dict_data_id)


def get_system_options() -> SystemOptionsResponse:
    return store.get_system_options()


def get_system_architecture() -> SystemArchitecture:
    return store.get_system_architecture()


def get_system_stats() -> SystemStats:
    return store.get_system_stats()


def get_workflow_task_list(
    status: str | None = None,
    module: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    page_size: int = 10,
    principal: Principal | None = None,
) -> WorkflowTaskListResponse:
    return store.get_workflow_tasks(status=status, module=module, keyword=keyword, page=page, page_size=page_size, principal=principal)


def get_workflow_task_detail(task_id: int, principal: Principal) -> WorkflowTaskDetailResponse:
    return WorkflowTaskDetailResponse(**store.get_workflow_task_detail(task_id, principal=principal))


def create_workflow_task(payload: WorkflowTaskUpsert):
    return store.create_workflow_task(payload)


def update_workflow_task(task_id: int, payload: WorkflowTaskUpsert):
    return store.update_workflow_task(task_id, payload)


def delete_workflow_task(task_id: int) -> None:
    store.delete_workflow_task(task_id)


def execute_workflow_task_action(task_id: int, payload: WorkflowTaskActionRequest, principal: Principal) -> WorkflowTaskDetailResponse:
    return WorkflowTaskDetailResponse(**store.execute_workflow_action(task_id, action=payload.action, comment=payload.comment, principal=principal))


def get_workflow_stats() -> WorkflowStats:
    return store.get_workflow_stats()


def get_workflow_options() -> WorkflowOptionsResponse:
    return store.get_workflow_options()


def get_user_profile(username: str) -> UserProfile:
    return store.get_profile(username)


def update_user_profile(username: str, payload: UserProfileUpdate) -> UserProfile:
    return store.update_profile(username, payload)
