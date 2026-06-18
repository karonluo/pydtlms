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


def test_create_advisor_screening_export_job_preserves_requested_scope(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "advisor.liu", ["recruitment_advisor_screening:read"])

    captured: dict[str, object] = {}

    def fake_create_registered_portal_student_export_job(payload, principal):
        captured["payload"] = payload.model_dump(mode="python")
        captured["principal_username"] = principal.username
        return {
            "message": "开始导出，请等待完成",
            "job": {
                "job_id": "job-1",
                "status": "pending",
                "file_name": "导师初筛导出.xlsx",
                "created_at": "2026-06-16T00:00:00",
                "started_at": None,
                "completed_at": None,
                "failed_at": None,
                "error_message": None,
                "download_url": None,
                "is_read": True,
            },
        }

    monkeypatch.setattr("app.api.v1.recruitment.create_registered_portal_student_export_job", fake_create_registered_portal_student_export_job)

    response = client.post(
        "/api/v1/recruitment/advisor-screening/export-jobs",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "ids": [1, 2],
            "keyword": "张",
            "advisor_names": [],
            "first_choice_advisor_names": [],
            "second_choice_advisor_names": [],
            "export_scope": "advisor_screening_submitted",
        },
    )

    assert response.status_code == 200
    assert captured["principal_username"] == "advisor.liu"
    assert captured["payload"]["ids"] == []
    assert captured["payload"]["keyword"] == "张"
    assert captured["payload"]["export_scope"] == "advisor_screening_submitted"


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


def test_initial_screening_confirmation_applications_endpoint_uses_dedicated_query(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "recruiter", ["recruitment:read"])

    captured_kwargs: dict[str, object] = {}

    def fake_list_initial_screening_confirmation_applications(**kwargs):
        captured_kwargs.update(kwargs)
        return {
            "items": [],
            "total": 0,
            "page": kwargs["page"],
            "page_size": kwargs["page_size"],
        }

    monkeypatch.setattr("app.api.v1.recruitment.list_initial_screening_confirmation_applications", fake_list_initial_screening_confirmation_applications)

    response = client.get(
        "/api/v1/recruitment/applications/initial-screening-confirmation",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"keyword": "SH2026", "plan_id": 5, "advisor_names": "刘亚,王强", "page": 2, "page_size": 20},
    )

    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert captured_kwargs == {
        "keyword": "SH2026",
        "plan_id": 5,
        "advisor_names": ["刘亚", "王强"],
        "page": 2,
        "page_size": 20,
    }


def test_rescore_advisor_screening_submitted_endpoint_delegates_to_service(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "advisor.liu", ["recruitment_advisor_screening:write"])

    captured: dict[str, object] = {}

    def fake_rescore_advisor_screening_submitted_application(application_id: int, principal):
        captured["application_id"] = application_id
        captured["principal_username"] = principal.username
        return {
            "id": application_id,
            "plan_id": 5,
            "business_key": "SH202605010001",
            "student_name": "测试学生",
            "material_status": "材料齐全",
            "application_status": "待导师初筛-第一志愿",
            "graduation_school": "东南大学",
            "highest_degree": "硕士",
            "intended_field": "人工智能",
        }

    monkeypatch.setattr("app.api.v1.recruitment.rescore_advisor_screening_submitted_application", fake_rescore_advisor_screening_submitted_application)

    response = client.post(
        "/api/v1/recruitment/applications/advisor-screening-submitted/123/rescore",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["application_status"] == "待导师初筛-第一志愿"
    assert captured == {"application_id": 123, "principal_username": "advisor.liu"}


def test_rescore_advisor_screening_submitted_endpoint_returns_bad_request_for_interview_stage(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "advisor.liu", ["recruitment_advisor_screening:write"])

    def fake_rescore_advisor_screening_submitted_application(application_id: int, principal):
        del application_id, principal
        raise ValueError("因为该学生已经到了面试阶段所以无法重新评分")

    monkeypatch.setattr("app.api.v1.recruitment.rescore_advisor_screening_submitted_application", fake_rescore_advisor_screening_submitted_application)

    response = client.post(
        "/api/v1/recruitment/applications/advisor-screening-submitted/123/rescore",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "因为该学生已经到了面试阶段所以无法重新评分"


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