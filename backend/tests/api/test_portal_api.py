from fastapi.testclient import TestClient

from app.main import app
from app.schemas.portal import PortalRegistrationResponse, PortalStudentRecord


def _portal_student_payload(student_id: int = 7) -> dict[str, object]:
    return {
        'id': student_id,
        'full_name': '张三',
        'phone_number': '13800001111',
        'email': 'zhangsan@example.com',
        'id_number': '320000199901011234',
        'graduation_school': '江南大学',
        'highest_degree': '硕士',
        'intended_field': '智能制造',
        'political_status': '中共党员',
        'selected_plan_id': 3,
        'selected_team_name': '智能制造联合团队',
        'selected_advisor_name': '刘亚',
        'self_evaluation': '具备算法与控制方向研究基础',
        'submitted_at': '2026-04-13 10:00:00',
    }


def _portal_student_record(student_id: int = 7) -> PortalStudentRecord:
    return PortalStudentRecord(**_portal_student_payload(student_id))


def test_portal_register_returns_profile(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr(
            'app.api.v1.portal.register_portal_student',
            lambda payload: PortalRegistrationResponse(message='注册成功，请登录后继续填写申请表', student=_portal_student_record()),
        )

        response = client.post(
            '/api/v1/portal/register',
            json={
                'phone_number': '13800001111',
                'email': 'zhangsan@example.com',
                'full_name': '张三',
                'id_number': '320000199901011234',
                'password': 'Secret123!',
            },
        )

        assert response.status_code == 201
        payload = response.json()
        assert payload['message'] == '注册成功，请登录后继续填写申请表'
        assert payload['student']['full_name'] == '张三'
        assert payload['student']['selected_team_name'] == '智能制造联合团队'


def test_portal_login_returns_session(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.login_portal_student', lambda payload: _portal_student_record())
        monkeypatch.setattr('app.api.v1.portal.create_portal_access_token', lambda student_id, full_name: f'portal-{student_id}')

        response = client.post(
            '/api/v1/portal/login',
            json={
                'account': '13800001111',
                'password': 'Secret123!',
            },
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['access_token'] == 'portal-7'
        assert payload['token_type'] == 'bearer'
        assert payload['student']['id'] == 7


def test_portal_forgot_password_returns_message(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.reset_portal_student_password', lambda payload: None)

        response = client.post(
            '/api/v1/portal/forgot-password',
            json={
                'account': 'zhangsan@example.com',
                'id_number': '320000199901011234',
                'new_password': 'NewSecret123!',
            },
        )

        assert response.status_code == 200
        assert response.json()['message'] == '密码已重置，请重新登录'


def test_portal_me_returns_profile(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.get_portal_student', lambda student_id: _portal_student_record(student_id))

        response = client.get('/api/v1/portal/me', headers={'Authorization': 'Bearer portal-token'})

        assert response.status_code == 200
        assert response.json()['id'] == 7
        assert response.json()['graduation_school'] == '江南大学'


def test_portal_plans_and_teams_require_auth_and_return_data(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr(
            'app.api.v1.portal.get_public_recruitment_plans',
            lambda: {
                'items': [
                    {
                        'id': 3,
                        'plan_name': '2026 秋季博士招生',
                        'academic_term': '2026-秋',
                        'current_stage': '报名配置',
                        'target_quota': 30,
                        'interview_group_count': 3,
                        'brochure_image_url': '/portal-brochures/uploads/plan-3.png',
                        'summary': '聚焦人工智能基础模型与交叉应用',
                    }
                ]
            },
        )
        monkeypatch.setattr(
            'app.api.v1.portal.get_public_teams',
            lambda: {
                'items': [
                    {
                        'id': 8,
                        'team_name': '智能制造联合团队',
                        'lead_advisor_name': '刘亚',
                        'advisor_names': ['刘亚', '徐素天'],
                        'department_name': '智能系统中心',
                        'discipline_name': '控制科学与工程',
                        'research_directions': ['智能制造', '工业视觉'],
                        'description': '围绕智能工厂与工业大模型开展招生',
                    }
                ]
            },
        )

        plans_response = client.get('/api/v1/portal/plans', headers={'Authorization': 'Bearer portal-token'})
        teams_response = client.get('/api/v1/portal/teams', headers={'Authorization': 'Bearer portal-token'})

        assert plans_response.status_code == 200
        assert teams_response.status_code == 200
        assert plans_response.json()['items'][0]['brochure_image_url'] == '/portal-brochures/uploads/plan-3.png'
        assert teams_response.json()['items'][0]['team_name'] == '智能制造联合团队'


def test_portal_application_submission_returns_business_key(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr(
            'app.api.v1.portal.submit_portal_application',
            lambda student_id, payload: {
                'student': _portal_student_payload(student_id),
                'application_business_key': 'RECRUIT-20260413-0007',
                'application_status': '报名已提交',
            },
        )

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'gender': '男',
                'birth_date': '1999-01-01',
                'native_place': '江苏无锡',
                'graduation_school': '江南大学',
                'highest_degree': '硕士',
                'intended_field': '智能制造',
                'political_status': '中共党员',
                'education_experience': '2017-2021 江南大学自动化本科；2021-2024 江南大学控制科学硕士',
                'practice_experience': '参与工业视觉检测项目',
                'personal_statement_text': '希望在智能制造方向继续深造',
                'signed_agreement': True,
                'selected_team_name': '智能制造联合团队',
                'selected_advisor_name': '刘亚',
                'self_evaluation': '具备算法与控制方向研究基础',
            },
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['application_business_key'] == 'RECRUIT-20260413-0007'
        assert payload['application_status'] == '报名已提交'
        assert payload['student']['selected_plan_id'] == 3
