from pydantic import BaseModel, Field


class SelectOption(BaseModel):
    label: str
    value: str


class PermissionOption(BaseModel):
    code: str
    name: str
    module_name: str
    description: str


class RoleRecord(BaseModel):
    id: int
    role_code: str
    role_name: str
    scope_name: str
    permissions: list[str]
    user_count: int = 0


class RoleUpsert(BaseModel):
    role_code: str
    role_name: str
    scope_name: str
    permissions: list[str] = Field(default_factory=list)


class RoleListResponse(BaseModel):
    items: list[RoleRecord]
    total: int


class SystemUserRecord(BaseModel):
    id: int
    username: str
    full_name: str
    role_code: str
    role_name: str
    department_name: str
    phone_number: str | None = None
    account_status: str
    last_login_at: str | None = None


class SystemUserUpsert(BaseModel):
    username: str
    full_name: str
    role_code: str
    department_name: str
    phone_number: str | None = None
    account_status: str
    password: str | None = None


class SystemUserListResponse(BaseModel):
    items: list[SystemUserRecord]
    total: int


class AuditPolicyRecord(BaseModel):
    id: int
    item: str
    policy: str
    status: str


class AuditPolicyUpsert(BaseModel):
    item: str
    policy: str
    status: str


class AuditPolicyListResponse(BaseModel):
    items: list[AuditPolicyRecord]
    total: int


class IntegrationRecord(BaseModel):
    id: int
    name: str
    direction: str
    cadence: str
    status: str
    owner: str


class IntegrationUpsert(BaseModel):
    name: str
    direction: str
    cadence: str
    status: str
    owner: str


class IntegrationListResponse(BaseModel):
    items: list[IntegrationRecord]
    total: int


class OperationLogRecord(BaseModel):
    id: int
    operated_at: str
    operator_username: str
    module_name: str
    entity_name: str
    entity_id: str
    action: str
    result: str
    summary: str


class OperationLogListResponse(BaseModel):
    items: list[OperationLogRecord]
    total: int


class SyncLogRecord(BaseModel):
    id: int
    source_system: str
    target_system: str
    sync_status: str
    record_count: int
    executed_at: str
    failure_reason: str | None = None


class SyncLogListResponse(BaseModel):
    items: list[SyncLogRecord]
    total: int


class PermissionCatalogResponse(BaseModel):
    items: list[PermissionOption]


class SystemOptionsResponse(BaseModel):
    account_status_options: list[SelectOption]
    role_scope_options: list[SelectOption]
    integration_direction_options: list[SelectOption]
    integration_cadence_options: list[SelectOption]
    integration_status_options: list[SelectOption]
    audit_status_options: list[SelectOption]
    operation_result_options: list[SelectOption]
    sync_status_options: list[SelectOption]


class BulkDeleteRequest(BaseModel):
    ids: list[int] = Field(default_factory=list)


class BulkActionResponse(BaseModel):
    success_count: int


class SystemArchitecture(BaseModel):
    authentication: str
    database: str
    cache: str
    audit: list[str]
    integrations: list[str]


class SystemStats(BaseModel):
    integration_total: int
    active_integration_total: int
    operation_log_total: int
    sync_failure_total: int
    user_total: int
    role_total: int