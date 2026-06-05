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



### dtlms_initial_screening_notifications

- 表用途说明：基于表名 `dtlms_initial_screening_notifications` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `notification_channel`：字段名按字面含义，业务语义需由领域方确认。
  - `notification_event`：字段名按字面含义，业务语义需由领域方确认。
  - `notification_status`：字段名按字面含义，业务语义需由领域方确认。
  - `recipient_address`：字段名按字面含义，业务语义需由领域方确认。
  - `recipient_user_id`：外键，引用相关实体的 `id`。
  - `recipient_username`：字段名按字面含义，业务语义需由领域方确认。
  - `payload_json`：JSON/JSONB 字段，存放结构化或半结构化数据。
  - `sent_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_integrations

- 表用途说明：基于表名 `dtlms_integrations` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `name`：字段名按字面含义，业务语义需由领域方确认。
  - `direction`：字段名按字面含义，业务语义需由领域方确认。
  - `cadence`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `owner`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。



### dtlms_interview_groups

- 表用途说明：基于表名 `dtlms_interview_groups` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `plan_id`：主键或外键，引用相关实体的 `id`。
  - `group_code`：字段名按字面含义，业务语义需由领域方确认。
  - `group_name`：字段名按字面含义，业务语义需由领域方确认。
  - `interview_mode`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_interview_schedules

- 表用途说明：基于表名 `dtlms_interview_schedules` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `interview_group_id`：外键，引用相关实体的 `id`。
  - `admission_ticket_no`：字段名按字面含义，业务语义需由领域方确认。
  - `starts_at`：字段名按字面含义，业务语义需由领域方确认。
  - `ends_at`：字段名按字面含义，业务语义需由领域方确认。
  - `schedule_status`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_interview_scores

- 表用途说明：基于表名 `dtlms_interview_scores` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `schedule_id`：主键或外键，引用相关实体的 `id`。
  - `evaluator_username`：字段名按字面含义，业务语义需由领域方确认。
  - `single_choice_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `fill_blank_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `coding_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `interview_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `ideological_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_login_logs

- 表用途说明：基于表名 `dtlms_login_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `login_status`：字段名按字面含义，业务语义需由领域方确认。
  - `login_ip`：字段名按字面含义，业务语义需由领域方确认。
  - `user_agent`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_material_scores

- 表用途说明：基于表名 `dtlms_material_scores` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `reviewer_assignment_id`：外键，引用相关实体的 `id`。
  - `material_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `recommendation_text`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_news_articles

- 表用途说明：基于表名 `dtlms_news_articles` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `news_code`：字段名按字面含义，业务语义需由领域方确认。
  - `news_title`：字段名按字面含义，业务语义需由领域方确认。
  - `news_content`：字段名按字面含义，业务语义需由领域方确认。
  - `news_type`：字段名按字面含义，业务语义需由领域方确认。
  - `publisher_user_id`：外键，引用相关实体的 `id`。
  - `publisher_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `publisher_name`：字段名按字面含义，业务语义需由领域方确认。
  - `reviewer_user_id`：外键，引用相关实体的 `id`。
  - `reviewer_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `reviewer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `published_at`：字段名按字面含义，业务语义需由领域方确认。
  - `status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `is_pinned`：字段名按字面含义，业务语义需由领域方确认。
  - `display_order`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_notification_delivery_logs

- 表用途说明：基于表名 `dtlms_notification_delivery_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `channel`：字段名按字面含义，业务语义需由领域方确认。
  - `template_code`：字段名按字面含义，业务语义需由领域方确认。
  - `recipient`：字段名按字面含义，业务语义需由领域方确认。
  - `subject`：字段名按字面含义，业务语义需由领域方确认。
  - `send_status`：字段名按字面含义，业务语义需由领域方确认。
  - `failure_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `triggered_by`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_notification_templates

- 表用途说明：基于表名 `dtlms_notification_templates` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `template_code`：字段名按字面含义，业务语义需由领域方确认。
  - `channel`：字段名按字面含义，业务语义需由领域方确认。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `content_template`：字段名按字面含义，业务语义需由领域方确认。
  - `variables_schema`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_operation_logs

