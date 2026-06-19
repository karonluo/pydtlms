from pydantic import BaseModel, Field, field_validator

from app.schemas.common import PaginationResponseBase, SelectOption
from app.schemas.contact import validate_optional_phone_number


class StudentSummary(BaseModel):
    student_no: str
    full_name: str
    status: str
    advisor_name: str
    team_name: str


class StudentLifecycleBoard(BaseModel):
    summary: list[StudentSummary]
    state_distribution: list["StudentStateItem"]


class StudentStateItem(BaseModel):
    label: str
    count: int


class StudentRecord(BaseModel):
    id: int
    portal_student_id: int | None = None
    student_no: str
    full_name: str
    status: str
    advisor_name: str
    advisor_id: int | None = None
    center_name: str
    degree_type: str
    enrollment_year: int
    phone_number: str | None = None
    political_status: str | None = None


class StudentUpsert(BaseModel):
    portal_student_id: int | None = None
    student_no: str
    full_name: str
    status: str
    advisor_name: str | None = None
    advisor_id: int | None = None
    center_name: str
    degree_type: str
    enrollment_year: int
    phone_number: str | None = None
    political_status: str | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number_field(cls, value: str | None) -> str | None:
        return validate_optional_phone_number(value)


class StudentManagementResponse(PaginationResponseBase):
    items: list[StudentRecord]


