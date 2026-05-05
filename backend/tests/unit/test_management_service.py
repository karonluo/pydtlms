from datetime import datetime

import pytest

from app.schemas.auth import UserProfileUpdate
from app.schemas.recruitment import RecruitApplicationRecord, RecruitPlanUpsert
from app.schemas.system import RoleUpsert
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
        self.created_students: list[dict] = []
        self.updated_students: list[dict] = []
        self.updated_portal_students: list[dict] = []
        self.deleted_center_ids: list[int] = []
        self.deleted_recruitment_plan_ids: list[int] = []
        self.portal_application_submissions: list[dict] = []
        self.updated_recruitment_applications: list[dict] = []
        self.saved_states: list[dict] = []
        self.synced_roles: list[dict] = []
        self.synced_operation_logs: list[dict] = []
        self.workflow_task_snapshot: dict | None = None
        self.dict_options_map: dict[str, list[dict]] = {}

    def load_state(self) -> dict | None:
        return None

    def load_team_state(self):
        raise AttributeError("load_team_state")

    def list_dict_options(self, dict_type: str) -> list[dict]:
        return list(self.dict_options_map.get(dict_type, []))

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

    def delete_recruitment_plan(self, plan_id) -> None:
        self.deleted_recruitment_plan_ids.append(int(plan_id))

    def sync_created_student(self, student_payload, operation_log=None, counters=None) -> None:
        self.created_students.append({"student_payload": student_payload, "operation_log": operation_log, "counters": counters})

    def sync_updated_student(self, student_payload, operation_log=None, counters=None) -> None:
        self.updated_students.append({"student_payload": student_payload, "operation_log": operation_log, "counters": counters})

    def sync_portal_student(self, student_payload, operation_log=None, counters=None) -> None:
        self.updated_portal_students.append({"student_payload": student_payload, "operation_log": operation_log, "counters": counters})
        self.saved_states.append({"portal_student_payload": student_payload, "operation_log": operation_log, "counters": counters})

    def sync_portal_application_submission(
        self,
        portal_student_payload,
        application_payload,
        operation_log=None,
        *,
        workflow_task=None,
        counters=None,
    ) -> None:
        self.portal_application_submissions.append(
            {
                "portal_student_payload": portal_student_payload,
                "application_payload": application_payload,
                "operation_log": operation_log,
                "workflow_task": workflow_task,
                "counters": counters,
            }
        )

    def sync_recruitment_application_status(self, application_id, payload) -> None:
        self.updated_recruitment_applications.append({"application_id": int(application_id), "payload": dict(payload)})

    def sync_role(self, role_payload, operation_log=None, *, counters=None) -> None:
        self.synced_roles.append({"role_payload": role_payload, "operation_log": operation_log, "counters": counters})

    def delete_role(self, role_id) -> None:
        self.deleted_center_ids.append(int(role_id))

    def sync_operation_log(self, operation_log, *, counters=None) -> None:
        self.synced_operation_logs.append({"operation_log": operation_log, "counters": counters})

    def get_workflow_task_snapshot(self, task_id):
        del task_id
        return self.workflow_task_snapshot

    def sync_user_profile(self, profile) -> None:
        self.saved_states.append({"profile": profile})

    def sync_system_user(self, user_payload, profile_payload=None, operation_log=None, *, counters=None) -> None:
        self.saved_states.append(
            {
                "user_payload": user_payload,
                "profile_payload": profile_payload,
                "operation_log": operation_log,
                "counters": counters,
            }
        )


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

    def send_portal_registration_success_async(self, full_name: str, email: str) -> None:
        self.send_portal_registration_success(full_name, email)

    def send_portal_password_reset_success(self, full_name: str, email: str, account: str) -> None:
        self.portal_password_reset_calls.append({"full_name": full_name, "email": email, "account": account})

    def send_portal_admin_password_reset(self, full_name: str, email: str, temporary_password: str) -> None:
        self.portal_admin_password_reset_calls.append({"full_name": full_name, "email": email, "temporary_password": temporary_password})

    def send_recruitment_status_update(self, **payload) -> None:
        self.recruitment_status_calls.append(payload)

    def send_message(self, *, to_email: str, subject: str, text_body: str) -> None:
        self.custom_message_calls.append({"to_email": to_email, "subject": subject, "text_body": text_body})

    def send_portal_registration_verification_code(self, email: str, verification_code: str) -> None:
        self.custom_message_calls.append(
            {
                "to_email": email,
                "subject": "学生门户邮箱验证码",
                "text_body": f"验证码：{verification_code}",
            }
        )

    def send_portal_login_verification_code(self, email: str, verification_code: str) -> None:
        self.custom_message_calls.append(
            {
                "to_email": email,
                "subject": "学生门户登录验证码",
                "text_body": f"验证码：{verification_code}",
            }
        )


class FakeCacheClient:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.ttl_values: dict[str, int] = {}

    def get(self, key: str):
        return self.values.get(key)

    def set(self, key: str, value, ex: int | None = None) -> bool:
        self.values[key] = str(value)
        if ex is not None:
            self.ttl_values[key] = int(ex)
        return True

    def exists(self, key: str) -> bool:
        return key in self.values

    def ttl(self, key: str) -> int:
        return int(self.ttl_values.get(key, -1))

    def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            if key in self.values:
                removed += 1
                self.values.pop(key, None)
            self.ttl_values.pop(key, None)
        return removed

    def incr(self, key: str) -> int:
        current = int(self.values.get(key, "0")) + 1
        self.values[key] = str(current)
        return current

    def expire(self, key: str, seconds: int) -> bool:
        self.ttl_values[key] = int(seconds)
        return True


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
        id_number="32000019990101123X",
        material_status="待审核",
        application_status="报名已提交",
    )


