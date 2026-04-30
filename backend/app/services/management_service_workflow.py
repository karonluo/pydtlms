from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStoreWorkflowMixin:
    def _workflow_action_result(self, task: dict[str, Any], principal_roles: list[str] | None = None) -> dict[str, Any]:
        return {
            "task": self._build_workflow_task_record(task, principal_roles=principal_roles),
            "history": [self._build_workflow_history_record(item) for item in task.get("history", [])],
        }

    def _workflow_definition(self, flow_code: str) -> dict[str, Any]:
        definition = MANAGED_WORKFLOW_DEFINITIONS.get(flow_code)
        if not definition:
            raise ValueError(f"Unsupported workflow flow: {flow_code}")
        return definition

    def _workflow_name_code(self, workflow_name: str) -> str:
        normalized = str(workflow_name or "").strip()
        if normalized in WORKFLOW_NAME_INITIALS_MAP:
            return WORKFLOW_NAME_INITIALS_MAP[normalized]
        ascii_code = "".join(char for char in normalized.upper() if "A" <= char <= "Z")
        if ascii_code:
            return ascii_code
        return "YWLC"

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

    def _workflow_business_key_date(self, created_at: str | None = None) -> str:
        text = str(created_at or "").strip()
        if len(text) >= 10:
            date_part = text[:10].replace("-", "")
            if len(date_part) == 8 and date_part.isdigit():
                return date_part
        return datetime.now().strftime("%Y%m%d")

    def _workflow_business_key_year(self, created_at: str | None = None) -> str:
        text = str(created_at or "").strip()
        if len(text) >= 4:
            year_part = text[:4]
            if year_part.isdigit():
                return year_part
        return datetime.now().strftime("%Y")

    def _next_workflow_business_sequence(self, workflow_code: str, business_date: str) -> int:
        cache_key = build_cache_key("workflow", "business-key", workflow_code, business_date)
        try:
            client = self._get_cache_client()
            sequence = int(client.incr(cache_key))
            if sequence == 1:
                client.expire(cache_key, 3 * 24 * 60 * 60)
            return sequence
        except Exception:
            fallback_key = f'workflow_business_key:{workflow_code}:{business_date}'
            self._counters[fallback_key] = int(self._counters.get(fallback_key, 0)) + 1
            return int(self._counters[fallback_key])

    def _workflow_business_key_exists(self, business_key: str) -> bool:
        for task in self._list("workflow_tasks"):
            if str(task.get("business_key") or "") == business_key:
                return True
        for definition in MANAGED_WORKFLOW_DEFINITIONS.values():
            for item in self._list(definition["business_dataset"]):
                if str(item.get("business_key") or item.get("candidate_no") or "") == business_key:
                    return True
        return False

    def _generate_workflow_business_key(self, workflow_name: str, created_at: str | None = None) -> str:
        workflow_code = self._workflow_name_code(workflow_name)
        business_date = self._workflow_business_key_date(created_at)
        while True:
            sequence = self._next_workflow_business_sequence(workflow_code, business_date)
            business_key = f"{workflow_code}{business_date}{sequence:04d}"
            if not self._workflow_business_key_exists(business_key):
                return business_key

    def _generate_recruitment_application_business_key(self, created_at: str | None = None) -> str:
        business_year = self._workflow_business_key_year(created_at)
        workflow_code = "SH"
        while True:
            sequence = self._next_workflow_business_sequence(workflow_code, business_year)
            business_key = f"{workflow_code}{business_year}{sequence:04d}"
            if not self._workflow_business_key_exists(business_key):
                return business_key

    @staticmethod
    def _is_standard_recruitment_application_business_key(business_key: Any) -> bool:
        normalized = str(business_key or "").strip()
        return len(normalized) == 10 and normalized.startswith("SH") and normalized[2:].isdigit()

    def _normalize_managed_business_key_candidate(
        self,
        flow_code: str,
        item: dict[str, Any],
        existing_key: str | None = None,
        created_at: str | None = None,
    ) -> tuple[str | None, str | None]:
        candidate_key = str(existing_key or item.get("business_key") or "").strip() or None
        business_key_created_at = created_at
        if flow_code == "recruitment_application":
            if not candidate_key:
                candidate_key = str(item.get("candidate_no") or "").strip() or None
            if candidate_key and not self._is_standard_recruitment_application_business_key(candidate_key):
                candidate_key = None
            business_key_created_at = business_key_created_at or str(item.get("applied_at") or item.get("created_at") or "").strip() or None
        return candidate_key, business_key_created_at

    def _workflow_business_key(self, flow_code: str, entity_id: int, existing_key: str | None = None, created_at: str | None = None) -> str:
        if existing_key:
            return str(existing_key)
        del entity_id
        if flow_code == "recruitment_application":
            return self._generate_recruitment_application_business_key(created_at=created_at)
        definition = self._workflow_definition(flow_code)
        return self._generate_workflow_business_key(definition["workflow_name"], created_at=created_at)

    def _workflow_process_definition_key(self, flow_code: str | None, workflow_name: str | None) -> str:
        normalized_flow_code = str(flow_code or "").strip()
        if normalized_flow_code:
            return normalized_flow_code.lower()
        return self._workflow_name_code(str(workflow_name or "未命名流程")).lower()

    @staticmethod
    def _workflow_deployment_id(process_definition_key: str) -> str:
        return (
            f"dep-{RuntimeManagementStoreWorkflowMixin._workflow_id_slug(process_definition_key, 24)}-"
            f"{RuntimeManagementStoreWorkflowMixin._workflow_id_hash(process_definition_key, 'deployment', length=8)}"
        )

    @staticmethod
    def _workflow_process_definition_id(process_definition_key: str) -> str:
        return (
            f"procdef-{RuntimeManagementStoreWorkflowMixin._workflow_id_slug(process_definition_key, 20)}-v1-"
            f"{RuntimeManagementStoreWorkflowMixin._workflow_id_hash(process_definition_key, 'process-definition', length=8)}"
        )

    @staticmethod
    def _workflow_process_instance_id(process_definition_key: str, business_key: str) -> str:
        return (
            f"procinst-{RuntimeManagementStoreWorkflowMixin._workflow_id_slug(process_definition_key, 16)}-"
            f"{RuntimeManagementStoreWorkflowMixin._workflow_id_slug(business_key, 18)}-"
            f"{RuntimeManagementStoreWorkflowMixin._workflow_id_hash(process_definition_key, business_key, 'process-instance', length=10)}"
        )

    @staticmethod
    def _workflow_task_definition_key(node_key: str | None, current_node: str | None) -> str:
        normalized_node_key = str(node_key or "").strip()
        if normalized_node_key:
            return normalized_node_key
        normalized_node = str(current_node or "").strip()
        return normalized_node or "manual_task"

    @staticmethod
    def _workflow_execution_id(process_instance_id: str, task_definition_key: str) -> str:
        return (
            f"exec-{RuntimeManagementStoreWorkflowMixin._workflow_id_slug(task_definition_key, 18)}-"
            f"{RuntimeManagementStoreWorkflowMixin._workflow_id_hash(process_instance_id, task_definition_key, 'execution', length=10)}"
        )

    def _workflow_candidate_groups(self, flow_code: str | None, node_key: str | None) -> list[str]:
        normalized_flow_code = str(flow_code or "").strip()
        normalized_node_key = str(node_key or "").strip()
        if not normalized_flow_code or not normalized_node_key:
            return []
        node = self._workflow_definition(normalized_flow_code)["nodes"].get(normalized_node_key)
        if not node:
            return []
        return [str(role) for role in node.get("handler_roles", []) if str(role).strip()]

    def _ensure_workflow_engine_metadata(self, task: dict[str, Any]) -> bool:
        process_definition_key = self._workflow_process_definition_key(task.get("flow_code"), task.get("workflow_name"))
        task_definition_key = self._workflow_task_definition_key(task.get("node_key"), task.get("current_node"))
        business_key = str(task.get("business_key") or "")
        process_instance_id = self._workflow_process_instance_id(process_definition_key, business_key or f'TASK-{task.get("id") or "0"}')
        execution_id = self._workflow_execution_id(process_instance_id, task_definition_key)
        metadata_updates = {
            "deployment_id": task.get("deployment_id") or self._workflow_deployment_id(process_definition_key),
            "process_definition_key": process_definition_key,
            "process_definition_id": task.get("process_definition_id") or self._workflow_process_definition_id(process_definition_key),
            "process_definition_version": int(task.get("process_definition_version") or 1),
            "process_instance_id": process_instance_id,
            "execution_id": execution_id,
            "task_definition_key": task_definition_key,
            "candidate_groups": self._workflow_candidate_groups(task.get("flow_code"), task.get("node_key")),
        }
        changed = False
        for key, value in metadata_updates.items():
            if task.get(key) != value:
                task[key] = value
                changed = True
        return changed

    def _workflow_task_index_by_entity(self, flow_code: str, entity_id: int) -> tuple[int, dict[str, Any]] | None:
        for index, item in enumerate(self._list("workflow_tasks")):
            if item.get("flow_code") == flow_code and int(item.get("entity_id") or 0) == entity_id:
                return index, item
        return None

    def _ensure_managed_business_key(self, flow_code: str, item: dict[str, Any], existing_key: str | None = None, created_at: str | None = None) -> tuple[str, bool]:
        candidate_key, business_key_created_at = self._normalize_managed_business_key_candidate(
            flow_code,
            item,
            existing_key=existing_key,
            created_at=created_at,
        )
        business_key = self._workflow_business_key(
            flow_code,
            int(item.get("id") or 0),
            existing_key=candidate_key,
            created_at=business_key_created_at,
        )
        changed = False
        if item.get("business_key") != business_key:
            item["business_key"] = business_key
            changed = True
        if flow_code == "recruitment_application" and item.get("candidate_no") != business_key:
            item["candidate_no"] = business_key
            changed = True
        return business_key, changed

    def _workflow_initial_node_key(self, flow_code: str) -> str:
        return next(iter(self._workflow_definition(flow_code)["nodes"]))

    def _workflow_due_at(self, flow_code: str, node_key: str) -> str:
        definition = self._workflow_definition(flow_code)
        due_days = int(definition["nodes"][node_key].get("due_days", 2))
        return (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d %H:%M:%S")

    def _workflow_handler_display(self, flow_code: str, node_key: str, item: dict[str, Any]) -> str:
        roles = self._workflow_definition(flow_code)["nodes"][node_key]["handler_roles"]
        if roles == ["advisor"] and item.get("advisor_name"):
            return str(item["advisor_name"])
        return " / ".join(ROLE_DISPLAY_NAMES.get(role, role) for role in roles)

    def _workflow_title(self, flow_code: str, item: dict[str, Any]) -> str:
        if flow_code == "recruitment_application":
            return f'{item["student_name"]}报名审核'
        if flow_code == "scientific_report":
            return f'{item["student_name"]}科研报告审阅'
        if flow_code == "outbound_study":
            return f'{item["student_name"]}外出研修申请'
        if flow_code == "thesis":
            return f'{item["student_name"]}授位审批'
        return str(item.get("student_name") or item.get("title") or "流程任务")

    def _workflow_form_summary(self, flow_code: str, item: dict[str, Any]) -> str:
        if flow_code == "recruitment_application":
            return f'业务编号：{item.get("business_key") or item.get("candidate_no") or "-"}；研究方向：{item["intended_field"]}；材料状态：{item["material_status"]}'
        if flow_code == "scientific_report":
            reviewer_name = item.get("reviewer_name") or "待分配"
            return f'周期：{item["period_label"]}；审阅人：{reviewer_name}'
        if flow_code == "outbound_study":
            return f'研修地点：{item["destination"]}；起止：{item["start_date"]} 至 {item["end_date"]}'
        if flow_code == "thesis":
            return f'论文题目：{item["title"]}；盲审状态：{item["blind_review_status"]}'
        return str(item.get("title") or item.get("student_name") or "")

    def _workflow_applicant_name(self, flow_code: str, item: dict[str, Any]) -> str:
        del flow_code
        return str(item.get("student_name") or item.get("full_name") or item.get("business_key") or item.get("candidate_no") or "未知申请人")

    def _principal_summary(self, principal: Any) -> dict[str, Any]:
        if hasattr(principal, "model_dump"):
            payload = principal.model_dump()
        elif isinstance(principal, dict):
            payload = principal
        else:
            payload = {
                "username": getattr(principal, "username", "system"),
                "full_name": getattr(principal, "full_name", getattr(principal, "username", "system")),
                "roles": list(getattr(principal, "roles", [])),
            }
        return {
            "username": payload.get("username", "system"),
            "full_name": payload.get("full_name", payload.get("username", "system")),
            "roles": list(payload.get("roles", [])),
        }

    def _workflow_action_options(self, task: dict[str, Any], principal_roles: list[str] | None = None) -> list[dict[str, str]]:
        flow_code = task.get("flow_code")
        node_key = task.get("node_key")
        if not flow_code or not node_key:
            return []
        node = self._workflow_definition(flow_code)["nodes"].get(node_key)
        if not node:
            return []
        if principal_roles and not set(node["handler_roles"]).intersection(principal_roles):
            return []
        return [{"action": action_code, "label": action_config["label"]} for action_code, action_config in node["actions"].items()]

    def _fallback_workflow_due_at(self, task: dict[str, Any]) -> str:
        due_at = task.get("due_at")
        if due_at:
            return str(due_at)
        created_at = str(task.get("created_at") or "").strip()
        if created_at:
            return created_at
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _build_workflow_task_record(self, task: dict[str, Any], principal_roles: list[str] | None = None) -> WorkflowTaskRecord:
        return WorkflowTaskRecord(
            id=int(task["id"]),
            workflow_name=str(task.get("workflow_name") or "未命名流程"),
            business_module=str(task.get("business_module") or "流程中心"),
            business_key=str(task.get("business_key") or f'TASK-{task["id"]}'),
            title=str(task.get("title") or "未命名任务"),
            applicant_name=str(task.get("applicant_name") or "未知申请人"),
            current_handler=str(task.get("current_handler") or "待分派"),
            current_node=str(task.get("current_node") or "待处理"),
            priority=str(task.get("priority") or "中"),
            status=str(task.get("status") or "待处理"),
            created_at=str(task.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            due_at=self._fallback_workflow_due_at(task),
            form_summary=str(task.get("form_summary") or ""),
            latest_comment=task.get("latest_comment"),
            available_actions=self._workflow_action_options(task, principal_roles=principal_roles),
            process_definition_key=task.get("process_definition_key"),
            process_definition_id=task.get("process_definition_id"),
            process_instance_id=task.get("process_instance_id"),
            execution_id=task.get("execution_id"),
            task_definition_key=task.get("task_definition_key"),
        )

    def _build_workflow_history_record(self, entry: dict[str, Any]) -> dict[str, Any]:
        return {
            "operated_at": entry["operated_at"],
            "operator_username": entry["operator_username"],
            "operator_full_name": entry["operator_full_name"],
            "action": entry["action"],
            "action_label": entry["action_label"],
            "from_node": entry["from_node"],
            "to_node": entry.get("to_node"),
            "result_status": entry["result_status"],
            "comment": entry.get("comment"),
        }

    def _workflow_task_index_by_business_key(self, business_key: str) -> tuple[int, dict[str, Any]] | None:
        for index, item in enumerate(self._list("workflow_tasks")):
            if item.get("business_key") == business_key:
                return index, item
        return None

    def _normalize_legacy_workflow_tasks(self) -> bool:
        changed = False
        for index, task in enumerate(self._list("workflow_tasks")):
            updated = dict(task)
            row_changed = False
            defaults = {
                "workflow_name": updated.get("workflow_name") or "未命名流程",
                "business_module": updated.get("business_module") or "流程中心",
                "business_key": updated.get("business_key") or self._generate_workflow_business_key(
                    str(updated.get("workflow_name") or "未命名流程"),
                    created_at=str(updated.get("created_at") or ""),
                ),
                "title": updated.get("title") or "未命名任务",
                "applicant_name": updated.get("applicant_name") or "未知申请人",
                "current_handler": updated.get("current_handler") or "待分派",
                "current_node": updated.get("current_node") or "待处理",
                "priority": updated.get("priority") or "中",
                "status": updated.get("status") or "待处理",
                "created_at": updated.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "due_at": self._fallback_workflow_due_at(updated),
                "form_summary": updated.get("form_summary") or "",
                "history": updated.get("history") or [],
            }
            for key, value in defaults.items():
                if updated.get(key) != value:
                    updated[key] = value
                    row_changed = True
            if self._ensure_workflow_engine_metadata(updated):
                row_changed = True
            if row_changed:
                self._list("workflow_tasks")[index] = updated
                changed = True
        return changed

    def _workflow_initial_item(self, flow_code: str, item: dict[str, Any]) -> dict[str, Any]:
        definition = self._workflow_definition(flow_code)
        initial_item = {**item, **definition.get("initial_field_values", {})}
        self._ensure_managed_business_key(flow_code, initial_item)
        return initial_item

    def _ensure_managed_status_fields_unchanged(self, dataset: str, current: dict[str, Any], incoming: dict[str, Any]) -> None:
        flow_code = WORKFLOW_DATASET_TO_FLOW.get(dataset)
        if not flow_code:
            return
        definition = self._workflow_definition(flow_code)
        changed_fields = [field for field in definition["managed_fields"] if current.get(field) != incoming.get(field)]
        if changed_fields:
            raise ValueError(f'字段 {", ".join(changed_fields)} 为流程托管状态，请通过审批流程活动变更')

    def _infer_workflow_runtime(self, flow_code: str, item: dict[str, Any]) -> dict[str, Any]:
        if flow_code == "recruitment_application":
            mapping = {
                "报名已提交": ("qualification_review", "待处理"),
                "资格审核通过": ("qualification_passed", "处理中"),
                "材料评分中": ("interview_arrangement", "处理中"),
                "面试待安排": ("admission_decision", "处理中"),
                "面试完成": ("admission_confirmation", "处理中"),
                "预录取": (None, "已通过"),
                "同意录取": (None, "已通过"),
                "驳回重填": (None, "已驳回"),
                "不录取": (None, "已驳回"),
            }
            node_key, task_status = mapping.get(item.get("application_status"), ("qualification_review", "待处理"))
            return {"node_key": node_key, "task_status": task_status}
        if flow_code == "scientific_report":
            if item.get("report_status") == "已通过":
                return {"node_key": None, "task_status": "已通过"}
            if item.get("report_status") == "退回修改":
                return {"node_key": None, "task_status": "已驳回"}
            return {"node_key": "advisor_review", "task_status": "待处理"}
        if flow_code == "outbound_study":
            if item.get("approval_status") in {"已批准", "研修中", "已结束"}:
                return {"node_key": None, "task_status": "已通过"}
            if item.get("approval_status") == "已驳回":
                return {"node_key": None, "task_status": "已驳回"}
            return {"node_key": "advisor_review", "task_status": "待处理"}
        if flow_code == "thesis":
            if item.get("degree_status") == "待正式答辩" or item.get("blind_review_status") == "已通过":
                return {"node_key": None, "task_status": "已通过"}
            if item.get("degree_status") == "未授位" or item.get("blind_review_status") == "未通过" or item.get("thesis_status") == "退回修改":
                return {"node_key": None, "task_status": "已驳回"}
            if item.get("degree_status") == "授位审批中" or item.get("blind_review_status") == "进行中":
                return {"node_key": "secretary_review", "task_status": "处理中"}
            return {"node_key": "advisor_precheck", "task_status": "待处理"}
        raise ValueError(f"Unsupported workflow flow: {flow_code}")

    def _sync_managed_workflow_task(self, flow_code: str, item: dict[str, Any], existing_task: dict[str, Any] | None = None) -> tuple[dict[str, Any], bool]:
        definition = self._workflow_definition(flow_code)
        runtime = self._infer_workflow_runtime(flow_code, item)
        node_key = runtime["node_key"]
        task_status = runtime["task_status"]
        task = dict(existing_task or {})
        previous_node_key = task.get("node_key")
        changed = False
        if not existing_task:
            task["id"] = self._next_id("workflow_tasks")
            task["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["history"] = []
            changed = True
        if "history" not in task:
            task["history"] = []
            changed = True
        item_business_key, item_key_changed = self._ensure_managed_business_key(
            flow_code,
            item,
            existing_key=task.get("business_key"),
            created_at=str(task.get("created_at") or ""),
        )
        if item_key_changed:
            changed = True
        task_updates = {
            "workflow_name": definition["workflow_name"],
            "business_module": definition["business_module"],
            "business_key": item_business_key,
            "title": self._workflow_title(flow_code, item),
            "applicant_name": self._workflow_applicant_name(flow_code, item),
            "priority": task.get("priority") or "中",
            "status": task_status,
            "current_node": definition["nodes"][node_key]["label"] if node_key else "流程结束",
            "current_handler": self._workflow_handler_display(flow_code, node_key, item) if node_key else "流程结束",
            "due_at": task.get("due_at") if not node_key else (self._workflow_due_at(flow_code, node_key) if not task.get("due_at") or not previous_node_key else task.get("due_at")),
            "form_summary": self._workflow_form_summary(flow_code, item),
            "latest_comment": task.get("latest_comment"),
            "flow_code": flow_code,
            "business_dataset": definition["business_dataset"],
            "entity_id": int(item["id"]),
            "node_key": node_key,
        }
        for key, value in task_updates.items():
            if task.get(key) != value:
                task[key] = value
                changed = True
        if self._ensure_workflow_engine_metadata(task):
            changed = True
        return task, changed

    def _migrate_workflow_runtime(self) -> bool:
        changed = False
        for flow_code, definition in MANAGED_WORKFLOW_DEFINITIONS.items():
            for item in self._list(definition["business_dataset"]):
                existing_business_key = str(item.get("business_key") or item.get("candidate_no") or "").strip() or None
                if existing_business_key:
                    _, item_changed = self._ensure_managed_business_key(flow_code, item, existing_key=existing_business_key)
                    if item_changed:
                        changed = True
                located = None
                if existing_business_key:
                    located = self._workflow_task_index_by_business_key(existing_business_key)
                if item.get("business_key"):
                    located = self._workflow_task_index_by_business_key(str(item["business_key"]))
                if located is None:
                    located = self._workflow_task_index_by_entity(flow_code, int(item["id"]))
                existing_task = located[1] if located else None
                task, task_changed = self._sync_managed_workflow_task(flow_code, item, existing_task=existing_task)
                if located is None:
                    self._list("workflow_tasks").insert(0, task)
                    changed = True
                elif task_changed:
                    self._list("workflow_tasks")[located[0]] = task
                    changed = True
        return changed

    def _start_managed_workflow(self, flow_code: str, item: dict[str, Any], operator_username: str) -> None:
        task, _ = self._sync_managed_workflow_task(flow_code, item)
        task["latest_comment"] = "流程已发起，等待节点处理。"
        task["history"] = [
            {
                "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operator_username": operator_username,
                "operator_full_name": operator_username,
                "action": "start",
                "action_label": "发起流程",
                "from_node": "开始",
                "to_node": task["current_node"],
                "result_status": task["status"],
                "comment": task["latest_comment"],
            }
        ]
        self._list("workflow_tasks").insert(0, task)

    def _update_runtime_managed_entity(self, dataset_name: str, entity_id: int, payload: dict[str, Any]) -> None:
        if dataset_name == "recruitment_applications":
            self._postgres_store.sync_recruitment_application_status(entity_id, payload)
            return
        if dataset_name == "scientific_reports":
            self._postgres_store.sync_scientific_report(payload)
            return
        if dataset_name == "outbound_studies":
            self._postgres_store.sync_outbound_study(payload)
            return
        if dataset_name == "theses":
            self._postgres_store.sync_thesis(payload)
            return
        raise ValueError(f"Unsupported managed dataset: {dataset_name}")

    def _persist_portal_student_change(
        self,
        student: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        update_student_counter: bool = False,
    ) -> None:
        counters = {"operation_logs": int(self._counters.get("operation_logs", 0))}
        if update_student_counter:
            counters["portal_students"] = int(self._counters.get("portal_students", 0))
        self._postgres_store.sync_portal_student(student, operation_log, counters=counters)

    def _persist_portal_application_submission(
        self,
        student: dict[str, Any],
        application: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        workflow_task: dict[str, Any] | None = None,
        created_application: bool = False,
        created_workflow_task: bool = False,
    ) -> None:
        counters = {"operation_logs": int(self._counters.get("operation_logs", 0))}
        if created_application:
            counters["recruitment_applications"] = int(self._counters.get("recruitment_applications", 0))
        if created_workflow_task:
            counters["workflow_tasks"] = int(self._counters.get("workflow_tasks", 0))
        self._postgres_store.sync_portal_application_submission(
            student,
            application,
            operation_log,
            workflow_task=workflow_task,
            counters=counters,
        )

    def _persist_student_change(
        self,
        student: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        created: bool = False,
    ) -> None:
        counters = {
            "students": int(self._counters.get("students", 0)),
            "operation_logs": int(self._counters.get("operation_logs", 0)),
        }
        if created:
            self._postgres_store.sync_created_student(student, operation_log=operation_log, counters=counters)
            return
        self._postgres_store.sync_updated_student(student, operation_log=operation_log, counters=counters)

    def _persist_recruitment_application_change(
        self,
        application: dict[str, Any],
        operation_log: dict[str, Any],
        *,
        workflow_task: dict[str, Any] | None = None,
        portal_student: dict[str, Any] | None = None,
        update_application_counter: bool = False,
        update_workflow_counter: bool = False,
    ) -> None:
        del application, operation_log, workflow_task, portal_student, update_application_counter, update_workflow_counter
        # Recruitment application edits affect both the formal relational tables
        # and the runtime mirror. Persist the full state so refreshes read back the
        # same data that was just saved.
        self._save()

    def get_workflow_task_detail(self, task_id: int, principal: Any) -> dict[str, Any]:
        principal_summary = self._principal_summary(principal)
        try:
            task = self._postgres_store.get_workflow_task_snapshot(task_id)
            if task is not None:
                return {
                    "task": self._build_workflow_task_record(task, principal_roles=principal_summary["roles"]),
                    "history": [self._build_workflow_history_record(item) for item in task.get("history", [])],
                }
        except Exception as exc:
            logger.warning("Load workflow task detail from PostgreSQL failed, fallback to in-memory state: %s", exc)
        _, task = self._find_required("workflow_tasks", task_id)
        return {
            "task": self._build_workflow_task_record(task, principal_roles=principal_summary["roles"]),
            "history": [self._build_workflow_history_record(item) for item in task.get("history", [])],
        }

    def execute_workflow_action(self, task_id: int, action: str, comment: str | None, principal: Any) -> dict[str, Any]:
        principal_summary = self._principal_summary(principal)
        notification_payload: dict[str, str] | None = None
        reset_portal_student: dict[str, Any] | None = None
        sync_student_master = False
        with self._lock:
            index, task = self._find_required("workflow_tasks", task_id)
            flow_code = task.get("flow_code")
            node_key = task.get("node_key")
            if not flow_code or not node_key:
                latest_history = task.get("history")[-1] if task.get("history") else None
                if (
                    task.get("status") in FINAL_WORKFLOW_STATUSES
                    and isinstance(latest_history, dict)
                    and str(latest_history.get("action") or "").strip() == str(action or "").strip()
                ):
                    return self._workflow_action_result(task, principal_roles=principal_summary["roles"])
                raise ValueError("当前任务不是流程驱动任务，不能执行流程动作")
            definition = self._workflow_definition(flow_code)
            node = definition["nodes"][node_key]
            if not set(node["handler_roles"]).intersection(principal_summary["roles"]):
                raise PermissionError("当前角色无权执行该流程活动")
            action_definition = node["actions"].get(action)
            if not action_definition:
                raise ValueError("当前节点不支持该流程动作")
            entity_index, entity = self._find_required(definition["business_dataset"], int(task["entity_id"]))
            updated_entity = {**entity, **action_definition.get("field_updates", {})}
            self._list(definition["business_dataset"])[entity_index] = updated_entity
            if flow_code == "recruitment_application" and str(updated_entity.get("application_status") or "").strip() == "驳回重填":
                reset_portal_student = self._reset_portal_student_submission_for_resubmission(updated_entity)

            next_node = action_definition.get("next_node")
            updated_task = dict(task)
            updated_task["status"] = action_definition["task_status"]
            updated_task["latest_comment"] = comment or action_definition["label"]
            updated_task["form_summary"] = self._workflow_form_summary(flow_code, updated_entity)
            updated_task["node_key"] = next_node
            updated_task["current_node"] = definition["nodes"][next_node]["label"] if next_node else "流程结束"
            updated_task["current_handler"] = self._workflow_handler_display(flow_code, next_node, updated_entity) if next_node else "流程结束"
            updated_task["due_at"] = self._workflow_due_at(flow_code, next_node) if next_node else updated_task["due_at"]
            updated_task.setdefault("history", []).append(
                {
                    "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "operator_username": principal_summary["username"],
                    "operator_full_name": principal_summary["full_name"],
                    "action": action,
                    "action_label": action_definition["label"],
                    "from_node": node["label"],
                    "to_node": definition["nodes"][next_node]["label"] if next_node else "流程结束",
                    "result_status": updated_task["status"],
                    "comment": updated_task["latest_comment"],
                }
            )
            self._ensure_workflow_engine_metadata(updated_task)
            self._list("workflow_tasks")[index] = updated_task
            operation_log = self._record_operation(
                "流程中心",
                definition["business_entity"],
                task["business_key"],
                action_definition["label"],
                f'{principal_summary["full_name"]} 执行 {definition["workflow_name"]} - {action_definition["label"]}',
                operator_username=principal_summary["username"],
            )
            try:
                self._update_runtime_managed_entity(definition["business_dataset"], int(task["entity_id"]), updated_entity)
                self._postgres_store.sync_workflow_task(
                    updated_task,
                    operation_log,
                    counters={"operation_logs": int(self._counters.get("operation_logs", 0))},
                )
                if reset_portal_student is not None:
                    self._persist_portal_student_change(reset_portal_student, operation_log)
            except Exception:
                self._save()
            if flow_code == "recruitment_application":
                notification_payload = self._build_recruitment_email_notification(updated_entity)
                sync_student_master = str(updated_entity.get("application_status") or "").strip() in ADMITTED_RECRUITMENT_APPLICATION_STATUSES
            result = self._workflow_action_result(updated_task, principal_roles=principal_summary["roles"])
            if sync_student_master:
                self._sync_student_master_from_recruitment_application(updated_entity)

        if notification_payload is not None and self._email_service.enabled():
            self._email_service.send_recruitment_status_update(**notification_payload)
        return result

    def _reset_portal_student_submission_for_resubmission(self, application: dict[str, Any]) -> dict[str, Any] | None:
        portal_student_id = int(application.get("portal_student_id") or 0)
        if portal_student_id <= 0:
            return None
        _, student = self._find_required("portal_students", portal_student_id)
        student["submitted_at"] = None
        student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draft = student.get("application_draft")
        if isinstance(draft, dict):
            draft["submitted_at"] = None
        return student

    def _build_recruitment_email_notification(self, application: dict[str, Any]) -> dict[str, str] | None:
        status = str(application.get("application_status") or "").strip()
        if status not in {"驳回重填", "资格审核通过", "预录取", "同意录取", "不录取"}:
            return None

        email = str(application.get("email") or "").strip()
        if not email:
            return None

        plan_name = ""
        plan_id = application.get("plan_id")
        if plan_id is not None:
            matched_plan = next((item for item in self._list("recruitment_plans") if int(item.get("id") or 0) == int(plan_id)), None)
            if matched_plan is not None:
                plan_name = str(matched_plan.get("plan_name") or "")

        return {
            "student_name": str(application.get("student_name") or "同学"),
            "email": email,
            "business_key": str(application.get("business_key") or ""),
            "application_status": status,
            "plan_name": plan_name,
        }

    def get_workflow_options(self) -> WorkflowOptionsResponse:
        applicants = {
            *[item.get("applicant_name") for item in self._list("workflow_tasks") if item.get("applicant_name")],
            *[item.get("full_name") for item in self._list("students") if item.get("full_name")],
        }
        handlers = {
            *[item.get("current_handler") for item in self._list("workflow_tasks") if item.get("current_handler")],
            *self._advisor_name_values(),
            *self._system_user_name_values(),
        }
        return WorkflowOptionsResponse(
            workflow_name_options=self._select_options_from_values([item.get("workflow_name") for item in self._list("workflow_tasks")]),
            business_module_options=self._select_options_from_values([item.get("business_module") for item in self._list("workflow_tasks")]),
            applicant_options=self._select_options_from_values(applicants),
            handler_options=self._select_options_from_values(handlers),
            current_node_options=self._select_options_from_values([item.get("current_node") for item in self._list("workflow_tasks")]),
            priority_options=self._dict_options("workflow_priority"),
            status_options=self._dict_options("workflow_status"),
        )

    def get_workflow_tasks(
        self,
        status: str | None = None,
        module: str | None = None,
        keyword: str | None = None,
        page: int = 1,
        page_size: int = 10,
        principal: Any | None = None,
    ) -> WorkflowTaskListResponse:
        principal_summary = self._principal_summary(principal or {"username": "system", "full_name": "system", "roles": []})
        try:
            items, total = self._postgres_store.list_workflow_tasks_page(
                status=status,
                module=module,
                keyword=keyword,
                page=page,
                page_size=page_size,
            )
            records = [self._build_workflow_task_record(item, principal_roles=principal_summary["roles"]) for item in items]
            return WorkflowTaskListResponse(items=records, total=total, page=page, page_size=page_size)
        except Exception as exc:
            logger.warning("Query workflow tasks from PostgreSQL with pagination failed, fallback to in-memory pagination: %s", exc)

        items = list(self._list("workflow_tasks"))
        if status:
            items = [item for item in items if item["status"] == status]
        if module:
            items = [item for item in items if item["business_module"] == module]
        if keyword:
            items = [item for item in items if self._matches_keyword(item["workflow_name"], item["business_key"], item["title"], item["applicant_name"], item["current_handler"], keyword=keyword)]
        records = [self._build_workflow_task_record(item, principal_roles=principal_summary["roles"]) for item in items]
        paged_items, total = self._paginate_items(records, page=page, page_size=page_size)
        return WorkflowTaskListResponse(items=paged_items, total=total, page=page, page_size=page_size)

    def create_workflow_task(self, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            item = payload.model_dump()
            item["id"] = self._next_id("workflow_tasks")
            item["created_at"] = item.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["business_key"] = self._generate_workflow_business_key(item.get("workflow_name") or "未命名流程", created_at=item["created_at"])
            self._ensure_workflow_engine_metadata(item)
            self._list("workflow_tasks").insert(0, item)
            operation_log = self._record_operation("审批中心", "审批任务", str(item["id"]), "新增", f'新增审批任务 {item["title"]}')
            try:
                self._postgres_store.sync_workflow_task(
                    item,
                    operation_log,
                    counters={
                        "workflow_tasks": int(self._counters.get("workflow_tasks", 0)),
                        "operation_logs": int(self._counters.get("operation_logs", 0)),
                    },
                )
            except Exception:
                self._save()
            return WorkflowTaskRecord(**item)

    def update_workflow_task(self, task_id: int, payload: WorkflowTaskUpsert) -> WorkflowTaskRecord:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            if item.get("flow_code"):
                raise ValueError("流程驱动任务不允许手工编辑，请通过流程动作推进")
            updated = {**item, **payload.model_dump(), "id": task_id, "business_key": item.get("business_key")}
            self._ensure_workflow_engine_metadata(updated)
            self._list("workflow_tasks")[index] = updated
            operation_log = self._record_operation("审批中心", "审批任务", str(task_id), "编辑", f'更新审批任务 {updated["title"]}')
            try:
                self._postgres_store.sync_workflow_task(updated, operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()
            return WorkflowTaskRecord(**updated)

    def delete_workflow_task(self, task_id: int) -> None:
        with self._lock:
            index, item = self._find_required("workflow_tasks", task_id)
            if item.get("flow_code"):
                raise ValueError("流程驱动任务不允许手工删除")
            self._list("workflow_tasks").pop(index)
            operation_log = self._record_operation("审批中心", "审批任务", str(task_id), "删除", f'删除审批任务 {item["title"]}')
            try:
                self._postgres_store.delete_workflow_task(int(task_id), item.get("process_instance_id"))
                self._postgres_store.sync_operation_log(operation_log, counters={"operation_logs": int(self._counters.get("operation_logs", 0))})
            except Exception:
                self._save()

    def get_workflow_stats(self) -> WorkflowStats:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = self._list("workflow_tasks")
        overdue_total = len([item for item in items if item["status"] in {"待处理", "处理中"} and item["due_at"] < now])
        return WorkflowStats(
            todo_total=len([item for item in items if item["status"] == "待处理"]),
            in_progress_total=len([item for item in items if item["status"] == "处理中"]),
            approved_total=len([item for item in items if item["status"] == "已通过"]),
            rejected_total=len([item for item in items if item["status"] == "已驳回"]),
            overdue_total=overdue_total,
        )
