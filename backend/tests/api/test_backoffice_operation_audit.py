from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.management_service import store as management_store


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _install_management_principal(monkeypatch, token: str = "token-admin") -> str:
    def fake_rbac_decode_token(current_token: str) -> dict[str, str]:
        if current_token != token:
            raise AssertionError(f"Unexpected token: {current_token}")
        return {"sub": "admin"}

    def fake_security_decode_token(current_token: str) -> dict[str, str]:
        if current_token != token:
            raise AssertionError(f"Unexpected token: {current_token}")
        return {"sub": "admin"}

    def fake_get_user_principal_context(username: str) -> dict[str, Any]:
        assert username == "admin"
        return {
            "username": "admin",
            "full_name": "管理员",
            "roles": ["platform_admin"],
            "permissions": ["system:write"],
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_rbac_decode_token)
    monkeypatch.setattr("app.main.decode_token", fake_security_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)
    return token


def test_backoffice_write_request_records_operation_log(monkeypatch, client: TestClient) -> None:
    token = _install_management_principal(monkeypatch)
    captured: dict[str, Any] = {}

    def fake_update_dict_type(dict_type_id: int, payload: Any) -> dict[str, Any]:
        assert dict_type_id == 1
        return {
            "id": dict_type_id,
            "dict_name": payload.dict_name,
            "dict_type": payload.dict_type,
            "status": payload.status,
            "remark": payload.remark,
            "data_count": 0,
        }

    def fake_record_operation_event(
        module_name: str,
        entity_name: str,
        entity_id: str,
        action: str,
        summary: str,
        operator_username: str = "admin",
        *,
        result: str = "success",
    ) -> dict[str, Any]:
        captured.update(
            {
                "module_name": module_name,
                "entity_name": entity_name,
                "entity_id": entity_id,
                "action": action,
                "summary": summary,
                "operator_username": operator_username,
                "result": result,
            }
        )
        return captured

    monkeypatch.setattr("app.api.v1.system.update_dict_type", fake_update_dict_type)
    monkeypatch.setattr("app.main.store.record_operation_event", fake_record_operation_event)

    response = client.put(
        "/api/v1/system/dict-types/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "dict_name": "测试字典",
            "dict_type": "test_dict",
            "status": "启用",
            "remark": "用于审计测试",
        },
    )

    assert response.status_code == 200
    assert captured["module_name"] == "系统治理"
    assert captured["entity_name"] == "dict-types"
    assert captured["entity_id"] == "1"
    assert captured["action"] == "编辑"
    assert captured["operator_username"] == "admin"
    assert captured["result"] == "success"
    assert "PUT /api/v1/system/dict-types/1" in captured["summary"]


def test_auth_post_request_is_excluded_from_backoffice_audit(monkeypatch, client: TestClient) -> None:
    called = {"value": False}

    def fake_authenticate_system_user(username: str, password: str) -> dict[str, Any] | None:
        if username == "admin" and password == "Admin@123456":
            return {
                "username": "admin",
                "full_name": "管理员",
                "roles": ["platform_admin"],
                "permissions": ["*"],
            }
        return None

    def fake_record_user_login(username: str) -> None:
        return None

    def fake_create_token_bundle(subject: str, roles: list[str], permissions: list[str], full_name: str | None = None) -> tuple[str, str]:
        return "token-admin", "refresh-admin"

    def fake_record_operation_event(*args, **kwargs):
        called["value"] = True
        return {}

    monkeypatch.setattr("app.api.v1.auth.authenticate_system_user", fake_authenticate_system_user)
    monkeypatch.setattr("app.api.v1.auth.record_user_login", fake_record_user_login)
    monkeypatch.setattr("app.api.v1.auth.create_token_bundle", fake_create_token_bundle)
    monkeypatch.setattr("app.main.store.record_operation_event", fake_record_operation_event)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "Admin@123456"},
    )

    assert response.status_code == 200
    assert called["value"] is False


def test_backoffice_write_request_keeps_single_log_when_manual_log_exists(monkeypatch, client: TestClient) -> None:
    token = _install_management_principal(monkeypatch)
    call_count = {"count": 0}

    def fake_update_dict_type(dict_type_id: int, payload: Any) -> dict[str, Any]:
        del payload
        management_store._record_operation(
            "系统治理",
            "字典类型",
            str(dict_type_id),
            "编辑",
            "手工业务日志",
            operator_username="admin",
            result="success",
        )
        return {
            "id": dict_type_id,
            "dict_name": "测试字典",
            "dict_type": "test_dict",
            "status": "启用",
            "remark": "用于审计测试",
            "data_count": 0,
        }

    def fake_record_operation_event(*args, **kwargs):
        call_count["count"] += 1
        return {}

    monkeypatch.setattr("app.api.v1.system.update_dict_type", fake_update_dict_type)
    monkeypatch.setattr("app.main.store.record_operation_event", fake_record_operation_event)

    response = client.put(
        "/api/v1/system/dict-types/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "dict_name": "测试字典",
            "dict_type": "test_dict",
            "status": "启用",
            "remark": "用于审计测试",
        },
    )

    assert response.status_code == 200
    assert call_count["count"] == 0
