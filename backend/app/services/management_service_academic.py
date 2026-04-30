from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStoreAcademicMixin:
    def get_training_workbench(self) -> TrainingWorkbench:
        outbound_counter = Counter(item["approval_status"] for item in self._list("outbound_studies"))
        return TrainingWorkbench(
            open_tasks=[
                TrainingTask(title="培养方案待学生确认", owner="导师", due_text="剩余 2 天", status="pending"),
                TrainingTask(title="科研报告待审阅", owner="导师", due_text="剩余 1 天", status="warning"),
                TrainingTask(title="外出研修超期未归提醒", owner="学合管理员", due_text="需要今日处置", status="critical"),
            ],
            supervision_rules=[
                {"rule": "入学 15 日内制定培养方案", "owner": "导师", "trigger": "自动待办"},
                {"rule": "学生 7 日内确认培养方案", "owner": "学生", "trigger": "站内信提醒"},
                {"rule": "科研报告逾期 7 日提醒导师", "owner": "系统控制", "trigger": "升级提醒"},
                {"rule": "外出研修需导师和学合管理员双节点审批", "owner": "审批中心", "trigger": "严格串行"},
            ],
            outbound_study_status=[
                {"status": label, "count": count} for label, count in outbound_counter.items()
            ],
        )

    def get_training_plans(
        self,
        keyword: str | None = None,
        plan_status: str | None = None,
        advisor_name: str | None = None,
        report_cycle: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> TrainingPlanListResponse:
        try:
            items, total = self._postgres_store.list_training_plans_page(
                keyword=keyword,
                plan_status=plan_status,
                advisor_name=advisor_name,
                report_cycle=report_cycle,
                page=page,
                page_size=page_size,
            )
            records = [TrainingPlanRecord(**item) for item in items]
            return TrainingPlanListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query training plans from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("training_plans"))
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item["student_no"], item["student_name"], item["scientific_goal"], keyword=keyword)
            ]
        if plan_status:
            items = [item for item in items if item["plan_status"] == plan_status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if report_cycle:
            items = [item for item in items if item["report_cycle"] == report_cycle]
        records = [TrainingPlanRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return TrainingPlanListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_training_plan(self, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("training_plans")
            self._list("training_plans").insert(0, item)
            operation_log = self._record_operation("培养管理", "培养方案", str(item["id"]), "登记方案", f'登记培养方案 {item["student_name"]}')
            try:
                self._postgres_store.sync_training_plan(
                    item,
                    operation_log,
                    counters={
                        "training_plans": int(self._counters.get("training_plans", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return TrainingPlanRecord(**item)

    def update_training_plan(self, plan_id: int, payload: TrainingPlanUpsert) -> TrainingPlanRecord:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            updated = {**item, **payload.model_dump(), "id": plan_id}
            self._list("training_plans")[index] = updated
            operation_log = self._record_operation("培养管理", "培养方案", str(plan_id), "维护方案", f'维护培养方案 {updated["student_name"]}')
            try:
                self._postgres_store.sync_training_plan(updated, operation_log)
            except Exception:
                self._save()
            return TrainingPlanRecord(**updated)

    def delete_training_plan(self, plan_id: int) -> None:
        with self._lock:
            index, item = self._find_required("training_plans", plan_id)
            self._list("training_plans").pop(index)
            operation_log = self._record_operation("培养管理", "培养方案", str(plan_id), "删除方案", f'删除培养方案 {item["student_name"]}')
            try:
                self._postgres_store.delete_training_plan(int(plan_id))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_training_plans(self, plan_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for plan_id in plan_ids:
            self.delete_training_plan(plan_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_scientific_reports(
        self,
        keyword: str | None = None,
        status: str | None = None,
        reviewer_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ScientificReportListResponse:
        try:
            items, total = self._postgres_store.list_scientific_reports_page(
                keyword=keyword,
                status=status,
                reviewer_name=reviewer_name,
                page=page,
                page_size=page_size,
            )
            records = [ScientificReportRecord(**item) for item in items]
            return ScientificReportListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query scientific reports from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("scientific_reports"))
        if status:
            items = [item for item in items if item["report_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item.get("business_key"), item["student_no"], item["student_name"], item["period_label"], item["summary"], keyword=keyword)
            ]
        if reviewer_name:
            items = [item for item in items if item.get("reviewer_name") == reviewer_name]
        records = [ScientificReportRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ScientificReportListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_scientific_report(self, payload: ScientificReportUpsert, principal: Any | None = None) -> ScientificReportRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("scientific_report", payload.model_dump())
            item["id"] = self._next_id("scientific_reports")
            self._list("scientific_reports").insert(0, item)
            self._start_managed_workflow("scientific_report", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("培养管理", "科研报告", str(item["id"]), "登记报告", f'登记科研报告 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.sync_scientific_report(
                    item,
                    operation_log,
                    counters={
                        "scientific_reports": int(self._counters.get("scientific_reports", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                        **({"workflow_tasks": int(self._counters.get("workflow_tasks", 0))} if task_located is not None else {}),
                    },
                )
                if task_located is not None:
                    self._postgres_store.sync_workflow_task(task_located[1])
            except Exception:
                self._save()
            return ScientificReportRecord(**item)

    def update_scientific_report(self, report_id: int, payload: ScientificReportUpsert) -> ScientificReportRecord:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            incoming = {**item, **payload.model_dump(), "id": report_id}
            self._ensure_managed_status_fields_unchanged("scientific_reports", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("scientific_report", report_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("scientific_report", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("scientific_reports")[index] = updated
            operation_log = self._record_operation("培养管理", "科研报告", str(report_id), "维护报告", f'维护科研报告 {updated["student_name"]}')
            try:
                self._postgres_store.sync_scientific_report(updated, operation_log)
                if task is not None:
                    self._postgres_store.sync_workflow_task(task)
            except Exception:
                self._save()
            return ScientificReportRecord(**updated)

    def delete_scientific_report(self, report_id: int) -> None:
        with self._lock:
            index, item = self._find_required("scientific_reports", report_id)
            located = self._workflow_task_index_by_entity("scientific_report", report_id)
            self._list("scientific_reports").pop(index)
            operation_log = self._record_operation("培养管理", "科研报告", str(report_id), "删除报告", f'删除科研报告 {item["student_name"]}')
            try:
                self._postgres_store.delete_scientific_report(int(report_id))
                if located is not None:
                    self._postgres_store.delete_workflow_task(int(located[1]["id"]), located[1].get("process_instance_id"))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_scientific_reports(self, report_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for report_id in report_ids:
            self.delete_scientific_report(report_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_outbound_studies(
        self,
        keyword: str | None = None,
        status: str | None = None,
        study_type: str | None = None,
        advisor_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> OutboundStudyListResponse:
        try:
            items, total = self._postgres_store.list_outbound_studies_page(
                keyword=keyword,
                status=status,
                study_type=study_type,
                advisor_name=advisor_name,
                page=page,
                page_size=page_size,
            )
            records = [OutboundStudyRecord(**item) for item in items]
            return OutboundStudyListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query outbound studies from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("outbound_studies"))
        if status:
            items = [item for item in items if item["approval_status"] == status]
        if keyword:
            items = [
                item
                for item in items
                if self._matches_keyword(item.get("business_key"), item["student_no"], item["student_name"], item["destination"], item.get("expected_outcome"), keyword=keyword)
            ]
        if study_type:
            items = [item for item in items if item["study_type"] == study_type]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        records = [OutboundStudyRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return OutboundStudyListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_outbound_study(self, payload: OutboundStudyUpsert, principal: Any | None = None) -> OutboundStudyRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("outbound_study", payload.model_dump())
            item["id"] = self._next_id("outbound_studies")
            self._list("outbound_studies").insert(0, item)
            self._start_managed_workflow("outbound_study", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("培养管理", "外出研修", str(item["id"]), "发起研修", f'发起外出研修 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.sync_outbound_study(
                    item,
                    operation_log,
                    counters={
                        "outbound_studies": int(self._counters.get("outbound_studies", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                        **({"workflow_tasks": int(self._counters.get("workflow_tasks", 0))} if task_located is not None else {}),
                    },
                )
                if task_located is not None:
                    self._postgres_store.sync_workflow_task(task_located[1])
            except Exception:
                self._save()
            return OutboundStudyRecord(**item)

    def update_outbound_study(self, study_id: int, payload: OutboundStudyUpsert) -> OutboundStudyRecord:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            incoming = {**item, **payload.model_dump(), "id": study_id}
            self._ensure_managed_status_fields_unchanged("outbound_studies", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("outbound_study", study_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("outbound_study", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("outbound_studies")[index] = updated
            operation_log = self._record_operation("培养管理", "外出研修", str(study_id), "维护研修", f'维护外出研修 {updated["student_name"]}')
            try:
                self._postgres_store.sync_outbound_study(updated, operation_log)
                if task is not None:
                    self._postgres_store.sync_workflow_task(task)
            except Exception:
                self._save()
            return OutboundStudyRecord(**updated)

    def delete_outbound_study(self, study_id: int) -> None:
        with self._lock:
            index, item = self._find_required("outbound_studies", study_id)
            located = self._workflow_task_index_by_entity("outbound_study", study_id)
            self._list("outbound_studies").pop(index)
            operation_log = self._record_operation("培养管理", "外出研修", str(study_id), "删除研修", f'删除外出研修 {item["student_name"]}')
            try:
                self._postgres_store.delete_outbound_study(int(study_id))
                if located is not None:
                    self._postgres_store.delete_workflow_task(int(located[1]["id"]), located[1].get("process_instance_id"))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_outbound_studies(self, study_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for study_id in study_ids:
            self.delete_outbound_study(study_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_training_stats(self) -> TrainingStats:
        return TrainingStats(
            training_plan_total=len(self._list("training_plans")),
            pending_confirmation_total=len([item for item in self._list("training_plans") if item["plan_status"] == "待学生确认"]),
            report_pending_total=len([item for item in self._list("scientific_reports") if item["report_status"] in {"待导师审阅", "退回修改"}]),
            outbound_active_total=len([item for item in self._list("outbound_studies") if item["approval_status"] in {"审批中", "研修中"}]),
        )

    def get_degree_workbench(self) -> DegreeWorkbench:
        status_counter = Counter(item["degree_status"] for item in self._list("theses"))
        return DegreeWorkbench(
            thesis_pipeline=[
                {"stage": "查重中", "count": len([item for item in self._list("theses") if item["thesis_status"] in {"待查重", "查重中"}])},
                {"stage": "盲审中", "count": len([item for item in self._list("theses") if item["blind_review_status"] == "进行中"])},
                {"stage": "预答辩待安排", "count": len([item for item in self._list("theses") if item["defense_status"] == "待安排"])},
                {"stage": "正式答辩待安排", "count": len([item for item in self._list("theses") if item["degree_status"] == "待正式答辩"])},
                {"stage": "授位审批", "count": status_counter.get("授位审批中", 0)},
            ],
            committee_tasks=[
                TrainingTask(title="指派盲审专家", owner="学位秘书", due_text="本周内", status="pending"),
                TrainingTask(title="组织预答辩会议", owner="导师", due_text="剩余 5 天", status="warning"),
                TrainingTask(title="学位委员会审议", owner="委员会秘书", due_text="答辩后 7 日内", status="pending"),
            ],
        )

    def get_theses(
        self,
        keyword: str | None = None,
        degree_status: str | None = None,
        advisor_name: str | None = None,
        thesis_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ThesisListResponse:
        try:
            items, total = self._postgres_store.list_theses_page(
                keyword=keyword,
                degree_status=degree_status,
                advisor_name=advisor_name,
                thesis_status=thesis_status,
                page=page,
                page_size=page_size,
            )
            records = [ThesisRecord(**item) for item in items]
            return ThesisListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query theses from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("theses"))
        if degree_status:
            items = [item for item in items if item["degree_status"] == degree_status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if thesis_status:
            items = [item for item in items if item["thesis_status"] == thesis_status]
        if keyword:
            term = keyword.lower()
            items = [
                item
                for item in items
                if term in str(item.get("business_key") or "").lower()
                or term in item["student_no"].lower()
                or term in item["student_name"].lower()
                or term in item["title"].lower()
            ]
        records = [ThesisRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ThesisListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_thesis(self, payload: ThesisUpsert, principal: Any | None = None) -> ThesisRecord:
        with self._lock:
            operator = self._principal_summary(principal or {"username": "admin", "full_name": "admin", "roles": []})
            item = self._workflow_initial_item("thesis", payload.model_dump())
            item["id"] = self._next_id("theses")
            self._list("theses").insert(0, item)
            self._start_managed_workflow("thesis", item, operator_username=operator["username"])
            task_located = self._workflow_task_index_by_business_key(str(item.get("business_key") or ""))
            operation_log = self._record_operation("学位管理", "论文主档", str(item["id"]), "新增", f'新增论文 {item["student_name"]}', operator_username=operator["username"])
            try:
                self._postgres_store.sync_thesis(
                    item,
                    operation_log,
                    counters={
                        "theses": int(self._counters.get("theses", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                        **({"workflow_tasks": int(self._counters.get("workflow_tasks", 0))} if task_located is not None else {}),
                    },
                )
                if task_located is not None:
                    self._postgres_store.sync_workflow_task(task_located[1])
            except Exception:
                self._save()
            return ThesisRecord(**item)

    def update_thesis(self, thesis_id: int, payload: ThesisUpsert) -> ThesisRecord:
        with self._lock:
            index, item = self._find_required("theses", thesis_id)
            incoming = {**item, **payload.model_dump(), "id": thesis_id}
            self._ensure_managed_status_fields_unchanged("theses", item, incoming)
            updated = incoming
            located = self._workflow_task_index_by_business_key(str(item.get("business_key") or updated.get("business_key") or ""))
            if located is None:
                located = self._workflow_task_index_by_entity("thesis", thesis_id)
            task = None
            if located is not None:
                task, task_changed = self._sync_managed_workflow_task("thesis", updated, existing_task=located[1])
                if task_changed:
                    self._list("workflow_tasks")[located[0]] = task
            self._list("theses")[index] = updated
            operation_log = self._record_operation("学位管理", "论文主档", str(thesis_id), "编辑", f'更新论文 {updated["student_name"]}')
            try:
                self._postgres_store.sync_thesis(updated, operation_log)
                if task is not None:
                    self._postgres_store.sync_workflow_task(task)
            except Exception:
                self._save()
            return ThesisRecord(**updated)

    def delete_thesis(self, thesis_id: int) -> None:
        with self._lock:
            index, item = self._find_required("theses", thesis_id)
            located = self._workflow_task_index_by_entity("thesis", thesis_id)
            self._list("theses").pop(index)
            operation_log = self._record_operation("学位管理", "论文主档", str(thesis_id), "删除", f'删除论文 {item["student_name"]}')
            try:
                self._postgres_store.delete_thesis(int(thesis_id))
                if located is not None:
                    self._postgres_store.delete_workflow_task(int(located[1]["id"]), located[1].get("process_instance_id"))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def get_thesis_reviews(
        self,
        thesis_id: int | None = None,
        keyword: str | None = None,
        expert_name: str | None = None,
        review_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> ThesisReviewListResponse:
        try:
            items, total = self._postgres_store.list_thesis_reviews_page(
                thesis_id=thesis_id,
                keyword=keyword,
                expert_name=expert_name,
                review_status=review_status,
                page=page,
                page_size=page_size,
            )
            records = [ThesisReviewRecord(**item) for item in items]
            return ThesisReviewListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query thesis reviews from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("thesis_reviews"))
        if thesis_id is not None:
            items = [item for item in items if item["thesis_id"] == thesis_id]
        if expert_name:
            items = [item for item in items if item["expert_name"] == expert_name]
        if review_status:
            items = [item for item in items if item["review_status"] == review_status]
        if keyword:
            items = [item for item in items if self._matches_keyword(item["thesis_title"], item["expert_name"], item.get("review_comment"), keyword=keyword)]
        records = [ThesisReviewRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return ThesisReviewListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_thesis_review(self, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("thesis_reviews")
            self._list("thesis_reviews").insert(0, item)
            operation_log = self._record_operation("学位管理", "盲审意见", str(item["id"]), "新增", f'新增盲审意见 {item["expert_name"]}')
            try:
                self._postgres_store.sync_thesis_review(
                    item,
                    operation_log,
                    counters={
                        "thesis_reviews": int(self._counters.get("thesis_reviews", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return ThesisReviewRecord(**item)

    def update_thesis_review(self, review_id: int, payload: ThesisReviewUpsert) -> ThesisReviewRecord:
        with self._lock:
            index, item = self._find_required("thesis_reviews", review_id)
            updated = {**item, **payload.model_dump(), "id": review_id}
            self._list("thesis_reviews")[index] = updated
            operation_log = self._record_operation("学位管理", "盲审意见", str(review_id), "编辑", f'更新盲审意见 {updated["expert_name"]}')
            try:
                self._postgres_store.sync_thesis_review(updated, operation_log)
            except Exception:
                self._save()
            return ThesisReviewRecord(**updated)

    def get_degree_stats(self) -> DegreeStats:
        return DegreeStats(
            thesis_total=len(self._list("theses")),
            plagiarism_pending_total=len([item for item in self._list("theses") if item["thesis_status"] in {"待查重", "查重中"}]),
            blind_review_pending_total=len([item for item in self._list("theses") if item["blind_review_status"] in {"进行中", "未送审"}]),
            defense_pending_total=len([item for item in self._list("theses") if item["defense_status"] in {"待安排", "未进入"}]),
            degree_granted_total=len([item for item in self._list("theses") if item["degree_status"] == "已授位"]),
        )
