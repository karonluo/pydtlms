import pytest

from app.schemas.recruitment import RecruitPlanUpsert
from app.schemas.student import CenterUpsert
from app.services.management_service import LazyRuntimeManagementStore, RuntimeManagementStore


class FakeRuntimeManagementStore:
    init_count = 0

    def __init__(self) -> None:
        type(self).init_count += 1
        self.label = "runtime-store"

    def ping(self) -> str:
        return self.label


class FakePostgresStateStore:
    def __init__(self) -> None:
        self.created_centers: list[dict] = []
        self.updated_centers: list[dict] = []
        self.deleted_center_ids: list[int] = []
        self.saved_states: list[dict] = []

    def load_state(self):
        return None

    def load_team_state(self):
        return []

    def get_portal_student_detail(self, student_id):
        del student_id
        return None

    def save_state(self, state) -> None:
        self.saved_states.append(state)

    def sync_created_center(self, team_payload, operation_log=None, counters=None) -> None:
        self.created_centers.append({"team_payload": team_payload, "operation_log": operation_log, "counters": counters})

    def sync_updated_center(self, team_payload, affected_students, operation_log=None, counters=None) -> None:
        self.updated_centers.append(
            {
                "team_payload": team_payload,
                "affected_students": affected_students,
                "operation_log": operation_log,
                "counters": counters,
            }
        )

    def sync_deleted_center(self, center_id, operation_log=None, counters=None) -> None:
        self.deleted_center_ids.append(int(center_id))


class FakeNotificationEmailService:
    def __init__(self) -> None:
        self.portal_registration_calls: list[dict] = []
        self.portal_password_reset_calls: list[dict] = []
        self.portal_admin_password_reset_calls: list[dict] = []
        self.recruitment_status_calls: list[dict] = []
        self.custom_message_calls: list[dict] = []
        self.is_enabled = True

    def enabled(self) -> bool:
        return self.is_enabled

    def send_portal_registration_success(self, full_name: str, email: str) -> None:
        self.portal_registration_calls.append({"full_name": full_name, "email": email})

    def send_portal_password_reset_success(self, full_name: str, email: str, account: str) -> None:
        self.portal_password_reset_calls.append({"full_name": full_name, "email": email, "account": account})

    def send_portal_admin_password_reset(self, full_name: str, email: str, temporary_password: str) -> None:
        self.portal_admin_password_reset_calls.append({"full_name": full_name, "email": email, "temporary_password": temporary_password})

    def send_recruitment_status_update(self, **payload) -> None:
        self.recruitment_status_calls.append(payload)

    def send_message(self, *, to_email: str, subject: str, text_body: str) -> None:
        self.custom_message_calls.append({"to_email": to_email, "subject": subject, "text_body": text_body})


def _build_center_payload(name: str) -> CenterUpsert:
    return CenterUpsert(
        center_name=name,
        director_name="刘亚",
        advisor_names=["刘亚", "袁野"],
        is_enabled=True,
        created_date="2026-04-21",
    )


def _build_plan_payload(name: str, description: str = "聚焦研究潜力与简章展示") -> RecruitPlanUpsert:
    return RecruitPlanUpsert(
        plan_name=name,
        academic_year="2026",
        semester="秋",
        brochure_image_url="/portal-brochures/test-plan.svg",
        plan_description=description,
    )


def _build_recruitment_application_payload():
    from app.schemas.recruitment import RecruitApplicationUpsert

    return RecruitApplicationUpsert(
        plan_id=1,
        student_name="邮件联调考生",
        graduation_school="江南大学",
        highest_degree="硕士",
        intended_field="智能制造",
        email="candidate-email@example.com",
        phone_number="13800009999",
        id_number="320000199901011234",
        material_status="待审核",
        application_status="报名已提交",
    )


def test_lazy_store_does_not_create_instance_until_attribute_access(monkeypatch) -> None:
    FakeRuntimeManagementStore.init_count = 0
    monkeypatch.setattr("app.services.management_service.RuntimeManagementStore", FakeRuntimeManagementStore)

    store = LazyRuntimeManagementStore()

    assert FakeRuntimeManagementStore.init_count == 0
    assert store._instance is None


def test_lazy_store_reuses_single_runtime_instance(monkeypatch) -> None:
    FakeRuntimeManagementStore.init_count = 0
    monkeypatch.setattr("app.services.management_service.RuntimeManagementStore", FakeRuntimeManagementStore)

    store = LazyRuntimeManagementStore()

    assert store.ping() == "runtime-store"
    assert store.label == "runtime-store"
    assert FakeRuntimeManagementStore.init_count == 1