- 表用途说明：基于表名 `dtlms_operation_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `operator_username`：字段名按字面含义，业务语义需由领域方确认。
  - `operator_role`：字段名按字面含义，业务语义需由领域方确认。
  - `module_name`：字段名按字面含义，业务语义需由领域方确认。
  - `entity_name`：字段名按字面含义，业务语义需由领域方确认。
  - `entity_id`：主键或外键，引用相关实体的 `id`。
  - `action`：字段名按字面含义，业务语义需由领域方确认。
  - `old_value`：字段名按字面含义，业务语义需由领域方确认。
  - `new_value`：字段名按字面含义，业务语义需由领域方确认。
  - `request_ip`：字段名按字面含义，业务语义需由领域方确认。
  - `result`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_outbound_studies

- 表用途说明：基于表名 `dtlms_outbound_studies` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_id`：主键或外键，引用相关实体的 `id`。
  - `study_type`：字段名按字面含义，业务语义需由领域方确认。
  - `destination`：字段名按字面含义，业务语义需由领域方确认。
  - `start_date`：字段名按字面含义，业务语义需由领域方确认。
  - `end_date`：字段名按字面含义，业务语义需由领域方确认。
  - `approval_status`：字段名按字面含义，业务语义需由领域方确认。
  - `expected_outcome`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。



### dtlms_permissions

- 表用途说明：基于表名 `dtlms_permissions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `permission_code`：字段名按字面含义，业务语义需由领域方确认。
  - `permission_name`：字段名按字面含义，业务语义需由领域方确认。
  - `module_name`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_achievement_records

- 表用途说明：基于表名 `dtlms_portal_application_achievement_records` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `achievement_type`：字段名按字面含义，业务语义需由领域方确认。
  - `paper_title`：字段名按字面含义，业务语义需由领域方确认。
  - `author_order`：字段名按字面含义，业务语义需由领域方确认。
  - `journal_or_conference`：字段名按字面含义，业务语义需由领域方确认。
  - `publish_or_index_month`：字段名按字面含义，业务语义需由领域方确认。
  - `award_name`：字段名按字面含义，业务语义需由领域方确认。
  - `awarding_organization`：字段名按字面含义，业务语义需由领域方确认。
  - `award_level`：字段名按字面含义，业务语义需由领域方确认。
  - `award_year`：字段名按字面含义，业务语义需由领域方确认。
  - `responsibility_text`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `achievement_month`：字段名按字面含义，业务语义需由领域方确认。
  - `award_rank`：字段名按字面含义，业务语义需由领域方确认。
  - `award_certificate_attachment_url`：资源或附件的 URL/路径。
  - `description_text`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_portal_application_attachments

- 表用途说明：基于表名 `dtlms_portal_application_attachments` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `portal_student_id`：外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `owner_type`：字段名按字面含义，业务语义需由领域方确认。
  - `owner_id`：主键或外键，引用相关实体的 `id`。
  - `attachment_category`：资源或附件的 URL/路径。
  - `file_name`：资源或附件的 URL/路径。
  - `file_url`：资源或附件的 URL/路径。
  - `file_type`：资源或附件的 URL/路径。
  - `file_size`：资源或附件的 URL/路径。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_declarations

- 表用途说明：基于表名 `dtlms_portal_application_declarations` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `has_read_declaration`：字段名按字面含义，业务语义需由领域方确认。
  - `declaration_text`：字段名按字面含义，业务语义需由领域方确认。
  - `progress_snapshot`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_education_experiences

- 表用途说明：基于表名 `dtlms_portal_application_education_experiences` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `sort_order`：字段名按字面含义，业务语义需由领域方确认。
  - `education_stage`：字段名按字面含义，业务语义需由领域方确认。
  - `start_month`：字段名按字面含义，业务语义需由领域方确认。
  - `end_month`：字段名按字面含义，业务语义需由领域方确认。
  - `school_name`：字段名按字面含义，业务语义需由领域方确认。
  - `major_name`：字段名按字面含义，业务语义需由领域方确认。
  - `average_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `gpa`：字段名按字面含义，业务语义需由领域方确认。
  - `ranking`：字段名按字面含义，业务语义需由领域方确认。
  - `verifier_name`：字段名按字面含义，业务语义需由领域方确认。
  - `verifier_phone`：联系电话或移动电话。
  - `transcript_attachment_url`：资源或附件的 URL/路径。
  - `degree_certificate_attachment_url`：资源或附件的 URL/路径。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `graduation_certificate_attachment_url`：资源或附件的 URL/路径。



### dtlms_portal_application_english_proficiencies

