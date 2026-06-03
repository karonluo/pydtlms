from __future__ import annotations

from app.schemas.portal import PortalApplicationDeclarationData, PortalPersonalStatementData
from app.schemas.recruitment import RecruitApplicationRecord, RecruitPortalApplicationDetail

from .management_service_shared import *


class RuntimeManagementStoreRecruitmentMixin:
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
            preferences=list(application.preferences or []),
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
        normalized_advisor_names = [str(item).strip() for item in (advisor_names or []) if str(item).strip()]
        if "advisor" in role_codes and not role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            advisor_name = str(principal_summary.get("full_name") or "").strip() or None
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
        records = self.get_recruitment_applications(
            keyword=keyword,
            plan_id=plan_id,
            status=status,
            portal_student_only=portal_student_only,
            advisor_names=advisor_names,
            principal=principal,
            page=1,
            page_size=10000,
        ).items
        return build_recruitment_template([record.model_dump() for record in records])

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
                workflow_located = self._workflow_task_index_by_business_key(str(entity.get("business_key") or ""))
                if workflow_located is None:
                    raise ValueError("未找到对应的流程任务")
                task_index, task = workflow_located
                if str(task.get("node_key") or "") != "advisor_screening":
                    raise ValueError("当前申请不在导师初筛环节")

                screening_round = self._resolve_advisor_screening_round(entity)
                screening_rounds.add(screening_round)
                if len(screening_rounds) > 1:
                    raise ValueError("一次只允许提交同一轮次的导师初筛记录")
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
            batch_id = int(
                sync_advisor_screening(
                    {
                        "advisor_user_id": None,
                        "advisor_username": principal_summary["username"],
                        "advisor_name": principal_summary["full_name"],
                        "advisor_role_code": "advisor",
                        "screening_round": screening_round,
                        "signature_base64": payload.signature_base64,
                        "submitted_at": submitted_at,
                    },
                    updated_applications,
                    updated_tasks,
                    operation_logs,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                )
            )

            for application in updated_applications:
                if application.get("screening_round") == "first_choice":
                    application["first_choice_screening_batch_id"] = batch_id
                else:
                    application["second_choice_screening_batch_id"] = batch_id

            if self._email_service.enabled():
                for application in updated_applications:
                    if str(application.get("application_status") or "") == "报名终止":
                        payload_data = self._build_recruitment_email_notification(application)
                        if payload_data is not None:
                            self._email_service.send_recruitment_status_update(**payload_data)

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

            if self._email_service.enabled():
                recruitment_notification = self._build_recruitment_email_notification(updated_entity, review_comment=payload.comment)
                if recruitment_notification is not None:
                    self._email_service.send_recruitment_status_update(**recruitment_notification)

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