def _build_portal_application_payload(plan_id: int, team_name: str, advisor_name: str):
    from app.schemas.portal import PortalApplicationUpsert

    return PortalApplicationUpsert(
        plan_id=plan_id,
        profile={
            "full_name_pinyin": "zhangsan",
            "profile_photo_url": "/portal-attachments/uploads/student-7/profile_photo/photo-a.jpg",
            "id_card_collage_url": "/portal-attachments/uploads/student-7/id_card_collage/id-card-a.jpg",
            "gender": "男",
            "ethnic_group": "汉族",
            "political_status": "共青团员",
            "mailing_address": "上海市徐汇区某路 100 号",
            "emergency_contact_name": "张家长",
            "emergency_contact_phone": "13800002222",
        },
        graduation_school="江南大学",
        highest_degree="硕士",
        selected_team_name=team_name,
        selected_advisor_name=advisor_name,
        intended_field=team_name,
        source_channel="实验室官网",
        english_proficiencies=[
            {
                "exam_name": "CET-6",
                "score_text": "520",
                "certificate_attachment_url": "/portal-attachments/uploads/student-7/english_certificate/cet6-a.pdf",
            }
        ],
        family_members=[
            {"member_name": "张父", "relation_type": "父亲", "contact_phone": "13800001111"},
        ],
        personal_statement={
            "personal_statement_text": "个人陈述" + "丁" * 280,
            "growth_experience_text": "成长" + "甲" * 280,
            "program_application_reason_text": "申报" + "乙" * 280,
            "career_plan_text": "规划" + "丙" * 280,
            "resume_attachment_url": "/portal-attachments/uploads/student-7/resume/resume-a.pdf",
        },
        declaration={
            "has_read_declaration": True,
        },
        signed_agreement=True,
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


def test_get_centers_filters_by_director_id(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()

    def list_centers_page(*, keyword=None, is_enabled=None, director_id=None, page=1, page_size=10):
        del keyword, is_enabled, page, page_size
        items = [
            {
                "id": 1,
                "center_name": "智能制造联合团队",
                "director_name": "林达华",
                "director_id": 1002,
                "advisor_names": ["林达华", "刘亚"],
                "advisor_ids": [1002, 1001],
                "advisor_relation_ids": [11, 12],
                "is_enabled": True,
                "created_date": "2026-04-21",
                "member_student_count": 2,
                "active_student_count": 2,
            },
            {
                "id": 2,
                "center_name": "前沿探索中心",
                "director_name": "刘亚",
                "director_id": 1001,
                "advisor_names": ["刘亚"],
                "advisor_ids": [1001],
                "advisor_relation_ids": [13],
                "is_enabled": True,
                "created_date": "2026-04-21",
                "member_student_count": 1,
                "active_student_count": 1,
            },
        ]
        filtered = [item for item in items if director_id is None or item["director_id"] == director_id]
        return filtered, len(filtered)

    fake_postgres.list_centers_page = list_centers_page
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    response = store.get_centers(director_id=1002)

    assert response.total == 1
    assert response.items[0].center_name == "智能制造联合团队"
    assert response.items[0].director_name == "林达华"
    assert response.items[0].director_id == 1002


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


def test_recruitment_application_record_allows_nullable_intended_field() -> None:
    record = RecruitApplicationRecord(
        id=27,
        plan_id=1,
        business_key="ZSLQSP202605010027",
        student_name="注册学生",
        graduation_school="江南大学",
        highest_degree="硕士",
        intended_field=None,
        material_status="材料齐全",
        application_status="报名已提交",
    )

    assert record.intended_field is None


def test_get_portal_profile_options_places_masses_after_league_member(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_postgres.dict_options_map["student_political_status"] = [
        {"label": "民盟盟员", "value": "民盟盟员"},
        {"label": "群众", "value": "群众"},
        {"label": "共青团员", "value": "共青团员"},
        {"label": "中共党员", "value": "中共党员"},
    ]
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()

    values = [item.value for item in store.get_portal_profile_options().political_status_options]

    assert values.index("群众") == values.index("共青团员") + 1


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


def test_create_role_uses_relational_sync(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    record = store.create_role(
        RoleUpsert(
            role_code="quality_reviewer",
            role_name="质量审核员",
            scope_name="系统治理",
            permissions=[],
        )
    )

    assert record.role_code == "quality_reviewer"
    assert len(fake_postgres.synced_roles) == 1
    assert fake_postgres.synced_roles[0]["role_payload"]["role_name"] == "质量审核员"
    assert fake_postgres.synced_roles[0]["counters"]["roles"] == store._counters["roles"]


def test_get_workflow_task_detail_prefers_postgres_snapshot(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_postgres.workflow_task_snapshot = {
        "id": 88,
        "workflow_name": "科研报告审批",
        "business_module": "培养管理",
        "business_key": "SR-20260401-0001",
        "title": "科研报告审批任务",
        "applicant_name": "张三",
        "current_handler": "导师组",
        "current_node": "导师审核",
        "priority": "高",
        "status": "待处理",
        "created_at": "2026-04-01 09:00:00",
        "due_at": "2026-04-03 18:00:00",
        "flow_code": "scientific_report",
        "node_key": "advisor_review",
        "entity_id": 12,
        "candidate_groups": ["advisors"],
        "history": [
            {
                "operated_at": "2026-04-01 09:00:00",
                "operator_username": "admin",
                "operator_full_name": "管理员",
                "action": "start",
                "action_label": "发起流程",
                "from_node": "开始",
                "to_node": "导师审核",
                "result_status": "待处理",
                "comment": "已提交",
            }
        ],
    }
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    detail = store.get_workflow_task_detail(88, {"username": "advisor", "full_name": "导师", "roles": ["advisor"]})

    assert detail["task"].id == 88
    assert detail["task"].workflow_name == "科研报告审批"
    assert detail["history"][0]["action_label"] == "发起流程"


def test_update_profile_without_bound_system_user_still_persists_operation_log(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    store.state.setdefault("profiles", {})["portal-only"] = {
        "username": "portal-only",
        "full_name": "门户访客",
        "role_name": "门户用户",
        "department_name": "校外",
        "phone_number": None,
        "email": "portal@example.com",
        "theme_color": "#0f4cbd",
    }

    updated = store.update_profile(
        "portal-only",
        UserProfileUpdate(full_name="门户访客-更新", department_name="校友", phone_number="13800001111", email="portal@example.com", theme_color="#123456"),
    )

    assert updated.full_name == "门户访客-更新"
    assert len(fake_postgres.synced_operation_logs) == 1
    assert fake_postgres.synced_operation_logs[0]["operation_log"]["entity_id"] == "portal-only"


def test_delete_recruitment_plan_removes_plan_and_syncs_incrementally(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_recruitment_plan(_build_plan_payload("2026 待删除计划"))

    store.delete_recruitment_plan(created.id)

    assert all(item["id"] != created.id for item in store.state["recruitment_plans"])
    assert fake_postgres.deleted_recruitment_plan_ids == [created.id]


def test_delete_recruitment_plan_rejects_when_applications_exist(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()

    with pytest.raises(ValueError, match="当前招生计划下仍有报名申请，不能删除"):
        store.delete_recruitment_plan(1)


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
            id_number="320000199902022221",
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
            id_number="320000199903033336",
            password="Secret123!",
        )
    )

    fake_mailer.portal_registration_calls.clear()
    store.reset_portal_student_password(
        PortalPasswordResetRequest(
            account="password-reset@example.com",
            id_number="320000199903033336",
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


def test_execute_workflow_action_creates_student_master_and_sends_reject_email(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009999",
            email="candidate-email@example.com",
            full_name="邮件联调考生",
            id_number="32000019990101123X",
            password="Secret123!",
        )
    )
    applicant_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "candidate-email@example.com")
    application = store.submit_portal_application(
        applicant_id,
        _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name),
    )

    approve_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == application.application_business_key)
    store.execute_workflow_action(
        approve_task_id,
        "approve",
        None,
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    created_student = next(item for item in store.state["students"] if item["full_name"] == "邮件联调考生")
    assert created_student["full_name"] == "邮件联调考生"
    assert created_student["team_name"] == available_team.team_name
    assert created_student["advisor_name"] == "刘亚"
    assert created_student["student_no"].startswith("D")

    rejected_application = store.create_recruitment_application(
        _build_recruitment_application_payload().model_copy(update={"email": "candidate-reject@example.com", "phone_number": "13800009998", "id_number": "32000019990101124X", "student_name": "驳回联调考生"}),
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )
    reject_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == rejected_application.business_key)
    store.execute_workflow_action(
        reject_task_id,
        "reject",
        "材料信息不足",
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    assert fake_mailer.recruitment_status_calls[-1] == {
        "student_name": "驳回联调考生",
        "email": "candidate-reject@example.com",
        "business_key": rejected_application.business_key,
        "application_status": "驳回重填",
        "plan_name": "2026 秋季博士招生",
    }


def test_execute_workflow_action_creates_student_master_with_portal_student_id(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009999",
            email="candidate-email@example.com",
            full_name="邮件联调考生",
            id_number="32000019990101123X",
            password="Secret123!",
        )
    )

    applicant_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "candidate-email@example.com")
    application = store.submit_portal_application(
        applicant_id,
        _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name),
    )

    approve_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == application.application_business_key)
    store.execute_workflow_action(
        approve_task_id,
        "approve",
        None,
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    created_student = next(item for item in store.state["students"] if item["full_name"] == "邮件联调考生")
    assert created_student["portal_student_id"] == applicant_id
    assert fake_postgres.created_students[-1]["student_payload"]["portal_student_id"] == applicant_id


def test_rejected_portal_application_resets_submission_and_allows_resubmit(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009966",
            email="resubmit-student@example.com",
            full_name="驳回重填学生",
            id_number="320000199909099934",
            password="Secret123!",
        )
    )
    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "resubmit-student@example.com")
    payload = _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name)
    first_submit = store.submit_portal_application(student_id, payload)

    reject_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == first_submit.application_business_key)
    store.execute_workflow_action(
        reject_task_id,
        "reject",
        "请补充材料后重新提交",
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    portal_student = next(item for item in store.state["portal_students"] if item["id"] == student_id)
    latest_application = next(item for item in store.state["recruitment_applications"] if item["business_key"] == first_submit.application_business_key)
    assert portal_student["submitted_at"] is None
    assert latest_application["application_status"] == "驳回重填"
    assert fake_postgres.updated_recruitment_applications[-1]["application_id"] == latest_application["id"]
    assert fake_postgres.updated_recruitment_applications[-1]["payload"]["application_status"] == "驳回重填"
    assert fake_postgres.updated_portal_students[-1]["student_payload"]["id"] == student_id
    assert fake_postgres.updated_portal_students[-1]["student_payload"]["submitted_at"] is None

    second_submit = store.submit_portal_application(student_id, payload)
    assert second_submit.application_status == "报名已提交"


def test_execute_workflow_action_returns_current_detail_for_duplicate_terminal_reject(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    rejected_application = store.create_recruitment_application(
        _build_recruitment_application_payload().model_copy(
            update={
                "email": "candidate-duplicate-reject@example.com",
                "phone_number": "13800009977",
                "id_number": "32000019990101127X",
                "student_name": "重复驳回联调考生",
            }
        ),
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )
    reject_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == rejected_application.business_key)

    first_result = store.execute_workflow_action(
        reject_task_id,
        "reject",
        "材料信息不足",
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )
    second_result = store.execute_workflow_action(
        reject_task_id,
        "reject",
        "材料信息不足",
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    assert first_result["task"].status == "已驳回"
    assert second_result["task"].status == "已驳回"
    assert second_result["task"].id == reject_task_id
    assert len(second_result["history"]) == len(first_result["history"])
    assert second_result["history"][-1]["action"] == "reject"


def test_get_registered_portal_students_marks_returned_forms(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009965",
            email="returned-student@example.com",
            full_name="状态联调学生",
            id_number="320000199909099918",
            password="Secret123!",
        )
    )
    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "returned-student@example.com")
    payload = _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name)
    first_submit = store.submit_portal_application(student_id, payload)
    reject_task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == first_submit.application_business_key)
    store.execute_workflow_action(
        reject_task_id,
        "reject",
        "退回补充",
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    response = store.get_registered_portal_students(page=1, page_size=20)
    returned_record = next(item for item in response.items if item.email == "returned-student@example.com")
    assert returned_record.application_form_status == "驳回重填"
    assert returned_record.recruitment_application_status == "驳回重填"
    assert returned_record.submitted_at is None


def test_update_recruitment_application_persists_full_state(monkeypatch) -> None:
    from app.schemas.recruitment import RecruitApplicationUpsert

    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_recruitment_application(_build_recruitment_application_payload())

    updated = store.update_recruitment_application(
        created.id,
        RecruitApplicationUpsert(
            plan_id=created.plan_id,
            student_name="已更新考生",
            graduation_school="复旦大学",
            highest_degree="博士",
            intended_field="具身智能",
            email="candidate-email@example.com",
            phone_number="13800009999",
            id_number="32000019990101123X",
            material_status="材料齐全",
            application_status="报名已提交",
            source_channel="导师推荐",
            source_channel_other="校友引荐",
        ),
    )

    assert updated.student_name == "已更新考生"
    assert updated.graduation_school == "复旦大学"
    assert updated.intended_field == "具身智能"
    assert updated.material_status == "材料齐全"
    assert fake_postgres.saved_states
    saved_application = next(item for item in fake_postgres.saved_states[-1]["recruitment_applications"] if item["id"] == created.id)
    assert saved_application["student_name"] == "已更新考生"
    assert saved_application["graduation_school"] == "复旦大学"
    assert saved_application["intended_field"] == "具身智能"
    assert saved_application["source_channel"] == "导师推荐"
    assert saved_application["source_channel_other"] == "校友引荐"


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
            id_number="320000199904044440",
            password="Secret123!",
        )
    )

    assert fake_mailer.portal_registration_calls == []


