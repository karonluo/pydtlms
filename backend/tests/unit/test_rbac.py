import pytest
from fastapi import HTTPException

from app.core.rbac import require_permissions
from app.schemas.auth import Principal


def build_principal(permissions: list[str]) -> Principal:
    return Principal(
        username="admin",
        full_name="管理员",
        roles=["platform_admin"],
        permissions=permissions,
    )


def test_require_permissions_allows_super_admin_wildcard() -> None:
    principal = build_principal(["*"])

    dependency = require_permissions("dashboard:view")

    assert dependency(principal) is principal


def test_require_permissions_rejects_missing_permission() -> None:
    principal = build_principal(["students:view"])
    dependency = require_permissions("dashboard:view")

    with pytest.raises(HTTPException) as exc_info:
        dependency(principal)

    assert exc_info.value.status_code == 403
    assert "dashboard:view" in str(exc_info.value.detail)