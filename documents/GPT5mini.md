项目与数据库概览（由 GPT5mini 生成）
=====================================

说明：本文件基于当前工作区 `backend` 代码与 `backend/sql` 中的建表脚本提取总结。注意：你在 `.env` 中将 `POSTGRES_DB` 设置为 `test25`（正式环境的库），请谨慎操作，本文仅为阅读与理解，不执行写操作。

1. 高层架构
----------------
- 后端：FastAPI（`app/main.py`），以 `settings.api_v1_prefix` 暴露 REST API（多个子路由：`auth`, `dashboard`, `portal`, `recruitment`, `students`, ...）。
- 配置：基于 `pydantic-settings`（`app/core/config.py`），从 `backend/.env` 加载运行时配置。
- 鉴权：JWT + 会话管理（`app/core/security.py` 与 `app/core/session_store.py`），使用 `OAuth2PasswordBearer` 提供 token 路径。
- 数据库：主要使用 PostgreSQL。
  - 两种访问方式共存：
    - 直接 SQL（`psycopg` / psycopg3）用于复杂、性能敏感或批量脚本（诸多 `backend/scripts/*.py`，以及 `app/services/postgres_state_store_*.py` 系列）。
    - SQLAlchemy engine 用作一般 DB session（`app/core/database.py` 暴露 `SessionLocal` 用于依赖注入）。
- 缓存/队列：Redis（可配置 sentinel），配置项在 `app/core/config.py`。
- 前端代理：开发时可启用前端代理（`frontend_dev_proxy_enabled`），后端在启动时可将未知请求代理到前端 dev server。

2. 重要子系统与服务
项目与数据库概览（由 GPT5mini 生成）
=====================================

说明：本文件基于当前工作区 `backend` 代码与 `backend/sql` 中的建表脚本提取总结。注意：你在 `.env` 中将 `POSTGRES_DB` 设置为 `test25`（正式环境的库），请谨慎操作，本文仅为阅读与理解，不执行写操作。

1. 高层架构
----------------
- 后端：FastAPI（`app/main.py`），以 `settings.api_v1_prefix` 暴露 REST API（多个子路由：`auth`, `dashboard`, `portal`, `recruitment`, `students`, ...）。
- 配置：基于 `pydantic-settings`（`app/core/config.py`），从 `backend/.env` 加载运行时配置。
- 鉴权：JWT + 会话管理（`app/core/security.py` 与 `app/core/session_store.py`），使用 `OAuth2PasswordBearer` 提供 token 路径。
- 数据库：主要使用 PostgreSQL。
  - 两种访问方式共存：
    - 直接 SQL（`psycopg` / psycopg3）用于复杂、性能敏感或批量脚本（诸多 `backend/scripts/*.py`，以及 `app/services/postgres_state_store_*.py` 系列）。
    - SQLAlchemy engine 用作一般 DB session（`app/core/database.py` 暴露 `SessionLocal` 用于依赖注入）。
- 缓存/队列：Redis（可配置 sentinel），配置项在 `app/core/config.py`。
- 前端代理：开发时可启用前端代理（`frontend_dev_proxy_enabled`），后端在启动时可将未知请求代理到前端 dev server。

2. 重要子系统与服务
------------------------
- `app/services/postgres_state_store_query.py`：集中式、原生 SQL 查询集合，负责 dashboard 报表、统计与多表联查（高中低耦合 SQL、CTE、LATERAL、DISTINCT ON）。许多接口依赖此文件，查询异常会导致 503。
- `app/services/postgres_state_store_core.py`：封装 psycopg 连接、schema 检查、schema 初始化保护、以及若干启动数据迁移/补丁辅助函数（如 business_key 归一化等）。
- `backend/scripts/`：一系列可独立运行的验证/报表脚本（如 `get_undergrad_school_rankings.py`, `get_school_students.py`）。

...（文件略）

# 下面为每张表的自动生成字段与关系说明（草稿）

<!-- BEGIN auto-generated table descriptions -->

## 每张表的字段与关系说明（自动生成草稿）

### dtlms_achievements

- 表用途说明：基于表名 `dtlms_achievements` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `achievement_type`：字段名按字面含义，业务语义需由领域方确认。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `published_at`：字段名按字面含义，业务语义需由领域方确认。
  - `publisher_name`：字段名按字面含义，业务语义需由领域方确认。
  - `ranking_text`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_admission_decisions