- 表用途说明：基于表名 `dtlms_portal_application_english_proficiencies` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `exam_name`：字段名按字面含义，业务语义需由领域方确认。
  - `score_text`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `certificate_attachment_url`：资源或附件的 URL/路径。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_family_members

- 表用途说明：基于表名 `dtlms_portal_application_family_members` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `member_name`：字段名按字面含义，业务语义需由领域方确认。
  - `relation_type`：字段名按字面含义，业务语义需由领域方确认。
  - `employer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `job_title`：字段名按字面含义，业务语义需由领域方确认。
  - `contact_phone`：联系电话或移动电话。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_personal_statements

- 表用途说明：基于表名 `dtlms_portal_application_personal_statements` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `personal_statement_text`：字段名按字面含义，业务语义需由领域方确认。
  - `ai_problem_statement`：字段名按字面含义，业务语义需由领域方确认。
  - `ai_industry_opinion`：字段名按字面含义，业务语义需由领域方确认。
  - `resume_attachment_url`：资源或附件的 URL/路径。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `growth_experience_text`：字段名按字面含义，业务语义需由领域方确认。
  - `program_application_reason_text`：字段名按字面含义，业务语义需由领域方确认。
  - `career_plan_text`：字段名按字面含义，业务语义需由领域方确认。
  - `supporting_material_attachment_url`：资源或附件的 URL/路径。



### dtlms_portal_application_practice_experiences

- 表用途说明：基于表名 `dtlms_portal_application_practice_experiences` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `start_month`：字段名按字面含义，业务语义需由领域方确认。
  - `end_month`：字段名按字面含义，业务语义需由领域方确认。
  - `organization_name`：字段名按字面含义，业务语义需由领域方确认。
  - `position_name`：字段名按字面含义，业务语义需由领域方确认。
  - `responsibility_text`：字段名按字面含义，业务语义需由领域方确认。
  - `verifier_name`：字段名按字面含义，业务语义需由领域方确认。
  - `verifier_phone`：联系电话或移动电话。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_portal_application_preferences

- 表用途说明：基于表名 `dtlms_portal_application_preferences` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `preference_order`：字段名按字面含义，业务语义需由领域方确认。
  - `research_center_name`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_name`：字段名按字面含义，业务语义需由领域方确认。
  - `is_optional`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `team_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_user_id`：外键，引用相关实体的 `id`。



### dtlms_portal_student_profiles

- 表用途说明：基于表名 `dtlms_portal_student_profiles` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `portal_student_id`：外键，引用相关实体的 `id`。
  - `full_name_pinyin`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `gender`：字段名按字面含义，业务语义需由领域方确认。
  - `birth_date`：字段名按字面含义，业务语义需由领域方确认。
  - `ethnic_group`：字段名按字面含义，业务语义需由领域方确认。
  - `native_place`：字段名按字面含义，业务语义需由领域方确认。
  - `political_status`：字段名按字面含义，业务语义需由领域方确认。
  - `marital_status`：字段名按字面含义，业务语义需由领域方确认。
  - `religious_belief`：字段名按字面含义，业务语义需由领域方确认。
  - `id_type`：字段名按字面含义，业务语义需由领域方确认。
  - `mailing_address`：字段名按字面含义，业务语义需由领域方确认。
  - `emergency_contact_name`：字段名按字面含义，业务语义需由领域方确认。
  - `emergency_contact_phone`：联系电话或移动电话。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `profile_photo_url`：资源或附件的 URL/路径。
  - `id_card_collage_url`：资源或附件的 URL/路径。



### dtlms_portal_students

