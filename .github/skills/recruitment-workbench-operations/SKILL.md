---
name: recruitment-workbench-operations
description: 'Use when implementing or changing recruitment plans, recruitment applications, qualification review flow, interview arrangement, admission decision, or recruitment workbench pages and APIs.'
argument-hint: 'Describe the recruitment feature, affected entities, fields, workflow steps, and UI expectations'
user-invocable: true
disable-model-invocation: false
---

# Recruitment Workbench Operations

## When to Use
- 调整招生计划、招生申请、报名材料、评分准备、面试安排、录取决策逻辑。
- 新增招生字段、筛选条件、统计口径、工作台表格列或详情信息。
- 修复招生申请与审批任务之间的状态不一致问题。
- 维护招生工作台页面、接口与后端数据结构。

## Core Files
- `backend/app/schemas/recruitment.py`
- `backend/app/api/v1/recruitment.py`
- `backend/app/services/management_service.py`
- `frontend/src/views/recruitment/RecruitmentWorkbenchView.vue`
- `frontend/src/api/recruitment.ts`
- `frontend/src/components/table/TableRowActions.vue`

## Domain Constraints
- 报名申请属于 workflow 托管业务对象时，`application_status` 不能再被普通编辑路径直接覆盖。
- `business_key` 与历史兼容字段（如 `candidate_no`）必须保持一致或兼容映射。
- 招生计划与申请列表通常都需要保留分页、筛选与统计联动。

## Procedure
1. 明确本次变更作用于招生计划还是报名申请。
2. 如果是报名申请状态或审批步骤，先按 workflow 技能处理流程定义，再回到 recruitment 领域补充字段与页面。
3. 修改 schema、service、API，再同步前端类型与表单。
4. 若改动列表列或详情展示，检查 `business_key`、申请状态、审核人、分数等关键字段是否一致。
5. 最后回归申请创建、列表检索、详情查看与审批动作联动。

## Validation Checklist
- 招生计划增删改查正常。
- 报名申请 `business_key` 正常生成和显示。
- 招生申请状态与 workflow 任务状态一致。
- 详情页和清单页字段命名一致。
- 表格筛选、分页、操作按钮可用。
