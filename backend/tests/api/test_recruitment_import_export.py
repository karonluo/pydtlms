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
            "full_name": "测试用户",
            "roles": ["recruitment_admin"],
            "permissions": permissions,
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)
    return access_token


def test_import_recruitment_applications_endpoint_returns_import_result(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:write"])

    monkeypatch.setattr(
        "app.api.v1.recruitment.parse_recruitment_template",
        lambda file_bytes: [{"student_name": "张三", "first_choice": "人工智能", "material_status": "材料齐全"}],
    )
    monkeypatch.setattr(
        "app.api.v1.recruitment.import_recruitment_applications",
        lambda plan_id, rows, principal: {
            "imported_count": 1,
            "skipped_count": 0,
            "plan_id": plan_id,
            "imported_business_keys": ["ZSLQSP202604100001"],
            "issues": [],
        },
    )

    response = client.post(
        "/api/v1/recruitment/applications/import",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": ("资料审核名单.xlsx", b"fake-bytes", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"plan_id": "5"},
    )

    assert response.status_code == 200
    assert response.json()["imported_count"] == 1
    assert response.json()["plan_id"] == 5
    assert response.json()["imported_business_keys"] == ["ZSLQSP202604100001"]


def test_export_recruitment_applications_endpoint_returns_excel_stream(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:read"])
    monkeypatch.setattr("app.api.v1.recruitment.export_recruitment_applications", lambda **kwargs: b"xlsx-content")

    response = client.get(
        "/api/v1/recruitment/applications/export",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"keyword": "张三", "plan_id": 3, "status": "报名已提交"},
    )

    assert response.status_code == 200
    assert response.content == b"xlsx-content"
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert "attachment; filename*=UTF-8''" in response.headers["content-disposition"]


def test_download_recruitment_application_template_returns_blank_excel(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:read"])
    monkeypatch.setattr("app.api.v1.recruitment.export_recruitment_application_blank_template", lambda: b"blank-template")

    response = client.get(
        "/api/v1/recruitment/applications/template",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.content == b"blank-template"
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert "attachment; filename*=UTF-8''" in response.headers["content-disposition"]


def test_delete_recruitment_plan_endpoint_returns_no_content(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:write"])
    deleted_plan_ids: list[int] = []

    def fake_delete_recruitment_plan(plan_id: int) -> None:
        deleted_plan_ids.append(plan_id)

    monkeypatch.setattr("app.api.v1.recruitment.delete_recruitment_plan", fake_delete_recruitment_plan)

    response = client.delete(
        "/api/v1/recruitment/plans/9",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert deleted_plan_ids == [9]


def test_delete_recruitment_plan_endpoint_returns_bad_request_when_plan_has_applications(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:write"])

    def fake_delete_recruitment_plan(plan_id: int) -> None:
        raise ValueError(f"计划 {plan_id} 下仍有报名申请，不能删除")

    monkeypatch.setattr("app.api.v1.recruitment.delete_recruitment_plan", fake_delete_recruitment_plan)

    response = client.delete(
        "/api/v1/recruitment/plans/9",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "计划 9 下仍有报名申请，不能删除"