- 表用途说明：基于表名 `dtlms_portal_students` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `phone_number`：联系电话或移动电话。
  - `email`：电子邮箱地址。
  - `id_number`：字段名按字面含义，业务语义需由领域方确认。
  - `graduation_school`：字段名按字面含义，业务语义需由领域方确认。
  - `highest_degree`：字段名按字面含义，业务语义需由领域方确认。
  - `intended_field`：字段名按字面含义，业务语义需由领域方确认。
  - `political_status`：字段名按字面含义，业务语义需由领域方确认。
  - `selected_plan_id`：外键，引用相关实体的 `id`。
  - `selected_team_name`：字段名按字面含义，业务语义需由领域方确认。
  - `selected_advisor_name`：字段名按字面含义，业务语义需由领域方确认。
  - `self_evaluation`：字段名按字面含义，业务语义需由领域方确认。
  - `submitted_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `password_hash`：字段名按字面含义，业务语义需由领域方确认。
  - `gender`：字段名按字面含义，业务语义需由领域方确认。
  - `birth_date`：字段名按字面含义，业务语义需由领域方确认。
  - `ethnic_group`：字段名按字面含义，业务语义需由领域方确认。
  - `native_place`：字段名按字面含义，业务语义需由领域方确认。
  - `marital_status`：字段名按字面含义，业务语义需由领域方确认。
  - `religious_belief`：字段名按字面含义，业务语义需由领域方确认。
  - `id_type`：字段名按字面含义，业务语义需由领域方确认。
  - `mailing_address`：字段名按字面含义，业务语义需由领域方确认。
  - `english_level`：字段名按字面含义，业务语义需由领域方确认。
  - `family_info`：字段名按字面含义，业务语义需由领域方确认。
  - `education_experience`：字段名按字面含义，业务语义需由领域方确认。
  - `practice_experience`：字段名按字面含义，业务语义需由领域方确认。
  - `personal_profile`：资源或附件的 URL/路径。
  - `recommendation_notes`：字段名按字面含义，业务语义需由领域方确认。
  - `personal_statement_text`：字段名按字面含义，业务语义需由领域方确认。
  - `signed_agreement`：字段名按字面含义，业务语义需由领域方确认。
  - `account_status`：计数字段，整型。
  - `application_draft`：字段名按字面含义，业务语义需由领域方确认。
  - `selected_team_id`：外键，引用相关实体的 `id`。
  - `selected_advisor_user_id`：外键，引用相关实体的 `id`。



### dtlms_qualification_review_logs

- 表用途说明：基于表名 `dtlms_qualification_review_logs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `reviewer_user_id`：外键，引用相关实体的 `id`。
  - `reviewer_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `reviewer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `reviewer_role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `action`：字段名按字面含义，业务语义需由领域方确认。
  - `action_label`：字段名按字面含义，业务语义需由领域方确认。
  - `review_comment`：文本说明/备注字段。
  - `reviewed_at`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_qualification_reviews

- 表用途说明：基于表名 `dtlms_qualification_reviews` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `reviewer_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `review_status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `review_comment`：文本说明/备注字段。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_recruitment_applications

- 表用途说明：基于表名 `dtlms_recruitment_applications` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `plan_id`：主键或外键，引用相关实体的 `id`。
  - `student_name`：字段名按字面含义，业务语义需由领域方确认。
  - `candidate_no`：字段名按字面含义，业务语义需由领域方确认。
  - `gender`：字段名按字面含义，业务语义需由领域方确认。
  - `graduation_school`：字段名按字面含义，业务语义需由领域方确认。
  - `highest_degree`：字段名按字面含义，业务语义需由领域方确认。
  - `intended_field_id`：外键，引用相关实体的 `id`。
  - `application_status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。
  - `review_round`：字段名按字面含义，业务语义需由领域方确认。
  - `first_choice`：字段名按字面含义，业务语义需由领域方确认。
  - `second_choice`：字段名按字面含义，业务语义需由领域方确认。
  - `political_status`：字段名按字面含义，业务语义需由领域方确认。
  - `marital_status`：字段名按字面含义，业务语义需由领域方确认。
  - `religious_belief`：字段名按字面含义，业务语义需由领域方确认。
  - `native_place`：字段名按字面含义，业务语义需由领域方确认。
  - `phone_number`：联系电话或移动电话。
  - `email`：电子邮箱地址。
  - `mailing_address`：字段名按字面含义，业务语义需由领域方确认。
  - `id_type`：字段名按字面含义，业务语义需由领域方确认。
  - `id_number`：字段名按字面含义，业务语义需由领域方确认。
  - `undergraduate_school`：字段名按字面含义，业务语义需由领域方确认。
  - `accept_adjustment`：字段名按字面含义，业务语义需由领域方确认。
  - `undergraduate_average_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `undergraduate_gpa`：字段名按字面含义，业务语义需由领域方确认。
  - `undergraduate_rank`：字段名按字面含义，业务语义需由领域方确认。
  - `undergraduate_major`：字段名按字面含义，业务语义需由领域方确认。
  - `graduate_average_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `graduate_gpa`：字段名按字面含义，业务语义需由领域方确认。
  - `graduate_rank`：字段名按字面含义，业务语义需由领域方确认。
  - `graduate_major`：字段名按字面含义，业务语义需由领域方确认。
  - `intended_advisor_name`：字段名按字面含义，业务语义需由领域方确认。
  - `discovery_channel`：字段名按字面含义，业务语义需由领域方确认。
  - `graduate_school`：字段名按字面含义，业务语义需由领域方确认。
  - `overseas_university_name`：字段名按字面含义，业务语义需由领域方确认。
  - `overseas_master_university_name`：字段名按字面含义，业务语义需由领域方确认。
  - `self_evaluation`：字段名按字面含义，业务语义需由领域方确认。
  - `applied_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `research_problem`：字段名按字面含义，业务语义需由领域方确认。
  - `research_status_analysis`：字段名按字面含义，业务语义需由领域方确认。
  - `research_impact`：字段名按字面含义，业务语义需由领域方确认。
  - `ai_society_impact`：字段名按字面含义，业务语义需由领域方确认。
  - `dissenting_view`：字段名按字面含义，业务语义需由领域方确认。
  - `family_info`：字段名按字面含义，业务语义需由领域方确认。
  - `education_experience`：字段名按字面含义，业务语义需由领域方确认。
  - `practice_experience`：字段名按字面含义，业务语义需由领域方确认。
  - `personal_statement_text`：字段名按字面含义，业务语义需由领域方确认。
  - `student_activity_experience`：字段名按字面含义，业务语义需由领域方确认。
  - `personal_statement_attachment`：资源或附件的 URL/路径。
  - `material_list_attachment`：资源或附件的 URL/路径。
  - `supplementary_profile`：资源或附件的 URL/路径。
  - `portal_student_id`：外键，引用相关实体的 `id`。
  - `source_channel`：字段名按字面含义，业务语义需由领域方确认。
  - `source_channel_other`：字段名按字面含义，业务语义需由领域方确认。
  - `first_choice_team_id`：外键，引用相关实体的 `id`。
  - `second_choice_team_id`：外键，引用相关实体的 `id`。
  - `intended_advisor_user_id`：外键，引用相关实体的 `id`。
  - `advisor_screening_status`：字段名按字面含义，业务语义需由领域方确认。
  - `advisor_screening_round`：字段名按字面含义，业务语义需由领域方确认。
  - `first_choice_screening_batch_id`：外键，引用相关实体的 `id`。
  - `second_choice_screening_batch_id`：外键，引用相关实体的 `id`。
  - `first_choice_screening_submitted_at`：字段名按字面含义，业务语义需由领域方确认。
  - `second_choice_screening_submitted_at`：字段名按字面含义，业务语义需由领域方确认。
  - `first_choice_screening_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `second_choice_screening_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `initial_screening_status`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_result`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_confirmed_at`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_confirmer_username`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_confirmer_name`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_notification_status`：字段名按字面含义，业务语义需由领域方确认。
  - `initial_screening_notification_sent_at`：字段名按字面含义，业务语义需由领域方确认。
  - `next_stage_name`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_recruitment_plans

