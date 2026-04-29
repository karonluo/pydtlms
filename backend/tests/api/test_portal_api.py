from pathlib import Path
from threading import RLock

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.recruitment import RecruitApplicationRecord
from app.schemas.portal import PortalRegistrationEmailCodeResponse, PortalRegistrationResponse, PortalStudentRecord
from app.services.management_service import RuntimeManagementStore


def _portal_student_payload(student_id: int = 7) -> dict[str, object]:
    return {
        'id': student_id,
        'full_name': '张三',
        'phone_number': '13800001111',
        'email': 'zhangsan@example.com',
        'id_number': '32000019990101123X',
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


def _build_personal_statement_payload(include_resume: bool = True, include_supporting_material: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {
        'growth_experience_text': '成长' + '甲' * 280,
        'program_application_reason_text': '申报' + '乙' * 280,
        'career_plan_text': '规划' + '丙' * 280,
    }
    if include_resume:
        payload['resume_attachment_url'] = '/portal-attachments/uploads/student-7/resume/resume-a.pdf'
    if include_supporting_material:
        payload['supporting_material_attachment_url'] = '/portal-attachments/uploads/student-7/supporting_material/supporting-material.zip'
    return payload


def test_portal_register_returns_profile(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.validate_portal_registration_email_code', lambda email, verification_code: None)
        monkeypatch.setattr('app.api.v1.portal.clear_portal_registration_email_code', lambda email: None)
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
                'id_number': '32000019990101123X',
                'password': 'Secret123!',
                'email_verification_code': '123456',
            },
        )

        assert response.status_code == 201
        payload = response.json()
        assert payload['message'] == '注册成功，请登录后继续填写申请表'
        assert payload['student']['full_name'] == '张三'
        assert payload['student']['selected_team_name'] == '智能制造联合团队'


def test_portal_send_registration_email_code_returns_message(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr(
            'app.api.v1.portal.send_portal_registration_email_code',
            lambda email: PortalRegistrationEmailCodeResponse(
                message='邮件验证码已发送，请查收邮箱',
                expires_in_seconds=600,
                cooldown_seconds=60,
            ),
        )

        response = client.post(
            '/api/v1/portal/register/email-code',
            json={'email': 'zhangsan@example.com'},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['message'] == '邮件验证码已发送，请查收邮箱'
        assert payload['cooldown_seconds'] == 60


def test_portal_send_login_email_code_returns_message(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr(
            'app.api.v1.portal.send_portal_login_email_code',
            lambda email: PortalRegistrationEmailCodeResponse(
                message='登录验证码已发送，请查收邮箱',
                expires_in_seconds=600,
                cooldown_seconds=60,
            ),
        )

        response = client.post(
            '/api/v1/portal/login/email-code/send',
            json={'email': 'zhangsan@example.com'},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['message'] == '登录验证码已发送，请查收邮箱'
        assert payload['cooldown_seconds'] == 60


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


def test_portal_login_by_email_code_returns_session(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.login_portal_student_by_email_code', lambda email, verification_code: _portal_student_record())
        monkeypatch.setattr('app.api.v1.portal.create_portal_access_token', lambda student_id, full_name: f'portal-{student_id}')

        response = client.post(
            '/api/v1/portal/login/email-code',
            json={
                'email': 'zhangsan@example.com',
                'email_verification_code': '123456',
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
                'id_number': '32000019990101123X',
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


def test_portal_public_config_returns_application_v2_switch(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_admissions_info_url', 'https://admissions.example.com')
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', True)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_block_message', '4月30日（周四）20点之前开放，敬请期待')

        response = client.get('/api/v1/portal/public-config', headers={'Authorization': 'Bearer portal-token'})

        assert response.status_code == 200
        assert response.json() == {
            'portal_admissions_info_url': 'https://admissions.example.com',
            'portal_application_v2_blocked': True,
            'portal_application_v2_block_message': '4月30日（周四）20点之前开放，敬请期待',
        }


def test_portal_application_submission_returns_business_key(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
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
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张父', 'relation_type': '父亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
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


def test_portal_application_submission_is_blocked_when_switch_is_enabled(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', True)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_block_message', '4月30日（周四）20点之前开放，敬请期待')

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'graduation_school': '江南大学',
                'highest_degree': '硕士',
                'selected_team_name': '智能制造联合团队',
                'intended_field': '智能制造',
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
            },
        )

        assert response.status_code == 403
        assert response.json()['detail'] == '4月30日（周四）20点之前开放，敬请期待'


def test_portal_application_draft_is_blocked_when_switch_is_enabled(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', True)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_block_message', '4月30日（周四）20点之前开放，敬请期待')

        response = client.post(
            '/api/v1/portal/applications/draft',
            headers={'Authorization': 'Bearer portal-token'},
            json={'plan_id': 3},
        )

        assert response.status_code == 403
        assert response.json()['detail'] == '4月30日（周四）20点之前开放，敬请期待'


def test_portal_attachment_upload_returns_public_url(monkeypatch, tmp_path: Path) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.PORTAL_ATTACHMENT_UPLOAD_DIR', tmp_path)

        response = client.post(
            '/api/v1/portal/attachments/upload',
            headers={'Authorization': 'Bearer portal-token'},
            data={'category': 'resume'},
            files={'file': ('resume.pdf', b'%PDF-1.7 mock file', 'application/pdf')},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['category'] == 'resume'
        assert payload['file_name'] == 'resume.pdf'
        assert payload['url'].startswith('/portal-attachments/uploads/student-7/resume/')
        uploaded_files = list((tmp_path / 'student-7' / 'resume').glob('resume-*'))
        assert len(uploaded_files) == 1
        assert uploaded_files[0].read_bytes() == b'%PDF-1.7 mock file'


def test_portal_id_card_collage_upload_accepts_jpg(monkeypatch, tmp_path: Path) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.PORTAL_ATTACHMENT_UPLOAD_DIR', tmp_path)

        response = client.post(
            '/api/v1/portal/attachments/upload',
            headers={'Authorization': 'Bearer portal-token'},
            data={'category': 'id_card_collage'},
            files={'file': ('id-card.jpg', b'\xff\xd8\xff mock jpeg', 'image/jpeg')},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['category'] == 'id_card_collage'
        assert payload['file_name'] == 'id-card.jpg'
        assert payload['url'].startswith('/portal-attachments/uploads/student-7/id_card_collage/')


def test_portal_attachment_upload_rejects_unsupported_file_type(monkeypatch, tmp_path: Path) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.PORTAL_ATTACHMENT_UPLOAD_DIR', tmp_path)

        response = client.post(
            '/api/v1/portal/attachments/upload',
            headers={'Authorization': 'Bearer portal-token'},
            data={'category': 'resume'},
            files={'file': ('resume.txt', b'plain text', 'text/plain')},
        )

        assert response.status_code == 400
        assert response.json()['detail'] == '附件格式不受支持'


def test_portal_attachment_upload_accepts_octet_stream_when_suffix_is_valid(monkeypatch, tmp_path: Path) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.PORTAL_ATTACHMENT_UPLOAD_DIR', tmp_path)

        response = client.post(
            '/api/v1/portal/attachments/upload',
            headers={'Authorization': 'Bearer portal-token'},
            data={'category': 'resume'},
            files={'file': ('resume.pdf', b'%PDF-1.7 octet stream', 'application/octet-stream')},
        )

        assert response.status_code == 200
        assert response.json()['category'] == 'resume'


def test_portal_attachment_upload_accepts_powershell_form_content_type(monkeypatch, tmp_path: Path) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.PORTAL_ATTACHMENT_UPLOAD_DIR', tmp_path)

        response = client.post(
            '/api/v1/portal/attachments/upload',
            headers={'Authorization': 'Bearer portal-token'},
            data={'category': 'resume'},
            files={'file': ('resume.pdf', b'%PDF-1.7 powershell form', 'application/x-msdownload')},
        )

        assert response.status_code == 200
        assert response.json()['category'] == 'resume'


def test_portal_application_submission_accepts_structured_attachment_fields(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_submit(student_id, payload):
        captured['student_id'] = student_id
        captured['payload'] = payload.model_dump(mode='json', exclude_none=True)
        return {
            'student': _portal_student_payload(student_id),
            'application_business_key': 'RECRUIT-20260421-0007',
            'application_status': '报名已提交',
        }

    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
        monkeypatch.setattr('app.api.v1.portal.submit_portal_application', fake_submit)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'profile': {
                    'id_card_collage_url': '/portal-attachments/uploads/student-7/id_card_collage/id-card.jpg',
                    'gender': '男',
                    'birth_date': '1999-01-01',
                    'native_place': '江苏无锡',
                    'political_status': '中共党员',
                },
                'source_channel': '实验室官网',
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                        'transcript_attachment_url': '/portal-attachments/uploads/student-7/education_transcript/transcript-a.pdf',
                        'degree_certificate_attachment_url': '/portal-attachments/uploads/student-7/education_degree_certificate/degree-a.pdf',
                    }
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张父', 'relation_type': '父亲'},
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'personal_statement': {
                    **_build_personal_statement_payload(include_resume=True, include_supporting_material=True),
                },
                'declaration': {
                    'has_read_declaration': True,
                    'declaration_text': '本人承诺以上填写内容真实、准确。',
                },
            },
        )

        assert response.status_code == 200
        assert response.json()['application_business_key'] == 'RECRUIT-20260421-0007'
        assert captured['student_id'] == 7
        payload = captured['payload']
        assert payload['profile']['id_card_collage_url'].endswith('id-card.jpg')
        assert payload['education_experiences'][1]['transcript_attachment_url'].endswith('transcript-a.pdf')
        assert payload['education_experiences'][1]['degree_certificate_attachment_url'].endswith('degree-a.pdf')
        assert payload['english_proficiencies'][0]['certificate_attachment_url'].endswith('cet6-a.pdf')
        assert payload['personal_statement']['growth_experience_text'].startswith('成长')
        assert payload['personal_statement']['resume_attachment_url'].endswith('resume-a.pdf')
        assert payload['personal_statement']['supporting_material_attachment_url'].endswith('supporting-material.zip')
        assert payload['material_list_attachment'].endswith('supporting-material.zip')


def test_portal_application_submission_rejects_short_personal_statement(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '硕士在读',
                        'school_name': '江南大学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科毕业',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张父', 'relation_type': '父亲'},
                ],
                'personal_statement': {
                    'growth_experience_text': '成长经历过短',
                    'program_application_reason_text': '申报理由过短',
                    'career_plan_text': '发展规划过短',
                    'resume_attachment_url': '/portal-attachments/uploads/student-7/resume/resume-a.pdf',
                },
            },
        )

        assert response.status_code == 422
        assert '800-1200' in response.text


def test_portal_application_submission_rejects_missing_resume_attachment(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '硕士在读',
                        'school_name': '江南大学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科毕业',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张父', 'relation_type': '父亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=False),
            },
        )

        assert response.status_code == 422
        assert '简历附件' in response.text


def test_portal_application_submission_rejects_bachelor_graduate_without_master_stage(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科毕业',
                        'school_name': '江南大学',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '本科毕业' in response.text


def test_portal_application_draft_rejects_bachelor_current_with_master_stage(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications/draft',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '硕士在读',
                        'school_name': '上海人工智能实验室联培项目',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '本科在读' in response.text


def test_portal_application_draft_rejects_bachelor_graduate_stage_without_master_stage(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications/draft',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科毕业',
                        'school_name': '',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '本科毕业' in response.text


def test_portal_application_draft_rejects_blank_second_education_experience(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications/draft',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '',
                        'school_name': '',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '教育经历2' in response.text


def test_portal_application_submission_rejects_non_bachelor_second_education_experience(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '硕士在读',
                        'school_name': '上海人工智能实验室联培项目',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '教育经历2' in response.text


def test_portal_application_draft_rejects_incomplete_practice_with_dates(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications/draft',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'practice_experiences': [
                    {
                        'start_month': '2023-07',
                        'organization_name': '',
                        'position_name': '',
                        'responsibility_text': '参与现场测试',
                        'verifier_name': '',
                        'verifier_phone': '',
                    }
                ],
            },
        )

        assert response.status_code == 422
        assert '实践经历1' in response.text
        assert '除职责外其余字段均必填' in response.text


def test_portal_application_submission_rejects_more_than_two_practice_experiences(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'practice_experiences': [
                    {
                        'organization_name': '单位一',
                    },
                    {
                        'organization_name': '单位二',
                    },
                    {
                        'organization_name': '单位三',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '实践经历最多填写 2 条' in response.text


def test_portal_application_submission_strips_blank_practice_placeholder(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_submit(student_id, payload):
        captured['student_id'] = student_id
        captured['payload'] = payload.model_dump(mode='json', exclude_none=True)
        return {
            'student': _portal_student_payload(student_id),
            'application_business_key': 'RECRUIT-20260429-0007',
            'application_status': '报名已提交',
        }

    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
        monkeypatch.setattr('app.api.v1.portal.submit_portal_application', fake_submit)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'practice_experiences': [
                    {
                        'start_month': '',
                        'end_month': '',
                        'organization_name': '',
                        'position_name': '',
                        'responsibility_text': '',
                        'verifier_name': '',
                        'verifier_phone': '',
                    }
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'IELTS',
                        'score_text': '7.0',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/ielts-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
            },
        )

        assert response.status_code == 200
        payload = captured['payload']
        assert payload['practice_experiences'] == []
        assert 'practice_experience' not in payload


def test_portal_application_submission_rejects_missing_english_proficiency(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
            },
        )

        assert response.status_code == 422
        assert '英语能力' in response.text


def test_portal_application_submission_rejects_english_proficiency_without_attachment(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                    }
                ],
            },
        )

        assert response.status_code == 422
        assert '英语证明附件' in response.text


def test_portal_application_submission_rejects_missing_parent_family_member(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '', 'relation_type': '父亲'},
                    {'member_name': '', 'relation_type': '母亲'},
                ],
            },
        )

        assert response.status_code == 422
        assert '父母信息至少填写一方' in response.text


def test_portal_application_submission_accepts_single_parent_family_member(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_submit(student_id, payload):
        captured['payload'] = payload.model_dump(mode='json', exclude_none=True)
        return {
            'student': _portal_student_payload(student_id),
            'application_business_key': 'RECRUIT-20260429-0010',
            'application_status': '报名已提交',
        }

    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
        monkeypatch.setattr('app.api.v1.portal.submit_portal_application', fake_submit)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'IELTS',
                        'score_text': '7.0',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/ielts-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
            },
        )

        assert response.status_code == 200
        payload = captured['payload']
        assert payload['family_members'] == [{'member_name': '张母', 'relation_type': '母亲'}]


def test_portal_application_submission_rejects_more_than_four_achievement_records(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'achievement_records': [
                    {'achievement_type': '论文发表'},
                    {'achievement_type': '科研项目'},
                    {'achievement_type': '学生活动'},
                    {'achievement_type': '获奖经历'},
                    {'achievement_type': '论文发表'},
                ],
            },
        )

        assert response.status_code == 422
        assert '成果经历最多填写 4 条' in response.text


