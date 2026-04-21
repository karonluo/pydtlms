from __future__ import annotations

from datetime import datetime
import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)


class PostgresStateStore:
    CONNECT_TIMEOUT_SECONDS = 5
    RUNTIME_COUNTERS_REGCLASS = "public.dtlms_runtime_counters"
    MIGRATION_SQL_FILES: tuple[str, ...] = (
        "015_team_schema_migration.sql",
        "016_business_key_migration.sql",
        "017_workflow_flowable_schema.sql",
        "018_recruitment_application_profile.sql",
        "019_portal_student_and_brochure.sql",
        "021_portal_auth_and_profile_fields.sql",
        "022_portal_application_structured_schema.sql",
        "023_runtime_team_store.sql",
        "024_recruitment_plan_description.sql",
        "025_portal_student_account_status.sql",
        "026_portal_profile_photo_and_ethnic_dict.sql",
        "050_dict_schema.sql",
    )

    DATASET_TABLES: dict[str, str] = {
        "profiles": "dtlms_runtime_profiles",
        "students": "dtlms_runtime_students",
        "teams": "dtlms_runtime_teams",
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
        "portal_students": "dtlms_runtime_portal_students",
    }

    SQL_FILES: tuple[str, ...] = (
        "000_create_database.sql",
        "010_init_schema.sql",
        "015_team_schema_migration.sql",
        "016_business_key_migration.sql",
        "017_workflow_flowable_schema.sql",
        "018_recruitment_application_profile.sql",
        "019_portal_student_and_brochure.sql",
        "021_portal_auth_and_profile_fields.sql",
        "022_portal_application_structured_schema.sql",
        "023_runtime_team_store.sql",
        "024_recruitment_plan_description.sql",
        "025_portal_student_account_status.sql",
        "026_portal_profile_photo_and_ethnic_dict.sql",
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
            f"dbname={database_name} user={username} password={settings.postgres_password} "
            f"client_encoding=utf8 connect_timeout={self.CONNECT_TIMEOUT_SECONDS}"
        )

    def _schema_initialized(self, cur: psycopg.Cursor[Any]) -> bool:
        cur.execute("SELECT to_regclass(%s) AS table_name", (self.RUNTIME_COUNTERS_REGCLASS,))
        row = cur.fetchone()
        return bool(row and row[0])

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
                if self._schema_initialized(cur):
                    for file_name in self.MIGRATION_SQL_FILES:
                        sql_text = (self._sql_dir / file_name).read_text(encoding="utf-8")
                        cur.execute(sql_text)
                    self._schema_ready = True
                    return
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
                    cur.execute("SELECT to_regclass(%s) AS table_name", (self.RUNTIME_COUNTERS_REGCLASS,))
                    row = cur.fetchone()
                    if not row or not row["table_name"]:
                        return None

                    cur.execute("SELECT counter_name, counter_value FROM dtlms_runtime_counters")
                    counters = {row["counter_name"]: int(row["counter_value"]) for row in cur.fetchall()}
                    if not counters:
                        return None

                    state: dict[str, Any] = {"counters": counters}
                    for dataset, table_name in self.DATASET_TABLES.items():
                        cur.execute(f"SELECT payload FROM {table_name}")
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

    def update_runtime_system_user(self, user_id: int, payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_system_users (id, payload, updated_at)
                    VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE
                    SET payload = EXCLUDED.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (int(user_id), self._json_payload(payload)),
                )
            conn.commit()

    def update_runtime_profile(self, username: str, payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_profiles (username, payload, updated_at)
                    VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                    ON CONFLICT (username) DO UPDATE
                    SET payload = EXCLUDED.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (str(username), self._json_payload(payload)),
                )
            conn.commit()

    def update_runtime_portal_student(self, student_id: int, payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_portal_students (id, payload, updated_at)
                    VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE
                    SET payload = EXCLUDED.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (int(student_id), self._json_payload(payload)),
                )
            conn.commit()

    def update_runtime_counter(self, counter_name: str, counter_value: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_counters (counter_name, counter_value, updated_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (counter_name) DO UPDATE
                    SET counter_value = EXCLUDED.counter_value,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (str(counter_name), int(counter_value)),
                )
            conn.commit()

    def insert_runtime_operation_log(self, payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_operation_logs (id, payload, updated_at)
                    VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE
                    SET payload = EXCLUDED.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (int(payload["id"]), self._json_payload(payload)),
                )
            conn.commit()

    def load_team_state(self) -> list[dict[str, Any]]:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        t.id,
                        t.team_code,
                        t.team_name,
                        COALESCE(t.department_name, '') AS department_name,
                        COALESCE(t.discipline_name, '') AS discipline_name,
                        COALESCE(lead.full_name, '') AS lead_advisor_name,
                        COALESCE(advisor_names.advisor_names, ARRAY[]::text[]) AS advisor_names,
                        t.research_directions,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS established_on,
                        t.description
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT array_agg(DISTINCT advisor.full_name ORDER BY advisor.full_name) AS advisor_names
                        FROM dtlms_team_advisors ta
                        JOIN dtlms_advisors advisor ON advisor.id = ta.advisor_id AND advisor.is_deleted = FALSE
                        WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                    ) advisor_names ON TRUE
                    WHERE t.is_deleted = FALSE
                    ORDER BY t.id
                    """
                )
                rows = cur.fetchall()

        return [
            {
                "id": int(row["id"]),
                "team_code": row["team_code"],
                "team_name": row["team_name"],
                "department_name": row["department_name"],
                "discipline_name": row["discipline_name"],
                "lead_advisor_name": row["lead_advisor_name"] or None,
                "advisor_names": list(row["advisor_names"] or []),
                "research_directions": self._split_delimited_values(row["research_directions"]),
                "status": self._team_status_label(row["team_status"]),
                "established_on": row["established_on"],
                "description": row["description"],
            }
            for row in rows
        ]

    def sync_updated_center(
        self,
        team_payload: dict[str, Any],
        affected_students: list[dict[str, Any]],
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                for counter_name, counter_value in (counters or {}).items():
                    cur.execute(
                        """
                        INSERT INTO dtlms_runtime_counters (counter_name, counter_value)
                        VALUES (%s, %s)
                        ON CONFLICT (counter_name) DO UPDATE
                        SET counter_value = EXCLUDED.counter_value
                        """,
                        (counter_name, int(counter_value)),
                    )

                cur.execute(
                    """
                    INSERT INTO dtlms_runtime_teams (id, payload, updated_at)
                    VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                    ON CONFLICT (id) DO UPDATE
                    SET payload = EXCLUDED.payload,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (int(team_payload["id"]), self._json_payload(team_payload)),
                )

                for student in affected_students:
                    cur.execute(
                        """
                        INSERT INTO dtlms_runtime_students (id, payload, updated_at)
                        VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                        ON CONFLICT (id) DO UPDATE
                        SET payload = EXCLUDED.payload,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (int(student["id"]), self._json_payload(student)),
                    )

                if operation_log:
                    cur.execute(
                        """
                        INSERT INTO dtlms_runtime_operation_logs (id, payload, updated_at)
                        VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                        ON CONFLICT (id) DO UPDATE
                        SET payload = EXCLUDED.payload,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (int(operation_log["id"]), self._json_payload(operation_log)),
                    )
                    cur.execute(
                        """
                        INSERT INTO dtlms_operation_logs (
                            id, operator_username, operator_role, module_name, entity_name, entity_id,
                            action, old_value, new_value, request_ip, result, created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s::jsonb, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE
                        SET operator_username = EXCLUDED.operator_username,
                            module_name = EXCLUDED.module_name,
                            entity_name = EXCLUDED.entity_name,
                            entity_id = EXCLUDED.entity_id,
                            action = EXCLUDED.action,
                            new_value = EXCLUDED.new_value,
                            request_ip = EXCLUDED.request_ip,
                            result = EXCLUDED.result,
                            updated_at = EXCLUDED.updated_at
                        """,
                        (
                            int(operation_log["id"]),
                            operation_log.get("operator_username", "admin"),
                            "runtime_seed",
                            operation_log.get("module_name"),
                            operation_log.get("entity_name"),
                            operation_log.get("entity_id"),
                            operation_log.get("action"),
                            self._json_payload({"summary": operation_log.get("summary")}),
                            "127.0.0.1",
                            operation_log.get("result", "success"),
                            operation_log.get("operated_at"),
                            operation_log.get("operated_at"),
                        ),
                    )

                advisor_map = self._fetch_map(
                    cur,
                    "SELECT id, full_name AS key FROM dtlms_advisors WHERE is_deleted = FALSE",
                )
                lead_advisor_name = team_payload.get("lead_advisor_name")
                lead_advisor_id = advisor_map.get(lead_advisor_name) if lead_advisor_name else None
                established_on = team_payload.get("created_on") or team_payload.get("established_on")
                cur.execute(
                    """
                    INSERT INTO dtlms_teams (
                        id, team_code, team_name, department_name, discipline_name, lead_advisor_id,
                        research_directions, team_status, established_on, description, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET team_code = EXCLUDED.team_code,
                        team_name = EXCLUDED.team_name,
                        department_name = EXCLUDED.department_name,
                        discipline_name = EXCLUDED.discipline_name,
                        lead_advisor_id = EXCLUDED.lead_advisor_id,
                        research_directions = EXCLUDED.research_directions,
                        team_status = EXCLUDED.team_status,
                        established_on = EXCLUDED.established_on,
                        description = EXCLUDED.description,
                        updated_at = CURRENT_TIMESTAMP,
                        is_deleted = FALSE
                    """,
                    (
                        int(team_payload["id"]),
                        team_payload.get("team_code"),
                        team_payload.get("team_name"),
                        team_payload.get("department_name") or "未分配院系",
                        team_payload.get("discipline_name"),
                        lead_advisor_id,
                        self._normalize_research_directions(team_payload.get("research_directions")),
                        self._map_team_status(team_payload.get("status", "启用")),
                        established_on,
                        team_payload.get("description"),
                    ),
                )

                cur.execute("DELETE FROM dtlms_team_advisors WHERE team_id = %s", (int(team_payload["id"]),))
                advisor_names = self._normalize_name_list(team_payload.get("advisor_names"))
                if lead_advisor_name and lead_advisor_name not in advisor_names:
                    advisor_names.insert(0, lead_advisor_name)
                inserted_advisors: set[int] = set()
                for advisor_name in advisor_names:
                    advisor_id = advisor_map.get(advisor_name)
                    if not advisor_id or advisor_id in inserted_advisors:
                        continue
                    inserted_advisors.add(advisor_id)
                    cur.execute(
                        """
                        INSERT INTO dtlms_team_advisors (team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted)
                        VALUES (%s, %s, %s, %s, NULL, FALSE)
                        """,
                        (
                            int(team_payload["id"]),
                            advisor_id,
                            "lead" if advisor_name == lead_advisor_name else "member",
                            established_on,
                        ),
                    )
            conn.commit()

    def sync_created_center(
        self,
        team_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.sync_updated_center(
            team_payload,
            affected_students=[],
            operation_log=operation_log,
            counters=counters,
        )

    def sync_deleted_center(
        self,
        center_id: int,
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                for counter_name, counter_value in (counters or {}).items():
                    cur.execute(
                        """
                        INSERT INTO dtlms_runtime_counters (counter_name, counter_value)
                        VALUES (%s, %s)
                        ON CONFLICT (counter_name) DO UPDATE
                        SET counter_value = EXCLUDED.counter_value
                        """,
                        (counter_name, int(counter_value)),
                    )

                cur.execute("DELETE FROM dtlms_runtime_teams WHERE id = %s", (int(center_id),))
                cur.execute("DELETE FROM dtlms_team_advisors WHERE team_id = %s", (int(center_id),))
                cur.execute("DELETE FROM dtlms_teams WHERE id = %s", (int(center_id),))

                if operation_log:
                    cur.execute(
                        """
                        INSERT INTO dtlms_runtime_operation_logs (id, payload, updated_at)
                        VALUES (%s, %s::jsonb, CURRENT_TIMESTAMP)
                        ON CONFLICT (id) DO UPDATE
                        SET payload = EXCLUDED.payload,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (int(operation_log["id"]), self._json_payload(operation_log)),
                    )
                    cur.execute(
                        """
                        INSERT INTO dtlms_operation_logs (
                            id, operator_username, operator_role, module_name, entity_name, entity_id,
                            action, old_value, new_value, request_ip, result, created_at, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, %s::jsonb, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE
                        SET operator_username = EXCLUDED.operator_username,
                            module_name = EXCLUDED.module_name,
                            entity_name = EXCLUDED.entity_name,
                            entity_id = EXCLUDED.entity_id,
                            action = EXCLUDED.action,
                            new_value = EXCLUDED.new_value,
                            request_ip = EXCLUDED.request_ip,
                            result = EXCLUDED.result,
                            updated_at = EXCLUDED.updated_at
                        """,
                        (
                            int(operation_log["id"]),
                            operation_log.get("operator_username", "admin"),
                            "runtime_seed",
                            operation_log.get("module_name"),
                            operation_log.get("entity_name"),
                            operation_log.get("entity_id"),
                            operation_log.get("action"),
                            self._json_payload({"summary": operation_log.get("summary")}),
                            "127.0.0.1",
                            operation_log.get("result", "success"),
                            operation_log.get("operated_at"),
                            operation_log.get("operated_at"),
                        ),
                    )
            conn.commit()

    def _seed_relational_tables(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        self._seed_users_and_roles(cur, state)
        advisor_map = self._seed_advisors(cur, state)
        team_map = self._seed_teams(cur, state, advisor_map)
        student_map = self._seed_students(cur, state, advisor_map, team_map)
        plan_map, field_map, group_ids = self._seed_recruitment(cur, state)
        training_plan_map = self._seed_training(cur, state, student_map, advisor_map)
        self._seed_portal_students(cur, state, plan_map)
        self._seed_recruitment_applications(cur, state, plan_map, field_map, group_ids)
        self._seed_portal_application_structures(cur, state)
        thesis_map = self._seed_degree(cur, state, student_map, advisor_map)
        self._seed_operation_logs(cur, state)
        self._seed_sync_logs(cur, state)
        self._seed_system_configs(cur, state)
        self._seed_training_plan_versions(cur, state, training_plan_map)
        self._seed_admission_decisions(cur, state, plan_map)
        self._seed_thesis_reviews(cur, state, thesis_map)
        self._seed_workflow_engine(cur, state)

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

    def _seed_recruitment(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> tuple[dict[int, int], dict[str, int], dict[str, Any]]:
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
                    id, plan_code, plan_name, academic_year, semester, plan_description, start_date, end_date, target_quota, plan_status, brochure_image_url, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    f"PLAN-{item['id']:03d}",
                    item["plan_name"],
                    item["academic_year"],
                    item["semester"],
                    item.get("plan_description"),
                    f"{item['academic_year']}-03-01 08:00:00+08",
                    f"{item['academic_year']}-10-31 18:00:00+08",
                    int(item["target_quota"]),
                    plan_status,
                    item.get("brochure_image_url"),
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
        return plan_map, field_map, group_ids

    def _seed_recruitment_applications(
        self,
        cur: psycopg.Cursor[Any],
        state: dict[str, Any],
        plan_map: dict[int, int],
        field_map: dict[str, int],
        group_ids: dict[str, Any],
    ) -> None:
        application_rows = state.get("recruitment_applications", [])
        portal_students = state.get("portal_students", [])
        for item in application_rows:
            matched_student = next(
                (
                    student for student in portal_students
                    if int(student.get("id") or 0) == int(item.get("portal_student_id") or 0)
                ),
                None,
            )
            if matched_student is None:
                matched_student = next(
                    (
                        student for student in portal_students
                        if int(student.get("selected_plan_id") or 0) == int(item.get("plan_id") or 0)
                        and (
                            (student.get("phone_number") and student.get("phone_number") == item.get("phone_number"))
                            or (student.get("email") and student.get("email") == item.get("email"))
                            or (student.get("id_number") and student.get("id_number") == item.get("id_number"))
                        )
                    ),
                    None,
                )
            draft = self._derive_portal_application_draft(matched_student) if matched_student else None
            application_status = self._map_application_status(item.get("application_status", "报名已提交"))
            application_columns = [
                "id",
                "plan_id",
                "portal_student_id",
                "business_key",
                "student_name",
                "candidate_no",
                "gender",
                "graduation_school",
                "highest_degree",
                "intended_field_id",
                "application_status",
                "review_round",
                "first_choice",
                "second_choice",
                "political_status",
                "marital_status",
                "religious_belief",
                "native_place",
                "phone_number",
                "email",
                "mailing_address",
                "id_type",
                "id_number",
                "undergraduate_school",
                "accept_adjustment",
                "undergraduate_average_score",
                "undergraduate_gpa",
                "undergraduate_rank",
                "undergraduate_major",
                "graduate_average_score",
                "graduate_gpa",
                "graduate_rank",
                "graduate_major",
                "intended_advisor_name",
                "discovery_channel",
                "source_channel",
                "source_channel_other",
                "graduate_school",
                "overseas_university_name",
                "overseas_master_university_name",
                "self_evaluation",
                "applied_at",
                "research_problem",
                "research_status_analysis",
                "research_impact",
                "ai_society_impact",
                "dissenting_view",
                "family_info",
                "education_experience",
                "practice_experience",
                "personal_statement_text",
                "student_activity_experience",
                "personal_statement_attachment",
                "material_list_attachment",
                "supplementary_profile",
            ]
            application_values = (
                int(item["id"]),
                plan_map[int(item["plan_id"])],
                int(item.get("portal_student_id") or matched_student.get("id") or 0) if matched_student or item.get("portal_student_id") else None,
                item.get("business_key") or item["candidate_no"],
                item["student_name"],
                item["candidate_no"],
                item.get("gender") or "未知",
                item.get("graduation_school"),
                item.get("highest_degree"),
                field_map.get(item.get("intended_field")),
                application_status,
                item.get("review_round"),
                item.get("first_choice"),
                item.get("second_choice"),
                item.get("political_status"),
                item.get("marital_status"),
                item.get("religious_belief"),
                item.get("native_place"),
                item.get("phone_number"),
                item.get("email"),
                item.get("mailing_address"),
                item.get("id_type"),
                item.get("id_number"),
                item.get("undergraduate_school"),
                item.get("accept_adjustment"),
                item.get("undergraduate_average_score"),
                item.get("undergraduate_gpa"),
                item.get("undergraduate_rank"),
                item.get("undergraduate_major"),
                item.get("graduate_average_score"),
                item.get("graduate_gpa"),
                item.get("graduate_rank"),
                item.get("graduate_major"),
                item.get("intended_advisor_name"),
                item.get("discovery_channel"),
                item.get("source_channel") or (draft or {}).get("source_channel"),
                item.get("source_channel_other") or (draft or {}).get("source_channel_other"),
                item.get("graduate_school"),
                item.get("overseas_university_name"),
                item.get("overseas_master_university_name"),
                item.get("self_evaluation"),
                item.get("applied_at"),
                item.get("research_problem"),
                item.get("research_status_analysis"),
                item.get("research_impact"),
                item.get("ai_society_impact"),
                item.get("dissenting_view"),
                item.get("family_info"),
                item.get("education_experience"),
                item.get("practice_experience"),
                item.get("personal_statement_text"),
                item.get("student_activity_experience"),
                item.get("personal_statement_attachment"),
                item.get("material_list_attachment"),
                item.get("supplementary_profile"),
            )
            cur.execute(
                f"INSERT INTO dtlms_recruitment_applications ({', '.join(application_columns)}, is_deleted) VALUES ({', '.join(['%s'] * len(application_columns))}, FALSE)",
                application_values,
            )
            cur.execute(
                "INSERT INTO dtlms_application_materials (application_id, material_type, material_status, file_url, is_deleted) VALUES (%s, %s, %s, %s, FALSE)",
                (
                    int(item["id"]),
                    "报名材料",
                    self._map_material_status(item.get("material_status", "待补材料")),
                    item.get("material_list_attachment") or f"/materials/{item['candidate_no']}.zip",
                ),
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

    def _seed_portal_students(self, cur: psycopg.Cursor[Any], state: dict[str, Any], plan_map: dict[int, int]) -> None:
        cur.execute("TRUNCATE TABLE dtlms_portal_students RESTART IDENTITY CASCADE")
        for item in state.get("portal_students", []):
            selected_plan_id = item.get("selected_plan_id")
            cur.execute(
                """
                INSERT INTO dtlms_portal_students (
                    id, full_name, phone_number, email, id_number, password_hash, gender, birth_date,
                    ethnic_group, native_place, marital_status, religious_belief, id_type, mailing_address,
                    graduation_school, highest_degree, intended_field, political_status, english_level,
                    family_info, education_experience, practice_experience, personal_profile,
                    recommendation_notes, personal_statement_text, signed_agreement, selected_plan_id,
                    selected_team_name, selected_advisor_name, self_evaluation, submitted_at, account_status, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(item["id"]),
                    item["full_name"],
                    item["phone_number"],
                    item["email"],
                    item["id_number"],
                    item.get("password_hash"),
                    item.get("gender"),
                    item.get("birth_date"),
                    item.get("ethnic_group"),
                    item.get("native_place"),
                    item.get("marital_status"),
                    item.get("religious_belief"),
                    item.get("id_type"),
                    item.get("mailing_address"),
                    item.get("graduation_school"),
                    item.get("highest_degree"),
                    item.get("intended_field"),
                    item.get("political_status"),
                    item.get("english_level"),
                    item.get("family_info"),
                    item.get("education_experience"),
                    item.get("practice_experience"),
                    item.get("personal_profile"),
                    item.get("recommendation_notes"),
                    item.get("personal_statement_text"),
                    bool(item.get("signed_agreement")),
                    plan_map.get(int(selected_plan_id)) if selected_plan_id else None,
                    item.get("selected_team_name"),
                    item.get("selected_advisor_name"),
                    item.get("self_evaluation"),
                    item.get("submitted_at"),
                    self._normalize_portal_account_status(item.get("account_status")),
                    item.get("created_at"),
                    item.get("updated_at"),
                ),
            )

    def _seed_portal_application_structures(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        application_rows = state.get("recruitment_applications", [])
        for student in state.get("portal_students", []):
            profile = self._derive_portal_profile(student)
            if profile is not None:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_student_profiles (
                        portal_student_id, full_name_pinyin, gender, birth_date, ethnic_group, native_place,
                        political_status, marital_status, religious_belief, id_type, mailing_address,
                        profile_photo_url,
                        emergency_contact_name, emergency_contact_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(student["id"]),
                        profile.get("full_name_pinyin"),
                        profile.get("gender"),
                        profile.get("birth_date"),
                        profile.get("ethnic_group"),
                        profile.get("native_place"),
                        profile.get("political_status"),
                        profile.get("marital_status"),
                        profile.get("religious_belief"),
                        profile.get("id_type"),
                        profile.get("mailing_address"),
                        profile.get("profile_photo_url"),
                        profile.get("emergency_contact_name"),
                        profile.get("emergency_contact_phone"),
                    ),
                )

            draft = self._derive_portal_application_draft(student)
            matched_application = self._match_portal_application(student, application_rows)
            if draft is None or matched_application is None:
                continue
            application_id = int(matched_application["id"])

            def insert_attachment(owner_type: str, owner_id: int | None, category: str, file_url: str | None) -> None:
                if not file_url:
                    return
                file_name = str(file_url).rstrip("/").split("/")[-1] or f"{category}.dat"
                file_suffix = Path(file_name).suffix.lower().lstrip(".") or None
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_attachments (
                        portal_student_id, application_id, owner_type, owner_id, attachment_category,
                        file_name, file_url, file_type
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (int(student["id"]), application_id, owner_type, owner_id, category, file_name, file_url, file_suffix),
                )

            for preference in draft.get("preferences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_preferences (
                        application_id, preference_order, research_center_name, advisor_name, is_optional
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        int(preference.get("preference_order") or 1),
                        preference.get("research_center_name"),
                        preference.get("advisor_name"),
                        bool(preference.get("is_optional")),
                    ),
                )

            for education in draft.get("education_experiences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_education_experiences (
                        application_id, sort_order, education_stage, start_month, end_month, school_name,
                        major_name, average_score, gpa, ranking, verifier_name, verifier_phone,
                        transcript_attachment_url, degree_certificate_attachment_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        application_id,
                        int(education.get("sort_order") or 1),
                        education.get("education_stage"),
                        education.get("start_month"),
                        education.get("end_month"),
                        education.get("school_name"),
                        education.get("major_name"),
                        education.get("average_score"),
                        education.get("gpa"),
                        education.get("ranking"),
                        education.get("verifier_name"),
                        education.get("verifier_phone"),
                        education.get("transcript_attachment_url"),
                        education.get("degree_certificate_attachment_url"),
                    ),
                )
                education_row = cur.fetchone()
                education_id = int(education_row[0]) if education_row else None
                insert_attachment("education_experience", education_id, "transcript", education.get("transcript_attachment_url"))
                insert_attachment("education_experience", education_id, "degree_certificate", education.get("degree_certificate_attachment_url"))

            for practice in draft.get("practice_experiences", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_practice_experiences (
                        application_id, start_month, end_month, organization_name, position_name,
                        responsibility_text, verifier_name, verifier_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        practice.get("start_month"),
                        practice.get("end_month"),
                        practice.get("organization_name"),
                        practice.get("position_name"),
                        practice.get("responsibility_text"),
                        practice.get("verifier_name"),
                        practice.get("verifier_phone"),
                    ),
                )

            for english in draft.get("english_proficiencies", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_english_proficiencies (
                        application_id, exam_name, score_text, certificate_attachment_url
                    ) VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        application_id,
                        english.get("exam_name"),
                        english.get("score_text") or "",
                        english.get("certificate_attachment_url"),
                    ),
                )
                english_row = cur.fetchone()
                english_id = int(english_row[0]) if english_row else None
                insert_attachment("english_proficiency", english_id, "english_certificate", english.get("certificate_attachment_url"))

            for member in draft.get("family_members", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_family_members (
                        application_id, member_name, relation_type, employer_name, job_title, contact_phone
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        member.get("member_name"),
                        member.get("relation_type"),
                        member.get("employer_name"),
                        member.get("job_title"),
                        member.get("contact_phone"),
                    ),
                )

            for achievement in draft.get("achievement_records", []):
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_achievement_records (
                        application_id, achievement_type, paper_title, author_order, journal_or_conference,
                        publish_or_index_month, award_name, awarding_organization, award_level,
                        award_year, responsibility_text
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        achievement.get("achievement_type"),
                        achievement.get("paper_title"),
                        achievement.get("author_order"),
                        achievement.get("journal_or_conference"),
                        achievement.get("publish_or_index_month"),
                        achievement.get("award_name"),
                        achievement.get("awarding_organization"),
                        achievement.get("award_level"),
                        achievement.get("award_year"),
                        achievement.get("responsibility_text"),
                    ),
                )

            personal_statement = draft.get("personal_statement") if isinstance(draft.get("personal_statement"), dict) else {}
            if personal_statement:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_personal_statements (
                        application_id, personal_statement_text, ai_problem_statement, ai_industry_opinion, resume_attachment_url
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        application_id,
                        personal_statement.get("personal_statement_text"),
                        personal_statement.get("ai_problem_statement"),
                        personal_statement.get("ai_industry_opinion"),
                        personal_statement.get("resume_attachment_url"),
                    ),
                )
                insert_attachment("personal_statement", application_id, "resume", personal_statement.get("resume_attachment_url"))

            declaration = draft.get("declaration") if isinstance(draft.get("declaration"), dict) else {}
            if declaration:
                cur.execute(
                    """
                    INSERT INTO dtlms_portal_application_declarations (
                        application_id, has_read_declaration, declaration_text, progress_snapshot
                    ) VALUES (%s, %s, %s, %s::jsonb)
                    """,
                    (
                        application_id,
                        bool(declaration.get("has_read_declaration")),
                        declaration.get("declaration_text"),
                        json.dumps(declaration.get("progress_snapshot")) if declaration.get("progress_snapshot") is not None else None,
                    ),
                )

            legacy_personal_statement_attachment = matched_application.get("personal_statement_attachment")
            if legacy_personal_statement_attachment and legacy_personal_statement_attachment != personal_statement.get("resume_attachment_url"):
                insert_attachment("portal_application", application_id, "personal_statement", legacy_personal_statement_attachment)
            insert_attachment("portal_application", application_id, "materials", matched_application.get("material_list_attachment"))

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
                    id, business_key, student_id, training_plan_id, period_label, report_status, summary,
                    attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
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
                    id, business_key, student_id, advisor_id, study_type, destination, start_date, end_date,
                    approval_status, expected_outcome, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
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
                    id, business_key, student_id, advisor_id, title, plagiarism_rate, thesis_status,
                    blind_review_status, defense_date, degree_granted, is_deleted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                """,
                (
                    int(item["id"]),
                    item["business_key"],
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
        cur.execute("SELECT id FROM dtlms_recruitment_applications")
        existing_application_ids = {int(row[0]) for row in cur.fetchall()}
        for application_id, item in application_ids.items():
            if application_id not in existing_application_ids:
                logger.warning("Skip admission decision seed because recruitment application %s does not exist", application_id)
                continue
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

    def _seed_workflow_engine(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None:
        cur.execute(
            "TRUNCATE TABLE "
            "dtlms_wf_ru_identitylink, dtlms_wf_ru_variable, dtlms_wf_ru_task, dtlms_wf_ru_execution, "
            "dtlms_wf_hi_varinst, dtlms_wf_hi_actinst, dtlms_wf_hi_taskinst, dtlms_wf_hi_procinst, "
            "dtlms_wf_re_procdef, dtlms_wf_re_deployment, dtlms_wf_de_model"
        )
        tasks = list(state.get("workflow_tasks", []))
        inserted_models: set[str] = set()
        inserted_deployments: set[str] = set()
        inserted_procdefs: set[str] = set()
        inserted_procinsts: set[str] = set()
        inserted_variables: set[str] = set()

        for task in tasks:
            process_definition_key = str(task.get("process_definition_key") or task.get("flow_code") or "adhoc_workflow")
            task_definition_key = str(task.get("task_definition_key") or task.get("node_key") or "manual_task")
            business_key = str(task.get("business_key") or task.get("id") or "0")
            process_definition_id = str(task.get("process_definition_id") or self._workflow_process_definition_id(process_definition_key))
            deployment_id = str(task.get("deployment_id") or self._workflow_deployment_id(process_definition_key))
            process_instance_id = str(task.get("process_instance_id") or self._workflow_process_instance_id(process_definition_key, business_key))
            execution_id = str(task.get("execution_id") or self._workflow_execution_id(process_instance_id, task_definition_key))
            workflow_name = str(task.get("workflow_name") or "未命名流程")
            resource_name = f"{process_definition_key}.bpmn20.xml"
            terminal = self._is_workflow_terminal(task)
            start_time = str(task.get("created_at") or "")
            end_time = self._workflow_end_time(task) if terminal else None
            duration_ms = self._workflow_duration_millis(start_time, end_time)
            candidate_groups = self._normalize_name_list(task.get("candidate_groups"))

            if process_definition_key not in inserted_models:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_de_model (
                        id_, name_, key_, category_, version_, model_type_, description_, meta_info_,
                        created_, last_updated_, deployment_id_, resource_name_, editor_source_extra_value_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s::jsonb)
                    """,
                    (
                        f"MODEL-{process_definition_key}",
                        workflow_name,
                        process_definition_key,
                        task.get("business_module") or "流程中心",
                        int(task.get("process_definition_version") or 1),
                        0,
                        f"{workflow_name} 流程模型",
                        self._json_payload({"source": "runtime_seed", "workflow_name": workflow_name}),
                        start_time,
                        end_time or start_time,
                        deployment_id,
                        resource_name,
                        self._json_payload({"business_module": task.get("business_module"), "flow_code": task.get("flow_code")}),
                    ),
                )
                inserted_models.add(process_definition_key)

            if deployment_id not in inserted_deployments:
                cur.execute(
                    "INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_) VALUES (%s, %s, %s, %s, %s)",
                    (deployment_id, workflow_name, task.get("business_module") or "流程中心", process_definition_key, start_time),
                )
                inserted_deployments.add(deployment_id)

            if process_definition_id not in inserted_procdefs:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_re_procdef (
                        id_, key_, version_, deployment_id_, resource_name_, diagram_resource_name_, name_, category_, description_, suspension_state_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        process_definition_id,
                        process_definition_key,
                        int(task.get("process_definition_version") or 1),
                        deployment_id,
                        resource_name,
                        f"{process_definition_key}.png",
                        workflow_name,
                        task.get("business_module") or "流程中心",
                        f"{workflow_name} 定义",
                        1,
                    ),
                )
                inserted_procdefs.add(process_definition_id)

            if process_instance_id not in inserted_procinsts:
                cur.execute(
                    """
                    INSERT INTO dtlms_wf_hi_procinst (
                        id_, proc_inst_id_, business_key_, proc_def_id_, start_time_, end_time_, duration_ms_,
                        start_user_id_, end_act_id_, delete_reason_, start_act_id_, state_
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        process_instance_id,
                        process_instance_id,
                        business_key,
                        process_definition_id,
                        start_time,
                        end_time,
                        duration_ms,
                        None,
                        None if not terminal else task_definition_key,
                        "rejected" if str(task.get("status") or "") == "已驳回" else None,
                        "startEvent",
                        "COMPLETED" if terminal else "ACTIVE",
                    ),
                )
                inserted_procinsts.add(process_instance_id)

            cur.execute(
                """
                INSERT INTO dtlms_wf_hi_taskinst (
                    id_, task_def_key_, proc_def_id_, proc_inst_id_, exec_id_, name_, business_key_, assignee_, owner_,
                    start_time_, claim_time_, end_time_, duration_ms_, due_date_, delete_reason_, priority_, category_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    f"TASK-{int(task['id'])}",
                    task_definition_key,
                    process_definition_id,
                    process_instance_id,
                    execution_id,
                    task.get("title") or workflow_name,
                    business_key,
                    None,
                    None,
                    start_time,
                    None,
                    end_time,
                    duration_ms,
                    task.get("due_at"),
                    "rejected" if str(task.get("status") or "") == "已驳回" else None,
                    int(self._workflow_priority_value(task.get("priority"))),
                    task.get("business_module") or "流程中心",
                ),
            )

            self._insert_workflow_history_activities(
                cur,
                task=task,
                process_definition_id=process_definition_id,
                process_instance_id=process_instance_id,
                execution_id=execution_id,
                task_definition_key=task_definition_key,
            )

            self._insert_workflow_history_variables(
                cur,
                task=task,
                process_instance_id=process_instance_id,
                execution_id=execution_id,
                inserted_variables=inserted_variables,
            )

            if terminal:
                continue

            cur.execute(
                """
                INSERT INTO dtlms_wf_ru_execution (
                    id_, proc_inst_id_, proc_def_id_, business_key_, parent_id_, act_id_, is_active_, is_concurrent_, is_scope_, start_time_, start_user_id_
                ) VALUES (%s, %s, %s, %s, NULL, %s, TRUE, FALSE, TRUE, %s, %s)
                """,
                (execution_id, process_instance_id, process_definition_id, business_key, task_definition_key, start_time, None),
            )
            cur.execute(
                """
                INSERT INTO dtlms_wf_ru_task (
                    id_, exec_id_, proc_inst_id_, proc_def_id_, task_def_key_, name_, business_key_, assignee_, owner_,
                    create_time_, due_date_, claim_time_, priority_, suspension_state_, form_key_, description_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s, %s)
                """,
                (
                    f"TASK-{int(task['id'])}",
                    execution_id,
                    process_instance_id,
                    process_definition_id,
                    task_definition_key,
                    task.get("title") or workflow_name,
                    business_key,
                    None,
                    None,
                    start_time,
                    task.get("due_at"),
                    int(self._workflow_priority_value(task.get("priority"))),
                    1,
                    business_key,
                    task.get("form_summary"),
                ),
            )
            for group_id in candidate_groups:
                cur.execute(
                    "INSERT INTO dtlms_wf_ru_identitylink (task_id_, proc_inst_id_, user_id_, group_id_, link_type_) VALUES (%s, %s, NULL, %s, %s)",
                    (f"TASK-{int(task['id'])}", process_instance_id, group_id, "candidate"),
                )
            self._insert_workflow_runtime_variables(cur, task=task, process_instance_id=process_instance_id, execution_id=execution_id)

    def _insert_workflow_history_activities(
        self,
        cur: psycopg.Cursor[Any],
        task: dict[str, Any],
        process_definition_id: str,
        process_instance_id: str,
        execution_id: str,
        task_definition_key: str,
    ) -> None:
        history = list(task.get("history") or [])
        if not history:
            cur.execute(
                """
                INSERT INTO dtlms_wf_hi_actinst (
                    id_, proc_def_id_, proc_inst_id_, exec_id_, act_id_, act_name_, act_type_, assignee_, start_time_, end_time_, duration_ms_, business_key_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    f"ACT-{int(task['id'])}-0",
                    process_definition_id,
                    process_instance_id,
                    execution_id,
                    task_definition_key,
                    task.get("current_node") or task.get("title") or "流程节点",
                    "userTask",
                    None,
                    task.get("created_at"),
                    None if not self._is_workflow_terminal(task) else self._workflow_end_time(task),
                    self._workflow_duration_millis(task.get("created_at"), self._workflow_end_time(task) if self._is_workflow_terminal(task) else None),
                    task.get("business_key"),
                ),
            )
            return
        for index, entry in enumerate(history, start=1):
            operated_at = entry.get("operated_at")
            cur.execute(
                """
                INSERT INTO dtlms_wf_hi_actinst (
                    id_, proc_def_id_, proc_inst_id_, exec_id_, act_id_, act_name_, act_type_, assignee_, start_time_, end_time_, duration_ms_, business_key_
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    f"ACT-{int(task['id'])}-{index}",
                    process_definition_id,
                    process_instance_id,
                    execution_id,
                    entry.get("action") or task_definition_key,
                    entry.get("action_label") or entry.get("to_node") or entry.get("from_node") or task.get("current_node") or "流程节点",
                    "userTask",
                    entry.get("operator_username"),
                    operated_at,
                    operated_at,
                    0,
                    task.get("business_key"),
                ),
            )

    def _insert_workflow_history_variables(
        self,
        cur: psycopg.Cursor[Any],
        task: dict[str, Any],
        process_instance_id: str,
        execution_id: str,
        inserted_variables: set[str],
    ) -> None:
        for name, value in self._workflow_variable_rows(task).items():
            variable_id = f"HVAR-{process_instance_id}-{name}"
            if variable_id in inserted_variables:
                continue
            inserted_variables.add(variable_id)
            cur.execute(
                """
                INSERT INTO dtlms_wf_hi_varinst (
                    id_, proc_inst_id_, exec_id_, task_id_, name_, var_type_, text_value_, number_value_, json_value_, create_time_, last_updated_time_
                ) VALUES (%s, %s, %s, NULL, %s, %s, %s, %s, %s::jsonb, %s, %s)
                """,
                (
                    variable_id,
                    process_instance_id,
                    execution_id,
                    name,
                    "json" if isinstance(value, (dict, list)) else ("number" if isinstance(value, int) else "string"),
                    None if isinstance(value, (dict, list, int)) else str(value),
                    value if isinstance(value, int) else None,
                    self._json_payload(value) if isinstance(value, (dict, list)) else self._json_payload({"value": value}),
                    task.get("created_at"),
                    self._workflow_end_time(task) or task.get("created_at"),
                ),
            )

    def _insert_workflow_runtime_variables(self, cur: psycopg.Cursor[Any], task: dict[str, Any], process_instance_id: str, execution_id: str) -> None:
        for name, value in self._workflow_variable_rows(task).items():
            cur.execute(
                """
                INSERT INTO dtlms_wf_ru_variable (
                    id_, exec_id_, proc_inst_id_, task_id_, name_, var_type_, text_value_, number_value_, json_value_, create_time_
                ) VALUES (%s, %s, %s, NULL, %s, %s, %s, %s, %s::jsonb, %s)
                """,
                (
                    f"RVAR-{process_instance_id}-{name}",
                    execution_id,
                    process_instance_id,
                    name,
                    "json" if isinstance(value, (dict, list)) else ("number" if isinstance(value, int) else "string"),
                    None if isinstance(value, (dict, list, int)) else str(value),
                    value if isinstance(value, int) else None,
                    self._json_payload(value) if isinstance(value, (dict, list)) else self._json_payload({"value": value}),
                    task.get("created_at"),
                ),
            )

    @staticmethod
    def _workflow_priority_value(priority: Any) -> int:
        mapping = {"低": 25, "中": 50, "高": 75, "紧急": 100}
        return mapping.get(str(priority or "中"), 50)

    @staticmethod
    def _is_workflow_terminal(task: dict[str, Any]) -> bool:
        return str(task.get("status") or "") in {"已通过", "已驳回"} or str(task.get("current_node") or "") == "流程结束"

    @staticmethod
    def _workflow_end_time(task: dict[str, Any]) -> str | None:
        history = list(task.get("history") or [])
        if history:
            return str(history[-1].get("operated_at") or "") or None
        return None

    def _workflow_duration_millis(self, start_time: Any, end_time: Any) -> int | None:
        if not start_time or not end_time:
            return None
        try:
            started_at = datetime.strptime(str(start_time), "%Y-%m-%d %H:%M:%S")
            ended_at = datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
        return max(int((ended_at - started_at).total_seconds() * 1000), 0)

    @staticmethod
    def _workflow_variable_rows(task: dict[str, Any]) -> dict[str, Any]:
        return {
            "businessKey": str(task.get("business_key") or ""),
            "businessModule": str(task.get("business_module") or "流程中心"),
            "flowCode": str(task.get("flow_code") or ""),
            "entityId": int(task.get("entity_id") or 0),
            "currentNode": str(task.get("current_node") or ""),
            "taskStatus": str(task.get("status") or ""),
            "candidateGroups": [str(item) for item in task.get("candidate_groups") or []],
        }

    @staticmethod
    def _workflow_id_slug(value: str | None, max_length: int) -> str:
        normalized = "".join(character.lower() for character in str(value or "") if character.isalnum())
        if not normalized:
            normalized = "x"
        return normalized[:max_length]

    @staticmethod
    def _workflow_id_hash(*parts: Any, length: int = 10) -> str:
        raw_value = "::".join(str(part or "") for part in parts)
        return hashlib.sha1(raw_value.encode("utf-8")).hexdigest()[:length]

    @classmethod
    def _workflow_deployment_id(cls, process_definition_key: str) -> str:
        return f"dep-{cls._workflow_id_slug(process_definition_key, 24)}-{cls._workflow_id_hash(process_definition_key, 'deployment', length=8)}"

    @classmethod
    def _workflow_process_definition_id(cls, process_definition_key: str) -> str:
        return f"procdef-{cls._workflow_id_slug(process_definition_key, 20)}-v1-{cls._workflow_id_hash(process_definition_key, 'process-definition', length=8)}"

    @classmethod
    def _workflow_process_instance_id(cls, process_definition_key: str, business_key: str) -> str:
        return (
            f"procinst-{cls._workflow_id_slug(process_definition_key, 16)}-"
            f"{cls._workflow_id_slug(business_key, 18)}-"
            f"{cls._workflow_id_hash(process_definition_key, business_key, 'process-instance', length=10)}"
        )

    @classmethod
    def _workflow_execution_id(cls, process_instance_id: str, task_definition_key: str) -> str:
        return f"exec-{cls._workflow_id_slug(task_definition_key, 18)}-{cls._workflow_id_hash(process_instance_id, task_definition_key, 'execution', length=10)}"

    def _fetch_map(self, cur: psycopg.Cursor[Any], query: str) -> dict[str, Any]:
        cur.execute(query)
        rows = cur.fetchall()
        if not rows:
            return {}
        first_row = rows[0]
        if isinstance(first_row, dict):
            return {str(row["key"]): row["id"] for row in rows}
        return {str(row[1]): row[0] for row in rows}

    @staticmethod
    def _parse_json_list(value: Any) -> list[dict[str, Any]]:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if not value:
            return []
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return []
            if isinstance(parsed, list):
                return [item for item in parsed if isinstance(item, dict)]
        return []

    @classmethod
    def _derive_portal_profile(cls, student: dict[str, Any]) -> dict[str, Any] | None:
        profile = student.get("profile") if isinstance(student.get("profile"), dict) else {}
        for key in (
            "full_name_pinyin",
            "profile_photo_url",
            "gender",
            "birth_date",
            "ethnic_group",
            "native_place",
            "political_status",
            "marital_status",
            "religious_belief",
            "id_type",
            "mailing_address",
            "emergency_contact_name",
            "emergency_contact_phone",
        ):
            profile.setdefault(key, student.get(key))
        return profile if any(value not in (None, "", [], {}) for value in profile.values()) else None

    @classmethod
    def _derive_portal_application_draft(cls, student: dict[str, Any]) -> dict[str, Any] | None:
        draft = student.get("application_draft") if isinstance(student.get("application_draft"), dict) else {}
        preferences = draft.get("preferences") if isinstance(draft.get("preferences"), list) else []
        if not preferences and student.get("selected_team_name"):
            preferences = [
                {
                    "preference_order": 1,
                    "research_center_name": student.get("selected_team_name"),
                    "advisor_name": student.get("selected_advisor_name"),
                    "is_optional": False,
                }
            ]
        english_proficiencies = draft.get("english_proficiencies") if isinstance(draft.get("english_proficiencies"), list) else []
        english_level = str(student.get("english_level") or "").strip()
        if not english_proficiencies and english_level:
            exam_name, _, score_text = english_level.partition(":")
            english_proficiencies = [{"exam_name": exam_name.strip() or english_level, "score_text": score_text.strip() or None}]
        personal_statement = draft.get("personal_statement") if isinstance(draft.get("personal_statement"), dict) else {}
        if student.get("personal_statement_text") and not personal_statement.get("personal_statement_text"):
            personal_statement["personal_statement_text"] = student.get("personal_statement_text")
        declaration = draft.get("declaration") if isinstance(draft.get("declaration"), dict) else {}
        declaration.setdefault("has_read_declaration", bool(student.get("signed_agreement")))
        derived = {
            "selected_plan_id": draft.get("selected_plan_id", student.get("selected_plan_id")),
            "source_channel": draft.get("source_channel"),
            "source_channel_other": draft.get("source_channel_other"),
            "preferences": preferences,
            "education_experiences": draft.get("education_experiences") or cls._parse_json_list(student.get("education_experience")),
            "practice_experiences": draft.get("practice_experiences") or cls._parse_json_list(student.get("practice_experience")),
            "english_proficiencies": english_proficiencies,
            "family_members": draft.get("family_members") or cls._parse_json_list(student.get("family_info")),
            "achievement_records": draft.get("achievement_records") or cls._parse_json_list(student.get("recommendation_notes")),
            "personal_statement": personal_statement,
            "declaration": declaration,
            "submitted_at": draft.get("submitted_at", student.get("submitted_at")),
        }
        has_content = any(value not in (None, "", [], {}) for key, value in derived.items() if key != "selected_plan_id") or derived.get("selected_plan_id") is not None
        return derived if has_content else None

    @staticmethod
    def _match_portal_application(student: dict[str, Any], application_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
        student_id = int(student.get("id") or 0)
        selected_plan_id = student.get("selected_plan_id")
        phone_number = student.get("phone_number")
        email = student.get("email")
        id_number = student.get("id_number")
        for item in application_rows:
            if int(item.get("portal_student_id") or 0) == student_id and (selected_plan_id is None or int(item.get("plan_id") or 0) == int(selected_plan_id)):
                return item
        for item in application_rows:
            if selected_plan_id is not None and int(item.get("plan_id") or 0) != int(selected_plan_id):
                continue
            if phone_number and item.get("phone_number") == phone_number:
                return item
            if email and item.get("email") == email:
                return item
            if id_number and item.get("id_number") == id_number:
                return item
        return None

    def get_portal_student_detail(self, student_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ps.*,
                        pp.full_name_pinyin,
                        pp.profile_photo_url,
                        pp.emergency_contact_name,
                        pp.emergency_contact_phone
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_portal_student_profiles pp ON pp.portal_student_id = ps.id
                    WHERE ps.id = %s
                    """,
                    (int(student_id),),
                )
                row = cur.fetchone()
                if not row:
                    return None
                student = dict(row)
                profile = self._derive_portal_profile(student)
                if profile is not None:
                    student["profile"] = profile

                selected_plan_id = student.get("selected_plan_id")
                cur.execute(
                    """
                    SELECT id, plan_id, source_channel, source_channel_other, intended_advisor_name, applied_at
                    FROM dtlms_recruitment_applications
                    WHERE is_deleted = FALSE AND portal_student_id = %s
                    ORDER BY CASE WHEN plan_id = %s THEN 0 ELSE 1 END,
                             COALESCE(applied_at, created_at) DESC,
                             id DESC
                    LIMIT 1
                    """,
                    (int(student_id), int(selected_plan_id) if selected_plan_id is not None else -1),
                )
                application = cur.fetchone()
                if not application:
                    draft = self._derive_portal_application_draft(student)
                    if draft is not None:
                        student["application_draft"] = draft
                    return student

                application_id = int(application["id"])
                cur.execute(
                    """
                    SELECT preference_order, research_center_name, advisor_name, is_optional
                    FROM dtlms_portal_application_preferences
                    WHERE application_id = %s
                    ORDER BY preference_order ASC, id ASC
                    """,
                    (application_id,),
                )
                preferences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT sort_order, education_stage, start_month, end_month, school_name, major_name,
                           average_score, gpa, ranking, verifier_name, verifier_phone,
                           transcript_attachment_url, degree_certificate_attachment_url
                    FROM dtlms_portal_application_education_experiences
                    WHERE application_id = %s
                    ORDER BY sort_order ASC, id ASC
                    """,
                    (application_id,),
                )
                education_experiences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT start_month, end_month, organization_name, position_name, responsibility_text,
                           verifier_name, verifier_phone
                    FROM dtlms_portal_application_practice_experiences
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                practice_experiences = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT exam_name, score_text, certificate_attachment_url
                    FROM dtlms_portal_application_english_proficiencies
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                english_proficiencies = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT member_name, relation_type, employer_name, job_title, contact_phone
                    FROM dtlms_portal_application_family_members
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                family_members = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT achievement_type, paper_title, author_order, journal_or_conference,
                           publish_or_index_month, award_name, awarding_organization,
                           award_level, award_year, responsibility_text
                    FROM dtlms_portal_application_achievement_records
                    WHERE application_id = %s
                    ORDER BY id ASC
                    """,
                    (application_id,),
                )
                achievement_records = [dict(item) for item in cur.fetchall()]
                cur.execute(
                    """
                    SELECT personal_statement_text, ai_problem_statement, ai_industry_opinion, resume_attachment_url
                    FROM dtlms_portal_application_personal_statements
                    WHERE application_id = %s
                    """,
                    (application_id,),
                )
                personal_statement_row = cur.fetchone()
                cur.execute(
                    """
                    SELECT has_read_declaration, declaration_text, progress_snapshot
                    FROM dtlms_portal_application_declarations
                    WHERE application_id = %s
                    """,
                    (application_id,),
                )
                declaration_row = cur.fetchone()
                student["application_draft"] = {
                    "selected_plan_id": int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None,
                    "source_channel": application.get("source_channel"),
                    "source_channel_other": application.get("source_channel_other"),
                    "preferences": preferences,
                    "education_experiences": education_experiences,
                    "practice_experiences": practice_experiences,
                    "english_proficiencies": english_proficiencies,
                    "family_members": family_members,
                    "achievement_records": achievement_records,
                    "personal_statement": dict(personal_statement_row) if personal_statement_row else {},
                    "declaration": dict(declaration_row) if declaration_row else {"has_read_declaration": bool(student.get("signed_agreement"))},
                    "submitted_at": self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at"),
                }
                if preferences:
                    student["selected_team_name"] = preferences[0].get("research_center_name") or student.get("selected_team_name")
                    student["selected_advisor_name"] = preferences[0].get("advisor_name") or application.get("intended_advisor_name") or student.get("selected_advisor_name")
                student["selected_plan_id"] = int(application.get("plan_id") or student.get("selected_plan_id") or 0) or None
                student["submitted_at"] = self._stringify_datetime(application.get("applied_at")) or student.get("submitted_at")
                return student

    def list_workflow_tasks_page(
        self,
        status: str | None = None,
        module: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if status:
            where_clauses.append("COALESCE(payload->>'status', '') = %s")
            params.append(status)
        if module:
            where_clauses.append("COALESCE(payload->>'business_module', '') = %s")
            params.append(module)
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                concat_ws(
                    ' ',
                    COALESCE(payload->>'workflow_name', ''),
                    COALESCE(payload->>'business_key', ''),
                    COALESCE(payload->>'title', ''),
                    COALESCE(payload->>'applicant_name', ''),
                    COALESCE(payload->>'current_handler', '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT COUNT(*) AS total FROM dtlms_runtime_workflow_tasks WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                cur.execute(
                    f"""
                    SELECT payload
                    FROM dtlms_runtime_workflow_tasks
                    WHERE {where_sql}
                    ORDER BY COALESCE(payload->>'created_at', '') DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                items: list[dict[str, Any]] = []
                for row in cur.fetchall():
                    payload = row.get("payload")
                    if isinstance(payload, dict):
                        items.append(payload)
                return items, total

    def list_students_page(
        self,
        keyword: str | None = None,
        status: str | None = None,
        advisor_name: str | None = None,
        center_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["s.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    s.student_no ILIKE %s
                    OR s.full_name ILIKE %s
                    OR COALESCE(t.team_name, '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if status:
            where_clauses.append("s.current_status = %s")
            params.append(self._map_student_status(status))
        if advisor_name:
            where_clauses.append("COALESCE(a.full_name, '') = %s")
            params.append(advisor_name)
        if center_name:
            where_clauses.append("COALESCE(t.team_name, '') = %s")
            params.append(center_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                """
                cur.execute(count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        s.id,
                        s.student_no,
                        s.full_name,
                        s.current_status,
                        COALESCE(a.full_name, '') AS advisor_name,
                        COALESCE(t.team_name, '') AS team_name,
                        s.degree_type,
                        s.enrollment_year,
                        s.phone_number,
                        s.political_status
                    FROM dtlms_students s
                    LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
                    LEFT JOIN dtlms_teams t ON t.id = s.team_id
                    WHERE {where_sql}
                    ORDER BY s.id DESC
                    LIMIT %s OFFSET %s
                """
                cur.execute(page_sql, [*params, page_size, offset])
                return [self._normalize_student_row(dict(row)) for row in cur.fetchall()], total

    def list_registered_portal_students_page(
        self,
        keyword: str | None = None,
        application_form_status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    ps.full_name ILIKE %s
                    OR ps.phone_number ILIKE %s
                    OR ps.email ILIKE %s
                    OR ps.id_number ILIKE %s
                    OR COALESCE(rp.plan_name, '') ILIKE %s
                    OR COALESCE(ps.selected_advisor_name, '') ILIKE %s
                    OR COALESCE(ps.selected_team_name, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 7)

        normalized_status = str(application_form_status or "").strip()
        if normalized_status == "已填写报名":
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NOT NULL")
        elif normalized_status == "未填写报名":
            where_clauses.append("COALESCE(ps.submitted_at, latest_application.applied_at) IS NULL")

        where_sql = " AND ".join(where_clauses)
        latest_application_sql = """
            LEFT JOIN LATERAL (
                SELECT ra.application_status, ra.applied_at
                FROM dtlms_recruitment_applications ra
                WHERE ra.is_deleted = FALSE AND ra.portal_student_id = ps.id
                ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                LIMIT 1
            ) latest_application ON TRUE
        """

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                """
                cur.execute(count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        ps.id,
                        ps.full_name,
                        ps.phone_number,
                        ps.email,
                        ps.id_number,
                        ps.account_status,
                        rp.plan_name AS selected_plan_name,
                        ps.selected_team_name,
                        ps.selected_advisor_name,
                        ps.created_at,
                        ps.submitted_at,
                        latest_application.application_status,
                        latest_application.applied_at
                    FROM dtlms_portal_students ps
                    LEFT JOIN dtlms_recruitment_plans rp ON rp.id = ps.selected_plan_id
                    {latest_application_sql}
                    WHERE {where_sql}
                    ORDER BY ps.created_at DESC, ps.id DESC
                    LIMIT %s OFFSET %s
                """
                cur.execute(page_sql, [*params, page_size, offset])
                return [self._normalize_registered_portal_student_row(dict(row)) for row in cur.fetchall()], total

    def list_operation_logs_page(
        self,
        keyword: str | None = None,
        module_name: str | None = None,
        result: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                (
                    operator_username ILIKE %s
                    OR entity_name ILIKE %s
                    OR COALESCE(new_value->>'summary', '') ILIKE %s
                )
                """
            )
            keyword_like = f"%{str(keyword).strip()}%"
            params.extend([keyword_like, keyword_like, keyword_like])
        if module_name:
            where_clauses.append("module_name = %s")
            params.append(module_name)
        if result:
            where_clauses.append("result = %s")
            params.append(result)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT COUNT(*) AS total FROM dtlms_operation_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                cur.execute(
                    f"""
                    SELECT id, created_at, operator_username, module_name, entity_name, entity_id, action, result, new_value
                    FROM dtlms_operation_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_operation_log_row(dict(row)) for row in cur.fetchall()], total

    def list_recruitment_applications_page(
        self,
        keyword: str | None = None,
        plan_id: int | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["ra.is_deleted = FALSE"]
        params: list[Any] = []

        if plan_id is not None:
            where_clauses.append("ra.plan_id = %s")
            params.append(int(plan_id))
        if status:
            where_clauses.append("ra.application_status = %s")
            params.append(self._map_application_status(status))
        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    COALESCE(ra.business_key, '') ILIKE %s
                    OR COALESCE(ra.candidate_no, '') ILIKE %s
                    OR COALESCE(ra.student_name, '') ILIKE %s
                    OR COALESCE(ra.graduation_school, '') ILIKE %s
                    OR COALESCE(ra.graduate_school, '') ILIKE %s
                    OR COALESCE(rf.field_name, '') ILIKE %s
                    OR COALESCE(ra.first_choice, '') ILIKE %s
                    OR COALESCE(ra.second_choice, '') ILIKE %s
                    OR COALESCE(ra.intended_advisor_name, '') ILIKE %s
                    OR COALESCE(ra.phone_number, '') ILIKE %s
                    OR COALESCE(ra.email, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like] * 11)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    WHERE {where_sql}
                """
                cur.execute(count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        ra.*,
                        rf.field_name AS intended_field,
                        am.material_status,
                        qr.reviewer_username AS reviewer_name,
                        ad.final_score
                    FROM dtlms_recruitment_applications ra
                    LEFT JOIN dtlms_research_fields rf ON rf.id = ra.intended_field_id AND rf.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT material_status
                        FROM dtlms_application_materials
                        WHERE application_id = ra.id AND is_deleted = FALSE
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) am ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT reviewer_username
                        FROM dtlms_qualification_reviews
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) qr ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT final_score
                        FROM dtlms_admission_decisions
                        WHERE application_id = ra.id
                        ORDER BY updated_at DESC, id DESC
                        LIMIT 1
                    ) ad ON TRUE
                    WHERE {where_sql}
                    ORDER BY COALESCE(ra.applied_at, ra.created_at) DESC, ra.id DESC
                    LIMIT %s OFFSET %s
                """
                cur.execute(page_sql, [*params, page_size, offset])
                return [self._normalize_recruitment_application_row(dict(row)) for row in cur.fetchall()], total

    def list_centers_page(
        self,
        keyword: str | None = None,
        is_enabled: bool | None = None,
        director_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["t.is_deleted = FALSE"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    t.team_name ILIKE %s
                    OR COALESCE(lead.full_name, '') ILIKE %s
                    OR EXISTS (
                        SELECT 1
                        FROM dtlms_team_advisors ta_keyword
                        JOIN dtlms_advisors advisor_keyword ON advisor_keyword.id = ta_keyword.advisor_id AND advisor_keyword.is_deleted = FALSE
                        WHERE ta_keyword.team_id = t.id
                          AND ta_keyword.is_deleted = FALSE
                          AND advisor_keyword.full_name ILIKE %s
                    )
                )
                """
            )
            params.extend([keyword_like] * 3)
        if is_enabled is not None:
            where_clauses.append("t.team_status = %s" if is_enabled else "t.team_status <> %s")
            params.append("active")
        if director_name:
            where_clauses.append("COALESCE(lead.full_name, '') = %s")
            params.append(director_name)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                count_sql = f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    WHERE {where_sql}
                """
                cur.execute(count_sql, params)
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                page_sql = f"""
                    SELECT
                        t.id,
                        t.team_name,
                        lead.full_name AS director_name,
                        COALESCE(advisor_names.advisor_names, '') AS advisor_names,
                        t.team_status,
                        COALESCE(TO_CHAR(t.established_on, 'YYYY-MM-DD'), TO_CHAR(t.created_at::date, 'YYYY-MM-DD')) AS created_date,
                        COALESCE(student_stats.member_student_count, 0) AS member_student_count,
                        COALESCE(student_stats.active_student_count, 0) AS active_student_count
                    FROM dtlms_teams t
                    LEFT JOIN dtlms_advisors lead ON lead.id = t.lead_advisor_id AND lead.is_deleted = FALSE
                    LEFT JOIN LATERAL (
                        SELECT string_agg(DISTINCT advisor.full_name, '、' ORDER BY advisor.full_name) AS advisor_names
                        FROM dtlms_team_advisors ta
                        JOIN dtlms_advisors advisor ON advisor.id = ta.advisor_id AND advisor.is_deleted = FALSE
                        WHERE ta.team_id = t.id AND ta.is_deleted = FALSE
                    ) advisor_names ON TRUE
                    LEFT JOIN LATERAL (
                        SELECT
                            COUNT(*) AS member_student_count,
                            COUNT(*) FILTER (WHERE s.current_status IN ('enrolled', 'internship', 'outbound', 'thesis')) AS active_student_count
                        FROM dtlms_students s
                        WHERE s.team_id = t.id AND s.is_deleted = FALSE
                    ) student_stats ON TRUE
                    WHERE {where_sql}
                    ORDER BY t.id DESC
                    LIMIT %s OFFSET %s
                """
                cur.execute(page_sql, [*params, page_size, offset])
                return [self._normalize_center_row(dict(row)) for row in cur.fetchall()], total

    def list_sync_logs_page(
        self,
        keyword: str | None = None,
        sync_status: str | None = None,
        source_system: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    source_system ILIKE %s
                    OR target_system ILIKE %s
                    OR COALESCE(failure_reason, '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if sync_status:
            where_clauses.append("sync_status = %s")
            params.append(sync_status)
        if source_system:
            where_clauses.append("source_system = %s")
            params.append(source_system)

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT COUNT(*) AS total FROM dtlms_data_sync_logs WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                cur.execute(
                    f"""
                    SELECT id, source_system, target_system, sync_status, record_count, created_at, failure_reason
                    FROM dtlms_data_sync_logs
                    WHERE {where_sql}
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_sync_log_row(dict(row)) for row in cur.fetchall()], total

    def list_system_users_page(
        self,
        keyword: str | None = None,
        role_code: str | None = None,
        account_status: str | None = None,
        department_name: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if keyword and str(keyword).strip():
            keyword_like = f"%{str(keyword).strip()}%"
            where_clauses.append(
                """
                (
                    COALESCE(u.payload->>'username', '') ILIKE %s
                    OR COALESCE(u.payload->>'full_name', '') ILIKE %s
                    OR COALESCE(u.payload->>'department_name', '') ILIKE %s
                )
                """
            )
            params.extend([keyword_like, keyword_like, keyword_like])
        if role_code:
            where_clauses.append("COALESCE(u.payload->>'role_code', '') = %s")
            params.append(role_code)
        if account_status:
            where_clauses.append("COALESCE(u.payload->>'account_status', '') = %s")
            params.append(account_status)
        if department_name:
            where_clauses.append("COALESCE(u.payload->>'department_name', '') ILIKE %s")
            params.append(f"%{department_name}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT COUNT(*) AS total FROM dtlms_runtime_system_users u WHERE {where_sql}",
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                cur.execute(
                    f"""
                    SELECT u.payload AS user_payload, r.payload AS role_payload
                    FROM dtlms_runtime_system_users u
                    LEFT JOIN dtlms_runtime_roles r ON COALESCE(r.payload->>'role_code', '') = COALESCE(u.payload->>'role_code', '')
                    WHERE {where_sql}
                    ORDER BY u.id DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_system_user_row(dict(row)) for row in cur.fetchall()], total

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
    def _student_status_label(value: str | None) -> str:
        mapping = {
            "enrolled": "在校",
            "outbound": "外出研修",
            "thesis": "学位论文阶段",
            "internship": "实习中",
        }
        return mapping.get(str(value or ""), "在校")

    @classmethod
    def _normalize_student_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "student_no": str(row.get("student_no") or ""),
            "full_name": str(row.get("full_name") or ""),
            "status": cls._student_status_label(row.get("current_status")),
            "advisor_name": str(row.get("advisor_name") or ""),
            "center_name": str(row.get("team_name") or ""),
            "degree_type": str(row.get("degree_type") or ""),
            "enrollment_year": int(row.get("enrollment_year") or 0),
            "phone_number": row.get("phone_number"),
            "political_status": row.get("political_status"),
        }

    @classmethod
    def _normalize_registered_portal_student_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        submitted_at = cls._stringify_datetime(row.get("submitted_at") or row.get("applied_at"))
        return {
            "id": int(row["id"]),
            "full_name": str(row.get("full_name") or ""),
            "phone_number": str(row.get("phone_number") or ""),
            "email": str(row.get("email") or ""),
            "id_number": str(row.get("id_number") or ""),
            "account_status": cls._normalize_portal_account_status(row.get("account_status")),
            "application_form_status": "已填写报名" if submitted_at else "未填写报名",
            "selected_plan_name": row.get("selected_plan_name"),
            "selected_center_name": row.get("selected_team_name"),
            "selected_advisor_name": row.get("selected_advisor_name"),
            "recruitment_application_status": cls._application_status_label(row.get("application_status")) if row.get("application_status") else None,
            "registered_at": cls._stringify_datetime(row.get("created_at")),
            "submitted_at": submitted_at,
        }

    @staticmethod
    def _normalize_portal_account_status(value: Any) -> str:
        text = str(value or "").strip()
        if text in {"已注销", "停用"}:
            return "停用"
        return "启用"

    @staticmethod
    def _normalize_operation_log_row(row: dict[str, Any]) -> dict[str, Any]:
        new_value = row.get("new_value") if isinstance(row.get("new_value"), dict) else {}
        return {
            "id": int(row["id"]),
            "operated_at": str(row.get("created_at") or ""),
            "operator_username": str(row.get("operator_username") or ""),
            "module_name": str(row.get("module_name") or ""),
            "entity_name": str(row.get("entity_name") or ""),
            "entity_id": str(row.get("entity_id") or ""),
            "action": str(row.get("action") or ""),
            "result": str(row.get("result") or ""),
            "summary": str(new_value.get("summary") or ""),
        }

    @classmethod
    def _normalize_recruitment_application_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "plan_id": int(row.get("plan_id") or 0),
            "business_key": str(row.get("business_key") or ""),
            "candidate_no": row.get("candidate_no"),
            "review_round": row.get("review_round"),
            "student_name": str(row.get("student_name") or ""),
            "first_choice": row.get("first_choice"),
            "second_choice": row.get("second_choice"),
            "gender": row.get("gender"),
            "political_status": row.get("political_status"),
            "marital_status": row.get("marital_status"),
            "religious_belief": row.get("religious_belief"),
            "native_place": row.get("native_place"),
            "phone_number": row.get("phone_number"),
            "email": row.get("email"),
            "mailing_address": row.get("mailing_address"),
            "id_type": row.get("id_type"),
            "id_number": row.get("id_number"),
            "graduation_school": str(row.get("graduation_school") or ""),
            "undergraduate_school": row.get("undergraduate_school"),
            "accept_adjustment": row.get("accept_adjustment"),
            "undergraduate_average_score": row.get("undergraduate_average_score"),
            "undergraduate_gpa": row.get("undergraduate_gpa"),
            "undergraduate_rank": row.get("undergraduate_rank"),
            "undergraduate_major": row.get("undergraduate_major"),
            "graduate_average_score": row.get("graduate_average_score"),
            "graduate_gpa": row.get("graduate_gpa"),
            "graduate_rank": row.get("graduate_rank"),
            "graduate_major": row.get("graduate_major"),
            "highest_degree": str(row.get("highest_degree") or ""),
            "intended_field": row.get("intended_field"),
            "intended_advisor_name": row.get("intended_advisor_name"),
            "discovery_channel": row.get("discovery_channel"),
            "source_channel": row.get("source_channel"),
            "source_channel_other": row.get("source_channel_other"),
            "graduate_school": row.get("graduate_school"),
            "overseas_university_name": row.get("overseas_university_name"),
            "overseas_master_university_name": row.get("overseas_master_university_name"),
            "self_evaluation": row.get("self_evaluation"),
            "applied_at": cls._stringify_datetime(row.get("applied_at")),
            "research_problem": row.get("research_problem"),
            "research_status_analysis": row.get("research_status_analysis"),
            "research_impact": row.get("research_impact"),
            "ai_society_impact": row.get("ai_society_impact"),
            "dissenting_view": row.get("dissenting_view"),
            "family_info": row.get("family_info"),
            "education_experience": row.get("education_experience"),
            "practice_experience": row.get("practice_experience"),
            "personal_statement_text": row.get("personal_statement_text"),
            "student_activity_experience": row.get("student_activity_experience"),
            "personal_statement_attachment": row.get("personal_statement_attachment"),
            "material_list_attachment": row.get("material_list_attachment"),
            "supplementary_profile": row.get("supplementary_profile"),
            "material_status": cls._material_status_label(row.get("material_status")),
            "application_status": cls._application_status_label(row.get("application_status")),
            "reviewer_name": row.get("reviewer_name"),
            "final_score": float(row["final_score"]) if row.get("final_score") is not None else None,
        }

    @classmethod
    def _normalize_center_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "center_name": str(row.get("team_name") or ""),
            "director_name": str(row.get("director_name") or ""),
            "advisor_names": cls._split_delimited_values(row.get("advisor_names")),
            "is_enabled": str(row.get("team_status") or "") == "active",
            "created_date": cls._stringify_datetime(row.get("created_date")),
            "member_student_count": int(row.get("member_student_count") or 0),
            "active_student_count": int(row.get("active_student_count") or 0),
        }

    @classmethod
    def _normalize_sync_log_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "source_system": str(row.get("source_system") or ""),
            "target_system": str(row.get("target_system") or ""),
            "sync_status": str(row.get("sync_status") or ""),
            "record_count": int(row.get("record_count") or 0),
            "executed_at": cls._stringify_datetime(row.get("created_at")) or "",
            "failure_reason": row.get("failure_reason"),
        }

    @classmethod
    def _normalize_system_user_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        user_payload = row.get("user_payload") if isinstance(row.get("user_payload"), dict) else {}
        role_payload = row.get("role_payload") if isinstance(row.get("role_payload"), dict) else {}
        return {
            "id": int(user_payload.get("id") or 0),
            "username": str(user_payload.get("username") or ""),
            "full_name": str(user_payload.get("full_name") or ""),
            "role_code": str(user_payload.get("role_code") or ""),
            "role_name": str(role_payload.get("role_name") or user_payload.get("role_code") or ""),
            "department_name": str(user_payload.get("department_name") or ""),
            "phone_number": user_payload.get("phone_number"),
            "account_status": str(user_payload.get("account_status") or ""),
            "last_login_at": cls._stringify_datetime(user_payload.get("last_login_at")),
        }

    @staticmethod
    def _stringify_datetime(value: Any) -> str | None:
        if value is None:
            return None
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        text = str(value).strip()
        return text or None

    @staticmethod
    def _split_delimited_values(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        text = str(value or "").strip()
        if not text:
            return []
        return [item.strip() for item in text.split("、") if item.strip()]

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
    def _team_status_label(value: str | None) -> str:
        mapping = {
            "active": "启用",
            "inactive": "停用",
            "planning": "筹建",
            "archived": "归档",
        }
        return mapping.get(str(value or ""), "启用")

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
            "同意录取": "admitted",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _application_status_label(value: str | None) -> str:
        mapping = {
            "submitted": "报名已提交",
            "qualified": "资格审核通过",
            "scoring": "材料评分中",
            "interviewed": "面试完成",
            "pre_admitted": "预录取",
            "admitted": "同意录取",
        }
        return mapping.get(str(value or ""), "报名已提交")

    @staticmethod
    def _map_material_status(value: str) -> str:
        mapping = {
            "材料齐全": "approved",
            "待补材料": "pending",
        }
        return mapping.get(value, "pending")

    @staticmethod
    def _material_status_label(value: str | None) -> str:
        mapping = {
            "approved": "材料齐全",
            "pending": "待补材料",
        }
        return mapping.get(str(value or ""), "待补材料")

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