- 表用途说明：基于表名 `dtlms_recruitment_plans` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `plan_code`：字段名按字面含义，业务语义需由领域方确认。
  - `plan_name`：字段名按字面含义，业务语义需由领域方确认。
  - `academic_year`：字段名按字面含义，业务语义需由领域方确认。
  - `semester`：字段名按字面含义，业务语义需由领域方确认。
  - `start_date`：字段名按字面含义，业务语义需由领域方确认。
  - `end_date`：字段名按字面含义，业务语义需由领域方确认。
  - `target_quota`：字段名按字面含义，业务语义需由领域方确认。
  - `plan_status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `brochure_image_url`：资源或附件的 URL/路径。
  - `plan_description`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_research_fields

- 表用途说明：基于表名 `dtlms_research_fields` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `field_code`：字段名按字面含义，业务语义需由领域方确认。
  - `field_name`：字段名按字面含义，业务语义需由领域方确认。
  - `description`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_research_projects

- 表用途说明：基于表名 `dtlms_research_projects` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `project_code`：字段名按字面含义，业务语义需由领域方确认。
  - `project_name`：字段名按字面含义，业务语义需由领域方确认。
  - `principal_advisor_id`：外键，引用相关实体的 `id`。
  - `funding_amount`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_reviewer_assignments

- 表用途说明：基于表名 `dtlms_reviewer_assignments` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `reviewer_username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `reviewer_role`：字段名按字面含义，业务语义需由领域方确认。
  - `assignment_status`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_role_permissions

