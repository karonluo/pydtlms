from pydantic import BaseModel


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


class StudentManagementResponse(BaseModel):
    items: list[StudentRecord]
    total: int


class StudentStats(BaseModel):
    total_students: int
    active_students: int
    outbound_students: int
    thesis_students: int
    advisor_count: int