def test_send_portal_registration_email_code_writes_cache_and_sends_email(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    store = RuntimeManagementStore()

    response = store.send_portal_registration_email_code("verify@example.com")

    code_key = store._portal_registration_email_code_key("verify@example.com")
    cooldown_key = store._portal_registration_email_cooldown_key("verify@example.com")
    assert response.cooldown_seconds == 60
    assert response.expires_in_seconds == 600
    assert len(fake_cache.get(code_key) or "") == 6
    assert fake_cache.ttl(cooldown_key) == 60
    assert fake_mailer.custom_message_calls[-1]["to_email"] == "verify@example.com"
    assert fake_cache.get(code_key) in fake_mailer.custom_message_calls[-1]["text_body"]


def test_send_portal_login_email_code_writes_cache_and_sends_email(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_mailer = FakeNotificationEmailService()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.NotificationEmailService", lambda: fake_mailer)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001234",
            email="login-verify@example.com",
            full_name="验证码登录学生",
            id_number="320000199909099993",
            password="Secret123!",
        )
    )

    response = store.send_portal_login_email_code("login-verify@example.com")

    code_key = store._portal_login_email_code_key("login-verify@example.com")
    cooldown_key = store._portal_login_email_cooldown_key("login-verify@example.com")
    assert response.cooldown_seconds == 60
    assert response.expires_in_seconds == 600
    assert len(fake_cache.get(code_key) or "") == 6
    assert fake_cache.ttl(cooldown_key) == 60
    assert fake_mailer.custom_message_calls[-1]["to_email"] == "login-verify@example.com"
    assert fake_cache.get(code_key) in fake_mailer.custom_message_calls[-1]["text_body"]