- 表用途说明：基于表名 `dtlms_role_permissions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `role_id`：主键或外键，引用相关实体的 `id`。
  - `permission_id`：主键或外键，引用相关实体的 `id`。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_roles

- 表用途说明：基于表名 `dtlms_roles` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `role_code`：字段名按字面含义，业务语义需由领域方确认。
  - `role_name`：字段名按字面含义，业务语义需由领域方确认。
  - `description`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `scope_name`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_schema_migrations

- 表用途说明：基于表名 `dtlms_schema_migrations` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `file_name`：资源或附件的 URL/路径。
  - `applied_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_scientific_reports

- 表用途说明：基于表名 `dtlms_scientific_reports` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `training_plan_id`：外键，引用相关实体的 `id`。
  - `period_label`：字段名按字面含义，业务语义需由领域方确认。
  - `report_status`：字段名按字面含义，业务语义需由领域方确认。
  - `summary`：文本说明/备注字段。
  - `attachment_url`：资源或附件的 URL/路径。
  - `reviewer_advisor_id`：外键，引用相关实体的 `id`。
  - `review_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `review_comment`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。



### dtlms_student_advisor_history

- 表用途说明：基于表名 `dtlms_student_advisor_history` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_id`：主键或外键，引用相关实体的 `id`。
  - `relation_type`：字段名按字面含义，业务语义需由领域方确认。
  - `start_date`：字段名按字面含义，业务语义需由领域方确认。
  - `end_date`：字段名按字面含义，业务语义需由领域方确认。
  - `change_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_student_team_history

- 表用途说明：基于表名 `dtlms_student_team_history` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `team_id`：主键或外键，引用相关实体的 `id`。
  - `start_date`：字段名按字面含义，业务语义需由领域方确认。
  - `end_date`：字段名按字面含义，业务语义需由领域方确认。
  - `change_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_students

- 表用途说明：基于表名 `dtlms_students` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_no`：字段名按字面含义，业务语义需由领域方确认。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `gender`：字段名按字面含义，业务语义需由领域方确认。
  - `political_status`：字段名按字面含义，业务语义需由领域方确认。
  - `phone_number`：联系电话或移动电话。
  - `identity_no`：字段名按字面含义，业务语义需由领域方确认。
  - `enrollment_year`：字段名按字面含义，业务语义需由领域方确认。
  - `degree_type`：字段名按字面含义，业务语义需由领域方确认。
  - `team_name`：字段名按字面含义，业务语义需由领域方确认。
  - `current_status`：字段名按字面含义，业务语义需由领域方确认。
  - `primary_advisor_id`：外键，引用相关实体的 `id`。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `team_id`：主键或外键，引用相关实体的 `id`。
  - `portal_student_id`：外键，引用相关实体的 `id`。



### dtlms_system_configs

- 表用途说明：基于表名 `dtlms_system_configs` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `config_key`：字段名按字面含义，业务语义需由领域方确认。
  - `config_value`：字段名按字面含义，业务语义需由领域方确认。
  - `description`：文本说明/备注字段。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_team_advisors

- 表用途说明：基于表名 `dtlms_team_advisors` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `team_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_role`：字段名按字面含义，业务语义需由领域方确认。
  - `joined_on`：字段名按字面含义，业务语义需由领域方确认。
  - `left_on`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `advisor_user_id`：外键，引用相关实体的 `id`。



### dtlms_teams

- 表用途说明：基于表名 `dtlms_teams` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `team_code`：字段名按字面含义，业务语义需由领域方确认。
  - `team_name`：字段名按字面含义，业务语义需由领域方确认。
  - `department_name`：字段名按字面含义，业务语义需由领域方确认。
  - `discipline_name`：字段名按字面含义，业务语义需由领域方确认。
  - `lead_advisor_id`：外键，引用相关实体的 `id`。
  - `research_directions`：字段名按字面含义，业务语义需由领域方确认。
  - `team_status`：字段名按字面含义，业务语义需由领域方确认。
  - `established_on`：字段名按字面含义，业务语义需由领域方确认。
  - `description`：文本说明/备注字段。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `lead_user_id`：外键，引用相关实体的 `id`。



### dtlms_theses

- 表用途说明：基于表名 `dtlms_theses` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_id`：主键或外键，引用相关实体的 `id`。
  - `title`：字段名按字面含义，业务语义需由领域方确认。
  - `plagiarism_rate`：字段名按字面含义，业务语义需由领域方确认。
  - `thesis_status`：字段名按字面含义，业务语义需由领域方确认。
  - `blind_review_status`：字段名按字面含义，业务语义需由领域方确认。
  - `defense_date`：字段名按字面含义，业务语义需由领域方确认。
  - `degree_granted`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `business_key`：业务唯一标识，用于跨系统或幂等性校验。



