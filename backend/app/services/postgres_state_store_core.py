from __future__ import annotations

from datetime import datetime
import hashlib
import json
import logging
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


logger = logging.getLogger(__name__)

WORKFLOW_FLOW_DATASET_MAP = {
    "recruitment_application": "recruitment_applications",
    "scientific_report": "scientific_reports",
    "outbound_study": "outbound_studies",
    "thesis": "theses",
}


class PostgresStateStoreCoreMixin:
    if TYPE_CHECKING:
        def _seed_relational_tables(self, cur: psycopg.Cursor[Any], state: dict[str, Any]) -> None: ...

    CONNECT_TIMEOUT_SECONDS = 5
    SCHEMA_SENTINEL_REGCLASS = "public.dtlms_users"
    def __init__(self) -> None:
        self._schema_ready = False

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
        cur.execute("SELECT to_regclass(%s) AS table_name", (self.SCHEMA_SENTINEL_REGCLASS,))
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

    @staticmethod
    def _execute_dynamic(cur: psycopg.Cursor[Any], query: str, params: Any | None = None) -> None:
        cur.execute(cast(Any, query), params)

    def ensure_database(self) -> None:
        with self._connect("postgres", autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.postgres_db,))
                exists = cur.fetchone() is not None
                if not exists:
                    self._execute_dynamic(cur, f'CREATE DATABASE "{settings.postgres_db}"')

    def ensure_schema(self) -> None:
        if self._schema_ready:
            return
        self.ensure_database()
        with self._connect(settings.postgres_db, autocommit=True) as conn:
            with conn.cursor() as cur:
                if self._schema_initialized(cur):
                    self._schema_ready = True
                    return
                raise RuntimeError(
                    "PostgreSQL formal schema is missing. Automatic SQL file execution has been disabled; apply the required schema updates manually before starting the service."
                )

    def load_state(self) -> dict[str, Any] | None:
        self.ensure_schema()
        return None

    def save_state(self, state: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._seed_relational_tables(cur, state)
            conn.commit()

    def normalize_recruitment_application_business_keys(self) -> int:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS tmp_startup_recruitment_application_business_keys")
                cur.execute(
                    """
                    CREATE TEMP TABLE tmp_startup_recruitment_application_business_keys (
                        application_id BIGINT PRIMARY KEY,
                        old_workflow_key VARCHAR(64),
                        new_business_key VARCHAR(64) NOT NULL
                    ) ON COMMIT DROP
                    """
                )
                cur.execute(
                    """
                    INSERT INTO tmp_startup_recruitment_application_business_keys (application_id, old_workflow_key, new_business_key)
                    WITH numbered AS (
                        SELECT
                            ra.id AS application_id,
                            COALESCE(
                                workflow_key.old_workflow_key,
                                NULLIF(BTRIM(COALESCE(ra.business_key, ra.candidate_no, '')), '')
                            ) AS old_workflow_key,
                            CONCAT(
                                'SH',
                                (
                                    COALESCE(
                                        EXTRACT(YEAR FROM COALESCE(ra.applied_at, ra.created_at, CURRENT_TIMESTAMP))::INTEGER,
                                        EXTRACT(YEAR FROM CURRENT_TIMESTAMP)::INTEGER
                                    ) + 1
                                )::TEXT,
                                LPAD(
                                    ROW_NUMBER() OVER (
                                        PARTITION BY COALESCE(
                                            EXTRACT(YEAR FROM COALESCE(ra.applied_at, ra.created_at, CURRENT_TIMESTAMP))::INTEGER,
                                            EXTRACT(YEAR FROM CURRENT_TIMESTAMP)::INTEGER
                                        ) + 1
                                        ORDER BY COALESCE(ra.applied_at, ra.created_at, CURRENT_TIMESTAMP), ra.id
                                    )::TEXT,
                                    4,
                                    '0'
                                )
                            ) AS new_business_key
                        FROM dtlms_recruitment_applications ra
                                                LEFT JOIN LATERAL (
                                                        SELECT NULLIF(BTRIM(ht.business_key_), '') AS old_workflow_key
                                                        FROM dtlms_wf_hi_varinst hv_entity
                                                        JOIN dtlms_wf_hi_varinst hv_flow
                                                            ON hv_flow.proc_inst_id_ = hv_entity.proc_inst_id_
                                                         AND hv_flow.name_ = 'flowCode'
                                                        JOIN dtlms_wf_hi_taskinst ht
                                                            ON ht.proc_inst_id_ = hv_entity.proc_inst_id_
                                                        WHERE hv_entity.name_ = 'entityId'
                                                            AND COALESCE(hv_entity.text_value_, hv_entity.json_value_ ->> 'value', '') = ra.id::TEXT
                                                            AND COALESCE(hv_flow.text_value_, hv_flow.json_value_ ->> 'value', '') = 'recruitment_application'
                                                            AND NULLIF(BTRIM(COALESCE(ht.business_key_, '')), '') IS NOT NULL
                                                        ORDER BY ht.start_time_ DESC, ht.id_ DESC
                                                        LIMIT 1
                                                ) workflow_key ON TRUE
                        WHERE ra.is_deleted = FALSE
                    )
                    SELECT application_id, old_workflow_key, new_business_key
                    FROM numbered
                    """
                )
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM dtlms_recruitment_applications ra
                    JOIN tmp_startup_recruitment_application_business_keys mapping
                      ON mapping.application_id = ra.id
                    WHERE ra.is_deleted = FALSE
                      AND (
                        ra.business_key IS DISTINCT FROM mapping.new_business_key
                        OR ra.candidate_no IS DISTINCT FROM mapping.new_business_key
                      )
                    """
                )
                changed_row = cur.fetchone()
                changed_count = int(changed_row[0] if changed_row else 0)
                if changed_count > 0:
                    cur.execute(
                        """
                        UPDATE dtlms_recruitment_applications ra
                        SET business_key = CONCAT('__TMP_SH__', ra.id::TEXT),
                            candidate_no = CONCAT('__TMP_SH__', ra.id::TEXT),
                            updated_at = CURRENT_TIMESTAMP
                        FROM tmp_startup_recruitment_application_business_keys mapping
                        WHERE ra.id = mapping.application_id
                          AND ra.is_deleted = FALSE
                          AND (
                            ra.business_key IS DISTINCT FROM mapping.new_business_key
                            OR ra.candidate_no IS DISTINCT FROM mapping.new_business_key
                          )
                        """
                    )
                    cur.execute(
                        """
                        UPDATE dtlms_recruitment_applications ra
                        SET business_key = mapping.new_business_key,
                            candidate_no = mapping.new_business_key,
                            updated_at = CURRENT_TIMESTAMP
                        FROM tmp_startup_recruitment_application_business_keys mapping
                        WHERE ra.id = mapping.application_id
                          AND ra.is_deleted = FALSE
                          AND (
                            ra.business_key IS DISTINCT FROM mapping.new_business_key
                            OR ra.candidate_no IS DISTINCT FROM mapping.new_business_key
                          )
                        """
                    )
                cur.execute(
                    """
                    UPDATE dtlms_wf_hi_procinst procinst
                    SET business_key_ = mapping.new_business_key
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND procinst.business_key_ = mapping.old_workflow_key
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_hi_taskinst taskinst
                    SET business_key_ = mapping.new_business_key
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND taskinst.business_key_ = mapping.old_workflow_key
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_hi_actinst actinst
                    SET business_key_ = mapping.new_business_key
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND actinst.business_key_ = mapping.old_workflow_key
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_ru_execution execution
                    SET business_key_ = mapping.new_business_key
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND execution.business_key_ = mapping.old_workflow_key
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_ru_task runtime_task
                    SET business_key_ = mapping.new_business_key,
                        form_key_ = CASE
                            WHEN runtime_task.form_key_ = mapping.old_workflow_key THEN mapping.new_business_key
                            ELSE runtime_task.form_key_
                        END,
                        description_ = CASE
                            WHEN COALESCE(runtime_task.description_, '') LIKE '业务编号：%'
                                THEN regexp_replace(runtime_task.description_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
                            ELSE runtime_task.description_
                        END
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND (
                          runtime_task.business_key_ = mapping.old_workflow_key
                          OR runtime_task.form_key_ = mapping.old_workflow_key
                      )
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_ru_variable runtime_variable
                    SET text_value_ = CASE
                            WHEN runtime_variable.name_ = 'businessKey' THEN mapping.new_business_key
                            WHEN runtime_variable.name_ = 'formSummary' AND COALESCE(runtime_variable.text_value_, '') LIKE '业务编号：%'
                                THEN regexp_replace(runtime_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
                            ELSE runtime_variable.text_value_
                        END,
                        json_value_ = CASE
                            WHEN runtime_variable.name_ = 'businessKey'
                                THEN jsonb_set(COALESCE(runtime_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
                            WHEN runtime_variable.name_ = 'formSummary'
                                THEN jsonb_set(
                                    COALESCE(runtime_variable.json_value_, '{}'::jsonb),
                                    '{value}',
                                    to_jsonb(
                                        regexp_replace(
                                            COALESCE(runtime_variable.json_value_ ->> 'value', ''),
                                            '^业务编号：[^；]*；',
                                            '业务编号：' || mapping.new_business_key || '；'
                                        )::TEXT
                                    ),
                                    TRUE
                                )
                            ELSE runtime_variable.json_value_
                        END
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND (
                          (runtime_variable.name_ = 'businessKey' AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
                          OR (
                              runtime_variable.name_ = 'formSummary'
                              AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
                          )
                      )
                    """
                )
                cur.execute(
                    """
                    UPDATE dtlms_wf_hi_varinst history_variable
                    SET text_value_ = CASE
                            WHEN history_variable.name_ = 'businessKey' THEN mapping.new_business_key
                            WHEN history_variable.name_ = 'formSummary' AND COALESCE(history_variable.text_value_, '') LIKE '业务编号：%'
                                THEN regexp_replace(history_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
                            ELSE history_variable.text_value_
                        END,
                        json_value_ = CASE
                            WHEN history_variable.name_ = 'businessKey'
                                THEN jsonb_set(COALESCE(history_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
                            WHEN history_variable.name_ = 'formSummary'
                                THEN jsonb_set(
                                    COALESCE(history_variable.json_value_, '{}'::jsonb),
                                    '{value}',
                                    to_jsonb(
                                        regexp_replace(
                                            COALESCE(history_variable.json_value_ ->> 'value', ''),
                                            '^业务编号：[^；]*；',
                                            '业务编号：' || mapping.new_business_key || '；'
                                        )::TEXT
                                    ),
                                    TRUE
                                )
                            ELSE history_variable.json_value_
                        END,
                        last_updated_time_ = CURRENT_TIMESTAMP
                    FROM tmp_startup_recruitment_application_business_keys mapping
                    WHERE mapping.old_workflow_key IS NOT NULL
                      AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
                      AND (
                          (history_variable.name_ = 'businessKey' AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
                          OR (
                              history_variable.name_ = 'formSummary'
                              AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
                          )
                      )
                    """
                )
            conn.commit()
        return changed_count

    def get_user_profile(self, username: str) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        username,
                        full_name,
                        role_name,
                        department_name,
                        introduction,
                        phone_number,
                        email,
                        theme_color
                    FROM dtlms_user_profiles
                    WHERE username = %s
                    """,
                    (str(username),),
                )
                row = cur.fetchone()
                return dict(row) if row else None

    def sync_user_profile(self, profile_payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO dtlms_user_profiles (
                        username, full_name, role_name, department_name, introduction, phone_number, email, theme_color
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE
                    SET full_name = EXCLUDED.full_name,
                        role_name = EXCLUDED.role_name,
                        department_name = EXCLUDED.department_name,
                        introduction = EXCLUDED.introduction,
                        phone_number = EXCLUDED.phone_number,
                        email = EXCLUDED.email,
                        theme_color = EXCLUDED.theme_color,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        str(profile_payload["username"]),
                        profile_payload.get("full_name"),
                        profile_payload.get("role_name") or "未分配角色",
                        profile_payload.get("department_name") or "",
                        profile_payload.get("introduction"),
                        profile_payload.get("phone_number"),
                        profile_payload.get("email"),
                        profile_payload.get("theme_color") or "#0f4cbd",
                    ),
                )
                cur.execute(
                    """
                    UPDATE dtlms_users
                    SET full_name = %s,
                        email = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                    """,
                    (
                        profile_payload.get("full_name"),
                        profile_payload.get("email"),
                        str(profile_payload["username"]),
                    ),
                )
            conn.commit()

    @staticmethod
    def _sync_runtime_counters_in_tx(cur: psycopg.Cursor[Any], counters: dict[str, int] | None) -> None:
        del cur, counters

    def _sync_operation_log_in_tx(self, cur: psycopg.Cursor[Any], operation_log: dict[str, Any] | None) -> None:
        if not operation_log:
            return
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

    def sync_operation_log(
        self,
        operation_log: dict[str, Any],
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def _sync_notification_delivery_log_in_tx(self, cur: psycopg.Cursor[Any], notification_log: dict[str, Any] | None) -> None:
        if not notification_log:
            return
        cur.execute(
            """
            INSERT INTO dtlms_notification_delivery_logs (
                id, channel, template_code, recipient, subject, send_status,
                failure_reason, business_key, triggered_by, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET channel = EXCLUDED.channel,
                template_code = EXCLUDED.template_code,
                recipient = EXCLUDED.recipient,
                subject = EXCLUDED.subject,
                send_status = EXCLUDED.send_status,
                failure_reason = EXCLUDED.failure_reason,
                business_key = EXCLUDED.business_key,
                triggered_by = EXCLUDED.triggered_by,
                updated_at = EXCLUDED.updated_at
            """,
            (
                int(notification_log["id"]),
                notification_log.get("channel"),
                notification_log.get("template_code"),
                notification_log.get("recipient"),
                notification_log.get("subject"),
                notification_log.get("send_status"),
                notification_log.get("failure_reason"),
                notification_log.get("business_key"),
                notification_log.get("triggered_by"),
                notification_log.get("sent_at"),
                notification_log.get("sent_at"),
            ),
        )

    def sync_notification_delivery_log(
        self,
        notification_log: dict[str, Any],
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_notification_delivery_log_in_tx(cur, notification_log)
            conn.commit()

    def _fetch_student_key_map(self, cur: psycopg.Cursor[Any]) -> dict[str, int]:
        cur.execute("SELECT id, student_no AS key FROM dtlms_students WHERE is_deleted = FALSE")
        return self._fetch_map(cur, "SELECT id, student_no AS key FROM dtlms_students WHERE is_deleted = FALSE")

    def _fetch_advisor_key_map(self, cur: psycopg.Cursor[Any]) -> dict[str, int]:
        return self._fetch_map(cur, "SELECT id, full_name AS key FROM dtlms_advisors WHERE is_deleted = FALSE")

    def _fetch_role_key_map(self, cur: psycopg.Cursor[Any]) -> dict[str, int]:
        return self._fetch_map(cur, "SELECT id, role_code AS key FROM dtlms_roles WHERE is_deleted = FALSE")

    def _fetch_permission_key_map(self, cur: psycopg.Cursor[Any]) -> dict[str, int]:
        return self._fetch_map(cur, "SELECT id, permission_code AS key FROM dtlms_permissions WHERE is_deleted = FALSE")

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
            "workflowName": str(task.get("workflow_name") or "未命名流程"),
            "businessModule": str(task.get("business_module") or "流程中心"),
            "applicantName": str(task.get("applicant_name") or "未知申请人"),
            "currentHandler": str(task.get("current_handler") or "待分派"),
            "flowCode": str(task.get("flow_code") or ""),
            "entityId": int(task.get("entity_id") or 0),
            "currentNode": str(task.get("current_node") or ""),
            "nodeKey": str(task.get("node_key") or task.get("task_definition_key") or ""),
            "taskStatus": str(task.get("status") or ""),
            "formSummary": str(task.get("form_summary") or ""),
            "latestComment": str(task.get("latest_comment") or ""),
            "candidateGroups": [str(item) for item in task.get("candidate_groups") or []],
            "historyEntries": list(task.get("history") or []),
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
        self._execute_dynamic(cur, query)
        rows = cur.fetchall()
        if not rows:
            return {}
        first_row = rows[0]
        if isinstance(first_row, dict):
            return {str(row["key"]): row["id"] for row in rows}
        return {str(row[1]): row[0] for row in rows}

    def _ensure_advisors_exist(self, cur: psycopg.Cursor[Any], advisor_names: list[str] | tuple[str, ...] | set[str] | None) -> dict[str, int]:
        normalized_names = self._normalize_name_list(advisor_names)
        advisor_map = self._fetch_map(cur, "SELECT id, full_name AS key FROM dtlms_advisors WHERE is_deleted = FALSE")
        missing_names = [name for name in normalized_names if name not in advisor_map]
        for advisor_name in missing_names:
            cur.execute(
                """
                WITH allocated AS (
                    SELECT nextval(pg_get_serial_sequence('dtlms_advisors', 'id')) AS advisor_id
                )
                INSERT INTO dtlms_advisors (
                    id, advisor_no, full_name, title, organization_name, research_direction, annual_quota, is_deleted
                )
                SELECT
                    advisor_id,
                    CONCAT('ADV', LPAD(advisor_id::TEXT, 3, '0')),
                    %s,
                    '导师',
                    '未分配单位',
                    '待补充',
                    0,
                    FALSE
                FROM allocated
                """,
                (advisor_name,),
            )
        if missing_names:
            advisor_map = self._fetch_map(cur, "SELECT id, full_name AS key FROM dtlms_advisors WHERE is_deleted = FALSE")
        return advisor_map

    def _ensure_advisors_for_user_ids(
        self,
        cur: psycopg.Cursor[Any],
        advisor_user_ids: list[int] | tuple[int, ...] | set[int] | None,
    ) -> dict[int, int]:
        normalized_user_ids = sorted({int(item) for item in (advisor_user_ids or []) if int(item or 0) > 0})
        if not normalized_user_ids:
            return {}

        cur.execute(
            """
            SELECT
                u.id AS user_id,
                u.full_name,
                COALESCE(a.id, 0) AS advisor_id
            FROM dtlms_users u
            LEFT JOIN dtlms_advisors a ON a.user_id = u.id AND a.is_deleted = FALSE
            WHERE u.id = ANY(%s)
            """,
            (normalized_user_ids,),
        )
        rows = [dict(row) if isinstance(row, dict) else {"user_id": row[0], "full_name": row[1], "advisor_id": row[2]} for row in cur.fetchall()]

        for row in rows:
            if int(row.get("advisor_id") or 0) > 0:
                continue
            user_id = int(row["user_id"])
            full_name = str(row.get("full_name") or "").strip()
            cur.execute(
                """
                WITH allocated AS (
                    SELECT nextval(pg_get_serial_sequence('dtlms_advisors', 'id')) AS advisor_id
                )
                INSERT INTO dtlms_advisors (
                    id, advisor_no, full_name, title, organization_name, research_direction, annual_quota, user_id, is_deleted
                )
                SELECT
                    advisor_id,
                    CONCAT('ADV', LPAD(advisor_id::TEXT, 3, '0')),
                    %s,
                    '导师',
                    COALESCE(NULLIF(u.department_name, ''), '未分配单位'),
                    '待补充',
                    0,
                    u.id,
                    FALSE
                FROM allocated
                JOIN dtlms_users u ON u.id = %s
                ON CONFLICT (user_id) DO UPDATE
                SET full_name = EXCLUDED.full_name,
                    organization_name = EXCLUDED.organization_name,
                    is_deleted = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (full_name, user_id),
            )

        cur.execute(
            """
            SELECT user_id, id AS advisor_id
            FROM dtlms_advisors
            WHERE is_deleted = FALSE
              AND user_id = ANY(%s)
            """,
            (normalized_user_ids,),
        )
        return {int(row[0]): int(row[1]) for row in cur.fetchall()}

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
        profile: dict[str, Any] = cast(dict[str, Any], student.get("profile")) if isinstance(student.get("profile"), dict) else {}
        for key in (
            "full_name_pinyin",
            "profile_photo_url",
            "id_card_collage_url",
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
        draft: dict[str, Any] = cast(dict[str, Any], student.get("application_draft")) if isinstance(student.get("application_draft"), dict) else {}
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
        personal_statement: dict[str, Any] = cast(dict[str, Any], draft.get("personal_statement")) if isinstance(draft.get("personal_statement"), dict) else {}
        if student.get("personal_statement_text") and not personal_statement.get("personal_statement_text"):
            personal_statement["personal_statement_text"] = student.get("personal_statement_text")
        declaration: dict[str, Any] = cast(dict[str, Any], draft.get("declaration")) if isinstance(draft.get("declaration"), dict) else {}
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

    @classmethod
    def _merge_portal_application_draft(cls, base_draft: dict[str, Any] | None, overlay_draft: dict[str, Any] | None) -> dict[str, Any] | None:
        merged: dict[str, Any] = dict(base_draft or {})
        if isinstance(overlay_draft, dict):
            for key, value in overlay_draft.items():
                merged[key] = value

        has_content = any(value not in (None, "", [], {}) for key, value in merged.items() if key != "selected_plan_id") or merged.get("selected_plan_id") is not None
        return merged if has_content else None

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
            "advisor_id": int(row.get("advisor_id") or 0) or None,
            "center_name": str(row.get("team_name") or ""),
            "degree_type": str(row.get("degree_type") or ""),
            "enrollment_year": int(row.get("enrollment_year") or 0),
            "phone_number": row.get("phone_number"),
            "political_status": row.get("political_status"),
        }

    @classmethod
    def _normalize_recruitment_plan_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        academic_year = str(row.get("academic_year") or "")
        semester = str(row.get("semester") or "")
        return {
            "id": int(row["id"]),
            "plan_name": str(row.get("plan_name") or ""),
            "academic_term": f"{academic_year} {semester}".strip(),
            "academic_year": academic_year,
            "semester": semester,
            "application_count": int(row.get("application_count") or 0),
            "brochure_image_url": row.get("brochure_image_url"),
            "plan_description": row.get("plan_description"),
        }

    @classmethod
    def _normalize_training_plan_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "student_no": str(row.get("student_no") or ""),
            "student_name": str(row.get("student_name") or ""),
            "advisor_name": str(row.get("advisor_name") or ""),
            "version_no": str(row.get("version_no") or ""),
            "report_cycle": str(row.get("report_cycle") or ""),
            "plan_status": cls._training_plan_status_label(row.get("plan_status")),
            "scientific_goal": str(row.get("scientific_goal") or ""),
            "assessment_rule": str(row.get("assessment_rule") or ""),
        }

    @classmethod
    def _normalize_scientific_report_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "business_key": str(row.get("business_key") or ""),
            "student_no": str(row.get("student_no") or ""),
            "student_name": str(row.get("student_name") or ""),
            "period_label": str(row.get("period_label") or ""),
            "report_status": cls._report_status_label(row.get("report_status")),
            "reviewer_name": row.get("reviewer_name"),
            "review_score": float(row["review_score"]) if row.get("review_score") is not None else None,
            "summary": str(row.get("summary") or ""),
        }

    @classmethod
    def _normalize_outbound_study_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "business_key": str(row.get("business_key") or ""),
            "student_no": str(row.get("student_no") or ""),
            "student_name": str(row.get("student_name") or ""),
            "advisor_name": str(row.get("advisor_name") or ""),
            "study_type": str(row.get("study_type") or ""),
            "destination": str(row.get("destination") or ""),
            "start_date": cls._stringify_datetime(row.get("start_date")) or "",
            "end_date": cls._stringify_datetime(row.get("end_date")) or "",
            "approval_status": cls._outbound_status_label(row.get("approval_status")),
            "expected_outcome": row.get("expected_outcome"),
        }

    @classmethod
    def _normalize_thesis_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "business_key": str(row.get("business_key") or ""),
            "student_no": str(row.get("student_no") or ""),
            "student_name": str(row.get("student_name") or ""),
            "advisor_name": str(row.get("advisor_name") or ""),
            "title": str(row.get("title") or ""),
            "plagiarism_rate": float(row["plagiarism_rate"]) if row.get("plagiarism_rate") is not None else None,
            "thesis_status": cls._thesis_status_label(row.get("thesis_status")),
            "blind_review_status": cls._blind_review_status_label(row.get("blind_review_status")),
            "defense_status": cls._defense_status_label(row.get("defense_date")),
            "degree_status": cls._degree_status_label(row.get("degree_granted"), row.get("defense_date")),
        }

    @classmethod
    def _normalize_thesis_review_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "thesis_id": int(row.get("thesis_id") or 0),
            "thesis_title": str(row.get("thesis_title") or ""),
            "expert_name": str(row.get("expert_name") or ""),
            "review_score": float(row["review_score"]) if row.get("review_score") is not None else None,
            "review_status": cls._thesis_review_status_label(row.get("review_status")),
            "review_comment": row.get("review_comment"),
        }

    @classmethod
    def _normalize_registered_portal_student_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        recruitment_application_status = cls._application_status_label(row.get("application_status")) if row.get("application_status") else None
        submitted_at = None if recruitment_application_status == "驳回重填" else cls._stringify_datetime(row.get("submitted_at") or row.get("applied_at"))
        return {
            "id": int(row["id"]),
            "full_name": str(row.get("full_name") or ""),
            "phone_number": str(row.get("phone_number") or ""),
            "email": str(row.get("email") or ""),
            "id_number": str(row.get("id_number") or ""),
            "account_status": cls._normalize_portal_account_status(row.get("account_status")),
            "application_form_status": "驳回重填" if recruitment_application_status == "驳回重填" else ("已填写报名" if submitted_at else "未填写报名"),
            "selected_plan_name": row.get("selected_plan_name"),
            "selected_center_name": row.get("selected_team_name"),
            "selected_advisor_name": row.get("selected_advisor_name"),
            "recruitment_application_id": int(row.get("recruitment_application_id") or 0) or None,
            "recruitment_application_business_key": (str(row.get("recruitment_application_business_key") or "") or None),
            "recruitment_application_status": recruitment_application_status,
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
        new_value: dict[str, Any] = cast(dict[str, Any], row.get("new_value")) if isinstance(row.get("new_value"), dict) else {}
        return {
            "id": int(row["id"]),
            "operated_at": PostgresStateStoreCoreMixin._stringify_datetime(row.get("created_at")) or "",
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
            "portal_student_id": int(row.get("portal_student_id") or 0) or None,
            "candidate_no": row.get("candidate_no"),
            "review_round": row.get("review_round"),
            "student_name": str(row.get("student_name") or ""),
            "first_choice_team_id": int(row.get("first_choice_team_id") or 0) or None,
            "first_choice": row.get("first_choice"),
            "second_choice_team_id": int(row.get("second_choice_team_id") or 0) or None,
            "second_choice": row.get("second_choice"),
            "full_name_pinyin": row.get("full_name_pinyin"),
            "profile_photo_url": row.get("profile_photo_url"),
            "id_card_collage_url": row.get("id_card_collage_url"),
            "gender": row.get("gender"),
            "birth_date": row.get("birth_date"),
            "ethnic_group": row.get("ethnic_group"),
            "political_status": row.get("political_status"),
            "marital_status": row.get("marital_status"),
            "religious_belief": row.get("religious_belief"),
            "native_place": row.get("native_place"),
            "phone_number": row.get("phone_number"),
            "email": row.get("email"),
            "mailing_address": row.get("mailing_address"),
            "emergency_contact_name": row.get("emergency_contact_name"),
            "emergency_contact_phone": row.get("emergency_contact_phone"),
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
            "intended_advisor_user_id": int(row.get("intended_advisor_user_id") or 0) or None,
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

    @staticmethod
    def _normalize_academic_year_start(value: Any) -> str:
        text = str(value or "").strip()
        if not text:
            return "2026"
        first_segment = text.split("-")[0].strip()
        if first_segment.isdigit() and len(first_segment) == 4:
            return first_segment
        digits = "".join(character for character in text if character.isdigit())
        if len(digits) >= 4:
            return digits[:4]
        return "2026"

    @classmethod
    def _normalize_center_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "center_name": str(row.get("team_name") or ""),
            "director_name": str(row.get("director_name") or ""),
            "director_id": int(row.get("director_id") or 0) or None,
            "advisor_names": cls._split_delimited_values(row.get("advisor_names")),
            "advisor_ids": [int(item) for item in (row.get("advisor_ids") or []) if item is not None],
            "advisor_relation_ids": [int(item) for item in (row.get("advisor_relation_ids") or []) if item is not None],
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
    def _normalize_notification_delivery_log_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "channel": str(row.get("channel") or ""),
            "template_code": row.get("template_code"),
            "recipient": str(row.get("recipient") or ""),
            "subject": str(row.get("subject") or ""),
            "send_status": str(row.get("send_status") or ""),
            "sent_at": cls._stringify_datetime(row.get("created_at")) or "",
            "business_key": row.get("business_key"),
            "triggered_by": row.get("triggered_by"),
            "failure_reason": row.get("failure_reason"),
        }

    @staticmethod
    def _normalize_role_row(row: dict[str, Any]) -> dict[str, Any]:
        permissions = row.get("permissions") or []
        return {
            "id": int(row.get("id") or 0),
            "role_code": str(row.get("role_code") or ""),
            "role_name": str(row.get("role_name") or ""),
            "scope_name": str(row.get("scope_name") or "系统管理"),
            "permissions": [str(item) for item in permissions if str(item).strip()],
            "user_count": int(row.get("user_count") or 0),
        }

    @staticmethod
    def _normalize_audit_policy_row(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row.get("id") or 0),
            "item": str(row.get("item") or ""),
            "policy": str(row.get("policy") or ""),
            "status": str(row.get("status") or ""),
        }

    @staticmethod
    def _normalize_integration_row(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row.get("id") or 0),
            "name": str(row.get("name") or ""),
            "direction": str(row.get("direction") or ""),
            "cadence": str(row.get("cadence") or ""),
            "status": str(row.get("status") or ""),
            "owner": str(row.get("owner") or ""),
        }

    @classmethod
    def _normalize_workflow_task_snapshot_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        task_key = str(row.get("task_key") or "")
        task_id = int(task_key.replace("TASK-", "") or 0)
        flow_code = str(row.get("flow_code") or "").strip() or None
        candidate_groups = row.get("candidate_groups")
        if isinstance(candidate_groups, dict) and "value" in candidate_groups:
            candidate_groups = candidate_groups["value"]
        history_entries = row.get("history_entries")
        if isinstance(history_entries, dict) and "value" in history_entries:
            history_entries = history_entries["value"]
        return {
            "id": task_id,
            "workflow_name": str(row.get("workflow_name") or row.get("process_definition_name") or "未命名流程"),
            "business_module": str(row.get("business_module") or "流程中心"),
            "business_key": str(row.get("business_key_") or ""),
            "title": str(row.get("title") or "未命名任务"),
            "applicant_name": str(row.get("applicant_name") or "未知申请人"),
            "current_handler": str(row.get("current_handler") or "待分派"),
            "current_node": str(row.get("current_node") or "待处理"),
            "priority": cls._workflow_priority_label(row.get("priority_")),
            "status": str(row.get("task_status") or "待处理"),
            "created_at": cls._stringify_datetime(row.get("start_time_")) or "",
            "due_at": cls._stringify_datetime(row.get("due_date_")) or cls._stringify_datetime(row.get("start_time_")) or "",
            "form_summary": str(row.get("form_summary") or ""),
            "latest_comment": row.get("latest_comment"),
            "process_definition_key": row.get("process_definition_key"),
            "process_definition_id": row.get("proc_def_id_"),
            "process_instance_id": row.get("proc_inst_id_"),
            "execution_id": row.get("exec_id_"),
            "task_definition_key": row.get("task_def_key_"),
            "flow_code": flow_code,
            "business_dataset": WORKFLOW_FLOW_DATASET_MAP.get(flow_code),
            "node_key": row.get("node_key") or row.get("task_def_key_"),
            "entity_id": int(row.get("entity_id") or 0),
            "candidate_groups": [str(item) for item in (candidate_groups or []) if str(item).strip()],
            "history": cls._parse_json_list(history_entries),
        }

    @staticmethod
    def _workflow_priority_label(value: Any) -> str:
        mapping = {25: "低", 50: "中", 75: "高", 100: "紧急"}
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            return str(value or "中") or "中"
        return mapping.get(numeric, "中")

    @classmethod
    def _normalize_system_user_row(cls, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": int(row.get("id") or 0),
            "username": str(row.get("username") or ""),
            "full_name": str(row.get("full_name") or ""),
            "role_code": str(row.get("role_code") or ""),
            "role_name": str(row.get("role_name") or row.get("role_code") or ""),
            "department_name": str(row.get("department_name") or ""),
            "introduction": row.get("introduction"),
            "email": row.get("email"),
            "phone_number": row.get("phone_number"),
            "account_status": str(row.get("account_status") or ""),
            "last_login_at": cls._stringify_datetime(row.get("last_login_at")),
        }

    @staticmethod
    def _stringify_datetime(value: Any) -> str | None:
        if value is None:
            return None
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        text = str(value).strip()
        if not text:
            return None
        normalized = text.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            return text
        return parsed.strftime("%Y-%m-%d %H:%M:%S")

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
    def _training_plan_status_label(value: str | None) -> str:
        mapping = {
            "draft": "草稿",
            "pending_confirm": "待学生确认",
            "effective": "执行中",
            "archived": "已归档",
        }
        return mapping.get(str(value or ""), "草稿")

    @staticmethod
    def _map_report_status(value: str) -> str:
        mapping = {
            "待导师审阅": "reviewing",
            "已通过": "reviewed",
            "退回修改": "rework",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _report_status_label(value: str | None) -> str:
        mapping = {
            "submitted": "待提交",
            "reviewing": "待导师审阅",
            "reviewed": "已通过",
            "rework": "退回修改",
        }
        return mapping.get(str(value or ""), "待提交")

    @staticmethod
    def _map_outbound_status(value: str) -> str:
        mapping = {
            "审批中": "submitted",
            "研修中": "approved",
            "已完成": "completed",
        }
        return mapping.get(value, "submitted")

    @staticmethod
    def _outbound_status_label(value: str | None) -> str:
        mapping = {
            "submitted": "审批中",
            "approved": "研修中",
            "completed": "已完成",
        }
        return mapping.get(str(value or ""), "审批中")

    @staticmethod
    def _thesis_status_label(value: str | None) -> str:
        mapping = {
            "plagiarism_passed": "查重通过",
            "review_passed": "盲审通过",
            "rework": "退回修改",
            "draft": "待查重",
        }
        return mapping.get(str(value or ""), "待查重")

    @staticmethod
    def _blind_review_status_label(value: str | None) -> str:
        mapping = {
            "pending": "未送审",
            "reviewing": "进行中",
            "passed": "已通过",
        }
        return mapping.get(str(value or ""), "未送审")

    @staticmethod
    def _defense_status_label(defense_date: Any) -> str:
        return "待安排" if defense_date is None else "已安排"

    @staticmethod
    def _degree_status_label(value: str | None, defense_date: Any) -> str:
        if str(value or "") == "reviewing":
            return "授位审批中"
        if str(value or "") == "granted":
            return "已授位"
        if defense_date is not None:
            return "待正式答辩"
        return "待申请"

    @staticmethod
    def _thesis_review_status_label(value: str | None) -> str:
        mapping = {
            "approved": "通过",
            "rejected": "不通过",
            "pending": "待审阅",
        }
        return mapping.get(str(value or ""), "待审阅")

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
            "驳回重填": "returned",
            "不录取": "rejected",
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
            "returned": "驳回重填",
            "rejected": "不录取",
            "qualified": "资格审核通过",
            "scoring": "材料评分中",
            "interviewed": "面试完成",
            "pre_admitted": "预录取",
            "admitted": "同意录取",
        }
        return mapping.get(str(value or ""), "报名已提交")

    @classmethod
    def _portal_resubmittable_application_status(cls, value: str | None) -> bool:
        status = str(value or "").strip()
        if not status:
            return False
        return status in {"returned", "rejected", "驳回重填", "不录取"} or cls._application_status_label(status) in {"驳回重填", "不录取"}

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