def test_login_portal_student_by_email_code_succeeds_and_clears_code(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001235",
            email="email-code-login@example.com",
            full_name="邮箱验证码学生",
            id_number="320000199909099969",
            password="Secret123!",
        )
    )
    fake_cache.set(store._portal_login_email_code_key("email-code-login@example.com"), "123456", ex=600)
    fake_cache.set(store._portal_login_email_cooldown_key("email-code-login@example.com"), "1", ex=60)

    record = store.login_portal_student_by_email_code("email-code-login@example.com", "123456")

    assert record.email == "email-code-login@example.com"
    assert fake_cache.get(store._portal_login_email_code_key("email-code-login@example.com")) is None


def test_login_portal_student_normalizes_datetime_submitted_at(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalLoginRequest, PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001237",
            email="datetime-login@example.com",
            full_name="时间登录学生",
            id_number="320000199909099969",
            password="Secret123!",
        )
    )

    student = next(item for item in store.state["portal_students"] if item["email"] == "datetime-login@example.com")
    student["submitted_at"] = datetime(2026, 5, 1, 10, 20, 30)
    student["application_draft"] = {"submitted_at": datetime(2026, 5, 1, 10, 20, 30)}

    record = store.login_portal_student(PortalLoginRequest(account="datetime-login@example.com", password="Secret123!"))

    assert record.submitted_at == "2026-05-01 10:20:30"
    assert record.application_draft is not None
    assert record.application_draft.submitted_at == "2026-05-01 10:20:30"