### dtlms_thesis_reviews

- 表用途说明：基于表名 `dtlms_thesis_reviews` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `thesis_id`：主键或外键，引用相关实体的 `id`。
  - `expert_name`：字段名按字面含义，业务语义需由领域方确认。
  - `review_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `review_status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `review_comment`：文本说明/备注字段。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_training_plan_versions

- 表用途说明：基于表名 `dtlms_training_plan_versions` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `training_plan_id`：外键，引用相关实体的 `id`。
  - `version_no`：字段名按字面含义，业务语义需由领域方确认。
  - `change_reason`：字段名按字面含义，业务语义需由领域方确认。
  - `plan_snapshot`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_training_plans

- 表用途说明：基于表名 `dtlms_training_plans` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `student_id`：主键或外键，引用相关实体的 `id`。
  - `advisor_id`：主键或外键，引用相关实体的 `id`。
  - `version_no`：字段名按字面含义，业务语义需由领域方确认。
  - `report_cycle`：字段名按字面含义，业务语义需由领域方确认。
  - `plan_status`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `scientific_goal`：字段名按字面含义，业务语义需由领域方确认。
  - `assessment_rule`：字段名按字面含义，业务语义需由领域方确认。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_user_profiles

- 表用途说明：基于表名 `dtlms_user_profiles` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `role_name`：字段名按字面含义，业务语义需由领域方确认。
  - `department_name`：字段名按字面含义，业务语义需由领域方确认。
  - `phone_number`：联系电话或移动电话。
  - `email`：电子邮箱地址。
  - `theme_color`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `introduction`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_user_roles

- 表用途说明：基于表名 `dtlms_user_roles` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `user_id`：主键或外键，引用相关实体的 `id`。
  - `role_id`：主键或外键，引用相关实体的 `id`。
  - `grant_source`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_users

- 表用途说明：基于表名 `dtlms_users` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `username`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `full_name`：用户名或显示名字符串，用于标识用户账户/姓名。
  - `email`：电子邮箱地址。
  - `password_hash`：字段名按字面含义，业务语义需由领域方确认。
  - `is_active`：状态字段，通常为有限枚举值，请参照业务文档或字典表。
  - `is_deleted`：逻辑删除标志，`true` 表示已删除（软删除）。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `department_name`：字段名按字面含义，业务语义需由领域方确认。
  - `phone_number`：联系电话或移动电话。
  - `last_login_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



### dtlms_wf_de_model

- 表用途说明：基于表名 `dtlms_wf_de_model` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `key_`：字段名按字面含义，业务语义需由领域方确认。
  - `category_`：字段名按字面含义，业务语义需由领域方确认。
  - `version_`：字段名按字面含义，业务语义需由领域方确认。
  - `model_type_`：字段名按字面含义，业务语义需由领域方确认。
  - `description_`：字段名按字面含义，业务语义需由领域方确认。
  - `meta_info_`：字段名按字面含义，业务语义需由领域方确认。
  - `created_`：字段名按字面含义，业务语义需由领域方确认。
  - `last_updated_`：字段名按字面含义，业务语义需由领域方确认。
  - `tenant_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `deployment_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `resource_name_`：字段名按字面含义，业务语义需由领域方确认。
  - `editor_source_value_`：字段名按字面含义，业务语义需由领域方确认。
  - `editor_source_extra_value_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_hi_actinst

- 表用途说明：基于表名 `dtlms_wf_hi_actinst` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_def_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `exec_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `act_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `act_name_`：字段名按字面含义，业务语义需由领域方确认。
  - `act_type_`：字段名按字面含义，业务语义需由领域方确认。
  - `assignee_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `end_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `duration_ms_`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_hi_procinst

