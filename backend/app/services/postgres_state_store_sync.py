from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)


class PostgresStateStoreSyncMixin:
    def update_runtime_system_user(self, user_id: int, payload: dict[str, Any]) -> None:
        del user_id
        self.sync_system_user(payload, None, None)

    def delete_runtime_system_user(self, user_id: int) -> None:
        self.delete_system_user(user_id)

    def update_runtime_profile(self, username: str, payload: dict[str, Any]) -> None:
        del username
        self.sync_user_profile(payload)

    def delete_runtime_profile(self, username: str) -> None:
        self.delete_user_profile(username)

    def sync_role(
        self,
        role_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute(
                    """
                    INSERT INTO dtlms_roles (id, role_code, role_name, scope_name, description, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET role_code = EXCLUDED.role_code,
                        role_name = EXCLUDED.role_name,
                        scope_name = EXCLUDED.scope_name,
                        description = EXCLUDED.description,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(role_payload["id"]),
                        role_payload.get("role_code"),
                        role_payload.get("role_name"),
                        role_payload.get("scope_name") or "系统管理",
                        role_payload.get("description"),
                    ),
                )
                permission_map = self._fetch_permission_key_map(cur)
                cur.execute("DELETE FROM dtlms_role_permissions WHERE role_id = %s", (int(role_payload["id"]),))
                for permission_code in role_payload.get("permissions", []):
                    permission_id = permission_map.get(str(permission_code))
                    if not permission_id:
                        continue
                    cur.execute(
                        """
                        INSERT INTO dtlms_role_permissions (role_id, permission_id)
                        VALUES (%s, %s)
                        ON CONFLICT (role_id, permission_id) DO NOTHING
                        """,
                        (int(role_payload["id"]), int(permission_id)),
                    )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_role(self, role_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_roles SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(role_id),))
                cur.execute("DELETE FROM dtlms_role_permissions WHERE role_id = %s", (int(role_id),))
            conn.commit()

    def sync_system_user(
        self,
        user_payload: dict[str, Any],
        profile_payload: dict[str, Any] | None = None,
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute(
                    """
                    INSERT INTO dtlms_users (
                        id, username, full_name, email, department_name, phone_number,
                        password_hash, is_active, is_deleted, last_login_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET username = EXCLUDED.username,
                        full_name = EXCLUDED.full_name,
                        email = EXCLUDED.email,
                        department_name = EXCLUDED.department_name,
                        phone_number = EXCLUDED.phone_number,
                        password_hash = EXCLUDED.password_hash,
                        is_active = EXCLUDED.is_active,
                        is_deleted = FALSE,
                        last_login_at = EXCLUDED.last_login_at,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(user_payload["id"]),
                        user_payload.get("username"),
                        user_payload.get("full_name"),
                        (profile_payload or {}).get("email"),
                        user_payload.get("department_name") or "",
                        user_payload.get("phone_number"),
                        user_payload.get("password_hash"),
                        str(user_payload.get("account_status") or "启用") == "启用",
                        user_payload.get("last_login_at"),
                    ),
                )
                role_map = self._fetch_role_key_map(cur)
                cur.execute("DELETE FROM dtlms_user_roles WHERE user_id = %s", (int(user_payload["id"]),))
                role_id = role_map.get(str(user_payload.get("role_code") or ""))
                if role_id:
                    cur.execute(
                        """
                        INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id, role_id) DO UPDATE
                        SET grant_source = EXCLUDED.grant_source,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (int(user_payload["id"]), int(role_id), "runtime_sync"),
                    )
                if profile_payload is not None:
                    cur.execute(
                        """
                        INSERT INTO dtlms_user_profiles (
                            username, full_name, role_name, department_name, phone_number, email, theme_color
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (username) DO UPDATE
                        SET full_name = EXCLUDED.full_name,
                            role_name = EXCLUDED.role_name,
                            department_name = EXCLUDED.department_name,
                            phone_number = EXCLUDED.phone_number,
                            email = EXCLUDED.email,
                            theme_color = EXCLUDED.theme_color,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (
                            str(profile_payload["username"]),
                            profile_payload.get("full_name") or user_payload.get("full_name"),
                            profile_payload.get("role_name") or user_payload.get("role_code") or "未分配角色",
                            profile_payload.get("department_name") or user_payload.get("department_name") or "",
                            profile_payload.get("phone_number") or user_payload.get("phone_number"),
                            profile_payload.get("email"),
                            profile_payload.get("theme_color") or "#0f4cbd",
                        ),
                    )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_system_user(self, user_id: int, username: str | None = None) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if username is None:
                    cur.execute("SELECT username FROM dtlms_users WHERE id = %s", (int(user_id),))
                    row = cur.fetchone()
                    username = str(row[0]) if row else None
                cur.execute(
                    "UPDATE dtlms_users SET is_deleted = TRUE, is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (int(user_id),),
                )
                cur.execute("DELETE FROM dtlms_user_roles WHERE user_id = %s", (int(user_id),))
                if username:
                    cur.execute("DELETE FROM dtlms_user_profiles WHERE username = %s", (str(username),))
            conn.commit()

    def delete_user_profile(self, username: str) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM dtlms_user_profiles WHERE username = %s", (str(username),))
            conn.commit()

    def sync_audit_policy(
        self,
        policy_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute(
                    """
                    INSERT INTO dtlms_audit_policies (id, item, policy, status, is_deleted)
                    VALUES (%s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET item = EXCLUDED.item,
                        policy = EXCLUDED.policy,
                        status = EXCLUDED.status,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(policy_payload["id"]),
                        policy_payload.get("item"),
                        policy_payload.get("policy"),
                        policy_payload.get("status") or "启用",
                    ),
                )
                cur.execute(
                    """
                    INSERT INTO dtlms_system_configs (config_key, config_value, description)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (config_key) DO UPDATE
                    SET config_value = EXCLUDED.config_value,
                        description = EXCLUDED.description,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (f"audit.policy.{int(policy_payload['id'])}", policy_payload.get("policy") or "", policy_payload.get("item") or ""),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_audit_policy(self, policy_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_audit_policies SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(policy_id),))
                cur.execute("DELETE FROM dtlms_system_configs WHERE config_key = %s", (f"audit.policy.{int(policy_id)}",))
            conn.commit()

    def sync_integration(
        self,
        integration_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute(
                    """
                    INSERT INTO dtlms_integrations (id, name, direction, cadence, status, owner, is_deleted)
                    VALUES (%s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET name = EXCLUDED.name,
                        direction = EXCLUDED.direction,
                        cadence = EXCLUDED.cadence,
                        status = EXCLUDED.status,
                        owner = EXCLUDED.owner,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(integration_payload["id"]),
                        integration_payload.get("name"),
                        integration_payload.get("direction"),
                        integration_payload.get("cadence"),
                        integration_payload.get("status") or "正常",
                        integration_payload.get("owner") or "",
                    ),
                )
                cur.execute(
                    """
                    INSERT INTO dtlms_system_configs (config_key, config_value, description)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (config_key) DO UPDATE
                    SET config_value = EXCLUDED.config_value,
                        description = EXCLUDED.description,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        f"integration.{int(integration_payload['id'])}.{integration_payload.get('name')}",
                        f"{integration_payload.get('direction')}|{integration_payload.get('cadence')}|{integration_payload.get('status')}|{integration_payload.get('owner')}",
                        "外部集成概览",
                    ),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_integration(self, integration_id: int, integration_name: str | None = None) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                if integration_name is None:
                    cur.execute("SELECT name FROM dtlms_integrations WHERE id = %s", (int(integration_id),))
                    row = cur.fetchone()
                    integration_name = str(row[0]) if row else None
                cur.execute("UPDATE dtlms_integrations SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(integration_id),))
                if integration_name:
                    cur.execute("DELETE FROM dtlms_system_configs WHERE config_key = %s", (f"integration.{int(integration_id)}.{integration_name}",))
            conn.commit()

    def sync_training_plan(
        self,
        plan_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                student_map = self._fetch_student_key_map(cur)
                advisor_map = self._fetch_advisor_key_map(cur)
                student_id = student_map[str(plan_payload.get("student_no") or "")]
                advisor_id = advisor_map[str(plan_payload.get("advisor_name") or "")]
                cur.execute(
                    """
                    INSERT INTO dtlms_training_plans (
                        id, student_id, advisor_id, version_no, report_cycle, plan_status,
                        scientific_goal, assessment_rule, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET student_id = EXCLUDED.student_id,
                        advisor_id = EXCLUDED.advisor_id,
                        version_no = EXCLUDED.version_no,
                        report_cycle = EXCLUDED.report_cycle,
                        plan_status = EXCLUDED.plan_status,
                        scientific_goal = EXCLUDED.scientific_goal,
                        assessment_rule = EXCLUDED.assessment_rule,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(plan_payload["id"]),
                        int(student_id),
                        int(advisor_id),
                        plan_payload.get("version_no") or "v1.0",
                        plan_payload.get("report_cycle") or "每学期",
                        self._map_training_plan_status(str(plan_payload.get("plan_status") or "待学生确认")),
                        plan_payload.get("scientific_goal") or "",
                        plan_payload.get("assessment_rule") or "",
                    ),
                )
                cur.execute(
                    "SELECT id FROM dtlms_training_plan_versions WHERE training_plan_id = %s AND version_no = %s ORDER BY id DESC LIMIT 1",
                    (int(plan_payload["id"]), plan_payload.get("version_no") or "v1.0"),
                )
                version_row = cur.fetchone()
                if version_row:
                    cur.execute(
                        "UPDATE dtlms_training_plan_versions SET plan_snapshot = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                        (plan_payload.get("scientific_goal") or "", int(version_row[0])),
                    )
                else:
                    cur.execute(
                        "INSERT INTO dtlms_training_plan_versions (training_plan_id, version_no, change_reason, plan_snapshot) VALUES (%s, %s, %s, %s)",
                        (int(plan_payload["id"]), plan_payload.get("version_no") or "v1.0", "在线维护", plan_payload.get("scientific_goal") or ""),
                    )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_training_plan(self, plan_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_training_plans SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(plan_id),))
            conn.commit()

    def sync_scientific_report(
        self,
        report_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                student_map = self._fetch_student_key_map(cur)
                advisor_map = self._fetch_advisor_key_map(cur)
                student_id = student_map[str(report_payload.get("student_no") or "")]
                cur.execute(
                    "SELECT id FROM dtlms_training_plans WHERE student_id = %s AND is_deleted = FALSE ORDER BY updated_at DESC, id DESC LIMIT 1",
                    (int(student_id),),
                )
                plan_row = cur.fetchone()
                if not plan_row:
                    raise ValueError("科研报告关联的培养方案不存在")
                reviewer_id = advisor_map.get(str(report_payload.get("reviewer_name") or "")) if report_payload.get("reviewer_name") else None
                cur.execute(
                    """
                    INSERT INTO dtlms_scientific_reports (
                        id, business_key, student_id, training_plan_id, period_label, report_status,
                        summary, attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET business_key = EXCLUDED.business_key,
                        student_id = EXCLUDED.student_id,
                        training_plan_id = EXCLUDED.training_plan_id,
                        period_label = EXCLUDED.period_label,
                        report_status = EXCLUDED.report_status,
                        summary = EXCLUDED.summary,
                        attachment_url = EXCLUDED.attachment_url,
                        reviewer_advisor_id = EXCLUDED.reviewer_advisor_id,
                        review_score = EXCLUDED.review_score,
                        review_comment = EXCLUDED.review_comment,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(report_payload["id"]),
                        report_payload.get("business_key"),
                        int(student_id),
                        int(plan_row[0]),
                        report_payload.get("period_label") or "",
                        self._map_report_status(str(report_payload.get("report_status") or "待导师审阅")),
                        report_payload.get("summary") or "",
                        f"/reports/{report_payload.get('student_no')}/{report_payload.get('period_label')}.pdf",
                        int(reviewer_id) if reviewer_id else None,
                        report_payload.get("review_score"),
                        report_payload.get("review_comment") or report_payload.get("latest_comment"),
                    ),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_scientific_report(self, report_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_scientific_reports SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(report_id),))
            conn.commit()

    def sync_outbound_study(
        self,
        study_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                student_map = self._fetch_student_key_map(cur)
                advisor_map = self._fetch_advisor_key_map(cur)
                cur.execute(
                    """
                    INSERT INTO dtlms_outbound_studies (
                        id, business_key, student_id, advisor_id, study_type, destination,
                        start_date, end_date, approval_status, expected_outcome, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET business_key = EXCLUDED.business_key,
                        student_id = EXCLUDED.student_id,
                        advisor_id = EXCLUDED.advisor_id,
                        study_type = EXCLUDED.study_type,
                        destination = EXCLUDED.destination,
                        start_date = EXCLUDED.start_date,
                        end_date = EXCLUDED.end_date,
                        approval_status = EXCLUDED.approval_status,
                        expected_outcome = EXCLUDED.expected_outcome,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(study_payload["id"]),
                        study_payload.get("business_key"),
                        int(student_map[str(study_payload.get("student_no") or "")]),
                        int(advisor_map[str(study_payload.get("advisor_name") or "")]),
                        study_payload.get("study_type") or "",
                        study_payload.get("destination") or "",
                        study_payload.get("start_date"),
                        study_payload.get("end_date"),
                        self._map_outbound_status(str(study_payload.get("approval_status") or "审批中")),
                        study_payload.get("expected_outcome"),
                    ),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_outbound_study(self, study_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_outbound_studies SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(study_id),))
            conn.commit()

    def sync_thesis(
        self,
        thesis_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                student_map = self._fetch_student_key_map(cur)
                advisor_map = self._fetch_advisor_key_map(cur)
                cur.execute(
                    """
                    INSERT INTO dtlms_theses (
                        id, business_key, student_id, advisor_id, title, plagiarism_rate,
                        thesis_status, blind_review_status, defense_date, degree_granted, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET business_key = EXCLUDED.business_key,
                        student_id = EXCLUDED.student_id,
                        advisor_id = EXCLUDED.advisor_id,
                        title = EXCLUDED.title,
                        plagiarism_rate = EXCLUDED.plagiarism_rate,
                        thesis_status = EXCLUDED.thesis_status,
                        blind_review_status = EXCLUDED.blind_review_status,
                        defense_date = EXCLUDED.defense_date,
                        degree_granted = EXCLUDED.degree_granted,
                        is_deleted = FALSE,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(thesis_payload["id"]),
                        thesis_payload.get("business_key"),
                        int(student_map[str(thesis_payload.get("student_no") or "")]),
                        int(advisor_map[str(thesis_payload.get("advisor_name") or "")]),
                        thesis_payload.get("title") or "",
                        thesis_payload.get("plagiarism_rate"),
                        self._map_thesis_status(str(thesis_payload.get("thesis_status") or "待查重")),
                        self._map_blind_review_status(str(thesis_payload.get("blind_review_status") or "未送审")),
                        self._map_defense_date(str(thesis_payload.get("defense_status") or "未进入")),
                        self._map_degree_status(str(thesis_payload.get("degree_status") or "待申请")),
                    ),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_thesis(self, thesis_id: int) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE dtlms_theses SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(thesis_id),))
            conn.commit()

    def sync_thesis_review(
        self,
        review_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute(
                    """
                    INSERT INTO dtlms_thesis_reviews (
                        id, thesis_id, expert_name, review_score, review_status, review_comment
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET thesis_id = EXCLUDED.thesis_id,
                        expert_name = EXCLUDED.expert_name,
                        review_score = EXCLUDED.review_score,
                        review_status = EXCLUDED.review_status,
                        review_comment = EXCLUDED.review_comment,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        int(review_payload["id"]),
                        int(review_payload.get("thesis_id") or 0),
                        review_payload.get("expert_name") or "",
                        review_payload.get("review_score"),
                        self._map_review_progress(str(review_payload.get("review_status") or "待提交")),
                        review_payload.get("review_comment"),
                    ),
                )
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def _delete_workflow_engine_task_in_tx(self, cur: psycopg.Cursor[Any], task_id: int, process_instance_id: str | None = None) -> None:
        task_key = f"TASK-{int(task_id)}"
        related_proc_insts: set[str] = set()

        proc_inst = str(process_instance_id or "").strip()
        if proc_inst:
            related_proc_insts.add(proc_inst)

        cur.execute("SELECT proc_inst_id_ FROM dtlms_wf_hi_taskinst WHERE id_ = %s", (task_key,))
        related_proc_insts.update(
            str(row[0]).strip()
            for row in cur.fetchall()
            if row and str(row[0] or "").strip()
        )

        cur.execute("SELECT proc_inst_id_ FROM dtlms_wf_ru_task WHERE id_ = %s", (task_key,))
        related_proc_insts.update(
            str(row[0]).strip()
            for row in cur.fetchall()
            if row and str(row[0] or "").strip()
        )

        for related_proc_inst in related_proc_insts:
            cur.execute("DELETE FROM dtlms_wf_ru_identitylink WHERE proc_inst_id_ = %s OR task_id_ = %s", (related_proc_inst, task_key))
            cur.execute(
                "DELETE FROM dtlms_wf_ru_variable WHERE proc_inst_id_ = %s OR task_id_ = %s OR id_ LIKE %s",
                (related_proc_inst, task_key, f"RVAR-{related_proc_inst}-%"),
            )
            cur.execute("DELETE FROM dtlms_wf_ru_task WHERE proc_inst_id_ = %s OR id_ = %s", (related_proc_inst, task_key))
            cur.execute("DELETE FROM dtlms_wf_ru_execution WHERE proc_inst_id_ = %s", (related_proc_inst,))
            cur.execute("DELETE FROM dtlms_wf_hi_varinst WHERE proc_inst_id_ = %s", (related_proc_inst,))
            cur.execute("DELETE FROM dtlms_wf_hi_actinst WHERE proc_inst_id_ = %s", (related_proc_inst,))
            cur.execute("DELETE FROM dtlms_wf_hi_taskinst WHERE proc_inst_id_ = %s OR id_ = %s", (related_proc_inst, task_key))
            cur.execute("DELETE FROM dtlms_wf_hi_procinst WHERE proc_inst_id_ = %s", (related_proc_inst,))

        cur.execute("DELETE FROM dtlms_wf_ru_identitylink WHERE task_id_ = %s", (task_key,))
        cur.execute("DELETE FROM dtlms_wf_ru_variable WHERE task_id_ = %s", (task_key,))
        cur.execute("DELETE FROM dtlms_wf_ru_task WHERE id_ = %s", (task_key,))
        cur.execute("DELETE FROM dtlms_wf_hi_taskinst WHERE id_ = %s", (task_key,))

    def _sync_workflow_task_in_tx(self, cur: psycopg.Cursor[Any], task_payload: dict[str, Any]) -> None:
        task = dict(task_payload)
        business_key = str(task.get("business_key") or f"TASK-{task.get('id') or '0'}")
        workflow_name = str(task.get("workflow_name") or "未命名流程")
        process_definition_key = str(task.get("process_definition_key") or task.get("flow_code") or "adhoc_workflow")
        task_definition_key = str(task.get("task_definition_key") or task.get("node_key") or "manual_task")
        process_definition_id = str(task.get("process_definition_id") or self._workflow_process_definition_id(process_definition_key))
        deployment_id = str(task.get("deployment_id") or self._workflow_deployment_id(process_definition_key))
        process_instance_id = str(task.get("process_instance_id") or self._workflow_process_instance_id(process_definition_key, business_key))
        execution_id = str(task.get("execution_id") or self._workflow_execution_id(process_instance_id, task_definition_key))
        start_time = str(task.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        terminal = self._is_workflow_terminal(task)
        candidate_groups = self._normalize_name_list(task.get("candidate_groups"))
        resource_name = f"{process_definition_key}.bpmn20.xml"

        self._delete_workflow_engine_task_in_tx(cur, int(task["id"]), process_instance_id)
        cur.execute(
            """
            INSERT INTO dtlms_wf_de_model (
                id_, name_, key_, category_, version_, model_type_, description_, meta_info_, deployment_id_, resource_name_, editor_source_extra_value_
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s::jsonb)
            ON CONFLICT (id_) DO UPDATE
            SET name_ = EXCLUDED.name_,
                category_ = EXCLUDED.category_,
                deployment_id_ = EXCLUDED.deployment_id_,
                resource_name_ = EXCLUDED.resource_name_,
                editor_source_extra_value_ = EXCLUDED.editor_source_extra_value_,
                last_updated_ = CURRENT_TIMESTAMP
            """,
            (
                f"MODEL-{process_definition_key}",
                workflow_name,
                process_definition_key,
                task.get("business_module") or "流程中心",
                int(task.get("process_definition_version") or 1),
                0,
                f"{workflow_name} 定义",
                self._json_payload({"business_module": task.get("business_module"), "flow_code": task.get("flow_code")}),
                deployment_id,
                resource_name,
                self._json_payload({"source": "runtime_sync", "workflow_name": workflow_name}),
            ),
        )
        cur.execute(
            """
            INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_) DO UPDATE
            SET name_ = EXCLUDED.name_,
                category_ = EXCLUDED.category_,
                key_ = EXCLUDED.key_,
                deploy_time_ = EXCLUDED.deploy_time_
            """,
            (deployment_id, workflow_name, task.get("business_module") or "流程中心", process_definition_key, start_time),
        )
        cur.execute(
            """
            INSERT INTO dtlms_wf_re_procdef (
                id_, key_, version_, deployment_id_, resource_name_, diagram_resource_name_, name_, category_, description_, suspension_state_
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_) DO UPDATE
            SET key_ = EXCLUDED.key_,
                deployment_id_ = EXCLUDED.deployment_id_,
                resource_name_ = EXCLUDED.resource_name_,
                diagram_resource_name_ = EXCLUDED.diagram_resource_name_,
                name_ = EXCLUDED.name_,
                category_ = EXCLUDED.category_,
                description_ = EXCLUDED.description_
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
                self._workflow_end_time(task),
                self._workflow_duration_millis(start_time, self._workflow_end_time(task)),
                None,
                None if not terminal else task_definition_key,
                "rejected" if str(task.get("status") or "") == "已驳回" else None,
                "startEvent",
                "COMPLETED" if terminal else "ACTIVE",
            ),
        )
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
                self._workflow_end_time(task),
                self._workflow_duration_millis(start_time, self._workflow_end_time(task)),
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
        self._insert_workflow_history_variables(cur, task=task, process_instance_id=process_instance_id, execution_id=execution_id, inserted_variables=set())
        if not terminal:
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

    def sync_workflow_task(
        self,
        task_payload: dict[str, Any],
        operation_log: dict[str, Any] | None = None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_workflow_task_in_tx(cur, task_payload)
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def delete_workflow_task(self, task_id: int, process_instance_id: str | None = None) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._delete_workflow_engine_task_in_tx(cur, int(task_id), process_instance_id)
            conn.commit()

    def update_runtime_role(self, role_id: int, payload: dict[str, Any]) -> None:
        del role_id
        self.sync_role(payload)

    def delete_runtime_role(self, role_id: int) -> None:
        self.delete_role(role_id)

    def update_runtime_workflow_task(self, task_id: int, payload: dict[str, Any]) -> None:
        del task_id
        self.sync_workflow_task(payload)

    def delete_runtime_workflow_task(self, task_id: int) -> None:
        self.delete_workflow_task(task_id)

    def update_runtime_recruitment_plan(self, plan_id: int, payload: dict[str, Any]) -> None:
        del plan_id
        self.sync_recruitment_plan(payload, None)

    def sync_recruitment_plan(
        self,
        plan_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)

                academic_year_start = self._normalize_academic_year_start(plan_payload.get("academic_year"))
                current_stage = str(plan_payload.get("current_stage") or "资格审核")
                is_open = bool(plan_payload.get("is_open", True))
                target_quota = int(plan_payload.get("target_quota") or 0)
                cur.execute(
                    """
                    INSERT INTO dtlms_recruitment_plans (
                        id, plan_code, plan_name, academic_year, semester, plan_description,
                        start_date, end_date, target_quota, brochure_image_url, plan_status, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET plan_code = EXCLUDED.plan_code,
                        plan_name = EXCLUDED.plan_name,
                        academic_year = EXCLUDED.academic_year,
                        semester = EXCLUDED.semester,
                        plan_description = EXCLUDED.plan_description,
                        start_date = EXCLUDED.start_date,
                        end_date = EXCLUDED.end_date,
                        target_quota = EXCLUDED.target_quota,
                        brochure_image_url = EXCLUDED.brochure_image_url,
                        plan_status = EXCLUDED.plan_status,
                        updated_at = CURRENT_TIMESTAMP,
                        is_deleted = FALSE
                    """,
                    (
                        int(plan_payload["id"]),
                        f"PLAN-{int(plan_payload['id']):03d}",
                        plan_payload.get("plan_name"),
                        plan_payload.get("academic_year"),
                        plan_payload.get("semester"),
                        plan_payload.get("plan_description"),
                        f"{academic_year_start}-03-01 08:00:00+08",
                        f"{academic_year_start}-10-31 18:00:00+08",
                        target_quota,
                        plan_payload.get("brochure_image_url"),
                        self._map_plan_status(current_stage, is_open),
                    ),
                )
            conn.commit()

    def delete_runtime_recruitment_plan(self, plan_id: int) -> None:
        self.delete_recruitment_plan(plan_id)

    def delete_recruitment_plan(self, plan_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, plan_name, academic_year, semester, brochure_image_url, plan_description
                    FROM dtlms_recruitment_plans
                    WHERE id = %s AND is_deleted = FALSE
                    """,
                    (int(plan_id),),
                )
                record = cur.fetchone()
                if record is None:
                    return None
                cur.execute(
                    "SELECT COUNT(*) AS total FROM dtlms_recruitment_applications WHERE plan_id = %s AND is_deleted = FALSE",
                    (int(plan_id),),
                )
                count_row = cur.fetchone()
                if int((count_row or {}).get("total") or 0) > 0:
                    raise ValueError("当前招生计划下仍有报名申请，不能删除")
                cur.execute(
                    """
                    DELETE FROM dtlms_interview_scores
                    WHERE schedule_id IN (
                        SELECT schedule.id
                        FROM dtlms_interview_schedules schedule
                        JOIN dtlms_interview_groups grp ON grp.id = schedule.interview_group_id
                        WHERE grp.plan_id = %s
                    )
                    """,
                    (int(plan_id),),
                )
                cur.execute(
                    """
                    DELETE FROM dtlms_interview_schedules
                    WHERE interview_group_id IN (
                        SELECT id FROM dtlms_interview_groups WHERE plan_id = %s
                    )
                    """,
                    (int(plan_id),),
                )
                cur.execute(
                    "DELETE FROM dtlms_interview_groups WHERE plan_id = %s",
                    (int(plan_id),),
                )
                cur.execute(
                    "DELETE FROM dtlms_recruitment_plans WHERE id = %s",
                    (int(plan_id),),
                )
            conn.commit()
        return dict(record)

    def update_runtime_training_plan(self, plan_id: int, payload: dict[str, Any]) -> None:
        del plan_id
        self.sync_training_plan(payload)

    def delete_runtime_training_plan(self, plan_id: int) -> None:
        self.delete_training_plan(plan_id)

    def update_runtime_thesis_review(self, review_id: int, payload: dict[str, Any]) -> None:
        del review_id
        self.sync_thesis_review(payload)

    def update_runtime_scientific_report(self, report_id: int, payload: dict[str, Any]) -> None:
        del report_id
        self.sync_scientific_report(payload)

    def delete_runtime_scientific_report(self, report_id: int) -> None:
        self.delete_scientific_report(report_id)

    def update_runtime_outbound_study(self, study_id: int, payload: dict[str, Any]) -> None:
        del study_id
        self.sync_outbound_study(payload)

    def delete_runtime_outbound_study(self, study_id: int) -> None:
        self.delete_outbound_study(study_id)

    def update_runtime_thesis(self, thesis_id: int, payload: dict[str, Any]) -> None:
        del thesis_id
        self.sync_thesis(payload)

    def sync_recruitment_application_status(self, application_id: int, payload: dict[str, Any]) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                application_status = self._map_application_status(str(payload.get("application_status") or ""))
                cur.execute(
                    """
                    UPDATE dtlms_recruitment_applications
                    SET application_status = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND is_deleted = FALSE
                    """,
                    (application_status, int(application_id)),
                )
                portal_student_id = int(payload.get("portal_student_id") or 0)
                if application_status in {"returned", "rejected"} and portal_student_id > 0:
                    cur.execute(
                        """
                        UPDATE dtlms_portal_students
                        SET submitted_at = NULL,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (portal_student_id,),
                    )
            conn.commit()

    def sync_portal_application_submission(
        self,
        portal_student_payload: dict[str, Any],
        application_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        *,
        workflow_task: dict[str, Any] | None = None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)

                cur.execute(
                    "SELECT id FROM dtlms_research_fields WHERE field_name = %s AND is_deleted = FALSE ORDER BY id ASC LIMIT 1",
                    (application_payload.get("intended_field"),),
                )
                intended_field_row = cur.fetchone()
                intended_field_id = int(intended_field_row[0]) if intended_field_row else None

                cur.execute(
                    """
                    INSERT INTO dtlms_portal_students (
                        id, full_name, phone_number, email, id_number, password_hash, gender, birth_date,
                        ethnic_group, native_place, marital_status, religious_belief, id_type, mailing_address,
                        graduation_school, highest_degree, intended_field, political_status, english_level,
                        family_info, education_experience, practice_experience, personal_profile,
                        recommendation_notes, personal_statement_text, signed_agreement, selected_plan_id,
                        selected_team_id, selected_team_name, selected_advisor_user_id, selected_advisor_name,
                        self_evaluation, submitted_at, account_status, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET full_name = EXCLUDED.full_name,
                        phone_number = EXCLUDED.phone_number,
                        email = EXCLUDED.email,
                        id_number = EXCLUDED.id_number,
                        password_hash = EXCLUDED.password_hash,
                        gender = EXCLUDED.gender,
                        birth_date = EXCLUDED.birth_date,
                        ethnic_group = EXCLUDED.ethnic_group,
                        native_place = EXCLUDED.native_place,
                        marital_status = EXCLUDED.marital_status,
                        religious_belief = EXCLUDED.religious_belief,
                        id_type = EXCLUDED.id_type,
                        mailing_address = EXCLUDED.mailing_address,
                        graduation_school = EXCLUDED.graduation_school,
                        highest_degree = EXCLUDED.highest_degree,
                        intended_field = EXCLUDED.intended_field,
                        political_status = EXCLUDED.political_status,
                        english_level = EXCLUDED.english_level,
                        family_info = EXCLUDED.family_info,
                        education_experience = EXCLUDED.education_experience,
                        practice_experience = EXCLUDED.practice_experience,
                        personal_profile = EXCLUDED.personal_profile,
                        recommendation_notes = EXCLUDED.recommendation_notes,
                        personal_statement_text = EXCLUDED.personal_statement_text,
                        signed_agreement = EXCLUDED.signed_agreement,
                        selected_plan_id = EXCLUDED.selected_plan_id,
                        selected_team_id = EXCLUDED.selected_team_id,
                        selected_team_name = EXCLUDED.selected_team_name,
                        selected_advisor_user_id = EXCLUDED.selected_advisor_user_id,
                        selected_advisor_name = EXCLUDED.selected_advisor_name,
                        self_evaluation = EXCLUDED.self_evaluation,
                        submitted_at = EXCLUDED.submitted_at,
                        account_status = EXCLUDED.account_status,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        int(portal_student_payload["id"]),
                        portal_student_payload.get("full_name"),
                        portal_student_payload.get("phone_number"),
                        portal_student_payload.get("email"),
                        portal_student_payload.get("id_number"),
                        portal_student_payload.get("password_hash"),
                        portal_student_payload.get("gender"),
                        portal_student_payload.get("birth_date"),
                        portal_student_payload.get("ethnic_group"),
                        portal_student_payload.get("native_place"),
                        portal_student_payload.get("marital_status"),
                        portal_student_payload.get("religious_belief"),
                        portal_student_payload.get("id_type"),
                        portal_student_payload.get("mailing_address"),
                        portal_student_payload.get("graduation_school"),
                        portal_student_payload.get("highest_degree"),
                        portal_student_payload.get("intended_field"),
                        portal_student_payload.get("political_status"),
                        portal_student_payload.get("english_level"),
                        portal_student_payload.get("family_info"),
                        portal_student_payload.get("education_experience"),
                        portal_student_payload.get("practice_experience"),
                        portal_student_payload.get("personal_profile"),
                        portal_student_payload.get("recommendation_notes"),
                        portal_student_payload.get("personal_statement_text"),
                        bool(portal_student_payload.get("signed_agreement")),
                        portal_student_payload.get("selected_plan_id"),
                        portal_student_payload.get("selected_team_id"),
                        portal_student_payload.get("selected_team_name"),
                        portal_student_payload.get("selected_advisor_user_id"),
                        portal_student_payload.get("selected_advisor_name"),
                        portal_student_payload.get("self_evaluation"),
                        portal_student_payload.get("submitted_at"),
                        self._normalize_portal_account_status(portal_student_payload.get("account_status")),
                        portal_student_payload.get("created_at"),
                        portal_student_payload.get("updated_at"),
                    ),
                )

                profile = self._derive_portal_profile(portal_student_payload)
                if profile is None:
                    cur.execute(
                        "DELETE FROM dtlms_portal_student_profiles WHERE portal_student_id = %s",
                        (int(portal_student_payload["id"]),),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_student_profiles (
                            portal_student_id, full_name_pinyin, profile_photo_url, id_card_collage_url, gender, birth_date, ethnic_group,
                            native_place, political_status, marital_status, religious_belief, id_type,
                            mailing_address, emergency_contact_name, emergency_contact_phone
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (portal_student_id) DO UPDATE
                        SET full_name_pinyin = EXCLUDED.full_name_pinyin,
                            profile_photo_url = EXCLUDED.profile_photo_url,
                            id_card_collage_url = EXCLUDED.id_card_collage_url,
                            gender = EXCLUDED.gender,
                            birth_date = EXCLUDED.birth_date,
                            ethnic_group = EXCLUDED.ethnic_group,
                            native_place = EXCLUDED.native_place,
                            political_status = EXCLUDED.political_status,
                            marital_status = EXCLUDED.marital_status,
                            religious_belief = EXCLUDED.religious_belief,
                            id_type = EXCLUDED.id_type,
                            mailing_address = EXCLUDED.mailing_address,
                            emergency_contact_name = EXCLUDED.emergency_contact_name,
                            emergency_contact_phone = EXCLUDED.emergency_contact_phone,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (
                            int(portal_student_payload["id"]),
                            profile.get("full_name_pinyin"),
                            profile.get("profile_photo_url"),
                            profile.get("id_card_collage_url"),
                            profile.get("gender"),
                            profile.get("birth_date"),
                            profile.get("ethnic_group"),
                            profile.get("native_place"),
                            profile.get("political_status"),
                            profile.get("marital_status"),
                            profile.get("religious_belief"),
                            profile.get("id_type"),
                            profile.get("mailing_address"),
                            profile.get("emergency_contact_name"),
                            profile.get("emergency_contact_phone"),
                        ),
                    )

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
                    "first_choice_team_id",
                    "first_choice",
                    "second_choice_team_id",
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
                    "intended_advisor_user_id",
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
                    "created_at",
                    "updated_at",
                ]
                application_values = (
                    int(application_payload["id"]),
                    int(application_payload.get("plan_id") or 0),
                    int(application_payload.get("portal_student_id") or portal_student_payload["id"]),
                    application_payload.get("business_key"),
                    application_payload.get("student_name"),
                    application_payload.get("candidate_no") or application_payload.get("business_key"),
                    application_payload.get("gender") or "未知",
                    application_payload.get("graduation_school"),
                    application_payload.get("highest_degree"),
                    intended_field_id,
                    self._map_application_status(str(application_payload.get("application_status") or "报名已提交")),
                    application_payload.get("review_round"),
                    application_payload.get("first_choice_team_id"),
                    application_payload.get("first_choice"),
                    application_payload.get("second_choice_team_id"),
                    application_payload.get("second_choice"),
                    application_payload.get("political_status"),
                    application_payload.get("marital_status"),
                    application_payload.get("religious_belief"),
                    application_payload.get("native_place"),
                    application_payload.get("phone_number"),
                    application_payload.get("email"),
                    application_payload.get("mailing_address"),
                    application_payload.get("id_type"),
                    application_payload.get("id_number"),
                    application_payload.get("undergraduate_school"),
                    application_payload.get("accept_adjustment"),
                    application_payload.get("undergraduate_average_score"),
                    application_payload.get("undergraduate_gpa"),
                    application_payload.get("undergraduate_rank"),
                    application_payload.get("undergraduate_major"),
                    application_payload.get("graduate_average_score"),
                    application_payload.get("graduate_gpa"),
                    application_payload.get("graduate_rank"),
                    application_payload.get("graduate_major"),
                    application_payload.get("intended_advisor_user_id"),
                    application_payload.get("intended_advisor_name"),
                    application_payload.get("discovery_channel"),
                    application_payload.get("source_channel"),
                    application_payload.get("source_channel_other"),
                    application_payload.get("graduate_school"),
                    application_payload.get("overseas_university_name"),
                    application_payload.get("overseas_master_university_name"),
                    application_payload.get("self_evaluation"),
                    application_payload.get("applied_at"),
                    application_payload.get("research_problem"),
                    application_payload.get("research_status_analysis"),
                    application_payload.get("research_impact"),
                    application_payload.get("ai_society_impact"),
                    application_payload.get("dissenting_view"),
                    application_payload.get("family_info"),
                    application_payload.get("education_experience"),
                    application_payload.get("practice_experience"),
                    application_payload.get("personal_statement_text"),
                    application_payload.get("student_activity_experience"),
                    application_payload.get("personal_statement_attachment"),
                    application_payload.get("material_list_attachment"),
                    application_payload.get("supplementary_profile"),
                    application_payload.get("created_at") or application_payload.get("applied_at") or portal_student_payload.get("created_at"),
                    application_payload.get("updated_at") or application_payload.get("applied_at") or portal_student_payload.get("updated_at"),
                )
                update_columns = [column for column in application_columns if column not in {"id", "created_at"}]
                cur.execute(
                    f"""
                    INSERT INTO dtlms_recruitment_applications ({', '.join(application_columns)}, is_deleted)
                    VALUES ({', '.join(['%s'] * len(application_columns))}, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET {', '.join(f'{column} = EXCLUDED.{column}' for column in update_columns)},
                        is_deleted = FALSE
                    """,
                    application_values,
                )

                application_id = int(application_payload["id"])
                portal_student_id = int(portal_student_payload["id"])
                draft = self._derive_portal_application_draft(portal_student_payload) or {}

                cur.execute("DELETE FROM dtlms_portal_application_preferences WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_education_experiences WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_practice_experiences WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_english_proficiencies WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_family_members WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_achievement_records WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_personal_statements WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_declarations WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_portal_application_attachments WHERE application_id = %s", (application_id,))
                cur.execute("DELETE FROM dtlms_application_materials WHERE application_id = %s", (application_id,))

                def insert_attachment(
                    owner_type: str,
                    owner_id: int | None,
                    category: str,
                    file_url: str | None,
                    file_name: str | None = None,
                ) -> None:
                    if not file_url:
                        return
                    attachment_name = str(file_name or "").strip() or str(file_url).rstrip("/").split("/")[-1] or f"{category}.dat"
                    file_suffix = Path(attachment_name).suffix.lower().lstrip(".") or None
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_application_attachments (
                            portal_student_id, application_id, owner_type, owner_id, attachment_category,
                            file_name, file_url, file_type
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (portal_student_id, application_id, owner_type, owner_id, category, attachment_name, file_url, file_suffix),
                    )

                for preference in draft.get("preferences", []):
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_application_preferences (
                            application_id, preference_order, team_id, research_center_name, advisor_user_id, advisor_name, is_optional
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            application_id,
                            int(preference.get("preference_order") or 1),
                            int(preference.get("team_id") or 0) or None,
                            preference.get("research_center_name"),
                            int(preference.get("advisor_user_id") or 0) or None,
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
                            transcript_attachment_url, degree_certificate_attachment_url, graduation_certificate_attachment_url
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                            education.get("graduation_certificate_attachment_url"),
                        ),
                    )
                    education_row = cur.fetchone()
                    education_id = int(education_row[0]) if education_row else None
                    insert_attachment(
                        "education_experience",
                        education_id,
                        "transcript",
                        education.get("transcript_attachment_url"),
                        education.get("transcript_attachment_name"),
                    )
                    insert_attachment(
                        "education_experience",
                        education_id,
                        "degree_certificate",
                        education.get("degree_certificate_attachment_url"),
                        education.get("degree_certificate_attachment_name"),
                    )
                    insert_attachment(
                        "education_experience",
                        education_id,
                        "graduation_certificate",
                        education.get("graduation_certificate_attachment_url"),
                        education.get("graduation_certificate_attachment_name"),
                    )

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
                    insert_attachment(
                        "english_proficiency",
                        english_id,
                        "english_certificate",
                        english.get("certificate_attachment_url"),
                        english.get("certificate_attachment_name"),
                    )

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
                            publish_or_index_month, achievement_month, award_name, award_rank,
                            award_certificate_attachment_url, awarding_organization, award_level,
                            award_year, description_text, responsibility_text
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            application_id,
                            achievement.get("achievement_type"),
                            achievement.get("paper_title"),
                            achievement.get("author_order"),
                            achievement.get("journal_or_conference"),
                            achievement.get("publish_or_index_month"),
                            achievement.get("achievement_month"),
                            achievement.get("award_name"),
                            achievement.get("award_rank"),
                            achievement.get("award_certificate_attachment_url"),
                            achievement.get("awarding_organization"),
                            achievement.get("award_level"),
                            achievement.get("award_year"),
                            achievement.get("description_text"),
                            achievement.get("responsibility_text"),
                        ),
                    )
                    achievement_row = cur.fetchone()
                    achievement_id = int(achievement_row[0]) if achievement_row else None
                    insert_attachment(
                        "achievement_record",
                        achievement_id,
                        "achievement_award_certificate",
                        achievement.get("award_certificate_attachment_url"),
                        achievement.get("award_certificate_attachment_name"),
                    )

                personal_statement = draft.get("personal_statement") if isinstance(draft.get("personal_statement"), dict) else {}
                if personal_statement:
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_application_personal_statements (
                            application_id,
                            personal_statement_text,
                            growth_experience_text,
                            program_application_reason_text,
                            career_plan_text,
                            resume_attachment_url,
                            supporting_material_attachment_url,
                            ai_problem_statement,
                            ai_industry_opinion
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            application_id,
                            personal_statement.get("personal_statement_text"),
                            personal_statement.get("growth_experience_text"),
                            personal_statement.get("program_application_reason_text"),
                            personal_statement.get("career_plan_text"),
                            personal_statement.get("resume_attachment_url"),
                            personal_statement.get("supporting_material_attachment_url"),
                            personal_statement.get("ai_problem_statement"),
                            personal_statement.get("ai_industry_opinion"),
                        ),
                    )
                    insert_attachment(
                        "personal_statement",
                        application_id,
                        "resume",
                        personal_statement.get("resume_attachment_url"),
                        personal_statement.get("resume_attachment_name"),
                    )

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

                legacy_personal_statement_attachment = application_payload.get("personal_statement_attachment")
                if legacy_personal_statement_attachment and legacy_personal_statement_attachment != personal_statement.get("resume_attachment_url"):
                    insert_attachment("portal_application", application_id, "personal_statement", legacy_personal_statement_attachment)

                material_list_attachment = application_payload.get("material_list_attachment")
                insert_attachment("portal_application", application_id, "materials", material_list_attachment)
                cur.execute(
                    """
                    INSERT INTO dtlms_application_materials (application_id, material_type, material_status, file_url, is_deleted)
                    VALUES (%s, %s, %s, %s, FALSE)
                    """,
                    (
                        application_id,
                        "报名材料",
                        self._map_material_status(str(application_payload.get("material_status") or "待补材料")),
                        material_list_attachment or f"/materials/{application_payload.get('candidate_no') or application_payload.get('business_key')}.zip",
                    ),
                )
            conn.commit()

    def delete_runtime_recruitment_application(self, application_id: int) -> None:
        self.delete_recruitment_application(application_id)

    def delete_recruitment_application(self, application_id: int) -> dict[str, Any] | None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, student_name, business_key, application_status
                    FROM dtlms_recruitment_applications
                    WHERE id = %s AND is_deleted = FALSE
                    """,
                    (int(application_id),),
                )
                record = cur.fetchone()
                if record is not None:
                    cur.execute(
                        """
                        UPDATE dtlms_recruitment_applications
                        SET is_deleted = TRUE,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (int(application_id),),
                    )
                    cur.execute(
                        "UPDATE dtlms_application_materials SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE application_id = %s",
                        (int(application_id),),
                    )
            conn.commit()
        return dict(record) if record is not None else None

    def update_runtime_audit_policy(self, policy_id: int, payload: dict[str, Any]) -> None:
        del policy_id
        self.sync_audit_policy(payload)

    def delete_runtime_audit_policy(self, policy_id: int) -> None:
        self.delete_audit_policy(policy_id)

    def update_runtime_integration(self, integration_id: int, payload: dict[str, Any]) -> None:
        del integration_id
        self.sync_integration(payload)

    def delete_runtime_integration(self, integration_id: int) -> None:
        self.delete_integration(integration_id)

    def delete_runtime_thesis(self, thesis_id: int) -> None:
        self.delete_thesis(thesis_id)

    def update_runtime_portal_student(self, student_id: int, payload: dict[str, Any]) -> None:
        del student_id
        self.sync_portal_student(payload, None)

    def sync_portal_student(
        self,
        portal_student_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        *,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)

                cur.execute(
                    """
                    INSERT INTO dtlms_portal_students (
                        id, full_name, phone_number, email, id_number, password_hash, gender, birth_date,
                        ethnic_group, native_place, marital_status, religious_belief, id_type, mailing_address,
                        graduation_school, highest_degree, intended_field, political_status, english_level,
                        family_info, education_experience, practice_experience, personal_profile,
                        recommendation_notes, personal_statement_text, signed_agreement, selected_plan_id,
                        selected_team_id, selected_team_name, selected_advisor_user_id, selected_advisor_name,
                        self_evaluation, submitted_at, account_status, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE
                    SET full_name = EXCLUDED.full_name,
                        phone_number = EXCLUDED.phone_number,
                        email = EXCLUDED.email,
                        id_number = EXCLUDED.id_number,
                        password_hash = EXCLUDED.password_hash,
                        gender = EXCLUDED.gender,
                        birth_date = EXCLUDED.birth_date,
                        ethnic_group = EXCLUDED.ethnic_group,
                        native_place = EXCLUDED.native_place,
                        marital_status = EXCLUDED.marital_status,
                        religious_belief = EXCLUDED.religious_belief,
                        id_type = EXCLUDED.id_type,
                        mailing_address = EXCLUDED.mailing_address,
                        graduation_school = EXCLUDED.graduation_school,
                        highest_degree = EXCLUDED.highest_degree,
                        intended_field = EXCLUDED.intended_field,
                        political_status = EXCLUDED.political_status,
                        english_level = EXCLUDED.english_level,
                        family_info = EXCLUDED.family_info,
                        education_experience = EXCLUDED.education_experience,
                        practice_experience = EXCLUDED.practice_experience,
                        personal_profile = EXCLUDED.personal_profile,
                        recommendation_notes = EXCLUDED.recommendation_notes,
                        personal_statement_text = EXCLUDED.personal_statement_text,
                        signed_agreement = EXCLUDED.signed_agreement,
                        selected_plan_id = EXCLUDED.selected_plan_id,
                        selected_team_id = EXCLUDED.selected_team_id,
                        selected_team_name = EXCLUDED.selected_team_name,
                        selected_advisor_user_id = EXCLUDED.selected_advisor_user_id,
                        selected_advisor_name = EXCLUDED.selected_advisor_name,
                        self_evaluation = EXCLUDED.self_evaluation,
                        submitted_at = EXCLUDED.submitted_at,
                        account_status = EXCLUDED.account_status,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (
                        int(portal_student_payload["id"]),
                        portal_student_payload.get("full_name"),
                        portal_student_payload.get("phone_number"),
                        portal_student_payload.get("email"),
                        portal_student_payload.get("id_number"),
                        portal_student_payload.get("password_hash"),
                        portal_student_payload.get("gender"),
                        portal_student_payload.get("birth_date"),
                        portal_student_payload.get("ethnic_group"),
                        portal_student_payload.get("native_place"),
                        portal_student_payload.get("marital_status"),
                        portal_student_payload.get("religious_belief"),
                        portal_student_payload.get("id_type"),
                        portal_student_payload.get("mailing_address"),
                        portal_student_payload.get("graduation_school"),
                        portal_student_payload.get("highest_degree"),
                        portal_student_payload.get("intended_field"),
                        portal_student_payload.get("political_status"),
                        portal_student_payload.get("english_level"),
                        portal_student_payload.get("family_info"),
                        portal_student_payload.get("education_experience"),
                        portal_student_payload.get("practice_experience"),
                        portal_student_payload.get("personal_profile"),
                        portal_student_payload.get("recommendation_notes"),
                        portal_student_payload.get("personal_statement_text"),
                        bool(portal_student_payload.get("signed_agreement")),
                        portal_student_payload.get("selected_plan_id"),
                        portal_student_payload.get("selected_team_id"),
                        portal_student_payload.get("selected_team_name"),
                        portal_student_payload.get("selected_advisor_user_id"),
                        portal_student_payload.get("selected_advisor_name"),
                        portal_student_payload.get("self_evaluation"),
                        portal_student_payload.get("submitted_at"),
                        self._normalize_portal_account_status(portal_student_payload.get("account_status")),
                        portal_student_payload.get("created_at"),
                        portal_student_payload.get("updated_at"),
                    ),
                )

                profile = self._derive_portal_profile(portal_student_payload)
                if profile is None:
                    cur.execute(
                        "DELETE FROM dtlms_portal_student_profiles WHERE portal_student_id = %s",
                        (int(portal_student_payload["id"]),),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO dtlms_portal_student_profiles (
                            portal_student_id, full_name_pinyin, profile_photo_url, id_card_collage_url, gender, birth_date, ethnic_group,
                            native_place, political_status, marital_status, religious_belief, id_type,
                            mailing_address, emergency_contact_name, emergency_contact_phone
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (portal_student_id) DO UPDATE
                        SET full_name_pinyin = EXCLUDED.full_name_pinyin,
                            profile_photo_url = EXCLUDED.profile_photo_url,
                            id_card_collage_url = EXCLUDED.id_card_collage_url,
                            gender = EXCLUDED.gender,
                            birth_date = EXCLUDED.birth_date,
                            ethnic_group = EXCLUDED.ethnic_group,
                            native_place = EXCLUDED.native_place,
                            political_status = EXCLUDED.political_status,
                            marital_status = EXCLUDED.marital_status,
                            religious_belief = EXCLUDED.religious_belief,
                            id_type = EXCLUDED.id_type,
                            mailing_address = EXCLUDED.mailing_address,
                            emergency_contact_name = EXCLUDED.emergency_contact_name,
                            emergency_contact_phone = EXCLUDED.emergency_contact_phone,
                            updated_at = CURRENT_TIMESTAMP
                        """,
                        (
                            int(portal_student_payload["id"]),
                            profile.get("full_name_pinyin"),
                            profile.get("profile_photo_url"),
                            profile.get("id_card_collage_url"),
                            profile.get("gender"),
                            profile.get("birth_date"),
                            profile.get("ethnic_group"),
                            profile.get("native_place"),
                            profile.get("political_status"),
                            profile.get("marital_status"),
                            profile.get("religious_belief"),
                            profile.get("id_type"),
                            profile.get("mailing_address"),
                            profile.get("emergency_contact_name"),
                            profile.get("emergency_contact_phone"),
                        ),
                    )
            conn.commit()

    def update_runtime_counter(self, counter_name: str, counter_value: int) -> None:
        del counter_name, counter_value

    def insert_runtime_operation_log(self, payload: dict[str, Any]) -> None:
        self.sync_operation_log(payload)

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
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)

                lead_user_id = int(team_payload.get("director_id") or team_payload.get("lead_user_id") or 0) or None
                advisor_user_ids = [int(item) for item in (team_payload.get("advisor_ids") or []) if int(item or 0) > 0]
                if lead_user_id and lead_user_id not in advisor_user_ids:
                    advisor_user_ids.insert(0, lead_user_id)
                advisor_id_map = self._ensure_advisors_for_user_ids(cur, advisor_user_ids)
                lead_advisor_id = advisor_id_map.get(lead_user_id) if lead_user_id else None
                established_on = team_payload.get("created_on") or team_payload.get("established_on")
                cur.execute(
                    """
                    INSERT INTO dtlms_teams (
                        id, team_code, team_name, department_name, discipline_name, lead_advisor_id, lead_user_id,
                        research_directions, team_status, established_on, description, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET team_code = EXCLUDED.team_code,
                        team_name = EXCLUDED.team_name,
                        department_name = EXCLUDED.department_name,
                        discipline_name = EXCLUDED.discipline_name,
                        lead_advisor_id = EXCLUDED.lead_advisor_id,
                        lead_user_id = EXCLUDED.lead_user_id,
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
                        lead_user_id,
                        self._normalize_research_directions(team_payload.get("research_directions")),
                        self._map_team_status(team_payload.get("status", "启用")),
                        established_on,
                        team_payload.get("description"),
                    ),
                )

                cur.execute(
                    """
                    SELECT id, advisor_user_id
                    FROM dtlms_team_advisors
                    WHERE team_id = %s
                    """,
                    (int(team_payload["id"]),),
                )
                existing_relations = {
                    int(row[1]): int(row[0])
                    for row in cur.fetchall()
                    if int(row[1] or 0) > 0
                }
                selected_user_ids = set(advisor_user_ids)
                if selected_user_ids:
                    cur.execute(
                        """
                        UPDATE dtlms_team_advisors
                        SET is_deleted = TRUE,
                            left_on = COALESCE(left_on, CURRENT_DATE),
                            updated_at = CURRENT_TIMESTAMP
                        WHERE team_id = %s
                          AND advisor_user_id IS NOT NULL
                          AND advisor_user_id <> ALL(%s)
                        """,
                        (int(team_payload["id"]), sorted(selected_user_ids)),
                    )

                for advisor_user_id in advisor_user_ids:
                    advisor_id = advisor_id_map.get(advisor_user_id)
                    if not advisor_id:
                        continue
                    advisor_role = "lead" if lead_user_id and advisor_user_id == lead_user_id else "member"
                    relation_id = existing_relations.get(advisor_user_id)
                    if relation_id is not None:
                        cur.execute(
                            """
                            UPDATE dtlms_team_advisors
                            SET advisor_id = %s,
                                advisor_role = %s,
                                joined_on = COALESCE(joined_on, %s),
                                left_on = NULL,
                                is_deleted = FALSE,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (advisor_id, advisor_role, established_on, relation_id),
                        )
                        continue
                    cur.execute(
                        """
                        INSERT INTO dtlms_team_advisors (
                            team_id, advisor_id, advisor_user_id, advisor_role, joined_on, left_on, is_deleted
                        ) VALUES (%s, %s, %s, %s, %s, NULL, FALSE)
                        """,
                        (int(team_payload["id"]), advisor_id, advisor_user_id, advisor_role, established_on),
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

    def sync_updated_student(
        self,
        student_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                self._sync_operation_log_in_tx(cur, operation_log)

                team_map = self._fetch_map(cur, "SELECT id, team_name AS key FROM dtlms_teams WHERE is_deleted = FALSE")
                team_name = str(student_payload.get("team_name") or "").strip()
                advisor_name = str(student_payload.get("advisor_name") or "").strip()
                advisor_map = self._ensure_advisors_exist(cur, [advisor_name] if advisor_name else [])
                team_id = team_map.get(team_name) if team_name else None
                advisor_id = advisor_map.get(advisor_name) if advisor_name else None
                status = self._map_student_status(str(student_payload.get("status") or "在校"))
                cur.execute(
                    """
                    INSERT INTO dtlms_students (
                        id, portal_student_id, student_no, full_name, gender, political_status, phone_number, identity_no,
                        enrollment_year, degree_type, team_id, current_status, primary_advisor_id, is_deleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)
                    ON CONFLICT (id) DO UPDATE
                    SET portal_student_id = EXCLUDED.portal_student_id,
                        student_no = EXCLUDED.student_no,
                        full_name = EXCLUDED.full_name,
                        political_status = EXCLUDED.political_status,
                        phone_number = EXCLUDED.phone_number,
                        enrollment_year = EXCLUDED.enrollment_year,
                        degree_type = EXCLUDED.degree_type,
                        team_id = EXCLUDED.team_id,
                        current_status = EXCLUDED.current_status,
                        primary_advisor_id = EXCLUDED.primary_advisor_id,
                        updated_at = CURRENT_TIMESTAMP,
                        is_deleted = FALSE
                    """,
                    (
                        int(student_payload["id"]),
                        int(student_payload.get("portal_student_id") or 0) or None,
                        student_payload.get("student_no"),
                        student_payload.get("full_name"),
                        "未知",
                        student_payload.get("political_status"),
                        student_payload.get("phone_number"),
                        f"ID-{student_payload.get('student_no')}",
                        int(student_payload.get("enrollment_year") or 0),
                        student_payload.get("degree_type"),
                        team_id,
                        status,
                        advisor_id,
                    ),
                )
            conn.commit()

    def sync_created_student(
        self,
        student_payload: dict[str, Any],
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.sync_updated_student(student_payload, operation_log=operation_log, counters=counters)

    def sync_deleted_student(
        self,
        student_id: int,
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute("UPDATE dtlms_students SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (int(student_id),))
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()

    def sync_deleted_center(
        self,
        center_id: int,
        operation_log: dict[str, Any] | None,
        counters: dict[str, int] | None = None,
    ) -> None:
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            with conn.cursor() as cur:
                self._sync_runtime_counters_in_tx(cur, counters)
                cur.execute("DELETE FROM dtlms_team_advisors WHERE team_id = %s", (int(center_id),))
                cur.execute("DELETE FROM dtlms_teams WHERE id = %s", (int(center_id),))
                self._sync_operation_log_in_tx(cur, operation_log)
            conn.commit()
