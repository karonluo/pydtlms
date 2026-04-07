from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, SoftDeleteMixin, TimestampMixin


class RecruitmentPlan(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_recruitment_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    plan_name: Mapped[str] = mapped_column(String(255), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(16), nullable=False)
    semester: Mapped[str] = mapped_column(String(16), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    target_quota: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    plan_status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")


class ResearchField(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_research_fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    field_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    field_name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class RecruitmentApplication(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_recruitment_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_plans.id"), nullable=False)
    business_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    student_name: Mapped[str] = mapped_column(String(128), nullable=False)
    candidate_no: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(16), nullable=False)
    graduation_school: Mapped[str | None] = mapped_column(String(255))
    highest_degree: Mapped[str | None] = mapped_column(String(64))
    intended_field_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_research_fields.id"))
    application_status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")


class ApplicationMaterial(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_application_materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    material_type: Mapped[str] = mapped_column(String(64), nullable=False)
    material_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)


class QualificationReview(Base, TimestampMixin):
    __tablename__ = "dtlms_qualification_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    reviewer_username: Mapped[str] = mapped_column(String(64), nullable=False)
    review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    review_comment: Mapped[str | None] = mapped_column(Text)


class ReviewerAssignment(Base, TimestampMixin):
    __tablename__ = "dtlms_reviewer_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    reviewer_username: Mapped[str] = mapped_column(String(64), nullable=False)
    reviewer_role: Mapped[str] = mapped_column(String(32), nullable=False)
    assignment_status: Mapped[str] = mapped_column(String(32), nullable=False, default="assigned")


class MaterialScore(Base, TimestampMixin):
    __tablename__ = "dtlms_material_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    reviewer_assignment_id: Mapped[int] = mapped_column(ForeignKey("dtlms_reviewer_assignments.id"), nullable=False)
    material_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    recommendation_text: Mapped[str | None] = mapped_column(Text)


class InterviewGroup(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_interview_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_plans.id"), nullable=False)
    group_code: Mapped[str] = mapped_column(String(64), nullable=False)
    group_name: Mapped[str] = mapped_column(String(128), nullable=False)
    interview_mode: Mapped[str] = mapped_column(String(32), nullable=False, default="offline")


class InterviewSchedule(Base, TimestampMixin):
    __tablename__ = "dtlms_interview_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    interview_group_id: Mapped[int] = mapped_column(ForeignKey("dtlms_interview_groups.id"), nullable=False)
    admission_ticket_no: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    schedule_status: Mapped[str] = mapped_column(String(32), nullable=False, default="scheduled")


class InterviewScore(Base, TimestampMixin):
    __tablename__ = "dtlms_interview_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("dtlms_interview_schedules.id"), nullable=False)
    evaluator_username: Mapped[str] = mapped_column(String(64), nullable=False)
    single_choice_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    fill_blank_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    coding_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    interview_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    ideological_score: Mapped[float | None] = mapped_column(Numeric(5, 2))


class WrittenExamScore(Base, TimestampMixin):
    __tablename__ = "dtlms_written_exam_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    exam_date: Mapped[date | None] = mapped_column(Date)
    exam_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    import_batch_no: Mapped[str | None] = mapped_column(String(64))


class AdmissionDecision(Base, TimestampMixin):
    __tablename__ = "dtlms_admission_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("dtlms_recruitment_applications.id"), nullable=False)
    decision_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    rank_no: Mapped[int | None] = mapped_column(Integer)
    final_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    transfer_option: Mapped[str | None] = mapped_column(String(64))
    decision_comment: Mapped[str | None] = mapped_column(Text)