def test_create_center_uses_incremental_sync(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    record = store.create_center(_build_center_payload("增量新增研究中心"))

    assert record.center_name == "增量新增研究中心"
    assert len(fake_postgres.created_centers) == 1
    assert fake_postgres.created_centers[0]["team_payload"]["team_name"] == "增量新增研究中心"


def test_delete_center_uses_incremental_sync(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_center(_build_center_payload("增量删除研究中心"))
    store.delete_center(created.id)

    assert created.id in fake_postgres.deleted_center_ids


def test_update_center_falls_back_to_full_save_when_incremental_sync_fails(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()

    def raising_sync_updated_center(*args, **kwargs) -> None:
        raise RuntimeError("sync failed")

    fake_postgres.sync_updated_center = raising_sync_updated_center
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_center(_build_center_payload("增量回退研究中心"))
    save_calls: list[bool] = []
    monkeypatch.setattr(store, "_save", lambda: save_calls.append(True))

    updated = store.update_center(
        created.id,
        _build_center_payload("增量回退研究中心-已更新"),
    )

    assert updated.center_name == "增量回退研究中心-已更新"
    assert save_calls == [True]


def test_migrate_state_backfills_recruitment_plan_fields(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_postgres.load_state = lambda: {
        "roles": [],
        "profiles": {},
        "teams": [],
        "students": [],
        "portal_students": [],
        "system_users": [],
        "audit_policies": [],
        "recruitment_plans": [{"id": 9, "plan_name": "历史计划", "academic_year": "2025", "semester": "春"}],
    }
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()

    migrated_plan = store.state["recruitment_plans"][0]
    assert migrated_plan["plan_description"] is None
    assert migrated_plan["current_stage"] == "报名配置"
    assert migrated_plan["target_quota"] == 0
    assert migrated_plan["interview_group_count"] == 0
    assert migrated_plan["is_open"] is True
    assert migrated_plan["brochure_image_url"] is None


def test_get_recruitment_plans_matches_keyword_with_plan_description(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    response = store.get_recruitment_plans(keyword="产业问题导向", page=1, page_size=10)

    assert response.total == 1
    record = response.items[0]
    assert record.plan_name == "2026 工程博士专项"
    assert record.plan_description == "面向工程实践与产业问题导向申请人，强调场景落地与交叉协同。"
    assert set(record.model_dump().keys()) == {
        "id",
        "plan_name",
        "academic_term",
        "academic_year",
        "semester",
        "application_count",
        "brochure_image_url",
        "plan_description",
    }


def test_create_recruitment_plan_keeps_internal_defaults_while_returning_trimmed_record(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_recruitment_plan(_build_plan_payload("2026 新计划", "只保留五个字段"))

    stored_plan = next(item for item in store.state["recruitment_plans"] if item["id"] == created.id)
    assert stored_plan["current_stage"] == "报名配置"
    assert stored_plan["target_quota"] == 0
    assert stored_plan["interview_group_count"] == 0
    assert stored_plan["is_open"] is True
    assert stored_plan["plan_description"] == "只保留五个字段"
    assert created.plan_description == "只保留五个字段"
    assert set(created.model_dump().keys()) == {
        "id",
        "plan_name",
        "academic_term",
        "academic_year",
        "semester",
        "application_count",
        "brochure_image_url",
        "plan_description",
    }


def test_get_public_recruitment_plans_exposes_description_as_summary(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    response = store.get_public_recruitment_plans()

    public_plan = response.items[0]
    assert public_plan.plan_name == "2026 智能制造联合培养"
    assert public_plan.summary == "聚焦智能制造方向联合培养，适合具备制造业、自动化、AI 背景的申请人。"
    assert set(public_plan.model_dump().keys()) == {
        "id",
        "plan_name",
        "academic_term",
        "brochure_image_url",
        "summary",
    }


def test_get_public_recruitment_plans_returns_latest_plan_first(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    store.state["recruitment_plans"] = [
        {"id": 1, "plan_name": "2025 春季补录", "academic_year": "2025", "semester": "春", "plan_description": "春季补录说明"},
        {"id": 2, "plan_name": "2026 秋季博士招生", "academic_year": "2026", "semester": "秋", "plan_description": "秋季计划说明"},
        {"id": 3, "plan_name": "2026 春季计划", "academic_year": "2026", "semester": "春", "plan_description": "春季计划说明"},
    ]

    response = store.get_public_recruitment_plans()

    assert [item.plan_name for item in response.items] == ["2026 秋季博士招生", "2026 春季计划", "2025 春季补录"]


def test_register_portal_student_sends_email_notification(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800002222",
            email="new-student@example.com",
            full_name="新注册学生",
            id_number="320000199902022222",
            password="Secret123!",
        )
    )

    assert fake_mailer.portal_registration_calls == [{"full_name": "新注册学生", "email": "new-student@example.com"}]


def test_reset_portal_student_password_sends_email_notification(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalPasswordResetRequest, PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800003333",
            email="password-reset@example.com",
            full_name="密码重置学生",
            id_number="320000199903033333",
            password="Secret123!",
        )
    )

    fake_mailer.portal_registration_calls.clear()
    store.reset_portal_student_password(
        PortalPasswordResetRequest(
            account="password-reset@example.com",
            id_number="320000199903033333",
            new_password="NewSecret123!",
        )
    )

    assert fake_mailer.portal_password_reset_calls == [
        {"full_name": "密码重置学生", "email": "password-reset@example.com", "account": "password-reset@example.com"}
    ]


def test_execute_workflow_action_sends_recruitment_pass_email(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    store = RuntimeManagementStore()
    application = store.create_recruitment_application(
        _build_recruitment_application_payload(),
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    task_id = store.state["workflow_tasks"][0]["id"]
    store.execute_workflow_action(
        task_id,
        "approve",
        None,
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    assert fake_mailer.recruitment_status_calls == [
        {
            "student_name": "邮件联调考生",
            "email": "candidate-email@example.com",
            "business_key": application.business_key,
            "application_status": "资格审核通过",
            "plan_name": "2026 秋季博士招生",
        }
    ]


def test_register_portal_student_does_not_trigger_email_when_smtp_disabled(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    fake_mailer.is_enabled = False
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800004444",
            email="no-smtp@example.com",
            full_name="未配置邮箱学生",
            id_number="320000199904044444",
            password="Secret123!",
        )
    )

    assert fake_mailer.portal_registration_calls == []


def test_register_portal_student_rejects_duplicate_phone_number(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001111",
            email="original-phone-check@example.com",
            full_name="基准学生",
            id_number="320000199905055555",
            password="Secret123!",
        )
    )
    with pytest.raises(ValueError, match="该手机号已注册，请直接登录"):
        store.register_portal_student(
            PortalRegistrationRequest(
                phone_number="13800001111",
                email="different-phone-check@example.com",
                full_name="同手机号学生",
                id_number="320000199905055556",
                password="Secret123!",
            )
        )


def test_register_portal_student_rejects_duplicate_email(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800005555",
            email="portal-student@example.com",
            full_name="基准学生",
            id_number="320000199906066666",
            password="Secret123!",
        )
    )
    with pytest.raises(ValueError, match="该邮箱已注册，请直接登录"):
        store.register_portal_student(
            PortalRegistrationRequest(
                phone_number="13800005556",
                email="portal-student@example.com",
                full_name="同邮箱学生",
                id_number="320000199906066667",
                password="Secret123!",
            )
        )


def test_register_portal_student_rejects_duplicate_id_number(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800006666",
            email="original-id-check@example.com",
            full_name="基准学生",
            id_number="320000199901011234",
            password="Secret123!",
        )
    )
    with pytest.raises(ValueError, match="该身份证号已注册，请使用找回密码"):
        store.register_portal_student(
            PortalRegistrationRequest(
                phone_number="13800006667",
                email="different-id-check@example.com",
                full_name="同身份证学生",
                id_number="320000199901011234",
                password="Secret123!",
            )
        )


def test_register_portal_student_allows_same_full_name(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    response = store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800007777",
            email="same-name@example.com",
            full_name="张三",
            id_number="320000199907077777",
            password="Secret123!",
        )
    )

    assert response.student.full_name == "张三"
    assert response.student.phone_number == "13800007777"


def test_get_registered_portal_students_marks_submission_status(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalApplicationUpsert, PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800008888",
            email="submitted-student@example.com",
            full_name="已报名学生",
            id_number="320000199908088888",
            password="Secret123!",
        )
    )
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009998",
            email="registered-only@example.com",
            full_name="未报名学生",
            id_number="320000199909099998",
            password="Secret123!",
        )
    )

    submitted_student_id = next(
        item["id"] for item in store.state["portal_students"] if item["email"] == "submitted-student@example.com"
    )
    store.submit_portal_application(
        submitted_student_id,
        PortalApplicationUpsert(
            plan_id=available_plan.id,
            graduation_school="江南大学",
            highest_degree="硕士",
            selected_team_name=available_team.team_name,
            selected_advisor_name=available_team.lead_advisor_name,
            intended_field=available_team.team_name,
            signed_agreement=True,
        ),
    )

    response = store.get_registered_portal_students(page=1, page_size=20)
    status_map = {item.email: item.application_form_status for item in response.items}

    assert status_map["submitted-student@example.com"] == "已填写报名"
    assert status_map["registered-only@example.com"] == "未填写报名"


def test_get_student_stats_includes_registered_portal_student_counts(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalApplicationUpsert, PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009991",
            email="stats-submitted@example.com",
            full_name="统计已报名",
            id_number="320000199909099991",
            password="Secret123!",
        )
    )
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009992",
            email="stats-unsubmitted@example.com",
            full_name="统计未报名",
            id_number="320000199909099992",
            password="Secret123!",
        )
    )

    submitted_student_id = next(
        item["id"] for item in store.state["portal_students"] if item["email"] == "stats-submitted@example.com"
    )
    store.submit_portal_application(
        submitted_student_id,
        PortalApplicationUpsert(
            plan_id=available_plan.id,
            graduation_school="东南大学",
            highest_degree="硕士",
            selected_team_name=available_team.team_name,
            selected_advisor_name=available_team.lead_advisor_name,
            intended_field=available_team.team_name,
            signed_agreement=True,
        ),
    )

    stats = store.get_student_stats()

    assert stats.registered_portal_total == 2
    assert stats.portal_submitted_total == 1
    assert stats.portal_unsubmitted_total == 1