- 表用途说明：基于表名 `dtlms_admission_decisions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `decision_status`：字段名按字面含义，业务语义需由领域方确认。
  - `rank_no`：字段名按字面含义，业务语义需由领域方确认。
  - `final_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `transfer_option`：字段名按字面含义，业务语义需由领域方确认。
  - `decision_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisor_screening_batches

- 表用途说明：基于表名 `dtlms_advisor_screening_batches` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `advisor_user_id`：外键，引用相关实体的 `id`。
  - `advisor_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `advisor_name`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_round`：字段名按字面含义，业务语义需由领域方确认。
  - `signature_base64`：字段名按字面含义，业务语义需由领域方确认。
  - `submitted_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisor_screening_items

- 表用途说明：基于表名 `dtlms_advisor_screening_items` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `batch_id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `candidate_no`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_round`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `is_passed`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_status`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisors

- 表用途说明：基于表名 `dtlms_advisors` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `advisor_no`：字段名按字面含义，业务语义需由领域方确认。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `organization_name`：字段名按字面含义，业务语义需由领域方确认。
  - `research_direction`：字段名按字面含义，业务语义需由领域方确认。
  - `annual_quota`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `user_id`：主键或外键，引用相关实体的 `id`。



### dtlms_application_materials

- 表用途说明：基于表名 `dtlms_application_materials` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `material_type`：字段名按字面含义，业务语义需由领域方确认。
  - `material_status`：字段名按字面含义，业务语义需由领域方确认。
  - `file_url`：资源或附件的 URL/路径。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_audit_policies

- 表用途说明：基于表名 `dtlms_audit_policies` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `item`：字段名按字面含义，业务语义需由领域方确认。
  - `policy`：文本说明/备注字段。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。



### dtlms_background_assessments

- 表用途说明：基于表名 `dtlms_background_assessments` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `evaluator_user_id`：外键，引用相关实体的 `id`。
  - `evaluator_username`：字段名按字面含义，业务语义需由领域方确认。
  - `evaluator_name`：字段名按字面含义，业务语义需由领域方确认。
  - `evaluator_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `assessment_result`：字段名按字面含义，业务语义需由领域方确认。
  - `assessment_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `assessed_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_data_sync_logs

- 表用途说明：基于表名 `dtlms_data_sync_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `source_system`：字段名按字面含义，业务语义需由领域方确认。
  - `target_system`：字段名按字面含义，业务语义需由领域方确认。
  - `sync_status`：字段名按字面含义，业务语义需由领域方确认。
  - `record_count`：计数字段，整型。
  - `failure_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_dict_data

- 表用途说明：基于表名 `dtlms_dict_data` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `dict_type_id`：外键，引用相关实体的 `id`。
  - `dict_type`：字段名按字面含义，业务语义需由领域方确认。
  - `label`：字段名按字面含义，业务语义需由领域方确认。
  - `value`：字段名按字面含义，业务语义需由领域方确认。
  - `sort_order`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `color_type`：字段名按字面含义，业务语义需由领域方确认。
  - `css_class`：字段名按字面含义，业务语义需由领域方确认。
  - `remark`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_dict_types

- 表用途说明：基于表名 `dtlms_dict_types` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `dict_name`：字段名按字面含义，业务语义需由领域方确认。
  - `dict_type`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `remark`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_initial_screening_confirmations

- 表用途说明：基于表名 `dtlms_initial_screening_confirmations` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `candidate_no`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_user_id`：外键，引用相关实体的 `id`。
  - `confirmer_username`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmation_result`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmation_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmed_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。


--- 结束

数据库设计
--------------------
下面按表列出字段（简要）与表间外键关系，供查阅与维护时参考。字段仅列出关键/常用列以便快速定位，索引与约束在需要时参照 `backend/sql/*.sql` 原始脚本。若后续表结构有变更，我会同步更新此节。

- `dtlms_users`
  - PK: `id`
  - 关键字段: `username`, `full_name`, `email`, `password_hash`, `portal_student_id` (FK -> `dtlms_portal_students.id`)