def test_portal_application_submission_rejects_incomplete_paper_achievement(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'CET-6',
                        'score_text': '520',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'achievement_records': [
                    {
                        'achievement_type': '论文发表',
                        'achievement_month': '2025-03',
                        'paper_title': '复杂工业系统中的诊断方法研究',
                    }
                ],
            },
        )

        assert response.status_code == 422
        assert '论文发表时' in response.text
        assert '作者序位' in response.text


def test_portal_application_submission_rejects_award_achievement_without_certificate(monkeypatch) -> None:
    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'IELTS',
                        'score_text': '7.0',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/ielts-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'achievement_records': [
                    {
                        'achievement_type': '获奖经历',
                        'achievement_month': '2024-11',
                        'award_name': '全国研究生数学建模竞赛',
                        'award_rank': '一等奖',
                        'description_text': '担任主要建模成员并完成答辩。',
                    }
                ],
            },
        )

        assert response.status_code == 422
        assert '获奖经历时' in response.text
        assert '获奖证明' in response.text


def test_portal_application_submission_accepts_structured_achievement_records(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_submit(student_id, payload):
        captured['payload'] = payload.model_dump(mode='json', exclude_none=True)
        return {
            'student': _portal_student_payload(student_id),
            'application_business_key': 'RECRUIT-20260429-0011',
            'application_status': '报名已提交',
        }

    with TestClient(app) as client:
        monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
        monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
        monkeypatch.setattr('app.api.v1.portal.submit_portal_application', fake_submit)

        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    },
                ],
                'english_proficiencies': [
                    {
                        'exam_name': 'IELTS',
                        'score_text': '7.0',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/ielts-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张母', 'relation_type': '母亲'},
                ],
                'achievement_records': [
                    {
                        'achievement_type': '论文发表',
                        'achievement_month': '2025-03',
                        'paper_title': '复杂工业系统中的诊断方法研究',
                        'author_order': '第一作者',
                        'journal_or_conference': '控制与决策',
                        'description_text': '围绕复杂工业系统的故障诊断方法展开研究。',
                    },
                    {
                        'achievement_type': '获奖经历',
                        'achievement_month': '2024-11',
                        'award_name': '全国研究生数学建模竞赛',
                        'award_rank': '一等奖',
                        'award_certificate_attachment_url': '/portal-attachments/uploads/student-7/achievement_award_certificate/math-modeling.pdf',
                        'description_text': '担任主要建模成员并完成答辩。',
                    },
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
            },
        )

        assert response.status_code == 200
        payload = captured['payload']
        achievement_records = payload['achievement_records']
        assert achievement_records[0]['achievement_month'] == '2025-03'
        assert achievement_records[0]['publish_or_index_month'] == '2025-03'
        assert achievement_records[0]['description_text'] == '围绕复杂工业系统的故障诊断方法展开研究。'
        assert achievement_records[0]['responsibility_text'] == '围绕复杂工业系统的故障诊断方法展开研究。'
        assert achievement_records[1]['award_rank'] == '一等奖'
        assert achievement_records[1]['award_level'] == '一等奖'
        assert achievement_records[1]['award_year'] == '2024'
        assert achievement_records[1]['award_certificate_attachment_url'].endswith('math-modeling.pdf')


