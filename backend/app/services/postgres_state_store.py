from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)


class PostgresStateStore:
    DATASET_TABLES: dict[str, str] = {
        "profiles": "dtlms_runtime_profiles",
        "students": "dtlms_runtime_students",
        "recruitment_plans": "dtlms_runtime_recruitment_plans",
        "recruitment_applications": "dtlms_runtime_recruitment_applications",
        "training_plans": "dtlms_runtime_training_plans",
        "scientific_reports": "dtlms_runtime_scientific_reports",
        "outbound_studies": "dtlms_runtime_outbound_studies",
        "theses": "dtlms_runtime_theses",
        "thesis_reviews": "dtlms_runtime_thesis_reviews",
        "roles": "dtlms_runtime_roles",
        "system_users": "dtlms_runtime_system_users",
        "audit_policies": "dtlms_runtime_audit_policies",
        "integrations": "dtlms_runtime_integrations",
        "operation_logs": "dtlms_runtime_operation_logs",
        "sync_logs": "dtlms_runtime_sync_logs",
        "workflow_tasks": "dtlms_runtime_workflow_tasks",
    }

    SQL_FILES: tuple[str, ...] = (
        "000_create_database.sql",
        "010_init_schema.sql",
        "015_team_schema_migration.sql",
        "020_views.sql",
        "030_seed_rbac.sql",
        "040_runtime_store.sql",
        "050_dict_schema.sql",
    )

    def __init__(self) -> None:
        self._schema_ready = False
        self._sql_dir = BACKEND_DIR / "sql"

    def _connection_users(self) -> list[str]:
        candidates = [settings.postgres_user]
        if settings.postgres_user == "postgre":
            candidates.append("postgres")
        return list(dict.fromkeys(candidates))

    def _build_dsn(self, database_name: str, username: str) -> str:
        return (
            f"host={settings.postgres_host} port={settings.postgres_port} "
            f"dbname={database_name} user={username} password={settings.postgres_password} client_encoding=utf8"
        )

    def _connect(self, database_name: str, autocommit: bool = False) -> psycopg.Connection[Any]:
        last_error: Exception | None = None
        for username in self._connection_users():
            try:
                return psycopg.connect(self._build_dsn(database_name, username), autocommit=autocommit)
            except Exception as exc:
                last_error = exc
        if last_error is None:
            raise RuntimeError("No PostgreSQL connection candidates configured")
        raise last_error

    def ensure_database(self) -> None:
        with self._connect("postgres", autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.postgres_db,))
                exists = cur.fetchone() is not None
                if not exists:
                    cur.execute(f'CREATE DATABASE "{settings.postgres_db}"')

    def ensure_schema(self) -> None:
        if self._schema_ready:
            return
        self.ensure_database()
        with self._connect(settings.postgres_db, autocommit=True) as conn:
            with conn.cursor() as cur:
                for file_name in self.SQL_FILES[1:]:
                    sql_text = (self._sql_dir / file_name).read_text(encoding="utf-8")
                    cur.execute(sql_text)
        self._schema_ready = True

    def load_state(self) -> dict[str, Any] | None:
        try:
            self.ensure_schema()
            with self._connect(settings.postgres_db) as conn:
                conn.row_factory = dict_row
                with conn.cursor() as cur:
                    cur.execute("SELECT to_regclass('public.dtlms_runtime_counters') AS table_name")
                    if not cur.fetchone()["table_name"]:
                        return None

                    cur.execute("SELECT counter_name, counter_value FROM dtlms_runtime_counters")
                    counters = {row["counter_name"]: int(row["counter_value"]) for row in cur.fetchall()}
                    if not counters:
                        return None

                    state: dict[str, Any] = {"counters": counters}
                    for dataset, table_name in self.DATASET_TABLES.items():
                        cur.execute(f"SELECT payload FROM {table_name} ORDER BY updated_at DESC, 1 DESC")
                        rows = [row["payload"] for row in cur.fetchall()]
                        if dataset == "profiles":
                            state[dataset] = {row["username"]: row for row in rows}
                        else:
                            state[dataset] = rows
                    return state
        except Exception as exc:
            logger.warning("Load state from PostgreSQL failed: %s", exc)
            return None

    def save_state(self, state: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE dtlms_runtime_counters")
                for counter_name, counter_value in state.get("counters", {}).items():
                    cur.execute(
                        "INSERT INTO dtlms_runtime_counters (counter_name, counter_value) VALUES (%s, %s)",
                        (counter_name, int(counter_value)),
                    )

                for dataset, table_name in self.DATASET_TABLES.items():
                    cur.execute(f"TRUNCATE TABLE {table_name}")
                    items = state.get(dataset, {})
                    if dataset == "profiles":
                        values = list(items.values())
                        for item in values:
                            cur.execute(
                                f"INSERT INTO {table_name} (username, payload) VALUES (%s, %s::jsonb)",
                                (item["username"], self._json_payload(item)),
                            )
                    else:
                        for item in items:
                            cur.execute(
                                f"INSERT INTO {table_name} (id, payload) VALUES (%s, %s::jsonb)",
                                (int(item["id"]), self._json_payload(item)),
                            )

                self._seed_relational_tables(cur, state)
            conn.commit()

    def _seed_relational_tables(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        self._seed_users_and_roles(cur, state)
        advisor_map = self._seed_advisors(cur, state)
        team_map = self._seed_teams(cur, state, advisor_map)
        student_map = self._seed_students(cur, state, advisor_map, team_map)
        plan_map = self._seed_recruitment(cur, state)
        training_plan_map = self._seed_training(cur, state, student_map, advisor_map)
        thesis_map = self._seed_degree(cur, state, student_map, advisor_map)
        self._seed_operation_logs(cur, state)
        self._seed_sync_logs(cur, state)
        self._seed_system_configs(cur, state)
        self._seed_training_plan_versions(cur, state, training_plan_map)
        self._seed_admission_decisions(cur, state, plan_map)
        self._seed_thesis_reviews(cur, state, thesis_map)

    def _seed_users_and_roles(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        from app.core.security import get_password_hash

        cur.execute("TRUNCATE TABLE dtlms_user_roles, dtlms_users RESTART IDENTITY CASCADE")
        users = state.get("system_users", [])
        profiles = state.get("profiles", {})
        role_id_map = self._fetch_map(cur, "SELECT id, role_code AS key FROM dtlms_roles")

        for item in users:
            profile = profiles.get(item["username"], {})
            password_hash = item.get("password_hash") or get_password_hash("ChangeMe@123456")
            cur.execute(
                """
                INSERT INTO dtlms_users (id, username, full_name, email, password_hash, is_active, is_deleted)
                VALUES (%s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["username"],
                    item["full_name"],
                    profile.get("email"),
                    password_hash,
                    item.get("account_status") == "启用",
                ),
            )
            role_id = role_id_map.get(item["role_code"])
            if role_id:
                cur.execute(
                    "INSERT INTO dtlms_user_roles (user_id, role_id, grant_source) VALUES (%s, %s, %s)",
                    (int(item["id"]), int(role_id), "runtime_seed"),
                )

    def _seed_advisors(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_student_advisor_history, dtlms_advisors RESTART IDENTITY CASCADE")
        names: list[str] = []
        for dataset in ("students", "training_plans", "outbound_studies", "theses"):
            for item in state.get(dataset, []):
                advisor_name = item.get("advisor_name")
                if advisor_name and advisor_name not in names:
                    names.append(advisor_name)

        advisor_map: dict[str, int] = {}
        for index, name in enumerate(names, start=1):
            title = "教授" if index % 2 else "副教授"
            organization = "智能制造学院" if name in {"刘亚", "袁野"} else "工业软件学院"
            direction = "博士生培养与过程治理" if name == "袁野" else "智能制造与工业互联网"
            cur.execute(
                """
                INSERT INTO dtlms_advisors (id, advisor_no, full_name, title, organization_name, research_direction, annual_quota, is_deleted)
                VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (index, f"ADV{index:03d}", name, title, organization, direction, 6 + index),
            )
            advisor_map[name] = index
        return advisor_map

    def _seed_teams(self, cur: psycopg.Cursor[Any], state: dict[str, Any], advisor_map: dict[str, int]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_student_team_history, dtlms_team_advisors, dtlms_teams RESTART IDENTITY CASCADE")
        team_map: dict[str, int] = {}
        for item in state.get("teams", []):
            team_id = int(item["id"])
            lead_advisor_name = item.get("lead_advisor_name")
            lead_advisor_id = advisor_map.get(lead_advisor_name) if lead_advisor_name else None
            cur.execute(
                """
                INSERT INTO dtlms_teams (
                    id, team_code, team_name, department_name, discipline_name, lead_advisor_id,
                    research_directions, team_status, established_on, description, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    team_id,
                    item["team_code"],
                    item["team_name"],
                    item.get("department_name") or "未分配院系",
                    item.get("discipline_name"),
                    lead_advisor_id,
                    self._normalize_research_directions(item.get("research_directions")),
                    self._map_team_status(item.get("status", "启用")),
                    item.get("established_on"),
                    item.get("description"),
                ),
            )
            team_map[item["team_name"]] = team_id

            advisor_names = self._normalize_name_list(item.get("advisor_names"))
            if lead_advisor_name and lead_advisor_name not in advisor_names:
                advisor_names.insert(0, lead_advisor_name)

            inserted_advisors: set[int] = set()
            for advisor_name in advisor_names:
                advisor_id = advisor_map.get(advisor_name)
                if not advisor_id or advisor_id in inserted_advisors:
                    continue
                inserted_advisors.add(advisor_id)
                advisor_role = "lead" if advisor_name == lead_advisor_name else "member"
                cur.execute(
                    """
                    INSERT INTO dtlms_team_advisors (
                        team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted
                    ) VALUES (%s, %s, %s, %s, NULL, FALSE)
                    """,
                    (team_id, advisor_id, advisor_role, item.get("established_on")),
                )
        return team_map

    def _seed_students(self, cur: psycopg.Cursor[Any], state: dict[str, Any], advisor_map: dict[str, int], team_map: dict[str, int]) -> dict[str, int]:
        cur.execute("TRUNCATE TABLE dtlms_students RESTART IDENTITY CASCADE")
        student_map: dict[str, int] = {}
        for item in state.get("students", []):
            status = self._map_student_status(item.get("status", "在校"))
            team_id = team_map.get(item.get("team_name")) if item.get("team_name") else None
            cur.execute(
                """
                INSERT INTO dtlms_students (
                    id, student_no, full_name, gender, political_status, phone_number, identity_no,
                    enrollment_year, degree_type, team_id, current_status, primary_advisor_id, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["student_no"],
                    item["full_name"],
                    "未知",
                    item.get("political_status"),
                    item.get("phone_number"),
                    f"ID-{item['student_no']}",
                    int(item["enrollment_year"]),
                    item["degree_type"],
                    team_id,
                    status,
                    advisor_map.get(item.get("advisor_name")),
                ),
            )
            student_map[item["student_no"]] = int(item["id"])
            if team_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_student_team_history (student_id, team_id, start_date, end_date, change_reason)
                    VALUES (%s, %s, %s, NULL, %s)
                    """,
                    (int(item["id"]), team_id, f"{item['enrollment_year']}-09-01", "初始化导入"),
                )
            advisor_id = advisor_map.get(item.get("advisor_name"))
            if advisor_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_student_advisor_history (student_id, advisor_id, relation_type, start_date, end_date, change_reason)
                    VALUES (%s, %s, 'primary', %s, NULL, %s)
                    """,
                    (int(item["id"]), advisor_id, f"{item['enrollment_year']}-09-01", "初始化导入"),
                )
        return student_map

    def _seed_recruitment(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> dict[int, int]:
        cur.execute(
            "TRUNCATE TABLE dtlms_admission_decisions, dtlms_written_exam_scores, dtlms_interview_scores, "
            "dtlms_interview_schedules, dtlms_interview_groups, dtlms_material_scores, dtlms_reviewer_assignments, "
            "dtlms_qualification_reviews, dtlms_application_materials, dtlms_recruitment_applications, "
            "dtlms_research_fields, dtlms_recruitment_plans RESTART IDENTITY CASCADE"
        )

        field_names = sorted({item["intended_field"] for item in state.get("recruitment_applications", []) if item.get("intended_field")})
        field_map: dict[str, int] = {}
        for index, field_name in enumerate(field_names, start=1):
            cur.execute(
                "INSERT INTO dtlms_research_fields (id, field_code, field_name, description, is_deleted) VALUES (%s, %s, %s, %s, FALSE)",
                (index, f"FIELD{index:03d}", field_name, f"{field_name}方向"),
            )
            field_map[field_name] = index

        plan_map: dict[int, int] = {}
        for item in state.get("recruitment_plans", []):
            plan_status = self._map_plan_status(item.get("current_stage", "资格审核"), item.get("is_open", True))
            cur.execute(
                """
                INSERT INTO dtlms_recruitment_plans (
                    id, plan_code, plan_name, academic_year, semester, start_date, end_date, target_quota, plan_status, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    f"PLAN-{item['id']:03d}",
                    item["plan_name"],
                    item["academic_year"],
                    item["semester"],
                    f"{item['academic_year']}-03-01 08:00:00+08",
                    f"{item['academic_year']}-10-31 18:00:00+08",
                    int(item["target_quota"]),
                    plan_status,
                ),
            )
            plan_map[int(item["id"])] = int(item["id"])

            for group_index in range(1, int(item.get("interview_group_count", 0)) + 1):
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_groups (plan_id, group_code, group_name, interview_mode, is_deleted)
                    VALUES (%s, %s, %s, %s, FALSE)
                    """,
                    (int(item["id"]), f"G{group_index:02d}", f"第{group_index}面试组", "offline"),
                )

        group_ids = self._fetch_map(cur, "SELECT id, (plan_id::text || ':' || group_code) AS key FROM dtlms_interview_groups")
        application_rows = state.get("recruitment_applications", [])
        for item in application_rows:
            application_status = self._map_application_status(item.get("application_status", "报名已提交"))
            cur.execute(
                """
                INSERT INTO dtlms_recruitment_applications (
                    id, plan_id, student_name, candidate_no, gender, graduation_school, highest_degree,
                    intended_field_id, application_status, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    plan_map[int(item["plan_id"])],
                    item["student_name"],
                    item["candidate_no"],
                    "未知",
                    item.get("graduation_school"),
                    item.get("highest_degree"),
                    field_map.get(item.get("intended_field")),
                    application_status,
                ),
            )
            cur.execute(
                "INSERT INTO dtlms_application_materials (application_id, material_type, material_status, file_url, is_deleted) VALUES (%s, %s, %s, %s, FALSE)",
                (int(item["id"]), "报名材料", self._map_material_status(item.get("material_status", "待补材料")), f"/materials/{item['candidate_no']}.zip"),
            )
            reviewer = item.get("reviewer_name") or "system.auto"
            cur.execute(
                "INSERT INTO dtlms_qualification_reviews (application_id, reviewer_username, review_status, review_comment) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), reviewer, self._map_review_status(application_status), f"导入状态：{item.get('application_status') or '报名已提交'}"),
            )
            cur.execute(
                "INSERT INTO dtlms_reviewer_assignments (application_id, reviewer_username, reviewer_role, assignment_status) VALUES (%s, %s, %s, %s) RETURNING id",
                (int(item["id"]), reviewer, "reviewer", "assigned"),
            )
            reviewer_assignment_id = int(cur.fetchone()[0])
            cur.execute(
                "INSERT INTO dtlms_material_scores (application_id, reviewer_assignment_id, material_score, recommendation_text) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), reviewer_assignment_id, item.get("final_score"), "按模拟数据导入"),
            )
            group_key = f"{item['plan_id']}:G01"
            interview_group_id = group_ids.get(group_key)
            if interview_group_id:
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_schedules (
                        application_id, interview_group_id, admission_ticket_no, starts_at, ends_at, schedule_status
                    ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (
                        int(item["id"]),
                        int(interview_group_id),
                        f"TKT-{item['candidate_no']}",
                        "2026-04-18 09:00:00+08",
                        "2026-04-18 09:30:00+08",
                        "completed" if item.get("final_score") is not None else "scheduled",
                    ),
                )
                schedule_id = int(cur.fetchone()[0])
                cur.execute(
                    """
                    INSERT INTO dtlms_interview_scores (
                        schedule_id, evaluator_username, single_choice_score, fill_blank_score, coding_score,
                        interview_score, ideological_score
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (schedule_id, reviewer, None, None, None, item.get("final_score"), 95.0),
                )
            cur.execute(
                "INSERT INTO dtlms_written_exam_scores (application_id, exam_date, exam_score, import_batch_no) VALUES (%s, %s, %s, %s)",
                (int(item["id"]), "2026-03-20", item.get("final_score"), "SIM-2026-01"),
            )
        return plan_map

    def _seed_training(self, cur: psycopg.Cursor[Any], state: dict[str, Any], student_map: dict[str, int], advisor_map: dict[str, int]) -> dict[int, int]:
        cur.execute(
            "TRUNCATE TABLE dtlms_training_plan_versions, dtlms_scientific_reports, dtlms_outbound_studies, dtlms_training_plans RESTART IDENTITY CASCADE"
        )
        training_plan_map: dict[int, int] = {}
        for item in state.get("training_plans", []):
            cur.execute(
                """
                INSERT INTO dtlms_training_plans (
                    id, student_id, advisor_id, version_no, report_cycle, plan_status, scientific_goal, assessment_rule, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["version_no"],
                    item["report_cycle"],
                    self._map_training_plan_status(item.get("plan_status", "待学生确认")),
                    item["scientific_goal"],
                    item["assessment_rule"],
                ),
            )
            training_plan_map[int(item["id"])] = int(item["id"])

        training_plan_by_student = {item["student_no"]: int(item["id"]) for item in state.get("training_plans", [])}
        for item in state.get("scientific_reports", []):
            cur.execute(
                """
                INSERT INTO dtlms_scientific_reports (
                    id, student_id, training_plan_id, period_label, report_status, summary,
                    attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    student_map[item["student_no"]],
                    training_plan_by_student[item["student_no"]],
                    item["period_label"],
                    self._map_report_status(item.get("report_status", "待导师审阅")),
                    item["summary"],
                    f"/reports/{item['student_no']}/{item['period_label']}.pdf",
                    advisor_map.get(item.get("reviewer_name")) if item.get("reviewer_name") else None,
                    item.get("review_score"),
                    f"导入状态：{item.get('report_status')}",
                ),
            )

        for item in state.get("outbound_studies", []):
            cur.execute(
                """
                INSERT INTO dtlms_outbound_studies (
                    id, student_id, advisor_id, study_type, destination, start_date, end_date,
                    approval_status, expected_outcome, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["study_type"],
                    item["destination"],
                    item["start_date"],
                    item["end_date"],
                    self._map_outbound_status(item.get("approval_status", "审批中")),
                    item.get("expected_outcome"),
                ),
            )
        return training_plan_map

    def _seed_degree(self, cur: psycopg.Cursor[Any], state: dict[str, Any], student_map: dict[str, int], advisor_map: dict[str, int]) -> dict[int, int]:
        cur.execute("TRUNCATE TABLE dtlms_thesis_reviews, dtlms_theses RESTART IDENTITY CASCADE")
        thesis_map: dict[int, int] = {}
        for item in state.get("theses", []):
            cur.execute(
                """
                INSERT INTO dtlms_theses (
                    id, student_id, advisor_id, title, plagiarism_rate, thesis_status,
                    blind_review_status, defense_date, degree_granted, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    student_map[item["student_no"]],
                    advisor_map[item["advisor_name"]],
                    item["title"],
                    item.get("plagiarism_rate"),
                    self._map_thesis_status(item.get("thesis_status", "待提交")),
                    self._map_blind_review_status(item.get("blind_review_status", "未送审")),
                    self._map_defense_date(item.get("defense_status", "未进入")),
                    self._map_degree_status(item.get("degree_status", "待申请")),
                ),
            )
            thesis_map[int(item["id"])] = int(item["id"])
        return thesis_map

    def _seed_training_plan_versions(self, cur: psycopg.Cursor[Any], state: dict[str, Any], training_plan_map: dict[int, int]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_training_plan_versions RESTART IDENTITY CASCADE")
        for item in state.get("training_plans", []):
            cur.execute(
                "INSERT INTO dtlms_training_plan_versions (training_plan_id, version_no, change_reason, plan_snapshot) VALUES (%s, %s, %s, %s)",
                (training_plan_map[int(item["id"])], item["version_no"], "初始化导入", item["scientific_goal"]),
            )

    def _seed_admission_decisions(self, cur: psycopg.Cursor[Any], state: dict[str, Any], plan_map: dict[int, int]) -> None:
        application_ids = {int(item["id"]): item for item in state.get("recruitment_applications", [])}
        for application_id, item in application_ids.items():
            decision_status = self._map_decision_status(item.get("application_status", "报名已提交"))
            cur.execute(
                "INSERT INTO dtlms_admission_decisions (application_id, decision_status, rank_no, final_score, transfer_option, decision_comment) VALUES (%s, %s, %s, %s, %s, %s)",
                (application_id, decision_status, application_id, item.get("final_score"), None, f"来源计划 {plan_map[int(item['plan_id'])]}"),
            )

    def _seed_thesis_reviews(self, cur: psycopg.Cursor[Any], state: dict[str, Any], thesis_map: dict[int, int]) -> None:
        for item in state.get("thesis_reviews", []):
            cur.execute(
                "INSERT INTO dtlms_thesis_reviews (id, thesis_id, expert_name, review_score, review_status, review_comment) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    int(item["id"]),
                    thesis_map[int(item["thesis_id"])],
                    item["expert_name"],
                    item.get("review_score"),
                    self._map_review_progress(item.get("review_status", "待提交")),
                    item.get("review_comment"),
                ),
            )

    def _seed_operation_logs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_operation_logs RESTART IDENTITY CASCADE")
        for item in state.get("operation_logs", []):
            cur.execute(
                """
                INSERT INTO dtlms_operation_logs (
                    id, operator_username, operator_role, module_name, entity_name, entity_id,
                    action, old_value, new_value, request_ip, result, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s::jsonb, %s, %s, %s, %s)
                """,
                (
                    int(item["id"]),
                    item["operator_username"],
                    "runtime_seed",
                    item["module_name"],
                    item["entity_name"],
                    item["entity_id"],
                    item["action"],
                    self._json_payload({"summary": item.get("summary")}),
                    "127.0.0.1",
                    item.get("result", "success"),
                    item["operated_at"],
                    item["operated_at"],
                ),
            )

    def _seed_sync_logs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_data_sync_logs RESTART IDENTITY CASCADE")
        for item in state.get("sync_logs", []):
            cur.execute(
                "INSERT INTO dtlms_data_sync_logs (id, source_system, target_system, sync_status, record_count, failure_reason, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    int(item["id"]),
                    item["source_system"],
                    item["target_system"],
                    item["sync_status"],
                    int(item["record_count"]),
                    item.get("failure_reason"),
                    item["executed_at"],
                    item["executed_at"],
                ),
            )

    def _seed_system_configs(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        for item in state.get("audit_policies", []):
            cur.execute(
                """
                INSERT INTO dtlms_system_configs (config_key, config_value, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value, description = EXCLUDED.description, updated_at = CURRENT_TIMESTAMP
                """,
                (f"audit.policy.{int(item['id'])}", item["policy"], item["item"]),
            )
        for item in state.get("integrations", []):
            cur.execute(
                """
                INSERT INTO dtlms_system_configs (config_key, config_value, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value, description = EXCLUDED.description, updated_at = CURRENT_TIMESTAMP
                """,
                (
                    f"integration.{int(item['id'])}.{item['name']}",
                    f"{item['direction']}|{item['cadence']}|{item['status']}|{item['owner']}",
                    "外部集成概览",
                ),
            )

    def _fetch_map(self, cur: psycopg.Cursor[Any], query: str) -> dict[str, Any]:
        cur.execute(query)
        rows = cur.fetchall()
        if not rows:
            return {}
        first_row = rows[0]
        if isinstance(first_row, dict):
            return {str(row["key"]): row["id"] for row in rows}
        return {str(row[1]): row[0] for row in rows}

    def list_dict_types(self, keyword: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["t.is_deleted = FALSE"]
                params: list[Any] = []
                if status:
                    where_clauses.append("t.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(t.dict_name ILIKE %s OR t.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT t.id, t.dict_name, t.dict_type, t.status, t.remark, COUNT(d.id) AS data_count
                    FROM dtlms_dict_types t
                    LEFT JOIN dtlms_dict_data d ON d.dict_type_id = t.id AND d.is_deleted = FALSE
                    WHERE {' AND '.join(where_clauses)}
                    GROUP BY t.id
                    ORDER BY t.id DESC
                """
                cur.execute(sql_text, params)
                return [self._normalize_dict_row(dict(row) | {"data_count": int(row["data_count"])} ) for row in cur.fetchall()]

    def list_dict_data(self, keyword: str | None = None, dict_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                where_clauses = ["d.is_deleted = FALSE", "t.is_deleted = FALSE"]
                params: list[Any] = []
                if dict_type:
                    where_clauses.append("d.dict_type = %s")
                    params.append(dict_type)
                if status:
                    where_clauses.append("d.status = %s")
                    params.append(status)
                if keyword:
                    where_clauses.append("(d.label ILIKE %s OR d.value ILIKE %s OR d.dict_type ILIKE %s)")
                    params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
                sql_text = f"""
                    SELECT d.id, d.dict_type, t.dict_name, d.label, d.value, d.sort_order, d.status, d.color_type, d.css_class, d.remark
                    FROM dtlms_dict_data d
                    JOIN dtlms_dict_types t ON t.id = d.dict_type_id
                    WHERE {' AND '.join(where_clauses)}
                    ORDER BY d.dict_type ASC, d.sort_order ASC, d.id ASC
                """
                cur.execute(sql_text, params)
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def list_dict_options(self, dict_type: str) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT label, value, color_type, css_class
                    FROM dtlms_dict_data
                    WHERE is_deleted = FALSE AND status = '启用' AND dict_type = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (dict_type,),
                )
                return [self._normalize_dict_row(dict(row)) for row in cur.fetchall()]

    def create_dict_type(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s", (payload["dict_type"],))
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark")),
                )
                record = self._normalize_dict_row(dict(cur.fetchone()))
            conn.commit()
        return record | {"data_count": 0}

    def update_dict_type(self, dict_type_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id, dict_type FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                current = cur.fetchone()
                if not current:
                    raise KeyError(dict_type_id)
                cur.execute(
                    "SELECT id FROM dtlms_dict_types WHERE is_deleted = FALSE AND dict_type = %s AND id <> %s",
                    (payload["dict_type"], dict_type_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict type already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_types
                    SET dict_name = %s, dict_type = %s, status = %s, remark = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_name, dict_type, status, remark
                    """,
                    (payload["dict_name"], payload["dict_type"], payload["status"], payload.get("remark"), dict_type_id),
                )
                record = self._normalize_dict_row(dict(cur.fetchone()))
                if current["dict_type"] != payload["dict_type"]:
                    cur.execute(
                        "UPDATE dtlms_dict_data SET dict_type = %s, updated_at = CURRENT_TIMESTAMP WHERE dict_type_id = %s AND is_deleted = FALSE",
                        (payload["dict_type"], dict_type_id),
                    )
                cur.execute("SELECT COUNT(*) AS count FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                count_row = cur.fetchone()
            conn.commit()
        return record | {"data_count": int(count_row["count"])}

    def delete_dict_type(self, dict_type_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_types WHERE id = %s AND is_deleted = FALSE", (dict_type_id,))
                if not cur.fetchone():
                    raise KeyError(dict_type_id)
                cur.execute("SELECT COUNT(*) FROM dtlms_dict_data WHERE dict_type_id = %s AND is_deleted = FALSE", (dict_type_id,))
                if int(cur.fetchone()[0]) > 0:
                    raise ValueError("Dict type still has dict data")
                cur.execute("UPDATE dtlms_dict_types SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_type_id,))
            conn.commit()

    def create_dict_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE",
                    (payload["dict_type"], payload["value"]),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                    ),
                )
                record = self._normalize_dict_row(dict(cur.fetchone()))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    def update_dict_data(self, dict_data_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute(
                    "SELECT id, dict_name FROM dtlms_dict_types WHERE dict_type = %s AND is_deleted = FALSE",
                    (payload["dict_type"],),
                )
                dict_type_row = cur.fetchone()
                if not dict_type_row:
                    raise ValueError("Dict type does not exist")
                cur.execute(
                    "SELECT id FROM dtlms_dict_data WHERE dict_type = %s AND value = %s AND is_deleted = FALSE AND id <> %s",
                    (payload["dict_type"], payload["value"], dict_data_id),
                )
                if cur.fetchone():
                    raise ValueError("Dict value already exists")
                cur.execute(
                    """
                    UPDATE dtlms_dict_data
                    SET dict_type_id = %s,
                        dict_type = %s,
                        label = %s,
                        value = %s,
                        sort_order = %s,
                        status = %s,
                        color_type = %s,
                        css_class = %s,
                        remark = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING id, dict_type, label, value, sort_order, status, color_type, css_class, remark
                    """,
                    (
                        int(dict_type_row["id"]),
                        payload["dict_type"],
                        payload["label"],
                        payload["value"],
                        int(payload.get("sort_order", 0)),
                        payload["status"],
                        payload.get("color_type"),
                        payload.get("css_class"),
                        payload.get("remark"),
                        dict_data_id,
                    ),
                )
                record = self._normalize_dict_row(dict(cur.fetchone()))
            conn.commit()
        return record | {"dict_name": dict_type_row["dict_name"]}

    @staticmethod
    def _normalize_dict_row(row: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in row.items():
            if isinstance(value, str):
                normalized[key] = value.strip()
            else:
                normalized[key] = value
        return normalized

    def delete_dict_data(self, dict_data_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM dtlms_dict_data WHERE id = %s AND is_deleted = FALSE", (dict_data_id,))
                if not cur.fetchone():
                    raise KeyError(dict_data_id)
                cur.execute("UPDATE dtlms_dict_data SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (dict_data_id,))
            conn.commit()

    @staticmethod
    def _json_payload(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False)

    @staticmethod
    def _normalize_name_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [item.strip() for item in value.split(",") if item.strip()]
        return []

    @staticmethod
    def _normalize_research_directions(value: Any) -> str | None:
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            return "、".join(items) if items else None
        if isinstance(value, str):
            return value.strip() or None
        return None

    @staticmethod
    def _map_student_status(value: str) -> str:
        mapping = {
            "在校": "enrolled",
            "外出研修": "outbound",
            "学位论文阶段": "thesis",
            "实习中": "internship",
        }
        return mapping.get(value, "enrolled")

    @staticmethod
    def _map_team_status(value: str) -> str:
        mapping = {
            "启用": "active",
            "停用": "inactive",
            "筹建": "planning",
            "归档": "archived",
        }
        return mapping.get(value, "active")

    @staticmethod
    def _map_training_plan_status(value: str) -> str:
        mapping = {
            "待学生确认": "pending_confirm",
            "执行中": "effective",
            "已归档": "archived",
        }
        return mapping.get(value, "draft")

    @staticmethod
    def _map_report_status(value: str) -> str:
        mapping = {
            "待导师审阅": "reviewing",
            "已通过": "reviewed",
            "退回修改": "rework",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _map_outbound_status(value: str) -> str:
        mapping = {
            "审批中": "submitted",
            "研修中": "approved",
            "已完成": "completed",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _map_thesis_status(value: str) -> str:
        mapping = {
            "退回修改": "rework",
            "查重通过": "plagiarism_passed",
            "盲审通过": "review_passed",
        }
        return mapping.get(value, "draft")

    @staticmethod
    def _map_blind_review_status(value: str) -> str:
        mapping = {
            "未送审": "pending",
            "进行中": "reviewing",
            "已通过": "passed",
        }
        return mapping.get(value, "pending")

    @staticmethod
    def _map_degree_status(value: str) -> str:
        mapping = {
            "待申请": "pending",
            "授位审批中": "reviewing",
            "待正式答辩": "pending",
            "已授位": "granted",
        }
        return mapping.get(value, "pending")

    @staticmethod
    def _map_defense_date(value: str) -> str | None:
        mapping = {
            "待安排": "2026-06-18",
            "预答辩完成": "2026-05-20",
        }
        return mapping.get(value)

    @staticmethod
    def _map_plan_status(stage: str, is_open: bool) -> str:
        if not is_open:
            return "closed"
        if stage in {"资格审核", "评分推荐"}:
            return "published"
        return "admitting"

    @staticmethod
    def _map_application_status(value: str) -> str:
        mapping = {
            "报名已提交": "submitted",
            "资格审核通过": "qualified",
            "材料评分中": "scoring",
            "面试完成": "interviewed",
            "预录取": "pre_admitted",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _map_material_status(value: str) -> str:
        mapping = {
            "材料齐全": "approved",
            "待补材料": "pending",
        }
        return mapping.get(value, "pending")

    @staticmethod
    def _map_review_status(application_status: str) -> str:
        if application_status in {"qualified", "scoring", "interviewed", "pre_admitted"}:
            return "approved"
        return "pending"

    @staticmethod
    def _map_decision_status(value: str) -> str:
        mapping = {
            "预录取": "pre_admit",
            "同意录取": "admitted",
        }
        return mapping.get(value, "pending")

    @staticmethod
    def _map_review_progress(value: str) -> str:
        mapping = {
            "已提交": "submitted",
            "已通过": "passed",
        }
        return mapping.get(value, "pending")