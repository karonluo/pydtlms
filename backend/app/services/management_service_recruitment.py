from __future__ import annotations

from typing import Any, TYPE_CHECKING, cast

from app.core.config import settings
from app.schemas.portal import PortalApplicationDeclarationData, PortalPersonalStatementData
from app.schemas.dashboard import (
    DashboardRecruitmentAdvisorChoiceDistribution,
    DashboardRecruitmentAdvisorChoiceDistributionResponse,
    DashboardRecruitmentAdvisorChoiceItem,
    DashboardUndergraduateSchoolStudentItem,
    DashboardUndergraduateSchoolStudentListResponse,
)
from app.schemas.recruitment import (
    CampOfferImportIssue,
    CampOfferImportResult,
    CampOfferListResponse,
    CampOfferRecord,
    CampOfferStats,
    CampOfferUpsert,
    RecruitApplicationRecord,
    RecruitPortalApplicationDetail,
)

from app.services.recruitment_excel_service import build_advisor_screening_template

from .management_service_shared import *


class RuntimeManagementStoreRecruitmentMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    @staticmethod
    def _normalize_screening_actor_values(principal_summary: dict[str, Any]) -> tuple[str, str]:
        return str(principal_summary.get("username") or "").strip(), str(principal_summary.get("full_name") or "").strip()

    @staticmethod
    def _resolve_portal_advisor_screening_status(application: RecruitApplicationRecord) -> str | None:
        screening_round = str(application.advisor_screening_round or "").strip()
        current_score = application.second_choice_screening_score if screening_round == "second_choice" else application.first_choice_screening_score
        if current_score is not None:
            return "已通过" if float(current_score) >= 80 else "不通过"

        normalized_status = str(application.advisor_screening_status or "").strip()
        if not normalized_status:
            return None
        return {
            "pending": "未填写",
            "submitted": "已提交",
            "passed": "已通过",
            "rejected": "不通过",
        }.get(normalized_status, normalized_status)

    def _resolve_advisor_screening_round(self, application: dict[str, Any]) -> str:
        normalized_round = str(application.get("advisor_screening_round") or "").strip()
        if normalized_round in {"first_choice", "second_choice"}:
            return normalized_round
        status = str(application.get("application_status") or "").strip()
        if status == "待导师初筛-第二志愿":
            return "second_choice"
        return "first_choice"

    def _principal_matches_screening_advisor(self, application: dict[str, Any], screening_round: str, principal_summary: dict[str, Any]) -> bool:
        role_codes = {str(item).strip() for item in principal_summary.get("roles", []) if str(item).strip()}
        if "platform_admin" in role_codes:
            return True

        username, full_name = self._normalize_screening_actor_values(principal_summary)
        expected_values = {username, full_name}
        expected_values = {item for item in expected_values if item}
        if not expected_values:
            return False

        advisor_candidates: set[str] = set()
        if screening_round == "first_choice":
            advisor_candidates.update(
                {
                    str(application.get("intended_advisor_name") or "").strip(),
                    str(application.get("first_choice") or "").strip(),
                }
            )
        else:
            advisor_candidates.add(str(application.get("second_choice") or "").strip())
        advisor_candidates = {item for item in advisor_candidates if item}
        return bool(advisor_candidates.intersection(expected_values))

    def _resolve_rescore_screening_round(self, application: dict[str, Any], principal_summary: dict[str, Any]) -> str:
        username, full_name = self._normalize_screening_actor_values(principal_summary)
        expected_values = {item for item in (username, full_name) if item}
        if not expected_values:
            raise PermissionError("当前账号不是该申请当前轮次的责任导师")

        first_choice_candidates = {
            str(application.get("first_choice") or "").strip(),
            str(application.get("intended_advisor_name") or "").strip(),
        }
        second_choice_candidates = {
            str(application.get("second_choice") or "").strip(),
        }

        first_choice_matched = bool({item for item in first_choice_candidates if item}.intersection(expected_values))
        second_choice_matched = bool({item for item in second_choice_candidates if item}.intersection(expected_values))

        if first_choice_matched and not second_choice_matched:
            return "first_choice"
        if second_choice_matched and not first_choice_matched:
            return "second_choice"
        if first_choice_matched and second_choice_matched:
            return "first_choice"
        raise PermissionError("当前账号不是该申请当前轮次的责任导师")

    @staticmethod
    def _build_rescore_block_message(screening_round: str, application: dict[str, Any]) -> str:
        first_choice_submitted = bool(application.get("first_choice_screening_submitted_at") or application.get("first_choice_screening_batch_id"))
        has_second_choice = bool(str(application.get("second_choice") or "").strip())
        second_choice_submitted = bool(application.get("second_choice_screening_submitted_at") or application.get("second_choice_screening_batch_id"))
        current_status = str(application.get("application_status") or "").strip()
        if screening_round == "first_choice":
            if not first_choice_submitted:
                return "第一志愿导师需要已提交后才能重新评分"
            if has_second_choice and second_choice_submitted:
                return "第二志愿导师已经提交，第一志愿导师不能重新评分"
            if current_status not in {"initial_screening_confirmation", "待初筛确认", "报名终止", "initial_screening_second", "待导师初筛-第二志愿"}:
                return "当前申请不在初筛确认或报名终止环节，无法重新评分"
            return ""
        second_choice_submitted = bool(application.get("second_choice_screening_submitted_at") or application.get("second_choice_screening_batch_id"))
        if not second_choice_submitted:
            return "第二志愿导师需要已提交后才能重新评分"
        if current_status not in {"initial_screening_confirmation", "待初筛确认", "报名终止"}:
            return "当前申请不在初筛确认或报名终止环节，无法重新评分"
        return ""

    @staticmethod
    def _advisor_screening_submission_locked(application: dict[str, Any], screening_round: str) -> bool:
        if screening_round == "second_choice":
            return bool(application.get("second_choice_screening_batch_id") or application.get("second_choice_screening_submitted_at"))
        return bool(application.get("first_choice_screening_batch_id") or application.get("first_choice_screening_submitted_at"))

    def _build_workflow_transition_record(
        self,
        task: dict[str, Any],
        updated_entity: dict[str, Any],
        *,
        next_node: str | None,
        task_status: str,
        comment: str | None,
        action: str,
        action_label: str,
        principal_summary: dict[str, Any],
    ) -> dict[str, Any]:
        definition = self._workflow_definition(str(task.get("flow_code") or ""))
        current_node_key = str(task.get("node_key") or "")
        current_node = definition["nodes"].get(current_node_key, {})
        updated_task = dict(task)
        updated_task["status"] = task_status
        updated_task["latest_comment"] = comment or action_label
        updated_task["form_summary"] = self._workflow_form_summary(str(task.get("flow_code") or ""), updated_entity)
        updated_task["node_key"] = next_node
        updated_task["current_node"] = definition["nodes"][next_node]["label"] if next_node else "流程结束"
        updated_task["current_handler"] = self._workflow_handler_display(str(task.get("flow_code") or ""), next_node, updated_entity) if next_node else "流程结束"
        updated_task["due_at"] = self._workflow_due_at(str(task.get("flow_code") or ""), next_node) if next_node else updated_task.get("due_at")
        updated_task.setdefault("history", []).append(
            {
                "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator_username": principal_summary["username"],
                "operator_full_name": principal_summary["full_name"],
                "action": action,
                "action_label": action_label,
                "from_node": str(current_node.get("label") or current_node_key or "流程节点"),
                "to_node": definition["nodes"][next_node]["label"] if next_node else "流程结束",
                "result_status": updated_task["status"],
                "comment": updated_task["latest_comment"],
            }
        )
        self._ensure_workflow_engine_metadata(updated_task)
        return updated_task

    @staticmethod
    def _build_recruitment_portal_application_detail(application: RecruitApplicationRecord) -> RecruitPortalApplicationDetail:
        personal_statement = application.personal_statement or PortalPersonalStatementData()
        if not personal_statement.supporting_material_attachment_url and application.material_list_attachment:
            personal_statement = personal_statement.model_copy(
                update={
                    "supporting_material_attachment_url": application.material_list_attachment,
                    "supporting_material_attachment_name": application.material_list_attachment_name,
                }
            )
        preferences = list(application.preferences or [])
        first_choice = application.first_choice or (preferences[0].advisor_name if len(preferences) > 0 else None)
        second_choice = application.second_choice or (preferences[1].advisor_name if len(preferences) > 1 else None)
        return RecruitPortalApplicationDetail(
            application_id=application.id,
            plan_id=application.plan_id,
            business_key=application.business_key,
            candidate_no=application.candidate_no,
            student_name=application.student_name,
            phone_number=application.phone_number,
            email=application.email,
            id_number=application.id_number,
            application_status=application.application_status,
            material_status=application.material_status,
            advisor_screening_status=RuntimeManagementStoreRecruitmentMixin._resolve_portal_advisor_screening_status(application),
            advisor_screening_round=application.advisor_screening_round,
            advisor_screening_submitted_at=application.advisor_screening_submitted_at,
            advisor_signature_base64=application.advisor_signature_base64,
            first_choice=first_choice,
            second_choice=second_choice,
            first_choice_id=application.first_choice_id,
            second_choice_id=application.second_choice_id,
            first_choice_screening_score=application.first_choice_screening_score,
            second_choice_screening_score=application.second_choice_screening_score,
            initial_screening_status=application.initial_screening_status,
            initial_screening_result=application.initial_screening_result,
            next_stage_name=application.next_stage_name,
            reviewer_name=application.reviewer_name,
            submitted_at=application.applied_at,
            background_assessments=list(application.background_assessments or []),
            qualification_review_history=list(application.qualification_review_history or []),
            profile=application.profile,
            source_channel=application.source_channel or application.discovery_channel,
            source_channel_other=application.source_channel_other,
            preferences=preferences,
            education_experiences=list(application.education_experiences or []),
            practice_experiences=list(application.practice_experiences or []),
            english_proficiencies=list(application.english_proficiencies or []),
            family_members=list(application.family_members or []),
            achievement_records=list(application.achievement_records or []),
            personal_statement=personal_statement,
            declaration=application.declaration or PortalApplicationDeclarationData(has_read_declaration=False),
        )

    def _build_recruit_plan_record(self, item: dict[str, Any]) -> RecruitPlanRecord:
        application_count = len([application for application in self._list("recruitment_applications") if application["plan_id"] == item["id"]])
        return RecruitPlanRecord(
            id=item["id"],
            plan_name=item["plan_name"],
            academic_term=f'{item["academic_year"]} {item["semester"]}',
            academic_year=item["academic_year"],
            semester=item["semester"],
            application_count=application_count,
            brochure_image_url=item.get("brochure_image_url"),
            plan_description=item.get("plan_description"),
        )

    def get_recruitment_workbench(self) -> RecruitWorkbench:
        status_counter = Counter(item["application_status"] for item in self._list("recruitment_applications"))
        return RecruitWorkbench(
            plans=[
                RecruitPlanSummary(
                    plan_name=plan.plan_name,
                    academic_term=plan.academic_term,
                    plan_description=plan.plan_description,
                    application_count=plan.application_count,
                )
                for plan in self.get_recruitment_plans().items
            ],
            pipeline=[
                {"stage": "报名已提交", "count": status_counter.get("报名已提交", 0), "status": "active"},
                {"stage": "资格审核通过", "count": status_counter.get("资格审核通过", 0), "status": "active"},
                {"stage": "材料评分中", "count": status_counter.get("材料评分中", 0), "status": "active"},
                {"stage": "面试完成", "count": status_counter.get("面试完成", 0), "status": "active"},
                {"stage": "预录取", "count": status_counter.get("预录取", 0) + status_counter.get("同意录取", 0), "status": "attention"},
            ],
            pending_tasks=[
                {"title": "资格审核待处理", "owner": "管理员", "due_text": "今日 18:00"},
                {"title": "评分人分配确认", "owner": "招生秘书", "due_text": "明日 12:00"},
                {"title": "面试组自动分配复核", "owner": "面试组织岗", "due_text": "两日内"},
            ],
        )

    def get_recruitment_plans(
        self,
        keyword: str | None = None,
        semester: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RecruitPlanListResponse:
        try:
            items, total = self._postgres_store.list_recruitment_plans_page(
                keyword=keyword,
                semester=semester,
                page=page,
                page_size=page_size,
            )
            records = [RecruitPlanRecord(**item) for item in items]
            return RecruitPlanListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query recruitment plans from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("招生计划数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def create_recruitment_plan(self, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item.setdefault("current_stage", "报名配置")
            item.setdefault("target_quota", 0)
            item.setdefault("interview_group_count", 0)
            item.setdefault("is_open", True)
            item["id"] = self._next_id("recruitment_plans")
            self._list("recruitment_plans").insert(0, item)
            operation_log = self._record_operation("招生管理", "招生计划", str(item["id"]), "新增", f'新增招生计划 {item["plan_name"]}')
            try:
                self._postgres_store.sync_recruitment_plan(
                    item,
                    operation_log,
                    counters={
                        "recruitment_plans": int(self._counters.get("recruitment_plans", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return self._build_recruit_plan_record(item)

    def update_recruitment_plan(self, plan_id: int, payload: RecruitPlanUpsert) -> RecruitPlanRecord:
        with self._lock:
            index, item = self._find_required("recruitment_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("recruitment_plans")[index] = updated
            operation_log = self._record_operation("招生管理", "招生计划", str(plan_id), "编辑", f'更新招生计划 {updated["plan_name"]}')
            try:
                self._postgres_store.sync_recruitment_plan(
                    updated,
                    operation_log,
                    counters={
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return self._build_recruit_plan_record(updated)

    def delete_recruitment_plan(self, plan_id: int) -> None:
        with self._lock:
            index, item = self._find_required("recruitment_plans", plan_id)
            has_applications = any(int(application.get("plan_id") or 0) == int(plan_id) for application in self._list("recruitment_applications"))
            if has_applications:
                raise ValueError("当前招生计划下仍有报名申请，不能删除")
            self._list("recruitment_plans").pop(index)
            operation_log = self._record_operation("招生管理", "招生计划", str(plan_id), "删除", f'删除招生计划 {item["plan_name"]}')
            try:
                self._postgres_store.delete_recruitment_plan(int(plan_id))
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def get_recruitment_applications(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        portal_student_only: bool = False,
        advisor_names: list[str] | None = None,
        principal: Any | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RecruitApplicationListResponse:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": [], "permissions": []})
        role_codes = {str(item) for item in principal_summary["roles"] if str(item).strip()}
        advisor_name = None
        advisor_user_id = None
        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if "advisor" in role_codes and not role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            advisor_name = str(principal_summary.get("full_name") or "").strip() or None
            try:
                advisor_user_id = int(principal_summary.get("user_id") or 0) or None
            except Exception:
                advisor_user_id = None
            if normalized_advisor_names and advisor_name not in normalized_advisor_names:
                return RecruitApplicationListResponse(items=[], total=0, page=page, page_size=page_size)
            normalized_advisor_names = [advisor_name] if advisor_name else []
        try:
            items, total = self._postgres_store.list_recruitment_applications_page(
                keyword=keyword,
                plan_id=plan_id,
                status=status,
                portal_student_only=portal_student_only,
                advisor_name=advisor_name,
                advisor_names=normalized_advisor_names or None,
                advisor_user_id=advisor_user_id,
                page=page,
                page_size=page_size,
            )
            records = [RecruitApplicationRecord(**item) for item in items]
            return RecruitApplicationListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query recruitment applications from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("招生报名数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_recruitment_application_detail(self, application_id: int) -> RecruitApplicationRecord:
        try:
            item = self._postgres_store.get_recruitment_application_detail(application_id)
            if item is not None:
                return RecruitApplicationRecord(**item)
        except Exception as exc:
            logger.warning("Query recruitment application detail from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("招生报名详情当前仅允许从数据库读取，PostgreSQL 查询失败") from exc
        raise DatabaseUnavailableError("招生报名详情当前仅允许从数据库读取，未找到对应记录")

    def _resolve_camp_offer_plan_id(self, explicit_plan_id: int | None = None) -> int:
        if explicit_plan_id is not None:
            return int(explicit_plan_id)
        latest_plan_id = self._postgres_store.get_latest_recruitment_plan_id()
        if latest_plan_id is None:
            raise ValueError("当前没有可用招生计划，无法确定 plan_id")
        return int(latest_plan_id)

    def _validate_camp_offer_candidate_no_exists(self, candidate_no: str) -> None:
        normalized_candidate_no = str(candidate_no or "").strip()
        if not normalized_candidate_no:
            raise ValueError("candidate_no 不能为空")
        items, total = self._postgres_store.list_recruitment_applications_page(keyword=normalized_candidate_no, page=1, page_size=5)
        matched = any(str(item.get("candidate_no") or "").strip() == normalized_candidate_no for item in items)
        if total <= 0 or not matched:
            raise ValueError(f"报名号不存在：{normalized_candidate_no}")

    def get_camp_offers(
        self,
        *,
        keyword: str | None = None,
        plan_id: int | None = None,
        is_sent_mail: bool | None = None,
        is_agree: bool | None = None,
        is_in_camp_selection: bool | None = None,
        first_choice_advisor: str | None = None,
        first_choice_team: str | None = None,
        first_choice_score_op: str | None = None,
        first_choice_score: float | None = None,
        second_choice_advisor: str | None = None,
        second_choice_team: str | None = None,
        second_choice_score_op: str | None = None,
        second_choice_score: float | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        page: int = 1,
        page_size: int = 10,
        principal: Any | None = None,
    ) -> CampOfferListResponse:
        visible_advisor_names = self._postgres_store.resolve_camp_offer_visible_advisor_names(principal)
        is_center_leader = self._postgres_store.resolve_camp_offer_is_center_leader(principal)
        items, total = self._postgres_store.list_camp_offers_page(
            keyword=keyword,
            plan_id=plan_id,
            is_sent_mail=is_sent_mail,
            is_agree=is_agree,
            is_in_camp_selection=is_in_camp_selection,
            first_choice_advisor=first_choice_advisor,
            first_choice_team=first_choice_team,
            first_choice_score_op=first_choice_score_op,
            first_choice_score=first_choice_score,
            second_choice_advisor=second_choice_advisor,
            second_choice_team=second_choice_team,
            second_choice_score_op=second_choice_score_op,
            second_choice_score=second_choice_score,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
            visible_advisor_names=visible_advisor_names,
            is_center_leader=is_center_leader,
        )
        records = [CampOfferRecord(**item) for item in items]
        return CampOfferListResponse(items=records, total=total, page=page, page_size=page_size)

    def get_camp_offer_detail(
        self,
        offer_id: int,
        principal: Any | None = None,
    ) -> CampOfferRecord:
        visible_advisor_names = self._postgres_store.resolve_camp_offer_visible_advisor_names(principal)
        is_center_leader = self._postgres_store.resolve_camp_offer_is_center_leader(principal)
        item = self._postgres_store.get_camp_offer_detail(
            int(offer_id),
            visible_advisor_names=visible_advisor_names,
            is_center_leader=is_center_leader,
        )
        if item is None:
            raise KeyError("Camp offer not found")
        return CampOfferRecord(**item)

    def count_camp_offer_stats(
        self,
        *,
        keyword: str | None = None,
        plan_id: int | None = None,
        is_sent_mail: bool | None = None,
        is_agree: bool | None = None,
        is_in_camp_selection: bool | None = None,
        first_choice_advisor: str | None = None,
        first_choice_team: str | None = None,
        first_choice_score_op: str | None = None,
        first_choice_score: float | None = None,
        second_choice_advisor: str | None = None,
        second_choice_team: str | None = None,
        second_choice_score_op: str | None = None,
        second_choice_score: float | None = None,
    ) -> dict[str, int]:
        return self._postgres_store.count_camp_offer_stats(
            keyword=keyword,
            plan_id=plan_id,
            is_sent_mail=is_sent_mail,
            is_agree=is_agree,
            is_in_camp_selection=is_in_camp_selection,
            first_choice_advisor=first_choice_advisor,
            first_choice_team=first_choice_team,
            first_choice_score_op=first_choice_score_op,
            first_choice_score=first_choice_score,
            second_choice_advisor=second_choice_advisor,
            second_choice_team=second_choice_team,
            second_choice_score_op=second_choice_score_op,
            second_choice_score=second_choice_score,
        )

    def get_camp_offer_stats(
        self,
        *,
        keyword: str | None = None,
        plan_id: int | None = None,
        is_sent_mail: bool | None = None,
        is_agree: bool | None = None,
        first_choice_advisor: str | None = None,
        first_choice_team: str | None = None,
        first_choice_score_op: str | None = None,
        first_choice_score: float | None = None,
        second_choice_advisor: str | None = None,
        second_choice_team: str | None = None,
        second_choice_score_op: str | None = None,
        second_choice_score: float | None = None,
    ) -> CampOfferStats:
        counts = self._postgres_store.count_camp_offer_stats(
            keyword=keyword,
            plan_id=plan_id,
            is_sent_mail=is_sent_mail,
            is_agree=is_agree,
            first_choice_advisor=first_choice_advisor,
            first_choice_team=first_choice_team,
            first_choice_score_op=first_choice_score_op,
            first_choice_score=first_choice_score,
            second_choice_advisor=second_choice_advisor,
            second_choice_team=second_choice_team,
            second_choice_score_op=second_choice_score_op,
            second_choice_score=second_choice_score,
        )
        return CampOfferStats(**counts)

    def export_camp_offers(
        self,
        *,
        keyword: str | None = None,
        plan_id: int | None = None,
        is_sent_mail: bool | None = None,
        is_agree: bool | None = None,
        is_in_camp_selection: bool | None = None,
        first_choice_advisor: str | None = None,
        first_choice_team: str | None = None,
        first_choice_score_op: str | None = None,
        first_choice_score: float | None = None,
        second_choice_advisor: str | None = None,
        second_choice_team: str | None = None,
        second_choice_score_op: str | None = None,
        second_choice_score: float | None = None,
        principal: Any | None = None,
    ) -> list[dict[str, Any]]:
        """Return all camp-offer rows matching the supplied filters (ignoring
        pagination). Used by the /camp-offers/export endpoint to build an
        Excel workbook for the operator."""

        visible_advisor_names = self._postgres_store.resolve_camp_offer_visible_advisor_names(principal)
        is_center_leader = self._postgres_store.resolve_camp_offer_is_center_leader(principal)
        items, _ = self._postgres_store.list_camp_offers_page(
            keyword=keyword,
            plan_id=plan_id,
            is_sent_mail=is_sent_mail,
            is_agree=is_agree,
            is_in_camp_selection=is_in_camp_selection,
            first_choice_advisor=first_choice_advisor,
            first_choice_team=first_choice_team,
            first_choice_score_op=first_choice_score_op,
            first_choice_score=first_choice_score,
            second_choice_advisor=second_choice_advisor,
            second_choice_team=second_choice_team,
            second_choice_score_op=second_choice_score_op,
            second_choice_score=second_choice_score,
            sort_by=None,
            sort_order=None,
            page=1,
            page_size=50000,
            visible_advisor_names=visible_advisor_names,
            is_center_leader=is_center_leader,
        )
        return [dict(item) for item in items]

    def create_camp_offer(self, payload: CampOfferUpsert, principal: Any | None = None) -> CampOfferRecord:
        with self._lock:
            plan_id = self._resolve_camp_offer_plan_id(payload.plan_id)
            candidate_no = str(payload.candidate_no or "").strip()
            self._validate_camp_offer_candidate_no_exists(candidate_no)
            duplicated = self._postgres_store.find_camp_offer_by_candidate_plan(candidate_no=candidate_no, plan_id=plan_id)
            if duplicated is not None:
                raise ValueError("该报名号在当前招生计划下已存在入营名单记录")

            operation_log = self._record_operation(
                "招生管理",
                "入营名单",
                candidate_no,
                "新增",
                f"新增入营名单 {candidate_no}",
                operator_username=self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})["username"],
            )
            inserted = self._postgres_store.create_camp_offer(
                {
                    "candidate_no": candidate_no,
                    "plan_id": plan_id,
                    "is_sent_mail": payload.is_sent_mail,
                    "is_agree": payload.is_agree,
                    "reason": payload.reason,
                    "student_offer_submitted_at": payload.student_offer_submitted_at,
                    # 2026-07-03: 黑客松夏令营字段 (新增路径, 与 update 保持一致)
                    "hackathon_score": payload.hackathon_score,
                    "hackathon_comments": payload.hackathon_comments,
                    "accepted": payload.accepted,
                    # 2026-07-06: 录取学校
                    "admission_offered_school": payload.admission_offered_school,
                    "is_in_camp_selection": payload.is_in_camp_selection,
                },
                operation_log,
            )
            return self.get_camp_offer_detail(int(inserted.get("id") or 0))

    def update_camp_offer(self, offer_id: int, payload: CampOfferUpsert, principal: Any | None = None) -> CampOfferRecord:
        with self._lock:
            existing = self._postgres_store.get_camp_offer_detail(int(offer_id))
            if existing is None:
                raise KeyError("Camp offer not found")

            plan_id = self._resolve_camp_offer_plan_id(payload.plan_id)
            candidate_no = str(payload.candidate_no or "").strip()
            self._validate_camp_offer_candidate_no_exists(candidate_no)
            duplicated = self._postgres_store.find_camp_offer_by_candidate_plan(candidate_no=candidate_no, plan_id=plan_id)
            if duplicated is not None and int(duplicated.get("id") or 0) != int(offer_id):
                raise ValueError("该报名号在当前招生计划下已存在入营名单记录")

            operation_log = self._record_operation(
                "招生管理",
                "入营名单",
                str(offer_id),
                "编辑",
                f"更新入营名单 {candidate_no}",
                operator_username=self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})["username"],
            )
            updated = self._postgres_store.update_camp_offer(
                int(offer_id),
                {
                    "candidate_no": candidate_no,
                    "plan_id": plan_id,
                    "is_sent_mail": payload.is_sent_mail,
                    "is_agree": payload.is_agree,
                    "reason": payload.reason,
                    "student_offer_submitted_at": payload.student_offer_submitted_at,
                    # 2026-07-03: 黑客松夏令营字段 (前端 CampOfferUpsert 已存在, 但 service 之前漏传,
                    # 导致编辑保存后 dtlms_plan_offer.hackathon_score / hackathon_comments / accepted
                    # 全部被写为 NULL, 出现"保存成功但值未更新" 的 bug)
                    "hackathon_score": payload.hackathon_score,
                    "hackathon_comments": payload.hackathon_comments,
                    "accepted": payload.accepted,
                    # 2026-07-06: 录取学校
                    "admission_offered_school": payload.admission_offered_school,
                    "is_in_camp_selection": payload.is_in_camp_selection,
                },
                operation_log,
            )
            if not updated:
                raise KeyError("Camp offer not found")
            return self.get_camp_offer_detail(int(offer_id))
    # ------------------------------------------------------------------

    # 2026-07-03: 黑客松入取状态 (dtlms_plan_offer.accepted) 变更入口
    # - 仅允许写入 4 个状态: NULL / "declined" / "accepted_pending_send" / "pending"
    # - 权限校验: 书院管理员 / 平台管理员放行；
    #             其他角色需 can_change_accepted=True (即该导师/中心负责人在该学生一/二志愿中分数 >= 80)
    # - 写操作: 仅更新 accepted 字段 + updated_at，不联动其他字段
    # - 状态可逆: 允许反复修改 (不锁状态机)
    # ------------------------------------------------------------------
    def _principal_can_change_camp_offer_accepted(
        self,
        offer_row: dict[str, Any],
        principal_summary: dict[str, Any],
        principal: Any | None = None,
    ) -> bool:
        """判断 principal 是否有权限修改指定入营名单的 accepted 字段。

        规则 (2026-07-03 二次确认后):
        1) 书院管理员 (AILABMGT) / 平台管理员 (platform_admin) -> 放行
        2) 否则:
           - 仅当 principal 是 dtlms_team_leaders 中任一中心的 lead_user_id 时,
             才能依赖 offer_row["can_change_accepted"] (SQL 层已计算好, 只对中心负责人命中 first/second_choice 分数规则才为 True)
           - 普通 advisor 即使 first/second_choice 命中且分数>=80 也不允许改
        3) 其他情况 -> False

        注意: SQL 层 (postgres_state_store_query_recruitment.list_camp_offers_page) 同样
        已用 is_center_leader 守卫, 客户端即便绕过前端直接调用 API 也会被服务端拒绝。
        """
        role_codes = {str(item).strip() for item in principal_summary.get("roles", []) if str(item).strip()}
        if "AILABMGT" in role_codes or "platform_admin" in role_codes:
            return True
        # 非白名单: 必须同时满足「是中心负责人」+ 「SQL 层算出的 can_change_accepted=True」
        is_center_leader = self._postgres_store.resolve_camp_offer_is_center_leader(principal if principal is not None else principal_summary)
        if not is_center_leader:
            return False
        return bool(offer_row.get("can_change_accepted") or False)

    def set_camp_offer_accepted_status(
        self,
        offer_id: int,
        accepted: str | None,
        principal: Any | None = None,
    ) -> CampOfferRecord:
        """业务侧统一入口: 变更入营名单 accepted 状态 (录取/不录取/待定/清空)。

        2026-07-03 需求: 录取/不录取/待定/清空 4 个动作使用同一个 service 方法，
        由 API 层用 action 字符串区分 (accept/decline/pending/clear)，
        这样可以共用 4 条规则的权限校验。

        参数:
            offer_id:  入营名单主键 id
            accepted:  目标状态，4 选 1: None | "declined" | "accepted_pending_send" | "pending"
            principal:  当前登录人 (包含 username / full_name / roles / permissions)

        返回:
            CampOfferRecord (包含更新后的状态)

        异常:
            KeyError - 入营名单不存在
            PermissionError - 当前账号无权限修改此行
            ValueError - accepted 状态非法 (应不会发生，sync 层会再次校验)
        """
        with self._lock:
            # 1) 查询并校验存在 (带可见性 + 中心负责人标记, 让返回的 can_change_accepted 准确)
            visible_advisor_names = self._postgres_store.resolve_camp_offer_visible_advisor_names(principal)
            is_center_leader_for_perm = self._postgres_store.resolve_camp_offer_is_center_leader(principal)
            existing = self._postgres_store.get_camp_offer_detail(
                int(offer_id),
                visible_advisor_names=visible_advisor_names,
                is_center_leader=is_center_leader_for_perm,
            )
            if existing is None:
                raise KeyError("Camp offer not found")

            # 2) 权限校验 (书院管理员/平台管理员放行；其他角色需 can_change_accepted=True)
            principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": []})
            if not self._principal_can_change_camp_offer_accepted(existing, principal_summary, principal=principal):
                raise PermissionError("当前账号无权修改此入营名单的入取状态")

            # 3) 仅更新 accepted 字段 (sync 层会校验状态白名单)
            operation_log = self._record_operation(
                "招生管理",
                "入营名单",
                str(offer_id),
                "修改入取状态",
                f"设置 accepted={accepted!r}",
                operator_username=principal_summary["username"],
            )
            updated = self._postgres_store.set_camp_offer_accepted(
                int(offer_id),
                accepted,
                operation_log,
            )
            if not updated:
                raise KeyError("Camp offer not found")

            # 4) 返回最新记录 (供前端立即刷新)
            return self.get_camp_offer_detail(int(offer_id))


    def delete_camp_offer(self, offer_id: int, principal: Any | None = None) -> None:
        with self._lock:
            existing = self._postgres_store.get_camp_offer_detail(int(offer_id))
            if existing is None:
                raise KeyError("Camp offer not found")
            candidate_no = str(existing.get("candidate_no") or "").strip()
            operation_log = self._record_operation(
                "招生管理",
                "入营名单",
                str(offer_id),
                "删除",
                f"删除入营名单 {candidate_no}",
                operator_username=self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})["username"],
            )
            deleted = self._postgres_store.delete_camp_offer(int(offer_id), operation_log)
            if not deleted:
                raise KeyError("Camp offer not found")

    def import_camp_offers(
        self,
        *,
        rows: list[dict[str, Any]],
        plan_id: int | None = None,
        principal: Any | None = None,
    ) -> CampOfferImportResult:
        with self._lock:
            default_plan_id = self._resolve_camp_offer_plan_id(plan_id)
            imported_ids: list[int] = []
            issues: list[CampOfferImportIssue] = []
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            for row_number, row in enumerate(rows, start=2):
                candidate_no = str(row.get("candidate_no") or "").strip()
                if not candidate_no:
                    issues.append(CampOfferImportIssue(row_number=row_number, candidate_no=None, reason="candidate_no 为空，已跳过"))
                    continue
                try:
                    row_plan_id = row.get("plan_id")
                    resolved_plan_id = int(str(row_plan_id).strip()) if row_plan_id not in (None, "") else default_plan_id
                except Exception:
                    issues.append(CampOfferImportIssue(row_number=row_number, candidate_no=candidate_no, reason="plan_id 非法，已跳过"))
                    continue
                try:
                    self._validate_camp_offer_candidate_no_exists(candidate_no)
                except ValueError as exc:
                    issues.append(CampOfferImportIssue(row_number=row_number, candidate_no=candidate_no, reason=str(exc)))
                    continue
                duplicated = self._postgres_store.find_camp_offer_by_candidate_plan(candidate_no=candidate_no, plan_id=resolved_plan_id)
                if duplicated is not None:
                    issues.append(CampOfferImportIssue(row_number=row_number, candidate_no=candidate_no, reason="该报名号在当前计划下已存在，已跳过"))
                    continue

                is_sent_mail_raw = str(row.get("is_sent_mail") or "").strip().lower()
                is_agree_raw = str(row.get("is_agree") or "").strip().lower()
                operation_log = self._record_operation(
                    "招生管理",
                    "入营名单",
                    candidate_no,
                    "导入",
                    f"导入入营名单 {candidate_no}",
                    operator_username=operator["username"],
                )
                inserted = self._postgres_store.create_camp_offer(
                    {
                        "candidate_no": candidate_no,
                        "plan_id": resolved_plan_id,
                        "is_sent_mail": is_sent_mail_raw in {"1", "true", "yes", "y", "是", "已发送"},
                        "is_agree": None if is_agree_raw == "" else is_agree_raw in {"1", "true", "yes", "y", "是", "同意"},
                        "reason": str(row.get("reason") or "").strip() or None,
                        "student_offer_submitted_at": str(row.get("student_offer_submitted_at") or "").strip() or None,
                    },
                    operation_log,
                )
                inserted_id = int(inserted.get("id") or 0)
                if inserted_id:
                    imported_ids.append(inserted_id)

            return CampOfferImportResult(
                imported_count=len(imported_ids),
                skipped_count=len(issues),
                plan_id=default_plan_id,
                imported_ids=imported_ids,
                issues=issues,
            )

    def get_recruitment_portal_application_detail(self, application_id: int) -> RecruitPortalApplicationDetail:
        application = self.get_recruitment_application_detail(application_id)
        return self._build_recruitment_portal_application_detail(application)

    def get_dashboard_undergraduate_school_rankings(self, limit: int = 20) -> list[DashboardUndergraduateSchoolRankingItem]:
        try:
            items = self._postgres_store.list_dashboard_undergraduate_school_rankings(limit=limit)
            return [DashboardUndergraduateSchoolRankingItem(**item) for item in items]
        except Exception as exc:
            logger.warning("Query dashboard undergraduate school rankings from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("本科院校排名当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_dashboard_undergraduate_school_group_distribution(self) -> DashboardUndergraduateSchoolGroupDistributionResponse:
        try:
            payload = self._postgres_store.list_dashboard_undergraduate_school_group_distribution()
            return DashboardUndergraduateSchoolGroupDistributionResponse(
                total_applications=int(payload.get("total_applications") or 0),
                groups=[
                    DashboardUndergraduateSchoolGroupDistribution(
                        group_name=str(group.get("group_name") or ""),
                        dict_type=str(group.get("dict_type") or ""),
                        total=int(group.get("total") or 0),
                        items=[DashboardUndergraduateSchoolGroupItem(**item) for item in group.get("items", [])],
                    )
                    for group in payload.get("groups", [])
                ],
            )
        except Exception as exc:
            logger.warning("Query dashboard undergraduate school group distribution from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("重点院校报名分布当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_dashboard_undergraduate_school_group_students(
        self,
        *,
        dict_type: str,
        school_name: str | None = None,
        bucket: str | None = None,
    ) -> DashboardUndergraduateSchoolStudentListResponse:
        try:
            items = self._postgres_store.list_dashboard_undergraduate_school_group_students(
                dict_type=dict_type,
                school_name=school_name,
                bucket=bucket,
            )
            normalized_bucket = str(bucket or "").strip().lower()
            normalized_school_name = str(school_name or "").strip()
            display_name = normalized_school_name or ("其他" if normalized_bucket == "other" else "重点院校")
            return DashboardUndergraduateSchoolStudentListResponse(
                school_name=display_name,
                total=len(items),
                items=[DashboardUndergraduateSchoolStudentItem(**item) for item in items],
            )
        except Exception as exc:
            logger.warning("Query dashboard undergraduate school group student list from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("重点院校报名学生清单当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_dashboard_undergraduate_school_students(self, school_name: str) -> DashboardUndergraduateSchoolStudentListResponse:
        try:
            items = self._postgres_store.list_dashboard_undergraduate_school_students(school_name)
            normalized_school_name = str(school_name or "").strip()
            return DashboardUndergraduateSchoolStudentListResponse(
                school_name=normalized_school_name,
                total=len(items),
                items=[DashboardUndergraduateSchoolStudentItem(**item) for item in items],
            )
        except Exception as exc:
            logger.warning("Query dashboard undergraduate school student list from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("本科院校报名学生清单当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_dashboard_recruitment_advisor_choice_distribution(self) -> DashboardRecruitmentAdvisorChoiceDistributionResponse:
        try:
            payload = self._postgres_store.list_dashboard_recruitment_advisor_choice_distribution()
            return DashboardRecruitmentAdvisorChoiceDistributionResponse(
                choices=[
                    DashboardRecruitmentAdvisorChoiceDistribution(
                        choice_round=str(choice.get("choice_round") or ""),
                        choice_name=str(choice.get("choice_name") or ""),
                        total=int(choice.get("total") or 0),
                        items=[
                            DashboardRecruitmentAdvisorChoiceItem(
                                advisor_name=str(item.get("advisor_name") or ""),
                                student_count=int(item.get("student_count") or 0),
                                percentage=float(item.get("percentage") or 0),
                            )
                            for item in choice.get("items", [])
                        ],
                    )
                    for choice in payload.get("choices", [])
                ],
            )
        except Exception as exc:
            logger.warning("Query dashboard advisor choice distribution from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("报名导师志愿分布当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_dashboard_recruitment_advisor_choice_students(
        self,
        *,
        choice_round: str,
        advisor_name: str | None = None,
        bucket: str | None = None,
    ) -> DashboardUndergraduateSchoolStudentListResponse:
        try:
            items = self._postgres_store.list_dashboard_recruitment_advisor_choice_students(
                choice_round=choice_round,
                advisor_name=advisor_name,
                bucket=bucket,
            )
            choice_name = "第一志愿导师" if choice_round == "first_choice" else "第二志愿导师"
            if str(bucket or "").strip().lower() == "other":
                display_name = f"{choice_name}其他导师"
            else:
                display_name = f"{choice_name} - {str(advisor_name or '').strip()}"
            return DashboardUndergraduateSchoolStudentListResponse(
                school_name=display_name,
                total=len(items),
                items=[DashboardUndergraduateSchoolStudentItem(**item) for item in items],
            )
        except Exception as exc:
            logger.warning("Query dashboard advisor choice student list from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("报名导师志愿学生清单当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def create_recruitment_application(self, payload: RecruitApplicationUpsert, principal: Any | None = None) -> RecruitApplicationRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("recruitment_application", payload.model_dump())
            item["id"] = self._next_id("recruitment_applications")
            self._list("recruitment_applications").insert(0, item)
            self._start_managed_workflow("recruitment_application", item, operator_username=operator["username"])
            workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("招生管理", "报名申请", str(item["id"]), "新增", f'新增报名申请 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._persist_recruitment_application_change(
                    item,
                    operation_log,
                    workflow_task=workflow_located[1] if workflow_located is not None else None,
                    update_application_counter=True,
                    update_workflow_counter=workflow_located is not None,
                )
            except Exception:
                self._save()
            return RecruitApplicationRecord(**item)

    def import_recruitment_applications(
        self,
        plan_id: int,
        rows: list[dict[str, Any]],
        principal: Any | None = None,
    ) -> RecruitApplicationImportResult:
        with self._lock:
            self._find_required("recruitment_plans", plan_id)
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            imported_business_keys: list[str] = []
            issues: list[RecruitApplicationImportIssue] = []
            for row_number, row in enumerate(rows, start=2):
                student_name = str(row.get("student_name") or "").strip()
                if not student_name:
                    issues.append(RecruitApplicationImportIssue(row_number=row_number, student_name=None, reason="姓名为空，已跳过"))
                    continue

                duplicated = next(
                    (
                        item
                        for item in self._list("recruitment_applications")
                        if int(item.get("plan_id") or 0) == int(plan_id)
                        and str(item.get("student_name") or "").strip() == student_name
                        and (
                            (row.get("phone_number") and item.get("phone_number") == row.get("phone_number"))
                            or (row.get("email") and item.get("email") == row.get("email"))
                        )
                    ),
                    None,
                )
                if duplicated:
                    issues.append(
                        RecruitApplicationImportIssue(
                            row_number=row_number,
                            student_name=student_name,
                            reason=f'检测到重复报名申请，已跳过：{duplicated.get("business_key")}',
                        )
                    )
                    continue

                payload_data = {
                    **row,
                    "plan_id": int(plan_id),
                    "business_key": None,
                    "candidate_no": None,
                    "graduation_school": row.get("graduation_school") or row.get("undergraduate_school") or "待补充",
                    "highest_degree": row.get("highest_degree") or "硕士",
                    "intended_field": row.get("intended_field") or row.get("first_choice") or row.get("second_choice") or "待分配方向",
                    "material_status": row.get("material_status") or "待审核",
                    "application_status": row.get("application_status") or "报名已提交",
                    "reviewer_name": row.get("reviewer_name") or None,
                    "final_score": None,
                }
                item = self._workflow_initial_item("recruitment_application", RecruitApplicationUpsert(**payload_data).model_dump())
                item["id"] = self._next_id("recruitment_applications")
                self._list("recruitment_applications").insert(0, item)
                self._start_managed_workflow("recruitment_application", item, operator_username=operator["username"])
                workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
                operation_log = self._record_operation("招生管理", "报名申请", str(item["id"]), "导入", f'导入报名申请 {item["student_name"]}', operator_username=operator["username"])
                try:
                    self._persist_recruitment_application_change(
                        item,
                        operation_log,
                        workflow_task=workflow_located[1] if workflow_located is not None else None,
                        update_application_counter=True,
                        update_workflow_counter=workflow_located is not None,
                    )
                except Exception:
                    self._save()
                imported_business_keys.append(str(item["business_key"]))

            return RecruitApplicationImportResult(
                imported_count=len(imported_business_keys),
                skipped_count=len(issues),
                plan_id=int(plan_id),
                imported_business_keys=imported_business_keys,
                issues=issues,
            )

    def export_recruitment_applications(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        portal_student_only: bool = False,
        advisor_names: list[str] | None = None,
        principal: Principal | Any | None = None,
    ) -> bytes:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": [], "permissions": []})
        role_codes = {str(item) for item in principal_summary["roles"] if str(item).strip()}
        advisor_name = None
        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if "advisor" in role_codes and not role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            advisor_name = str(principal_summary.get("full_name") or "").strip() or None
            if normalized_advisor_names and advisor_name not in normalized_advisor_names:
                return build_recruitment_template([])
            normalized_advisor_names = [advisor_name] if advisor_name else []
        items, _ = self._postgres_store.list_recruitment_applications_page(
            keyword=keyword,
            plan_id=plan_id,
            status=status,
            portal_student_only=portal_student_only,
            advisor_name=advisor_name,
            advisor_names=normalized_advisor_names or None,
            page=1,
            page_size=10000,
        )
        return build_recruitment_template(items)

    def export_advisor_screening_applications(
        self,
        *,
        keyword: str | None = None,
        advisor_name: str | None = None,
        advisor_user_id: int | None = None,
        screening_round: str | None = None,
        status: str | None = None,
    ) -> bytes:
        rows, _ = self._postgres_store.list_recruitment_applications_page(
            keyword=keyword,
            status=status,
            advisor_name=advisor_name,
            advisor_user_id=advisor_user_id,
            page=1,
            page_size=10000,
        )
        normalized_round = str(screening_round or "").strip()
        export_rows: list[dict[str, Any]] = []
        for row in rows:
            row_round = str(row.get("advisor_screening_round") or "").strip()
            if normalized_round and row_round != normalized_round:
                continue
            export_rows.append(
                {
                    "candidate_no": row.get("candidate_no"),
                    "business_key": row.get("business_key"),
                    "student_name": row.get("student_name"),
                    "choice_name": "第二志愿" if row_round == "second_choice" else "第一志愿",
                    "advisor_screening_round": row_round,
                    "first_choice": row.get("first_choice"),
                    "second_choice": row.get("second_choice"),
                    "first_choice_screening_score": row.get("first_choice_screening_score"),
                    "second_choice_screening_score": row.get("second_choice_screening_score"),
                    "application_status": row.get("application_status"),
                    "advisor_screening_status": row.get("advisor_screening_status"),
                    "applied_at": row.get("applied_at"),
                    "first_choice_screening_submitted_at": row.get("first_choice_screening_submitted_at"),
                    "second_choice_screening_submitted_at": row.get("second_choice_screening_submitted_at"),
                }
            )
        return build_advisor_screening_template(export_rows)

    def export_recruitment_application_blank_template(self) -> bytes:
        return build_recruitment_template([])

    def update_recruitment_application(self, application_id: int, payload: RecruitApplicationUpsert) -> RecruitApplicationRecord:
        with self._lock:
            index, item = self._find_required("recruitment_applications", application_id)
            incoming = {**item, **payload.model_dump(), "id": application_id}
            self._ensure_managed_status_fields_unchanged("recruitment_applications", item, incoming)
            updated = incoming
            workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            workflow_task = None
            if workflow_located is not None:
                workflow_task, task_changed = self._sync_managed_workflow_task("recruitment_application", updated, existing_task=workflow_located[1])
                if task_changed:
                    self._list("workflow_tasks")[workflow_located[0]] = workflow_task
            self._list("recruitment_applications")[index] = updated
            operation_log = self._record_operation("招生管理", "报名申请", str(application_id), "编辑", f'更新报名申请 {updated["student_name"]}')
            try:
                self._persist_recruitment_application_change(updated, operation_log, workflow_task=workflow_task)
            except Exception:
                self._save()
            return RecruitApplicationRecord(**updated)

    def update_recruitment_application_advisor_choices(
        self,
        application_id: int,
        *,
        first_choice: str | None,
        first_choice_id: int | None,
        second_choice: str | None,
        second_choice_id: int | None,
        principal: Principal | None = None,
    ) -> RecruitApplicationRecord:
        del principal
        with self._lock:
            index, item = self._find_required("recruitment_applications", application_id)
            updated = dict(item)
            updated["first_choice"] = str(first_choice).strip() if first_choice is not None else None
            updated["first_choice_id"] = int(first_choice_id) if first_choice_id is not None else None
            updated["second_choice"] = str(second_choice).strip() if second_choice is not None else None
            updated["second_choice_id"] = int(second_choice_id) if second_choice_id is not None else None
            updated["intended_advisor_name"] = updated["first_choice"]
            updated["intended_advisor_user_id"] = updated["first_choice_id"]
            workflow_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            workflow_task = None
            if workflow_located is not None:
                if str(updated.get("application_status") or "").strip() in {"待导师初筛-第一志愿", "待导师初筛-第二志愿"}:
                    updated["advisor_screening_status"] = "pending"
                    updated["advisor_screening_round"] = "first_choice" if str(updated.get("application_status") or "").strip() != "待导师初筛-第二志愿" else "second_choice"
                workflow_task, task_changed = self._sync_managed_workflow_task("recruitment_application", updated, existing_task=workflow_located[1])
                if task_changed:
                    self._list("workflow_tasks")[workflow_located[0]] = workflow_task
            self._list("recruitment_applications")[index] = updated
            operation_log = self._record_operation("招生管理", "报名申请", str(application_id), "编辑导师", f'更新报名申请导师志愿 {updated["student_name"]}')
            try:
                sync_advisor_choices = getattr(self._postgres_store, "sync_recruitment_application_advisor_choices", None)
                if not callable(sync_advisor_choices):
                    raise DatabaseUnavailableError("导师志愿更新当前仅允许写入数据库，缺少正式持久化能力")
                sync_advisor_choices(
                    int(application_id),
                    updated,
                    workflow_task,
                    operation_log,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                )
            except Exception:
                logger.exception("Persist recruitment advisor choice change failed")
                raise
            return RecruitApplicationRecord(**updated)

    def submit_advisor_screening_batch(
        self,
        payload: AdvisorScreeningBatchSubmitRequest,
        *,
        principal: Principal,
    ) -> AdvisorScreeningBatchSubmitResponse:
        principal_summary = self._principal_summary(principal)
        submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_records: list[RecruitApplicationRecord] = []
        updated_applications: list[dict[str, Any]] = []
        updated_tasks: list[dict[str, Any]] = []
        operation_logs: list[dict[str, Any]] = []
        screening_rounds: set[str] = set()

        with self._lock:
            for item in payload.items:
                entity_index, entity = self._find_required("recruitment_applications", int(item.application_id))
                business_key = str(entity.get("business_key") or "").strip()
                workflow_task: dict[str, Any] | None
                if settings.recruitment_uses_db_judgment:
                    workflow_snapshot = getattr(self._postgres_store, "get_workflow_task_snapshot_by_business_key", None)
                    workflow_task = cast(dict[str, Any] | None, workflow_snapshot(business_key)) if callable(workflow_snapshot) else None
                else:
                    workflow_task = None

                workflow_located = self._workflow_task_index_by_business_key(business_key)
                if workflow_task is None:
                    workflow_task = workflow_located[1] if workflow_located is not None else None

                if workflow_task is None or workflow_located is None:
                    raise ValueError("未找到对应的流程任务")
                task_index, task = workflow_located
                if str(workflow_task.get("node_key") or "") != "advisor_screening":
                    raise ValueError("当前申请不在导师初筛环节")

                screening_round = self._resolve_advisor_screening_round(entity)
                screening_rounds.add(screening_round)
                if len(screening_rounds) > 1:
                    raise ValueError("一次只允许提交同一轮次的导师初筛记录")
                if self._advisor_screening_submission_locked(entity, screening_round):
                    raise ValueError("当前申请该轮导师初筛已提交，不能重复提交")
                if not self._principal_matches_screening_advisor(entity, screening_round, principal_summary):
                    raise PermissionError("当前账号不是该申请当前轮次的责任导师")

                advisor_score = float(item.advisor_score)
                is_passed = advisor_score >= 80
                updated_entity = dict(entity)
                updated_entity["advisor_screening_status"] = "submitted"
                updated_entity["advisor_screening_round"] = screening_round

                next_node: str | None
                task_status = "处理中"
                action_label = "导师初筛自动通过" if is_passed else "导师初筛自动不通过"
                comment = f"{action_label}，分数 {advisor_score:.2f}，系统按 80 分阈值自动判定"
                if screening_round == "first_choice":
                    updated_entity["first_choice_screening_score"] = advisor_score
                    updated_entity["first_choice_screening_submitted_at"] = submitted_at
                    if is_passed:
                        updated_entity["application_status"] = "待初筛确认"
                        updated_entity["initial_screening_status"] = "pending"
                        next_node = "initial_screening_confirmation"
                    else:
                        has_second_choice = bool(str(entity.get("second_choice") or "").strip())
                        if has_second_choice:
                            updated_entity["application_status"] = "待导师初筛-第二志愿"
                            updated_entity["advisor_screening_status"] = "pending"
                            updated_entity["advisor_screening_round"] = "second_choice"
                            next_node = "advisor_screening"
                        else:
                            updated_entity["application_status"] = "报名终止"
                            updated_entity["initial_screening_result"] = "rejected"
                            next_node = None
                            task_status = "已驳回"
                else:
                    updated_entity["second_choice_screening_score"] = advisor_score
                    updated_entity["second_choice_screening_submitted_at"] = submitted_at
                    if is_passed:
                        updated_entity["application_status"] = "待初筛确认"
                        updated_entity["initial_screening_status"] = "pending"
                        next_node = "initial_screening_confirmation"
                    else:
                        updated_entity["application_status"] = "报名终止"
                        updated_entity["initial_screening_result"] = "rejected"
                        next_node = None
                        task_status = "已驳回"

                updated_task = self._build_workflow_transition_record(
                    task,
                    updated_entity,
                    next_node=next_node,
                    task_status=task_status,
                    comment=comment,
                    action="submit_advisor_screening",
                    action_label=action_label,
                    principal_summary=principal_summary,
                )

                operation_log = self._record_operation(
                    "招生管理",
                    "报名申请",
                    str(entity.get("business_key") or entity.get("id") or ""),
                    action_label,
                    f'{principal_summary["full_name"]} 提交导师初筛',
                    operator_username=principal_summary["username"],
                    target_name=str(entity.get("student_name") or ""),
                )

                self._list("recruitment_applications")[entity_index] = updated_entity
                self._list("workflow_tasks")[task_index] = updated_task
                updated_applications.append(
                    {
                        **updated_entity,
                        "screening_round": screening_round,
                        "advisor_score": advisor_score,
                        "is_passed": is_passed,
                        "submitted_at": submitted_at,
                    }
                )
                updated_tasks.append(updated_task)
                operation_logs.append(operation_log)
                updated_records.append(RecruitApplicationRecord(**updated_entity))

            sync_advisor_screening = getattr(self._postgres_store, "sync_advisor_screening_batch", None)
            if not callable(sync_advisor_screening):
                raise DatabaseUnavailableError("导师初筛当前仅允许写入数据库，缺少正式持久化能力")

            screening_round = next(iter(screening_rounds))
            signature_base64 = str(payload.signature_base64 or "").strip()
            advisor_username = str(principal_summary["username"])
            advisor_name = str(principal_summary["full_name"])
            batch_id = int(
                cast(
                    int,
                    sync_advisor_screening(
                    {
                        "advisor_user_id": None,
                        "advisor_username": advisor_username,
                        "advisor_name": advisor_name,
                        "advisor_role_code": "advisor",
                        "screening_round": screening_round,
                        "signature_base64": signature_base64,
                        "submitted_at": submitted_at,
                    },
                    updated_applications,
                    updated_tasks,
                    operation_logs,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                ),
                )
            )

            for application in updated_applications:
                if application.get("screening_round") == "first_choice":
                    application["first_choice_screening_batch_id"] = batch_id
                else:
                    application["second_choice_screening_batch_id"] = batch_id

            if self._email_service.enabled():
                for application in updated_applications:
                    # 终止类结果不再发送邮件通知；仅保留资料审核驳回重填等非终止邮件。
                    if str(application.get("application_status") or "") == "报名终止":
                        continue

        return AdvisorScreeningBatchSubmitResponse(
            batch_id=batch_id,
            screening_round=screening_round,
            submitted_count=len(updated_records),
            applications=updated_records,
        )

    def confirm_initial_screening(
        self,
        application_id: int,
        payload: InitialScreeningConfirmationRequest,
        *,
        principal: Principal,
    ) -> RecruitApplicationRecord:
        principal_summary = self._principal_summary(principal)
        confirmed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._lock:
            entity_index, entity = self._find_required("recruitment_applications", int(application_id))
            workflow_located = self._workflow_task_index_by_business_key(str(entity.get("business_key") or ""))
            if workflow_located is None:
                raise ValueError("未找到对应的流程任务")
            task_index, task = workflow_located
            if str(task.get("node_key") or "") != "initial_screening_confirmation":
                raise ValueError("当前申请不在初筛确认环节")

            updated_entity = dict(entity)
            updated_entity["initial_screening_status"] = "confirmed"
            updated_entity["initial_screening_result"] = payload.result
            updated_entity["initial_screening_confirmed_at"] = confirmed_at
            updated_entity["initial_screening_confirmer_username"] = principal_summary["username"]
            updated_entity["initial_screening_confirmer_name"] = principal_summary["full_name"]
            updated_entity["initial_screening_notification_status"] = "pending"

            if payload.result == "passed":
                updated_entity["application_status"] = "入营面试"
                updated_entity["next_stage_name"] = "入营面试"
                updated_entity["advisor_screening_status"] = "passed"
                next_node = "camp_interview"
                task_status = "处理中"
                action_label = "初筛确认通过"
            else:
                updated_entity["application_status"] = "报名终止"
                updated_entity["advisor_screening_status"] = "rejected"
                next_node = None
                task_status = "已驳回"
                action_label = "初筛确认不通过"

            updated_task = self._build_workflow_transition_record(
                task,
                updated_entity,
                next_node=next_node,
                task_status=task_status,
                comment=payload.comment,
                action="confirm_initial_screening",
                action_label=action_label,
                principal_summary=principal_summary,
            )
            operation_log = self._record_operation(
                "招生管理",
                "报名申请",
                str(entity.get("business_key") or entity.get("id") or ""),
                action_label,
                f'{principal_summary["full_name"]} 执行初筛确认',
                operator_username=principal_summary["username"],
                target_name=str(entity.get("student_name") or ""),
            )
            notification_payloads = [
                {
                    "application_id": int(entity["id"]),
                    "business_key": str(entity.get("business_key") or ""),
                    "notification_channel": "email",
                    "notification_event": "initial_screening_confirmation",
                    "notification_status": "pending",
                    "recipient_address": updated_entity.get("email"),
                    "recipient_user_id": updated_entity.get("portal_student_id"),
                    "recipient_username": None,
                    "payload_json": {
                        "application_status": updated_entity.get("application_status"),
                        "result": payload.result,
                    },
                    "sent_at": None,
                },
                {
                    "application_id": int(entity["id"]),
                    "business_key": str(entity.get("business_key") or ""),
                    "notification_channel": "site_message",
                    "notification_event": "initial_screening_confirmation",
                    "notification_status": "pending",
                    "recipient_address": None,
                    "recipient_user_id": updated_entity.get("portal_student_id"),
                    "recipient_username": None,
                    "payload_json": {
                        "application_status": updated_entity.get("application_status"),
                        "result": payload.result,
                    },
                    "sent_at": None,
                },
            ]
            sync_confirmation = getattr(self._postgres_store, "sync_initial_screening_confirmation", None)
            if not callable(sync_confirmation):
                raise DatabaseUnavailableError("初筛确认当前仅允许写入数据库，缺少正式持久化能力")
            sync_confirmation(
                {
                    "application_id": int(entity["id"]),
                    "business_key": str(entity.get("business_key") or ""),
                    "candidate_no": str(entity.get("candidate_no") or entity.get("business_key") or ""),
                    "confirmer_user_id": None,
                    "confirmer_username": principal_summary["username"],
                    "confirmer_name": principal_summary["full_name"],
                    "confirmer_role_code": "AILABMGT",
                    "confirmation_result": payload.result,
                    "confirmation_comment": payload.comment,
                    "confirmed_at": confirmed_at,
                },
                updated_entity,
                updated_task,
                notification_payloads,
                operation_log,
                counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
            )

            self._list("recruitment_applications")[entity_index] = updated_entity
            self._list("workflow_tasks")[task_index] = updated_task

            if self._email_service.workflow_notifications_enabled():
                recruitment_notification = self._build_recruitment_email_notification(updated_entity, review_comment=payload.comment)
                if recruitment_notification is not None:
                    self._email_service.send_recruitment_status_update(**recruitment_notification)

            return RecruitApplicationRecord(**updated_entity)

    def rescore_advisor_screening_submitted_application(self, application_id: int, *, principal: Any | None = None) -> RecruitApplicationRecord:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": []})

        with self._lock:
            entity_index, entity = self._find_required("recruitment_applications", int(application_id))
            workflow_located = self._workflow_task_index_by_business_key(str(entity.get("business_key") or ""))
            if workflow_located is None:
                raise ValueError("未找到对应的流程任务")
            task_index, task = workflow_located
            current_stage = self._infer_registered_portal_current_stage(entity, task)
            current_node_key = str(task.get("node_key") or "").strip()
            application_status = str(entity.get("application_status") or "").strip()

            if current_stage == "camp_interview" or current_node_key == "camp_interview" or application_status == "入营面试":
                raise ValueError("因为该学生已经到了面试阶段所以无法重新评分")
            is_confirmation_stage = current_stage == "initial_screening_confirmation" or current_node_key == "initial_screening_confirmation" or application_status == "待初筛确认"
            is_terminated_stage = current_stage == "terminated" or application_status == "报名终止"
            is_second_screening_stage = current_stage == "initial_screening_second" or current_node_key == "initial_screening_second" or application_status == "待导师初筛-第二志愿"
            if not is_confirmation_stage and not is_terminated_stage and not is_second_screening_stage:
                raise ValueError("当前申请不在初筛确认或报名终止环节，无法重新评分")

            screening_round = self._resolve_rescore_screening_round(entity, principal_summary)
            block_message = self._build_rescore_block_message(screening_round, entity)
            if block_message:
                raise ValueError(block_message)

            if screening_round not in {"first_choice", "second_choice"}:
                screening_round = "second_choice" if entity.get("second_choice_screening_submitted_at") else "first_choice"

            updated_entity = dict(entity)
            if screening_round == "second_choice":
                updated_entity["application_status"] = "待导师初筛-第二志愿"
                updated_entity["advisor_screening_round"] = "second_choice"
                updated_entity["second_choice_screening_submitted_at"] = None
                updated_entity["second_choice_screening_score"] = None
                updated_entity["second_choice_screening_batch_id"] = None
            else:
                updated_entity["application_status"] = "待导师初筛-第一志愿"
                updated_entity["advisor_screening_round"] = "first_choice"
                updated_entity["first_choice_screening_submitted_at"] = None
                updated_entity["first_choice_screening_score"] = None
                updated_entity["first_choice_screening_batch_id"] = None

            updated_entity["advisor_screening_status"] = "pending"
            updated_entity["advisor_screening_submitted_at"] = None
            updated_entity["initial_screening_status"] = None
            updated_entity["initial_screening_result"] = None
            updated_entity["initial_screening_confirmed_at"] = None
            updated_entity["initial_screening_confirmer_username"] = None
            updated_entity["initial_screening_confirmer_name"] = None
            updated_entity["initial_screening_notification_status"] = None
            updated_entity["initial_screening_notification_sent_at"] = None
            updated_entity["next_stage_name"] = None
            updated_entity["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            updated_task = dict(task)
            updated_task["node_key"] = "advisor_screening"
            updated_task["current_node"] = "导师初筛"
            updated_task["current_handler"] = str(updated_entity.get("first_choice") or updated_entity.get("second_choice") or updated_entity.get("intended_advisor_name") or "导师")
            updated_task["status"] = "处理中"
            updated_task["latest_comment"] = "重新评分回退至导师初筛环节"
            updated_task.setdefault("history", []).append(
                {
                    "operated_at": updated_entity["updated_at"],
                    "operator_username": principal_summary["username"],
                    "operator_full_name": principal_summary["full_name"],
                    "action": "rescore_advisor_screening_submitted",
                    "action_label": "重新评分",
                    "from_node": str(task.get("current_node") or "初筛确认"),
                    "to_node": "导师初筛",
                    "result_status": "处理中",
                    "comment": "重新评分回退至导师初筛环节",
                }
            )
            self._ensure_workflow_engine_metadata(updated_task)

            operation_log = self._record_operation(
                "招生管理",
                "报名申请",
                str(application_id),
                "重新评分",
                f'将 {updated_entity.get("student_name") or ""} 的已提交记录回退至导师初筛环节',
                operator_username=principal_summary["username"],
            )

            try:
                self._postgres_store.rollback_recruitment_application_stage(
                    updated_entity,
                    updated_task,
                    clear_background_assessments=False,
                    clear_initial_screening_confirmation=True,
                    operation_log=operation_log,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                )
            except Exception as exc:
                logger.exception("Rescore submitted advisor-screening application persistence failed")
                raise RuntimeError("重新评分回退持久化失败，请稍后重试或联系管理员") from exc

            self._list("recruitment_applications")[entity_index] = updated_entity
            self._list("workflow_tasks")[task_index] = updated_task

            return RecruitApplicationRecord(**updated_entity)

    def delete_recruitment_application(self, application_id: int) -> None:
        with self._lock:
            list_items = self._list("recruitment_applications")
            index = next((item_index for item_index, item in enumerate(list_items) if int(item.get("id") or 0) == int(application_id)), None)
            item = list_items.pop(index) if index is not None else None
            try:
                deleted_record = self._postgres_store.delete_recruitment_application(int(application_id))
                if deleted_record is None and item is None:
                    raise KeyError(application_id)
                deleted_name = str((item or deleted_record or {}).get("student_name") or application_id)
                operation_log = self._record_operation("招生管理", "报名申请", str(application_id), "删除", f"删除报名申请 {deleted_name}")
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
                if item is None and deleted_record is not None:
                    self.state["recruitment_applications"] = [
                        existing for existing in list_items if int(existing.get("id") or 0) != int(application_id)
                    ]
            except KeyError:
                raise
            except Exception:
                self._save()

    def get_recruitment_stats(self) -> RecruitStats:
        plans = self._list("recruitment_plans")
        applications = self._list("recruitment_applications")
        return RecruitStats(
            plan_count=len(plans),
            open_plan_count=len(plans),
            application_total=len(applications),
            pending_review_total=len([item for item in applications if item["application_status"] in {"报名已提交", "资格审核通过", "材料评分中", "面试待安排"}]),
            pre_admit_total=len([item for item in applications if item["application_status"] in {"预录取", "同意录取"}]),
        )


    # 2026-07-09: 书院管理员在 /recruitment/camp-offers 选中学生 → 发送"录取通知书"邮件.
    # 业务规则:
    #   1) 每个 candidate 必须存在 dtlms_plan_offer 行 (同 plan_id);
    #   2) 当前 accepted 必须在 [accepted_pending_send, accepted_confirmed, accepted_rejected] 中 (允许重发, 不允许 declined/pending 状态发);
    #   3) 写库: accepted = 'accepted_sent' + accepted_notification_sent_at = now() + 清空 student_submitted_offer_at;
    #   4) 发邮件: 实际收件人统一写死 lk139@126.com (测试期); 文案 = portal 卡片同源.
    # 返回: dict { sent: int, failed: list[{candidate_no, reason}], skipped: list[{candidate_no, reason}] }
    def send_offer_notifications(
        self,
        *,
        candidate_nos: list[str],
        principal: Any | None = None,
    ) -> dict[str, Any]:
        from datetime import datetime

        from app.services.email_service import NotificationEmailService

        normalized = [str(c or "").strip() for c in (candidate_nos or []) if str(c or "").strip()]
        if not normalized:
            return {"sent": 0, "failed": [], "skipped": []}

        # 1) 查这些 candidate 当前 accepted 状态
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT candidate_no, plan_id, accepted, accepted_notification_sent_at,
                           student_submitted_offer_at
                    FROM dtlms_plan_offer
                    WHERE candidate_no = ANY(%s)
                    """,
                    (normalized,),
                )
                rows = cur.fetchall()
        row_map = {str(r.get("candidate_no") or "").strip(): r for r in rows}

        valid_statuses = {"accepted_pending_send", "accepted_confirmed", "accepted_rejected"}
        sent = 0
        failed: list[dict[str, str]] = []
        skipped: list[dict[str, str]] = []
        now_iso = datetime.now().strftime("%Y 年 %-m 月 %-d 日") if hasattr(datetime, "now") else ""

        email_service = NotificationEmailService()

        for cno in normalized:
            row = row_map.get(cno)
            if not row:
                skipped.append({"candidate_no": cno, "reason": "未找到该学生的入营记录"})
                continue
            current = row.get("accepted")
            if current not in valid_statuses:
                skipped.append({"candidate_no": cno, "reason": f"当前状态 {current} 不允许发送录取通知 (应处于 录取未发送/录取已确认/录取已拒绝)"})
                continue

            plan_id = int(row.get("plan_id") or 0)
            if plan_id <= 0:
                failed.append({"candidate_no": cno, "reason": "plan_id 缺失"})
                continue

            # 2) 写库: 状态置 accepted_sent + accepted_notification_sent_at = now + 清空 student_submitted_offer_at
            try:
                with self._connect(settings.postgres_db) as conn:
                    conn.row_factory = dict_row
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            UPDATE dtlms_plan_offer
                            SET accepted = 'accepted_sent',
                                accepted_notification_sent_at = now(),
                                student_submitted_offer_at = NULL,
                                updated_at = now()
                            WHERE candidate_no = %s AND plan_id = %s
                              AND accepted = %s
                            RETURNING candidate_no, admission_offered_school, accepted_notification_sent_at
                            """,
                            (cno, plan_id, current),
                        )
                        upd = cur.fetchone()
            except Exception as exc:
                failed.append({"candidate_no": cno, "reason": f"DB update failed: {exc}"})
                continue
            if not upd:
                failed.append({"candidate_no": cno, "reason": "状态已变更, 操作被拒绝"})
                continue

            # 3) 发邮件
            try:
                school = (upd.get("admission_offered_school") or "").strip() or "上海人工智能实验室"
                sent_at = upd.get("accepted_notification_sent_at")
                if sent_at is None:
                    sent_at_dt = datetime.now()
                elif hasattr(sent_at, "strftime"):
                    sent_at_dt = sent_at
                else:
                    from datetime import datetime as _dt
                    sent_at_dt = _dt.now()
                ymd = sent_at_dt.strftime("%Y 年 %-m 月 %-d 日") if hasattr(sent_at_dt, "strftime") else str(sent_at_dt)
                email_service.send_admission_offer_letter(
                    student_name=cno,  # 暂用报名号作为称呼 (后续可改为从 portal_student 取 full_name)
                    student_email="",  # 写空, 由 email_service 内部替换为 lk139@126.com
                    admission_offered_school=school,
                    accepted_notification_sent_at_ymd=ymd,
                    offer_timeout_hours=self._resolve_offer_timeout_hours() if hasattr(self, "_resolve_offer_timeout_hours") else 24,
                    portal_offer_url="/portal/home/offer",
                    business_key=cno,
                )
                sent += 1
            except Exception as exc:
                failed.append({"candidate_no": cno, "reason": f"send mail failed: {exc}"})
                continue

        return {"sent": sent, "failed": failed, "skipped": skipped}

    def _resolve_offer_timeout_hours(self) -> int:
        """2026-07-09: 从字典 student_signed_offer_timeout_hours 读超时阈值; fallback 24."""
        try:
            items = self._postgres_store.list_dict_data(dict_type="student_signed_offer_timeout_hours", status="启用") or []
        except Exception:
            items = []
        for it in items:
            v = it.get("value") if isinstance(it, dict) else None
            if v is None:
                continue
            try:
                n = int(str(v).strip())
                if n > 0:
                    return n
            except (TypeError, ValueError):
                continue
        return 24