def test_portal_application_submission_creates_new_record_without_deadlock(monkeypatch) -> None:
    portal_submission_calls: list[dict[str, object]] = []
    saved_markers: list[str] = []

    class DummyStore:
        def __init__(self) -> None:
            self._lock = RLock()
            self.state = {
                'portal_students': [
                    {
                        'id': 7,
                        'full_name': '张三',
                        'phone_number': '13800001111',
                        'email': 'zhangsan@example.com',
                        'id_number': '32000019990101123X',
                    }
                ],
                'recruitment_plans': [{'id': 3, 'is_open': True, 'plan_name': '2026 秋季博士招生'}],
                'teams': [
                    {
                        'id': 8,
                        'team_name': '智能制造联合团队',
                        'lead_advisor_name': '刘亚',
                        'advisor_names': ['刘亚', '徐素天'],
                        'status': '启用',
                    }
                ],
                'recruitment_applications': [],
                'workflow_tasks': [],
                'operation_logs': [],
                'counters': {'recruitment_applications': 1, 'workflow_tasks': 1, 'operation_logs': 1},
            }

        def _list(self, dataset: str):
            return self.state.setdefault(dataset, [])

        def _find_required(self, dataset: str, item_id: int):
            for index, item in enumerate(self._list(dataset)):
                if int(item.get('id', 0)) == int(item_id):
                    return index, item
            raise KeyError(item_id)

        def _normalize_name_list(self, value, fallback=None):
            names = [str(item).strip() for item in (value or []) if str(item).strip()]
            if fallback and fallback not in names:
                names.insert(0, fallback)
            return names

        def _ensure_team_exists(self, team_name: str):
            return next(item for item in self._list('teams') if item['team_name'] == team_name)

        def _normalize_portal_account_status(self, value):
            return str(value or '启用').strip() or '启用'

        def _build_portal_profile_payload(self, payload):
            return {'gender': payload.gender, 'birth_date': payload.birth_date, 'native_place': payload.native_place}

        def _build_portal_application_draft_payload(self, payload, advisor_name: str, submitted_at: str):
            data = payload.model_dump(mode='json', exclude_none=True)
            preferences = data.get('preferences') or []
            if preferences and advisor_name:
                preferences[0]['advisor_name'] = advisor_name
            data['selected_advisor_name'] = advisor_name
            data['submitted_at'] = submitted_at
            return data

        def _next_id(self, counter_name: str) -> int:
            current = int(self.state['counters'].get(counter_name, 1))
            self.state['counters'][counter_name] = current + 1
            return current

        def _principal_summary(self, principal):
            return principal

        def _workflow_initial_item(self, workflow_name: str, payload: dict[str, object]):
            return {
                **payload,
                'business_key': 'RECRUIT-20260421-0007',
                'application_status': '报名已提交',
            }

        def _start_managed_workflow(self, workflow_name: str, item: dict[str, object], operator_username: str | None = None):
            return None

        def _record_operation(self, *args, **kwargs):
            return None

        def _workflow_task_index_by_business_key(self, business_key: str):
            del business_key
            return None

        def _save(self):
            saved_markers.append('saved')

        def sync_portal_application_submission(self, student, application, operation_log, workflow_task=None, counters=None):
            portal_submission_calls.append(
                {
                    'student': student,
                    'application': application,
                    'operation_log': operation_log,
                    'workflow_task': workflow_task,
                    'counters': counters,
                }
            )

        def _persist_portal_application_submission(
            self,
            student,
            application,
            operation_log,
            *,
            workflow_task=None,
            created_application=False,
            created_workflow_task=False,
        ):
            counters = {'operation_logs': int(self.state['counters'].get('operation_logs', 0))}
            if created_application:
                counters['recruitment_applications'] = int(self.state['counters'].get('recruitment_applications', 0))
            if created_workflow_task:
                counters['workflow_tasks'] = int(self.state['counters'].get('workflow_tasks', 0))
            self.sync_portal_application_submission(
                student,
                application,
                operation_log,
                workflow_task=workflow_task,
                counters=counters,
            )

        def get_portal_student(self, student_id: int):
            student = next(item for item in self._list('portal_students') if int(item['id']) == int(student_id))
            return PortalStudentRecord(**student)

    store = DummyStore()

    monkeypatch.setattr('app.api.v1.portal.resolve_portal_student_id', lambda credentials: 7)
    monkeypatch.setattr('app.api.v1.portal.settings.portal_application_v2_blocked', False)
    monkeypatch.setattr(
        'app.api.v1.portal.submit_portal_application',
        lambda student_id, payload: RuntimeManagementStore.submit_portal_application(store, student_id, payload),
    )

    with TestClient(app) as client:
        response = client.post(
            '/api/v1/portal/applications',
            headers={'Authorization': 'Bearer portal-token'},
            json={
                'plan_id': 3,
                'source_channel': '实验室官网',
                'preferences': [
                    {
                        'preference_order': 1,
                        'research_center_name': '智能制造联合团队',
                        'advisor_name': '刘亚',
                        'is_optional': False,
                    }
                ],
                'education_experiences': [
                    {
                        'sort_order': 1,
                        'education_stage': '高中毕业',
                        'school_name': '无锡市第一中学',
                    },
                    {
                        'sort_order': 2,
                        'education_stage': '本科在读',
                        'school_name': '江南大学',
                    }
                ],
                'profile': {
                    'gender': '男',
                    'birth_date': '1999-01-01',
                    'native_place': '江苏无锡',
                },
                'english_proficiencies': [
                    {
                        'exam_name': 'TOEFL',
                        'score_text': '103',
                        'certificate_attachment_url': '/portal-attachments/uploads/student-7/english_certificate/toefl-a.pdf',
                    }
                ],
                'family_members': [
                    {'member_name': '张父', 'relation_type': '父亲'},
                ],
                'personal_statement': _build_personal_statement_payload(include_resume=True),
                'declaration': {
                    'has_read_declaration': True,
                    'declaration_text': '本人承诺以上填写内容真实、准确。',
                },
            },
        )

    assert response.status_code == 200
    assert response.json()['application_business_key'] == 'RECRUIT-20260421-0007'
    assert len(store.state['recruitment_applications']) == 1
    assert len(portal_submission_calls) == 1
    assert saved_markers == []


def test_portal_register_rejects_invalid_id_number() -> None:
    with TestClient(app) as client:
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

        assert response.status_code == 422


def test_portal_register_rejects_invalid_phone_or_email() -> None:
    with TestClient(app) as client:
        response = client.post(
            '/api/v1/portal/register',
            json={
                'phone_number': '12345',
                'email': 'invalid-email',
                'full_name': '张三',
                'id_number': '32000019990101123X',
                'password': 'Secret123!',
            },
        )

        assert response.status_code == 422
