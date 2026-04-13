from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _install_principal_resolution(monkeypatch, token_subjects: dict[str, str], contexts: dict[str, dict[str, Any]]) -> None:
    def fake_decode_token(token: str) -> dict[str, str]:
        subject = token_subjects.get(token)
        if subject is None:
            raise AssertionError(f"Unexpected token: {token}")
        return {"sub": subject}

    def fake_get_user_principal_context(username: str) -> dict[str, Any]:
        return contexts[username]

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)


def _install_login_service(monkeypatch, token_subjects: dict[str, str], user_contexts: dict[str, dict[str, Any]]) -> None:
    def fake_authenticate_system_user(username: str, password: str) -> dict[str, Any] | None:
        if username == "admin" and password == "Admin@123456":
            return user_contexts[username]
        if username == "liu.ya" and password == "LiuYa@2026":
            return user_contexts[username]
        return None

    def fake_record_user_login(username: str) -> None:
        return None

    def fake_create_token_bundle(
        subject: str,
        roles: list[str],
        permissions: list[str],
        full_name: str | None = None,
    ) -> tuple[str, str]:
        access_token = f"token-{subject}"
        token_subjects[access_token] = subject
        return access_token, f"refresh-{subject}"

    monkeypatch.setattr("app.api.v1.auth.authenticate_system_user", fake_authenticate_system_user)
    monkeypatch.setattr("app.api.v1.auth.record_user_login", fake_record_user_login)
    monkeypatch.setattr("app.api.v1.auth.create_token_bundle", fake_create_token_bundle)


def _dashboard_payload() -> dict[str, list[dict[str, str | None]]]:
    metric = {
        "label": "总览",
        "value": "1",
        "target": "/dashboard",
        "trend": "+0%",
        "status": "正常",
    }
    return {
        "lifecycle_coverage": [metric],
        "recruitment_metrics": [metric],
        "training_metrics": [metric],
        "degree_metrics": [metric],
        "alerts": [{"level": "提示", "title": "流程正常", "owner": "系统", "due_text": "今日"}],
        "workflow_metrics": [metric],
    }


def _system_user_list_payload() -> dict[str, Any]:
    return {
        "total": 1,
        "page": 1,
        "page_size": 10,
        "items": [
            {
                "id": 1,
                "username": "admin",
                "full_name": "管理员",
                "role_code": "platform_admin",
                "role_name": "平台管理员",
                "department_name": "系统管理部",
                "phone_number": "13800000000",
                "account_status": "启用",
                "last_login_at": "2026-04-07 09:00:00",
            }
        ],
    }


def test_login_returns_tokens_for_valid_credentials(monkeypatch, client: TestClient) -> None:
    token_subjects: dict[str, str] = {}
    user_contexts = {
        "admin": {
            "username": "admin",
            "full_name": "管理员",
            "roles": ["platform_admin"],
            "permissions": ["*"],
        },
        "liu.ya": {
            "username": "liu.ya",
            "full_name": "刘亚",
            "roles": ["advisor"],
            "permissions": ["dashboard:read", "students:read", "training:read", "workflow:read"],
        },
    }

    _install_login_service(monkeypatch, token_subjects, user_contexts)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "Admin@123456"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token-admin"
    assert response.json()["refresh_token"] == "refresh-admin"
    assert response.json()["token_type"] == "bearer"


def test_login_rejects_invalid_credentials(monkeypatch, client: TestClient) -> None:
    token_subjects: dict[str, str] = {}
    user_contexts = {
        "admin": {
            "username": "admin",
            "full_name": "管理员",
            "roles": ["platform_admin"],
            "permissions": ["*"],
        },
    }

    _install_login_service(monkeypatch, token_subjects, user_contexts)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "WrongPassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_admin_can_access_me_dashboard_and_system_users_with_wildcard_permission(monkeypatch, client: TestClient) -> None:
    token_subjects: dict[str, str] = {}
    user_contexts = {
        "admin": {
            "username": "admin",
            "full_name": "管理员",
            "roles": ["platform_admin"],
            "permissions": ["*"],
        },
    }

    _install_login_service(monkeypatch, token_subjects, user_contexts)
    _install_principal_resolution(monkeypatch, token_subjects, user_contexts)
    monkeypatch.setattr("app.api.v1.dashboard.get_dashboard_overview", _dashboard_payload)
    monkeypatch.setattr("app.api.v1.system.get_system_user_list", lambda **kwargs: _system_user_list_payload())

    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "Admin@123456"},
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    me_response = client.get("/api/v1/auth/me", headers=headers)
    dashboard_response = client.get("/api/v1/dashboard/overview", headers=headers)
    system_users_response = client.get("/api/v1/system/users", headers=headers)

    assert me_response.status_code == 200
    assert me_response.json()["permissions"] == ["*"]
    assert dashboard_response.status_code == 200
    assert dashboard_response.json()["alerts"][0]["title"] == "流程正常"
    assert system_users_response.status_code == 200
    assert system_users_response.json()["items"][0]["username"] == "admin"


def test_advisor_can_access_dashboard_but_is_forbidden_from_system_users(monkeypatch, client: TestClient) -> None:
    token_subjects: dict[str, str] = {}
    user_contexts = {
        "liu.ya": {
            "username": "liu.ya",
            "full_name": "刘亚",
            "roles": ["advisor"],
            "permissions": ["dashboard:read", "students:read", "training:read", "workflow:read"],
        },
    }

    _install_login_service(monkeypatch, token_subjects, user_contexts)
    _install_principal_resolution(monkeypatch, token_subjects, user_contexts)
    monkeypatch.setattr("app.api.v1.dashboard.get_dashboard_overview", _dashboard_payload)
    monkeypatch.setattr("app.api.v1.system.get_system_user_list", lambda **kwargs: _system_user_list_payload())

    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "liu.ya", "password": "LiuYa@2026"},
    )
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    me_response = client.get("/api/v1/auth/me", headers=headers)
    dashboard_response = client.get("/api/v1/dashboard/overview", headers=headers)
    system_users_response = client.get("/api/v1/system/users", headers=headers)

    assert me_response.status_code == 200
    assert me_response.json()["permissions"] == ["dashboard:read", "students:read", "training:read", "workflow:read"]
    assert dashboard_response.status_code == 200
    assert system_users_response.status_code == 403
    assert system_users_response.json()["detail"] == "Missing permissions: system:read"