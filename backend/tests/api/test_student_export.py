from datetime import datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.news import NewsArticleRecord
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


def test_registered_portal_students_list_endpoint_accepts_multiple_advisor_names(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    captured: dict[str, Any] = {}

    def fake_get_registered_portal_student_list(**kwargs):
        captured.update(kwargs)
        return {
            "items": [],
            "total": 0,
            "page": kwargs.get("page", 1),
            "page_size": kwargs.get("page_size", 10),
        }

    monkeypatch.setattr("app.api.v1.students.get_registered_portal_student_list", fake_get_registered_portal_student_list)

    response = client.get(
        "/api/v1/students/portal-registrations",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "keyword": "张三",
            "application_form_status": "已填写报名",
            "recruitment_application_status": "待初筛确认",
            "advisor_names": "刘亚,何琳",
            "page": 1,
            "page_size": 10,
        },
    )

    assert response.status_code == 200
    assert captured["advisor_names"] == ["刘亚", "何琳"]
    assert captured["recruitment_application_status"] == "待初筛确认"


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


def test_create_registered_portal_student_export_job_endpoint_uses_business_audit_summary(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["students:read"])
    monkeypatch.setattr(
        "app.api.v1.students.create_registered_portal_student_export_job",
        lambda payload, principal: RegisteredPortalStudentExportJobCreateResponse(
            message="开始导出，请等待完成",
            job=RegisteredPortalStudentExportJobRecord(
                job_id="job-2",
                status="pending",
                file_name="注册学生导出_20260514153000.xlsx",
                created_at="2026-05-14 15:30:00",
                is_read=True,
            ),
        ),
    )
    captured: dict[str, Any] = {}

    def capture_audit(module_name, entity_name, entity_id, action, summary, **kwargs):
        captured.update(
            {
                "module_name": module_name,
                "entity_name": entity_name,
                "entity_id": entity_id,
                "action": action,
                "summary": summary,
                **kwargs,
            }
        )
        return {
            "module_name": module_name,
            "entity_name": entity_name,
            "entity_id": entity_id,
            "action": action,
            "summary": summary,
            **kwargs,
        }

    monkeypatch.setattr("app.main.store.record_operation_event", capture_audit)

    response = client.post(
        "/api/v1/students/portal-registrations/export-jobs",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"ids": [11, 12]},
    )

    assert response.status_code == 200
    assert captured["summary"] == "导出注册学生"
    assert captured["action"] == "导出"
    assert captured["entity_name"] == "注册学生"


def test_publish_news_endpoint_uses_business_audit_summary(monkeypatch, client: TestClient) -> None:
    access_token = _install_principal_resolution(monkeypatch, "news-admin", ["recruitment:write"])
    monkeypatch.setattr(
        "app.api.v1.news.publish_news_article",
        lambda news_article_id, principal: NewsArticleRecord(
            id=news_article_id,
            news_code="NEWS202606070001",
            news_title="示例新闻",
            news_content="示例内容",
            news_type="通知",
            publisher_user_id=1,
            publisher_username="news-admin",
            publisher_name="测试用户",
            reviewer_user_id=None,
            reviewer_username=None,
            reviewer_name=None,
            published_at=datetime(2026, 6, 7, 12, 0, 0),
            status="已发布",
            is_pinned=False,
            display_order=0,
            created_at=datetime(2026, 6, 7, 11, 59, 0),
            updated_at=datetime(2026, 6, 7, 12, 0, 0),
        ),
    )
    captured: dict[str, Any] = {}

    def capture_audit(module_name, entity_name, entity_id, action, summary, **kwargs):
        captured.update(
            {
                "module_name": module_name,
                "entity_name": entity_name,
                "entity_id": entity_id,
                "action": action,
                "summary": summary,
                **kwargs,
            }
        )
        return {
            "module_name": module_name,
            "entity_name": entity_name,
            "entity_id": entity_id,
            "action": action,
            "summary": summary,
            **kwargs,
        }

    monkeypatch.setattr("app.main.store.record_operation_event", capture_audit)

    response = client.post(
        "/api/v1/recruitment/news/1/publish",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert captured["summary"] == "发布新闻"
    assert captured["action"] == "发布"
    assert captured["entity_name"] == "新闻"
    assert captured["entity_id"] == "1"


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