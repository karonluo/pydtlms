from pathlib import Path
from typing import Any

import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi.testclient import TestClient

from app.main import app



def install_principal_resolution(subject: str, permissions: list[str]) -> str:
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
            "roles": ["AILABMGT"],
            "permissions": permissions,
        }

    from app.core import rbac

    rbac.decode_token = fake_decode_token
    rbac.get_user_principal_context = fake_get_user_principal_context
    return access_token



def main() -> None:
    access_token = install_principal_resolution("academy-admin", ["recruitment_registered_students:write"])
    captured: dict[str, Any] = {}

    def fake_get_registered_portal_student_detail(student_id: int):
        print(f"student detail lookup: {student_id}")
        return {
            "id": 27,
            "recruitment_application_id": 88,
        }

    def fake_get_recruitment_application_detail(application_id: int):
        print(f"application detail lookup: {application_id}")
        return {
            "id": 88,
            "plan_id": 3,
            "business_key": "SH20260001",
            "portal_student_id": 27,
            "student_name": "罗凯",
            "graduation_school": "江南大学",
            "highest_degree": "硕士",
            "intended_field": "智能制造",
            "material_status": "已提交",
            "application_status": "待导师初筛-第一志愿",
            "first_choice": "周伯文（1001）",
            "second_choice": "丁宁（1002）",
            "first_choice_id": 1001,
            "second_choice_id": 1002,
        }

    def fake_update_recruitment_application_advisor_choices(application_id: int, **kwargs):
        print(f"advisor update application_id={application_id} payload={kwargs}")
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

    import app.services.dashboard_service as dashboard_service

    dashboard_service.get_registered_portal_student_detail = fake_get_registered_portal_student_detail
    dashboard_service.get_recruitment_application_detail = fake_get_recruitment_application_detail
    dashboard_service.update_recruitment_application_advisor_choices = fake_update_recruitment_application_advisor_choices

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

    print("status:", response.status_code)
    print("response:", response.json())
    print("captured:", captured)
    if response.status_code != 200:
        raise SystemExit(1)
    if captured.get("application_id") != 88:
        raise SystemExit(2)
    if captured.get("first_choice_id") != 1001:
        raise SystemExit(3)
    if captured.get("second_choice_id") != 1002:
        raise SystemExit(4)


if __name__ == "__main__":
    main()
