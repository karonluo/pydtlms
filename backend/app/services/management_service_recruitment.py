from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStoreRecruitmentMixin:
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
            logger.warning("Query recruitment plans from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = [self._build_recruit_plan_record(item) for item in self._list("recruitment_plans")]
        if keyword:
            items = [item for item in items if self._matches_keyword(item.plan_name, item.academic_term, item.plan_description, keyword=keyword)]
        if semester:
            items = [item for item in items if item.semester == semester]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return RecruitPlanListResponse(items=paged_items, total=total, page=page, page_size=page_size)

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
        page: int = 1,
        page_size: int = 10,
    ) -> RecruitApplicationListResponse:
        try:
            items, total = self._postgres_store.list_recruitment_applications_page(
                keyword=keyword,
                plan_id=plan_id,
                status=status,
                page=page,
                page_size=page_size,
            )
            records = [RecruitApplicationRecord(**item) for item in items]
            return RecruitApplicationListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query recruitment applications from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("recruitment_applications"))
        if plan_id is not None:
            items = [item for item in items if item["plan_id"] == plan_id]
        if status:
            items = [item for item in items if item["application_status"] == status]
        if keyword:
            term = keyword.lower()
            items = [
                item
                for item in items
                if term in str(item.get("business_key") or "").lower()
                or term in str(item.get("candidate_no") or "").lower()
                or term in item["student_name"].lower()
                or term in str(item.get("graduation_school") or "").lower()
                or term in str(item.get("graduate_school") or "").lower()
                or term in str(item.get("intended_field") or "").lower()
                or term in str(item.get("first_choice") or "").lower()
                or term in str(item.get("second_choice") or "").lower()
                or term in str(item.get("intended_advisor_name") or "").lower()
                or term in str(item.get("phone_number") or "").lower()
                or term in str(item.get("email") or "").lower()
            ]
        records = [RecruitApplicationRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RecruitApplicationListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_recruitment_application_detail(self, application_id: int) -> RecruitApplicationRecord:
        try:
            item = self._postgres_store.get_recruitment_application_detail(application_id)
            if item is not None:
                return RecruitApplicationRecord(**item)
        except Exception as exc:
            logger.warning("Query recruitment application detail from PostgreSQL failed, fallback to in-memory data: %s", exc)

        _, item = self._find_required("recruitment_applications", application_id)
        return RecruitApplicationRecord(**item)

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
    ) -> bytes:
        records = self.get_recruitment_applications(keyword=keyword, plan_id=plan_id, status=status, page=1, page_size=10000).items
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
