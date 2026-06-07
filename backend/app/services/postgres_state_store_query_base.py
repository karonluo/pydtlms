"""Base PostgreSQL query helpers shared by all query mixins.

This module contains low-level helpers that are reused across the feature
specific query mixins.
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

class PostgresStateStoreQueryBaseMixin:
    """Query mixin extracted by functional module."""

    if TYPE_CHECKING:
        def ensure_schema(self) -> None:
            """Ensure PostgreSQL schema and migrations are available."""
            ...

        def _connect(self, database_name: str, autocommit: bool = False) -> psycopg.Connection[Any]:
            """Return a PostgreSQL connection for the given database."""
            ...

        def __getattr__(self, name: str) -> Any:
            """Resolve attributes from composed mixins at runtime."""
            ...

    @staticmethod
    def _resolve_attachment_name(
        attachment_rows: list[dict[str, Any]],
        owner_type: str,
        owner_id: int | None,
        category: str,
        fallback_url: str | None = None,
    ) -> str | None:
        """Execute query logic for `_resolve_attachment_name`."""
        for item in attachment_rows:
            if str(item.get("owner_type") or "") != owner_type:
                continue
            if str(item.get("attachment_category") or "") != category:
                continue
            current_owner_id = item.get("owner_id")
            if owner_id is not None and int(current_owner_id or 0) != int(owner_id):
                continue
            file_name = str(item.get("file_name") or "").strip()
            if file_name:
                return file_name
        if fallback_url:
            return Path(str(fallback_url)).name or None
        return None

    @staticmethod
    def _execute_dynamic(
        cur: psycopg.Cursor[Any],
        query: str,
        params: Any | None = None,
    ) -> None:
        """Execute query logic for `_execute_dynamic`."""
        cur.execute(cast(Any, query), params)

    @staticmethod
    def _require_row(row: Any, context: str) -> dict[str, Any]:
        """Execute query logic for `_require_row`."""
        if row is None:
            raise RuntimeError(f"Expected row for {context}")
        return dict(cast(dict[str, Any], row))

    @staticmethod
    def _require_scalar_row(row: Any, context: str) -> Any:
        """Execute query logic for `_require_scalar_row`."""
        if row is None:
            raise RuntimeError(f"Expected row for {context}")
        return row

    @staticmethod
    def _principal_field_value(principal: Any | None, field_name: str) -> Any:
        """Execute query logic for `_principal_field_value`."""
        if principal is None:
            return None
        if isinstance(principal, dict):
            return principal.get(field_name)
        return getattr(principal, field_name, None)

    @classmethod
    def _principal_role_codes(cls, principal: Any | None) -> set[str]:
        """Execute query logic for `_principal_role_codes`."""
        raw_roles = cls._principal_field_value(principal, "roles") or []
        return {str(item).strip() for item in raw_roles if str(item).strip()}

    @classmethod
    def _needs_center_scope_filter(cls, principal: Any | None) -> bool:
        """Execute query logic for `_needs_center_scope_filter`."""
        role_codes = cls._principal_role_codes(principal)
        if not role_codes:
            return False
        if role_codes.intersection({"platform_admin", "AILABMGT", "academy_admin"}):
            return False
        return "advisor" in role_codes
