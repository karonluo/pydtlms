from typing import Any

from fastapi.testclient import TestClient

from app.main import app



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



def test_registered_portal_student_advisor_choices_endpoint_uses_linked_application(monkeypatch) -> None:
    access_token = _install_principal_resolution(monkeypatch, "student-admin", ["recruitment_registered_students:write"])
    captured: dict[str, Any] = {}

    def fake_get_registered_portal_student_detail(student_id: int):
        assert student_id == 27
        return {
            "id": 27,
            "recruitment_application_id": 88,
        }

    def fake_get_recruitment_application_detail(application_id: int):
        assert application_id == 88
        return {"id": 88}

    def fake_update_recruitment_application_advisor_choices(application_id: int, **kwargs):
        captured.update({"application_id": application_id, **kwargs})
        return {
            "id": application_id,
            "plan_id": 3,
            "business_key": "SH20260001",
            "portal_student_id": 27,
            "student_name": "罗凯",
            "graduation_school": "江南大学",
            "highest_degree": "硕士",
            "intended_field": "智能制造",
            "material_status": "已提交",
            "application_status": "待导师初筛-第一志愿",
        }

    monkeypatch.setattr("app.api.v1.students.get_registered_portal_student_detail", fake_get_registered_portal_student_detail)
    monkeypatch.setattr("app.api.v1.students.get_recruitment_application_detail", fake_get_recruitment_application_detail)
    monkeypatch.setattr("app.api.v1.students.update_recruitment_application_advisor_choices", fake_update_recruitment_application_advisor_choices)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/students/portal-registrations/27/advisor-choices",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "first_choice": "周伯文（1001）",
                "first_choice_id": 1001,
                "second_choice": "丁宁（1002）",
                "second_choice_id": 1002,
            },
        )

    assert response.status_code == 200
    assert captured["application_id"] == 88
    assert captured["first_choice_id"] == 1001
    assert captured["second_choice_id"] == 1002
