from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, SoftDeleteMixin, TimestampMixin


class Advisor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_advisors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    advisor_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    organization_name: Mapped[str] = mapped_column(String(128), nullable=False)
    research_direction: Mapped[str] = mapped_column(String(255), nullable=False)
    annual_quota: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Team(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    team_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    department_name: Mapped[str] = mapped_column(String(128), nullable=False)
    discipline_name: Mapped[str | None] = mapped_column(String(128))
    lead_advisor_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_advisors.id"))
    research_directions: Mapped[str | None] = mapped_column(Text)
    team_status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    established_on: Mapped[date | None] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(Text)


class TeamAdvisor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_team_advisors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("dtlms_teams.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("dtlms_advisors.id"), nullable=False)
    advisor_role: Mapped[str] = mapped_column(String(32), nullable=False, default="member")
    joined_on: Mapped[date | None] = mapped_column(Date)
    left_on: Mapped[date | None] = mapped_column(Date)


class Student(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    gender: Mapped[str] = mapped_column(String(16), nullable=False)
    political_status: Mapped[str | None] = mapped_column(String(32))
    phone_number: Mapped[str | None] = mapped_column(String(32))
    identity_no: Mapped[str | None] = mapped_column(String(64))
    enrollment_year: Mapped[int] = mapped_column(Integer, nullable=False)
    degree_type: Mapped[str] = mapped_column(String(32), nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_teams.id"))
    current_status: Mapped[str] = mapped_column(String(32), nullable=False, default="enrolled")
    primary_advisor_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_advisors.id"))


class StudentTeamHistory(Base, TimestampMixin):
    __tablename__ = "dtlms_student_team_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("dtlms_teams.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    change_reason: Mapped[str | None] = mapped_column(Text)


class StudentAdvisorHistory(Base, TimestampMixin):
    __tablename__ = "dtlms_student_advisor_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("dtlms_advisors.id"), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(32), nullable=False, default="primary")
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    change_reason: Mapped[str | None] = mapped_column(Text)


class ResearchProject(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_research_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    principal_advisor_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_advisors.id"))
    funding_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))


class TrainingPlan(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_training_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("dtlms_advisors.id"), nullable=False)
    version_no: Mapped[str] = mapped_column(String(16), nullable=False, default="v1.0")
    report_cycle: Mapped[str] = mapped_column(String(32), nullable=False)
    plan_status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    scientific_goal: Mapped[str] = mapped_column(Text, nullable=False)
    assessment_rule: Mapped[str] = mapped_column(Text, nullable=False)


class TrainingPlanVersion(Base, TimestampMixin):
    __tablename__ = "dtlms_training_plan_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    training_plan_id: Mapped[int] = mapped_column(ForeignKey("dtlms_training_plans.id"), nullable=False)
    version_no: Mapped[str] = mapped_column(String(16), nullable=False)
    change_reason: Mapped[str | None] = mapped_column(Text)
    plan_snapshot: Mapped[str] = mapped_column(Text, nullable=False)


class ScientificReport(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_scientific_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    training_plan_id: Mapped[int] = mapped_column(ForeignKey("dtlms_training_plans.id"), nullable=False)
    period_label: Mapped[str] = mapped_column(String(32), nullable=False)
    report_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    attachment_url: Mapped[str | None] = mapped_column(String(255))
    reviewer_advisor_id: Mapped[int | None] = mapped_column(ForeignKey("dtlms_advisors.id"))
    review_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    review_comment: Mapped[str | None] = mapped_column(Text)


class OutboundStudy(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_outbound_studies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("dtlms_advisors.id"), nullable=False)
    study_type: Mapped[str] = mapped_column(String(64), nullable=False)
    destination: Mapped[str] = mapped_column(String(128), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")
    expected_outcome: Mapped[str | None] = mapped_column(Text)


class Achievement(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    achievement_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    published_at: Mapped[date | None] = mapped_column(Date)
    publisher_name: Mapped[str | None] = mapped_column(String(255))
    ranking_text: Mapped[str | None] = mapped_column(String(64))


class Thesis(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "dtlms_theses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_key: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("dtlms_students.id"), nullable=False)
    advisor_id: Mapped[int] = mapped_column(ForeignKey("dtlms_advisors.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    plagiarism_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    thesis_status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    blind_review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    defense_date: Mapped[date | None] = mapped_column(Date)
    degree_granted: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")


class ThesisReview(Base, TimestampMixin):
    __tablename__ = "dtlms_thesis_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thesis_id: Mapped[int] = mapped_column(ForeignKey("dtlms_theses.id"), nullable=False)
    expert_name: Mapped[str] = mapped_column(String(128), nullable=False)
    review_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    review_comment: Mapped[str | None] = mapped_column(Text)
