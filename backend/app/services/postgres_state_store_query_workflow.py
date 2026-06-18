"""Workflow PostgreSQL query mixin.

This module contains workflow task state and workflow detail query helpers.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast

import psycopg
from psycopg.rows import dict_row

from app.core.config import BACKEND_DIR, settings


logger = logging.getLogger(__name__)

class PostgresStateStoreQueryWorkflowMixin:
    """Query mixin extracted by functional module."""

    def load_workflow_task_state(self) -> list[dict[str, Any]]:
        """Execute query logic for `load_workflow_task_state`."""
        # Reuse the PostgreSQL paged workflow query so startup does one batched read
        # instead of replaying a per-task snapshot query for every history row.
        items, _ = self.list_workflow_tasks_page(page=1, page_size=1_000_000)
        return items

    def list_workflow_tasks_page(
        self,
        status: str | None = None,
        module: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[dict[str, Any]], int]:
        """Execute query logic for `list_workflow_tasks_page`."""
        self.ensure_schema()
        offset = max(page - 1, 0) * page_size
        where_clauses = ["1 = 1"]
        params: list[Any] = []

        if status:
            where_clauses.append("COALESCE(vars.task_status, '') = %s")
            params.append(status)
        if module:
            where_clauses.append("COALESCE(vars.business_module, '') = %s")
            params.append(module)
        if keyword and str(keyword).strip():
            where_clauses.append(
                """
                concat_ws(
                    ' ',
                    COALESCE(vars.workflow_name, pd.name_, ''),
                    COALESCE(ht.business_key_, ''),
                    COALESCE(ht.name_, ''),
                    COALESCE(vars.applicant_name, ''),
                    COALESCE(vars.current_handler, '')
                ) ILIKE %s
                """
            )
            params.append(f"%{str(keyword).strip()}%")

        where_sql = " AND ".join(where_clauses)

        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT COUNT(*) AS total
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE {where_sql}
                    """,
                    params,
                )
                total_row = cur.fetchone()
                total = int(total_row["total"] if total_row else 0)

                self._execute_dynamic(
                    cur,
                    f"""
                    SELECT
                        ht.id_ AS task_key,
                        ht.business_key_,
                        ht.name_ AS title,
                        ht.start_time_,
                        ht.due_date_,
                        ht.priority_,
                        ht.proc_def_id_,
                        ht.proc_inst_id_,
                        ht.exec_id_,
                        ht.task_def_key_,
                        pd.key_ AS process_definition_key,
                        pd.name_ AS process_definition_name,
                        vars.workflow_name,
                        vars.business_module,
                        vars.applicant_name,
                        vars.current_handler,
                        vars.current_node,
                        vars.task_status,
                        vars.latest_comment,
                        vars.form_summary,
                        vars.flow_code,
                        vars.node_key,
                        vars.entity_id,
                        vars.candidate_groups,
                        vars.history_entries
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary,
                            MAX(CASE WHEN latest_var.name_ = 'flowCode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS flow_code,
                            MAX(CASE WHEN latest_var.name_ = 'nodeKey' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS node_key,
                            MAX(CASE WHEN latest_var.name_ = 'entityId' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS entity_id,
                            MAX(CASE WHEN latest_var.name_ = 'candidateGroups' THEN latest_var.json_value_::text END)::jsonb AS candidate_groups,
                            MAX(CASE WHEN latest_var.name_ = 'historyEntries' THEN latest_var.json_value_::text END)::jsonb AS history_entries
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE {where_sql}
                    ORDER BY ht.start_time_ DESC, ht.id_ DESC
                    LIMIT %s OFFSET %s
                    """,
                    [*params, page_size, offset],
                )
                return [self._normalize_workflow_task_snapshot_row(dict(row)) for row in cur.fetchall()], total

    def get_workflow_task_snapshot(self, task_id: int) -> dict[str, Any] | None:
        """Execute query logic for `get_workflow_task_snapshot`."""
        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ht.id_ AS task_key,
                        ht.business_key_,
                        ht.name_ AS title,
                        ht.start_time_,
                        ht.due_date_,
                        ht.priority_,
                        ht.proc_def_id_,
                        ht.proc_inst_id_,
                        ht.exec_id_,
                        ht.task_def_key_,
                        pd.key_ AS process_definition_key,
                        pd.name_ AS process_definition_name,
                        vars.workflow_name,
                        vars.business_module,
                        vars.applicant_name,
                        vars.current_handler,
                        vars.current_node,
                        vars.task_status,
                        vars.latest_comment,
                        vars.form_summary,
                        vars.flow_code,
                        vars.node_key,
                        vars.entity_id,
                        vars.candidate_groups,
                        vars.history_entries
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary,
                            MAX(CASE WHEN latest_var.name_ = 'flowCode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS flow_code,
                            MAX(CASE WHEN latest_var.name_ = 'nodeKey' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS node_key,
                            MAX(CASE WHEN latest_var.name_ = 'entityId' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS entity_id,
                            MAX(CASE WHEN latest_var.name_ = 'candidateGroups' THEN latest_var.json_value_::text END)::jsonb AS candidate_groups,
                            MAX(CASE WHEN latest_var.name_ = 'historyEntries' THEN latest_var.json_value_::text END)::jsonb AS history_entries
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE ht.id_ = %s
                    LIMIT 1
                    """,
                    (f"TASK-{int(task_id)}",),
                )
                row = cur.fetchone()
                return self._normalize_workflow_task_snapshot_row(dict(row)) if row else None

    def get_workflow_task_snapshot_by_business_key(self, business_key: str) -> dict[str, Any] | None:
        """Execute query logic for `get_workflow_task_snapshot_by_business_key`."""
        normalized_business_key = str(business_key or "").strip()
        if not normalized_business_key:
            return None

        self.ensure_schema()
        with self._connect(settings.postgres_db) as conn:
            conn.row_factory = dict_row
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        ht.id_ AS task_key,
                        ht.business_key_,
                        ht.name_ AS title,
                        ht.start_time_,
                        ht.due_date_,
                        ht.priority_,
                        ht.proc_def_id_,
                        ht.proc_inst_id_,
                        ht.exec_id_,
                        ht.task_def_key_,
                        pd.key_ AS process_definition_key,
                        pd.name_ AS process_definition_name,
                        vars.workflow_name,
                        vars.business_module,
                        vars.applicant_name,
                        vars.current_handler,
                        vars.current_node,
                        vars.task_status,
                        vars.latest_comment,
                        vars.form_summary,
                        vars.flow_code,
                        vars.node_key,
                        vars.entity_id,
                        vars.candidate_groups,
                        vars.history_entries
                    FROM dtlms_wf_hi_taskinst ht
                    JOIN dtlms_wf_re_procdef pd ON pd.id_ = ht.proc_def_id_
                    LEFT JOIN LATERAL (
                        SELECT
                            MAX(CASE WHEN latest_var.name_ = 'workflowName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS workflow_name,
                            MAX(CASE WHEN latest_var.name_ = 'businessModule' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS business_module,
                            MAX(CASE WHEN latest_var.name_ = 'applicantName' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS applicant_name,
                            MAX(CASE WHEN latest_var.name_ = 'currentHandler' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_handler,
                            MAX(CASE WHEN latest_var.name_ = 'currentNode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS current_node,
                            MAX(CASE WHEN latest_var.name_ = 'taskStatus' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS task_status,
                            MAX(CASE WHEN latest_var.name_ = 'latestComment' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS latest_comment,
                            MAX(CASE WHEN latest_var.name_ = 'formSummary' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS form_summary,
                            MAX(CASE WHEN latest_var.name_ = 'flowCode' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS flow_code,
                            MAX(CASE WHEN latest_var.name_ = 'nodeKey' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS node_key,
                            MAX(CASE WHEN latest_var.name_ = 'entityId' THEN COALESCE(latest_var.text_value_, latest_var.json_value_->>'value') END) AS entity_id,
                            MAX(CASE WHEN latest_var.name_ = 'candidateGroups' THEN latest_var.json_value_::text END)::jsonb AS candidate_groups,
                            MAX(CASE WHEN latest_var.name_ = 'historyEntries' THEN latest_var.json_value_::text END)::jsonb AS history_entries
                        FROM (
                            SELECT DISTINCT ON (hv.name_)
                                hv.name_,
                                hv.text_value_,
                                hv.json_value_
                            FROM dtlms_wf_hi_varinst hv
                            WHERE hv.proc_inst_id_ = ht.proc_inst_id_
                            ORDER BY hv.name_, hv.last_updated_time_ DESC, hv.id_ DESC
                        ) latest_var
                    ) vars ON TRUE
                    WHERE ht.business_key_ = %s
                    ORDER BY ht.start_time_ DESC, ht.id_ DESC
                    LIMIT 1
                    """,
                    (normalized_business_key,),
                )
                row = cur.fetchone()
                return self._normalize_workflow_task_snapshot_row(dict(row)) if row else None
