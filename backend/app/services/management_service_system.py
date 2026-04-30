from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStoreSystemMixin:
    def get_dict_types(self, keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> DictTypeListResponse:
        records = self._postgres_store.list_dict_types(keyword=keyword, status=status)
        items = [DictTypeRecord(**item) for item in records]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return DictTypeListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_dict_type(self, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.create_dict_type(payload.model_dump())
        return DictTypeRecord(**record)

    def update_dict_type(self, dict_type_id: int, payload: DictTypeUpsert) -> DictTypeRecord:
        record = self._postgres_store.update_dict_type(dict_type_id, payload.model_dump())
        return DictTypeRecord(**record)

    def delete_dict_type(self, dict_type_id: int) -> None:
        self._postgres_store.delete_dict_type(dict_type_id)

    def get_dict_data(
        self,
        keyword: str | None = None,
        dict_type: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> DictDataListResponse:
        records = self._postgres_store.list_dict_data(keyword=keyword, dict_type=dict_type, status=status)
        items = [DictDataRecord(**item) for item in records]
        paged_items, total = self._paginate_items(items, page=page, page_size=page_size)
        return DictDataListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_dict_data(self, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.create_dict_data(payload.model_dump())
        return DictDataRecord(**record)

    def update_dict_data(self, dict_data_id: int, payload: DictDataUpsert) -> DictDataRecord:
        record = self._postgres_store.update_dict_data(dict_data_id, payload.model_dump())
        return DictDataRecord(**record)

    def delete_dict_data(self, dict_data_id: int) -> None:
        self._postgres_store.delete_dict_data(dict_data_id)

    def get_roles(
        self,
        keyword: str | None = None,
        scope_name: str | None = None,
        permission: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> RoleListResponse:
        try:
            items, total = self._postgres_store.list_roles_page(
                keyword=keyword,
                scope_name=scope_name,
                permission=permission,
                page=page,
                page_size=page_size,
            )
            records = [RoleRecord(**item) for item in items]
            return RoleListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query roles from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("roles"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["role_code"], item["role_name"], item["scope_name"], keyword=keyword)]
        if scope_name:
            items = [item for item in items if item["scope_name"] == scope_name]
        if permission:
            items = [item for item in items if permission in item.get("permissions", [])]
        records = [self._build_role_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return RoleListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_role(self, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            item = payload.model_dump()
            if any(role["role_code"] == item["role_code"] for role in self._list("roles")):
                raise ValueError("Role code already exists")
            item["permissions"] = self._validate_permissions(item.get("permissions", []))
            item["id"] = self._next_id("roles")
            self._list("roles").insert(0, item)
            operation_log = self._record_operation("系统治理", "角色", str(item["id"]), "新建角色", f'新建角色 {item["role_name"]}')
            try:
                self._postgres_store.sync_role(
                    item,
                    operation_log,
                    counters={
                        "roles": int(self._counters.get("roles", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return self._build_role_record(item)

    def update_role(self, role_id: int, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            new_values = payload.model_dump()
            if any(role["role_code"] == new_values["role_code"] and role["id"] != role_id for role in self._list("roles")):
                raise ValueError("Role code already exists")
            new_values["permissions"] = self._validate_permissions(new_values.get("permissions", []))
            updated = {**item, **new_values, "id": role_id}
            self._list("roles")[index] = updated
            affected_users: list[dict[str, Any]] = []
            affected_profiles: list[tuple[str, dict[str, Any]]] = []
            if item["role_code"] != updated["role_code"]:
                for user_index, user in enumerate(self._list("system_users")):
                    if user["role_code"] == item["role_code"]:
                        updated_user = {**user, "role_code": updated["role_code"]}
                        self._list("system_users")[user_index] = updated_user
                        affected_users.append(updated_user)
                for username, profile in self.state.setdefault("profiles", {}).items():
                    if profile.get("role_name") in {item["role_name"], item["role_code"]}:
                        updated_profile = {**profile, "role_name": updated["role_name"]}
                        self.state["profiles"][username] = updated_profile
                        affected_profiles.append((username, updated_profile))
            elif item["role_name"] != updated["role_name"]:
                for username, profile in self.state.setdefault("profiles", {}).items():
                    if profile.get("role_name") == item["role_name"]:
                        updated_profile = {**profile, "role_name": updated["role_name"]}
                        self.state["profiles"][username] = updated_profile
                        affected_profiles.append((username, updated_profile))
            operation_log = self._record_operation("系统治理", "角色", str(role_id), "调整权限", f'更新角色 {updated["role_name"]} 的权限配置')
            try:
                self._postgres_store.sync_role(updated, operation_log)
                for affected_user in affected_users:
                    affected_profile = self.state.setdefault("profiles", {}).get(affected_user["username"])
                    self._postgres_store.sync_system_user(affected_user, affected_profile)
                for username, affected_profile in affected_profiles:
                    if username not in {user["username"] for user in affected_users}:
                        self._postgres_store.sync_user_profile(affected_profile)
            except Exception:
                self._save()
            return self._build_role_record(updated)

    def delete_role(self, role_id: int) -> None:
        with self._lock:
            index, item = self._find_required("roles", role_id)
            in_use = next((user for user in self._list("system_users") if user["role_code"] == item["role_code"]), None)
            if in_use:
                raise ValueError("Role is assigned to users")
            self._list("roles").pop(index)
            operation_log = self._record_operation("系统治理", "角色", str(role_id), "删除角色", f'删除角色 {item["role_name"]}')
            try:
                self._postgres_store.delete_role(int(role_id))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_roles(self, role_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for role_id in role_ids:
            self.delete_role(role_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_system_users(
        self,
        keyword: str | None = None,
        role_code: str | None = None,
        account_status: str | None = None,
        department_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> SystemUserListResponse:
        try:
            items, total = self._postgres_store.list_system_users_page(
                keyword=keyword,
                role_code=role_code,
                account_status=account_status,
                department_name=department_name,
                page=page,
                page_size=page_size,
            )
            records = [SystemUserRecord(**item) for item in items]
            return SystemUserListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query system users from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("system_users"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["username"], item["full_name"], item["department_name"], keyword=keyword)]
        if role_code:
            items = [item for item in items if item["role_code"] == role_code]
        if account_status:
            items = [item for item in items if item["account_status"] == account_status]
        if department_name:
            items = [item for item in items if department_name in item["department_name"]]
        records = [self._build_system_user_record(item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return SystemUserListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_system_user(self, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            item = payload.model_dump()
            if any(user["username"] == item["username"] for user in self._list("system_users")):
                raise ValueError("Username already exists")
            role = self._ensure_role_exists(item["role_code"])
            item["id"] = self._next_id("system_users")
            item["password_hash"] = PASSWORD_CONTEXT.hash(item.pop("password") or DEFAULT_USER_PASSWORD)
            item["last_login_at"] = None
            self._list("system_users").insert(0, item)
            self.state.setdefault("profiles", {})[item["username"]] = {
                "username": item["username"],
                "full_name": item["full_name"],
                "role_name": role["role_name"],
                "department_name": item["department_name"],
                "phone_number": item.get("phone_number"),
                "email": None,
                "theme_color": "#0f4cbd",
            }
            profile = self.state["profiles"][item["username"]]
            operation_log = self._record_operation("系统治理", "系统用户", str(item["id"]), "新建账号", f'新建系统账号 {item["full_name"]}')
            try:
                self._postgres_store.sync_system_user(
                    item,
                    profile,
                    operation_log,
                    counters={
                        "system_users": int(self._counters.get("system_users", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return self._build_system_user_record(item)

    def update_system_user(self, user_id: int, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            new_values = payload.model_dump()
            if any(user["username"] == new_values["username"] and user["id"] != user_id for user in self._list("system_users")):
                raise ValueError("Username already exists")
            role = self._ensure_role_exists(new_values["role_code"])
            password = new_values.pop("password")
            updated = {**item, **new_values, "id": user_id}
            if password:
                updated["password_hash"] = PASSWORD_CONTEXT.hash(password)
            self._list("system_users")[index] = updated
            profile = self.state.setdefault("profiles", {}).get(updated["username"], {})
            self.state["profiles"][updated["username"]] = {
                "username": updated["username"],
                "full_name": updated["full_name"],
                "role_name": role["role_name"],
                "department_name": updated["department_name"],
                "phone_number": updated.get("phone_number"),
                "email": profile.get("email"),
                "theme_color": profile.get("theme_color", "#0f4cbd"),
            }
            if item["username"] != updated["username"]:
                old_profile = self.state.setdefault("profiles", {}).pop(item["username"], None)
                if old_profile:
                    self.state["profiles"][updated["username"]] = {**old_profile, "username": updated["username"]}
            action_name = "停用账号" if updated["account_status"] != "启用" and item.get("account_status") == "启用" else "维护账号"
            current_profile = self.state["profiles"][updated["username"]]
            operation_log = self._record_operation("系统治理", "系统用户", str(user_id), action_name, f'更新系统账号 {updated["full_name"]}')
            try:
                self._postgres_store.sync_system_user(updated, current_profile, operation_log)
                if item["username"] != updated["username"]:
                    self._postgres_store.delete_user_profile(item["username"])
            except Exception:
                self._save()
            return self._build_system_user_record(updated)

    def delete_system_user(self, user_id: int, current_username: str | None = None) -> None:
        with self._lock:
            index, item = self._find_required("system_users", user_id)
            if current_username and item["username"] == current_username:
                raise ValueError("Cannot delete current user")
            self._list("system_users").pop(index)
            self.state.setdefault("profiles", {}).pop(item["username"], None)
            operation_log = self._record_operation("系统治理", "系统用户", str(user_id), "删除账号", f'删除系统账号 {item["full_name"]}')
            try:
                self._postgres_store.delete_system_user(int(user_id), item["username"])
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_system_users(self, user_ids: list[int], current_username: str | None = None) -> BulkActionResponse:
        success_count = 0
        for user_id in user_ids:
            self.delete_system_user(user_id, current_username=current_username)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_audit_policy_records(self, keyword: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10) -> AuditPolicyListResponse:
        try:
            items, total = self._postgres_store.list_audit_policies_page(
                keyword=keyword,
                status=status,
                page=page,
                page_size=page_size,
            )
            records = [AuditPolicyRecord(**item) for item in items]
            return AuditPolicyListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query audit policies from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("audit_policies"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["item"], item["policy"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        records = [AuditPolicyRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return AuditPolicyListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_audit_policy(self, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("audit_policies")
            self._list("audit_policies").insert(0, item)
            operation_log = self._record_operation("系统治理", "审计策略", str(item["id"]), "新建策略", f'新建审计策略 {item["item"]}')
            try:
                self._postgres_store.sync_audit_policy(
                    item,
                    operation_log,
                    counters={
                        "audit_policies": int(self._counters.get("audit_policies", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return AuditPolicyRecord(**item)

    def update_audit_policy(self, policy_id: int, payload: AuditPolicyUpsert) -> AuditPolicyRecord:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            updated = {**item, **payload.model_dump(), "id": policy_id}
            self._list("audit_policies")[index] = updated
            operation_log = self._record_operation("系统治理", "审计策略", str(policy_id), "维护策略", f'更新审计策略 {updated["item"]}')
            try:
                self._postgres_store.sync_audit_policy(updated, operation_log)
            except Exception:
                self._save()
            return AuditPolicyRecord(**updated)

    def delete_audit_policy(self, policy_id: int) -> None:
        with self._lock:
            index, item = self._find_required("audit_policies", policy_id)
            self._list("audit_policies").pop(index)
            operation_log = self._record_operation("系统治理", "审计策略", str(policy_id), "删除策略", f'删除审计策略 {item["item"]}')
            try:
                self._postgres_store.delete_audit_policy(int(policy_id))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_audit_policies(self, policy_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for policy_id in policy_ids:
            self.delete_audit_policy(policy_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_integrations(
        self,
        keyword: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> IntegrationListResponse:
        try:
            items, total = self._postgres_store.list_integrations_page(
                keyword=keyword,
                status=status,
                direction=direction,
                page=page,
                page_size=page_size,
            )
            records = [IntegrationRecord(**item) for item in items]
            return IntegrationListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query integrations from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("integrations"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["name"], item["owner"], item["direction"], keyword=keyword)]
        if status:
            items = [item for item in items if item["status"] == status]
        if direction:
            items = [item for item in items if item["direction"] == direction]
        records = [IntegrationRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return IntegrationListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_integration(self, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("integrations")
            self._list("integrations").insert(0, item)
            operation_log = self._record_operation("系统治理", "集成链路", str(item["id"]), "新建链路", f'新建集成链路 {item["name"]}')
            try:
                self._postgres_store.sync_integration(
                    item,
                    operation_log,
                    counters={
                        "integrations": int(self._counters.get("integrations", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return IntegrationRecord(**item)

    def update_integration(self, integration_id: int, payload: IntegrationUpsert) -> IntegrationRecord:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            updated = {**item, **payload.model_dump(), "id": integration_id}
            self._list("integrations")[index] = updated
            operation_log = self._record_operation("系统治理", "集成链路", str(integration_id), "维护链路", f'更新集成链路 {updated["name"]}')
            try:
                self._postgres_store.sync_integration(updated, operation_log)
            except Exception:
                self._save()
            return IntegrationRecord(**updated)

    def delete_integration(self, integration_id: int) -> None:
        with self._lock:
            index, item = self._find_required("integrations", integration_id)
            self._list("integrations").pop(index)
            operation_log = self._record_operation("系统治理", "集成链路", str(integration_id), "删除链路", f'删除集成链路 {item["name"]}')
            try:
                self._postgres_store.delete_integration(int(integration_id), item["name"])
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def delete_integrations(self, integration_ids: list[int]) -> BulkActionResponse:
        success_count = 0
        for integration_id in integration_ids:
            self.delete_integration(integration_id)
            success_count += 1
        return BulkActionResponse(success_count=success_count)

    def get_operation_logs(
        self,
        keyword: str | None = None,
        module_name: str | None = None,
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> OperationLogListResponse:
        try:
            items, total = self._postgres_store.list_operation_logs_page(
                keyword=keyword,
                module_name=module_name,
                result=result,
                page=page,
                page_size=page_size,
            )
            records = [OperationLogRecord(**item) for item in items]
            return OperationLogListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query operation logs from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("operation_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["operator_username"], item["entity_name"], item["summary"], keyword=keyword)]
        if module_name:
            items = [item for item in items if item["module_name"] == module_name]
        if result:
            items = [item for item in items if item["result"] == result]
        records = [OperationLogRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return OperationLogListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_sync_logs(
        self,
        keyword: str | None = None,
        sync_status: str | None = None,
        source_system: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> SyncLogListResponse:
        try:
            items, total = self._postgres_store.list_sync_logs_page(
                keyword=keyword,
                sync_status=sync_status,
                source_system=source_system,
                page=page,
                page_size=page_size,
            )
            records = [SyncLogRecord(**item) for item in items]
            return SyncLogListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query sync logs from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("sync_logs"))
        if keyword:
            items = [item for item in items if self._matches_keyword(item["source_system"], item["target_system"], item.get("failure_reason"), keyword=keyword)]
        if sync_status:
            items = [item for item in items if item["sync_status"] == sync_status]
        if source_system:
            items = [item for item in items if item["source_system"] == source_system]
        records = [SyncLogRecord(**item) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return SyncLogListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def get_system_architecture(self) -> SystemArchitecture:
        return SystemArchitecture(
            authentication="JWT + RBAC",
            database="PostgreSQL 17-",
            cache="Redis（单机/哨兵）",
            audit=["login_logs", "operation_logs", "data_sync_logs"],
            integrations=[item["name"] for item in self._list("integrations")],
        )

    def get_system_stats(self) -> SystemStats:
        return SystemStats(
            integration_total=len(self._list("integrations")),
            active_integration_total=len([item for item in self._list("integrations") if item["status"] == "正常"]),
            operation_log_total=len(self._list("operation_logs")),
            sync_failure_total=len([item for item in self._list("sync_logs") if item["sync_status"] != "success"]),
            user_total=len(self._list("system_users")),
            role_total=len(self._list("roles")),
        )

    def get_profile(self, username: str) -> UserProfile:
        profile = None
        try:
            profile = self._postgres_store.get_user_profile(username)
        except Exception as exc:
            logger.warning("Load profile from PostgreSQL failed for %s: %s", username, exc)

        if profile:
            self.state.setdefault("profiles", {})[username] = profile
            return UserProfile(**profile)

        profile = self.state.setdefault("profiles", {}).get(username)
        if not profile:
            fallback = next((item for item in self._list("system_users") if item["username"] == username), None)
            if not fallback:
                raise KeyError(username)
            role = self._role_lookup().get(fallback["role_code"])
            profile = {
                "username": fallback["username"],
                "full_name": fallback["full_name"],
                "role_name": role["role_name"] if role else fallback["role_code"],
                "department_name": fallback["department_name"],
                "phone_number": fallback.get("phone_number"),
                "email": None,
                "theme_color": "#0f4cbd",
            }
            self.state.setdefault("profiles", {})[username] = profile
            try:
                self._postgres_store.sync_user_profile(profile)
            except Exception as exc:
                logger.warning("Profile fallback runtime sync failed for %s: %s", username, exc)
        return UserProfile(**profile)

    def update_profile(self, username: str, payload: UserProfileUpdate) -> UserProfile:
        with self._lock:
            current = self.get_profile(username).model_dump()
            updated = {**current, **payload.model_dump(), "username": username}
            self.state.setdefault("profiles", {})[username] = updated
            updated_user: dict[str, Any] | None = None
            for index, item in enumerate(self._list("system_users")):
                if item["username"] == username:
                    updated_user = {**item, "full_name": updated["full_name"], "phone_number": updated.get("phone_number")}
                    self._list("system_users")[index] = updated_user
                    break
            operation_log = self._record_operation("个人空间", "个人资料", username, "编辑", f'更新个人资料 {updated["full_name"]}', operator_username=username)
            try:
                self._postgres_store.sync_user_profile(updated)
                if updated_user is not None:
                    self._postgres_store.sync_system_user(updated_user, updated, operation_log)
                else:
                    self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()
            return UserProfile(**updated)
