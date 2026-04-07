---
name: student-master-data-and-teams
description: 'Use when changing student master data, student lifecycle records, teams, advisor mapping, student status boards, or the student/team management pages and APIs.'
argument-hint: 'Describe the student or team change, data fields, lifecycle behavior, and any advisor/team impacts'
user-invocable: true
disable-model-invocation: false
---

# Student Master Data And Teams

## When to Use
- 调整学生主档、学生状态、团队信息、导师归属、团队成员统计。
- 新增学生字段、团队字段、查询筛选条件或导入展示项。
- 修复学生主数据与团队管理页面字段不一致问题。
- 扩展学生生命周期看板、状态卡片或统计口径。

## Core Files
- `backend/app/schemas/student.py`
- `backend/app/api/v1/students.py`
- `backend/app/services/management_service.py`
- `frontend/src/views/students/StudentsView.vue`
- `frontend/src/api/students.ts`
- `frontend/src/api/common.ts`

## Domain Constraints
- 学生主档应作为相对稳定的主数据源，不要把审批流托管状态直接混入普通主档编辑。
- 团队、导师、学生之间的归属关系需要同时考虑列表展示与统计摘要。
- 如果新增字段影响仪表盘或筛选条件，应同步检查 dashboard 聚合逻辑。

## Procedure
1. 确认变更目标是学生主档、团队信息还是生命周期状态板。
2. 在 schema 中补齐字段定义与分页响应类型。
3. 在 `management_service.py` 中同步增删改查、选项数据与统计口径。
4. 修改学生/团队页面表单、列表列、筛选项和详情展示。
5. 如字段参与其他业务模块联动，补查 recruitment、training、dashboard 的使用点。

## Validation Checklist
- 学生主档与团队页面都能正常查询和保存。
- 导师归属、团队人数、状态标签等聚合字段正确。
- 新字段在表单、列表、接口返回中保持一致。
- 分页、筛选、统计卡片未受破坏。
