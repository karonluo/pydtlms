from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.student import (
    RegisteredPortalStudentExportJobCreateResponse,
    RegisteredPortalStudentExportJobListResponse,
    RegisteredPortalStudentExportJobRecord,
)


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
            "roles": ["student_admin"],
            "permissions": permissions,
        }

    monkeypatch.setattr("app.core.rbac.decode_token", fake_decode_token)
    monkeypatch.setattr("app.core.rbac.get_user_principal_context", fake_get_user_principal_context)
    return access_token


def test_export_registered_portal_students_endpoint_returns_excel_stream(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    monkeypatch.setattr(
        "app.api.v1.students.export_registered_portal_students",
        lambda ids, **kwargs: b"portal-students-xlsx",
    )

    response = client.post(
        "/api/v1/students/portal-registrations/export",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"ids": [11, 12]},
    )

    assert response.status_code == 200
    assert response.content == b"portal-students-xlsx"
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert "attachment; filename*=UTF-8''" in response.headers["content-disposition"]


def test_create_registered_portal_student_export_job_endpoint_returns_job(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    monkeypatch.setattr(
        "app.api.v1.students.create_registered_portal_student_export_job",
        lambda payload, principal: RegisteredPortalStudentExportJobCreateResponse(
            message="开始导出，请等待完成",
            job=RegisteredPortalStudentExportJobRecord(
                job_id="job-1",
                status="pending",
                file_name="注册学生导出_20260514153000.xlsx",
                created_at="2026-05-14 15:30:00",
                is_read=True,
            ),
        ),
    )

    response = client.post(
        "/api/v1/students/portal-registrations/export-jobs",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"ids": [11, 12]},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "开始导出，请等待完成"
    assert response.json()["job"]["job_id"] == "job-1"


def test_list_registered_portal_student_export_jobs_endpoint_returns_jobs(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    monkeypatch.setattr(
        "app.api.v1.students.list_registered_portal_student_export_jobs",
        lambda principal: RegisteredPortalStudentExportJobListResponse(
            items=[
                RegisteredPortalStudentExportJobRecord(
                    job_id="job-1",
                    status="completed",
                    file_name="注册学生导出_20260514153000.xlsx",
                    created_at="2026-05-14 15:30:00",
                    completed_at="2026-05-14 15:31:10",
                    download_url="/api/v1/students/portal-registrations/export-jobs/job-1/download",
                    is_read=False,
                )
            ],
            unread_count=1,
        ),
    )

    response = client.get(
        "/api/v1/students/portal-registrations/export-jobs",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["unread_count"] == 1
    assert response.json()["items"][0]["status"] == "completed"


def test_download_registered_portal_student_export_job_returns_excel_stream(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    monkeypatch.setattr(
        "app.api.v1.students.get_registered_portal_student_export_job_download",
        lambda job_id, principal: ("注册学生导出_20260514153000.xlsx", b"portal-export-job-xlsx"),
    )

    response = client.get(
        "/api/v1/students/portal-registrations/export-jobs/job-1/download",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.content == b"portal-export-job-xlsx"
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def test_mark_registered_portal_student_export_jobs_read_returns_no_content(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    called = {"value": False}

    def fake_mark(principal) -> None:
        called["value"] = True

    monkeypatch.setattr("app.api.v1.students.mark_registered_portal_student_export_jobs_read", fake_mark)

    response = client.post(
        "/api/v1/students/portal-registrations/export-jobs/read",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
    assert called["value"] is True