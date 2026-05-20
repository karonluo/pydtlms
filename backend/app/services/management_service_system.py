from __future__ import annotations

from typing import TYPE_CHECKING

from .management_service_shared import *


class RuntimeManagementStoreSystemMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _record_system_user_failure(self, action: str, entity_id: str, username: str, reason: str) -> None:
        self.record_operation_event(
            "系统治理",
            "系统用户",
            entity_id,
            action,
            f"{action}失败：账号 {username}，原因：{reason}",
            result="failed",
        )

    def _cache_ttl(self, base_seconds: int, *, with_jitter: bool = True) -> int:
        if not with_jitter or CACHE_TTL_JITTER_SECONDS <= 0:
            return max(1, int(base_seconds))
        return max(1, int(base_seconds) + secrets.randbelow(CACHE_TTL_JITTER_SECONDS + 1))

    def _get_cache_client_safe(self):
        try:
            return self._get_cache_client()
        except Exception as exc:
            logger.warning("Redis cache unavailable, fallback to PostgreSQL direct read: %s", exc)
            return None

    def _get_cache_rebuild_lock(self, cache_key: str) -> Lock:
        with CACHE_REBUILD_LOCKS_GUARD:
            return CACHE_REBUILD_LOCKS.setdefault(cache_key, Lock())

    def _read_json_cache(self, cache_key: str) -> tuple[bool, Any | None]:
        client = self._get_cache_client_safe()
        if client is None:
            return False, None
        try:
            cached_value = client.get(cache_key)
        except Exception as exc:
            logger.warning("Read cache key %s failed: %s", cache_key, exc)
            return False, None
        if cached_value in (None, ""):
            return False, None
        if isinstance(cached_value, (bytes, bytearray)):
            cached_text = cached_value.decode("utf-8", errors="ignore")
        elif isinstance(cached_value, str):
            cached_text = cached_value
        else:
            return False, None
        try:
            payload = json.loads(cached_text)
        except Exception as exc:
            logger.warning("Decode cache key %s failed: %s", cache_key, exc)
            return False, None
        if isinstance(payload, dict) and payload.get(CACHE_NULL_SENTINEL_KEY) is True:
            return True, None
        return True, payload

    def _write_json_cache(self, cache_key: str, payload: Any, ttl_seconds: int, *, with_jitter: bool = True) -> None:
        client = self._get_cache_client_safe()
        if client is None:
            return
        try:
            client.set(
                cache_key,
                json.dumps(payload, ensure_ascii=False),
                ex=self._cache_ttl(ttl_seconds, with_jitter=with_jitter),
            )
        except Exception as exc:
            logger.warning("Write cache key %s failed: %s", cache_key, exc)

    def _delete_cache_keys(self, *cache_keys: str) -> None:
        normalized_keys = [str(key) for key in cache_keys if str(key).strip()]
        if not normalized_keys:
            return
        client = self._get_cache_client_safe()
        if client is None:
            return
        try:
            client.delete(*normalized_keys)
        except Exception as exc:
            logger.warning("Delete cache keys %s failed: %s", normalized_keys, exc)

    def _load_json_with_cache(self, cache_key: str, loader, *, ttl_seconds: int, null_ttl_seconds: int = CACHE_NULL_TTL_SECONDS):
        cache_hit, cached_payload = self._read_json_cache(cache_key)
        if cache_hit:
            return cached_payload
        rebuild_lock = self._get_cache_rebuild_lock(cache_key)
        with rebuild_lock:
            cache_hit, cached_payload = self._read_json_cache(cache_key)
            if cache_hit:
                return cached_payload
            payload = loader()
            if payload is None:
                self._write_json_cache(cache_key, {CACHE_NULL_SENTINEL_KEY: True}, null_ttl_seconds)
                return None
            self._write_json_cache(cache_key, payload, ttl_seconds)
            return payload

    def _system_user_auth_cache_key(self, username: str) -> str:
        return build_cache_key("system", "user", "auth", str(username))

    def _user_profile_cache_key(self, username: str) -> str:
        return build_cache_key("system", "user", "profile", str(username))

    def _system_user_list_cache_version_key(self) -> str:
        return build_cache_key("system", "users", "page-version")

    def _system_user_list_cache_version(self) -> str:
        client = self._get_cache_client_safe()
        if client is None:
            return "0"
        cache_key = self._system_user_list_cache_version_key()
        try:
            version = client.get(cache_key)
            if version:
                return str(version)
            client.set(cache_key, "1", ex=30 * 24 * 60 * 60)
            return "1"
        except Exception as exc:
            logger.warning("Read system user cache version failed: %s", exc)
            return "0"

    def _bump_system_user_list_cache_version(self) -> None:
        client = self._get_cache_client_safe()
        if client is None:
            return
        cache_key = self._system_user_list_cache_version_key()
        try:
            client.incr(cache_key)
            client.expire(cache_key, 30 * 24 * 60 * 60)
        except Exception as exc:
            logger.warning("Bump system user cache version failed: %s", exc)

    def _system_user_list_cache_key(
        self,
        *,
        keyword: str | None,
        role_code: str | None,
        account_status: str | None,
        department_name: str | None,
        page: int,
        page_size: int,
    ) -> str:
        fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "keyword": keyword,
                    "role_code": role_code,
                    "account_status": account_status,
                    "department_name": department_name,
                    "page": page,
                    "page_size": page_size,
                },
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:24]
        return build_cache_key("system", "users", "page", self._system_user_list_cache_version(), fingerprint)

    def _invalidate_system_user_cache(self, username: str | None = None, *, previous_username: str | None = None, bump_list_version: bool = True) -> None:
        cache_keys: list[str] = []
        if username:
            cache_keys.extend([self._system_user_auth_cache_key(username), self._user_profile_cache_key(username)])
        if previous_username and previous_username != username:
            cache_keys.extend([self._system_user_auth_cache_key(previous_username), self._user_profile_cache_key(previous_username)])
        self._delete_cache_keys(*cache_keys)
        if bump_list_version:
            self._bump_system_user_list_cache_version()

    def _invalidate_system_user_caches_for_role(self, role_code: str) -> None:
        usernames = [str(user.get("username") or "") for user in self._list("system_users") if user.get("role_code") == role_code]
        for username in usernames:
            self._invalidate_system_user_cache(username, bump_list_version=False)
        if usernames:
            self._bump_system_user_list_cache_version()

    def _load_system_user_auth_context(self, username: str) -> dict[str, Any] | None:
        cache_key = self._system_user_auth_cache_key(username)
        try:
            payload = self._load_json_with_cache(
                cache_key,
                lambda: self._postgres_store.get_system_user_by_username(username),
                ttl_seconds=SYSTEM_USER_AUTH_CACHE_TTL_SECONDS,
            )
        except Exception as exc:
            logger.warning("Load system auth context from PostgreSQL failed for %s: %s", username, exc)
            raise DatabaseUnavailableError("系统登录数据当前仅允许从数据库或Redis缓存读取，PostgreSQL 查询失败") from exc
        return dict(payload) if isinstance(payload, dict) else None

    def _normalize_system_user_contacts(self, payload: dict[str, Any], *, require_contact: bool) -> dict[str, Any]:
        normalized = dict(payload)
        introduction = normalized.get("introduction")
        normalized["introduction"] = str(introduction).strip() if introduction is not None else None
        if normalized.get("role_code") == "advisor" and not normalized.get("introduction"):
            raise ValueError("导师角色必须填写介绍")
        normalized["email"] = validate_email(normalized.get("email"), "邮箱") if require_contact else validate_optional_email(normalized.get("email"))
        normalized["phone_number"] = validate_phone_number(normalized.get("phone_number"), "手机号") if require_contact else validate_optional_phone_number(normalized.get("phone_number"))
        return normalized

    def _system_username_exists(self, username: str, *, exclude_user_id: int | None = None) -> bool:
        exists_in_postgres = getattr(self._postgres_store, "system_username_exists", None)
        if callable(exists_in_postgres):
            if bool(exists_in_postgres(username, exclude_user_id=exclude_user_id)):
                return True
        return any(
            user["username"] == username and (exclude_user_id is None or int(user["id"]) != int(exclude_user_id))
            for user in self._list("system_users")
        )

    def _get_system_user_for_write(self, user_id: int) -> tuple[int, dict[str, Any]]:
        runtime_users = self._list("system_users")
        runtime_index = next((index for index, user in enumerate(runtime_users) if int(user.get("id") or 0) == int(user_id)), None)
        postgres_loader = getattr(self._postgres_store, "get_system_user_by_id", None)
        if callable(postgres_loader):
            postgres_item = postgres_loader(int(user_id))
            if postgres_item is not None:
                if runtime_index is None:
                    runtime_users.insert(0, dict(postgres_item))
                    return 0, runtime_users[0]
                runtime_users[runtime_index] = {**runtime_users[runtime_index], **dict(postgres_item)}
                return runtime_index, runtime_users[runtime_index]
            if runtime_index is not None:
                return runtime_index, runtime_users[runtime_index]
            raise KeyError(user_id)
        if runtime_index is None:
            raise KeyError(user_id)
        return runtime_index, runtime_users[runtime_index]

    def _role_code_exists(self, role_code: str, *, exclude_role_id: int | None = None) -> bool:
        exists_in_postgres = getattr(self._postgres_store, "role_code_exists", None)
        if callable(exists_in_postgres):
            if bool(exists_in_postgres(role_code, exclude_role_id=exclude_role_id)):
                return True
        return any(
            role["role_code"] == role_code and (exclude_role_id is None or int(role["id"]) != int(exclude_role_id))
            for role in self._list("roles")
        )

    def _get_role_for_write(self, role_id: int) -> tuple[int, dict[str, Any]]:
        runtime_roles = self._list("roles")
        runtime_index = next((index for index, role in enumerate(runtime_roles) if int(role.get("id") or 0) == int(role_id)), None)
        postgres_loader = getattr(self._postgres_store, "get_role_by_id", None)
        if callable(postgres_loader):
            postgres_item = postgres_loader(int(role_id))
            if postgres_item is not None:
                if runtime_index is None:
                    runtime_roles.insert(0, dict(postgres_item))
                    return 0, runtime_roles[0]
                runtime_roles[runtime_index] = {**runtime_roles[runtime_index], **dict(postgres_item)}
                return runtime_index, runtime_roles[runtime_index]
            if runtime_index is not None:
                return runtime_index, runtime_roles[runtime_index]
            raise KeyError(role_id)
        if runtime_index is None:
            raise KeyError(role_id)
        return runtime_index, runtime_roles[runtime_index]

    def _get_audit_policy_for_write(self, policy_id: int) -> tuple[int, dict[str, Any]]:
        runtime_items = self._list("audit_policies")
        runtime_index = next((index for index, item in enumerate(runtime_items) if int(item.get("id") or 0) == int(policy_id)), None)
        postgres_loader = getattr(self._postgres_store, "get_audit_policy_by_id", None)
        if callable(postgres_loader):
            postgres_item = postgres_loader(int(policy_id))
            if postgres_item is not None:
                if runtime_index is None:
                    runtime_items.insert(0, dict(postgres_item))
                    return 0, runtime_items[0]
                runtime_items[runtime_index] = {**runtime_items[runtime_index], **dict(postgres_item)}
                return runtime_index, runtime_items[runtime_index]
            if runtime_index is not None:
                return runtime_index, runtime_items[runtime_index]
            raise KeyError(policy_id)
        if runtime_index is None:
            raise KeyError(policy_id)
        return runtime_index, runtime_items[runtime_index]

    def _get_integration_for_write(self, integration_id: int) -> tuple[int, dict[str, Any]]:
        runtime_items = self._list("integrations")
        runtime_index = next((index for index, item in enumerate(runtime_items) if int(item.get("id") or 0) == int(integration_id)), None)
        postgres_loader = getattr(self._postgres_store, "get_integration_by_id", None)
        if callable(postgres_loader):
            postgres_item = postgres_loader(int(integration_id))
            if postgres_item is not None:
                if runtime_index is None:
                    runtime_items.insert(0, dict(postgres_item))
                    return 0, runtime_items[0]
                runtime_items[runtime_index] = {**runtime_items[runtime_index], **dict(postgres_item)}
                return runtime_index, runtime_items[runtime_index]
            if runtime_index is not None:
                return runtime_index, runtime_items[runtime_index]
            raise KeyError(integration_id)
        if runtime_index is None:
            raise KeyError(integration_id)
        return runtime_index, runtime_items[runtime_index]

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
            logger.warning("Query roles from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("角色数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def create_role(self, payload: RoleUpsert) -> RoleRecord:
        with self._lock:
            item = payload.model_dump()
            if self._role_code_exists(item["role_code"]):
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
            index, item = self._get_role_for_write(role_id)
            new_values = payload.model_dump()
            if self._role_code_exists(new_values["role_code"], exclude_role_id=role_id):
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
            self._invalidate_system_user_caches_for_role(updated["role_code"])
            return self._build_role_record(updated)

    def delete_role(self, role_id: int) -> None:
        with self._lock:
            index, item = self._get_role_for_write(role_id)
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
        cache_key = self._system_user_list_cache_key(
            keyword=keyword,
            role_code=role_code,
            account_status=account_status,
            department_name=department_name,
            page=page,
            page_size=page_size,
        )
        try:
            def _load_page_payload() -> dict[str, Any]:
                items, total = self._postgres_store.list_system_users_page(
                    keyword=keyword,
                    role_code=role_code,
                    account_status=account_status,
                    department_name=department_name,
                    page=page,
                    page_size=page_size,
                )
                return {
                    "items": items,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                }

            payload = self._load_json_with_cache(
                cache_key,
                _load_page_payload,
                ttl_seconds=SYSTEM_USER_LIST_CACHE_TTL_SECONDS,
            )
            if not isinstance(payload, dict):
                raise RuntimeError("invalid system user cache payload")
            records = [SystemUserRecord(**item) for item in payload.get("items", [])]
            return SystemUserListResponse(items=records, total=int(payload.get("total") or 0), page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query system users from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("系统用户数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def create_system_user(self, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            raw_payload = payload.model_dump()
            username = str(raw_payload.get("username") or "")
            try:
                item = self._normalize_system_user_contacts(raw_payload, require_contact=False)
                if self._system_username_exists(item["username"]):
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
                    "introduction": item.get("introduction"),
                    "phone_number": item.get("phone_number"),
                    "email": item.get("email"),
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
                self._invalidate_system_user_cache(item["username"])
                self._write_json_cache(self._user_profile_cache_key(item["username"]), profile, USER_PROFILE_CACHE_TTL_SECONDS)
                return self._build_system_user_record(item)
            except ValueError as exc:
                self._record_system_user_failure("新建账号", username or "新账号", username or "未提供账号", str(exc))
                raise

    def update_system_user(self, user_id: int, payload: SystemUserUpsert) -> SystemUserRecord:
        with self._lock:
            raw_payload = payload.model_dump()
            username = str(raw_payload.get("username") or user_id)
            try:
                index, item = self._get_system_user_for_write(user_id)
            except KeyError:
                self._record_system_user_failure("维护账号", str(user_id), username or str(user_id), "系统账号不存在")
                raise
            try:
                new_values = self._normalize_system_user_contacts(raw_payload, require_contact=True)
                if self._system_username_exists(new_values["username"], exclude_user_id=user_id):
                    raise ValueError("Username already exists")
                role = self._ensure_role_exists(new_values["role_code"])
                password = new_values.pop("password")
                updated = {**item, **new_values, "id": user_id}
                if password:
                    updated["password_hash"] = PASSWORD_CONTEXT.hash(password)
                self._list("system_users")[index] = updated
                profile_store = self.state.setdefault("profiles", {})
                profile = profile_store.get(updated["username"], profile_store.get(item["username"], {}))
                self.state["profiles"][updated["username"]] = {
                    "username": updated["username"],
                    "full_name": updated["full_name"],
                    "role_name": role["role_name"],
                    "department_name": updated["department_name"],
                    "introduction": updated.get("introduction"),
                    "phone_number": updated.get("phone_number"),
                    "email": updated.get("email"),
                    "theme_color": profile.get("theme_color", "#0f4cbd"),
                }
                if item["username"] != updated["username"]:
                    old_profile = self.state.setdefault("profiles", {}).pop(item["username"], None)
                    if old_profile:
                        self.state["profiles"][updated["username"]] = {
                            **old_profile,
                            **self.state["profiles"][updated["username"]],
                            "username": updated["username"],
                        }
                action_name = "停用账号" if updated["account_status"] != "启用" and item.get("account_status") == "启用" else "维护账号"
                current_profile = self.state["profiles"][updated["username"]]
                operation_log = self._record_operation("系统治理", "系统用户", str(user_id), action_name, f'更新系统账号 {updated["full_name"]}')
                try:
                    self._postgres_store.sync_system_user(updated, current_profile, operation_log)
                    if item["username"] != updated["username"]:
                        self._postgres_store.delete_user_profile(item["username"])
                except Exception:
                    self._save()
                self._invalidate_system_user_cache(updated["username"], previous_username=item["username"])
                self._write_json_cache(self._user_profile_cache_key(updated["username"]), current_profile, USER_PROFILE_CACHE_TTL_SECONDS)
                return self._build_system_user_record(updated)
            except ValueError as exc:
                self._record_system_user_failure("维护账号", str(user_id), username or str(user_id), str(exc))
                raise

    def delete_system_user(self, user_id: int, current_username: str | None = None) -> None:
        with self._lock:
            index, item = self._get_system_user_for_write(user_id)
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
            self._invalidate_system_user_cache(item["username"])

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
            logger.warning("Query audit policies from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("审计策略数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

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
            index, item = self._get_audit_policy_for_write(policy_id)
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
            index, item = self._get_audit_policy_for_write(policy_id)
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
            logger.warning("Query integrations from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("集成链路数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

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
            index, item = self._get_integration_for_write(integration_id)
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
            index, item = self._get_integration_for_write(integration_id)
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
            logger.warning("Query operation logs from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("操作日志数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

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
            logger.warning("Query sync logs from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("同步日志数据当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_notification_delivery_logs(
        self,
        keyword: str | None = None,
        channel: str | None = None,
        send_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> NotificationDeliveryLogListResponse:
        try:
            items, total = self._postgres_store.list_notification_delivery_logs_page(
                keyword=keyword,
                channel=channel,
                send_status=send_status,
                page=page,
                page_size=page_size,
            )
            records = [NotificationDeliveryLogRecord(**item) for item in items]
            return NotificationDeliveryLogListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query notification delivery logs from PostgreSQL failed in database-only mode: %s", exc)
            raise DatabaseUnavailableError("通知发送日志当前仅允许从数据库读取，PostgreSQL 查询失败") from exc

    def get_system_architecture(self) -> SystemArchitecture:
        return SystemArchitecture(
            authentication="JWT + RBAC",
            database="PostgreSQL 17-",
            cache="Redis（单机/哨兵）",
            audit=["login_logs", "operation_logs", "data_sync_logs", "notification_delivery_logs"],
            integrations=[item["name"] for item in self._list("integrations")],
        )

    def get_system_stats(self) -> SystemStats:
        postgres_stats_loader = getattr(self._postgres_store, "get_system_stats_snapshot", None)
        if callable(postgres_stats_loader):
            try:
                return SystemStats(**postgres_stats_loader())
            except Exception as exc:
                logger.warning("Load system stats from PostgreSQL failed, fallback to runtime state: %s", exc)
        return SystemStats(
            integration_total=len(self._list("integrations")),
            active_integration_total=len([item for item in self._list("integrations") if item["status"] == "正常"]),
            operation_log_total=len(self._list("operation_logs")),
            sync_failure_total=len([item for item in self._list("sync_logs") if item["sync_status"] != "success"]),
            user_total=len(self._list("system_users")),
            role_total=len(self._list("roles")),
        )

    def get_profile(self, username: str) -> UserProfile:
        try:
            profile = self._load_json_with_cache(
                self._user_profile_cache_key(username),
                lambda: self._postgres_store.get_user_profile(username),
                ttl_seconds=USER_PROFILE_CACHE_TTL_SECONDS,
            )
        except Exception as exc:
            logger.warning("Load profile from PostgreSQL failed for %s: %s", username, exc)
            raise DatabaseUnavailableError("用户资料当前仅允许从数据库或Redis缓存读取，PostgreSQL 查询失败") from exc
        if not isinstance(profile, dict):
            raise KeyError(username)
        self.state.setdefault("profiles", {})[username] = dict(profile)
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
            self._invalidate_system_user_cache(username, bump_list_version=updated_user is not None)
            self._write_json_cache(self._user_profile_cache_key(username), updated, USER_PROFILE_CACHE_TTL_SECONDS)
            return UserProfile(**updated)
