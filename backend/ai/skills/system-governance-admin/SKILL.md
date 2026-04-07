---
name: system-governance-admin
description: 'Use when changing system users, roles, dictionaries, audit policies, integration links, operation logs, sync logs, or the governance/admin pages and APIs.'
argument-hint: 'Describe the governance module, records affected, permission rules, and UI/API changes needed'
user-invocable: true
disable-model-invocation: false
---

# System Governance Admin

## When to Use
- 维护系统用户、角色权限、字典、审计策略、集成链路、操作日志、同步日志。
- 调整后台治理模块的字段、筛选项、权限目录、状态标签与列表行为。
- 修复治理模块页面与后端接口不一致问题。
- 新增基础配置类能力时，需要同时考虑字典、权限和审计留痕。

## Core Files
- `backend/app/schemas/system.py`
- `backend/app/api/v1/system.py`
- `backend/app/services/management_service.py`
- `frontend/src/views/system/SystemView.vue`
- `frontend/src/views/system/DictView.vue`
- `frontend/src/api/system.ts`
- `frontend/src/utils/dictTag.ts`

## Domain Constraints
- 用户、角色、权限改动要同步考虑登录态、菜单访问、操作权限与审计记录。
- 字典变更如果影响多个业务页面，应检查前端下拉选项与标签颜色映射。
- 治理类页面通常是基础设施，不应破坏已有业务模块依赖。

## Procedure
1. 确定变更作用于用户、角色、字典、审计、集成链路还是日志。
2. 在 schema 与 service 中更新字段、选项、状态与分页响应。
3. 如涉及权限目录，检查认证与菜单访问链路。
4. 同步更新 `SystemView.vue`、`DictView.vue` 与前端 API 类型。
5. 回归基础增删改查、筛选、标签展示和日志记录。

## Validation Checklist
- 用户、角色、字典等基础治理页面可正常访问。
- 字典选项与颜色标签映射正确。
- 角色权限变更不会破坏既有页面访问。
- 审计策略、操作日志、同步日志展示正常。
