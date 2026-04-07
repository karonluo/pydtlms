from pydantic import BaseModel, Field

from app.schemas.common import PaginationResponseBase, SelectOption


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
    team_name: str
    degree_type: str
    enrollment_year: int
    phone_number: str | None = None
    political_status: str | None = None


class StudentUpsert(BaseModel):
    student_no: str
    full_name: str
    status: str
    advisor_name: str
    team_name: str
    degree_type: str
    enrollment_year: int
    phone_number: str | None = None
    political_status: str | None = None


class StudentManagementResponse(PaginationResponseBase):
    items: list[StudentRecord]


class TeamAdvisorMapItem(BaseModel):
    team_name: str
    advisors: list[SelectOption] = Field(default_factory=list)


class StudentOptionsResponse(BaseModel):
    status_options: list[SelectOption]
    degree_options: list[SelectOption]
    advisor_options: list[SelectOption]
    team_options: list[SelectOption]
    team_status_options: list[SelectOption]
    political_status_options: list[SelectOption] = Field(default_factory=list)
    department_options: list[SelectOption] = Field(default_factory=list)
    discipline_options: list[SelectOption] = Field(default_factory=list)
    team_advisor_map: list[TeamAdvisorMapItem] = Field(default_factory=list)


class TeamRecord(BaseModel):
    id: int
    team_code: str
    team_name: str
    department_name: str
    discipline_name: str
    lead_advisor_name: str
    advisor_names: list[str] = Field(default_factory=list)
    research_directions: list[str] = Field(default_factory=list)
    status: str
    established_on: str | None = None
    description: str | None = None
    member_student_count: int = 0
    active_student_count: int = 0


class TeamUpsert(BaseModel):
    team_code: str
    team_name: str
    department_name: str
    discipline_name: str
    lead_advisor_name: str
    advisor_names: list[str] = Field(default_factory=list)
    research_directions: list[str] = Field(default_factory=list)
    status: str
    established_on: str | None = None
    description: str | None = None


class TeamListResponse(PaginationResponseBase):
    items: list[TeamRecord]


class StudentStats(BaseModel):
    total_students: int
    active_students: int
    outbound_students: int
    thesis_students: int
    advisor_count: int
    team_total: int = 0
    active_team_total: int = 0
