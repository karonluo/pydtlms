---
name: backend-management-dialog-style
description: 'Use when standardizing dialog, confirmation, notice, and empty-state overlays across backend/admin modules, especially when aligning with the student registration dialog style.'
argument-hint: 'Describe the backend module, dialog type, whether it is a form, confirmation, or notice box, and the target reusable shell/style'
user-invocable: true
disable-model-invocation: false
---

# Backend Management Dialog Style

## When to Use
- 统一后台管理模块中的弹窗、确认框、提醒框与结果框样式。
- 让系统、招生、学生、培养、工作流等后台页面对话框对齐注册学生页的视觉结构。
- 抽取可复用的对话框壳、摘要区、提示区、底部按钮区和表单网格样式。
- 避免在各个页面里分别写一套 `el-dialog` 外壳、间距和摘要样式。

## Core Files
- `frontend/src/style.css`
- `frontend/src/views/students/StudentsView.vue`
- `frontend/src/views/system/SystemView.vue`
- `frontend/src/views/recruitment/NewsManagementView.vue`
- `frontend/src/views/workflow/WorkflowCenterView.vue`
- `frontend/src/views/training/TrainingView.vue`
- `frontend/src/views/degree/DegreeView.vue`

## Style Rules
- 优先复用注册学生页已经验证过的对话框结构与层级，而不是临时堆砌 `alert`、`confirm` 或 `popover`。
- 需要确认类操作时，优先使用带摘要和提示的自定义对话框壳，而不是裸消息框。
- 表单型对话框统一使用公共 `dialog-form`、`dialog-grid` 和 `dialog-footer` 语义类。
- 删除、停用、下线、发布等危险操作应具备明确的标题、摘要和提示信息。
- 如果多个模块都需要同类对话框，优先把样式沉到公共样式文件或共享组件中。

## Procedure
1. 确认该交互属于表单、确认、提醒还是结果展示。
2. 复用已有的注册学生对话框结构，先对齐布局，再处理字段内容。
3. 把重复的布局规则下沉到 `frontend/src/style.css` 或共享组件。
4. 保持各页面只负责业务文案与字段，不重复定义同一种壳样式。
5. 如新增确认操作，检查是否应使用统一的摘要区和按钮区。

## Validation Checklist
- 对话框边界、圆角、间距与注册学生页一致。
- 确认类弹窗包含必要摘要，不再呈现默认透明消息框。
- 公共样式在多个后台模块中可复用。
- 页面级样式不再复制同一套对话框壳。