def test_get_portal_student_refreshes_stale_runtime_submission_state(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    response = store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001238",
            email="portal-refresh@example.com",
            full_name="刷新状态学生",
            id_number="320000199909099985",
            password="Secret123!",
        )
    )

    student_id = response.student.id
    runtime_student = next(item for item in store.state["portal_students"] if item["id"] == student_id)
    runtime_student["submitted_at"] = "2026-04-20 10:00:00"
    runtime_student["application_draft"] = {"submitted_at": "2026-04-20 10:00:00"}

    def _get_portal_student_detail(_: int) -> dict:
        return {**runtime_student, "submitted_at": None, "application_draft": {"submitted_at": None}}

    fake_postgres.get_portal_student_detail = _get_portal_student_detail

    record = store.get_portal_student(student_id)

    assert record.submitted_at is None
    assert record.application_draft is not None
    assert record.application_draft.submitted_at is None
    assert runtime_student["submitted_at"] is None


def test_save_portal_application_draft_uses_refreshed_portal_student_state(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalApplicationDraftUpsert, PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    response = store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001239",
            email="portal-draft-refresh@example.com",
            full_name="刷新草稿学生",
            id_number="320000199909099993",
            password="Secret123!",
        )
    )

    student_id = response.student.id
    runtime_student = next(item for item in store.state["portal_students"] if item["id"] == student_id)
    runtime_student["submitted_at"] = "2026-04-20 10:00:00"
    runtime_student["application_draft"] = {"submitted_at": "2026-04-20 10:00:00"}

    def _get_portal_student_detail(_: int) -> dict:
        return {**runtime_student, "submitted_at": None, "application_draft": {"submitted_at": None}}

    fake_postgres.get_portal_student_detail = _get_portal_student_detail

    payload = _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name)
    record = store.save_portal_application_draft(student_id, PortalApplicationDraftUpsert.model_validate(payload.model_dump(mode="python")))

    assert record.submitted_at is None
    assert fake_postgres.updated_portal_students[-1]["student_payload"]["submitted_at"] is None


def test_login_portal_student_by_email_code_rejects_wrong_code(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800001236",
            email="email-code-login-wrong@example.com",
            full_name="验证码错误学生",
            id_number="320000199909099977",
            password="Secret123!",
        )
    )
    fake_cache.set(store._portal_login_email_code_key("email-code-login-wrong@example.com"), "654321", ex=600)

    with pytest.raises(ValueError, match="邮件验证码不正确"):
        store.login_portal_student_by_email_code("email-code-login-wrong@example.com", "123456")


def test_validate_portal_registration_email_code_rejects_wrong_code(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    store = RuntimeManagementStore()
    fake_cache.set(store._portal_registration_email_code_key("verify@example.com"), "654321", ex=600)

    with pytest.raises(ValueError, match="邮件验证码不正确"):
        store.validate_portal_registration_email_code("verify@example.com", "123456")


def test_clear_portal_registration_email_code_removes_cached_code(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    fake_cache = FakeCacheClient()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)
    monkeypatch.setattr("app.services.management_service.get_cache_client", lambda: fake_cache)

    store = RuntimeManagementStore()
    code_key = store._portal_registration_email_code_key("verify@example.com")
    cooldown_key = store._portal_registration_email_cooldown_key("verify@example.com")
    fake_cache.set(code_key, "123456", ex=600)
    fake_cache.set(cooldown_key, "1", ex=60)

    store.clear_portal_registration_email_code("verify@example.com")

    assert fake_cache.get(code_key) is None
    assert fake_cache.get(cooldown_key) is None


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
                id_number="320000199905055563",
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
            id_number="32000019990606666X",
            password="Secret123!",
        )
    )
    with pytest.raises(ValueError, match="该邮箱已注册，请直接登录"):
        store.register_portal_student(
            PortalRegistrationRequest(
                phone_number="13800005556",
                email="portal-student@example.com",
                full_name="同邮箱学生",
                id_number="320000199906066678",
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
            id_number="32000019990101123X",
            password="Secret123!",
        )
    )
    with pytest.raises(ValueError, match="该身份证号已注册，请使用找回密码"):
        store.register_portal_student(
            PortalRegistrationRequest(
                phone_number="13800006667",
                email="different-id-check@example.com",
                full_name="同身份证学生",
                id_number="32000019990101123X",
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
            id_number="320000199907077774",
            password="Secret123!",
        )
    )

    assert response.student.full_name == "张三"
    assert response.student.phone_number == "13800007777"


