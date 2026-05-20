from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import PaginationResponseBase, SelectOption
from app.schemas.contact import validate_optional_email, validate_optional_phone_number


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


class RoleListResponse(PaginationResponseBase):
    items: list[RoleRecord]


class SystemUserRecord(BaseModel):
    id: int
    username: str
    full_name: str
    role_code: str
    role_name: str
    department_name: str
    introduction: str | None = None
    email: str | None = None
    phone_number: str | None = None
    account_status: str
    last_login_at: str | None = None


class SystemUserUpsert(BaseModel):
    username: str
    full_name: str
    role_code: str
    department_name: str
    introduction: str | None = None
    email: str | None = None
    phone_number: str | None = None
    account_status: str
    password: str | None = None

    @field_validator("introduction")
    @classmethod
    def normalize_introduction(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @field_validator("email")
    @classmethod
    def validate_email_field(cls, value: str | None) -> str | None:
        return validate_optional_email(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str | None) -> str | None:
        return validate_optional_phone_number(value)

    @model_validator(mode="after")
    def validate_advisor_introduction(self) -> "SystemUserUpsert":
        if self.role_code == "advisor" and not self.introduction:
            raise ValueError("导师角色必须填写介绍")
        return self


class SystemUserListResponse(PaginationResponseBase):
    items: list[SystemUserRecord]


class AuditPolicyRecord(BaseModel):
    id: int
    item: str
    policy: str
    status: str


class AuditPolicyUpsert(BaseModel):
    item: str
    policy: str
    status: str


class AuditPolicyListResponse(PaginationResponseBase):
    items: list[AuditPolicyRecord]


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


class IntegrationListResponse(PaginationResponseBase):
    items: list[IntegrationRecord]


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


class OperationLogListResponse(PaginationResponseBase):
    items: list[OperationLogRecord]


class SyncLogRecord(BaseModel):
    id: int
    source_system: str
    target_system: str
    sync_status: str
    record_count: int
    executed_at: str
    failure_reason: str | None = None


class SyncLogListResponse(PaginationResponseBase):
    items: list[SyncLogRecord]


class NotificationDeliveryLogRecord(BaseModel):
    id: int
    channel: str
    template_code: str | None = None
    recipient: str
    subject: str
    send_status: str
    sent_at: str
    business_key: str | None = None
    triggered_by: str | None = None
    failure_reason: str | None = None


class NotificationDeliveryLogListResponse(PaginationResponseBase):
    items: list[NotificationDeliveryLogRecord]


class PermissionCatalogResponse(BaseModel):
    items: list[PermissionOption]


class DictTypeRecord(BaseModel):
    id: int
    dict_name: str
    dict_type: str
    status: str
    remark: str | None = None
    data_count: int = 0


class DictTypeUpsert(BaseModel):
    dict_name: str
    dict_type: str
    status: str
    remark: str | None = None


class DictTypeListResponse(PaginationResponseBase):
    items: list[DictTypeRecord]


class DictDataRecord(BaseModel):
    id: int
    dict_type: str
    dict_name: str
    label: str
    value: str
    sort_order: int
    status: str
    color_type: str | None = None
    css_class: str | None = None
    remark: str | None = None


class DictDataUpsert(BaseModel):
    dict_type: str
    label: str
    value: str
    sort_order: int = 0
    status: str
    color_type: str | None = None
    css_class: str | None = None
    remark: str | None = None


class DictDataListResponse(PaginationResponseBase):
    items: list[DictDataRecord]


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