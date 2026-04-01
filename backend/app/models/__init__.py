from app.models.base import Base
from app.models.recruitment import (
    AdmissionDecision,
    ApplicationMaterial,
    InterviewGroup,
    InterviewSchedule,
    InterviewScore,
    MaterialScore,
    QualificationReview,
    RecruitmentApplication,
    RecruitmentPlan,
    ResearchField,
    ReviewerAssignment,
    WrittenExamScore,
)
from app.models.system import (
    DataSyncLog,
    LoginLog,
    NotificationTemplate,
    OperationLog,
    Permission,
    Role,
    RolePermission,
    SystemConfig,
    User,
    UserRole,
)
from app.models.training import (
    Achievement,
    Advisor,
    OutboundStudy,
    ResearchProject,
    ScientificReport,
    Student,
    StudentAdvisorHistory,
    Thesis,
    ThesisReview,
    TrainingPlan,
    TrainingPlanVersion,
)

__all__ = ["Base"]
