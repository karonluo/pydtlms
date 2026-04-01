from app.schemas.auth import UserProfile, UserProfileUpdate
from app.schemas.dashboard import DashboardOverview
from app.schemas.recruitment import RecruitApplicationListResponse, RecruitPlanListResponse, RecruitStats, RecruitWorkbench
from app.schemas.student import StudentLifecycleBoard, StudentManagementResponse, StudentStats, StudentUpsert
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyUpsert,
    IntegrationListResponse,
    IntegrationUpsert,
    OperationLogListResponse,
    RoleListResponse,
    RoleUpsert,
    SyncLogListResponse,
    SystemArchitecture,
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


def get_training_plan_list() -> TrainingPlanListResponse:
    return store.get_training_plans()


def create_training_plan(payload: TrainingPlanUpsert):
    return store.create_training_plan(payload)


def update_training_plan(plan_id: int, payload: TrainingPlanUpsert):
    return store.update_training_plan(plan_id, payload)


def get_scientific_report_list(keyword: str | None = None, status: str | None = None) -> ScientificReportListResponse:
    return store.get_scientific_reports(keyword=keyword, status=status)


def create_scientific_report(payload: ScientificReportUpsert):
    return store.create_scientific_report(payload)


def update_scientific_report(report_id: int, payload: ScientificReportUpsert):
    return store.update_scientific_report(report_id, payload)


def get_outbound_study_list(keyword: str | None = None, status: str | None = None) -> OutboundStudyListResponse:
    return store.get_outbound_studies(keyword=keyword, status=status)


def create_outbound_study(payload: OutboundStudyUpsert):
    return store.create_outbound_study(payload)


def update_outbound_study(study_id: int, payload: OutboundStudyUpsert):
    return store.update_outbound_study(study_id, payload)


def get_training_stats() -> TrainingStats:
    return store.get_training_stats()


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


def get_role_list() -> RoleListResponse:
    return store.get_roles()


def create_role(payload: RoleUpsert):
    return store.create_role(payload)


def update_role(role_id: int, payload: RoleUpsert):
    return store.update_role(role_id, payload)


def get_system_user_list() -> SystemUserListResponse:
    return store.get_system_users()


def create_system_user(payload: SystemUserUpsert):
    return store.create_system_user(payload)


def update_system_user(user_id: int, payload: SystemUserUpsert):
    return store.update_system_user(user_id, payload)


def get_audit_policy_list() -> AuditPolicyListResponse:
    return store.get_audit_policy_records()


def create_audit_policy(payload: AuditPolicyUpsert):
    return store.create_audit_policy(payload)


def update_audit_policy(policy_id: int, payload: AuditPolicyUpsert):
    return store.update_audit_policy(policy_id, payload)


def get_integration_list() -> IntegrationListResponse:
    return store.get_integrations()


def create_integration(payload: IntegrationUpsert):
    return store.create_integration(payload)


def update_integration(integration_id: int, payload: IntegrationUpsert):
    return store.update_integration(integration_id, payload)


def get_operation_log_list() -> OperationLogListResponse:
    return store.get_operation_logs()


def get_sync_log_list() -> SyncLogListResponse:
    return store.get_sync_logs()


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
