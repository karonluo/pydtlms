"""System governance PostgreSQL query mixin.

This module contains system users, roles, audit logs, integrations, and dict queries.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)

class PostgresStateStoreQuerySystemMixin:
    """Query mixin extracted by functional module."""

    def get_system_user_by_id(self, user_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_system_user_by_id`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.id = %s AND u.is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(user_id),),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                normalized = self._normalize_system_user_row(dict(row))
                normalized["password_hash"] = row.get("password_hash")
                return normalized

    def get_system_user_by_username(self, username: str) -> dict[str, Any] | None:
        """Execute query logic for `get_system_user_by_username`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.username = %s AND u.is_deleted = FALSE
                    GROUP BY u.id, u.username, u.full_name, u.password_hash, r.role_code, r.role_name, up.department_name, u.department_name, up.introduction, up.email, u.email, up.phone_number, u.phone_number, u.is_active, u.last_login_at
                    LIMIT 1
                    """,
                    (str(username),),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                normalized = self._normalize_system_user_row(dict(row))
                normalized["password_hash"] = row.get("password_hash")
                normalized["permissions"] = [str(item) for item in (row.get("permissions") or []) if str(item).strip()]
                return normalized

    def system_username_exists(self, username: str, *, exclude_user_id: int | None = None) -> bool:
        """Execute query logic for `system_username_exists`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if exclude_user_id is None:
                    cur.execute(
                        "SELECT 1 FROM dtlms_users WHERE username = %s AND is_deleted = FALSE LIMIT 1",
                        (str(username),),
                    )
                else:
                    cur.execute(
                        "SELECT 1 FROM dtlms_users WHERE username = %s AND is_deleted = FALSE AND id <> %s LIMIT 1",
                        (str(username), int(exclude_user_id)),
                    )
                return cur.fetchone() is not None

    def load_role_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_role_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE r.is_deleted = FALSE
                    GROUP BY r.id
                    ORDER BY r.id ASC
                    """
                )
                return [self._normalize_role_row(dict(row)) for row in cur.fetchall()]

    def get_role_by_id(self, role_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_role_by_id`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE r.id = %s AND r.is_deleted = FALSE
                    GROUP BY r.id
                    LIMIT 1
                    """,
                    (int(role_id),),
                )
                row = cur.fetchone()
                return self._normalize_role_row(dict(row)) if row is not None else None

    def role_code_exists(self, role_code: str, *, exclude_role_id: int | None = None) -> bool:
        """Execute query logic for `role_code_exists`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if exclude_role_id is None:
                    cur.execute(
                        "SELECT 1 FROM dtlms_roles WHERE role_code = %s AND is_deleted = FALSE LIMIT 1",
                        (str(role_code),),
                    )
                else:
                    cur.execute(
                        "SELECT 1 FROM dtlms_roles WHERE role_code = %s AND is_deleted = FALSE AND id <> %s LIMIT 1",
                        (str(role_code), int(exclude_role_id)),
                    )
                return cur.fetchone() is not None

    def missing_permission_codes(self, permission_codes: list[str]) -> list[str]:
        """Execute query logic for `missing_permission_codes`."""
        normalized_codes = list(dict.fromkeys(str(code).strip() for code in permission_codes if str(code).strip()))
        if not normalized_codes:
            return []
        placeholders = ", ".join(["%s"] * len(normalized_codes))
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT permission_code FROM dtlms_permissions WHERE is_deleted = FALSE AND permission_code IN ({placeholders})",
                    normalized_codes,
                )
                existing_codes = {str(row[0]).strip() for row in cur.fetchall() if str(row[0]).strip()}
        return [code for code in normalized_codes if code not in existing_codes]

    def load_system_user_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_system_user_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        u.password_hash,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        COALESCE(up.email, u.email) AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE u.is_deleted = FALSE
                    ORDER BY u.id ASC
                    """
                )
                rows: list[dict[str, Any]] = []
                for row in cur.fetchall():
                    normalized = self._normalize_system_user_row(dict(row))
                    normalized["password_hash"] = row.get("password_hash")
                    rows.append(normalized)
                return rows

    def get_role_deletion_preview(self, role_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_role_deletion_preview`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, role_code, role_name, COALESCE(scope_name, '系统管理') AS scope_name
                    FROM dtlms_roles
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(role_id),),
                )
                role_row = cur.fetchone()
                if role_row is None:
                    return None
                cur.execute(
                    """
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        role_counts.role_count,
                        fallback.role_code AS fallback_role_code,
                        fallback.role_name AS fallback_role_name
                    FROM dtlms_users u
                    JOIN dtlms_user_roles ur_target ON ur_target.user_id = u.id AND ur_target.role_id = %s
                    LEFT JOIN LATERAL (
                        SELECT COUNT(*) AS role_count
                        FROM dtlms_user_roles ur_all
                        JOIN dtlms_roles r_all ON r_all.id = ur_all.role_id AND r_all.is_deleted = FALSE
                        WHERE ur_all.user_id = u.id
                    ) role_counts ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT r_rem.role_code, r_rem.role_name
                        FROM dtlms_user_roles ur_rem
                        JOIN dtlms_roles r_rem ON r_rem.id = ur_rem.role_id AND r_rem.is_deleted = FALSE
                        WHERE ur_rem.user_id = u.id AND ur_rem.role_id <> %s
                        ORDER BY r_rem.id ASC
                        LIMIT 1
                    ) fallback ON TRUE
                    WHERE u.is_deleted = FALSE
                    ORDER BY u.id ASC
                    """,
                    (int(role_id), int(role_id)),
                )
                assigned_users: list[dict[str, Any]] = []
                blocking_users: list[dict[str, Any]] = []
                for row in cur.fetchall():
                    role_count = int(row.get("role_count") or 0)
                    can_be_unbound = role_count > 1 and bool(row.get("fallback_role_code"))
                    item = {
                        "id": int(row["id"]),
                        "username": str(row["username"]),
                        "full_name": str(row["full_name"]),
                        "role_count": role_count,
                        "fallback_role_code": row.get("fallback_role_code"),
                        "fallback_role_name": row.get("fallback_role_name"),
                        "can_be_unbound": can_be_unbound,
                    }
                    assigned_users.append(item)
                    if not can_be_unbound:
                        blocking_users.append(item)
                return {
                    "id": int(role_row["id"]),
                    "role_code": str(role_row["role_code"]),
                    "role_name": str(role_row["role_name"]),
                    "scope_name": str(role_row["scope_name"]),
                    "assigned_users": assigned_users,
                    "blocking_users": blocking_users,
                    "assigned_user_count": len(assigned_users),
                    "blocking_user_count": len(blocking_users),
                    "can_force_delete": len(blocking_users) == 0,
                    "message": (
                        f"该角色当前被 {len(assigned_users)} 位用户使用。"
                        if assigned_users
                        else "该角色当前未被任何用户使用，可直接删除。"
                    ),
                }

    def load_user_profile_state(self) -> dict[str, dict[str, Any]]:
        """Execute query logic for `load_user_profile_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT username, full_name, role_name, department_name, introduction, phone_number, email, theme_color
                    FROM dtlms_user_profiles
                    ORDER BY username ASC
                    """
                )
                return {str(row["username"]): dict(row) for row in cur.fetchall()}

    def load_audit_policy_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_audit_policy_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, item, policy, status
                    FROM dtlms_audit_policies
                    WHERE is_deleted = FALSE
                    ORDER BY id ASC
                    """
                )
                return [self._normalize_audit_policy_row(dict(row)) for row in cur.fetchall()]

    def get_audit_policy_by_id(self, policy_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_audit_policy_by_id`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, item, policy, status
                    FROM dtlms_audit_policies
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(policy_id),),
                )
                row = cur.fetchone()
                return self._normalize_audit_policy_row(dict(row)) if row is not None else None

    def load_integration_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_integration_state`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, direction, cadence, status, owner
                    FROM dtlms_integrations
                    WHERE is_deleted = FALSE
                    ORDER BY id ASC
                    """
                )
                return [self._normalize_integration_row(dict(row)) for row in cur.fetchall()]

    def get_integration_by_id(self, integration_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_integration_by_id`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, direction, cadence, status, owner
                    FROM dtlms_integrations
                    WHERE id = %s AND is_deleted = FALSE
                    LIMIT 1
                    """,
                    (int(integration_id),),
                )
                row = cur.fetchone()
                return self._normalize_integration_row(dict(row)) if row is not None else None

    def get_system_stats_snapshot(self) -> dict[str, int]:
        """Execute query logic for `get_system_stats_snapshot`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        (SELECT COUNT(*) FROM dtlms_integrations WHERE is_deleted = FALSE) AS integration_total,
                        (SELECT COUNT(*) FROM dtlms_integrations WHERE is_deleted = FALSE AND status = '正常') AS active_integration_total,
                        (SELECT COUNT(*) FROM dtlms_operation_logs) AS operation_log_total,
                        (SELECT COUNT(*) FROM dtlms_data_sync_logs WHERE sync_status <> 'success') AS sync_failure_total,
                        (SELECT COUNT(*) FROM dtlms_users WHERE is_deleted = FALSE) AS user_total,
                        (SELECT COUNT(*) FROM dtlms_roles WHERE is_deleted = FALSE) AS role_total
                    """
                )
                row = cur.fetchone()
                return {
                    "integration_total": int(row["integration_total"] if row else 0),
                    "active_integration_total": int(row["active_integration_total"] if row else 0),
                    "operation_log_total": int(row["operation_log_total"] if row else 0),
                    "sync_failure_total": int(row["sync_failure_total"] if row else 0),
                    "user_total": int(row["user_total"] if row else 0),
                    "role_total": int(row["role_total"] if row else 0),
                }

    def list_operation_logs_page(
        self,
        keyword: str | None = None,
        module_name: str | None = None,
        log_scope: str = "management",
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_operation_logs_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    operator_username ILIKE %s
                    OR entity_name ILIKE %s
                    OR COALESCE(new_value->>'summary', '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if module_name:
            where_clauses.append("module_name = %s")
            params.append(module_name)
        normalized_scope = str(log_scope or "management").strip().lower()
        if normalized_scope == "management":
            where_clauses.append("module_name <> %s")
            params.append("学生门户")
        elif normalized_scope == "portal":
            where_clauses.append("module_name = %s")
            params.append("学生门户")
        if result:
            where_clauses.append("result = %s")
            params.append(result)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_operation_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, created_at, operator_username, module_name, entity_name, entity_id, action, result, new_value
                    FROM dtlms_operation_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_operation_log_row(dict(row)) for row in cur.fetchall()], total

    def list_sync_logs_page(
        self,
        keyword: str | None = None,
        sync_status: str | None = None,
        source_system: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_sync_logs_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    source_system ILIKE %s
                    OR target_system ILIKE %s
                    OR COALESCE(failure_reason, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if sync_status:
            where_clauses.append("sync_status = %s")
            params.append(sync_status)
        if source_system:
            where_clauses.append("source_system = %s")
            params.append(source_system)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_data_sync_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, source_system, target_system, sync_status, record_count, created_at, failure_reason
                    FROM dtlms_data_sync_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_sync_log_row(dict(row)) for row in cur.fetchall()], total

    def list_notification_delivery_logs_page(
        self,
        keyword: str | None = None,
        channel: str | None = None,
        send_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_notification_delivery_logs_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    recipient ILIKE %s
                    OR subject ILIKE %s
                    OR COALESCE(template_code, '') ILIKE %s
                    OR COALESCE(failure_reason, '') ILIKE %s
                    OR COALESCE(business_key, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 5)
        if channel:
            where_clauses.append("channel = %s")
            params.append(channel)
        if send_status:
            where_clauses.append("send_status = %s")
            params.append(send_status)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"SELECT COUNT(*) AS total FROM dtlms_notification_delivery_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT id, channel, template_code, recipient, subject, send_status, failure_reason, business_key, triggered_by, created_at
                    FROM dtlms_notification_delivery_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_notification_delivery_log_row(dict(row)) for row in cur.fetchall()], total

    def list_roles_page(
        self,
        keyword: str | None = None,
        scope_name: str | None = None,
        permission: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_roles_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["r.is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(r.role_code ILIKE %s OR r.role_name ILIKE %s OR COALESCE(r.scope_name, '') ILIKE %s)")
            params.extend([keyword_like, keyword_like, keyword_like])
        if scope_name:
            where_clauses.append("COALESCE(r.scope_name, '') = %s")
            params.append(scope_name)
        if permission:
            where_clauses.append(
                "EXISTS (SELECT 1 FROM dtlms_role_permissions rp2 JOIN dtlms_permissions p2 ON p2.id = rp2.permission_id AND p2.is_deleted = FALSE WHERE rp2.role_id = r.id AND p2.permission_code = %s)"
            )
            params.append(permission)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_roles r WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        r.id,
                        r.role_code,
                        r.role_name,
                        COALESCE(r.scope_name, '系统管理') AS scope_name,
                        COALESCE(array_agg(DISTINCT p.permission_code) FILTER (WHERE p.permission_code IS NOT NULL), ARRAY[]::varchar[]) AS permissions,
                        COUNT(DISTINCT ur.user_id) FILTER (WHERE u.is_deleted = FALSE) AS user_count
                    FROM dtlms_roles r
                    LEFT JOIN dtlms_role_permissions rp ON rp.role_id = r.id
                    LEFT JOIN dtlms_permissions p ON p.id = rp.permission_id AND p.is_deleted = FALSE
                    LEFT JOIN dtlms_user_roles ur ON ur.role_id = r.id
                    LEFT JOIN dtlms_users u ON u.id = ur.user_id
                    WHERE {where_sql}
                    GROUP BY r.id
                    ORDER BY r.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_role_row(dict(row)) for row in cur.fetchall()], total

    def list_audit_policies_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_audit_policies_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(item ILIKE %s OR policy ILIKE %s)")
            params.extend([keyword_like, keyword_like])
        if status:
            where_clauses.append("status = %s")
            params.append(status)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_audit_policies WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"SELECT id, item, policy, status FROM dtlms_audit_policies WHERE {where_sql} ORDER BY id DESC LIMIT %s OFFSET %s",
                    [*params, page_size, offset],
                )
                return [self._normalize_audit_policy_row(dict(row)) for row in cur.fetchall()], total

    def list_integrations_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_integrations_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["is_deleted = FALSE"]
        params: list[Any] = []
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append("(name ILIKE %s OR owner ILIKE %s OR direction ILIKE %s)")
            params.extend([keyword_like, keyword_like, keyword_like])
        if status:
            where_clauses.append("status = %s")
            params.append(status)
        if direction:
            where_clauses.append("direction = %s")
            params.append(direction)
        where_sql = " AND ".join(where_clauses)
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(cur, f"SELECT COUNT(*) AS total FROM dtlms_integrations WHERE {where_sql}", params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)
                self._execute_dynamic(
                    cur,
                    f"SELECT id, name, direction, cadence, status, owner FROM dtlms_integrations WHERE {where_sql} ORDER BY id DESC LIMIT %s OFFSET %s",
                    [*params, page_size, offset],
                )
                return [self._normalize_integration_row(dict(row)) for row in cur.fetchall()], total

    def list_system_users_page(
        self,
        keyword: str | None = None,
        role_code: str | None = None,
        account_status: str | None = None,
        department_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_system_users_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["u.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    COALESCE(u.username, '') ILIKE %s
                    OR COALESCE(u.full_name, '') ILIKE %s
                    OR COALESCE(up.department_name, u.department_name, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if role_code:
            where_clauses.append("COALESCE(r.role_code, '') = %s")
            params.append(role_code)
        if account_status:
            where_clauses.append("CASE WHEN u.is_active THEN '启用' ELSE '停用' END = %s")
            params.append(account_status)
        if department_name:
            where_clauses.append("COALESCE(up.department_name, u.department_name, '') ILIKE %s")
            params.append(f"%{department_name}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        u.id,
                        u.username,
                        u.full_name,
                        COALESCE(r.role_code, '') AS role_code,
                        COALESCE(r.role_name, '') AS role_name,
                        COALESCE(up.department_name, u.department_name, '') AS department_name,
                        up.introduction AS introduction,
                        up.email AS email,
                        COALESCE(up.phone_number, u.phone_number) AS phone_number,
                        CASE WHEN u.is_active THEN '启用' ELSE '停用' END AS account_status,
                        u.last_login_at
                    FROM dtlms_users u
                    LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
                    LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
                    LEFT JOIN dtlms_user_profiles up ON up.username = u.username
                    WHERE {where_sql}
                    ORDER BY u.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_system_user_row(dict(row)) for row in cur.fetchall()], total

    def list_dict_types(self, keyword: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        """Execute query logic for `list_dict_types`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["t.is_deleted = FALSE"]
                params: list[Any] = []
                if status:
                    where_clauses.append("t.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(t.dict_name ILIKE %s OR t.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT t.id, t.dict_name, t.dict_type, t.status, t.remark, COUNT(d.id) AS data_count
                    FROM dtlms_dict_types t
                    LEFT JOIN dtlms_dict_data d ON d.dict_type_id = t.id AND d.is_deleted = FALSE
                    WHERE {' AND '.join(where_clauses)}
                    GROUP BY t.id
                    ORDER BY t.id DESC
                """
                self._execute_dynamic(cur, sql_text, params)
                return [self._normalize_dict_row(dict(row) | {"data_count": int(row["data_count"])} ) for row in cur.fetchall()]

    def list_dict_data(self, keyword: str | None = None, dict_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        """Execute query logic for `list_dict_data`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["d.is_deleted = FALSE", "t.is_deleted = FALSE"]
                params: list[Any] = []
                if dict_type:
                    where_clauses.append("d.dict_type = %s")
                    params.append(dict_type)
                if status:
                    where_clauses.append("d.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(d.label ILIKE %s OR d.value ILIKE %s OR d.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT d.id, d.dict_type, t.dict_name, d.label, d.value, d.sort_order, d.status, d.color_type, d.css_class, d.remark
                    FROM dtlms_dict_data d
                    JOIN dtlms_dict_types t ON t.id = d.dict_type_id
                    WHERE {' AND '.join(where_clauses)}
                    ORDER BY d.dict_type ASC, d.sort_order ASC, d.id ASC
                """
                self._execute_dynamic(cur, sql_text, params)
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def list_dict_options(self, dict_type: str) -> list[dict[str, Any]]:
        """Execute query logic for `list_dict_options`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT label, value, color_type, css_class
                    FROM dtlms_dict_data
                    WHERE is_deleted = FALSE AND status = '启用' AND dict_type = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (dict_type,),
                )
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def create_dict_type(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `create_dict_type`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s", (payload["dict_type"],))
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark")),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "create_dict_type"))
            conn.commit()
        return record | {"data_count": 0}

    def update_dict_type(self, dict_type_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `update_dict_type`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id, dict_type FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                current = cur.fetchone()
                if not current:
                    raise KeyError(dict_type_id)
                cur.execute(
                    "SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s AND id <> %s",
                    (payload["dict_type"], dict_type_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_types
                    SET dict_name = %s, dict_type = %s, status = %s, remark = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark"), dict_type_id),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "update_dict_type"))
                if current["dict_type"] != payload["dict_type"]:
                    cur.execute(
                        "UPDATE dtlms_dict_data SET dict_type = %s, updated_at = CURRENT_TIMESTAMP WHERE dict_type_id = %s AND is_deleted = FALSE",
                        (payload["dict_type"], dict_type_id),
                    )
                cur.execute("SELECT COUNT(*) AS count FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                count_row = cur.fetchone()
            conn.commit()
        return record | {"data_count": int(self._require_row(count_row, "update_dict_type_count")["count"])}

    def delete_dict_type(self, dict_type_id: int) -> None:
        """Execute query logic for `delete_dict_type`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                if not cur.fetchone():
                    raise KeyError(dict_type_id)
                cur.execute("SELECT COUNT(*) FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                if int(self._require_scalar_row(cur.fetchone(), "delete_dict_type_count")[0]) > 0:
                    raise ValueError("Dict type still has dict data")
                cur.execute("UPDATE dtlms_dict_types SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_type_id,))
            conn.commit()

    def create_dict_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `create_dict_data`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE",
                    (payload["dict_type"], payload["value"]),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                    ),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "create_dict_data"))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    def update_dict_data(self, dict_data_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `update_dict_data`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE AND id <> %s",
                    (payload["dict_type"], payload["value"], dict_data_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_data
                    SET dict_type_id = %s,
                        dict_type = %s,
                        label = %s,
                        value = %s,
                        sort_order = %s,
                        status = %s,
                        color_type = %s,
                        css_class = %s,
                        remark = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                        dict_data_id,
                    ),
                )
                record = self._normalize_dict_row(self._require_row(cur.fetchone(), "update_dict_data"))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    @staticmethod
    def _normalize_dict_row(row: dict[str, Any]) -> dict[str, Any]:
        """Execute query logic for `_normalize_dict_row`."""
        normalized: dict[str, Any] = {}
        for key, value in row.items():
            if isinstance(value, str):
                normalized[key] = value.strip()
            else:
                normalized[key] = value
        return normalized

    def delete_dict_data(self, dict_data_id: int) -> None:
        """Execute query logic for `delete_dict_data`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute("UPDATE dtlms_dict_data SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_data_id,))
            conn.commit()
