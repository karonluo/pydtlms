from fastapi import APIRouter, Depends, HTTPException, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyRecord,
    AuditPolicyUpsert,
    IntegrationListResponse,
    IntegrationRecord,
    IntegrationUpsert,
    OperationLogListResponse,
    RoleListResponse,
    RoleRecord,
    RoleUpsert,
    SyncLogListResponse,
    SystemArchitecture,
    SystemStats,
    SystemUserListResponse,
    SystemUserRecord,
    SystemUserUpsert,
)
from app.services.dashboard_service import (
    create_audit_policy,
    create_integration,
    create_role,
    create_system_user,
    get_audit_policy_list,
    get_integration_list,
    get_operation_log_list,
    get_role_list,
    get_sync_log_list,
    get_system_architecture,
    get_system_stats,
    get_system_user_list,
    update_audit_policy,
    update_integration,
    update_role,
    update_system_user,
)


router = APIRouter(prefix="/system", tags=["system"])


@router.get("/stats", response_model=SystemStats)
def system_stats(principal: Principal = Depends(require_permissions("system:read"))) -> SystemStats:
    return get_system_stats()


@router.get("/roles", response_model=RoleListResponse)
def roles(principal: Principal = Depends(require_permissions("system:read"))) -> RoleListResponse:
    return get_role_list()


@router.post("/roles", response_model=RoleRecord, status_code=status.HTTP_201_CREATED)
def create_role_record(payload: RoleUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> RoleRecord:
    return create_role(payload)


@router.put("/roles/{role_id}", response_model=RoleRecord)
def update_role_record(role_id: int, payload: RoleUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> RoleRecord:
    try:
        return update_role(role_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found") from exc


@router.get("/users", response_model=SystemUserListResponse)
def system_users(principal: Principal = Depends(require_permissions("system:read"))) -> SystemUserListResponse:
    return get_system_user_list()


@router.post("/users", response_model=SystemUserRecord, status_code=status.HTTP_201_CREATED)
def create_system_user_record(payload: SystemUserUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> SystemUserRecord:
    return create_system_user(payload)


@router.put("/users/{user_id}", response_model=SystemUserRecord)
def update_system_user_record(user_id: int, payload: SystemUserUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> SystemUserRecord:
    try:
        return update_system_user(user_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc


@router.get("/audit-policies", response_model=AuditPolicyListResponse)
def audit_policies(principal: Principal = Depends(require_permissions("audit:read"))) -> AuditPolicyListResponse:
    return get_audit_policy_list()


@router.post("/audit-policies", response_model=AuditPolicyRecord, status_code=status.HTTP_201_CREATED)
def create_audit_policy_record(payload: AuditPolicyUpsert, principal: Principal = Depends(require_permissions("audit:write"))) -> AuditPolicyRecord:
    return create_audit_policy(payload)


@router.put("/audit-policies/{policy_id}", response_model=AuditPolicyRecord)
def update_audit_policy_record(policy_id: int, payload: AuditPolicyUpsert, principal: Principal = Depends(require_permissions("audit:write"))) -> AuditPolicyRecord:
    try:
        return update_audit_policy(policy_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit policy not found") from exc


@router.get("/integrations", response_model=IntegrationListResponse)
def integrations(principal: Principal = Depends(require_permissions("system:read"))) -> IntegrationListResponse:
    return get_integration_list()


@router.post("/integrations", response_model=IntegrationRecord, status_code=status.HTTP_201_CREATED)
def create_integration_record(payload: IntegrationUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> IntegrationRecord:
    return create_integration(payload)


@router.put("/integrations/{integration_id}", response_model=IntegrationRecord)
def update_integration_record(integration_id: int, payload: IntegrationUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> IntegrationRecord:
    try:
        return update_integration(integration_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found") from exc


@router.get("/operation-logs", response_model=OperationLogListResponse)
def operation_logs(principal: Principal = Depends(require_permissions("audit:read"))) -> OperationLogListResponse:
    return get_operation_log_list()


@router.get("/sync-logs", response_model=SyncLogListResponse)
def sync_logs(principal: Principal = Depends(require_permissions("audit:read"))) -> SyncLogListResponse:
    return get_sync_log_list()


@router.get("/architecture", response_model=SystemArchitecture)
def architecture(principal: Principal = Depends(require_permissions("system:read"))) -> SystemArchitecture:
    return get_system_architecture()
