from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
from uuid import uuid4

from app.core.config import settings
from app.services.recruitment_excel_service import build_registered_portal_students_template

from .management_service_shared import *


class RuntimeManagementStoreStudentsMixin:
    _registered_portal_export_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="registered-portal-export")
    _registered_portal_export_jobs: dict[str, dict[str, Any]] = {}
    _registered_portal_export_jobs_lock = RLock()

    @staticmethod
    def _registered_portal_export_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _registered_portal_export_job_file_name() -> str:
        return f"注册学生导出_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"

    @staticmethod
    def _build_registered_portal_export_job_record(job: dict[str, Any]) -> RegisteredPortalStudentExportJobRecord:
        return RegisteredPortalStudentExportJobRecord(
            job_id=str(job.get("job_id") or ""),
            status=str(job.get("status") or "pending"),
            file_name=str(job.get("file_name") or "注册学生导出.xlsx"),
            created_at=str(job.get("created_at") or ""),
            started_at=job.get("started_at"),
            completed_at=job.get("completed_at"),
            failed_at=job.get("failed_at"),
            error_message=job.get("error_message"),
            download_url=job.get("download_url"),
            is_read=bool(job.get("is_read", True)),
        )

    def _run_registered_portal_export_job(self, job_id: str) -> None:
        with self._registered_portal_export_jobs_lock:
            job = self._registered_portal_export_jobs.get(job_id)
            if job is None:
                return
            job["status"] = "running"
            job["started_at"] = self._registered_portal_export_timestamp()
            job["error_message"] = None

        try:
            content = self.export_registered_portal_students(
                list(job.get("student_ids") or []),
                keyword=job.get("keyword"),
                application_form_status=job.get("application_form_status"),
            )
            temp_dir = Path(tempfile.gettempdir()) / "pydtlms-export-jobs"
            temp_dir.mkdir(parents=True, exist_ok=True)
            file_path = temp_dir / f"{job_id}.xlsx"
            file_path.write_bytes(content)
        except Exception as exc:
            with self._registered_portal_export_jobs_lock:
                failed_job = self._registered_portal_export_jobs.get(job_id)
                if failed_job is None:
                    return
                failed_job["status"] = "failed"
                failed_job["failed_at"] = self._registered_portal_export_timestamp()
                failed_job["error_message"] = str(exc)
                failed_job["download_url"] = None
                failed_job["is_read"] = False
            return

        with self._registered_portal_export_jobs_lock:
            completed_job = self._registered_portal_export_jobs.get(job_id)
            if completed_job is None:
                return
            completed_job["status"] = "completed"
            completed_job["completed_at"] = self._registered_portal_export_timestamp()
            completed_job["file_path"] = str(file_path)
            completed_job["download_url"] = f"/api/v1/students/portal-registrations/export-jobs/{job_id}/download"
            completed_job["is_read"] = False

    def create_registered_portal_student_export_job(
        self,
        payload: RegisteredPortalStudentExportRequest,
        *,
        principal: Principal,
    ) -> RegisteredPortalStudentExportJobCreateResponse:
        job_id = uuid4().hex
        job = {
            "job_id": job_id,
            "owner": principal.username,
            "status": "pending",
            "file_name": self._registered_portal_export_job_file_name(),
            "created_at": self._registered_portal_export_timestamp(),
            "started_at": None,
            "completed_at": None,
            "failed_at": None,
            "error_message": None,
            "download_url": None,
            "file_path": None,
            "is_read": True,
            "student_ids": list(payload.ids),
            "keyword": payload.keyword,
            "application_form_status": payload.application_form_status,
        }
        with self._registered_portal_export_jobs_lock:
            self._registered_portal_export_jobs[job_id] = job
        self._registered_portal_export_executor.submit(self._run_registered_portal_export_job, job_id)
        return RegisteredPortalStudentExportJobCreateResponse(
            message="开始导出，请等待完成",
            job=self._build_registered_portal_export_job_record(job),
        )

    def list_registered_portal_student_export_jobs(
        self,
        *,
        principal: Principal,
    ) -> RegisteredPortalStudentExportJobListResponse:
        with self._registered_portal_export_jobs_lock:
            jobs = [
                item for item in self._registered_portal_export_jobs.values()
                if str(item.get("owner") or "") == principal.username
            ]
            jobs.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
            records = [self._build_registered_portal_export_job_record(item) for item in jobs[:10]]
        unread_count = len([item for item in records if not item.is_read and item.status in {"completed", "failed"}])
        return RegisteredPortalStudentExportJobListResponse(items=records, unread_count=unread_count)

    def mark_registered_portal_student_export_jobs_read(self, *, principal: Principal) -> None:
        with self._registered_portal_export_jobs_lock:
            for item in self._registered_portal_export_jobs.values():
                if str(item.get("owner") or "") != principal.username:
                    continue
                if str(item.get("status") or "") in {"completed", "failed"}:
                    item["is_read"] = True

    def get_registered_portal_student_export_job_download(self, job_id: str, *, principal: Principal) -> tuple[str, bytes]:
        with self._registered_portal_export_jobs_lock:
            job = self._registered_portal_export_jobs.get(job_id)
            if job is None or str(job.get("owner") or "") != principal.username:
                raise KeyError(job_id)
            if str(job.get("status") or "") != "completed":
                raise ValueError("导出尚未完成，请稍后重试")
            file_path = str(job.get("file_path") or "").strip()
            file_name = str(job.get("file_name") or "注册学生导出.xlsx")

        if not file_path:
            raise ValueError("导出文件不存在，请重新导出")
        path = Path(file_path)
        if not path.exists():
            raise ValueError("导出文件不存在，请重新导出")
        return file_name, path.read_bytes()

    @staticmethod
    def _registered_portal_student_export_text(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _registered_portal_attachment_value(url: Any, name: Any) -> str | None:
        resolved_url = settings.build_absolute_site_url(RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(url))
        if resolved_url:
            return resolved_url
        return RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(name)

    @staticmethod
    def _registered_portal_bool_text(value: Any) -> str | None:
        if value is None:
            return None
        return "是" if bool(value) else "否"

    @staticmethod
    def _registered_portal_json_text(value: Any) -> str | None:
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            value = value.model_dump(mode="json")
        if value in ({}, [], ""):
            return None
        return json.dumps(
            value,
            ensure_ascii=False,
            default=lambda item: item.model_dump(mode="json") if hasattr(item, "model_dump") else item,
        )

    @staticmethod
    def _registered_portal_application_sort_key(application: dict[str, Any]) -> tuple[str, int]:
        return (
            str(application.get("applied_at") or application.get("created_at") or ""),
            int(application.get("id") or 0),
        )

    def _get_latest_registered_portal_application_item(self, student_id: int) -> dict[str, Any] | None:
        latest_application: dict[str, Any] | None = None
        for application in self._list("recruitment_applications"):
            if int(application.get("portal_student_id") or 0) != int(student_id):
                continue
            if latest_application is None or self._registered_portal_application_sort_key(application) >= self._registered_portal_application_sort_key(latest_application):
                latest_application = application
        return latest_application

    @staticmethod
    def _get_undergraduate_education_experience(application: RecruitApplicationRecord | None) -> Any | None:
        if application is None:
            return None
        for item in application.education_experiences or []:
            stage = str(getattr(item, "education_stage", "") or "").strip()
            if stage in {"本科在读", "本科毕业"}:
                return item
        return None

    @staticmethod
    def _registered_portal_application_form_status(submitted_at: Any, application_status: str | None) -> tuple[str, str | None]:
        normalized_submitted_at = RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(submitted_at)
        if application_status == "驳回重填":
            return "驳回重填", None
        if normalized_submitted_at:
            return "已填写报名", normalized_submitted_at
        return "未填写报名", None

    def _resolve_registered_portal_student_export_ids(
        self,
        student_ids: list[int],
        *,
        keyword: str | None,
        application_form_status: str | None,
    ) -> list[int]:
        normalized_ids: list[int] = []
        seen_ids: set[int] = set()
        for raw_id in student_ids:
            student_id = int(raw_id)
            if student_id <= 0 or student_id in seen_ids:
                continue
            seen_ids.add(student_id)
            normalized_ids.append(student_id)
        if normalized_ids:
            return normalized_ids

        total_hint = max(len(self._list("portal_students")), 1)
        response = self.get_registered_portal_students(
            keyword=keyword,
            application_form_status=application_form_status,
            page=1,
            page_size=total_hint,
        )
        return [item.id for item in response.items]

    def _build_registered_portal_student_export_row(
        self,
        student: PortalStudentRecord,
        application_status: str | None,
        application_id: int | None,
        application_business_key: str | None,
        registered_at: str | None,
        plan_name: str | None,
    ) -> dict[str, Any]:
        profile = student.profile
        draft = student.application_draft
        preferences = list((draft.preferences if draft else []) or [])
        education_experiences = list((draft.education_experiences if draft else []) or [])
        practice_experiences = list((draft.practice_experiences if draft else []) or [])
        english_proficiencies = list((draft.english_proficiencies if draft else []) or [])
        family_members = list((draft.family_members if draft else []) or [])
        achievement_records = list((draft.achievement_records if draft else []) or [])
        personal_statement = draft.personal_statement if draft else None
        declaration = draft.declaration if draft else None

        application_form_status, submitted_at = self._registered_portal_application_form_status(student.submitted_at, application_status)
        undergraduate = None
        for item in education_experiences:
            stage = self._registered_portal_student_export_text(getattr(item, "education_stage", None))
            if stage in {"本科在读", "本科毕业"}:
                undergraduate = item
                break

        record: dict[str, Any] = {
            "full_name": self._registered_portal_student_export_text(student.full_name),
            "phone_number": self._registered_portal_student_export_text(student.phone_number),
            "email": self._registered_portal_student_export_text(student.email),
            "id_number": self._registered_portal_student_export_text(student.id_number),
            "portal_business_key": self._registered_portal_student_export_text(student.business_key),
            "candidate_no": self._registered_portal_student_export_text(student.candidate_no),
            "account_status": self._normalize_portal_account_status(student.account_status),
            "application_form_status": application_form_status,
            "selected_plan_id": student.selected_plan_id,
            "selected_plan_name": plan_name,
            "selected_team_id": student.selected_team_id,
            "selected_center_name": self._registered_portal_student_export_text(student.selected_team_name),
            "selected_advisor_user_id": student.selected_advisor_user_id,
            "selected_advisor_name": self._registered_portal_student_export_text(student.selected_advisor_name),
            "recruitment_application_business_key": self._registered_portal_student_export_text(application_business_key),
            "recruitment_application_id": application_id,
            "recruitment_application_status": self._registered_portal_student_export_text(application_status) or "未提交",
            "registered_at": self._registered_portal_student_export_text(registered_at),
            "submitted_at": submitted_at,
            "full_name_pinyin": self._registered_portal_student_export_text(getattr(profile, "full_name_pinyin", None)),
            "profile_photo_url": self._registered_portal_attachment_value(getattr(profile, "profile_photo_url", None), None),
            "id_card_collage_url": self._registered_portal_attachment_value(getattr(profile, "id_card_collage_url", None), None),
            "gender": self._registered_portal_student_export_text(student.gender),
            "birth_date": self._registered_portal_student_export_text(student.birth_date),
            "ethnic_group": self._registered_portal_student_export_text(student.ethnic_group),
            "native_place": self._registered_portal_student_export_text(student.native_place),
            "political_status": self._registered_portal_student_export_text(student.political_status),
            "marital_status": self._registered_portal_student_export_text(student.marital_status),
            "religious_belief": self._registered_portal_student_export_text(student.religious_belief),
            "id_type": self._registered_portal_student_export_text(student.id_type),
            "mailing_address": self._registered_portal_student_export_text(student.mailing_address),
            "emergency_contact_name": self._registered_portal_student_export_text(getattr(profile, "emergency_contact_name", None)),
            "emergency_contact_phone": self._registered_portal_student_export_text(getattr(profile, "emergency_contact_phone", None)),
            "graduation_school": self._registered_portal_student_export_text(student.graduation_school),
            "highest_degree": self._registered_portal_student_export_text(student.highest_degree),
            "intended_field": self._registered_portal_student_export_text(student.intended_field),
            "source_channel": self._registered_portal_student_export_text(getattr(draft, "source_channel", None)),
            "source_channel_other": self._registered_portal_student_export_text(getattr(draft, "source_channel_other", None)),
            "english_level": self._registered_portal_student_export_text(student.english_level),
            "family_info": self._registered_portal_student_export_text(student.family_info),
            "education_experience": self._registered_portal_student_export_text(student.education_experience),
            "practice_experience": self._registered_portal_student_export_text(student.practice_experience),
            "personal_profile": self._registered_portal_student_export_text(student.personal_profile),
            "recommendation_notes": self._registered_portal_student_export_text(student.recommendation_notes),
            "personal_statement_text": self._registered_portal_student_export_text(student.personal_statement_text),
            "self_evaluation": self._registered_portal_student_export_text(student.self_evaluation),
            "signed_agreement": self._registered_portal_bool_text(student.signed_agreement),
            "application_profile_json": self._registered_portal_json_text(profile),
            "application_draft_json": self._registered_portal_json_text(draft),
            "preferences_json": self._registered_portal_json_text(preferences),
            "education_experiences_json": self._registered_portal_json_text(education_experiences),
            "practice_experiences_json": self._registered_portal_json_text(practice_experiences),
            "english_proficiencies_json": self._registered_portal_json_text(english_proficiencies),
            "family_members_json": self._registered_portal_json_text(family_members),
            "achievement_records_json": self._registered_portal_json_text(achievement_records),
            "personal_statement_json": self._registered_portal_json_text(personal_statement),
            "declaration_json": self._registered_portal_json_text(declaration),
            "declaration_progress_snapshot_json": self._registered_portal_json_text(getattr(declaration, "progress_snapshot", None)),
            "personal_statement_resume_attachment": self._registered_portal_attachment_value(
                getattr(personal_statement, "resume_attachment_url", None),
                getattr(personal_statement, "resume_attachment_name", None),
            ),
            "personal_statement_supporting_material_attachment": self._registered_portal_attachment_value(
                getattr(personal_statement, "supporting_material_attachment_url", None),
                getattr(personal_statement, "supporting_material_attachment_name", None),
            ),
            "personal_statement_growth_experience_text": self._registered_portal_student_export_text(
                getattr(personal_statement, "growth_experience_text", None)
            ),
            "personal_statement_why_apply_text": self._registered_portal_student_export_text(
                getattr(personal_statement, "why_apply_text", None)
            ),
            "personal_statement_career_plan_text": self._registered_portal_student_export_text(
                getattr(personal_statement, "career_plan_text", None)
            ),
            "personal_statement_research_interest_text": self._registered_portal_student_export_text(
                getattr(personal_statement, "research_interest_text", None)
            ),
            "personal_statement_personal_statement_text": self._registered_portal_student_export_text(
                getattr(personal_statement, "personal_statement_text", None)
            ),
            "declaration_has_read": self._registered_portal_bool_text(getattr(declaration, "has_read_declaration", None)),
            "declaration_text": self._registered_portal_student_export_text(getattr(declaration, "declaration_text", None)),
            "undergraduate_stage": self._registered_portal_student_export_text(getattr(undergraduate, "education_stage", None)),
            "undergraduate_start_month": self._registered_portal_student_export_text(getattr(undergraduate, "start_month", None)),
            "undergraduate_end_month": self._registered_portal_student_export_text(getattr(undergraduate, "end_month", None)),
            "undergraduate_school_name": self._registered_portal_student_export_text(getattr(undergraduate, "school_name", None)),
            "undergraduate_major_name": self._registered_portal_student_export_text(getattr(undergraduate, "major_name", None)),
            "undergraduate_average_score": self._registered_portal_student_export_text(getattr(undergraduate, "average_score", None)),
            "undergraduate_gpa": self._registered_portal_student_export_text(getattr(undergraduate, "gpa", None)),
            "undergraduate_ranking": self._registered_portal_student_export_text(getattr(undergraduate, "ranking", None)),
            "undergraduate_verifier_name": self._registered_portal_student_export_text(getattr(undergraduate, "verifier_name", None)),
            "undergraduate_verifier_phone": self._registered_portal_student_export_text(getattr(undergraduate, "verifier_phone", None)),
            "undergraduate_transcript_attachment": self._registered_portal_attachment_value(
                getattr(undergraduate, "transcript_attachment_url", None),
                getattr(undergraduate, "transcript_attachment_name", None),
            ),
            "undergraduate_degree_certificate_attachment": self._registered_portal_attachment_value(
                getattr(undergraduate, "degree_certificate_attachment_url", None),
                getattr(undergraduate, "degree_certificate_attachment_name", None),
            ),
            "undergraduate_graduation_certificate_attachment": self._registered_portal_attachment_value(
                getattr(undergraduate, "graduation_certificate_attachment_url", None),
                getattr(undergraduate, "graduation_certificate_attachment_name", None),
            ),
        }

        for index, preference in enumerate(preferences, start=1):
            record[f"preference_{index}_order"] = getattr(preference, "preference_order", None)
            record[f"preference_{index}_team_id"] = getattr(preference, "team_id", None)
            record[f"preference_{index}_research_center_name"] = self._registered_portal_student_export_text(
                getattr(preference, "research_center_name", None)
            )
            record[f"preference_{index}_advisor_user_id"] = getattr(preference, "advisor_user_id", None)
            record[f"preference_{index}_advisor_name"] = self._registered_portal_student_export_text(getattr(preference, "advisor_name", None))
            record[f"preference_{index}_is_optional"] = self._registered_portal_bool_text(getattr(preference, "is_optional", None))

        for index, education in enumerate(education_experiences, start=1):
            record[f"education_{index}_sort_order"] = getattr(education, "sort_order", None)
            record[f"education_{index}_stage"] = self._registered_portal_student_export_text(getattr(education, "education_stage", None))
            record[f"education_{index}_start_month"] = self._registered_portal_student_export_text(getattr(education, "start_month", None))
            record[f"education_{index}_end_month"] = self._registered_portal_student_export_text(getattr(education, "end_month", None))
            record[f"education_{index}_school_name"] = self._registered_portal_student_export_text(getattr(education, "school_name", None))
            record[f"education_{index}_major_name"] = self._registered_portal_student_export_text(getattr(education, "major_name", None))
            record[f"education_{index}_average_score"] = self._registered_portal_student_export_text(getattr(education, "average_score", None))
            record[f"education_{index}_gpa"] = self._registered_portal_student_export_text(getattr(education, "gpa", None))
            record[f"education_{index}_ranking"] = self._registered_portal_student_export_text(getattr(education, "ranking", None))
            record[f"education_{index}_verifier_name"] = self._registered_portal_student_export_text(getattr(education, "verifier_name", None))
            record[f"education_{index}_verifier_phone"] = self._registered_portal_student_export_text(getattr(education, "verifier_phone", None))
            record[f"education_{index}_transcript_attachment"] = self._registered_portal_attachment_value(
                getattr(education, "transcript_attachment_url", None),
                getattr(education, "transcript_attachment_name", None),
            )
            record[f"education_{index}_degree_certificate_attachment"] = self._registered_portal_attachment_value(
                getattr(education, "degree_certificate_attachment_url", None),
                getattr(education, "degree_certificate_attachment_name", None),
            )
            record[f"education_{index}_graduation_certificate_attachment"] = self._registered_portal_attachment_value(
                getattr(education, "graduation_certificate_attachment_url", None),
                getattr(education, "graduation_certificate_attachment_name", None),
            )

        for index, practice in enumerate(practice_experiences, start=1):
            record[f"practice_{index}_sort_order"] = getattr(practice, "sort_order", None)
            record[f"practice_{index}_start_month"] = self._registered_portal_student_export_text(getattr(practice, "start_month", None))
            record[f"practice_{index}_end_month"] = self._registered_portal_student_export_text(getattr(practice, "end_month", None))
            record[f"practice_{index}_organization_name"] = self._registered_portal_student_export_text(
                getattr(practice, "organization_name", None)
            )
            record[f"practice_{index}_position_name"] = self._registered_portal_student_export_text(getattr(practice, "position_name", None))
            record[f"practice_{index}_responsibility"] = self._registered_portal_student_export_text(getattr(practice, "responsibility", None))
            record[f"practice_{index}_verifier_name"] = self._registered_portal_student_export_text(getattr(practice, "verifier_name", None))
            record[f"practice_{index}_verifier_phone"] = self._registered_portal_student_export_text(getattr(practice, "verifier_phone", None))

        for index, english in enumerate(english_proficiencies, start=1):
            record[f"english_{index}_sort_order"] = getattr(english, "sort_order", None)
            record[f"english_{index}_exam_name"] = self._registered_portal_student_export_text(getattr(english, "exam_name", None))
            record[f"english_{index}_score_text"] = self._registered_portal_student_export_text(getattr(english, "score_text", None))
            record[f"english_{index}_certificate_attachment"] = self._registered_portal_attachment_value(
                getattr(english, "certificate_attachment_url", None),
                getattr(english, "certificate_attachment_name", None),
            )

        for index, family_member in enumerate(family_members, start=1):
            record[f"family_{index}_sort_order"] = getattr(family_member, "sort_order", None)
            record[f"family_{index}_member_name"] = self._registered_portal_student_export_text(getattr(family_member, "member_name", None))
            record[f"family_{index}_relation_type"] = self._registered_portal_student_export_text(getattr(family_member, "relation_type", None))
            record[f"family_{index}_employer_name"] = self._registered_portal_student_export_text(getattr(family_member, "employer_name", None))
            record[f"family_{index}_job_title"] = self._registered_portal_student_export_text(getattr(family_member, "job_title", None))
            record[f"family_{index}_contact_phone"] = self._registered_portal_student_export_text(getattr(family_member, "contact_phone", None))

        for index, achievement in enumerate(achievement_records, start=1):
            record[f"achievement_{index}_sort_order"] = getattr(achievement, "sort_order", None)
            record[f"achievement_{index}_achievement_type"] = self._registered_portal_student_export_text(
                getattr(achievement, "achievement_type", None)
            )
            record[f"achievement_{index}_achievement_month"] = self._registered_portal_student_export_text(
                getattr(achievement, "achievement_month", None)
            )
            record[f"achievement_{index}_paper_title"] = self._registered_portal_student_export_text(getattr(achievement, "paper_title", None))
            record[f"achievement_{index}_journal_or_conference"] = self._registered_portal_student_export_text(
                getattr(achievement, "journal_or_conference", None)
            )
            record[f"achievement_{index}_publish_or_index_month"] = self._registered_portal_student_export_text(
                getattr(achievement, "publish_or_index_month", None)
            )
            record[f"achievement_{index}_author_order"] = self._registered_portal_student_export_text(getattr(achievement, "author_order", None))
            record[f"achievement_{index}_award_name"] = self._registered_portal_student_export_text(getattr(achievement, "award_name", None))
            record[f"achievement_{index}_awarding_org"] = self._registered_portal_student_export_text(getattr(achievement, "awarding_org", None))
            record[f"achievement_{index}_award_level"] = self._registered_portal_student_export_text(getattr(achievement, "award_level", None))
            record[f"achievement_{index}_award_year"] = self._registered_portal_student_export_text(getattr(achievement, "award_year", None))
            record[f"achievement_{index}_award_rank"] = self._registered_portal_student_export_text(getattr(achievement, "award_rank", None))
            record[f"achievement_{index}_description_text"] = self._registered_portal_student_export_text(
                getattr(achievement, "description_text", None)
            )
            record[f"achievement_{index}_responsibility_text"] = self._registered_portal_student_export_text(
                getattr(achievement, "responsibility_text", None)
            )
            record[f"achievement_{index}_award_certificate_attachment"] = self._registered_portal_attachment_value(
                getattr(achievement, "award_certificate_attachment_url", None),
                getattr(achievement, "award_certificate_attachment_name", None),
            )

        return record

    def deactivate_registered_portal_student(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) == "停用":
                return RegisteredPortalStudentActionResponse(message="该注册学生账号已停用", account_status="停用")

            student["account_status"] = "停用"
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "停用账号", f'停用注册学生账号 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return RegisteredPortalStudentActionResponse(message="注册学生账号已停用", account_status="停用")

    def activate_registered_portal_student(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) == "启用":
                return RegisteredPortalStudentActionResponse(message="该注册学生账号已启用", account_status="启用")

            student["account_status"] = "启用"
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "启用账号", f'启用注册学生账号 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()
            return RegisteredPortalStudentActionResponse(message="注册学生账号已启用", account_status="启用")

    def reset_registered_portal_student_password(self, student_id: int) -> RegisteredPortalStudentActionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("已停用账号不可重置密码")

            temporary_password = self._generate_portal_temporary_password()
            student["password_hash"] = PASSWORD_CONTEXT.hash(temporary_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "重置密码", f'重置注册学生密码 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        email_sent = False
        if self._email_service.enabled():
            self._email_service.send_portal_admin_password_reset(
                str(student.get("full_name") or ""),
                str(student.get("email") or ""),
                temporary_password,
            )
            email_sent = True

        return RegisteredPortalStudentActionResponse(
            message="注册学生密码已重置",
            account_status=self._normalize_portal_account_status(student.get("account_status")),
            email_sent=email_sent,
            temporary_password=temporary_password,
        )

    def send_registered_portal_student_email(self, student_id: int, payload: RegisteredPortalStudentEmailRequest) -> RegisteredPortalStudentActionResponse:
        subject = payload.subject.strip()
        content = payload.content.strip()
        if not subject:
            raise ValueError("邮件主题不能为空")
        if not content:
            raise ValueError("邮件内容不能为空")

        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            operation_log = self._record_operation("学生管理", "注册学生", str(student_id), "发送邮件", f'向注册学生发送邮件 {student.get("full_name") or ""}')
            try:
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        email_sent = False
        if self._email_service.enabled():
            self._email_service.send_message(to_email=str(student.get("email") or ""), subject=subject, text_body=content)
            email_sent = True

        return RegisteredPortalStudentActionResponse(
            message="邮件发送请求已处理",
            account_status=self._normalize_portal_account_status(student.get("account_status")),
            email_sent=email_sent,
        )

    def get_student_board(self) -> StudentLifecycleBoard:
        distribution = Counter(item["status"] for item in self._list("students"))
        return StudentLifecycleBoard(
            summary=[StudentSummary(student_no=item["student_no"], full_name=item["full_name"], status=item["status"], advisor_name=item["advisor_name"], team_name=item["team_name"]) for item in self._list("students")[:8]],
            state_distribution=[StudentStateItem(label=label, count=count) for label, count in distribution.items()],
        )

    def get_students(
        self,
        keyword: str | None = None,
        status: str | None = None,
        advisor_name: str | None = None,
        center_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> StudentManagementResponse:
        try:
            items, total = self._postgres_store.list_students_page(
                keyword=keyword,
                status=status,
                advisor_name=advisor_name,
                center_name=center_name,
                page=page,
                page_size=page_size,
            )
            records = [StudentRecord(**item) for item in items]
            return StudentManagementResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query students from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("学生主数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_centers(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        director_id: int | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CenterListResponse:
        try:
            items, total = self._postgres_store.list_centers_page(
                keyword=keyword,
                is_enabled=is_enabled,
                director_id=director_id,
                page=page,
                page_size=page_size,
            )
            records = [
                CenterRecord(
                    **{
                        **item,
                        "director_name": self._resolve_center_director_name(item, self._normalize_name_list(item.get("advisor_names", []), item.get("director_name"))),
                        "advisor_names": self._normalize_name_list(item.get("advisor_names", []), item.get("director_name")),
                    }
                )
                for item in items
            ]
            return CenterListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query centers from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("团队中心数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_registered_portal_students(
        self,
        keyword: str | None = None,
        application_form_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RegisteredPortalStudentListResponse:
        try:
            items, total = self._postgres_store.list_registered_portal_students_page(
                keyword=keyword,
                application_form_status=application_form_status,
                page=page,
                page_size=page_size,
            )
            records = [RegisteredPortalStudentRecord(**item) for item in items]
            return RegisteredPortalStudentListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query registered portal students from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("门户注册学生数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def export_registered_portal_students(
        self,
        student_ids: list[int],
        *,
        keyword: str | None = None,
        application_form_status: str | None = None,
    ) -> bytes:
        normalized_ids = self._resolve_registered_portal_student_export_ids(
            student_ids,
            keyword=keyword,
            application_form_status=application_form_status,
        )
        if not normalized_ids:
            raise ValueError("当前筛选条件下无可导出的注册学生")

        plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}
        records: list[dict[str, Any]] = []
        for student_id in normalized_ids:
            latest_application_item = self._get_latest_registered_portal_application_item(student_id)
            _, raw_student = self._find_required("portal_students", student_id)
            portal_student = self.get_portal_student(student_id)
            application_id = int(latest_application_item.get("id") or 0) if latest_application_item is not None else None
            application_status = self._registered_portal_student_export_text(
                latest_application_item.get("application_status") if latest_application_item else None
            )
            application_business_key = self._registered_portal_student_export_text(
                latest_application_item.get("business_key") if latest_application_item else None
            )
            plan_id = portal_student.selected_plan_id
            plan_name = plan_name_map.get(int(plan_id or 0)) if plan_id is not None else None
            records.append(
                self._build_registered_portal_student_export_row(
                    portal_student,
                    application_status,
                    application_id,
                    application_business_key,
                    self._registered_portal_student_export_text(raw_student.get("created_at")),
                    plan_name,
                )
            )
        return build_registered_portal_students_template(records)

    def get_student_stats(self) -> StudentStats:
        distribution = Counter(item["status"] for item in self._list("students"))
        teams = self._list("teams")
        portal_students = self._list("portal_students")
        portal_submitted_total = len([item for item in portal_students if item.get("submitted_at")])
        return StudentStats(
            total_students=len(self._list("students")),
            active_students=distribution.get("在校", 0) + distribution.get("实习中", 0),
            outbound_students=distribution.get("外出研修", 0),
            thesis_students=distribution.get("学位论文阶段", 0),
            advisor_count=len({item["advisor_name"] for item in self._list("students")}),
            center_total=len(teams),
            enabled_center_total=len([item for item in teams if item.get("status") == "启用"]),
            registered_portal_total=len(portal_students),
            portal_submitted_total=portal_submitted_total,
            portal_unsubmitted_total=max(len(portal_students) - portal_submitted_total, 0),
        )

    def create_student(self, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            advisor_name = self._validate_student_payload(payload)
            item = {
                **payload.model_dump(exclude={"center_name"}),
                "advisor_name": advisor_name,
                "advisor_id": int(payload.advisor_id) if payload.advisor_id is not None else None,
                "team_name": payload.center_name,
            }
            item["id"] = self._next_id("students")
            self._list("students").insert(0, item)
            operation_log = self._record_operation("学生管理", "学生主档", str(item["id"]), "新增", f'新增学生 {item["full_name"]}')
            try:
                self._persist_student_change(item, operation_log, created=True)
                self._refresh_students_from_postgres()
            except Exception as exc:
                logger.warning("Incremental student create sync failed, fallback to full state save: %s", exc)
                self._save()
            return StudentRecord(center_name=item["team_name"], **{key: value for key, value in item.items() if key != "team_name"})

    def update_student(self, student_id: int, payload: StudentUpsert) -> StudentRecord:
        with self._lock:
            advisor_name = self._validate_student_payload(payload, current_student_id=student_id)
            index, item = self._find_required("students", student_id)
            updated = {
                **item,
                **payload.model_dump(exclude={"center_name"}),
                "advisor_name": advisor_name,
                "advisor_id": int(payload.advisor_id) if payload.advisor_id is not None else None,
                "team_name": payload.center_name,
                "id": student_id,
            }
            self._list("students")[index] = updated
            operation_log = self._record_operation("学生管理", "学生主档", str(student_id), "编辑", f'更新学生 {updated["full_name"]}')
            try:
                self._persist_student_change(updated, operation_log)
                self._refresh_students_from_postgres()
            except Exception as exc:
                logger.warning("Incremental student update sync failed, fallback to full state save: %s", exc)
                self._save()
            return StudentRecord(center_name=updated["team_name"], **{key: value for key, value in updated.items() if key != "team_name"})

    def delete_student(self, student_id: int) -> None:
        with self._lock:
            index, item = self._find_required("students", student_id)
            self._list("students").pop(index)
            operation_log = self._record_operation("学生管理", "学生主档", str(student_id), "删除", f'删除学生 {item["full_name"]}')
            try:
                self._postgres_store.sync_deleted_student(
                    student_id,
                    operation_log=operation_log,
                    counters={
                        "students": int(self._counters.get("students", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
                self._refresh_students_from_postgres()
            except Exception as exc:
                logger.warning("Incremental student delete sync failed, fallback to full state save: %s", exc)
                self._save()

    def create_center(self, payload: CenterUpsert) -> CenterRecord:
        with self._lock:
            item = self._validate_center_payload(payload)
            item["id"] = self._next_id("teams")
            item["team_code"] = f"CENTER-{item['id']:03d}"
            item.setdefault("department_name", "")
            item.setdefault("discipline_name", "")
            item.setdefault("research_directions", [])
            item.setdefault("established_on", item.get("created_on"))
            item.setdefault("description", None)
            self._list("teams").insert(0, item)
            self._record_operation("学生管理", "研究中心主数据", str(item["id"]), "新增研究中心", f'新增研究中心 {item["team_name"]}')
            try:
                self._postgres_store.sync_created_center(
                    item,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
                self._refresh_teams_from_postgres()
            except Exception as exc:
                logger.warning("Incremental center create sync failed, fallback to full state save: %s", exc)
                self._save()
            return self._build_center_record(item)

    def update_center(self, center_id: int, payload: CenterUpsert) -> CenterRecord:
        with self._lock:
            self._refresh_teams_from_postgres()
            self._refresh_students_from_postgres()
            index, current = self._find_required("teams", center_id)
            validated = self._validate_center_payload(payload, current_center_id=center_id)
            affected_students: list[dict[str, Any]] = []
            if current["team_name"] != validated["team_name"]:
                for student in self._list("students"):
                    if student.get("team_name") == current["team_name"]:
                        student["team_name"] = validated["team_name"]
                        affected_students.append(student)
            if any(student.get("team_name") == validated["team_name"] and student.get("advisor_name") not in validated["advisor_names"] for student in self._list("students")):
                raise ValueError("Current center members contain advisors outside the selected advisor set")
            updated = {**current, **validated, "id": center_id}
            self._list("teams")[index] = updated
            self._record_operation("学生管理", "研究中心主数据", str(center_id), "编辑研究中心", f'更新研究中心 {updated["team_name"]}')
            try:
                self._postgres_store.sync_updated_center(
                    updated,
                    affected_students=affected_students,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
                self._refresh_teams_from_postgres()
                self._refresh_students_from_postgres()
            except Exception as exc:
                logger.warning("Incremental center sync failed, fallback to full state save: %s", exc)
                self._save()
            return self._build_center_record(updated)

    def delete_center(self, center_id: int) -> None:
        with self._lock:
            index, item = self._find_required("teams", center_id)
            if any(student.get("team_name") == item["team_name"] for student in self._list("students")):
                raise ValueError("Center still has assigned students and cannot be deleted")
            self._list("teams").pop(index)
            self._record_operation("学生管理", "研究中心主数据", str(center_id), "删除研究中心", f'删除研究中心 {item["team_name"]}')
            try:
                self._postgres_store.sync_deleted_center(
                    center_id,
                    operation_log=self._list("operation_logs")[0] if self._list("operation_logs") else None,
                    counters={
                        "teams": int(self._counters.get("teams", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
                self._refresh_teams_from_postgres()
            except Exception as exc:
                logger.warning("Incremental center delete sync failed, fallback to full state save: %s", exc)
                self._save()

    def delete_centers(self, center_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for center_id in center_ids:
            self.delete_center(center_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)