- `dtlms_roles`
  - PK: `id`; 字段: `role_code`, `role_name`

- `dtlms_permissions`
  - PK: `id`; 字段: `permission_code`, `permission_name`, `module_name`

- `dtlms_user_roles`
  - PK: `id`; FKs: `user_id` -> `dtlms_users.id`, `role_id` -> `dtlms_roles.id`

- `dtlms_role_permissions`
  - PK: `id`; FKs: `role_id` -> `dtlms_roles.id`, `permission_id` -> `dtlms_permissions.id`

- `dtlms_advisors`
  - PK: `id`; 字段: `advisor_no`, `full_name`, `title`, `organization_name`, `annual_quota`

- `dtlms_teams`
  - PK: `id`; 字段: `team_code`, `team_name`, `lead_advisor_id` (FK -> `dtlms_advisors.id`)

- `dtlms_team_advisors`
  - PK: `id`; FKs: `team_id` -> `dtlms_teams.id`, `advisor_id` -> `dtlms_advisors.id`

- `dtlms_students`
  - PK: `id`; 关键字段: `student_no`, `full_name`, `enrollment_year`, `degree_type`, `team_id` (FK -> `dtlms_teams.id`), `primary_advisor_id` (FK -> `dtlms_advisors.id`)

- `dtlms_student_team_history`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `team_id` -> `dtlms_teams.id`

- `dtlms_student_advisor_history`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `advisor_id` -> `dtlms_advisors.id`

- `dtlms_research_projects`
  - PK: `id`; 字段: `project_code`, `project_name`, `principal_advisor_id` (FK -> `dtlms_advisors.id`)

- `dtlms_training_plans`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `advisor_id` -> `dtlms_advisors.id`

- `dtlms_training_plan_versions`
  - PK: `id`; FK: `training_plan_id` -> `dtlms_training_plans.id`

- `dtlms_scientific_reports`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `training_plan_id` -> `dtlms_training_plans.id`, `reviewer_advisor_id` -> `dtlms_advisors.id`

- `dtlms_outbound_studies`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `advisor_id` -> `dtlms_advisors.id`

- `dtlms_achievements`
  - PK: `id`; FK: `student_id` -> `dtlms_students.id`

- `dtlms_theses`
  - PK: `id`; FKs: `student_id` -> `dtlms_students.id`, `advisor_id` -> `dtlms_advisors.id`

- `dtlms_thesis_reviews`
  - PK: `id`; FK: `thesis_id` -> `dtlms_theses.id`

- `dtlms_recruitment_plans`
  - PK: `id`; 字段: `plan_code`, `plan_name`, `academic_year`, `start_date`, `end_date`

- `dtlms_portal_students`（注册学生主表）
  - PK: `id`;
  - 关键字段: `full_name`, `phone_number`, `email`, `id_number`, `candidate_no`, `selected_plan_id` (FK -> `dtlms_recruitment_plans.id`), `submitted_at`
  - 说明：多数 portal/申请表通过 `portal_student_id` 与此表关联；`candidate_no` 有触发器保证不可随意更改。

- `dtlms_portal_student_profiles`
  - PK: `portal_student_id` (FK -> `dtlms_portal_students.id`)

- `dtlms_research_fields`
  - PK: `id`; 字段: `field_code`, `field_name`

- `dtlms_recruitment_applications`
  - PK: `id`;
  - FKs: `plan_id` -> `dtlms_recruitment_plans.id`, `portal_student_id` -> `dtlms_portal_students.id`, `intended_field_id` -> `dtlms_research_fields.id`
  - 关键字段: `business_key`, `candidate_no`, `student_name`, `first_choice`, `second_choice`, `applied_at`, `application_status`, 多个 screening/审查字段

- 申请相关从表（均以 `application_id` 关联）
  - `dtlms_portal_application_preferences`：`application_id` -> `dtlms_recruitment_applications.id`（ON DELETE CASCADE）；字段：`preference_order`, `research_center_name`, `advisor_name`
  - `dtlms_portal_application_education_experiences`：`sort_order`, `education_stage`, `school_name`（本科记录通常 `sort_order=2`）
  - `dtlms_portal_application_practice_experiences`
  - `dtlms_portal_application_english_proficiencies`
  - `dtlms_portal_application_family_members`
  - `dtlms_portal_application_achievement_records`
  - `dtlms_portal_application_personal_statements`（PK = `application_id`）
  - `dtlms_portal_application_declarations`（PK = `application_id`）
  - `dtlms_portal_application_attachments`：同时包含 `portal_student_id` 与 `application_id`，并使用 `owner_type`/`owner_id` 做多态分配
  - `dtlms_application_materials`

