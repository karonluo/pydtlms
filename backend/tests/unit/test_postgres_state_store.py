import pytest

from app.services.postgres_state_store import PostgresStateStore


class FakeCursor:
    def __init__(self, fetchone_results=None, fetchall_results=None) -> None:
        self.fetchone_results = list(fetchone_results or [])
        self.fetchall_results = list(fetchall_results or [])
        self.executed: list[tuple[str, object]] = []

    def execute(self, sql, params=None) -> None:
        self.executed.append((sql, params))

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

    def fetchall(self):
        if self.fetchall_results:
            return self.fetchall_results.pop(0)
        return []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self.cursor_instance = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self) -> None:
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_build_dsn_includes_connect_timeout() -> None:
    store = PostgresStateStore()

    dsn = store._build_dsn("db_dtlms", "postgres")

    assert "dbname=db_dtlms" in dsn
    assert "user=postgres" in dsn
    assert f"connect_timeout={store.CONNECT_TIMEOUT_SECONDS}" in dsn


def test_schema_initialized_returns_true_when_formal_schema_exists() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchone_results=[("public.dtlms_users",)])

    assert store._schema_initialized(cursor) is True


def test_ensure_schema_skips_sql_execution_when_schema_exists(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_database", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name, autocommit=False: connection)
    monkeypatch.setattr(store, "_schema_initialized", lambda cur: True)

    store.ensure_schema()

    assert store._schema_ready is True
    assert cursor.executed == []


def test_ensure_schema_raises_when_schema_missing(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchall_results=[[]])
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_database", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name, autocommit=False: connection)
    monkeypatch.setattr(store, "_schema_initialized", lambda cur: False)

    with pytest.raises(RuntimeError, match="Automatic SQL file execution has been disabled"):
        store.ensure_schema()

    assert store._schema_ready is False
    assert cursor.executed == []


def test_normalize_system_user_row_preserves_email() -> None:
    row = PostgresStateStore._normalize_system_user_row(
        {
            "id": 12,
            "username": "ops.user",
            "full_name": "运维用户",
            "role_code": "ops",
            "role_name": "运维",
            "department_name": "信息中心",
            "email": "ops.user@example.com",
            "phone_number": "13800001111",
            "account_status": "启用",
            "last_login_at": None,
        }
    )

    assert row["email"] == "ops.user@example.com"


def test_seed_portal_application_structures_uses_application_id_for_personal_statement_attachment() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()
    state = {
        "portal_students": [
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "profile": {
                    "gender": "男",
                },
                "application_draft": {
                    "preferences": [],
                    "education_experiences": [],
                    "practice_experiences": [],
                    "english_proficiencies": [],
                    "family_members": [],
                    "achievement_records": [],
                    "personal_statement": {
                        "personal_statement_text": "真实联调提交",
                        "resume_attachment_url": "/portal-attachments/uploads/student-7/resume/resume-a.pdf",
                    },
                    "declaration": {
                        "has_read_declaration": True,
                        "declaration_text": "本人承诺以上填写内容真实、准确。",
                    },
                },
            }
        ],
        "recruitment_applications": [
            {
                "id": 15,
                "portal_student_id": 7,
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "personal_statement_attachment": None,
                "material_list_attachment": None,
            }
        ],
    }

    store._seed_portal_application_structures(cursor, state)

    personal_statement_sql = [sql for sql, _ in cursor.executed if "dtlms_portal_application_personal_statements" in sql]
    attachment_rows = [params for sql, params in cursor.executed if "dtlms_portal_application_attachments" in sql]

    assert len(personal_statement_sql) == 1
    assert "RETURNING id" not in personal_statement_sql[0]
    assert attachment_rows == [
        (7, 15, "personal_statement", 15, "resume", "resume-a.pdf", "/portal-attachments/uploads/student-7/resume/resume-a.pdf", "pdf")
    ]


