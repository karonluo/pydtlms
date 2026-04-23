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
    student_no: str
    full_name: str
    status: str
    advisor_name: str
    center_name: str
    degree_type: str
    enrollment_year: int
    phone_number: str | None = None
    political_status: str | None = None


class StudentUpsert(BaseModel):
    student_no: str
    full_name: str
    status: str
    advisor_name: str
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
    recruitment_application_status: str | None = None
    registered_at: str | None = None
    submitted_at: str | None = None


class RegisteredPortalStudentListResponse(PaginationResponseBase):
    items: list[RegisteredPortalStudentRecord]


class RegisteredPortalStudentEmailRequest(BaseModel):
    subject: str
    content: str


class RegisteredPortalStudentActionResponse(BaseModel):
    message: str
    account_status: str | None = None
    email_sent: bool | None = None
    temporary_password: str | None = None


class CenterAdvisorMapItem(BaseModel):
    center_name: str
    advisors: list[SelectOption] = Field(default_factory=list)


class StudentOptionsResponse(BaseModel):
    status_options: list[SelectOption]
    degree_options: list[SelectOption]
    advisor_options: list[SelectOption]
    center_options: list[SelectOption]
    political_status_options: list[SelectOption] = Field(default_factory=list)
    center_advisor_map: list[CenterAdvisorMapItem] = Field(default_factory=list)


class CenterRecord(BaseModel):
    id: int
    center_name: str
    director_name: str
    advisor_names: list[str] = Field(default_factory=list)
    is_enabled: bool = True
    created_date: str | None = None
    member_student_count: int = 0
    active_student_count: int = 0


class CenterUpsert(BaseModel):
    center_name: str
    director_name: str
    advisor_names: list[str] = Field(default_factory=list)
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
