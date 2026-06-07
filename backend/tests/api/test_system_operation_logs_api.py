from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _install_principal_resolution(monkeypatch, token: str = "token-auditor") -> str:
    def fake_decode_token(current_token: str) -> dict[str, str]:
        if current_token != token:
            raise AssertionError(f"Unexpected token: {current_token}")
        return {"sub": "auditor"}

    def fake_get_user_principal_context(username: str) -> dict[str, Any]:
        assert username == "auditor"
        return {
            "username": "auditor",
            "full_name": "审计员",
            "roles": ["platform_admin"],
            "permissions": ["audit:read"],
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)
    return token


def test_operation_logs_defaults_to_management_scope(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch)
    captured: dict[str, Any] = {}

    def fake_get_operation_log_list(
        keyword: str | None = None,
        module_name: str | None = None,
        log_scope: str = "management",
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        captured.update(
            {
                "keyword": keyword,
                "module_name": module_name,
                "log_scope": log_scope,
                "result": result,
                "page": page,
                "page_size": page_size,
            }
        )
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
        }

    monkeypatch.setattr("app.api.v1.system.get_operation_log_list", fake_get_operation_log_list)

    response = client.get(
        "/api/v1/system/operation-logs",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert captured["log_scope"] == "management"


def test_operation_logs_accepts_portal_scope(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch)
    captured: dict[str, Any] = {}

    def fake_get_operation_log_list(
        keyword: str | None = None,
        module_name: str | None = None,
        log_scope: str = "management",
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        captured["log_scope"] = log_scope
        return {
            "items": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
        }

    monkeypatch.setattr("app.api.v1.system.get_operation_log_list", fake_get_operation_log_list)

    response = client.get(
        "/api/v1/system/operation-logs",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"log_scope": "portal"},
    )

    assert response.status_code == 200
    assert captured["log_scope"] == "portal"