def test_seed_portal_application_structures_achievement_insert_placeholder_count_matches_params() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchone_results=[(31,)])
    state = {
        "portal_students": [
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "application_draft": {
                    "preferences": [],
                    "education_experiences": [],
                    "practice_experiences": [],
                    "english_proficiencies": [],
                    "family_members": [],
                    "achievement_records": [
                        {
                            "achievement_type": "获奖经历",
                            "paper_title": None,
                            "author_order": None,
                            "journal_or_conference": None,
                            "publish_or_index_month": None,
                            "achievement_month": "2024-08",
                            "award_name": "数学建模竞赛",
                            "award_rank": "一等奖",
                            "award_certificate_attachment_url": "/portal-attachments/uploads/student-7/achievement_award_certificate/math-modeling.pdf",
                            "award_certificate_attachment_name": "math-modeling.pdf",
                            "awarding_organization": "教育部",
                            "award_level": "国家级",
                            "award_year": "2024",
                            "description_text": "获奖描述",
                            "responsibility_text": "承担算法设计",
                        }
                    ],
                    "personal_statement": {},
                    "declaration": {},
                },
            }
        ],
        "recruitment_applications": [
            {
                "id": 15,
                "portal_student_id": 7,
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "personal_statement_attachment": None,
                "material_list_attachment": None,
            }
        ],
    }

    store._seed_portal_application_structures(cursor, state)

    achievement_sql, achievement_params = next(
        (sql, params)
        for sql, params in cursor.executed
        if "INSERT INTO dtlms_portal_application_achievement_records" in sql
    )

    assert achievement_sql.count("%s") == len(achievement_params)
    assert len(achievement_params) == 15


def test_list_registered_portal_students_page_returns_application_identifiers(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[{"total": 1}],
        fetchall_results=[[
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "id_number": "32000019990101123X",
                "account_status": "启用",
                "selected_plan_name": "2026博士招生",
                "selected_team_name": "智能制造联合团队",
                "selected_advisor_name": "刘亚",
                "created_at": "2026-04-01 10:00:00",
                "submitted_at": "2026-04-20 10:00:00",
                "recruitment_application_id": 15,
                "recruitment_application_business_key": "RECRUIT-20260420-0015",
                "application_status": "submitted",
                "applied_at": "2026-04-20 10:00:00",
            }
        ]],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    items, total = store.list_registered_portal_students_page(page=1, page_size=10)

    assert total == 1
    assert items[0]["recruitment_application_id"] == 15
    assert items[0]["recruitment_application_business_key"] == "RECRUIT-20260420-0015"
    assert items[0]["application_form_status"] == "已填写报名"


def test_list_registered_portal_students_page_marks_returned_forms(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[{"total": 1}],
        fetchall_results=[[
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "id_number": "32000019990101123X",
                "account_status": "启用",
                "selected_plan_name": "2026博士招生",
                "selected_team_name": "智能制造联合团队",
                "selected_advisor_name": "刘亚",
                "created_at": "2026-04-01 10:00:00",
                "submitted_at": None,
                "recruitment_application_id": 15,
                "recruitment_application_business_key": "RECRUIT-20260420-0015",
                "application_status": "returned",
                "applied_at": "2026-04-20 10:00:00",
            }
        ]],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    items, total = store.list_registered_portal_students_page(page=1, page_size=10)

    assert total == 1
    assert items[0]["application_form_status"] == "驳回重填"


def test_sync_recruitment_application_status_falls_back_to_db_portal_student_id(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchone_results=[(7,)])
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    store.sync_recruitment_application_status(15, {"application_status": "驳回重填"})

    assert connection.committed is True
    assert cursor.executed[0] == (
        "SELECT portal_student_id FROM dtlms_recruitment_applications WHERE id = %s AND is_deleted = FALSE",
        (15,),
    )
    assert cursor.executed[1][1] == ("returned", 15)
    assert cursor.executed[2][1] == (7,)


def test_get_portal_student_detail_hides_submitted_at_for_returned_application(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "id_number": "32000019990101123X",
                "account_status": "启用",
                "selected_plan_id": 3,
                "selected_team_id": None,
                "selected_team_name": None,
                "selected_advisor_user_id": None,
                "selected_advisor_name": None,
                "submitted_at": "2026-04-20 10:00:00",
                "signed_agreement": True,
            },
            {
                "id": 15,
                "plan_id": 3,
                "business_key": "RECRUIT-20260420-0015",
                "candidate_no": "RECRUIT-20260420-0015",
                "source_channel": "上海人工智能实验室官网",
                "source_channel_other": None,
                "intended_advisor_name": "刘亚",
                "application_status": "returned",
                "applied_at": "2026-04-20 10:00:00",
                "first_choice_team_id": None,
                "second_choice_team_id": None,
                "intended_advisor_user_id": None,
            },
            None,
            None,
        ],
        fetchall_results=[[], [], [], [], [], [], []],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    item = store.get_portal_student_detail(7)

    assert item is not None
    assert item["submitted_at"] is None
    assert item["application_draft"]["submitted_at"] is None