- 表用途说明：基于表名 `dtlms_wf_hi_procinst` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_def_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `end_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `duration_ms_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_user_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `end_act_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `delete_reason_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_act_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `state_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_hi_taskinst

- 表用途说明：基于表名 `dtlms_wf_hi_taskinst` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `task_def_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_def_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `exec_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `assignee_`：字段名按字面含义，业务语义需由领域方确认。
  - `owner_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `claim_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `end_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `duration_ms_`：字段名按字面含义，业务语义需由领域方确认。
  - `due_date_`：字段名按字面含义，业务语义需由领域方确认。
  - `delete_reason_`：字段名按字面含义，业务语义需由领域方确认。
  - `priority_`：字段名按字面含义，业务语义需由领域方确认。
  - `category_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_hi_varinst

- 表用途说明：基于表名 `dtlms_wf_hi_varinst` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `exec_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `task_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `var_type_`：字段名按字面含义，业务语义需由领域方确认。
  - `text_value_`：字段名按字面含义，业务语义需由领域方确认。
  - `number_value_`：字段名按字面含义，业务语义需由领域方确认。
  - `json_value_`：JSON/JSONB 字段，存放结构化或半结构化数据。
  - `create_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `last_updated_time_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_re_deployment

- 表用途说明：基于表名 `dtlms_wf_re_deployment` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `category_`：字段名按字面含义，业务语义需由领域方确认。
  - `key_`：字段名按字面含义，业务语义需由领域方确认。
  - `deploy_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `tenant_id_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_re_procdef

- 表用途说明：基于表名 `dtlms_wf_re_procdef` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `key_`：字段名按字面含义，业务语义需由领域方确认。
  - `version_`：字段名按字面含义，业务语义需由领域方确认。
  - `deployment_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `resource_name_`：字段名按字面含义，业务语义需由领域方确认。
  - `diagram_resource_name_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `category_`：字段名按字面含义，业务语义需由领域方确认。
  - `description_`：字段名按字面含义，业务语义需由领域方确认。
  - `suspension_state_`：字段名按字面含义，业务语义需由领域方确认。
  - `tenant_id_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_ru_execution

- 表用途说明：基于表名 `dtlms_wf_ru_execution` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_def_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `parent_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `act_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `is_active_`：字段名按字面含义，业务语义需由领域方确认。
  - `is_concurrent_`：字段名按字面含义，业务语义需由领域方确认。
  - `is_scope_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `start_user_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `super_exec_`：字段名按字面含义，业务语义需由领域方确认。
  - `tenant_id_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_ru_identitylink

- 表用途说明：基于表名 `dtlms_wf_ru_identitylink` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `task_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `user_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `group_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `link_type_`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_ru_task

- 表用途说明：基于表名 `dtlms_wf_ru_task` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `exec_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_def_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `task_def_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `business_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `assignee_`：字段名按字面含义，业务语义需由领域方确认。
  - `owner_`：字段名按字面含义，业务语义需由领域方确认。
  - `create_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `due_date_`：字段名按字面含义，业务语义需由领域方确认。
  - `claim_time_`：字段名按字面含义，业务语义需由领域方确认。
  - `priority_`：字段名按字面含义，业务语义需由领域方确认。
  - `suspension_state_`：字段名按字面含义，业务语义需由领域方确认。
  - `tenant_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `form_key_`：字段名按字面含义，业务语义需由领域方确认。
  - `description_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_wf_ru_variable

- 表用途说明：基于表名 `dtlms_wf_ru_variable` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id_`：字段名按字面含义，业务语义需由领域方确认。
  - `exec_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `proc_inst_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `task_id_`：字段名按字面含义，业务语义需由领域方确认。
  - `name_`：字段名按字面含义，业务语义需由领域方确认。
  - `var_type_`：字段名按字面含义，业务语义需由领域方确认。
  - `text_value_`：字段名按字面含义，业务语义需由领域方确认。
  - `number_value_`：字段名按字面含义，业务语义需由领域方确认。
  - `json_value_`：JSON/JSONB 字段，存放结构化或半结构化数据。
  - `create_time_`：字段名按字面含义，业务语义需由领域方确认。



### dtlms_written_exam_scores

- 表用途说明：基于表名 `dtlms_written_exam_scores` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。

- 字段说明：

  - `Column`：字段名按字面含义，业务语义需由领域方确认。
  - `id`：主键或外键，引用相关实体的 `id`。
  - `application_id`：主键或外键，引用相关实体的 `id`。
  - `exam_date`：字段名按字面含义，业务语义需由领域方确认。
  - `exam_score`：数值评分字段，通常为 `numeric` 或 `integer`。
  - `import_batch_no`：字段名按字面含义，业务语义需由领域方确认。
  - `created_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。
  - `updated_at`：时间戳，记录事件时间，通常为 `timestamp with time zone`。



<!-- END auto-generated table descriptions -->