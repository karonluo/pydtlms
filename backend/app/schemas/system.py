from pydantic import BaseModel


class RoleRecord(BaseModel):
    id: int
    role_code: str
    role_name: str
    scope_name: str
    permissions: list[str]


class RoleUpsert(BaseModel):
    role_code: str
    role_name: str
    scope_name: str
    permissions: list[str]


class RoleListResponse(BaseModel):
    items: list[RoleRecord]
    total: int


class SystemUserRecord(BaseModel):
    id: int
    username: str
    full_name: str
    role_code: str
    department_name: str
    phone_number: str | None = None
    account_status: str


class SystemUserUpsert(BaseModel):
    username: str
    full_name: str
    role_code: str
    department_name: str
    phone_number: str | None = None
    account_status: str


class SystemUserListResponse(BaseModel):
    items: list[SystemUserRecord]
    total: int


class AuditPolicyRecord(BaseModel):
    id: int
    item: str
    policy: str


class AuditPolicyUpsert(BaseModel):
    item: str
    policy: str


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