- 审核/筛选/面试流相关表
  - `dtlms_qualification_reviews`, `dtlms_qualification_review_logs`, `dtlms_background_assessments`（均以 `application_id` 关联）
  - `dtlms_advisor_screening_batches` 与 `dtlms_advisor_screening_items`（`batch_id` -> batches.id；`application_id` -> applications.id）
  - `dtlms_initial_screening_confirmations`, `dtlms_initial_screening_notifications`（均以 `application_id` 关联）
  - `dtlms_reviewer_assignments`, `dtlms_material_scores`（assignment/score 链接到 reviewer_assignment/application）
  - `dtlms_interview_groups`, `dtlms_interview_schedules`（`plan_id`、`application_id`）、`dtlms_interview_scores`
  - `dtlms_written_exam_scores`, `dtlms_admission_decisions`

- 日志/配置/通知/索引类表
  - `dtlms_login_logs`, `dtlms_operation_logs`, `dtlms_data_sync_logs`
  - `dtlms_notification_delivery_logs`, `dtlms_notification_templates`
  - `dtlms_system_configs`, `dtlms_audit_policies`, `dtlms_integrations`

- 内容发布表
  - `dtlms_news_articles`（发布/审核字段、publisher/reviewer user id/name）

说明与维护建议：
- 外键依赖关系集中在 `dtlms_portal_students`、`dtlms_recruitment_applications`、`dtlms_students`、`dtlms_advisors` 与 `dtlms_recruitment_plans` 这几张核心表，变更这些表需额外谨慎并准备回填脚本与索引调整。
- 报表/查询多基于 `applied_at` / `created_at` / `candidate_no` / `business_key` 等时间/唯一标识字段进行排序与去重，保持这些字段的语义与索引一致可大幅降低报表出错风险。
- 我会把这节作为“随手可更新的单源真相” —— 今后你若修改表或添加字段，告诉我我会立刻把该表条目更新到此文件。

实时数据库快照（来自 `test25`，只读导出）
-------------------------------------------------
下面是从 `test25` 数据库直接导出的表结构快照（仅展示 JSON 格式片段的摘要）。完整 JSON 已保存为：`tools/extract_schema_from_db.py` 的输出（控制台）。


示例（部分表摘录，来自 `test25` 导出）:

- `dtlms_users`:
  - 主键: `id`
  - 常见字段: `portal_student_id` (FK -> `dtlms_portal_students.id`), `username`, `full_name`, `email`, `department_name`, `phone_number`, `last_login_at`, `created_at`, `updated_at`。

- `dtlms_recruitment_applications`:
  - 主键: `id`
  - 常见字段: `applicant_id`, `candidate_no`, `status`, `created_at`, `updated_at`（详见 SQL 初始建表脚本 `010_init_schema.sql`）。

- 工作流相关表（节选）:
  - `dtlms_wf_de_model`: 主键 `id_`，字段 `name_`,`key_`,`version_`,`meta_info_`,`created_` 等。
  - `dtlms_wf_hi_actinst`: 主键 `id_`，外键 `proc_def_id_` -> `dtlms_wf_re_procdef.id_`。
  - `dtlms_wf_hi_procinst` / `dtlms_wf_hi_taskinst` / `dtlms_wf_ru_task`：包含执行与任务运行时信息，常见字段见导出 JSON。

- 分数与考试表:
  - `dtlms_written_exam_scores`: 主键 `id`，字段 `application_id` (FK -> `dtlms_recruitment_applications.id`)、`exam_date`、`exam_score`、`import_batch_no`、`created_at`、`updated_at`。

完整导出（原始文本/JSON 快照）已保存为 `documents/test25_schema.json`。如需我将每张表全部字段以 Markdown 表格形式嵌入此文档（更好阅读），我可以继续把整个 JSON 转换为逐表 Markdown 并追加到本节。

