from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _install_principal_resolution(monkeypatch, subject: str, permissions: list[str]) -> str:
    access_token = f"token-{subject}"

    def fake_decode_token(token: str) -> dict[str, str]:
        if token != access_token:
            raise AssertionError(f"Unexpected token: {token}")
        return {"sub": subject}

    def fake_get_user_principal_context(username: str) -> dict[str, Any]:
        assert username == subject
        return {
            "username": subject,
            "full_name": "系统管理员",
            "roles": ["platform_admin"],
            "permissions": permissions,
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)
    return access_token


def test_parse_system_user_import_file_endpoint_returns_rows(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "admin", ["system:write"])

    monkeypatch.setattr(
        "app.api.v1.system.parse_system_user_import_template",
        lambda file_bytes: [
            {
                "row_number": 2,
                "username": "zhangsan",
                "full_name": "张三",
                "role_code": "advisor",
                "account_status": "启用",
            }
        ],
    )

    response = client.post(
        "/api/v1/system/users/import/parse",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("系统用户导入模板.xlsx", b"fake-bytes", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_count"] == 1
    assert payload["rows"][0]["row_number"] == 2
    assert payload["rows"][0]["username"] == "zhangsan"


def test_import_system_user_rows_endpoint_returns_import_result(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "admin", ["system:write"])
    captured: dict[str, Any] = {}

    def fake_import_system_users(rows: list[dict[str, Any]], operator_username: str = "admin") -> dict[str, Any]:
        captured["rows"] = rows
        captured["operator_username"] = operator_username
        return {
            "total_count": len(rows),
            "success_count": len(rows),
            "created_count": 1,
            "updated_count": 0,
            "failed_count": 0,
            "issues": [],
            "message": "全部成功",
        }

    monkeypatch.setattr("app.api.v1.system.import_system_users", fake_import_system_users)

    response = client.post(
        "/api/v1/system/users/import/batch",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "rows": [
                {
                    "row_number": 2,
                    "username": None,
                    "full_name": "李四",
                    "role_code": "advisor",
                    "account_status": "启用",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "全部成功"
    assert captured["operator_username"] == "admin"
    assert captured["rows"][0]["full_name"] == "李四"