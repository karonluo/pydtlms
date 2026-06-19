from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
from types import SimpleNamespace
from uuid import uuid4
from typing import Any, TYPE_CHECKING

from psycopg.rows import dict_row

from app.core.config import settings
from app.services.recruitment_excel_service import build_registered_portal_students_template
from app.services.advisor_screening_pending_service import list_advisor_screening_pending_applications
from app.services.advisor_screening_submitted_service import (
    count_advisor_screening_submitted_applications,
    list_advisor_screening_submitted_applications,
)

from .management_service_shared import *


class RuntimeManagementStoreStudentsMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    _registered_portal_export_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="registered-portal-export")
    _registered_portal_export_jobs: dict[str, dict[str, Any]] = {}
    _registered_portal_export_jobs_lock = RLock()
    _ADVISOR_SCREENING_EXPORT_STATUSES = {
        "待导师初筛",
        "待导师初筛-第一志愿",
        "待导师初筛-第二志愿",
    }
    _REGISTERED_PORTAL_ROLLBACK_STAGE_CONFIG: dict[str, dict[str, Any]] = {
        "qualification_review": {"label": "资格审核", "node_key": "qualification_review", "application_status": "报名已提交", "rank": 1},
        "background_assessment": {"label": "背景评估", "node_key": "background_assessment", "application_status": "待背景评估", "rank": 2},
        "advisor_screening_first": {"label": "导师初筛-第一志愿", "node_key": "advisor_screening", "application_status": "待导师初筛-第一志愿", "rank": 3},
        "advisor_screening_second": {"label": "导师初筛-第二志愿", "node_key": "advisor_screening", "application_status": "待导师初筛-第二志愿", "rank": 4},
        "initial_screening_confirmation": {"label": "初筛确认", "node_key": "initial_screening_confirmation", "application_status": "待初筛确认", "rank": 5},
        "camp_interview": {"label": "入营面试", "node_key": "camp_interview", "application_status": "入营面试", "rank": 6},
    }

    @staticmethod
    def _registered_portal_export_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _registered_portal_export_namespace(value: Any) -> Any:
        if isinstance(value, dict):
            return SimpleNamespace(**{key: RuntimeManagementStoreStudentsMixin._registered_portal_export_namespace(item) for key, item in value.items()})
        if isinstance(value, list):
            return [RuntimeManagementStoreStudentsMixin._registered_portal_export_namespace(item) for item in value]
        return value

    @staticmethod
    def _registered_portal_export_job_file_name(export_scope: str | None = None) -> str:
        if str(export_scope or "").strip() in {"advisor_screening", "advisor_screening_pending", "advisor_screening_submitted"}:
            return f"导师初筛导出_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        return f"注册学生导出_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"

    @staticmethod
    def _principal_field_value(principal: Principal | dict[str, Any] | None, field_name: str) -> Any:
        if principal is None:
            return None
        if isinstance(principal, dict):
            return principal.get(field_name)
        return getattr(principal, field_name, None)

    @classmethod
    def _principal_role_codes(cls, principal: Principal | dict[str, Any] | None) -> set[str]:
        raw_roles = cls._principal_field_value(principal, "roles") or []
        return {str(item).strip() for item in raw_roles if str(item).strip()}

    @classmethod
    def _principal_permission_codes(cls, principal: Principal | dict[str, Any] | None) -> set[str]:
        raw_permissions = cls._principal_field_value(principal, "permissions") or []
        return {str(item).strip() for item in raw_permissions if str(item).strip()}

    @classmethod
    def _registered_portal_scope_advisor_name(cls, principal: Principal | dict[str, Any] | None) -> str | None:
        role_codes = cls._principal_role_codes(principal)
        if "advisor" not in role_codes or role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            return None
        full_name = str(cls._principal_field_value(principal, "full_name") or "").strip()
        if full_name:
            return full_name
        username = str(cls._principal_field_value(principal, "username") or "").strip()
        return username or None

    @classmethod
    def _resolve_registered_portal_advisor_filter(
        cls,
        advisor_names: list[str] | None,
        principal: Principal | dict[str, Any] | None,
    ) -> tuple[list[str], bool]:
        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        scoped_advisor_name = cls._registered_portal_scope_advisor_name(principal)
        if not scoped_advisor_name:
            return normalized_advisor_names, False
        if normalized_advisor_names:
            if scoped_advisor_name not in normalized_advisor_names:
                return [], True
            return [scoped_advisor_name], False
        return [scoped_advisor_name], False

    def _filter_registered_portal_student_ids_by_scope(
        self,
        student_ids: list[int],
        principal: Principal | dict[str, Any] | None,
    ) -> list[int]:
        scoped_advisor_name = self._registered_portal_scope_advisor_name(principal)
        if not scoped_advisor_name:
            return student_ids
        allowed_student_ids = {
            int(item.get("id") or 0)
            for item in self._list("portal_students")
            if str(item.get("selected_advisor_name") or "").strip() == scoped_advisor_name
        }
        return [student_id for student_id in student_ids if student_id in allowed_student_ids]

    @classmethod
    def _build_registered_portal_principal_snapshot(cls, principal: Principal | dict[str, Any]) -> dict[str, Any]:
        return {
            "username": str(cls._principal_field_value(principal, "username") or ""),
            "full_name": str(cls._principal_field_value(principal, "full_name") or ""),
            "roles": sorted(cls._principal_role_codes(principal)),
            "permissions": [str(item) for item in (cls._principal_field_value(principal, "permissions") or [])],
        }

    @classmethod
    def _registered_portal_background_assessment_filter_username(
        cls,
        principal: Principal | dict[str, Any] | None,
        *,
        show_all_background_assessed: bool,
    ) -> str | None:
        if show_all_background_assessed:
            return None
        role_codes = cls._principal_role_codes(principal)
        if not role_codes.intersection({"AILABMGT", "academy_admin"}):
            return None
        if "platform_admin" in role_codes:
            return None
        username = str(cls._principal_field_value(principal, "username") or "").strip()
        return username or None

    def _advisor_user_id_by_username(self, username: str | None) -> int | None:
        postgres_store = getattr(self, "_postgres_store", None)
        resolver = getattr(postgres_store, "_advisor_user_id_by_username", None)
        if callable(resolver):
            advisor_user_id = resolver(username)
            advisor_user_id_text = str(advisor_user_id or "").strip()
            return int(advisor_user_id_text) if advisor_user_id_text else None
        return None

    def _registered_portal_advisor_center_name(self, advisor_name: str | None) -> str | None:
        normalized_name = str(advisor_name or "").strip()
        if not normalized_name:
            return None

        postgres_store = getattr(self, "_postgres_store", None)
        connect = getattr(postgres_store, "_connect", None)
        if callable(connect):
            try:
                with connect(settings.postgres_db) as conn:
                    conn.row_factory = dict_row
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            SELECT t.team_name
                            FROM dtlms_users u
                            JOIN dtlms_user_roles ur ON ur.user_id = u.id
                            JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                            JOIN dtlms_team_advisors ta ON ta.advisor_user_id = u.id AND ta.is_deleted = FALSE
                            JOIN dtlms_teams t ON t.id = ta.team_id AND t.is_deleted = FALSE
                            WHERE u.full_name = %s
                              AND u.is_deleted = FALSE
                              AND r.role_code = 'advisor'
                            ORDER BY t.id DESC
                            LIMIT 1
                            """,
                            (normalized_name,),
                        )
                        row = cur.fetchone()
                        if row:
                            return self._registered_portal_student_export_text(row.get("team_name"))
            except Exception:
                pass

        list_centers_page = getattr(postgres_store, "list_centers_page", None)
        if callable(list_centers_page):
            try:
                items, _ = list_centers_page(
                    keyword=None,
                    is_enabled=None,
                    director_ids=None,
                    page=1,
                    page_size=1000,
                )
                items = []
            except Exception:
                pass
            for item in items:
                row = dict(item)
                center_name = self._registered_portal_student_export_text(row.get("center_name") or row.get("team_name"))
                director_name = self._registered_portal_student_export_text(row.get("director_name") or row.get("lead_user_name"))
                advisor_names = [self._registered_portal_student_export_text(value) for value in (row.get("advisor_names") or [])]
                if normalized_name == director_name or normalized_name in {value for value in advisor_names if value}:
                    return center_name
        return None

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
                plan_id=job.get("plan_id"),
                application_form_status=job.get("application_form_status"),
                recruitment_application_status=job.get("recruitment_application_status"),
                advisor_names=list(job.get("advisor_names") or []),
                first_choice_advisor_names=list(job.get("first_choice_advisor_names") or []),
                second_choice_advisor_names=list(job.get("second_choice_advisor_names") or []),
                export_scope=job.get("export_scope"),
                principal=job.get("principal_snapshot"),
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
                "file_name": self._registered_portal_export_job_file_name(payload.export_scope),
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
            "plan_id": payload.plan_id,
            "application_form_status": payload.application_form_status,
            "recruitment_application_status": payload.recruitment_application_status,
            "advisor_names": list(payload.advisor_names),
            "first_choice_advisor_names": list(payload.first_choice_advisor_names),
            "second_choice_advisor_names": list(payload.second_choice_advisor_names),
            "export_scope": payload.export_scope,
            "principal_snapshot": self._build_registered_portal_principal_snapshot(principal),
        }
        with self._registered_portal_export_jobs_lock:
            self._registered_portal_export_jobs[job_id] = job
        self._registered_portal_export_executor.submit(self._run_registered_portal_export_job, job_id)
        return RegisteredPortalStudentExportJobCreateResponse(
            message="开始导出，请等待完成",
            job=self._build_registered_portal_export_job_record(job),
        )

    @classmethod
    def _registered_portal_rollback_stage_config(cls, stage_key: str) -> dict[str, Any]:
        config = cls._REGISTERED_PORTAL_ROLLBACK_STAGE_CONFIG.get(str(stage_key).strip())
        if config is None:
            raise ValueError("不支持退回到所选环节")
        return config

    @classmethod
    def _registered_portal_rollback_stage_label(cls, stage_key: str) -> str:
        return str(cls._registered_portal_rollback_stage_config(stage_key)["label"])

    def _infer_registered_portal_current_stage(
        self,
        application: dict[str, Any],
        workflow_task: dict[str, Any] | None,
    ) -> str:
        task_node_key = str((workflow_task or {}).get("node_key") or "").strip()
        application_status = str(application.get("application_status") or "").strip()
        advisor_round = str(application.get("advisor_screening_round") or "").strip()
        first_choice_score = application.get("first_choice_screening_score")
        second_choice_score = application.get("second_choice_screening_score")

        if task_node_key == "qualification_review":
            return "qualification_review"
        if task_node_key == "background_assessment":
            return "background_assessment"
        if task_node_key == "advisor_screening":
            return "advisor_screening_second" if application_status == "待导师初筛-第二志愿" or advisor_round == "second_choice" else "advisor_screening_first"
        if task_node_key == "initial_screening_confirmation":
            return "initial_screening_confirmation"
        if task_node_key == "camp_interview":
            return "camp_interview"

        if application_status in {"报名已提交", "驳回重填"}:
            return "qualification_review"
        if application_status == "待背景评估":
            return "background_assessment"
        if application_status == "待导师初筛-第一志愿":
            return "advisor_screening_first"
        if application_status == "待导师初筛-第二志愿":
            return "advisor_screening_second"
        if application_status == "待初筛确认":
            return "initial_screening_confirmation"
        if application_status == "入营面试":
            return "camp_interview"
        if application_status == "报名终止":
            if str(application.get("initial_screening_status") or "").strip() == "confirmed" or application.get("initial_screening_result") is not None:
                return "initial_screening_confirmation"
            if second_choice_score is not None or advisor_round == "second_choice":
                return "advisor_screening_second"
            if first_choice_score is not None or str(application.get("advisor_screening_status") or "").strip() in {"submitted", "passed", "rejected"}:
                return "advisor_screening_first"
            try:
                if self._postgres_store.list_background_assessments(int(application.get("id") or 0)):
                    return "background_assessment"
            except Exception:
                pass
            return "qualification_review"
        raise ValueError("当前报名申请环节不支持退回")

    def _build_registered_portal_rollback_application(
        self,
        application: dict[str, Any],
        target_stage: str,
    ) -> tuple[dict[str, Any], dict[str, bool]]:
        updated = dict(application)
        cleanup_flags = {
            "clear_background_assessments": False,
            "clear_initial_screening_confirmation": False,
        }
        updated["next_stage_name"] = None

        def clear_initial_confirmation_fields() -> None:
            updated["initial_screening_status"] = None
            updated["initial_screening_result"] = None
            updated["initial_screening_confirmed_at"] = None
            updated["initial_screening_confirmer_username"] = None
            updated["initial_screening_confirmer_name"] = None
            updated["initial_screening_notification_status"] = None
            updated["initial_screening_notification_sent_at"] = None

        if target_stage == "qualification_review":
            updated["application_status"] = "报名已提交"
            updated["advisor_screening_status"] = None
            updated["advisor_screening_round"] = None
            updated["first_choice_screening_batch_id"] = None
            updated["second_choice_screening_batch_id"] = None
            updated["first_choice_screening_submitted_at"] = None
            updated["second_choice_screening_submitted_at"] = None
            updated["first_choice_screening_score"] = None
            updated["second_choice_screening_score"] = None
            clear_initial_confirmation_fields()
            cleanup_flags["clear_background_assessments"] = True
            cleanup_flags["clear_initial_screening_confirmation"] = True
            return updated, cleanup_flags

        if target_stage == "background_assessment":
            updated["application_status"] = "待背景评估"
            updated["advisor_screening_status"] = None
            updated["advisor_screening_round"] = None
            updated["first_choice_screening_batch_id"] = None
            updated["second_choice_screening_batch_id"] = None
            updated["first_choice_screening_submitted_at"] = None
            updated["second_choice_screening_submitted_at"] = None
            updated["first_choice_screening_score"] = None
            updated["second_choice_screening_score"] = None
            clear_initial_confirmation_fields()
            cleanup_flags["clear_background_assessments"] = True
            cleanup_flags["clear_initial_screening_confirmation"] = True
            return updated, cleanup_flags

        if target_stage == "advisor_screening_first":
            updated["application_status"] = "待导师初筛-第一志愿"
            updated["advisor_screening_status"] = "pending"
            updated["advisor_screening_round"] = "first_choice"
            updated["first_choice_screening_batch_id"] = None
            updated["second_choice_screening_batch_id"] = None
            updated["first_choice_screening_submitted_at"] = None
            updated["second_choice_screening_submitted_at"] = None
            updated["first_choice_screening_score"] = None
            updated["second_choice_screening_score"] = None
            clear_initial_confirmation_fields()
            cleanup_flags["clear_initial_screening_confirmation"] = True
            return updated, cleanup_flags

        if target_stage == "advisor_screening_second":
            updated["application_status"] = "待导师初筛-第二志愿"
            updated["advisor_screening_status"] = "pending"
            updated["advisor_screening_round"] = "second_choice"
            updated["second_choice_screening_batch_id"] = None
            updated["second_choice_screening_submitted_at"] = None
            updated["second_choice_screening_score"] = None
            clear_initial_confirmation_fields()
            cleanup_flags["clear_initial_screening_confirmation"] = True
            return updated, cleanup_flags

        if target_stage == "initial_screening_confirmation":
            screening_round = str(updated.get("advisor_screening_round") or "").strip()
            updated["application_status"] = "待初筛确认"
            updated["advisor_screening_status"] = "submitted"
            updated["advisor_screening_round"] = screening_round or "first_choice"
            updated["initial_screening_status"] = "pending"
            updated["initial_screening_result"] = None
            updated["initial_screening_confirmed_at"] = None
            updated["initial_screening_confirmer_username"] = None
            updated["initial_screening_confirmer_name"] = None
            updated["initial_screening_notification_status"] = "pending"
            updated["initial_screening_notification_sent_at"] = None
            cleanup_flags["clear_initial_screening_confirmation"] = True
            return updated, cleanup_flags

        if target_stage == "camp_interview":
            updated["application_status"] = "入营面试"
            updated["initial_screening_status"] = "confirmed"
            updated["initial_screening_result"] = "passed"
            updated["next_stage_name"] = "入营面试"
            return updated, cleanup_flags

        raise ValueError("不支持退回到所选环节")

    def rollback_registered_portal_student_stage(
        self,
        student_id: int,
        payload: RegisteredPortalStudentRollbackStageRequest,
        *,
        principal: Principal | dict[str, Any] | None = None,
    ) -> RegisteredPortalStudentActionResponse:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": []})
        role_codes = {str(item).strip() for item in principal_summary.get("roles", []) if str(item).strip()}
        permission_codes = self._principal_permission_codes(principal_summary)
        if "platform_admin" not in role_codes and "recruitment_registered_students:write" not in permission_codes:
            raise PermissionError("仅平台管理员或书院管理员可退回注册学生报名环节")

        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            application = self._get_latest_registered_portal_application_item(
                student_id,
                selected_plan_id=int(student.get("selected_plan_id") or 0) or None,
            )
            if application is None:
                raise ValueError("当前注册学生尚未生成报名申请")
            if not str(application.get("business_key") or "").strip():
                raise ValueError("当前报名申请缺少业务编号，无法执行退回")

            workflow_located = self._workflow_task_index_by_business_key(str(application.get("business_key") or ""))
            current_task = dict(workflow_located[1]) if workflow_located else None
            current_stage = self._infer_registered_portal_current_stage(application, current_task)
            current_rank = int(self._registered_portal_rollback_stage_config(current_stage)["rank"])
            target_stage = str(payload.target_stage or "").strip()
            target_config = self._registered_portal_rollback_stage_config(target_stage)
            target_rank = int(target_config["rank"])
            if target_rank > current_rank:
                raise ValueError("仅可退回到当前环节或更前的环节")

            updated_application, cleanup_flags = self._build_registered_portal_rollback_application(application, target_stage)
            updated_application["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            updated_task, _ = self._sync_managed_workflow_task(
                "recruitment_application",
                updated_application,
                existing_task=current_task,
            )
            if updated_task.get("node_key"):
                updated_task["due_at"] = self._workflow_due_at("recruitment_application", str(updated_task["node_key"]))
            rollback_label = str(target_config["label"])
            rollback_comment = str(payload.comment or "").strip() or f"平台管理员退回至{rollback_label}"
            previous_node_label = str((current_task or {}).get("current_node") or self._registered_portal_rollback_stage_label(current_stage))
            updated_task["latest_comment"] = rollback_comment
            updated_task.setdefault("history", []).append(
                {
                    "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "operator_username": principal_summary["username"],
                    "operator_full_name": principal_summary["full_name"],
                    "action": "rollback_stage",
                    "action_label": f"退回至{rollback_label}",
                    "from_node": previous_node_label,
                    "to_node": str(updated_task.get("current_node") or rollback_label),
                    "result_status": str(updated_task.get("status") or "处理中"),
                    "comment": rollback_comment,
                }
            )
            self._ensure_workflow_engine_metadata(updated_task)

            operation_log = self._record_operation(
                "学生管理",
                "注册学生",
                str(student_id),
                "退回环节",
                f'将 {updated_application.get("student_name") or student.get("full_name") or ""} 的报名申请退回至 {rollback_label}',
                operator_username=principal_summary["username"],
            )
            try:
                self._postgres_store.rollback_recruitment_application_stage(
                    updated_application,
                    updated_task,
                    clear_background_assessments=cleanup_flags["clear_background_assessments"],
                    clear_initial_screening_confirmation=cleanup_flags["clear_initial_screening_confirmation"],
                    operation_log=operation_log,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                )
            except Exception as exc:
                logger.exception("Persist registered portal rollback failed")
                raise RuntimeError("退回环节持久化失败，请稍后重试或联系管理员") from exc

            application_index, _ = self._find_required("recruitment_applications", int(application["id"]))
            self._list("recruitment_applications")[application_index] = updated_application
            if workflow_located:
                self._list("workflow_tasks")[workflow_located[0]] = updated_task
            else:
                self._list("workflow_tasks").insert(0, updated_task)

        email_sent = bool(self._email_service.workflow_notifications_enabled() and str(updated_application.get("email") or "").strip())
        if email_sent:
            self._email_service.send_recruitment_stage_rollback(
                student_name=str(updated_application.get("student_name") or student.get("full_name") or ""),
                email=str(updated_application.get("email") or ""),
                business_key=str(updated_application.get("business_key") or ""),
                target_stage_label=rollback_label,
                plan_name=str(updated_application.get("plan_name") or "").strip() or None,
            )

        return RegisteredPortalStudentActionResponse(
            message=f"已退回至{rollback_label}",
            account_status=self._normalize_portal_account_status(student.get("account_status")),
            email_sent=email_sent,
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
    def _registered_portal_summary_text(value: Any, *, field_name: str | None = None) -> str | None:
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            value = value.model_dump(mode="json")
        elif hasattr(value, "__dict__"):
            value = vars(value)
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            if text[:1] in {"{", "["}:
                try:
                    value = json.loads(text)
                except json.JSONDecodeError:
                    return text
            else:
                return text
        rendered = RuntimeManagementStoreStudentsMixin._registered_portal_render_summary_value(value, field_name=field_name)
        if rendered is None:
            return None
        text = rendered.strip()
        return text or None

    @staticmethod
    def _registered_portal_render_summary_value(value: Any, *, field_name: str | None = None) -> str | None:
        if isinstance(value, list):
            rendered_items = [
                item_text
                for item_text in (
                    RuntimeManagementStoreStudentsMixin._registered_portal_render_summary_item(item, field_name=field_name)
                    for item in value
                )
                if item_text
            ]
            if not rendered_items:
                return None
            return "\n".join(f"{index}. {item_text}" for index, item_text in enumerate(rendered_items, start=1))
        if isinstance(value, dict):
            return RuntimeManagementStoreStudentsMixin._registered_portal_render_summary_item(value, field_name=field_name)
        return RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(value)

    @staticmethod
    def _registered_portal_render_summary_item(value: Any, *, field_name: str | None = None) -> str | None:
        if not isinstance(value, dict):
            return RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(value)

        def render_text(item_key: str) -> str | None:
            item_value = value.get(item_key)
            if item_value in (None, "", [], {}):
                return None
            if isinstance(item_value, (dict, list)):
                rendered_value = RuntimeManagementStoreStudentsMixin._registered_portal_render_summary_value(item_value, field_name=field_name)
                return rendered_value.strip() if rendered_value else None
            return RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(item_value)

        if field_name == "education_experience":
            parts = [
                render_text("education_stage"),
                render_text("school_name"),
                render_text("major_name"),
                RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(
                    " - ".join(part for part in [render_text("start_month"), render_text("end_month")] if part)
                ),
                render_text("average_score"),
                render_text("gpa"),
                render_text("ranking"),
                RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(
                    " / ".join(part for part in [render_text("verifier_name"), render_text("verifier_phone")] if part)
                ),
            ]
        elif field_name == "practice_experience":
            parts = [
                RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(
                    " - ".join(part for part in [render_text("start_month"), render_text("end_month")] if part)
                ),
                render_text("organization_name"),
                render_text("position_name"),
                render_text("responsibility") or render_text("responsibility_text"),
                RuntimeManagementStoreStudentsMixin._registered_portal_student_export_text(
                    " / ".join(part for part in [render_text("verifier_name"), render_text("verifier_phone")] if part)
                ),
            ]
        elif field_name == "family_info":
            parts = [
                render_text("relation_type"),
                render_text("member_name"),
                render_text("employer_name"),
                render_text("job_title"),
                render_text("contact_phone"),
            ]
        elif field_name == "recommendation_notes":
            parts = [
                render_text("achievement_type"),
                render_text("achievement_month"),
                render_text("paper_title"),
                render_text("journal_or_conference"),
                render_text("publish_or_index_month"),
                render_text("author_order"),
                render_text("award_name"),
                render_text("awarding_org"),
                render_text("award_level"),
                render_text("award_year"),
                render_text("award_rank"),
                render_text("description_text"),
                render_text("responsibility_text"),
            ]
        elif field_name == "personal_statement_text":
            parts = [render_text(key) for key in value.keys()]
        else:
            parts = [f"{key}：{render_text(key)}" for key in value.keys() if render_text(key)]

        cleaned_parts = [part for part in parts if part]
        if not cleaned_parts:
            return None
        return "，".join(cleaned_parts)

    @staticmethod
    def _registered_portal_json_text(value: Any) -> str | None:
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            value = value.model_dump(mode="json")
        elif hasattr(value, "__dict__"):
            value = vars(value)
        if value in ({}, [], ""):
            return None
        return json.dumps(
            value,
            ensure_ascii=False,
            default=lambda item: item.model_dump(mode="json")
            if hasattr(item, "model_dump")
            else vars(item)
            if hasattr(item, "__dict__")
            else item,
        )

    @staticmethod
    def _registered_portal_application_sort_key(
        application: dict[str, Any],
        *,
        selected_plan_id: int | None = None,
    ) -> tuple[int, str, int]:
        plan_matched = 0
        if selected_plan_id is not None:
            try:
                plan_matched = 1 if int(application.get("plan_id") or 0) == int(selected_plan_id) else 0
            except Exception:
                plan_matched = 0
        return (
            plan_matched,
            str(application.get("applied_at") or application.get("created_at") or ""),
            int(application.get("id") or 0),
        )

    def _get_latest_registered_portal_application_item(
        self,
        student_id: int,
        *,
        selected_plan_id: int | None = None,
    ) -> dict[str, Any] | None:
        latest_application: dict[str, Any] | None = None
        for application in self._list("recruitment_applications"):
            if int(application.get("portal_student_id") or 0) != int(student_id):
                continue
            if latest_application is None or self._registered_portal_application_sort_key(
                application,
                selected_plan_id=selected_plan_id,
            ) >= self._registered_portal_application_sort_key(
                latest_application,
                selected_plan_id=selected_plan_id,
            ):
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
        normalized_application_status = str(application_status or "").strip()
        if normalized_application_status in {"驳回重填", "returned"}:
            return "驳回重填", None
        if normalized_submitted_at:
            return "已填写报名", normalized_submitted_at
        return "未填写报名", None

    def _resolve_registered_portal_student_export_ids(
        self,
        student_ids: list[int],
        *,
        keyword: str | None,
        plan_id: int | None = None,
        application_form_status: str | None,
        recruitment_application_status: str | None,
        show_all_background_assessed: bool,
        advisor_names: list[str] | None,
        first_choice_advisor_names: list[str] | None,
        second_choice_advisor_names: list[str] | None,
        first_choice_center_names: list[str] | None,
        second_choice_center_names: list[str] | None,
        export_scope: str | None = None,
        principal: Principal | dict[str, Any] | None = None,
    ) -> list[int]:
        if str(export_scope or "").strip() == "advisor_screening":
            return self._resolve_advisor_screening_portal_student_export_ids(
                student_ids,
                keyword=keyword,
                plan_id=plan_id,
                advisor_names=advisor_names,
                principal=principal,
            )

        normalized_ids: list[int] = []
        seen_ids: set[int] = set()
        for raw_id in student_ids:
            student_id = int(raw_id)
            if student_id <= 0 or student_id in seen_ids:
                continue
            seen_ids.add(student_id)
            normalized_ids.append(student_id)
        if normalized_ids:
            return self._filter_registered_portal_student_ids_by_scope(normalized_ids, principal)

        total_hint = max(len(self._list("portal_students")), 1)
        try:
            response = self.get_registered_portal_students(
                keyword=keyword,
                application_form_status=application_form_status,
                recruitment_application_status=recruitment_application_status,
                show_all_background_assessed=show_all_background_assessed,
                advisor_names=advisor_names,
                first_choice_advisor_names=first_choice_advisor_names,
                second_choice_advisor_names=second_choice_advisor_names,
                first_choice_center_names=first_choice_center_names,
                second_choice_center_names=second_choice_center_names,
                page=1,
                page_size=total_hint,
                principal=principal,
            )
            return [item.id for item in response.items]
        except DatabaseUnavailableError:
            return self._resolve_registered_portal_student_export_ids_from_state(
                keyword=keyword,
                application_form_status=application_form_status,
                recruitment_application_status=recruitment_application_status,
                show_all_background_assessed=show_all_background_assessed,
                advisor_names=advisor_names,
                first_choice_advisor_names=first_choice_advisor_names,
                second_choice_advisor_names=second_choice_advisor_names,
                first_choice_center_names=first_choice_center_names,
                second_choice_center_names=second_choice_center_names,
                principal=principal,
            )

    def _resolve_registered_portal_student_export_ids_from_state(
        self,
        *,
        keyword: str | None,
        application_form_status: str | None,
        recruitment_application_status: str | None,
        show_all_background_assessed: bool,
        advisor_names: list[str] | None,
        first_choice_advisor_names: list[str] | None,
        second_choice_advisor_names: list[str] | None,
        first_choice_center_names: list[str] | None,
        second_choice_center_names: list[str] | None,
        principal: Principal | dict[str, Any] | None,
    ) -> list[int]:
        effective_advisor_names, force_empty = self._resolve_registered_portal_advisor_filter(advisor_names, principal)
        if force_empty:
            return []
        normalized_first_choice_advisor_names = [str(item).strip() for item in (first_choice_advisor_names or []) if str(item).strip()]
        normalized_second_choice_advisor_names = [str(item).strip() for item in (second_choice_advisor_names or []) if str(item).strip()]
        normalized_first_choice_center_names = [str(item).strip() for item in (first_choice_center_names or []) if str(item).strip()]
        normalized_second_choice_center_names = [str(item).strip() for item in (second_choice_center_names or []) if str(item).strip()]

        keyword_text = str(keyword or "").strip().lower()
        plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}
        matched_ids: list[int] = []

        for student in self._list("portal_students"):
            student_id = int(student.get("id") or 0)
            if student_id <= 0:
                continue

            selected_advisor_name = str(student.get("selected_advisor_name") or "").strip()
            if effective_advisor_names and selected_advisor_name not in effective_advisor_names:
                continue

            latest_application = self._get_latest_registered_portal_application_item(
                student_id,
                selected_plan_id=int(student.get("selected_plan_id") or 0) or None,
            )
            latest_first_choice_name = str((latest_application.get("first_choice") if latest_application else student.get("first_choice")) or "").strip()
            latest_second_choice_name = str((latest_application.get("second_choice") if latest_application else student.get("second_choice")) or "").strip()
            latest_first_choice_center_name = self._registered_portal_advisor_center_name(latest_first_choice_name)
            latest_second_choice_center_name = self._registered_portal_advisor_center_name(latest_second_choice_name)
            if normalized_first_choice_advisor_names and latest_first_choice_name not in normalized_first_choice_advisor_names:
                continue
            if normalized_second_choice_advisor_names and latest_second_choice_name not in normalized_second_choice_advisor_names:
                continue
            if normalized_first_choice_center_names and str(latest_first_choice_center_name or "").strip() not in normalized_first_choice_center_names:
                continue
            if normalized_second_choice_center_names and str(latest_second_choice_center_name or "").strip() not in normalized_second_choice_center_names:
                continue
            application_status, _ = self._registered_portal_application_form_status(
                student.get("submitted_at"),
                str(latest_application.get("application_status") or "") if latest_application else None,
            )
            normalized_status = str(application_form_status or "").strip()
            if normalized_status and application_status != normalized_status:
                continue

            normalized_recruitment_status = str(recruitment_application_status or "").strip()
            latest_recruitment_status = str(latest_application.get("application_status") or "").strip() if latest_application else ""
            if normalized_recruitment_status and latest_recruitment_status != normalized_recruitment_status:
                continue

            if keyword_text:
                plan_name = plan_name_map.get(int(student.get("selected_plan_id") or 0), "")
                candidate_no = str(latest_application.get("candidate_no") or "") if latest_application else ""
                business_key = str(latest_application.get("business_key") or "") if latest_application else ""
                searchable_values = [
                    str(student.get("full_name") or ""),
                    str(student.get("phone_number") or ""),
                    str(student.get("email") or ""),
                    str(student.get("id_number") or ""),
                    plan_name,
                    selected_advisor_name,
                    str(student.get("selected_team_name") or ""),
                    candidate_no,
                    business_key,
                ]
                if not any(keyword_text in value.lower() for value in searchable_values if value):
                    continue

            matched_ids.append(student_id)

        return matched_ids

    def _resolve_advisor_screening_portal_student_export_ids(
        self,
        student_ids: list[int],
        *,
        keyword: str | None,
        plan_id: int | None,
        advisor_names: list[str] | None,
        principal: Principal | dict[str, Any] | None,
    ) -> list[int]:
        normalized_ids: list[int] = []
        seen_input_ids: set[int] = set()
        for raw_id in student_ids:
            student_id = int(raw_id)
            if student_id <= 0 or student_id in seen_input_ids:
                continue
            seen_input_ids.add(student_id)
            normalized_ids.append(student_id)

        response = self.get_recruitment_applications(
            keyword=keyword,
            plan_id=plan_id,
            status=",".join(sorted(self._ADVISOR_SCREENING_EXPORT_STATUSES)),
            advisor_names=advisor_names,
            principal=principal,
            page=1,
            page_size=10000,
        )
        allowed_student_ids: list[int] = []
        seen_allowed_ids: set[int] = set()
        for application in response.items:
            portal_student_id = int(getattr(application, "portal_student_id", None) or 0)
            if portal_student_id <= 0 or portal_student_id in seen_allowed_ids:
                continue
            seen_allowed_ids.add(portal_student_id)
            allowed_student_ids.append(portal_student_id)

        if normalized_ids:
            allowed_set = set(allowed_student_ids)
            return [student_id for student_id in normalized_ids if student_id in allowed_set]
        return allowed_student_ids

    def _build_registered_portal_student_export_row(
        self,
        student: PortalStudentRecord,
        application_status: str | None,
        application_id: int | None,
        application_business_key: str | None,
        registered_at: str | None,
        plan_name: str | None,
        first_choice_advisor_name: str | None = None,
        first_choice_screening_score: Any = None,
        first_choice_center_name: str | None = None,
        second_choice_advisor_name: str | None = None,
        second_choice_screening_score: Any = None,
        second_choice_center_name: str | None = None,
        preference_overrides: list[Any] | None = None,
    ) -> dict[str, Any]:
        profile = student.profile
        draft = student.application_draft
        preferences = list(preference_overrides or ((draft.preferences if draft else []) or []))
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
            "portal_business_key": self._registered_portal_student_export_text(getattr(student, "business_key", None)),
            "candidate_no": self._registered_portal_student_export_text(getattr(student, "candidate_no", None)),
            "account_status": self._normalize_portal_account_status(student.account_status),
            "application_form_status": application_form_status,
            "selected_plan_id": student.selected_plan_id,
            "selected_plan_name": plan_name,
            "first_choice_advisor_name": self._registered_portal_student_export_text(first_choice_advisor_name),
            "first_choice_screening_score": self._registered_portal_student_export_text(first_choice_screening_score),
            "first_choice_center_name": self._registered_portal_student_export_text(first_choice_center_name),
            "second_choice_advisor_name": self._registered_portal_student_export_text(second_choice_advisor_name),
            "second_choice_screening_score": self._registered_portal_student_export_text(second_choice_screening_score),
            "second_choice_center_name": self._registered_portal_student_export_text(second_choice_center_name),
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
            "family_info": self._registered_portal_summary_text(student.family_info, field_name="family_info"),
            "education_experience": self._registered_portal_summary_text(student.education_experience, field_name="education_experience"),
            "practice_experience": self._registered_portal_summary_text(student.practice_experience, field_name="practice_experience"),
            "personal_profile": self._registered_portal_student_export_text(student.personal_profile),
            "recommendation_notes": self._registered_portal_summary_text(student.recommendation_notes, field_name="recommendation_notes"),
            "personal_statement_text": self._registered_portal_summary_text(student.personal_statement_text, field_name="personal_statement_text"),
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
            record[f"preference_{index}_advisor_user_id"] = getattr(preference, "advisor_user_id", None)
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

    def _build_registered_portal_student_export_row_from_detail(
        self,
        student_detail: dict[str, Any],
        *,
        application_status: str | None,
        application_id: int | None,
        application_business_key: str | None,
        registered_at: str | None,
        plan_name: str | None,
        first_choice_advisor_name: str | None = None,
        second_choice_advisor_name: str | None = None,
    ) -> dict[str, Any]:
        portal_student = PortalStudentRecord.model_validate(student_detail)
        return self._build_registered_portal_student_export_row(
            portal_student,
            application_status,
            application_id,
            application_business_key,
            registered_at,
            plan_name,
            first_choice_advisor_name=first_choice_advisor_name,
            second_choice_advisor_name=second_choice_advisor_name,
        )

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
        if self._email_service.workflow_notifications_enabled():
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
        # 旧入参 director_id（单值）保留以兼容老调用方，新代码请使用 director_ids（多值）
        director_id: int | None = None,
        director_ids: list[int] | None = None,
        principal: Principal | dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CenterListResponse:
        # 兼容处理：director_id（单值）合并进 director_ids（多值）；director_ids 优先
        _merged_director_ids: list[int] = list(director_ids or [])
        if director_id and int(director_id) not in _merged_director_ids:
            _merged_director_ids.append(int(director_id))
        _effective_director_ids: list[int] | None = _merged_director_ids or None
        try:
            items, total = self._postgres_store.list_centers_page(
                keyword=keyword,
                is_enabled=is_enabled,
                director_ids=_effective_director_ids,
                principal=principal,
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
        recruitment_application_status: str | None = None,
        show_all_background_assessed: bool = False,
        advisor_names: list[str] | None = None,
        first_choice_advisor_names: list[str] | None = None,
        second_choice_advisor_names: list[str] | None = None,
        first_choice_center_names: list[str] | None = None,
        second_choice_center_names: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        page_size: int = 10,
        principal: Principal | dict[str, Any] | None = None,
    ) -> RegisteredPortalStudentListResponse:
        effective_advisor_names, force_empty = self._resolve_registered_portal_advisor_filter(advisor_names, principal)
        if force_empty:
            return RegisteredPortalStudentListResponse(items=[], total=0, page=page, page_size=page_size)
        academy_admin_background_assessment_username = self._registered_portal_background_assessment_filter_username(
            principal,
            show_all_background_assessed=show_all_background_assessed,
        )
        try:
            items, total = self._postgres_store.list_registered_portal_students_page(
                keyword=keyword,
                application_form_status=application_form_status,
                recruitment_application_status=recruitment_application_status,
                exclude_background_assessed_username=academy_admin_background_assessment_username,
                advisor_names=effective_advisor_names,
                first_choice_advisor_names=first_choice_advisor_names,
                second_choice_advisor_names=second_choice_advisor_names,
                first_choice_center_names=first_choice_center_names,
                second_choice_center_names=second_choice_center_names,
                sort_by=sort_by,
                sort_order=sort_order,
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
        plan_id: int | None = None,
        application_form_status: str | None = None,
        recruitment_application_status: str | None = None,
        show_all_background_assessed: bool = False,
        advisor_names: list[str] | None = None,
        first_choice_advisor_names: list[str] | None = None,
        second_choice_advisor_names: list[str] | None = None,
        first_choice_center_names: list[str] | None = None,
        second_choice_center_names: list[str] | None = None,
        export_scope: str | None = None,
        principal: Principal | dict[str, Any] | None = None,
    ) -> bytes:
        export_scope = str(export_scope or "").strip()
        if export_scope in {"advisor_screening", "advisor_screening_pending", "advisor_screening_submitted"}:
            advisor_name = self._registered_portal_scope_advisor_name(principal)
            role_codes = self._principal_role_codes(principal)
            if "advisor" in role_codes and role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
                advisor_name = None
            advisor_user_id = self._advisor_user_id_by_username(advisor_name) if advisor_name else None
            plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}
            export_rows: list[dict[str, Any]] = []
            if export_scope == "advisor_screening_submitted":
                submitted_total = count_advisor_screening_submitted_applications(
                    keyword=keyword,
                    advisor_name=advisor_name,
                    advisor_user_id=advisor_user_id,
                )
                if submitted_total <= 0:
                    return build_registered_portal_students_template(export_rows)
                submitted_rows = list_advisor_screening_submitted_applications(
                    keyword=keyword,
                    advisor_name=advisor_name,
                    advisor_user_id=advisor_user_id,
                    page=1,
                    page_size=submitted_total,
                ).items
                for row in submitted_rows:
                    student_detail = self._postgres_store.get_portal_student_detail(int(row.student_id))
                    if student_detail is None:
                        continue
                    application_detail = self._postgres_store.get_recruitment_application_detail(int(row.application_id)) if row.application_id else None
                    selected_plan_id = int(student_detail.get("selected_plan_id") or row.plan_id or 0) or None
                    plan_name = plan_name_map.get(int(selected_plan_id or 0)) if selected_plan_id is not None else None
                    first_choice_center_name = self._registered_portal_advisor_center_name(row.first_choice)
                    second_choice_center_name = self._registered_portal_advisor_center_name(row.second_choice)
                    export_rows.append(
                        self._build_registered_portal_student_export_row_from_detail(
                            student_detail,
                            application_status=row.application_status,
                            application_id=row.application_id,
                            application_business_key=row.business_key,
                            registered_at=self._registered_portal_student_export_text(
                                student_detail.get("created_at")
                                or student_detail.get("registered_at")
                                or row.first_choice_screening_submitted_at
                            ),
                            plan_name=plan_name,
                            first_choice_advisor_name=row.first_choice,
                            first_choice_screening_score=(application_detail or {}).get("first_choice_screening_score") if application_detail else None,
                            first_choice_center_name=first_choice_center_name,
                            second_choice_advisor_name=row.second_choice,
                            second_choice_screening_score=(application_detail or {}).get("second_choice_screening_score") if application_detail else None,
                            second_choice_center_name=second_choice_center_name,
                        )
                    )
            else:
                pending_rows = list_advisor_screening_pending_applications(
                    keyword=keyword,
                    advisor_username=str(self._principal_field_value(principal, "username") or "") if principal else None,
                    advisor_name=advisor_name,
                    advisor_user_id=advisor_user_id,
                )
                if not pending_rows:
                    return build_registered_portal_students_template(export_rows)
                for row in pending_rows:
                    portal_student_id = int(row.get("student_id") or row.get("portal_student_id") or 0)
                    if portal_student_id <= 0:
                        continue
                    student_detail = self._postgres_store.get_portal_student_detail(portal_student_id)
                    if student_detail is None:
                        continue
                    application_id = int(row.get("application_id") or row.get("id") or 0) or None
                    application_detail = self._postgres_store.get_recruitment_application_detail(application_id) if application_id else None
                    selected_plan_id = int(student_detail.get("selected_plan_id") or (application_detail or {}).get("plan_id") or 0) or None
                    plan_name = plan_name_map.get(int(selected_plan_id or 0)) if selected_plan_id is not None else None
                    first_choice_center_name = self._registered_portal_advisor_center_name(row.get("first_choice"))
                    second_choice_center_name = self._registered_portal_advisor_center_name(row.get("second_choice"))
                    export_rows.append(
                        self._build_registered_portal_student_export_row_from_detail(
                            student_detail,
                            application_status=(application_detail or {}).get("application_status"),
                            application_id=application_id,
                            application_business_key=row.get("business_key"),
                            registered_at=self._registered_portal_student_export_text(
                                student_detail.get("created_at")
                                or student_detail.get("registered_at")
                                or row.get("first_choice_screening_submitted_at")
                                or row.get("second_choice_screening_submitted_at")
                            ),
                            plan_name=plan_name,
                            first_choice_advisor_name=row.get("first_choice"),
                            first_choice_screening_score=(application_detail or {}).get("first_choice_screening_score") if application_detail else None,
                            first_choice_center_name=first_choice_center_name,
                            second_choice_advisor_name=row.get("second_choice"),
                            second_choice_screening_score=(application_detail or {}).get("second_choice_screening_score") if application_detail else None,
                            second_choice_center_name=second_choice_center_name,
                        )
                    )
            return build_registered_portal_students_template(export_rows)
        normalized_ids = self._resolve_registered_portal_student_export_ids(
            student_ids,
            keyword=keyword,
            plan_id=plan_id,
            application_form_status=application_form_status,
            recruitment_application_status=recruitment_application_status,
            show_all_background_assessed=show_all_background_assessed,
            advisor_names=advisor_names,
            first_choice_advisor_names=first_choice_advisor_names,
            second_choice_advisor_names=second_choice_advisor_names,
            first_choice_center_names=first_choice_center_names,
            second_choice_center_names=second_choice_center_names,
            export_scope=export_scope,
            principal=principal,
        )
        if not normalized_ids:
            raise ValueError("当前筛选条件下无可导出的注册学生")

        def _preference_advisor_name(items: list[Any], index: int) -> str | None:
            if index < 0 or index >= len(items):
                return None
            item = items[index]
            if isinstance(item, dict):
                return item.get("advisor_name")
            return getattr(item, "advisor_name", None)

        plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}
        records: list[dict[str, Any]] = []
        for student_id in normalized_ids:
            student_detail = self._postgres_store.get_portal_student_detail(student_id)
            if student_detail is None:
                continue
            portal_student = self._registered_portal_export_namespace(student_detail)
            latest_application_item = self._get_latest_registered_portal_application_item(
                student_id,
                selected_plan_id=int(getattr(portal_student, "selected_plan_id", 0) or 0) or None,
            )
            application_id = int(latest_application_item.get("id") or 0) if latest_application_item is not None else None
            application_status = self._registered_portal_student_export_text(
                latest_application_item.get("application_status") if latest_application_item else getattr(portal_student, "application_status", None)
            )
            application_business_key = self._registered_portal_student_export_text(
                latest_application_item.get("business_key") if latest_application_item else getattr(portal_student, "business_key", None)
            )
            application_detail = self._postgres_store.get_recruitment_application_detail(application_id) if application_id else None
            preference_items = list((application_detail or {}).get("preferences") or []) if application_id else []
            if not preference_items:
                portal_draft = getattr(portal_student, "application_draft", None)
                preference_items = list(getattr(portal_draft, "preferences", []) or [])
            first_choice_advisor_name = self._registered_portal_student_export_text(
                (application_detail or {}).get("first_choice")
                or (latest_application_item.get("first_choice") if latest_application_item else None)
                or getattr(portal_student, "first_choice", None)
                or _preference_advisor_name(preference_items, 0)
            )
            second_choice_advisor_name = self._registered_portal_student_export_text(
                (application_detail or {}).get("second_choice")
                or (latest_application_item.get("second_choice") if latest_application_item else None)
                or getattr(portal_student, "second_choice", None)
                or _preference_advisor_name(preference_items, 1)
            )
            portal_application_draft = getattr(portal_student, "application_draft", None)
            first_choice_screening_score = (application_detail or {}).get("first_choice_screening_score")
            if first_choice_screening_score is None and latest_application_item is not None:
                first_choice_screening_score = latest_application_item.get("first_choice_screening_score")
            if first_choice_screening_score is None and isinstance(portal_application_draft, dict):
                first_choice_screening_score = portal_application_draft.get("first_choice_screening_score")
            if first_choice_screening_score is None:
                first_choice_screening_score = getattr(portal_student, "first_choice_screening_score", None)

            second_choice_screening_score = (application_detail or {}).get("second_choice_screening_score")
            if second_choice_screening_score is None and latest_application_item is not None:
                second_choice_screening_score = latest_application_item.get("second_choice_screening_score")
            if second_choice_screening_score is None and isinstance(portal_application_draft, dict):
                second_choice_screening_score = portal_application_draft.get("second_choice_screening_score")
            if second_choice_screening_score is None:
                second_choice_screening_score = getattr(portal_student, "second_choice_screening_score", None)
            plan_id = getattr(portal_student, "selected_plan_id", None)
            plan_name = plan_name_map.get(int(plan_id or 0)) if plan_id is not None else None
            records.append(
                self._build_registered_portal_student_export_row(
                    portal_student,
                    application_status,
                    application_id,
                    application_business_key,
                    self._registered_portal_student_export_text(getattr(portal_student, "created_at", None)),
                    plan_name,
                    first_choice_advisor_name=first_choice_advisor_name,
                    first_choice_screening_score=first_choice_screening_score,
                    first_choice_center_name=self._registered_portal_advisor_center_name(first_choice_advisor_name),
                    second_choice_advisor_name=second_choice_advisor_name,
                    second_choice_screening_score=second_choice_screening_score,
                    second_choice_center_name=self._registered_portal_advisor_center_name(second_choice_advisor_name),
                    preference_overrides=(
                        [self._registered_portal_export_namespace(item) for item in preference_items] if preference_items else None
                    ),
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