def test_get_registered_portal_students_marks_submission_status(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800008888",
            email="submitted-student@example.com",
            full_name="已报名学生",
            id_number="320000199908088889",
            password="Secret123!",
        )
    )
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009998",
            email="registered-only@example.com",
            full_name="未报名学生",
            id_number="320000199909099985",
            password="Secret123!",
        )
    )

    submitted_student_id = next(
        item["id"] for item in store.state["portal_students"] if item["email"] == "submitted-student@example.com"
    )
    store.submit_portal_application(
        submitted_student_id,
        _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name),
    )

    response = store.get_registered_portal_students(page=1, page_size=20)
    status_map = {item.email: item.application_form_status for item in response.items}
    submitted_record = next(item for item in response.items if item.email == "submitted-student@example.com")

    assert status_map["submitted-student@example.com"] == "已填写报名"
    assert status_map["registered-only@example.com"] == "未填写报名"
    assert submitted_record.recruitment_application_id is not None
    assert submitted_record.recruitment_application_business_key


def test_get_student_stats_includes_registered_portal_student_counts(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009991",
            email="stats-submitted@example.com",
            full_name="统计已报名",
            id_number="320000199909099918",
            password="Secret123!",
        )
    )
    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009992",
            email="stats-unsubmitted@example.com",
            full_name="统计未报名",
            id_number="320000199909099926",
            password="Secret123!",
        )
    )

    submitted_student_id = next(
        item["id"] for item in store.state["portal_students"] if item["email"] == "stats-submitted@example.com"
    )
    store.submit_portal_application(
        submitted_student_id,
        _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name).model_copy(update={"graduation_school": "东南大学"}),
    )

    stats = store.get_student_stats()

    assert stats.registered_portal_total == 2
    assert stats.portal_submitted_total == 1
    assert stats.portal_unsubmitted_total == 1


def test_get_student_stats_uses_empty_formal_student_state_without_reviving_seed_centers(monkeypatch) -> None:
    class EmptyFormalStudentStateStore(FakePostgresStateStore):
        def load_student_state(self):
            return []

        def load_team_state(self):
            return [
                {
                    "id": 7,
                    "team_code": "CENTER-007",
                    "team_name": "前沿探索中心",
                    "department_name": "",
                    "discipline_name": "",
                    "lead_user_id": None,
                    "lead_advisor_name": None,
                    "advisor_names": [],
                    "advisor_ids": [],
                    "advisor_relation_ids": [],
                    "research_directions": [],
                    "status": "启用",
                    "established_on": "2026-04-30",
                    "description": None,
                },
                {
                    "id": 8,
                    "team_code": "CENTER-008",
                    "team_name": "AI For Science中心",
                    "department_name": "",
                    "discipline_name": "",
                    "lead_user_id": None,
                    "lead_advisor_name": None,
                    "advisor_names": [],
                    "advisor_ids": [],
                    "advisor_relation_ids": [],
                    "research_directions": [],
                    "status": "启用",
                    "established_on": "2026-04-30",
                    "description": None,
                },
            ]

        def load_recruitment_plan_state(self):
            return []

        def load_portal_student_state(self):
            return []

        def load_recruitment_application_state(self):
            return []

        def load_workflow_task_state(self):
            return []

    fake_postgres = EmptyFormalStudentStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    stats = store.get_student_stats()

    assert stats.total_students == 0
    assert stats.active_students == 0
    assert stats.center_total == 2
    assert stats.enabled_center_total == 2


def test_submit_portal_application_uses_incremental_portal_sync(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalApplicationUpsert, PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009990",
            email="incremental-submit@example.com",
            full_name="增量提交学生",
            id_number="32000019990909990X",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "incremental-submit@example.com")
    save_count_before_submit = len(fake_postgres.saved_states)
    response = store.submit_portal_application(
        student_id,
        _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name),
    )

    assert response.application_business_key.startswith("SH")
    assert response.application_business_key[2:6].isdigit()
    assert response.application_business_key[6:].isdigit()
    assert len(response.application_business_key) == 10
    assert len(fake_postgres.portal_application_submissions) == 1
    assert len(fake_postgres.saved_states) == save_count_before_submit


def test_migrate_workflow_runtime_normalizes_legacy_recruitment_business_key(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()
    created = store.create_recruitment_application(
        _build_recruitment_application_payload().model_copy(
            update={
                "student_name": "历史报名号考生",
                "phone_number": "13800006666",
                "email": "legacy-business-key@example.com",
                "id_number": "320000199901016666",
            }
        ),
        principal={"username": "admin", "full_name": "管理员", "roles": ["platform_admin"]},
    )

    legacy_business_key = "REC-20270301-0001"
    application = next(item for item in store.state["recruitment_applications"] if item["id"] == created.id)
    task_id = next(item["id"] for item in store.state["workflow_tasks"] if item["business_key"] == created.business_key)
    workflow_task = next(item for item in store.state["workflow_tasks"] if item["id"] == task_id)

    application["business_key"] = legacy_business_key
    application["candidate_no"] = legacy_business_key
    application["applied_at"] = "2027-03-01 10:00:00"
    application["created_at"] = "2027-03-01 10:00:00"
    workflow_task["business_key"] = legacy_business_key
    workflow_task["created_at"] = "2027-03-01 10:00:00"
    workflow_task["form_summary"] = f"业务编号：{legacy_business_key}；研究方向：{application['first_choice']}"

    changed = store._migrate_workflow_runtime()

    normalized_application = next(item for item in store.state["recruitment_applications"] if item["id"] == created.id)
    normalized_task = next(item for item in store.state["workflow_tasks"] if item["id"] == task_id)

    assert changed is True
    assert normalized_application["business_key"].startswith("SH2027")
    assert len(normalized_application["business_key"]) == 10
    assert normalized_application["candidate_no"] == normalized_application["business_key"]
    assert normalized_task["business_key"] == normalized_application["business_key"]
    assert normalized_task["form_summary"].startswith(f"业务编号：{normalized_application['business_key']}；")


def test_submit_portal_application_blocks_modification_after_submission(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009989",
            email="reapply-student@example.com",
            full_name="重报学生",
            id_number="320000199909099942",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "reapply-student@example.com")
    first_submit = _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name)
    store.submit_portal_application(student_id, first_submit)

    with pytest.raises(ValueError, match="当前仅支持只读浏览"):
        store.submit_portal_application(student_id, first_submit)


