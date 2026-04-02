from fastapi import APIRouter, Depends, HTTPException, status

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.system import (
    AuditPolicyListResponse,
    AuditPolicyRecord,
    AuditPolicyUpsert,
    BulkActionResponse,
    BulkDeleteRequest,
    IntegrationListResponse,
    IntegrationRecord,
    IntegrationUpsert,
    OperationLogListResponse,
    PermissionCatalogResponse,
    RoleListResponse,
    RoleRecord,
    RoleUpsert,
    SyncLogListResponse,
    SystemArchitecture,
    SystemOptionsResponse,
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
    delete_audit_policies,
    delete_audit_policy,
    delete_integration,
    delete_integrations,
    delete_role,
    delete_roles,
    delete_system_user,
    delete_system_users,
    get_audit_policy_list,
    get_integration_list,
    get_operation_log_list,
    get_role_list,
    get_sync_log_list,
    get_system_architecture,
    get_system_options,
    get_system_permission_catalog,
    get_system_stats,
    get_system_user_list,
    update_audit_policy,
    update_integration,
    update_role,
    update_system_user,
)


router = APIRouter(prefix="/system", tags=["system"])


def _handle_service_error(exc: ValueError) -> None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/stats", response_model=SystemStats)
def system_stats(principal: Principal = Depends(require_permissions("system:read"))) -> SystemStats:
    return get_system_stats()


@router.get("/options", response_model=SystemOptionsResponse)
def system_options(principal: Principal = Depends(require_permissions("system:read"))) -> SystemOptionsResponse:
    return get_system_options()


@router.get("/permissions", response_model=PermissionCatalogResponse)
def system_permissions(principal: Principal = Depends(require_permissions("system:read"))) -> PermissionCatalogResponse:
    return get_system_permission_catalog()


@router.get("/roles", response_model=RoleListResponse)
def roles(
    keyword: str | None = None,
    scope_name: str | None = None,
    permission: str | None = None,
    principal: Principal = Depends(require_permissions("system:read")),
) -> RoleListResponse:
    return get_role_list(keyword=keyword, scope_name=scope_name, permission=permission)


