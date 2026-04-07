---
name: workflow-approval-maintenance
description: 'Use when modifying, debugging, or extending workflow-driven approvals, role-based actions, business_key generation, workflow task detail/actions, or Flowable-compatible runtime/history sync for recruitment, scientific reports, outbound studies, and theses.'
argument-hint: 'Describe the business object, required workflow change, roles, actions, and expected final states'
user-invocable: true
disable-model-invocation: false
---

# Workflow Approval Maintenance

## When to Use
- 调整招生申请、科研报告、外出研修、论文主档的审批流。
- 新增或修改流程节点、动作、角色处理人、状态回写规则。
- 排查 workflow task 列表、详情、动作执行、历史轨迹问题。
- 维护 Flowable 风格兼容表、运行态同步、business_key 规则。
- 验证“不能通过普通新增/修改直接改托管状态”的约束是否仍然成立。

## Core Files
- `backend/app/services/management_service.py`
- `backend/app/services/postgres_state_store.py`
- `backend/app/api/v1/workflow.py`
- `backend/app/schemas/workflow.py`
- `backend/app/services/dashboard_service.py`
- `backend/scripts/simulate_managed_workflows.py`
- `backend/sql/017_workflow_flowable_schema.sql`
- `frontend/src/views/workflow/WorkflowCenterView.vue`
- `frontend/src/api/workflow.ts`

## Working Rules
1. 先确认目标对象是否属于托管流程对象：`recruitment_application`、`scientific_report`、`outbound_study`、`thesis`。
2. 所有托管状态必须由流程动作推进，不能通过普通 update 接口直接改写状态字段。
3. 修改流程时同时检查：节点标签、动作标签、角色权限、状态字段回写、任务详情字段、历史记录。
4. 如果流程元数据变更影响 PostgreSQL 兼容层，必须同步检查 `postgres_state_store.py` 与 SQL 初始化脚本。
5. 若涉及列表展示，确认前端只展示当前角色可执行的 `available_actions`。

## Procedure
1. 在 `management_service.py` 中定位对应流程定义与受托管字段。
2. 修改节点、动作、状态映射、business_key 或元数据生成逻辑。
3. 若返回结构变化，同步更新 workflow schema、API 与前端类型。
4. 若运行态或历史态落库字段变化，同步更新 PostgreSQL 兼容层与 SQL 脚本。
5. 用 `backend/scripts/simulate_managed_workflows.py` 回归通过/驳回分支。
6. 若涉及审批中心 UI，再检查详情弹窗、动作按钮、处理历史是否仍可用。

## Validation Checklist
- 托管对象状态只能由流程动作改变。
- 列表、详情、动作、历史接口字段一致。
- 角色越权操作会被拒绝。
- business_key 不为空且在任务与业务对象之间一致。
- Flowable 风格兼容表同步正常。
- 模拟脚本场景通过。
