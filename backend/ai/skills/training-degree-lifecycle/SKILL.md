---
name: training-degree-lifecycle
description: 'Use when changing training plans, scientific reports, outbound studies, theses, thesis reviews, degree workbench logic, or the lifecycle rules that connect training and degree stages.'
argument-hint: 'Describe the training or degree object, target fields, approval steps, and expected lifecycle behavior'
user-invocable: true
disable-model-invocation: false
---

# Training Degree Lifecycle

## When to Use
- 调整培养方案、科研报告、外出研修、论文主档、盲审意见、授位状态。
- 扩展培养与学位阶段的字段、列表、状态规则、统计摘要。
- 处理科研报告、外出研修、论文主档与审批流之间的联动问题。
- 维护训练模块与学位模块的前后端接口一致性。

## Core Files
- `backend/app/schemas/training.py`
- `backend/app/api/v1/training.py`
- `backend/app/api/v1/degree.py`
- `backend/app/services/management_service.py`
- `frontend/src/views/training/TrainingView.vue`
- `frontend/src/views/degree/DegreeView.vue`
- `frontend/src/api/training.ts`
- `frontend/src/api/degree.ts`

## Domain Constraints
- 科研报告、外出研修、论文主档都与 workflow 托管状态有关，改状态前先确认是否应通过审批动作推进。
- 学位模块当前只部分覆盖原始需求，若新增流程要明确是补“论文阶段”还是补“毕业离校阶段”。
- 训练与学位相关列表普遍带分页、统计与状态标签，字段变更要同步前后端。

## Procedure
1. 判定目标属于培养计划、科研报告、外出研修、论文主档还是盲审意见。
2. 若涉及托管状态，优先检查 workflow 定义；若是纯业务字段，再修改 schema、service、API。
3. 同步更新 `TrainingView.vue`、`DegreeView.vue` 及对应 API 类型。
4. 检查筛选条件、统计卡片、操作列和详情编辑路径。
5. 对科研报告、外出研修、论文主档优先做流程回归或状态回归验证。

## Validation Checklist
- 培养方案、科研报告、外出研修、论文主档列表均可正常加载。
- 状态字段与审批结果保持一致。
- 盲审/评审相关字段不会被错误覆盖。
- 页面分页、筛选、表单与详情联动正常。