class RegisteredPortalStudentRecord(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    id_number: str
    account_status: str
    application_form_status: str
    selected_plan_name: str | None = None
    selected_center_name: str | None = None
    selected_advisor_name: str | None = None
    first_choice_center_name: str | None = None
    second_choice_center_name: str | None = None
    first_choice_screening_score: float | None = None
    second_choice_screening_score: float | None = None
    recruitment_application_id: int | None = None
    recruitment_application_candidate_no: str | None = None
    recruitment_application_business_key: str | None = None
    recruitment_application_status: str | None = None
    registered_at: str | None = None
    submitted_at: str | None = None


class RegisteredPortalStudentListResponse(PaginationResponseBase):
    items: list[RegisteredPortalStudentRecord]


class RegisteredPortalStudentExportRequest(BaseModel):
    ids: list[int] = Field(default_factory=list)
    keyword: str | None = None
    plan_id: int | None = None
    application_form_status: str | None = None
    recruitment_application_status: str | None = None
    show_all_background_assessed: bool = False
    advisor_names: list[str] = Field(default_factory=list)
    first_choice_advisor_names: list[str] = Field(default_factory=list)
    second_choice_advisor_names: list[str] = Field(default_factory=list)
    first_choice_center_names: list[str] = Field(default_factory=list)
    second_choice_center_names: list[str] = Field(default_factory=list)
    export_scope: str | None = None


class RegisteredPortalStudentExportJobRecord(BaseModel):
    job_id: str
    status: str
    file_name: str
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    failed_at: str | None = None
    error_message: str | None = None
    download_url: str | None = None
    is_read: bool = True


class RegisteredPortalStudentExportJobListResponse(BaseModel):
    items: list[RegisteredPortalStudentExportJobRecord] = Field(default_factory=list)
    unread_count: int = 0


class RegisteredPortalStudentExportJobCreateResponse(BaseModel):
    message: str
    job: RegisteredPortalStudentExportJobRecord


class RegisteredPortalStudentEmailRequest(BaseModel):
    subject: str
    content: str


class RegisteredPortalStudentRollbackStageRequest(BaseModel):
    target_stage: str
    comment: str | None = None


class RegisteredPortalStudentActionResponse(BaseModel):
    message: str
    account_status: str | None = None
    email_sent: bool | None = None
    temporary_password: str | None = None


class RegisteredPortalStudentAdvisorChoiceUpdateRequest(BaseModel):
    first_choice: str
    first_choice_id: int | None = None
    second_choice: str | None = None
    second_choice_id: int | None = None


class CenterAdvisorMapItem(BaseModel):
    center_name: str
    advisors: list[SelectOption] = Field(default_factory=list)


class StudentOptionsResponse(BaseModel):
    status_options: list[SelectOption]
    degree_options: list[SelectOption]
    advisor_options: list[SelectOption]
    center_advisor_options: list[SelectOption] = Field(default_factory=list)
    registered_portal_advisor_filter_options: list[SelectOption] = Field(default_factory=list)
    registered_portal_first_choice_advisor_filter_options: list[SelectOption] = Field(default_factory=list)
    registered_portal_second_choice_advisor_filter_options: list[SelectOption] = Field(default_factory=list)
    registered_portal_application_status_options: list[SelectOption] = Field(default_factory=list)
    center_options: list[SelectOption]
    political_status_options: list[SelectOption] = Field(default_factory=list)
    center_advisor_map: list[CenterAdvisorMapItem] = Field(default_factory=list)


class CenterDirector(BaseModel):
    """研究中心负责人（来源表 dtlms_team_leaders）。

    设计说明：
    - dtlms_teams.lead_user_id 字段为历史单值设计，数据库层保留不动。
    - 实际负责人数据来源统一从 dtlms_team_leaders 表读取，支持一中心多负责人。
    - 代码层不读取 dtlms_teams.lead_user_id 字段。
    """
    user_id: int
    full_name: str


class CenterRecord(BaseModel):
    id: int
    center_name: str
    # 旧字段 director_name / director_id 保留以兼容老调用方，新代码请使用 director_ids / directors
    director_name: str  # 所有负责人姓名拼接（"张三, 李四"），保留兼容
    director_id: int | None = None  # 已废弃：保留仅用于兼容老调用方，逻辑上等同于 director_ids[0]
    # 新字段（多值设计）
    director_ids: list[int] = Field(default_factory=list)
    directors: list[CenterDirector] = Field(default_factory=list)
    advisor_names: list[str] = Field(default_factory=list)
    advisor_ids: list[int] = Field(default_factory=list)
    advisor_relation_ids: list[int] = Field(default_factory=list)
    is_enabled: bool = True
    created_date: str | None = None
    member_student_count: int = 0
    active_student_count: int = 0
    # 上营名单已提交且同意入营，且第一/第二志愿导师得分>=80并选择中心所属导师的学生数
    student_count: int = 0


class CenterUpsert(BaseModel):
    center_name: str
    # 兼容字段：director_name / director_id 仍可作为入参，但最终统一写入 director_ids
    # 优先级：director_ids 优先；director_id（单值）兼容；director_name 解析为 user_id 仅在 director_ids 为空时生效
    director_name: str | None = None  # 已废弃，保留仅用于兼容
    director_id: int | None = None  # 已废弃，保留仅用于兼容
    director_ids: list[int] = Field(default_factory=list)

    @field_validator("director_ids")
    @classmethod
    def _validate_director_ids(cls, value: list[int]) -> list[int]:
        # 必填、非空、去重、正整数
        if not value:
            raise ValueError("请选择至少一个研究中心负责人（director_ids 不能为空）")
        unique: list[int] = []
        seen: set[int] = set()
        for item in value:
            try:
                integer = int(item)
            except (TypeError, ValueError):
                continue
            if integer <= 0 or integer in seen:
                continue
            seen.add(integer)
            unique.append(integer)
        if not unique:
            raise ValueError("请选择至少一个研究中心负责人（director_ids 不能为空）")
        return unique

    advisor_names: list[str] = Field(default_factory=list)
    advisor_ids: list[int] = Field(default_factory=list)
    advisor_relation_ids: list[int] = Field(default_factory=list)
    is_enabled: bool = True
    created_date: str | None = None


class CenterListResponse(PaginationResponseBase):
    items: list[CenterRecord]


class StudentStats(BaseModel):
    total_students: int
    active_students: int
    outbound_students: int
    thesis_students: int
    advisor_count: int
    center_total: int = 0
    enabled_center_total: int = 0
    registered_portal_total: int = 0
    portal_submitted_total: int = 0
    portal_unsubmitted_total: int = 0