def test_deactivate_registered_portal_student_blocks_login(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalLoginRequest, PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009993",
            email="deactivate-student@example.com",
            full_name="注销学生",
            id_number="320000199909099993",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "deactivate-student@example.com")
    response = store.deactivate_registered_portal_student(student_id)

    assert response.account_status == "停用"
    with pytest.raises(ValueError, match="账号已停用，请联系管理员"):
        store.login_portal_student(PortalLoginRequest(account="deactivate-student@example.com", password="Secret123!"))


def test_activate_registered_portal_student_restores_login(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalLoginRequest, PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009996",
            email="reactivate-student@example.com",
            full_name="重新启用学生",
            id_number="320000199909099996",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "reactivate-student@example.com")
    store.deactivate_registered_portal_student(student_id)

    response = store.activate_registered_portal_student(student_id)

    assert response.account_status == "启用"
    record = store.login_portal_student(PortalLoginRequest(account="reactivate-student@example.com", password="Secret123!"))
    assert record.email == "reactivate-student@example.com"


def test_change_portal_student_password_requires_current_password(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalLoginRequest, PortalPasswordChangeRequest, PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009997",
            email="profile-password@example.com",
            full_name="个人空间学生",
            id_number="320000199909099997",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "profile-password@example.com")

    with pytest.raises(ValueError, match="当前密码不正确"):
        store.change_portal_student_password(
            student_id,
            PortalPasswordChangeRequest(current_password="Wrong123!", new_password="NewSecret123!"),
        )

    store.change_portal_student_password(
        student_id,
        PortalPasswordChangeRequest(current_password="Secret123!", new_password="NewSecret123!"),
    )

    record = store.login_portal_student(PortalLoginRequest(account="profile-password@example.com", password="NewSecret123!"))
    assert record.email == "profile-password@example.com"


def test_reset_registered_portal_student_password_sends_email_when_smtp_enabled(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009994",
            email="admin-reset-student@example.com",
            full_name="重置密码学生",
            id_number="320000199909099994",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "admin-reset-student@example.com")
    response = store.reset_registered_portal_student_password(student_id)

    assert response.email_sent is True
    assert response.temporary_password
    assert fake_mailer.portal_admin_password_reset_calls == [
        {
            "full_name": "重置密码学生",
            "email": "admin-reset-student@example.com",
            "temporary_password": response.temporary_password,
        }
    ]


def test_send_registered_portal_student_email_skips_when_smtp_disabled(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    fake_mailer.is_enabled = False
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalRegistrationRequest
    from app.schemas.student import RegisteredPortalStudentEmailRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009995",
            email="custom-email-student@example.com",
            full_name="邮件学生",
            id_number="320000199909099995",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "custom-email-student@example.com")
    response = store.send_registered_portal_student_email(
        student_id,
        RegisteredPortalStudentEmailRequest(subject="自定义通知", content="请尽快完善报名信息。"),
    )

    assert response.email_sent is False
    assert fake_mailer.custom_message_calls == []