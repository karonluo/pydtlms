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
                        'education_stage': '硕士',
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
                    'personal_statement_text': '希望在智能制造方向继续深造',
                    'resume_attachment_url': '/portal-attachments/uploads/student-7/resume/resume-a.pdf',
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
        assert payload['education_experiences'][0]['transcript_attachment_url'].endswith('transcript-a.pdf')
        assert payload['education_experiences'][0]['degree_certificate_attachment_url'].endswith('degree-a.pdf')
        assert payload['english_proficiencies'][0]['certificate_attachment_url'].endswith('cet6-a.pdf')
        assert payload['personal_statement']['resume_attachment_url'].endswith('resume-a.pdf')


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
                        'education_stage': '硕士',
                        'school_name': '江南大学',
                    }
                ],
                'profile': {
                    'gender': '男',
                    'birth_date': '1999-01-01',
                    'native_place': '江苏无锡',
                },
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