@router.post("/roles", response_model=RoleRecord, status_code=status.HTTP_201_CREATED)
def create_role_record(payload: RoleUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> RoleRecord:
    try:
        return create_role(payload)
    except ValueError as exc:
        _handle_service_error(exc)


@router.put("/roles/{role_id}", response_model=RoleRecord)
def update_role_record(role_id: int, payload: RoleUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> RoleRecord:
    try:
        return update_role(role_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_record(role_id: int, principal: Principal = Depends(require_permissions("system:write"))) -> None:
    try:
        delete_role(role_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/roles/batch-delete", response_model=BulkActionResponse)
def batch_delete_role_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("system:write"))) -> BulkActionResponse:
    try:
        return delete_roles(payload.ids)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.get("/users", response_model=SystemUserListResponse)
def system_users(
    keyword: str | None = None,
    role_code: str | None = None,
    account_status: str | None = None,
    department_name: str | None = None,
    principal: Principal = Depends(require_permissions("system:read")),
) -> SystemUserListResponse:
    return get_system_user_list(
        keyword=keyword,
        role_code=role_code,
        account_status=account_status,
        department_name=department_name,
    )


@router.post("/users", response_model=SystemUserRecord, status_code=status.HTTP_201_CREATED)
def create_system_user_record(payload: SystemUserUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> SystemUserRecord:
    try:
        return create_system_user(payload)
    except ValueError as exc:
        _handle_service_error(exc)


@router.put("/users/{user_id}", response_model=SystemUserRecord)
def update_system_user_record(user_id: int, payload: SystemUserUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> SystemUserRecord:
    try:
        return update_system_user(user_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system_user_record(user_id: int, principal: Principal = Depends(require_permissions("system:write"))) -> None:
    try:
        delete_system_user(user_id, current_username=principal.username)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.post("/users/batch-delete", response_model=BulkActionResponse)
def batch_delete_system_user_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("system:write"))) -> BulkActionResponse:
    try:
        return delete_system_users(payload.ids, current_username=principal.username)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") from exc
    except ValueError as exc:
        _handle_service_error(exc)


@router.get("/audit-policies", response_model=AuditPolicyListResponse)
def audit_policies(
    keyword: str | None = None,
    status: str | None = None,
    principal: Principal = Depends(require_permissions("audit:read")),
) -> AuditPolicyListResponse:
    return get_audit_policy_list(keyword=keyword, status=status)


@router.post("/audit-policies", response_model=AuditPolicyRecord, status_code=status.HTTP_201_CREATED)
def create_audit_policy_record(payload: AuditPolicyUpsert, principal: Principal = Depends(require_permissions("audit:write"))) -> AuditPolicyRecord:
    return create_audit_policy(payload)


@router.put("/audit-policies/{policy_id}", response_model=AuditPolicyRecord)
def update_audit_policy_record(policy_id: int, payload: AuditPolicyUpsert, principal: Principal = Depends(require_permissions("audit:write"))) -> AuditPolicyRecord:
    try:
        return update_audit_policy(policy_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit policy not found") from exc


@router.delete("/audit-policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_audit_policy_record(policy_id: int, principal: Principal = Depends(require_permissions("audit:write"))) -> None:
    try:
        delete_audit_policy(policy_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit policy not found") from exc


@router.post("/audit-policies/batch-delete", response_model=BulkActionResponse)
def batch_delete_audit_policy_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("audit:write"))) -> BulkActionResponse:
    try:
        return delete_audit_policies(payload.ids)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit policy not found") from exc


@router.get("/integrations", response_model=IntegrationListResponse)
def integrations(
    keyword: str | None = None,
    status: str | None = None,
    direction: str | None = None,
    principal: Principal = Depends(require_permissions("system:read")),
) -> IntegrationListResponse:
    return get_integration_list(keyword=keyword, status=status, direction=direction)


@router.post("/integrations", response_model=IntegrationRecord, status_code=status.HTTP_201_CREATED)
def create_integration_record(payload: IntegrationUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> IntegrationRecord:
    return create_integration(payload)


@router.put("/integrations/{integration_id}", response_model=IntegrationRecord)
def update_integration_record(integration_id: int, payload: IntegrationUpsert, principal: Principal = Depends(require_permissions("system:write"))) -> IntegrationRecord:
    try:
        return update_integration(integration_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found") from exc


@router.delete("/integrations/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_integration_record(integration_id: int, principal: Principal = Depends(require_permissions("system:write"))) -> None:
    try:
        delete_integration(integration_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found") from exc


@router.post("/integrations/batch-delete", response_model=BulkActionResponse)
def batch_delete_integration_records(payload: BulkDeleteRequest, principal: Principal = Depends(require_permissions("system:write"))) -> BulkActionResponse:
    try:
        return delete_integrations(payload.ids)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found") from exc


@router.get("/operation-logs", response_model=OperationLogListResponse)
def operation_logs(
    keyword: str | None = None,
    module_name: str | None = None,
    result: str | None = None,
    principal: Principal = Depends(require_permissions("audit:read")),
) -> OperationLogListResponse:
    return get_operation_log_list(keyword=keyword, module_name=module_name, result=result)


@router.get("/sync-logs", response_model=SyncLogListResponse)
def sync_logs(
    keyword: str | None = None,
    sync_status: str | None = None,
    source_system: str | None = None,
    principal: Principal = Depends(require_permissions("audit:read")),
) -> SyncLogListResponse:
    return get_sync_log_list(keyword=keyword, sync_status=sync_status, source_system=source_system)


@router.get("/architecture", response_model=SystemArchitecture)
def architecture(principal: Principal = Depends(require_permissions("system:read"))) -> SystemArchitecture:
    return get_system_architecture()