def test_get_portal_student_detail_hides_submitted_at_for_rejected_application(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "id_number": "32000019990101123X",
                "account_status": "启用",
                "selected_plan_id": 3,
                "selected_team_id": None,
                "selected_team_name": None,
                "selected_advisor_user_id": None,
                "selected_advisor_name": None,
                "submitted_at": "2026-04-20 10:00:00",
                "signed_agreement": True,
            },
            {
                "id": 15,
                "plan_id": 3,
                "business_key": "RECRUIT-20260420-0015",
                "candidate_no": "RECRUIT-20260420-0015",
                "source_channel": "上海人工智能实验室官网",
                "source_channel_other": None,
                "intended_advisor_name": "刘亚",
                "application_status": "rejected",
                "applied_at": "2026-04-20 10:00:00",
                "first_choice_team_id": None,
                "second_choice_team_id": None,
                "intended_advisor_user_id": None,
            },
            None,
            None,
        ],
        fetchall_results=[[], [], [], [], [], [], []],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    item = store.get_portal_student_detail(7)

    assert item is not None
    assert item["submitted_at"] is None
    assert item["application_draft"]["submitted_at"] is None


def test_get_portal_student_detail_prefers_saved_draft_over_existing_application(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[
            {
                "id": 7,
                "full_name": "张三",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "id_number": "32000019990101123X",
                "account_status": "启用",
                "selected_plan_id": 3,
                "selected_team_id": 11,
                "selected_team_name": "旧研究中心",
                "selected_advisor_user_id": 21,
                "selected_advisor_name": "旧导师",
                "submitted_at": None,
                "signed_agreement": True,
                "application_draft": {
                    "selected_plan_id": 3,
                    "source_channel": "其他",
                    "source_channel_other": "老师线下宣讲",
                    "preferences": [
                        {
                            "preference_order": 1,
                            "team_id": 12,
                            "research_center_name": "新研究中心",
                            "advisor_user_id": 22,
                            "advisor_name": "新导师",
                            "is_optional": False,
                        }
                    ],
                    "practice_experiences": [
                        {
                            "start_month": "2025-01",
                            "end_month": "2025-03",
                            "organization_name": "上海人工智能实验室",
                            "position_name": "算法实习生",
                            "responsibility_text": "参与多模态数据处理",
                            "verifier_name": "王老师",
                            "verifier_phone": "13800002222",
                        }
                    ],
                    "personal_statement": {
                        "growth_experience_text": "新的成长经历",
                        "resume_attachment_url": "/api/v1/portal/attachments/resume-new.pdf",
                        "resume_attachment_name": "resume-new.pdf",
                    },
                    "declaration": {
                        "has_read_declaration": True,
                    },
                },
            },
            {
                "id": 15,
                "plan_id": 3,
                "business_key": "RECRUIT-20260420-0015",
                "candidate_no": "RECRUIT-20260420-0015",
                "source_channel": "上海人工智能实验室官网",
                "source_channel_other": None,
                "intended_advisor_name": "旧导师",
                "application_status": "draft",
                "applied_at": None,
                "first_choice_team_id": 11,
                "second_choice_team_id": None,
                "intended_advisor_user_id": 21,
                "material_list_attachment": None,
            },
            {
                "personal_statement_text": "旧个人陈述",
                "growth_experience_text": "旧成长经历",
                "program_application_reason_text": None,
                "career_plan_text": None,
                "resume_attachment_url": "/api/v1/portal/attachments/resume-old.pdf",
                "supporting_material_attachment_url": None,
                "ai_problem_statement": None,
                "ai_industry_opinion": None,
            },
            {
                "has_read_declaration": True,
                "declaration_text": "旧声明",
                "progress_snapshot": None,
            },
        ],
        fetchall_results=[
            [
                {
                    "preference_order": 1,
                    "team_id": 11,
                    "research_center_name": "旧研究中心",
                    "advisor_user_id": 21,
                    "advisor_name": "旧导师",
                    "is_optional": False,
                }
            ],
            [],
            [],
            [],
            [],
            [],
            [],
        ],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    item = store.get_portal_student_detail(7)

    assert item is not None
    assert item["application_draft"]["source_channel"] == "其他"
    assert item["application_draft"]["source_channel_other"] == "老师线下宣讲"
    assert item["application_draft"]["preferences"][0]["research_center_name"] == "新研究中心"
    assert item["application_draft"]["preferences"][0]["advisor_name"] == "新导师"
    assert item["application_draft"]["practice_experiences"][0]["organization_name"] == "上海人工智能实验室"
    assert item["application_draft"]["personal_statement"]["growth_experience_text"] == "新的成长经历"
    assert item["application_draft"]["personal_statement"]["resume_attachment_url"] == "/api/v1/portal/attachments/resume-new.pdf"
    assert item["application_draft"]["personal_statement"]["resume_attachment_name"] == "resume-new.pdf"


def test_sync_recruitment_application_status_updates_relational_status(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    store.sync_recruitment_application_status(
        15,
        {
            "id": 15,
            "application_status": "驳回重填",
            "business_key": "RECRUIT-20260420-0015",
        },
    )

    assert len(cursor.executed) == 2
    lookup_sql, lookup_params = cursor.executed[0]
    update_sql, update_params = cursor.executed[1]
    assert "SELECT portal_student_id FROM dtlms_recruitment_applications" in lookup_sql
    assert lookup_params == (15,)
    assert "UPDATE dtlms_recruitment_applications" in update_sql
    assert update_params == ("returned", 15)


def test_sync_recruitment_application_status_clears_portal_submission_for_resubmittable_status(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)

    store.sync_recruitment_application_status(
        15,
        {
            "id": 15,
            "portal_student_id": 7,
            "application_status": "不录取",
            "business_key": "RECRUIT-20260420-0015",
        },
    )

    assert len(cursor.executed) == 2
    update_sql, update_params = cursor.executed[0]
    portal_update_sql, portal_update_params = cursor.executed[1]
    assert "UPDATE dtlms_recruitment_applications" in update_sql
    assert update_params == ("rejected", 15)
    assert "UPDATE dtlms_portal_students" in portal_update_sql
    assert portal_update_params == (7,)


def test_sync_portal_student_persists_application_draft_json(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)
    monkeypatch.setattr(store, "_sync_runtime_counters_in_tx", lambda cur, counters: None)
    monkeypatch.setattr(store, "_sync_operation_log_in_tx", lambda cur, operation_log: None)
    monkeypatch.setattr(store, "_derive_portal_profile", lambda payload: None)

    store.sync_portal_student(
        {
            "id": 7,
            "full_name": "张三",
            "phone_number": "13800001111",
            "email": "zhangsan@example.com",
            "id_number": "32000019990101123X",
            "account_status": "启用",
            "application_draft": {
                "source_channel": "其他",
                "source_channel_other": "老师宣讲",
                "preferences": [
                    {
                        "preference_order": 1,
                        "research_center_name": "具身智能中心",
                        "advisor_name": "刘亚",
                        "is_optional": False,
                    }
                ],
            },
        },
        None,
    )

    insert_sql, insert_params = cursor.executed[0]
    assert "application_draft" in insert_sql
    assert '"source_channel": "其他"' in insert_params[31]
    assert '"source_channel_other": "老师宣讲"' in insert_params[31]


def test_get_recruitment_application_detail_returns_full_portal_v2_sections(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(
        fetchone_results=[
            {
                "id": 15,
                "plan_id": 3,
                "business_key": "SH20270001",
                "portal_student_id": 7,
                "candidate_no": "SH20270001",
                "review_round": None,
                "student_name": "张三",
                "first_choice_team_id": 11,
                "first_choice": "具身智能中心",
                "second_choice_team_id": None,
                "second_choice": None,
                "gender": "男",
                "birth_date": "1999-01-01",
                "ethnic_group": "汉族",
                "political_status": "共青团员",
                "marital_status": "未婚",
                "religious_belief": "无",
                "native_place": "江苏无锡",
                "phone_number": "13800001111",
                "email": "zhangsan@example.com",
                "mailing_address": "上海市徐汇区",
                "full_name_pinyin": "ZHANG SAN",
                "profile_photo_url": "/api/v1/portal/attachments/profile.jpg",
                "id_card_collage_url": "/api/v1/portal/attachments/id-collage.jpg",
                "emergency_contact_name": "李四",
                "emergency_contact_phone": "13900002222",
                "id_type": "居民身份证",
                "id_number": "32000019990101123X",
                "graduation_school": "江南大学",
                "highest_degree": "本科毕业",
                "intended_field": "具身智能中心",
                "intended_advisor_user_id": 21,
                "intended_advisor_name": "刘亚",
                "discovery_channel": "老师宣讲",
                "source_channel": "其他",
                "source_channel_other": "老师宣讲",
                "self_evaluation": None,
                "applied_at": "2026-05-01 10:00:00",
                "research_problem": None,
                "research_status_analysis": "旧字段",
                "research_impact": None,
                "ai_society_impact": None,
                "dissenting_view": None,
                "family_info": None,
                "education_experience": None,
                "practice_experience": None,
                "personal_statement_text": None,
                "student_activity_experience": "旧活动",
                "personal_statement_attachment": None,
                "material_list_attachment": "/api/v1/portal/attachments/materials.zip",
                "supplementary_profile": "旧补充简介",
                "material_status": "submitted",
                "application_status": "submitted",
                "reviewer_name": None,
                "final_score": None,
            },
            {
                "personal_statement_text": "汇总陈述",
                "growth_experience_text": "成长经历",
                "program_application_reason_text": "申报理由",
                "career_plan_text": "职业规划",
                "resume_attachment_url": "/api/v1/portal/attachments/resume.pdf",
                "supporting_material_attachment_url": "/api/v1/portal/attachments/materials.zip",
                "ai_problem_statement": "关键科研问题",
                "ai_industry_opinion": "不同观点",
            },
            {
                "has_read_declaration": True,
                "declaration_text": "本人承诺材料真实",
                "progress_snapshot": {"preference_count": 1},
            },
        ],
        fetchall_results=[
            [],
            [{"preference_order": 1, "research_center_name": "具身智能中心", "advisor_name": "刘亚", "is_optional": False}],
            [],
            [],
            [{"id": 31, "exam_name": "IELTS", "score_text": "7.0", "certificate_attachment_url": "/api/v1/portal/attachments/ielts.pdf"}],
            [],
            [{"id": 41, "achievement_type": "获奖经历", "paper_title": None, "author_order": None, "journal_or_conference": None, "publish_or_index_month": None, "achievement_month": "2024-06", "award_name": "挑战杯", "award_rank": "一等奖", "award_certificate_attachment_url": "/api/v1/portal/attachments/award.pdf", "awarding_organization": None, "award_level": "一等奖", "award_year": "2024", "description_text": "获奖描述", "responsibility_text": "获奖描述"}],
        ],
    )
    connection = FakeConnection(cursor)

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)
    monkeypatch.setattr(store, "_resolve_attachment_name", lambda *args: {31: "ielts.pdf", 41: "award.pdf"}.get(int(args[2] or 0), ""))

    item = store.get_recruitment_application_detail(15)

    assert item is not None
    assert item["source_channel"] == "其他"
    assert item["source_channel_other"] == "老师宣讲"
    assert item["profile"]["birth_date"] == "1999-01-01"
    assert item["profile"]["ethnic_group"] == "汉族"
    assert item["profile"]["emergency_contact_name"] == "李四"
    assert len(item["english_proficiencies"]) == 1
    assert item["english_proficiencies"][0]["exam_name"] == "IELTS"
    assert item["english_proficiencies"][0]["certificate_attachment_name"] == "ielts.pdf"
    assert len(item["achievement_records"]) == 1
    assert item["achievement_records"][0]["award_name"] == "挑战杯"
    assert item["achievement_records"][0]["award_certificate_attachment_name"] == "award.pdf"
    assert item["personal_statement"]["growth_experience_text"] == "成长经历"
    assert item["personal_statement"]["program_application_reason_text"] == "申报理由"
    assert item["personal_statement"]["career_plan_text"] == "职业规划"


def test_sync_portal_application_submission_syncs_workflow_task_when_provided(monkeypatch) -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchone_results=[None])
    connection = FakeConnection(cursor)
    synced_tasks: list[dict] = []

    monkeypatch.setattr(store, "ensure_schema", lambda: None)
    monkeypatch.setattr(store, "_connect", lambda database_name: connection)
    monkeypatch.setattr(store, "_sync_runtime_counters_in_tx", lambda cur, counters: None)
    monkeypatch.setattr(store, "_sync_operation_log_in_tx", lambda cur, operation_log: None)
    monkeypatch.setattr(store, "_derive_portal_profile", lambda portal_student_payload: None)
    monkeypatch.setattr(store, "_derive_portal_application_draft", lambda portal_student_payload: {})
    monkeypatch.setattr(store, "_execute_dynamic", lambda cur, sql, params=None: cur.execute(sql, params))
    monkeypatch.setattr(store, "_sync_workflow_task_in_tx", lambda cur, task_payload: synced_tasks.append(task_payload))

    store.sync_portal_application_submission(
        {
            "id": 7,
            "full_name": "张三",
            "phone_number": "13800001111",
            "email": "zhangsan@example.com",
            "id_number": "32000019990101123X",
            "password_hash": "hashed",
            "account_status": "启用",
            "created_at": "2026-04-01 10:00:00",
            "updated_at": "2026-04-01 10:00:00",
        },
        {
            "id": 15,
            "portal_student_id": 7,
            "plan_id": 3,
            "business_key": "RECRUIT-20260420-0015",
            "student_name": "张三",
            "application_status": "报名已提交",
            "material_status": "材料齐全",
            "created_at": "2026-04-20 10:00:00",
            "updated_at": "2026-04-20 10:00:00",
        },
        None,
        workflow_task={
            "id": 21,
            "business_key": "RECRUIT-20260420-0015",
            "status": "待处理",
            "current_node": "资格审核",
            "node_key": "qualification_review",
        },
    )

    assert synced_tasks == [
        {
            "id": 21,
            "business_key": "RECRUIT-20260420-0015",
            "status": "待处理",
            "current_node": "资格审核",
            "node_key": "qualification_review",
        }
    ]
    assert connection.committed is True


def test_derive_portal_profile_includes_id_card_collage_url() -> None:
    store = PostgresStateStore()

    profile = store._derive_portal_profile(
        {
            "profile": {
                "full_name_pinyin": "ZHANG SAN",
                "id_card_collage_url": "/portal-attachments/uploads/student-7/id_card_collage/id-card.jpg",
            }
        }
    )

    assert profile is not None
    assert profile["id_card_collage_url"].endswith("id-card.jpg")


def test_seed_portal_students_persists_application_draft_payload() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor()

    store._seed_portal_students(
        cursor,
        {
            "portal_students": [
                {
                    "id": 7,
                    "full_name": "张三",
                    "phone_number": "13800001111",
                    "email": "zhangsan@example.com",
                    "id_number": "32000019990101123X",
                    "account_status": "启用",
                    "application_draft": {
                        "selected_plan_id": 3,
                        "education_experiences": [
                            {"sort_order": 1, "education_stage": "高中毕业", "school_name": "无锡市第一中学"}
                        ],
                    },
                }
            ]
        },
        {},
    )

    insert_sql, params = next((sql, params) for sql, params in cursor.executed if "INSERT INTO dtlms_portal_students" in sql)

    assert "application_draft" in insert_sql
    assert any(isinstance(item, str) and '"selected_plan_id": 3' in item for item in params)


def test_seed_recruitment_normalizes_academic_year_range_for_plan_dates() -> None:
    store = PostgresStateStore()
    cursor = FakeCursor(fetchall_results=[[]])
    state = {
        "recruitment_plans": [
            {
                "id": 3,
                "plan_name": "跨学年招生计划",
                "academic_year": "2026-2027",
                "semester": "春",
                "plan_description": "测试跨学年时间拼接",
                "target_quota": 10,
                "current_stage": "资格审核",
                "is_open": True,
                "brochure_image_url": None,
                "interview_group_count": 0,
            }
        ],
        "recruitment_applications": [],
    }

    store._seed_recruitment(cursor, state)

    plan_insert = next(params for sql, params in cursor.executed if "INSERT INTO dtlms_recruitment_plans" in sql)
    assert plan_insert[6] == "2026-03-01 08:00:00+08"
    assert plan_insert[7] == "2026-10-31 18:00:00+08"