注意：导出内容为生产 `test25` 的当前 schema 快照；如需我将完整 JSON 嵌入到此文档或另存为 `documents/test25_schema.json`，我可以继续写入。当前导出已保存在终端输出资源中。

---

完整表结构（逐表，来自 `documents/test25_schema.md`）


<!-- BEGIN AUTO-GENERATED test25 schema -->

#<!-- auto-generated from documents/test25_schema_full.md -->

**表/字段/关系 说明（概要）**

- **用途说明**: 本节基于数据库元数据与表/字段命名自动生成，用以快速理解数据模型结构；具体业务含义、枚举值与约束需由领域/产品方复核并补充。
- **表说明**: 每张表下方已给出按表名推断的功能简述（若存在疑义，请在表下方注记）。
- **字段说明**: 对常见字段名给出统一解释；对表内特殊字段给出建议性语义说明，供业务确认。
- **关系说明**: 在每张表的 **Foreign keys** 小节列出主外键关系；关系说明按“来源表.字段 -> 目标表.字段（约束名）”格式展示，并尽量说明该关联的业务含义。

通用字段说明（示例）:

- `id`: 表的主键，通常为自增序列（bigint）。
- `created_at`: 记录创建时间，通常为 `timestamp with time zone`，按 UTC 存储。
- `updated_at`: 记录最后更新时间。
- `is_deleted`: 软删除标志，`true` 表示逻辑已删除。
- `business_key`: 业务唯一标识，用于跨系统关联或幂等性校验。
- `application_id` / `student_id` / `user_id`: 外键，分别指向申请、学生或用户实体的 `id` 字段，用于表示从属/归属关系。

# 下面为每张表的自动生成字段与关系说明（草稿）

<!-- BEGIN auto-generated table descriptions -->

## 每张表的字段与关系说明（自动生成草稿）

### dtlms_achievements

- 表用途说明：基于表名 `dtlms_achievements` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `achievement_type`：字段名按字面含义，业务语义需由领域方确认。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `published_at`：字段名按字面含义，业务语义需由领域方确认。
  - `publisher_name`：字段名按字面含义，业务语义需由领域方确认。
  - `ranking_text`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。


### dtlms_admission_decisions

- 表用途说明：基于表名 `dtlms_admission_decisions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `decision_status`：字段名按字面含义，业务语义需由领域方确认。
  - `rank_no`：字段名按字面含义，业务语义需由领域方确认。
  - `final_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `transfer_option`：字段名按字面含义，业务语义需由领域方确认。
  - `decision_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。

...

<!-- END auto-generated table descriptions -->
<!-- BEGIN auto-generated table descriptions -->

## 每张表的字段与关系说明（自动生成草稿）

### dtlms_achievements

- 表用途说明：基于表名 `dtlms_achievements` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `achievement_type`：字段名按字面含义，业务语义需由领域方确认。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `published_at`：字段名按字面含义，业务语义需由领域方确认。
  - `publisher_name`：字段名按字面含义，业务语义需由领域方确认。
  - `ranking_text`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_admission_decisions

- 表用途说明：基于表名 `dtlms_admission_decisions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `decision_status`：字段名按字面含义，业务语义需由领域方确认。
  - `rank_no`：字段名按字面含义，业务语义需由领域方确认。
  - `final_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `transfer_option`：字段名按字面含义，业务语义需由领域方确认。
  - `decision_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisor_screening_batches

