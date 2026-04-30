from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStoreStudentsMixin:
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
            logger.warning("Query students from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("students"))
        if keyword:
            term = keyword.lower()
            items = [item for item in items if term in item["student_no"].lower() or term in item["full_name"].lower() or term in item["team_name"].lower()]
        if status:
            items = [item for item in items if item["status"] == status]
        if advisor_name:
            items = [item for item in items if item["advisor_name"] == advisor_name]
        if center_name:
            items = [item for item in items if item["team_name"] == center_name]
        records = [
            StudentRecord(
                id=item["id"],
                student_no=item["student_no"],
                full_name=item["full_name"],
                status=item["status"],
                advisor_name=item["advisor_name"],
                center_name=item["team_name"],
                degree_type=item["degree_type"],
                enrollment_year=item["enrollment_year"],
                phone_number=item.get("phone_number"),
                political_status=item.get("political_status"),
            )
            for item in items
        ]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return StudentManagementResponse(items=paged_items, total=total, page=page, page_size=page_size)

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
            logger.warning("Query centers from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("teams"))
        if keyword:
            items = [
                item for item in items
                if self._matches_keyword(
                    item.get("team_name"),
                    item.get("lead_advisor_name"),
                    *(item.get("advisor_names") or []),
                    keyword=keyword,
                )
            ]
        if is_enabled is not None:
            items = [item for item in items if (item.get("status") == "启用") == is_enabled]
        if director_id:
            items = [item for item in items if int(item.get("director_id") or item.get("lead_user_id") or 0) == int(director_id)]
        records = [self._build_center_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return CenterListResponse(items=paged_items, total=total, page=page, page_size=page_size)

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
            logger.warning("Query registered portal students from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        portal_students = list(self._list("portal_students"))
        applications = list(self._list("recruitment_applications"))
        plan_name_map = {int(item.get("id") or 0): str(item.get("plan_name") or "") for item in self._list("recruitment_plans")}

        latest_application_map: dict[int, dict[str, Any]] = {}
        for application in applications:
            portal_student_id = int(application.get("portal_student_id") or 0)
            if portal_student_id <= 0:
                continue
            previous = latest_application_map.get(portal_student_id)
            current_sort_key = str(application.get("applied_at") or application.get("created_at") or "")
            previous_sort_key = str(previous.get("applied_at") or previous.get("created_at") or "") if previous else ""
            if previous is None or current_sort_key >= previous_sort_key:
                latest_application_map[portal_student_id] = application

        records = []
        for student in portal_students:
            student_id = int(student.get("id") or 0)
            latest_application = latest_application_map.get(student_id)
            submitted_at = str(student.get("submitted_at") or latest_application.get("applied_at") or "").strip() if latest_application else str(student.get("submitted_at") or "").strip()
            application_status = str(latest_application.get("application_status") or "").strip() if latest_application else ""
            plan_id = student.get("selected_plan_id") or (latest_application.get("plan_id") if latest_application else None)
            record = RegisteredPortalStudentRecord(
                id=student_id,
                full_name=str(student.get("full_name") or ""),
                phone_number=str(student.get("phone_number") or ""),
                email=str(student.get("email") or ""),
                id_number=str(student.get("id_number") or ""),
                account_status=self._normalize_portal_account_status(student.get("account_status")),
                application_form_status="驳回重填" if application_status == "驳回重填" else ("已填写报名" if submitted_at else "未填写报名"),
                selected_plan_name=plan_name_map.get(int(plan_id or 0)) if plan_id is not None else None,
                selected_center_name=str(student.get("selected_team_name") or "") or None,
                selected_advisor_name=str(student.get("selected_advisor_name") or "") or None,
                recruitment_application_id=int(latest_application.get("id") or 0) if latest_application else None,
                recruitment_application_business_key=(str(latest_application.get("business_key") or "") or None) if latest_application else None,
                recruitment_application_status=application_status or None,
                registered_at=str(student.get("created_at") or "") or None,
                submitted_at=None if application_status == "驳回重填" else (submitted_at or None),
            )
            records.append(record)

        if keyword:
            records = [
                record for record in records
                if self._matches_keyword(
                    record.full_name,
                    record.phone_number,
                    record.email,
                    record.id_number,
                    record.selected_plan_name,
                    record.selected_center_name,
                    record.selected_advisor_name,
                    keyword=keyword,
                )
            ]
        if application_form_status:
            records = [record for record in records if record.application_form_status == application_form_status]

        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RegisteredPortalStudentListResponse(items=paged_items, total=total, page=page, page_size=page_size)

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