def test_save_portal_application_draft_blocks_modification_after_submission(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    from app.schemas.portal import PortalApplicationDraftUpsert, PortalRegistrationRequest

    store = RuntimeManagementStore()
    available_plan = store.get_public_recruitment_plans().items[0]
    available_team = store.get_public_teams().items[0]

    store.register_portal_student(
        PortalRegistrationRequest(
            phone_number="13800009987",
            email="readonly-student@example.com",
            full_name="只读学生",
            id_number="320000199909099934",
            password="Secret123!",
        )
    )

    student_id = next(item["id"] for item in store.state["portal_students"] if item["email"] == "readonly-student@example.com")
    payload = _build_portal_application_payload(available_plan.id, available_team.team_name, available_team.lead_advisor_name)
    store.submit_portal_application(student_id, payload)

    with pytest.raises(ValueError, match="当前仅支持只读浏览"):
        store.save_portal_application_draft(student_id, PortalApplicationDraftUpsert.model_validate(payload.model_dump(mode="python")))


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
            id_number="320000199909099969",
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
            id_number="320000199909099977",
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
            id_number="320000199909099942",
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
            id_number="320000199909099950",
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


def test_recruitment_application_upsert_rejects_invalid_resident_id_number() -> None:
    from pydantic import ValidationError

    from app.schemas.recruitment import RecruitApplicationUpsert

    with pytest.raises(ValidationError, match="居民身份证号码格式不正确"):
        RecruitApplicationUpsert(
            plan_id=1,
            student_name="身份证校验考生",
            graduation_school="江南大学",
            highest_degree="硕士",
            intended_field="智能制造",
            id_type="居民身份证",
            id_number="320000199901011234",
            material_status="待审核",
            application_status="报名已提交",
        )


def test_portal_registration_request_rejects_invalid_id_number() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalRegistrationRequest

    with pytest.raises(ValidationError, match="身份证号格式不正确"):
        PortalRegistrationRequest(
            full_name="无效身份证学生",
            phone_number="13800001234",
            email="invalid-id@example.com",
            id_number="320000199901011234",
            password="Secret123!",
        )


def test_portal_registration_request_rejects_invalid_phone_or_email() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalRegistrationRequest

    with pytest.raises(ValidationError, match="手机号格式不正确|邮箱格式不正确"):
        PortalRegistrationRequest(
            full_name="联系方式无效学生",
            phone_number="12345",
            email="invalid-email",
            id_number="32000019990101123X",
            password="Secret123!",
        )


def test_recruitment_application_upsert_rejects_invalid_phone_or_email() -> None:
    from pydantic import ValidationError

    from app.schemas.recruitment import RecruitApplicationUpsert

    with pytest.raises(ValidationError, match="手机号格式不正确|邮箱格式不正确"):
        RecruitApplicationUpsert(
            plan_id=1,
            student_name="联系方式校验考生",
            graduation_school="江南大学",
            highest_degree="硕士",
            intended_field="智能制造",
            phone_number="12345",
            email="invalid-email",
            material_status="待审核",
            application_status="报名已提交",
        )


def test_user_profile_update_rejects_invalid_phone_or_email() -> None:
    from pydantic import ValidationError

    from app.schemas.auth import UserProfileUpdate

    with pytest.raises(ValidationError, match="手机号格式不正确|邮箱格式不正确"):
        UserProfileUpdate(
            full_name="测试用户",
            phone_number="12345",
            email="invalid-email",
            theme_color="#409eff",
        )


def test_student_upsert_rejects_invalid_phone_number() -> None:
    from pydantic import ValidationError

    from app.schemas.student import StudentUpsert

    with pytest.raises(ValidationError, match="手机号格式不正确"):
        StudentUpsert(
            student_no="20260001",
            full_name="测试学生",
            status="在校",
            advisor_name="刘亚",
            center_name="智能制造联合团队",
            degree_type="工程博士",
            enrollment_year=2026,
            phone_number="12345",
        )


def test_system_user_upsert_rejects_invalid_phone_number() -> None:
    from pydantic import ValidationError

    from app.schemas.system import SystemUserUpsert

    with pytest.raises(ValidationError, match="手机号格式不正确"):
        SystemUserUpsert(
            username="invalid.phone",
            full_name="测试账号",
            role_code="admin",
            department_name="信息中心",
            phone_number="12345",
            account_status="启用",
            password="Secret123!",
        )


def test_portal_application_upsert_rejects_missing_basic_required_fields() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["profile"]["full_name_pinyin"] = ""
    payload["profile"]["emergency_contact_name"] = None

    with pytest.raises(ValidationError, match="基本信息以下字段必填：姓名拼音、紧急联系人姓名"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_upsert_rejects_invalid_emergency_contact_phone() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["profile"]["emergency_contact_phone"] = "12345"

    with pytest.raises(ValidationError, match="紧急联系人手机格式不正确"):
        PortalApplicationUpsert.model_validate(payload)


def test_build_portal_student_record_tolerates_invalid_legacy_emergency_contact_phone(monkeypatch) -> None:
    fake_postgres = FakePostgresStateStore()
    monkeypatch.setattr("app.services.management_service.PostgresStateStore", lambda: fake_postgres)

    store = RuntimeManagementStore()

    record = store._build_portal_student_record(
        {
            "id": 7,
            "full_name": "历史数据学生",
            "phone_number": "13800001111",
            "email": "legacy-portal@example.com",
            "id_number": "32000019990101123X",
            "account_status": "启用",
            "profile": {
                "full_name_pinyin": "LI SHI",
                "emergency_contact_name": "家长",
                "emergency_contact_phone": "1",
            },
        }
    )

    assert record.profile is not None
    assert record.profile.emergency_contact_phone is None


def test_portal_application_upsert_requires_source_channel_other_when_needed() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["source_channel"] = "其他"
    payload["source_channel_other"] = ""

    with pytest.raises(ValidationError, match="选择“其他”来源时，请补充说明"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_upsert_requires_source_channel() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["source_channel"] = ""

    with pytest.raises(ValidationError, match="请选择了解项目方式"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_upsert_requires_submission_declaration() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["signed_agreement"] = False
    payload["declaration"]["has_read_declaration"] = False

    with pytest.raises(ValidationError, match="请先确认提交声明"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_upsert_rejects_missing_english_certificate_attachment() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["english_proficiencies"][0]["certificate_attachment_url"] = ""

    with pytest.raises(ValidationError, match="英语能力1必须上传英语证明附件"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_upsert_rejects_personal_statement_over_1200_chars() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["personal_statement"]["personal_statement_text"] = "甲" * 1201

    with pytest.raises(ValidationError, match="个人陈述需控制在 1200 字以内"):
        PortalApplicationUpsert.model_validate(payload)


def test_portal_application_draft_upsert_rejects_missing_required_fields() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationDraftUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["profile"]["full_name_pinyin"] = ""

    with pytest.raises(ValidationError, match="基本信息以下字段必填：姓名拼音"):
        PortalApplicationDraftUpsert.model_validate(payload)


def test_portal_application_draft_upsert_validates_only_current_section_when_scope_provided() -> None:
    from app.schemas.portal import PortalApplicationDraftUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["validation_section_id"] = "basic-section"
    payload["profile"]["full_name_pinyin"] = "测试学生"
    payload["signed_agreement"] = False
    payload["declaration"]["has_read_declaration"] = False
    payload["english_proficiencies"] = []

    validated = PortalApplicationDraftUpsert.model_validate(payload)

    assert validated.validation_section_id == "basic-section"


def test_portal_application_draft_upsert_allows_current_bachelor_section_without_degree_and_graduation_attachments() -> None:
    from app.schemas.portal import PortalApplicationDraftUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["validation_section_id"] = "education-section"
    payload["education_experiences"] = [
        {
            "sort_order": 1,
            "education_stage": "高中毕业",
            "start_month": "2016-09",
            "end_month": "2019-06",
            "school_name": "无锡市第一中学",
            "verifier_name": "王老师",
            "verifier_phone": "13800002222",
        },
        {
            "sort_order": 2,
            "education_stage": "本科在读",
            "start_month": "2019-09",
            "school_name": "江南大学",
            "major_name": "自动化",
            "average_score": "89",
            "gpa": "3.8",
            "ranking": "12/120",
            "transcript_attachment_url": "/portal-attachments/uploads/student-7/education_transcript/transcript-a.pdf",
            "degree_certificate_attachment_url": "",
            "graduation_certificate_attachment_url": "",
            "verifier_name": "李老师",
            "verifier_phone": "13800003333",
        },
    ]

    validated = PortalApplicationDraftUpsert.model_validate(payload)

    assert validated.validation_section_id == "education-section"


def test_portal_application_draft_upsert_rejects_missing_degree_and_graduation_attachments_for_graduated_bachelor_section() -> None:
    from pydantic import ValidationError

    from app.schemas.portal import PortalApplicationDraftUpsert

    payload = _build_portal_application_payload(1, "智能制造联合团队", "刘亚").model_dump(mode="python")
    payload["validation_section_id"] = "education-section"
    payload["education_experiences"] = [
        {
            "sort_order": 1,
            "education_stage": "高中毕业",
            "start_month": "2016-09",
            "end_month": "2019-06",
            "school_name": "无锡市第一中学",
            "verifier_name": "王老师",
            "verifier_phone": "13800002222",
        },
        {
            "sort_order": 2,
            "education_stage": "本科毕业",
            "start_month": "2019-09",
            "end_month": "2023-06",
            "school_name": "江南大学",
            "major_name": "自动化",
            "average_score": "89",
            "gpa": "3.8",
            "ranking": "12/120",
            "transcript_attachment_url": "/portal-attachments/uploads/student-7/education_transcript/transcript-a.pdf",
            "degree_certificate_attachment_url": "",
            "graduation_certificate_attachment_url": "",
            "verifier_name": "李老师",
            "verifier_phone": "13800003333",
        },
        {
            "sort_order": 3,
            "education_stage": "硕士在读",
            "start_month": "2023-09",
            "school_name": "江南大学",
            "major_name": "控制科学与工程",
            "average_score": "91",
            "gpa": "3.9",
            "ranking": "8/60",
            "transcript_attachment_url": "/portal-attachments/uploads/student-7/education_transcript/transcript-b.pdf",
            "verifier_name": "周老师",
            "verifier_phone": "13800005555",
        },
    ]

    with pytest.raises(ValidationError, match="教育经历2以下字段必填：学位证附件、毕业证附件"):
        PortalApplicationDraftUpsert.model_validate(payload)