- 表用途说明：基于表名 `dtlms_advisor_screening_batches` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `advisor_user_id`：外键，引用相关实体的 `id`。
  - `advisor_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `advisor_name`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_round`：字段名按字面含义，业务语义需由领域方确认。
  - `signature_base64`：字段名按字面含义，业务语义需由领域方确认。
  - `submitted_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisor_screening_items

- 表用途说明：基于表名 `dtlms_advisor_screening_items` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `batch_id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `candidate_no`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_round`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `is_passed`：字段名按字面含义，业务语义需由领域方确认。
  - `screening_status`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_advisors

- 表用途说明：基于表名 `dtlms_advisors` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `advisor_no`：字段名按字面含义，业务语义需由领域方确认。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `organization_name`：字段名按字面含义，业务语义需由领域方确认。
  - `research_direction`：字段名按字面含义，业务语义需由领域方确认。
  - `annual_quota`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `user_id`：主键或外键，引用相关实体的 `id`。



### dtlms_application_materials

- 表用途说明：基于表名 `dtlms_application_materials` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `material_type`：字段名按字面含义，业务语义需由领域方确认。
  - `material_status`：字段名按字面含义，业务语义需由领域方确认。
  - `file_url`：资源或附件的 URL/路径。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_audit_policies

- 表用途说明：基于表名 `dtlms_audit_policies` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `item`：字段名按字面含义，业务语义需由领域方确认。
  - `policy`：文本说明/备注字段。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。



### dtlms_background_assessments

- 表用途说明：基于表名 `dtlms_background_assessments` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `evaluator_user_id`：外键，引用相关实体的 `id`。
  - `evaluator_username`：字段名按字面含义，业务语义需由领域方确认。
  - `evaluator_name`：字段名按字面含义，业务语义需由领域方确认。
  - `evaluator_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `assessment_result`：字段名按字面含义，业务语义需由领域方确认。
  - `assessment_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `assessed_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_data_sync_logs

- 表用途说明：基于表名 `dtlms_data_sync_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `source_system`：字段名按字面含义，业务语义需由领域方确认。
  - `target_system`：字段名按字面含义，业务语义需由领域方确认。
  - `sync_status`：字段名按字面含义，业务语义需由领域方确认。
  - `record_count`：计数字段，整型。
  - `failure_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_dict_data

- 表用途说明：基于表名 `dtlms_dict_data` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `dict_type_id`：外键，引用相关实体的 `id`。
  - `dict_type`：字段名按字面含义，业务语义需由领域方确认。
  - `label`：字段名按字面含义，业务语义需由领域方确认。
  - `value`：字段名按字面含义，业务语义需由领域方确认。
  - `sort_order`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `color_type`：字段名按字面含义，业务语义需由领域方确认。
  - `css_class`：字段名按字面含义，业务语义需由领域方确认。
  - `remark`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_dict_types

- 表用途说明：基于表名 `dtlms_dict_types` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `dict_name`：字段名按字面含义，业务语义需由领域方确认。
  - `dict_type`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `remark`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_initial_screening_confirmations

- 表用途说明：基于表名 `dtlms_initial_screening_confirmations` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `candidate_no`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_user_id`：外键，引用相关实体的 `id`。
  - `confirmer_username`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmer_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmation_result`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmation_comment`：字段名按字面含义，业务语义需由领域方确认。
  - `confirmed_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



# test25 schema (full export)
## dtlms_achievements
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_achievements_id_seq'::regclass) |
| student_id | bigint | NO |  |
| achievement_type | character varying | NO |  |
| title | character varying | NO |  |
| published_at | date | YES |  |
| publisher_name | character varying | YES |  |
| ranking_text | character varying | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- student_id -> dtlms_students.id  (dtlms_achievements_student_id_fkey)

## dtlms_admission_decisions
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_admission_decisions_id_seq'::regclass) |
| application_id | bigint | NO |  |
| decision_status | character varying | NO | 'pending'::character varying |
| rank_no | integer | YES |  |
| final_score | numeric | YES |  |
| transfer_option | character varying | YES |  |
| decision_comment | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_admission_decisions_application_id_fkey)

## dtlms_advisor_screening_batches
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_advisor_screening_batches_id_seq'::regclass) |
| advisor_user_id | bigint | YES |  |
| advisor_username | character varying | NO |  |
| advisor_name | character varying | YES |  |
| advisor_role_code | character varying | NO | 'advisor'::character varying |
| screening_round | character varying | NO |  |
| signature_base64 | text | NO |  |
| submitted_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_advisor_screening_items
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_advisor_screening_items_id_seq'::regclass) |
| batch_id | bigint | NO |  |
| application_id | bigint | NO |  |
| business_key | character varying | NO |  |
| candidate_no | character varying | NO |  |
| screening_round | character varying | NO |  |
| advisor_score | numeric | NO |  |
| is_passed | boolean | NO |  |
| screening_status | character varying | NO | 'submitted'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_advisor_screening_items_application_id_fkey)
- batch_id -> dtlms_advisor_screening_batches.id  (dtlms_advisor_screening_items_batch_id_fkey)

## dtlms_advisors
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_advisors_id_seq'::regclass) |
| advisor_no | character varying | NO |  |
| full_name | character varying | NO |  |
| title | character varying | NO |  |
| organization_name | character varying | NO |  |
| research_direction | character varying | NO |  |
| annual_quota | integer | NO | 0 |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| user_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- user_id -> dtlms_users.id  (fk_dtlms_advisors_user_id)

## dtlms_application_materials
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_application_materials_id_seq'::regclass) |
| application_id | bigint | NO |  |
| material_type | character varying | NO |  |
| material_status | character varying | NO | 'pending'::character varying |
| file_url | character varying | NO |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_application_materials_application_id_fkey)

## dtlms_audit_policies
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO |  |
| item | character varying | NO |  |
| policy | text | NO |  |
| status | character varying | NO | '启用'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| is_deleted | boolean | NO | false |
**Primary key:** id

## dtlms_background_assessments
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_background_assessments_id_seq'::regclass) |
| application_id | bigint | NO |  |
| evaluator_user_id | bigint | YES |  |
| evaluator_username | character varying | NO |  |
| evaluator_name | character varying | YES |  |
| evaluator_role_code | character varying | NO |  |
| assessment_result | character varying | NO |  |
| assessment_comment | text | YES |  |
| assessed_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_background_assessments_application_id_fkey)

## dtlms_data_sync_logs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_data_sync_logs_id_seq'::regclass) |
| source_system | character varying | NO |  |
| target_system | character varying | NO |  |
| sync_status | character varying | NO |  |
| record_count | integer | NO | 0 |
| failure_reason | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_dict_data
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_dict_data_id_seq'::regclass) |
| dict_type_id | bigint | NO |  |
| dict_type | character varying | NO |  |
| label | character varying | NO |  |
| value | character varying | NO |  |
| sort_order | integer | NO | 0 |
| status | character varying | NO | '启用'::character varying |
| color_type | character varying | YES |  |
| css_class | character varying | YES |  |
| remark | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- dict_type_id -> dtlms_dict_types.id  (dtlms_dict_data_dict_type_id_fkey)

## dtlms_dict_types
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_dict_types_id_seq'::regclass) |
| dict_name | character varying | NO |  |
| dict_type | character varying | NO |  |
| status | character varying | NO | '启用'::character varying |
| remark | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_initial_screening_confirmations
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_initial_screening_confirmations_id_seq'::regclass) |
| application_id | bigint | NO |  |
| business_key | character varying | NO |  |
| candidate_no | character varying | NO |  |
| confirmer_user_id | bigint | YES |  |
| confirmer_username | character varying | NO |  |
| confirmer_name | character varying | YES |  |
| confirmer_role_code | character varying | NO |  |
| confirmation_result | character varying | NO |  |
| confirmation_comment | text | YES |  |
| confirmed_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_initial_screening_confirmations_application_id_fkey)

## dtlms_initial_screening_notifications
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_initial_screening_notifications_id_seq'::regclass) |
| application_id | bigint | NO |  |
| business_key | character varying | NO |  |
| notification_channel | character varying | NO |  |
| notification_event | character varying | NO |  |
| notification_status | character varying | NO | 'pending'::character varying |
| recipient_address | character varying | YES |  |
| recipient_user_id | bigint | YES |  |
| recipient_username | character varying | YES |  |
| payload_json | jsonb | YES |  |
| sent_at | timestamp with time zone | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_initial_screening_notifications_application_id_fkey)

## dtlms_integrations
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO |  |
| name | character varying | NO |  |
| direction | character varying | NO |  |
| cadence | character varying | NO |  |
| status | character varying | NO | '正常'::character varying |
| owner | character varying | NO | ''::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| is_deleted | boolean | NO | false |
**Primary key:** id

## dtlms_interview_groups
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_interview_groups_id_seq'::regclass) |
| plan_id | bigint | NO |  |
| group_code | character varying | NO |  |
| group_name | character varying | NO |  |
| interview_mode | character varying | NO | 'offline'::character varying |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- plan_id -> dtlms_recruitment_plans.id  (dtlms_interview_groups_plan_id_fkey)


<!-- END AUTO-GENERATED test25 schema -->


