# 数据库 Schema 文档

> 自动生成，请勿手工修改。下次数据库结构变更后再次运行 `backend/sql/_extract_schema.py` 重新生成。

- 数据源: `host=47.117.107.23 port=15431 dbname=test062601`
- Schema: `public`
- 表格数量: 74
- 视图数量: 4
- 函数/存储过程数量: 0
- 序列数量: 55
- 索引数量: 167

## 目录

- [表（Tables）](#表tables)
- [视图（Views）](#视图views)
- [枚举/复合类型（Enums / Composite Types）](#枚举复合类型enums--composite-types)
- [序列（Sequences）](#序列sequences)
- [函数 / 存储过程（Functions）](#函数--存储过程functions)
- [索引（Indexes）](#索引indexes)
- [触发器（Triggers）](#触发器triggers)
- [表级约束（Table Constraints）](#表级约束table-constraints)

## 表（Tables）

### `dtlms_achievements`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_achievements_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `achievement_type` | character varying(32) | NO |  |
| `title` | character varying(255) | NO |  |
| `published_at` | date | YES |  |
| `publisher_name` | character varying(255) | YES |  |
| `ranking_text` | character varying(64) | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_achievements_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_achievements_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_achievements_pkey`: `CREATE UNIQUE INDEX dtlms_achievements_pkey ON public.dtlms_achievements USING btree (id)`

### `dtlms_admission_decisions`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_admission_decisions_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `decision_status` | character varying(32) | NO | 'pending'::character varying |
| `rank_no` | integer(32,0) | YES |  |
| `final_score` | numeric(5,2) | YES |  |
| `transfer_option` | character varying(64) | YES |  |
| `decision_comment` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_admission_decisions_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_admission_decisions_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_admission_decisions_pkey`: `CREATE UNIQUE INDEX dtlms_admission_decisions_pkey ON public.dtlms_admission_decisions USING btree (id)`
- `idx_admission_decision_status`: `CREATE INDEX idx_admission_decision_status ON public.dtlms_admission_decisions USING btree (decision_status)`

### `dtlms_advisor_screening_batches`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_advisor_screening_batches_id_seq'::regclass) |
| `advisor_user_id` | bigint(64,0) | YES |  |
| `advisor_username` | character varying(64) | NO |  |
| `advisor_name` | character varying(128) | YES |  |
| `advisor_role_code` | character varying(64) | NO | 'advisor'::character varying |
| `screening_round` | character varying(32) | NO |  |
| `signature_base64` | text | NO |  |
| `submitted_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_advisor_screening_batches_round` | CHECK | `CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text])))` |
| `dtlms_advisor_screening_batches_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_advisor_screening_batches_pkey`: `CREATE UNIQUE INDEX dtlms_advisor_screening_batches_pkey ON public.dtlms_advisor_screening_batches USING btree (id)`
- `idx_advisor_screening_batches_advisor_round`: `CREATE INDEX idx_advisor_screening_batches_advisor_round ON public.dtlms_advisor_screening_batches USING btree (advisor_username, screening_round, submitted_at DESC)`

### `dtlms_advisor_screening_items`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_advisor_screening_items_id_seq'::regclass) |
| `batch_id` | bigint(64,0) | NO |  |
| `application_id` | bigint(64,0) | NO |  |
| `business_key` | character varying(64) | NO |  |
| `candidate_no` | character varying(64) | NO |  |
| `screening_round` | character varying(32) | NO |  |
| `advisor_score` | numeric(5,2) | NO |  |
| `is_passed` | boolean | NO |  |
| `screening_status` | character varying(32) | NO | 'submitted'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_advisor_screening_items_round` | CHECK | `CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text])))` |
| `chk_advisor_screening_items_score_range` | CHECK | `CHECK (((advisor_score >= (0)::numeric) AND (advisor_score <= (100)::numeric)))` |
| `dtlms_advisor_screening_items_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_advisor_screening_items_batch_id_fkey` | FOREIGN KEY | `FOREIGN KEY (batch_id) REFERENCES dtlms_advisor_screening_batches(id) ON DELETE CASCADE` |
| `dtlms_advisor_screening_items_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `uq_advisor_screening_items_application_round` | UNIQUE | `UNIQUE (application_id, screening_round)` |
| `uq_advisor_screening_items_candidate_round` | UNIQUE | `UNIQUE (candidate_no, screening_round)` |

**索引**

- `dtlms_advisor_screening_items_pkey`: `CREATE UNIQUE INDEX dtlms_advisor_screening_items_pkey ON public.dtlms_advisor_screening_items USING btree (id)`
- `idx_advisor_screening_items_application`: `CREATE INDEX idx_advisor_screening_items_application ON public.dtlms_advisor_screening_items USING btree (application_id, screening_round, created_at DESC)`
- `idx_advisor_screening_items_batch`: `CREATE INDEX idx_advisor_screening_items_batch ON public.dtlms_advisor_screening_items USING btree (batch_id)`
- `idx_advisor_screening_items_business_key`: `CREATE INDEX idx_advisor_screening_items_business_key ON public.dtlms_advisor_screening_items USING btree (business_key)`
- `uq_advisor_screening_items_application_round`: `CREATE UNIQUE INDEX uq_advisor_screening_items_application_round ON public.dtlms_advisor_screening_items USING btree (application_id, screening_round)`
- `uq_advisor_screening_items_candidate_round`: `CREATE UNIQUE INDEX uq_advisor_screening_items_candidate_round ON public.dtlms_advisor_screening_items USING btree (candidate_no, screening_round)`

### `dtlms_advisors`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_advisors_id_seq'::regclass) |
| `advisor_no` | character varying(32) | NO |  |
| `full_name` | character varying(128) | NO |  |
| `title` | character varying(64) | NO |  |
| `organization_name` | character varying(128) | NO |  |
| `research_direction` | character varying(255) | NO |  |
| `annual_quota` | integer(32,0) | NO | 0 |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `user_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `fk_dtlms_advisors_user_id` | FOREIGN KEY | `FOREIGN KEY (user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `dtlms_advisors_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_advisors_advisor_no_key` | UNIQUE | `UNIQUE (advisor_no)` |

**索引**

- `dtlms_advisors_advisor_no_key`: `CREATE UNIQUE INDEX dtlms_advisors_advisor_no_key ON public.dtlms_advisors USING btree (advisor_no)`
- `dtlms_advisors_pkey`: `CREATE UNIQUE INDEX dtlms_advisors_pkey ON public.dtlms_advisors USING btree (id)`
- `idx_dtlms_advisors_user_id`: `CREATE UNIQUE INDEX idx_dtlms_advisors_user_id ON public.dtlms_advisors USING btree (user_id) WHERE (user_id IS NOT NULL)`

### `dtlms_application_materials`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_application_materials_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `material_type` | character varying(64) | NO |  |
| `material_status` | character varying(32) | NO | 'pending'::character varying |
| `file_url` | character varying(255) | NO |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_application_materials_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_application_materials_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_application_materials_pkey`: `CREATE UNIQUE INDEX dtlms_application_materials_pkey ON public.dtlms_application_materials USING btree (id)`

### `dtlms_audit_policies`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO |  |
| `item` | character varying(128) | NO |  |
| `policy` | text | NO |  |
| `status` | character varying(32) | NO | '启用'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `is_deleted` | boolean | NO | false |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_audit_policies_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_audit_policies_pkey`: `CREATE UNIQUE INDEX dtlms_audit_policies_pkey ON public.dtlms_audit_policies USING btree (id)`

### `dtlms_background_assessments`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_background_assessments_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `evaluator_user_id` | bigint(64,0) | YES |  |
| `evaluator_username` | character varying(64) | NO |  |
| `evaluator_name` | character varying(128) | YES |  |
| `evaluator_role_code` | character varying(64) | NO |  |
| `assessment_result` | character varying(32) | NO |  |
| `assessment_comment` | text | YES |  |
| `assessed_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_background_assessments_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_background_assessments_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_background_assessments_application_id_evaluator_usern_key` | UNIQUE | `UNIQUE (application_id, evaluator_username)` |

**索引**

- `dtlms_background_assessments_application_id_evaluator_usern_key`: `CREATE UNIQUE INDEX dtlms_background_assessments_application_id_evaluator_usern_key ON public.dtlms_background_assessments USING btree (application_id, evaluator_username)`
- `dtlms_background_assessments_pkey`: `CREATE UNIQUE INDEX dtlms_background_assessments_pkey ON public.dtlms_background_assessments USING btree (id)`
- `idx_background_assessment_application`: `CREATE INDEX idx_background_assessment_application ON public.dtlms_background_assessments USING btree (application_id, assessed_at DESC)`
- `idx_background_assessment_result`: `CREATE INDEX idx_background_assessment_result ON public.dtlms_background_assessments USING btree (assessment_result)`

### `dtlms_data_sync_logs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_data_sync_logs_id_seq'::regclass) |
| `source_system` | character varying(64) | NO |  |
| `target_system` | character varying(64) | NO |  |
| `sync_status` | character varying(32) | NO |  |
| `record_count` | integer(32,0) | NO | 0 |
| `failure_reason` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_data_sync_logs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_data_sync_logs_pkey`: `CREATE UNIQUE INDEX dtlms_data_sync_logs_pkey ON public.dtlms_data_sync_logs USING btree (id)`
- `idx_sync_logs_source_target`: `CREATE INDEX idx_sync_logs_source_target ON public.dtlms_data_sync_logs USING btree (source_system, target_system, created_at)`

### `dtlms_dict_data`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_dict_data_id_seq'::regclass) |
| `dict_type_id` | bigint(64,0) | NO |  |
| `dict_type` | character varying(100) | NO |  |
| `label` | character varying(100) | NO |  |
| `value` | character varying(100) | NO |  |
| `sort_order` | integer(32,0) | NO | 0 |
| `status` | character varying(32) | NO | '启用'::character varying |
| `color_type` | character varying(32) | YES |  |
| `css_class` | character varying(128) | YES |  |
| `remark` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_dict_data_status_check` | CHECK | `CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))` |
| `dtlms_dict_data_dict_type_id_fkey` | FOREIGN KEY | `FOREIGN KEY (dict_type_id) REFERENCES dtlms_dict_types(id)` |
| `dtlms_dict_data_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_dict_data_dict_type_value_key` | UNIQUE | `UNIQUE (dict_type, value)` |

**索引**

- `dtlms_dict_data_dict_type_value_key`: `CREATE UNIQUE INDEX dtlms_dict_data_dict_type_value_key ON public.dtlms_dict_data USING btree (dict_type, value)`
- `dtlms_dict_data_pkey`: `CREATE UNIQUE INDEX dtlms_dict_data_pkey ON public.dtlms_dict_data USING btree (id)`
- `idx_dtlms_dict_data_type_sort`: `CREATE INDEX idx_dtlms_dict_data_type_sort ON public.dtlms_dict_data USING btree (dict_type, sort_order, id)`

### `dtlms_dict_types`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_dict_types_id_seq'::regclass) |
| `dict_name` | character varying(100) | NO |  |
| `dict_type` | character varying(100) | NO |  |
| `status` | character varying(32) | NO | '启用'::character varying |
| `remark` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_dict_types_status_check` | CHECK | `CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))` |
| `dtlms_dict_types_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_dict_types_dict_type_key` | UNIQUE | `UNIQUE (dict_type)` |

**索引**

- `dtlms_dict_types_dict_type_key`: `CREATE UNIQUE INDEX dtlms_dict_types_dict_type_key ON public.dtlms_dict_types USING btree (dict_type)`
- `dtlms_dict_types_pkey`: `CREATE UNIQUE INDEX dtlms_dict_types_pkey ON public.dtlms_dict_types USING btree (id)`

### `dtlms_initial_screening_confirmations`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_initial_screening_confirmations_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `business_key` | character varying(64) | NO |  |
| `candidate_no` | character varying(64) | NO |  |
| `confirmer_user_id` | bigint(64,0) | YES |  |
| `confirmer_username` | character varying(64) | NO |  |
| `confirmer_name` | character varying(128) | YES |  |
| `confirmer_role_code` | character varying(64) | NO |  |
| `confirmation_result` | character varying(32) | NO |  |
| `confirmation_comment` | text | YES |  |
| `confirmed_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_initial_screening_confirmations_result` | CHECK | `CHECK (((confirmation_result)::text = ANY (ARRAY[('passed'::character varying)::text, ('rejected'::character varying)::text])))` |
| `dtlms_initial_screening_confirmations_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_initial_screening_confirmations_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `uq_initial_screening_confirmations_application` | UNIQUE | `UNIQUE (application_id)` |

**索引**

- `dtlms_initial_screening_confirmations_pkey`: `CREATE UNIQUE INDEX dtlms_initial_screening_confirmations_pkey ON public.dtlms_initial_screening_confirmations USING btree (id)`
- `idx_initial_screening_confirmations_application`: `CREATE INDEX idx_initial_screening_confirmations_application ON public.dtlms_initial_screening_confirmations USING btree (application_id, confirmed_at DESC)`
- `uq_initial_screening_confirmations_application`: `CREATE UNIQUE INDEX uq_initial_screening_confirmations_application ON public.dtlms_initial_screening_confirmations USING btree (application_id)`

### `dtlms_initial_screening_notifications`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_initial_screening_notifications_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `business_key` | character varying(64) | NO |  |
| `notification_channel` | character varying(32) | NO |  |
| `notification_event` | character varying(64) | NO |  |
| `notification_status` | character varying(32) | NO | 'pending'::character varying |
| `recipient_address` | character varying(255) | YES |  |
| `recipient_user_id` | bigint(64,0) | YES |  |
| `recipient_username` | character varying(64) | YES |  |
| `payload_json` | jsonb | YES |  |
| `sent_at` | timestamp with time zone | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_initial_screening_notifications_channel` | CHECK | `CHECK (((notification_channel)::text = ANY (ARRAY[('email'::character varying)::text, ('site_message'::character varying)::text])))` |
| `chk_initial_screening_notifications_status` | CHECK | `CHECK (((notification_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('sent'::character varying)::text, ('failed'::character varying)::text])))` |
| `dtlms_initial_screening_notifications_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_initial_screening_notifications_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_initial_screening_notifications_pkey`: `CREATE UNIQUE INDEX dtlms_initial_screening_notifications_pkey ON public.dtlms_initial_screening_notifications USING btree (id)`
- `idx_initial_screening_notifications_application`: `CREATE INDEX idx_initial_screening_notifications_application ON public.dtlms_initial_screening_notifications USING btree (application_id, created_at DESC)`
- `idx_initial_screening_notifications_status`: `CREATE INDEX idx_initial_screening_notifications_status ON public.dtlms_initial_screening_notifications USING btree (notification_status, notification_channel)`

### `dtlms_integrations`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO |  |
| `name` | character varying(128) | NO |  |
| `direction` | character varying(64) | NO |  |
| `cadence` | character varying(64) | NO |  |
| `status` | character varying(32) | NO | '正常'::character varying |
| `owner` | character varying(128) | NO | ''::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `is_deleted` | boolean | NO | false |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_integrations_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_integrations_pkey`: `CREATE UNIQUE INDEX dtlms_integrations_pkey ON public.dtlms_integrations USING btree (id)`

### `dtlms_interview_groups`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_interview_groups_id_seq'::regclass) |
| `plan_id` | bigint(64,0) | NO |  |
| `group_code` | character varying(64) | NO |  |
| `group_name` | character varying(128) | NO |  |
| `interview_mode` | character varying(32) | NO | 'offline'::character varying |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_interview_groups_plan_id_fkey` | FOREIGN KEY | `FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id)` |
| `dtlms_interview_groups_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_interview_groups_plan_id_group_code_key` | UNIQUE | `UNIQUE (plan_id, group_code)` |

**索引**

- `dtlms_interview_groups_pkey`: `CREATE UNIQUE INDEX dtlms_interview_groups_pkey ON public.dtlms_interview_groups USING btree (id)`
- `dtlms_interview_groups_plan_id_group_code_key`: `CREATE UNIQUE INDEX dtlms_interview_groups_plan_id_group_code_key ON public.dtlms_interview_groups USING btree (plan_id, group_code)`

### `dtlms_interview_schedules`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_interview_schedules_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `interview_group_id` | bigint(64,0) | NO |  |
| `admission_ticket_no` | character varying(64) | NO |  |
| `starts_at` | timestamp with time zone | NO |  |
| `ends_at` | timestamp with time zone | NO |  |
| `schedule_status` | character varying(32) | NO | 'scheduled'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_interview_schedules_check` | CHECK | `CHECK ((ends_at >= starts_at))` |
| `dtlms_interview_schedules_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_interview_schedules_interview_group_id_fkey` | FOREIGN KEY | `FOREIGN KEY (interview_group_id) REFERENCES dtlms_interview_groups(id)` |
| `dtlms_interview_schedules_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_interview_schedules_admission_ticket_no_key` | UNIQUE | `UNIQUE (admission_ticket_no)` |

**索引**

- `dtlms_interview_schedules_admission_ticket_no_key`: `CREATE UNIQUE INDEX dtlms_interview_schedules_admission_ticket_no_key ON public.dtlms_interview_schedules USING btree (admission_ticket_no)`
- `dtlms_interview_schedules_pkey`: `CREATE UNIQUE INDEX dtlms_interview_schedules_pkey ON public.dtlms_interview_schedules USING btree (id)`
- `idx_interview_schedule_time`: `CREATE INDEX idx_interview_schedule_time ON public.dtlms_interview_schedules USING btree (starts_at, ends_at)`

### `dtlms_interview_scores`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_interview_scores_id_seq'::regclass) |
| `schedule_id` | bigint(64,0) | NO |  |
| `evaluator_username` | character varying(64) | NO |  |
| `single_choice_score` | numeric(5,2) | YES |  |
| `fill_blank_score` | numeric(5,2) | YES |  |
| `coding_score` | numeric(5,2) | YES |  |
| `interview_score` | numeric(5,2) | YES |  |
| `ideological_score` | numeric(5,2) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_interview_scores_schedule_id_fkey` | FOREIGN KEY | `FOREIGN KEY (schedule_id) REFERENCES dtlms_interview_schedules(id)` |
| `dtlms_interview_scores_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_interview_scores_pkey`: `CREATE UNIQUE INDEX dtlms_interview_scores_pkey ON public.dtlms_interview_scores USING btree (id)`

### `dtlms_login_logs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_login_logs_id_seq'::regclass) |
| `username` | character varying(64) | NO |  |
| `login_status` | character varying(32) | NO |  |
| `login_ip` | character varying(64) | YES |  |
| `user_agent` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_login_logs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_login_logs_pkey`: `CREATE UNIQUE INDEX dtlms_login_logs_pkey ON public.dtlms_login_logs USING btree (id)`

### `dtlms_material_scores`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_material_scores_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `reviewer_assignment_id` | bigint(64,0) | NO |  |
| `material_score` | numeric(5,2) | YES |  |
| `recommendation_text` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_material_scores_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_material_scores_reviewer_assignment_id_fkey` | FOREIGN KEY | `FOREIGN KEY (reviewer_assignment_id) REFERENCES dtlms_reviewer_assignments(id)` |
| `dtlms_material_scores_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_material_scores_pkey`: `CREATE UNIQUE INDEX dtlms_material_scores_pkey ON public.dtlms_material_scores USING btree (id)`

### `dtlms_news_articles`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_news_articles_id_seq'::regclass) |
| `news_code` | character varying(64) | NO |  |
| `news_title` | character varying(255) | NO |  |
| `news_content` | text | NO |  |
| `news_type` | character varying(100) | NO |  |
| `publisher_user_id` | bigint(64,0) | YES |  |
| `publisher_username` | character varying(64) | YES |  |
| `publisher_name` | character varying(128) | YES |  |
| `reviewer_user_id` | bigint(64,0) | YES |  |
| `reviewer_username` | character varying(64) | YES |  |
| `reviewer_name` | character varying(128) | YES |  |
| `published_at` | timestamp with time zone | YES |  |
| `status` | character varying(32) | NO | '草稿'::character varying |
| `is_pinned` | boolean | NO | false |
| `display_order` | integer(32,0) | NO | 0 |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_dtlms_news_articles_status` | CHECK | `CHECK (((status)::text = ANY (ARRAY[('草稿'::character varying)::text, ('待发布'::character varying)::text, ('已发布'::character varying)::text, ('已下线'::character varying)::text])))` |
| `chk_dtlms_news_articles_type` | CHECK | `CHECK (((news_type)::text = ANY (ARRAY[('学生门户通知消息'::character varying)::text, ('学生门户新闻信息'::character varying)::text])))` |
| `dtlms_news_articles_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_news_articles_news_code_key` | UNIQUE | `UNIQUE (news_code)` |

**索引**

- `dtlms_news_articles_news_code_key`: `CREATE UNIQUE INDEX dtlms_news_articles_news_code_key ON public.dtlms_news_articles USING btree (news_code)`
- `dtlms_news_articles_pkey`: `CREATE UNIQUE INDEX dtlms_news_articles_pkey ON public.dtlms_news_articles USING btree (id)`
- `idx_dtlms_news_articles_deleted_order`: `CREATE INDEX idx_dtlms_news_articles_deleted_order ON public.dtlms_news_articles USING btree (is_deleted, display_order DESC, id DESC)`
- `idx_dtlms_news_articles_status_published`: `CREATE INDEX idx_dtlms_news_articles_status_published ON public.dtlms_news_articles USING btree (status, published_at DESC, display_order DESC, id DESC) WHERE (is_deleted = false)`
- `idx_dtlms_news_articles_type_status`: `CREATE INDEX idx_dtlms_news_articles_type_status ON public.dtlms_news_articles USING btree (news_type, status, published_at DESC, id DESC) WHERE (is_deleted = false)`

### `dtlms_notification_delivery_logs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_notification_delivery_logs_id_seq'::regclass) |
| `channel` | character varying(32) | NO |  |
| `template_code` | character varying(64) | YES |  |
| `recipient` | character varying(255) | NO |  |
| `subject` | character varying(255) | NO |  |
| `send_status` | character varying(32) | NO |  |
| `failure_reason` | text | YES |  |
| `business_key` | character varying(64) | YES |  |
| `triggered_by` | character varying(64) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_notification_delivery_logs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_notification_delivery_logs_pkey`: `CREATE UNIQUE INDEX dtlms_notification_delivery_logs_pkey ON public.dtlms_notification_delivery_logs USING btree (id)`
- `idx_notification_delivery_logs_channel_time`: `CREATE INDEX idx_notification_delivery_logs_channel_time ON public.dtlms_notification_delivery_logs USING btree (channel, created_at)`
- `idx_notification_delivery_logs_recipient`: `CREATE INDEX idx_notification_delivery_logs_recipient ON public.dtlms_notification_delivery_logs USING btree (recipient)`
- `idx_notification_delivery_logs_status_time`: `CREATE INDEX idx_notification_delivery_logs_status_time ON public.dtlms_notification_delivery_logs USING btree (send_status, created_at)`

### `dtlms_notification_templates`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_notification_templates_id_seq'::regclass) |
| `template_code` | character varying(64) | NO |  |
| `channel` | character varying(32) | NO |  |
| `title` | character varying(128) | NO |  |
| `content_template` | text | NO |  |
| `variables_schema` | jsonb | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_notification_templates_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_notification_templates_template_code_key` | UNIQUE | `UNIQUE (template_code)` |

**索引**

- `dtlms_notification_templates_pkey`: `CREATE UNIQUE INDEX dtlms_notification_templates_pkey ON public.dtlms_notification_templates USING btree (id)`
- `dtlms_notification_templates_template_code_key`: `CREATE UNIQUE INDEX dtlms_notification_templates_template_code_key ON public.dtlms_notification_templates USING btree (template_code)`

### `dtlms_operation_logs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_operation_logs_id_seq'::regclass) |
| `operator_username` | character varying(64) | NO |  |
| `operator_role` | character varying(64) | NO |  |
| `module_name` | character varying(64) | NO |  |
| `entity_name` | character varying(64) | NO |  |
| `entity_id` | character varying(64) | NO |  |
| `action` | character varying(32) | NO |  |
| `old_value` | jsonb | YES |  |
| `new_value` | jsonb | YES |  |
| `request_ip` | character varying(64) | YES |  |
| `result` | character varying(32) | NO | 'success'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_operation_logs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_operation_logs_pkey`: `CREATE UNIQUE INDEX dtlms_operation_logs_pkey ON public.dtlms_operation_logs USING btree (id)`
- `idx_operation_logs_entity`: `CREATE INDEX idx_operation_logs_entity ON public.dtlms_operation_logs USING btree (entity_name, entity_id)`
- `idx_operation_logs_module_time`: `CREATE INDEX idx_operation_logs_module_time ON public.dtlms_operation_logs USING btree (module_name, created_at)`

### `dtlms_outbound_studies`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_outbound_studies_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `advisor_id` | bigint(64,0) | NO |  |
| `study_type` | character varying(64) | NO |  |
| `destination` | character varying(128) | NO |  |
| `start_date` | date | NO |  |
| `end_date` | date | NO |  |
| `approval_status` | character varying(32) | NO | 'submitted'::character varying |
| `expected_outcome` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `business_key` | character varying(64) | NO |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_outbound_studies_check` | CHECK | `CHECK ((end_date >= start_date))` |
| `dtlms_outbound_studies_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_outbound_studies_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_outbound_studies_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_outbound_studies_pkey`: `CREATE UNIQUE INDEX dtlms_outbound_studies_pkey ON public.dtlms_outbound_studies USING btree (id)`
- `idx_outbound_studies_status`: `CREATE INDEX idx_outbound_studies_status ON public.dtlms_outbound_studies USING btree (approval_status)`
- `ux_dtlms_outbound_studies_business_key`: `CREATE UNIQUE INDEX ux_dtlms_outbound_studies_business_key ON public.dtlms_outbound_studies USING btree (business_key)`

### `dtlms_permissions`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_permissions_id_seq'::regclass) |
| `permission_code` | character varying(128) | NO |  |
| `permission_name` | character varying(128) | NO |  |
| `module_name` | character varying(64) | NO |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_permissions_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_permissions_permission_code_key` | UNIQUE | `UNIQUE (permission_code)` |

**索引**

- `dtlms_permissions_permission_code_key`: `CREATE UNIQUE INDEX dtlms_permissions_permission_code_key ON public.dtlms_permissions USING btree (permission_code)`
- `dtlms_permissions_pkey`: `CREATE UNIQUE INDEX dtlms_permissions_pkey ON public.dtlms_permissions USING btree (id)`

### `dtlms_plan_offer`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO |  |
| `candidate_no` | character varying(32) | YES |  |
| `is_agree` | boolean | YES |  |
| `timeout_datetime` | timestamp with time zone | YES |  |
| `portal_student_id` | bigint(64,0) | YES |  |
| `reson` | text | YES |  |
| `offer_url` | character varying(255) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `plan_id` | bigint(64,0) | YES |  |
| `is_sent_mail` | boolean | YES | false |
| `submitted_at` | timestamp with time zone | YES |  |
| `sent_mail_at` | timestamp with time zone | YES |  |
| `hackathon_score` | numeric(5,2) | YES |  |
| `hackathon_comments` | text | YES |  |
| `accepted` | character varying(32) | YES |  |
| `admission_offered_school` | character varying(64) | YES |  |
| `is_in_camp_selection` | boolean | NO | false |
| `accepted_notification_sent_at` | timestamp with time zone | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_plan_offer_accepted_check` | CHECK | `CHECK (((accepted IS NULL) OR ((accepted)::text = ANY (ARRAY[('declined'::character varying)::text, ('pending'::character varying)::text, ('accepted_pending_send'::character varying)::text, ('accepted_sent'::character varying)::text, ('accepted_confirmed'::character varying)::text, ('accepted_rejected'::character varying)::text]))))` |
| `dtlms_plan_offer_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_plan_offer_pkey`: `CREATE UNIQUE INDEX dtlms_plan_offer_pkey ON public.dtlms_plan_offer USING btree (id)`

### `dtlms_portal_application_achievement_records`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_achievement_records_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `achievement_type` | character varying(32) | NO |  |
| `paper_title` | character varying(255) | YES |  |
| `author_order` | character varying(32) | YES |  |
| `journal_or_conference` | character varying(255) | YES |  |
| `publish_or_index_month` | character varying(16) | YES |  |
| `award_name` | character varying(255) | YES |  |
| `awarding_organization` | character varying(255) | YES |  |
| `award_level` | character varying(128) | YES |  |
| `award_year` | character varying(16) | YES |  |
| `responsibility_text` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `achievement_month` | character varying(16) | YES |  |
| `award_rank` | character varying(64) | YES |  |
| `award_certificate_attachment_url` | character varying(512) | YES |  |
| `description_text` | text | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_achievement_record_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_achievement_records_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_achievement_records_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_achievement_records_pkey ON public.dtlms_portal_application_achievement_records USING btree (id)`
- `idx_portal_application_achievement_application`: `CREATE INDEX idx_portal_application_achievement_application ON public.dtlms_portal_application_achievement_records USING btree (application_id, achievement_type)`

### `dtlms_portal_application_attachments`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_attachments_id_seq'::regclass) |
| `portal_student_id` | bigint(64,0) | YES |  |
| `application_id` | bigint(64,0) | YES |  |
| `owner_type` | character varying(64) | NO |  |
| `owner_id` | bigint(64,0) | YES |  |
| `attachment_category` | character varying(64) | NO |  |
| `file_name` | character varying(255) | NO |  |
| `file_url` | text | NO |  |
| `file_type` | character varying(32) | YES |  |
| `file_size` | bigint(64,0) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_attachments_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_attachments_portal_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE` |
| `dtlms_portal_application_attachments_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_attachments_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_attachments_pkey ON public.dtlms_portal_application_attachments USING btree (id)`
- `idx_portal_application_attachment_owner`: `CREATE INDEX idx_portal_application_attachment_owner ON public.dtlms_portal_application_attachments USING btree (application_id, owner_type, owner_id)`

### `dtlms_portal_application_declarations`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `application_id` | bigint(64,0) | NO |  |
| `has_read_declaration` | boolean | NO | false |
| `declaration_text` | text | YES |  |
| `progress_snapshot` | jsonb | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`application_id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_declarations_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_declarations_pkey` | PRIMARY KEY | `PRIMARY KEY (application_id)` |

**索引**

- `dtlms_portal_application_declarations_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_declarations_pkey ON public.dtlms_portal_application_declarations USING btree (application_id)`

### `dtlms_portal_application_education_experiences`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_education_experiences_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `sort_order` | integer(32,0) | NO | 1 |
| `education_stage` | character varying(64) | NO |  |
| `start_month` | character varying(16) | YES |  |
| `end_month` | character varying(16) | YES |  |
| `school_name` | character varying(255) | NO |  |
| `major_name` | character varying(255) | YES |  |
| `average_score` | character varying(64) | YES |  |
| `gpa` | character varying(32) | YES |  |
| `ranking` | character varying(64) | YES |  |
| `verifier_name` | character varying(128) | YES |  |
| `verifier_phone` | character varying(32) | YES |  |
| `transcript_attachment_url` | text | YES |  |
| `degree_certificate_attachment_url` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `graduation_certificate_attachment_url` | text | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_portal_application_education_sort_order` | CHECK | `CHECK ((sort_order > 0))` |
| `dtlms_portal_application_education_experien_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_education_experiences_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_education_experiences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_education_experiences_pkey ON public.dtlms_portal_application_education_experiences USING btree (id)`
- `idx_portal_application_education_application`: `CREATE INDEX idx_portal_application_education_application ON public.dtlms_portal_application_education_experiences USING btree (application_id, sort_order)`

### `dtlms_portal_application_english_proficiencies`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_english_proficiencies_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `exam_name` | character varying(32) | NO |  |
| `score_text` | character varying(64) | NO |  |
| `certificate_attachment_url` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_english_proficienc_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_english_proficiencies_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_english_proficiencies_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_english_proficiencies_pkey ON public.dtlms_portal_application_english_proficiencies USING btree (id)`
- `idx_portal_application_english_application`: `CREATE INDEX idx_portal_application_english_application ON public.dtlms_portal_application_english_proficiencies USING btree (application_id)`

### `dtlms_portal_application_family_members`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_family_members_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `member_name` | character varying(64) | NO |  |
| `relation_type` | character varying(16) | NO |  |
| `employer_name` | character varying(255) | YES |  |
| `job_title` | character varying(128) | YES |  |
| `contact_phone` | character varying(32) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_family_members_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_family_members_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_family_members_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_family_members_pkey ON public.dtlms_portal_application_family_members USING btree (id)`
- `idx_portal_application_family_application`: `CREATE INDEX idx_portal_application_family_application ON public.dtlms_portal_application_family_members USING btree (application_id)`
- `ux_portal_application_family_parent_unique`: `CREATE UNIQUE INDEX ux_portal_application_family_parent_unique ON public.dtlms_portal_application_family_members USING btree (application_id, relation_type) WHERE ((relation_type)::text = ANY (ARRAY[('父亲'::character varying)::text, ('母亲'::character varying)::text]))`

### `dtlms_portal_application_personal_statements`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `application_id` | bigint(64,0) | NO |  |
| `personal_statement_text` | text | YES |  |
| `ai_problem_statement` | text | YES |  |
| `ai_industry_opinion` | text | YES |  |
| `resume_attachment_url` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `growth_experience_text` | text | YES |  |
| `program_application_reason_text` | text | YES |  |
| `career_plan_text` | text | YES |  |
| `supporting_material_attachment_url` | text | YES |  |

**主键**: (`application_id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_personal_statement_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_personal_statements_pkey` | PRIMARY KEY | `PRIMARY KEY (application_id)` |

**索引**

- `dtlms_portal_application_personal_statements_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_personal_statements_pkey ON public.dtlms_portal_application_personal_statements USING btree (application_id)`

### `dtlms_portal_application_practice_experiences`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_practice_experiences_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `start_month` | character varying(16) | YES |  |
| `end_month` | character varying(16) | YES |  |
| `organization_name` | character varying(255) | NO |  |
| `position_name` | character varying(128) | YES |  |
| `responsibility_text` | text | YES |  |
| `verifier_name` | character varying(128) | YES |  |
| `verifier_phone` | character varying(32) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_application_practice_experienc_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `dtlms_portal_application_practice_experiences_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_portal_application_practice_experiences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_practice_experiences_pkey ON public.dtlms_portal_application_practice_experiences USING btree (id)`
- `idx_portal_application_practice_application`: `CREATE INDEX idx_portal_application_practice_application ON public.dtlms_portal_application_practice_experiences USING btree (application_id)`

### `dtlms_portal_application_preferences`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_application_preferences_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `preference_order` | integer(32,0) | NO |  |
| `advisor_name` | character varying(128) | YES |  |
| `is_optional` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `advisor_user_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `chk_portal_application_preferences_order` | CHECK | `CHECK ((preference_order > 0))` |
| `dtlms_portal_application_preferences_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE` |
| `fk_dtlms_portal_application_preferences_advisor_user_id` | FOREIGN KEY | `FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `dtlms_portal_application_preferences_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `uq_portal_application_preferences_order` | UNIQUE | `UNIQUE (application_id, preference_order)` |

**索引**

- `dtlms_portal_application_preferences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_preferences_pkey ON public.dtlms_portal_application_preferences USING btree (id)`
- `idx_portal_application_preferences_application`: `CREATE INDEX idx_portal_application_preferences_application ON public.dtlms_portal_application_preferences USING btree (application_id, preference_order)`
- `uq_portal_application_preferences_order`: `CREATE UNIQUE INDEX uq_portal_application_preferences_order ON public.dtlms_portal_application_preferences USING btree (application_id, preference_order)`

### `dtlms_portal_student_profiles`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `portal_student_id` | bigint(64,0) | NO |  |
| `full_name_pinyin` | character varying(128) | YES |  |
| `gender` | character varying(16) | YES |  |
| `birth_date` | character varying(32) | YES |  |
| `ethnic_group` | character varying(64) | YES |  |
| `native_place` | character varying(128) | YES |  |
| `political_status` | character varying(64) | YES |  |
| `marital_status` | character varying(32) | YES |  |
| `religious_belief` | character varying(128) | YES |  |
| `id_type` | character varying(64) | YES |  |
| `mailing_address` | text | YES |  |
| `emergency_contact_name` | character varying(128) | YES |  |
| `emergency_contact_phone` | character varying(32) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `profile_photo_url` | character varying(255) | YES |  |
| `id_card_collage_url` | character varying(255) | YES |  |

**主键**: (`portal_student_id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_student_profiles_portal_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE` |
| `dtlms_portal_student_profiles_pkey` | PRIMARY KEY | `PRIMARY KEY (portal_student_id)` |

**索引**

- `dtlms_portal_student_profiles_pkey`: `CREATE UNIQUE INDEX dtlms_portal_student_profiles_pkey ON public.dtlms_portal_student_profiles USING btree (portal_student_id)`

### `dtlms_portal_students`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_portal_students_id_seq'::regclass) |
| `full_name` | character varying(128) | NO |  |
| `phone_number` | character varying(32) | NO |  |
| `email` | character varying(128) | NO |  |
| `id_number` | character varying(64) | NO |  |
| `graduation_school` | character varying(255) | YES |  |
| `highest_degree` | character varying(64) | YES |  |
| `intended_field` | character varying(128) | YES |  |
| `political_status` | character varying(64) | YES |  |
| `selected_plan_id` | bigint(64,0) | YES |  |
| `selected_team_name` | character varying(128) | YES |  |
| `selected_advisor_name` | character varying(128) | YES |  |
| `self_evaluation` | text | YES |  |
| `submitted_at` | timestamp with time zone | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `password_hash` | character varying(255) | YES |  |
| `gender` | character varying(16) | YES |  |
| `birth_date` | character varying(32) | YES |  |
| `ethnic_group` | character varying(64) | YES |  |
| `native_place` | character varying(128) | YES |  |
| `marital_status` | character varying(32) | YES |  |
| `religious_belief` | character varying(128) | YES |  |
| `id_type` | character varying(64) | YES |  |
| `mailing_address` | text | YES |  |
| `english_level` | character varying(128) | YES |  |
| `family_info` | text | YES |  |
| `education_experience` | text | YES |  |
| `practice_experience` | text | YES |  |
| `personal_profile` | text | YES |  |
| `recommendation_notes` | text | YES |  |
| `personal_statement_text` | text | YES |  |
| `signed_agreement` | boolean | NO | false |
| `account_status` | character varying(32) | NO | '启用'::character varying |
| `application_draft` | jsonb | YES |  |
| `selected_team_id` | bigint(64,0) | YES |  |
| `selected_advisor_user_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_portal_students_selected_plan_id_fkey` | FOREIGN KEY | `FOREIGN KEY (selected_plan_id) REFERENCES dtlms_recruitment_plans(id)` |
| `fk_dtlms_portal_students_selected_advisor_user_id` | FOREIGN KEY | `FOREIGN KEY (selected_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `fk_dtlms_portal_students_selected_team_id` | FOREIGN KEY | `FOREIGN KEY (selected_team_id) REFERENCES dtlms_teams(id) NOT VALID` |
| `dtlms_portal_students_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_portal_students_email_key` | UNIQUE | `UNIQUE (email)` |
| `dtlms_portal_students_id_number_key` | UNIQUE | `UNIQUE (id_number)` |
| `dtlms_portal_students_phone_number_key` | UNIQUE | `UNIQUE (phone_number)` |

**索引**

- `dtlms_portal_students_email_key`: `CREATE UNIQUE INDEX dtlms_portal_students_email_key ON public.dtlms_portal_students USING btree (email)`
- `dtlms_portal_students_id_number_key`: `CREATE UNIQUE INDEX dtlms_portal_students_id_number_key ON public.dtlms_portal_students USING btree (id_number)`
- `dtlms_portal_students_phone_number_key`: `CREATE UNIQUE INDEX dtlms_portal_students_phone_number_key ON public.dtlms_portal_students USING btree (phone_number)`
- `dtlms_portal_students_pkey`: `CREATE UNIQUE INDEX dtlms_portal_students_pkey ON public.dtlms_portal_students USING btree (id)`
- `idx_dtlms_portal_students_selected_team_id`: `CREATE INDEX idx_dtlms_portal_students_selected_team_id ON public.dtlms_portal_students USING btree (selected_team_id) WHERE (selected_team_id IS NOT NULL)`

### `dtlms_qualification_review_logs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_qualification_review_logs_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `reviewer_user_id` | bigint(64,0) | YES |  |
| `reviewer_username` | character varying(64) | NO |  |
| `reviewer_name` | character varying(128) | YES |  |
| `reviewer_role_code` | character varying(64) | YES |  |
| `action` | character varying(32) | NO |  |
| `action_label` | character varying(64) | NO |  |
| `review_comment` | text | YES |  |
| `reviewed_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_qualification_review_logs_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_qualification_review_logs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_qualification_review_logs_pkey`: `CREATE UNIQUE INDEX dtlms_qualification_review_logs_pkey ON public.dtlms_qualification_review_logs USING btree (id)`
- `idx_qualification_review_logs_application`: `CREATE INDEX idx_qualification_review_logs_application ON public.dtlms_qualification_review_logs USING btree (application_id, reviewed_at DESC)`
- `idx_qualification_review_logs_reviewer`: `CREATE INDEX idx_qualification_review_logs_reviewer ON public.dtlms_qualification_review_logs USING btree (reviewer_username, reviewed_at DESC)`

### `dtlms_qualification_reviews`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_qualification_reviews_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `reviewer_username` | character varying(64) | NO |  |
| `review_status` | character varying(32) | NO | 'pending'::character varying |
| `review_comment` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_qualification_reviews_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_qualification_reviews_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_qualification_reviews_pkey`: `CREATE UNIQUE INDEX dtlms_qualification_reviews_pkey ON public.dtlms_qualification_reviews USING btree (id)`

### `dtlms_recruitment_applications`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_recruitment_applications_id_seq'::regclass) |
| `plan_id` | bigint(64,0) | NO |  |
| `student_name` | character varying(128) | NO |  |
| `candidate_no` | character varying(64) | NO |  |
| `gender` | character varying(16) | NO |  |
| `graduation_school` | character varying(255) | YES |  |
| `highest_degree` | character varying(64) | YES |  |
| `intended_field_id` | bigint(64,0) | YES |  |
| `application_status` | character varying(32) | NO | 'submitted'::character varying |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `business_key` | character varying(64) | NO |  |
| `review_round` | character varying(64) | YES |  |
| `first_choice` | character varying(255) | YES |  |
| `second_choice` | character varying(255) | YES |  |
| `political_status` | character varying(64) | YES |  |
| `marital_status` | character varying(32) | YES |  |
| `religious_belief` | character varying(128) | YES |  |
| `native_place` | character varying(128) | YES |  |
| `phone_number` | character varying(64) | YES |  |
| `email` | character varying(255) | YES |  |
| `mailing_address` | text | YES |  |
| `id_type` | character varying(64) | YES |  |
| `id_number` | character varying(128) | YES |  |
| `undergraduate_school` | character varying(255) | YES |  |
| `accept_adjustment` | character varying(16) | YES |  |
| `undergraduate_average_score` | character varying(64) | YES |  |
| `undergraduate_gpa` | character varying(64) | YES |  |
| `undergraduate_rank` | character varying(64) | YES |  |
| `undergraduate_major` | character varying(255) | YES |  |
| `graduate_average_score` | character varying(64) | YES |  |
| `graduate_gpa` | character varying(64) | YES |  |
| `graduate_rank` | character varying(64) | YES |  |
| `graduate_major` | character varying(255) | YES |  |
| `intended_advisor_name` | character varying(128) | YES |  |
| `discovery_channel` | text | YES |  |
| `graduate_school` | character varying(255) | YES |  |
| `overseas_university_name` | character varying(255) | YES |  |
| `overseas_master_university_name` | character varying(255) | YES |  |
| `self_evaluation` | text | YES |  |
| `applied_at` | timestamp with time zone | YES |  |
| `research_problem` | text | YES |  |
| `research_status_analysis` | text | YES |  |
| `research_impact` | text | YES |  |
| `ai_society_impact` | text | YES |  |
| `dissenting_view` | text | YES |  |
| `family_info` | text | YES |  |
| `education_experience` | text | YES |  |
| `practice_experience` | text | YES |  |
| `personal_statement_text` | text | YES |  |
| `student_activity_experience` | text | YES |  |
| `personal_statement_attachment` | text | YES |  |
| `material_list_attachment` | text | YES |  |
| `supplementary_profile` | text | YES |  |
| `portal_student_id` | bigint(64,0) | YES |  |
| `source_channel` | character varying(64) | YES |  |
| `source_channel_other` | character varying(255) | YES |  |
| `first_choice_team_id` | bigint(64,0) | YES |  |
| `second_choice_team_id` | bigint(64,0) | YES |  |
| `intended_advisor_user_id` | bigint(64,0) | YES |  |
| `advisor_screening_status` | character varying(32) | YES | 'pending'::character varying |
| `advisor_screening_round` | character varying(32) | YES | 'first_choice'::character varying |
| `first_choice_screening_batch_id` | bigint(64,0) | YES |  |
| `second_choice_screening_batch_id` | bigint(64,0) | YES |  |
| `first_choice_screening_submitted_at` | timestamp with time zone | YES |  |
| `second_choice_screening_submitted_at` | timestamp with time zone | YES |  |
| `first_choice_screening_score` | numeric(5,2) | YES |  |
| `second_choice_screening_score` | numeric(5,2) | YES |  |
| `initial_screening_status` | character varying(32) | YES | 'pending'::character varying |
| `initial_screening_result` | character varying(32) | YES |  |
| `initial_screening_confirmed_at` | timestamp with time zone | YES |  |
| `initial_screening_confirmer_username` | character varying(64) | YES |  |
| `initial_screening_confirmer_name` | character varying(128) | YES |  |
| `initial_screening_notification_status` | character varying(32) | YES | 'pending'::character varying |
| `initial_screening_notification_sent_at` | timestamp with time zone | YES |  |
| `next_stage_name` | character varying(64) | YES |  |
| `first_choice_id` | bigint(64,0) | YES |  |
| `second_choice_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_recruitment_applications_intended_field_id_fkey` | FOREIGN KEY | `FOREIGN KEY (intended_field_id) REFERENCES dtlms_research_fields(id)` |
| `dtlms_recruitment_applications_plan_id_fkey` | FOREIGN KEY | `FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id)` |
| `dtlms_recruitment_applications_portal_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id)` |
| `fk_dtlms_recruitment_applications_first_choice_id` | FOREIGN KEY | `FOREIGN KEY (first_choice_id) REFERENCES dtlms_users(id) NOT VALID` |
| `fk_dtlms_recruitment_applications_first_choice_team_id` | FOREIGN KEY | `FOREIGN KEY (first_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID` |
| `fk_dtlms_recruitment_applications_intended_advisor_user_id` | FOREIGN KEY | `FOREIGN KEY (intended_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `fk_dtlms_recruitment_applications_second_choice_id` | FOREIGN KEY | `FOREIGN KEY (second_choice_id) REFERENCES dtlms_users(id) NOT VALID` |
| `fk_dtlms_recruitment_applications_second_choice_team_id` | FOREIGN KEY | `FOREIGN KEY (second_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID` |
| `dtlms_recruitment_applications_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_recruitment_applications_candidate_no_key` | UNIQUE | `UNIQUE (candidate_no)` |

**索引**

- `dtlms_recruitment_applications_candidate_no_key`: `CREATE UNIQUE INDEX dtlms_recruitment_applications_candidate_no_key ON public.dtlms_recruitment_applications USING btree (candidate_no)`
- `dtlms_recruitment_applications_pkey`: `CREATE UNIQUE INDEX dtlms_recruitment_applications_pkey ON public.dtlms_recruitment_applications USING btree (id)`
- `idx_applications_plan_status`: `CREATE INDEX idx_applications_plan_status ON public.dtlms_recruitment_applications USING btree (plan_id, application_status)`
- `idx_applications_portal_student`: `CREATE INDEX idx_applications_portal_student ON public.dtlms_recruitment_applications USING btree (portal_student_id)`
- `idx_dtlms_recruitment_applications_email`: `CREATE INDEX idx_dtlms_recruitment_applications_email ON public.dtlms_recruitment_applications USING btree (email)`
- `idx_dtlms_recruitment_applications_first_choice_team_id`: `CREATE INDEX idx_dtlms_recruitment_applications_first_choice_team_id ON public.dtlms_recruitment_applications USING btree (first_choice_team_id) WHERE (first_choice_team_id IS NOT NULL)`
- `idx_dtlms_recruitment_applications_phone_number`: `CREATE INDEX idx_dtlms_recruitment_applications_phone_number ON public.dtlms_recruitment_applications USING btree (phone_number)`
- `idx_recruitment_applications_advisor_screening_status`: `CREATE INDEX idx_recruitment_applications_advisor_screening_status ON public.dtlms_recruitment_applications USING btree (advisor_screening_status, advisor_screening_round)`
- `idx_recruitment_applications_initial_screening_status`: `CREATE INDEX idx_recruitment_applications_initial_screening_status ON public.dtlms_recruitment_applications USING btree (initial_screening_status, initial_screening_result)`
- `ux_dtlms_recruitment_applications_business_key`: `CREATE UNIQUE INDEX ux_dtlms_recruitment_applications_business_key ON public.dtlms_recruitment_applications USING btree (business_key)`

### `dtlms_recruitment_plans`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_recruitment_plans_id_seq'::regclass) |
| `plan_code` | character varying(64) | NO |  |
| `plan_name` | character varying(255) | NO |  |
| `academic_year` | character varying(16) | NO |  |
| `semester` | character varying(16) | NO |  |
| `start_date` | timestamp with time zone | NO |  |
| `end_date` | timestamp with time zone | NO |  |
| `target_quota` | integer(32,0) | NO | 0 |
| `plan_status` | character varying(32) | NO | 'draft'::character varying |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `brochure_image_url` | character varying(255) | YES |  |
| `plan_description` | text | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_recruitment_plans_check` | CHECK | `CHECK ((end_date >= start_date))` |
| `dtlms_recruitment_plans_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_recruitment_plans_plan_code_key` | UNIQUE | `UNIQUE (plan_code)` |

**索引**

- `dtlms_recruitment_plans_pkey`: `CREATE UNIQUE INDEX dtlms_recruitment_plans_pkey ON public.dtlms_recruitment_plans USING btree (id)`
- `dtlms_recruitment_plans_plan_code_key`: `CREATE UNIQUE INDEX dtlms_recruitment_plans_plan_code_key ON public.dtlms_recruitment_plans USING btree (plan_code)`

### `dtlms_research_fields`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_research_fields_id_seq'::regclass) |
| `field_code` | character varying(64) | NO |  |
| `field_name` | character varying(128) | NO |  |
| `description` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_research_fields_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_research_fields_field_code_key` | UNIQUE | `UNIQUE (field_code)` |

**索引**

- `dtlms_research_fields_field_code_key`: `CREATE UNIQUE INDEX dtlms_research_fields_field_code_key ON public.dtlms_research_fields USING btree (field_code)`
- `dtlms_research_fields_pkey`: `CREATE UNIQUE INDEX dtlms_research_fields_pkey ON public.dtlms_research_fields USING btree (id)`

### `dtlms_research_projects`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_research_projects_id_seq'::regclass) |
| `project_code` | character varying(64) | NO |  |
| `project_name` | character varying(255) | NO |  |
| `principal_advisor_id` | bigint(64,0) | YES |  |
| `funding_amount` | numeric(12,2) | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_research_projects_principal_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (principal_advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_research_projects_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_research_projects_project_code_key` | UNIQUE | `UNIQUE (project_code)` |

**索引**

- `dtlms_research_projects_pkey`: `CREATE UNIQUE INDEX dtlms_research_projects_pkey ON public.dtlms_research_projects USING btree (id)`
- `dtlms_research_projects_project_code_key`: `CREATE UNIQUE INDEX dtlms_research_projects_project_code_key ON public.dtlms_research_projects USING btree (project_code)`

### `dtlms_reviewer_assignments`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_reviewer_assignments_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `reviewer_username` | character varying(64) | NO |  |
| `reviewer_role` | character varying(32) | NO |  |
| `assignment_status` | character varying(32) | NO | 'assigned'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_reviewer_assignments_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_reviewer_assignments_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_reviewer_assignments_pkey`: `CREATE UNIQUE INDEX dtlms_reviewer_assignments_pkey ON public.dtlms_reviewer_assignments USING btree (id)`

### `dtlms_role_permissions`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_role_permissions_id_seq'::regclass) |
| `role_id` | bigint(64,0) | NO |  |
| `permission_id` | bigint(64,0) | NO |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_role_permissions_permission_id_fkey` | FOREIGN KEY | `FOREIGN KEY (permission_id) REFERENCES dtlms_permissions(id)` |
| `dtlms_role_permissions_role_id_fkey` | FOREIGN KEY | `FOREIGN KEY (role_id) REFERENCES dtlms_roles(id)` |
| `dtlms_role_permissions_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_role_permissions_role_id_permission_id_key` | UNIQUE | `UNIQUE (role_id, permission_id)` |

**索引**

- `dtlms_role_permissions_pkey`: `CREATE UNIQUE INDEX dtlms_role_permissions_pkey ON public.dtlms_role_permissions USING btree (id)`
- `dtlms_role_permissions_role_id_permission_id_key`: `CREATE UNIQUE INDEX dtlms_role_permissions_role_id_permission_id_key ON public.dtlms_role_permissions USING btree (role_id, permission_id)`

### `dtlms_roles`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_roles_id_seq'::regclass) |
| `role_code` | character varying(64) | NO |  |
| `role_name` | character varying(128) | NO |  |
| `description` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `scope_name` | character varying(128) | NO | '系统管理'::character varying |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_roles_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_roles_role_code_key` | UNIQUE | `UNIQUE (role_code)` |

**索引**

- `dtlms_roles_pkey`: `CREATE UNIQUE INDEX dtlms_roles_pkey ON public.dtlms_roles USING btree (id)`
- `dtlms_roles_role_code_key`: `CREATE UNIQUE INDEX dtlms_roles_role_code_key ON public.dtlms_roles USING btree (role_code)`

### `dtlms_schema_migrations`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `file_name` | character varying(255) | NO |  |
| `applied_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`file_name`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_schema_migrations_pkey` | PRIMARY KEY | `PRIMARY KEY (file_name)` |

**索引**

- `dtlms_schema_migrations_pkey`: `CREATE UNIQUE INDEX dtlms_schema_migrations_pkey ON public.dtlms_schema_migrations USING btree (file_name)`

### `dtlms_scientific_reports`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_scientific_reports_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `training_plan_id` | bigint(64,0) | NO |  |
| `period_label` | character varying(32) | NO |  |
| `report_status` | character varying(32) | NO | 'pending'::character varying |
| `summary` | text | NO |  |
| `attachment_url` | character varying(255) | YES |  |
| `reviewer_advisor_id` | bigint(64,0) | YES |  |
| `review_score` | numeric(5,2) | YES |  |
| `review_comment` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `business_key` | character varying(64) | NO |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_scientific_reports_report_status_check` | CHECK | `CHECK (((report_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('submitted'::character varying)::text, ('reviewing'::character varying)::text, ('reviewed'::character varying)::text, ('rework'::character varying)::text])))` |
| `dtlms_scientific_reports_reviewer_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (reviewer_advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_scientific_reports_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_scientific_reports_training_plan_id_fkey` | FOREIGN KEY | `FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id)` |
| `dtlms_scientific_reports_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_scientific_reports_pkey`: `CREATE UNIQUE INDEX dtlms_scientific_reports_pkey ON public.dtlms_scientific_reports USING btree (id)`
- `idx_reports_student_period`: `CREATE INDEX idx_reports_student_period ON public.dtlms_scientific_reports USING btree (student_id, period_label)`
- `ux_dtlms_scientific_reports_business_key`: `CREATE UNIQUE INDEX ux_dtlms_scientific_reports_business_key ON public.dtlms_scientific_reports USING btree (business_key)`

### `dtlms_student_advisor_history`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_student_advisor_history_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `advisor_id` | bigint(64,0) | NO |  |
| `relation_type` | character varying(32) | NO | 'primary'::character varying |
| `start_date` | date | NO |  |
| `end_date` | date | YES |  |
| `change_reason` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_student_advisor_history_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_student_advisor_history_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_student_advisor_history_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_student_advisor_history_pkey`: `CREATE UNIQUE INDEX dtlms_student_advisor_history_pkey ON public.dtlms_student_advisor_history USING btree (id)`

### `dtlms_student_team_history`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_student_team_history_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `team_id` | bigint(64,0) | NO |  |
| `start_date` | date | NO |  |
| `end_date` | date | YES |  |
| `change_reason` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_student_team_history_check` | CHECK | `CHECK (((end_date IS NULL) OR (end_date >= start_date)))` |
| `dtlms_student_team_history_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_student_team_history_team_id_fkey` | FOREIGN KEY | `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)` |
| `dtlms_student_team_history_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_student_team_history_pkey`: `CREATE UNIQUE INDEX dtlms_student_team_history_pkey ON public.dtlms_student_team_history USING btree (id)`

### `dtlms_students`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_students_id_seq'::regclass) |
| `student_no` | character varying(32) | NO |  |
| `full_name` | character varying(128) | NO |  |
| `gender` | character varying(16) | NO |  |
| `political_status` | character varying(32) | YES |  |
| `phone_number` | character varying(32) | YES |  |
| `identity_no` | character varying(64) | YES |  |
| `enrollment_year` | integer(32,0) | NO |  |
| `degree_type` | character varying(32) | NO |  |
| `team_name` | character varying(128) | YES |  |
| `current_status` | character varying(32) | NO | 'enrolled'::character varying |
| `primary_advisor_id` | bigint(64,0) | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `team_id` | bigint(64,0) | YES |  |
| `portal_student_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_students_primary_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (primary_advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_students_team_id_fkey` | FOREIGN KEY | `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)` |
| `fk_dtlms_students_portal_student_id` | FOREIGN KEY | `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) NOT VALID` |
| `dtlms_students_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_students_student_no_key` | UNIQUE | `UNIQUE (student_no)` |

**索引**

- `dtlms_students_pkey`: `CREATE UNIQUE INDEX dtlms_students_pkey ON public.dtlms_students USING btree (id)`
- `dtlms_students_student_no_key`: `CREATE UNIQUE INDEX dtlms_students_student_no_key ON public.dtlms_students USING btree (student_no)`
- `idx_dtlms_students_portal_student_id`: `CREATE UNIQUE INDEX idx_dtlms_students_portal_student_id ON public.dtlms_students USING btree (portal_student_id) WHERE (portal_student_id IS NOT NULL)`
- `idx_students_primary_advisor`: `CREATE INDEX idx_students_primary_advisor ON public.dtlms_students USING btree (primary_advisor_id)`
- `idx_students_status`: `CREATE INDEX idx_students_status ON public.dtlms_students USING btree (current_status)`

### `dtlms_system_configs`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_system_configs_id_seq'::regclass) |
| `config_key` | character varying(128) | NO |  |
| `config_value` | text | NO |  |
| `description` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_system_configs_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_system_configs_config_key_key` | UNIQUE | `UNIQUE (config_key)` |

**索引**

- `dtlms_system_configs_config_key_key`: `CREATE UNIQUE INDEX dtlms_system_configs_config_key_key ON public.dtlms_system_configs USING btree (config_key)`
- `dtlms_system_configs_pkey`: `CREATE UNIQUE INDEX dtlms_system_configs_pkey ON public.dtlms_system_configs USING btree (id)`

### `dtlms_team_advisors`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_team_advisors_id_seq'::regclass) |
| `team_id` | bigint(64,0) | NO |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `advisor_user_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_team_advisors_team_id_fkey` | FOREIGN KEY | `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)` |
| `fk_dtlms_team_advisors_advisor_user_id` | FOREIGN KEY | `FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `dtlms_team_advisors_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_team_advisors_pkey`: `CREATE UNIQUE INDEX dtlms_team_advisors_pkey ON public.dtlms_team_advisors USING btree (id)`
- `idx_dtlms_team_advisors_team_user`: `CREATE INDEX idx_dtlms_team_advisors_team_user ON public.dtlms_team_advisors USING btree (team_id, advisor_user_id) WHERE (advisor_user_id IS NOT NULL)`

### `dtlms_team_leaders`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO |  |
| `team_id` | bigint(64,0) | NO |  |
| `user_id` | bigint(64,0) | NO |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `fk_dtlms_team_leaders_team_id` | FOREIGN KEY | `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)` |
| `fk_dtlms_team_leaders_user_id` | FOREIGN KEY | `FOREIGN KEY (user_id) REFERENCES dtlms_users(id)` |
| `dtlms_team_leaders_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_team_leaders_team_id_user_id_key` | UNIQUE | `UNIQUE (team_id, user_id)` |

**索引**

- `dtlms_team_leaders_pkey`: `CREATE UNIQUE INDEX dtlms_team_leaders_pkey ON public.dtlms_team_leaders USING btree (id)`
- `dtlms_team_leaders_team_id_user_id_key`: `CREATE UNIQUE INDEX dtlms_team_leaders_team_id_user_id_key ON public.dtlms_team_leaders USING btree (team_id, user_id)`
- `idx_dtlms_team_leaders_team_id`: `CREATE INDEX idx_dtlms_team_leaders_team_id ON public.dtlms_team_leaders USING btree (team_id)`
- `idx_dtlms_team_leaders_user_id`: `CREATE INDEX idx_dtlms_team_leaders_user_id ON public.dtlms_team_leaders USING btree (user_id)`

### `dtlms_teams`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_teams_id_seq'::regclass) |
| `team_code` | character varying(32) | NO |  |
| `team_name` | character varying(128) | NO |  |
| `department_name` | character varying(128) | NO |  |
| `discipline_name` | character varying(128) | YES |  |
| `research_directions` | text | YES |  |
| `team_status` | character varying(32) | NO | 'active'::character varying |
| `established_on` | date | YES |  |
| `description` | text | YES |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `lead_user_id` | bigint(64,0) | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_teams_team_status_check` | CHECK | `CHECK (((team_status)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text, ('planning'::character varying)::text, ('archived'::character varying)::text])))` |
| `fk_dtlms_teams_lead_user_id` | FOREIGN KEY | `FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID` |
| `dtlms_teams_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_teams_team_code_key` | UNIQUE | `UNIQUE (team_code)` |
| `dtlms_teams_team_name_key` | UNIQUE | `UNIQUE (team_name)` |

**索引**

- `dtlms_teams_pkey`: `CREATE UNIQUE INDEX dtlms_teams_pkey ON public.dtlms_teams USING btree (id)`
- `dtlms_teams_team_code_key`: `CREATE UNIQUE INDEX dtlms_teams_team_code_key ON public.dtlms_teams USING btree (team_code)`
- `dtlms_teams_team_name_key`: `CREATE UNIQUE INDEX dtlms_teams_team_name_key ON public.dtlms_teams USING btree (team_name)`
- `idx_dtlms_teams_lead_user_id`: `CREATE INDEX idx_dtlms_teams_lead_user_id ON public.dtlms_teams USING btree (lead_user_id) WHERE (lead_user_id IS NOT NULL)`

### `dtlms_theses`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_theses_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `advisor_id` | bigint(64,0) | NO |  |
| `title` | character varying(255) | NO |  |
| `plagiarism_rate` | numeric(5,2) | YES |  |
| `thesis_status` | character varying(32) | NO | 'draft'::character varying |
| `blind_review_status` | character varying(32) | NO | 'pending'::character varying |
| `defense_date` | date | YES |  |
| `degree_granted` | character varying(32) | NO | 'pending'::character varying |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `business_key` | character varying(64) | NO |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_theses_plagiarism_rate_check` | CHECK | `CHECK (((plagiarism_rate IS NULL) OR (plagiarism_rate <= (100)::numeric)))` |
| `dtlms_theses_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_theses_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_theses_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_theses_pkey`: `CREATE UNIQUE INDEX dtlms_theses_pkey ON public.dtlms_theses USING btree (id)`
- `idx_thesis_status`: `CREATE INDEX idx_thesis_status ON public.dtlms_theses USING btree (thesis_status)`
- `ux_dtlms_theses_business_key`: `CREATE UNIQUE INDEX ux_dtlms_theses_business_key ON public.dtlms_theses USING btree (business_key)`

### `dtlms_thesis_reviews`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_thesis_reviews_id_seq'::regclass) |
| `thesis_id` | bigint(64,0) | NO |  |
| `expert_name` | character varying(128) | NO |  |
| `review_score` | numeric(5,2) | YES |  |
| `review_status` | character varying(32) | NO | 'pending'::character varying |
| `review_comment` | text | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_thesis_reviews_thesis_id_fkey` | FOREIGN KEY | `FOREIGN KEY (thesis_id) REFERENCES dtlms_theses(id)` |
| `dtlms_thesis_reviews_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_thesis_reviews_pkey`: `CREATE UNIQUE INDEX dtlms_thesis_reviews_pkey ON public.dtlms_thesis_reviews USING btree (id)`

### `dtlms_training_plan_versions`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_training_plan_versions_id_seq'::regclass) |
| `training_plan_id` | bigint(64,0) | NO |  |
| `version_no` | character varying(16) | NO |  |
| `change_reason` | text | YES |  |
| `plan_snapshot` | text | NO |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_training_plan_versions_training_plan_id_fkey` | FOREIGN KEY | `FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id)` |
| `dtlms_training_plan_versions_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_training_plan_versions_pkey`: `CREATE UNIQUE INDEX dtlms_training_plan_versions_pkey ON public.dtlms_training_plan_versions USING btree (id)`

### `dtlms_training_plans`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_training_plans_id_seq'::regclass) |
| `student_id` | bigint(64,0) | NO |  |
| `advisor_id` | bigint(64,0) | NO |  |
| `version_no` | character varying(16) | NO | 'v1.0'::character varying |
| `report_cycle` | character varying(32) | NO |  |
| `plan_status` | character varying(32) | NO | 'draft'::character varying |
| `scientific_goal` | text | NO |  |
| `assessment_rule` | text | NO |  |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_training_plans_plan_status_check` | CHECK | `CHECK (((plan_status)::text = ANY (ARRAY[('draft'::character varying)::text, ('pending_confirm'::character varying)::text, ('effective'::character varying)::text, ('archived'::character varying)::text])))` |
| `dtlms_training_plans_version_no_check` | CHECK | `CHECK (((version_no)::text <> ''::text))` |
| `dtlms_training_plans_advisor_id_fkey` | FOREIGN KEY | `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)` |
| `dtlms_training_plans_student_id_fkey` | FOREIGN KEY | `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)` |
| `dtlms_training_plans_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_training_plans_pkey`: `CREATE UNIQUE INDEX dtlms_training_plans_pkey ON public.dtlms_training_plans USING btree (id)`
- `idx_training_plan_student`: `CREATE INDEX idx_training_plan_student ON public.dtlms_training_plans USING btree (student_id)`

### `dtlms_user_profiles`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `username` | character varying(64) | NO |  |
| `full_name` | character varying(128) | NO |  |
| `role_name` | character varying(128) | NO |  |
| `department_name` | character varying(128) | NO |  |
| `phone_number` | character varying(32) | YES |  |
| `email` | character varying(128) | YES |  |
| `theme_color` | character varying(32) | NO | '#0f4cbd'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `introduction` | text | YES |  |

**主键**: (`username`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_user_profiles_username_fkey` | FOREIGN KEY | `FOREIGN KEY (username) REFERENCES dtlms_users(username) ON UPDATE CASCADE ON DELETE CASCADE` |
| `dtlms_user_profiles_pkey` | PRIMARY KEY | `PRIMARY KEY (username)` |

**索引**

- `dtlms_user_profiles_pkey`: `CREATE UNIQUE INDEX dtlms_user_profiles_pkey ON public.dtlms_user_profiles USING btree (username)`

### `dtlms_user_roles`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_user_roles_id_seq'::regclass) |
| `user_id` | bigint(64,0) | NO |  |
| `role_id` | bigint(64,0) | NO |  |
| `grant_source` | character varying(64) | NO | 'bootstrap'::character varying |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_user_roles_role_id_fkey` | FOREIGN KEY | `FOREIGN KEY (role_id) REFERENCES dtlms_roles(id)` |
| `dtlms_user_roles_user_id_fkey` | FOREIGN KEY | `FOREIGN KEY (user_id) REFERENCES dtlms_users(id)` |
| `dtlms_user_roles_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_user_roles_user_id_role_id_key` | UNIQUE | `UNIQUE (user_id, role_id)` |

**索引**

- `dtlms_user_roles_pkey`: `CREATE UNIQUE INDEX dtlms_user_roles_pkey ON public.dtlms_user_roles USING btree (id)`
- `dtlms_user_roles_user_id_role_id_key`: `CREATE UNIQUE INDEX dtlms_user_roles_user_id_role_id_key ON public.dtlms_user_roles USING btree (user_id, role_id)`

### `dtlms_users`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_users_id_seq'::regclass) |
| `username` | character varying(64) | NO |  |
| `full_name` | character varying(128) | NO |  |
| `email` | character varying(128) | YES |  |
| `password_hash` | character varying(255) | NO |  |
| `is_active` | boolean | NO | true |
| `is_deleted` | boolean | NO | false |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `department_name` | character varying(128) | NO | ''::character varying |
| `phone_number` | character varying(32) | YES |  |
| `last_login_at` | timestamp with time zone | YES |  |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_users_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |
| `dtlms_users_username_key` | UNIQUE | `UNIQUE (username)` |

**索引**

- `dtlms_users_pkey`: `CREATE UNIQUE INDEX dtlms_users_pkey ON public.dtlms_users USING btree (id)`
- `dtlms_users_username_key`: `CREATE UNIQUE INDEX dtlms_users_username_key ON public.dtlms_users USING btree (username)`

### `dtlms_wf_de_model`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `name_` | character varying(255) | NO |  |
| `key_` | character varying(128) | NO |  |
| `category_` | character varying(128) | YES |  |
| `version_` | integer(32,0) | NO | 1 |
| `model_type_` | integer(32,0) | NO | 0 |
| `description_` | text | YES |  |
| `meta_info_` | jsonb | YES |  |
| `created_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `last_updated_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `tenant_id_` | character varying(64) | YES |  |
| `deployment_id_` | character varying(64) | YES |  |
| `resource_name_` | character varying(255) | YES |  |
| `editor_source_value_` | text | YES |  |
| `editor_source_extra_value_` | jsonb | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_de_model_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_de_model_pkey`: `CREATE UNIQUE INDEX dtlms_wf_de_model_pkey ON public.dtlms_wf_de_model USING btree (id_)`

### `dtlms_wf_hi_actinst`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `proc_def_id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `exec_id_` | character varying(64) | YES |  |
| `act_id_` | character varying(128) | NO |  |
| `act_name_` | character varying(255) | YES |  |
| `act_type_` | character varying(64) | NO |  |
| `assignee_` | character varying(64) | YES |  |
| `start_time_` | timestamp with time zone | NO |  |
| `end_time_` | timestamp with time zone | YES |  |
| `duration_ms_` | bigint(64,0) | YES |  |
| `business_key_` | character varying(64) | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_hi_actinst_proc_def_id__fkey` | FOREIGN KEY | `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)` |
| `dtlms_wf_hi_actinst_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_hi_actinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_actinst_pkey ON public.dtlms_wf_hi_actinst USING btree (id_)`
- `idx_dtlms_wf_hi_actinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_actinst_proc_inst ON public.dtlms_wf_hi_actinst USING btree (proc_inst_id_)`

### `dtlms_wf_hi_procinst`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `business_key_` | character varying(64) | YES |  |
| `proc_def_id_` | character varying(64) | NO |  |
| `start_time_` | timestamp with time zone | NO |  |
| `end_time_` | timestamp with time zone | YES |  |
| `duration_ms_` | bigint(64,0) | YES |  |
| `start_user_id_` | character varying(64) | YES |  |
| `end_act_id_` | character varying(128) | YES |  |
| `delete_reason_` | character varying(255) | YES |  |
| `start_act_id_` | character varying(128) | YES |  |
| `state_` | character varying(32) | NO | 'ACTIVE'::character varying |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_hi_procinst_proc_def_id__fkey` | FOREIGN KEY | `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)` |
| `dtlms_wf_hi_procinst_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |
| `dtlms_wf_hi_procinst_proc_inst_id__key` | UNIQUE | `UNIQUE (proc_inst_id_)` |

**索引**

- `dtlms_wf_hi_procinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_procinst_pkey ON public.dtlms_wf_hi_procinst USING btree (id_)`
- `dtlms_wf_hi_procinst_proc_inst_id__key`: `CREATE UNIQUE INDEX dtlms_wf_hi_procinst_proc_inst_id__key ON public.dtlms_wf_hi_procinst USING btree (proc_inst_id_)`
- `idx_dtlms_wf_hi_procinst_business_key`: `CREATE INDEX idx_dtlms_wf_hi_procinst_business_key ON public.dtlms_wf_hi_procinst USING btree (business_key_)`

### `dtlms_wf_hi_taskinst`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `task_def_key_` | character varying(128) | YES |  |
| `proc_def_id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `exec_id_` | character varying(64) | YES |  |
| `name_` | character varying(255) | NO |  |
| `business_key_` | character varying(64) | YES |  |
| `assignee_` | character varying(64) | YES |  |
| `owner_` | character varying(64) | YES |  |
| `start_time_` | timestamp with time zone | NO |  |
| `claim_time_` | timestamp with time zone | YES |  |
| `end_time_` | timestamp with time zone | YES |  |
| `duration_ms_` | bigint(64,0) | YES |  |
| `due_date_` | timestamp with time zone | YES |  |
| `delete_reason_` | character varying(255) | YES |  |
| `priority_` | integer(32,0) | NO | 50 |
| `category_` | character varying(128) | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_hi_taskinst_proc_def_id__fkey` | FOREIGN KEY | `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)` |
| `dtlms_wf_hi_taskinst_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_hi_taskinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_taskinst_pkey ON public.dtlms_wf_hi_taskinst USING btree (id_)`
- `idx_dtlms_wf_hi_taskinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_taskinst_proc_inst ON public.dtlms_wf_hi_taskinst USING btree (proc_inst_id_)`

### `dtlms_wf_hi_varinst`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(128) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `exec_id_` | character varying(64) | YES |  |
| `task_id_` | character varying(64) | YES |  |
| `name_` | character varying(128) | NO |  |
| `var_type_` | character varying(32) | NO |  |
| `text_value_` | text | YES |  |
| `number_value_` | bigint(64,0) | YES |  |
| `json_value_` | jsonb | YES |  |
| `create_time_` | timestamp with time zone | NO |  |
| `last_updated_time_` | timestamp with time zone | NO |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_hi_varinst_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_hi_varinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_varinst_pkey ON public.dtlms_wf_hi_varinst USING btree (id_)`
- `idx_dtlms_wf_hi_varinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_varinst_proc_inst ON public.dtlms_wf_hi_varinst USING btree (proc_inst_id_)`

### `dtlms_wf_re_deployment`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `name_` | character varying(255) | NO |  |
| `category_` | character varying(128) | YES |  |
| `key_` | character varying(128) | YES |  |
| `deploy_time_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `tenant_id_` | character varying(64) | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_re_deployment_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_re_deployment_pkey`: `CREATE UNIQUE INDEX dtlms_wf_re_deployment_pkey ON public.dtlms_wf_re_deployment USING btree (id_)`

### `dtlms_wf_re_procdef`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `key_` | character varying(128) | NO |  |
| `version_` | integer(32,0) | NO | 1 |
| `deployment_id_` | character varying(64) | YES |  |
| `resource_name_` | character varying(255) | YES |  |
| `diagram_resource_name_` | character varying(255) | YES |  |
| `name_` | character varying(255) | NO |  |
| `category_` | character varying(128) | YES |  |
| `description_` | text | YES |  |
| `suspension_state_` | integer(32,0) | NO | 1 |
| `tenant_id_` | character varying(64) | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_re_procdef_deployment_id__fkey` | FOREIGN KEY | `FOREIGN KEY (deployment_id_) REFERENCES dtlms_wf_re_deployment(id_)` |
| `dtlms_wf_re_procdef_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_re_procdef_pkey`: `CREATE UNIQUE INDEX dtlms_wf_re_procdef_pkey ON public.dtlms_wf_re_procdef USING btree (id_)`
- `idx_dtlms_wf_re_procdef_key`: `CREATE INDEX idx_dtlms_wf_re_procdef_key ON public.dtlms_wf_re_procdef USING btree (key_)`

### `dtlms_wf_ru_execution`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `proc_def_id_` | character varying(64) | NO |  |
| `business_key_` | character varying(64) | YES |  |
| `parent_id_` | character varying(64) | YES |  |
| `act_id_` | character varying(128) | YES |  |
| `is_active_` | boolean | NO | true |
| `is_concurrent_` | boolean | NO | false |
| `is_scope_` | boolean | NO | true |
| `start_time_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `start_user_id_` | character varying(64) | YES |  |
| `super_exec_` | character varying(64) | YES |  |
| `tenant_id_` | character varying(64) | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_ru_execution_proc_def_id__fkey` | FOREIGN KEY | `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)` |
| `dtlms_wf_ru_execution_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_ru_execution_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_execution_pkey ON public.dtlms_wf_ru_execution USING btree (id_)`
- `idx_dtlms_wf_ru_execution_proc_inst`: `CREATE INDEX idx_dtlms_wf_ru_execution_proc_inst ON public.dtlms_wf_ru_execution USING btree (proc_inst_id_)`

### `dtlms_wf_ru_identitylink`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | bigint(64,0) | NO | nextval('dtlms_wf_ru_identitylink_id__seq'::regclass) |
| `task_id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | YES |  |
| `user_id_` | character varying(64) | YES |  |
| `group_id_` | character varying(64) | YES |  |
| `link_type_` | character varying(32) | NO |  |
| `created_at_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_ru_identitylink_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_ru_identitylink_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_identitylink_pkey ON public.dtlms_wf_ru_identitylink USING btree (id_)`

### `dtlms_wf_ru_task`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(64) | NO |  |
| `exec_id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `proc_def_id_` | character varying(64) | NO |  |
| `task_def_key_` | character varying(128) | YES |  |
| `name_` | character varying(255) | NO |  |
| `business_key_` | character varying(64) | YES |  |
| `assignee_` | character varying(64) | YES |  |
| `owner_` | character varying(64) | YES |  |
| `create_time_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `due_date_` | timestamp with time zone | YES |  |
| `claim_time_` | timestamp with time zone | YES |  |
| `priority_` | integer(32,0) | NO | 50 |
| `suspension_state_` | integer(32,0) | NO | 1 |
| `tenant_id_` | character varying(64) | YES |  |
| `form_key_` | character varying(255) | YES |  |
| `description_` | text | YES |  |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_ru_task_exec_id__fkey` | FOREIGN KEY | `FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_)` |
| `dtlms_wf_ru_task_proc_def_id__fkey` | FOREIGN KEY | `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)` |
| `dtlms_wf_ru_task_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_ru_task_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_task_pkey ON public.dtlms_wf_ru_task USING btree (id_)`
- `idx_dtlms_wf_ru_task_business_key`: `CREATE INDEX idx_dtlms_wf_ru_task_business_key ON public.dtlms_wf_ru_task USING btree (business_key_)`
- `idx_dtlms_wf_ru_task_proc_inst`: `CREATE INDEX idx_dtlms_wf_ru_task_proc_inst ON public.dtlms_wf_ru_task USING btree (proc_inst_id_)`

### `dtlms_wf_ru_variable`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id_` | character varying(128) | NO |  |
| `exec_id_` | character varying(64) | NO |  |
| `proc_inst_id_` | character varying(64) | NO |  |
| `task_id_` | character varying(64) | YES |  |
| `name_` | character varying(128) | NO |  |
| `var_type_` | character varying(32) | NO |  |
| `text_value_` | text | YES |  |
| `number_value_` | bigint(64,0) | YES |  |
| `json_value_` | jsonb | YES |  |
| `create_time_` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id_`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_wf_ru_variable_exec_id__fkey` | FOREIGN KEY | `FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_)` |
| `dtlms_wf_ru_variable_pkey` | PRIMARY KEY | `PRIMARY KEY (id_)` |

**索引**

- `dtlms_wf_ru_variable_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_variable_pkey ON public.dtlms_wf_ru_variable USING btree (id_)`

### `dtlms_written_exam_scores`

| 列名 | 数据类型 | 可空 | 默认值 |
|------|----------|------|--------|
| `id` | bigint(64,0) | NO | nextval('dtlms_written_exam_scores_id_seq'::regclass) |
| `application_id` | bigint(64,0) | NO |  |
| `exam_date` | date | YES |  |
| `exam_score` | numeric(5,2) | YES |  |
| `import_batch_no` | character varying(64) | YES |  |
| `created_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| `updated_at` | timestamp with time zone | NO | CURRENT_TIMESTAMP |

**主键**: (`id`)

**约束**

| 名称 | 类型 | 定义 |
|------|------|------|
| `dtlms_written_exam_scores_application_id_fkey` | FOREIGN KEY | `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)` |
| `dtlms_written_exam_scores_pkey` | PRIMARY KEY | `PRIMARY KEY (id)` |

**索引**

- `dtlms_written_exam_scores_pkey`: `CREATE UNIQUE INDEX dtlms_written_exam_scores_pkey ON public.dtlms_written_exam_scores USING btree (id)`

## 视图（Views）

### `dtlms_v_degree_pipeline`

```sql
 SELECT t.id AS thesis_id,
    s.student_no,
    s.full_name,
    a.full_name AS advisor_name,
    t.title,
    t.plagiarism_rate,
    t.thesis_status,
    t.blind_review_status,
    t.defense_date,
    t.degree_granted,
    count(tr.id) AS review_count,
    avg(tr.review_score) AS avg_review_score
   FROM (((dtlms_theses t
     JOIN dtlms_students s ON ((s.id = t.student_id)))
     JOIN dtlms_advisors a ON ((a.id = t.advisor_id)))
     LEFT JOIN dtlms_thesis_reviews tr ON ((tr.thesis_id = t.id)))
  WHERE (t.is_deleted = false)
  GROUP BY t.id, s.student_no, s.full_name, a.full_name, t.title, t.plagiarism_rate, t.thesis_status, t.blind_review_status, t.defense_date, t.degree_granted;
```

### `dtlms_v_recruitment_dashboard`

```sql
 SELECT rp.id AS plan_id,
    rp.plan_code,
    rp.plan_name,
    rp.academic_year,
    rp.semester,
    rp.plan_status,
    count(DISTINCT ra.id) AS application_total,
    count(DISTINCT
        CASE
            WHEN ((ra.application_status)::text = 'qualified'::text) THEN ra.id
            ELSE NULL::bigint
        END) AS qualified_total,
    count(DISTINCT
        CASE
            WHEN ((ra.application_status)::text = 'interviewing'::text) THEN ra.id
            ELSE NULL::bigint
        END) AS interviewing_total,
    count(DISTINCT
        CASE
            WHEN ((ad.decision_status)::text = ANY (ARRAY[('pre_admitted'::character varying)::text, ('accepted'::character varying)::text])) THEN ad.id
            ELSE NULL::bigint
        END) AS admitted_total,
    avg(ms.material_score) AS avg_material_score
   FROM (((dtlms_recruitment_plans rp
     LEFT JOIN dtlms_recruitment_applications ra ON (((ra.plan_id = rp.id) AND (ra.is_deleted = false))))
     LEFT JOIN dtlms_material_scores ms ON ((ms.application_id = ra.id)))
     LEFT JOIN dtlms_admission_decisions ad ON ((ad.application_id = ra.id)))
  WHERE (rp.is_deleted = false)
  GROUP BY rp.id, rp.plan_code, rp.plan_name, rp.academic_year, rp.semester, rp.plan_status;
```

### `dtlms_v_student_lifecycle_snapshot`

```sql
 WITH latest_report AS (
         SELECT DISTINCT ON (dtlms_scientific_reports.student_id) dtlms_scientific_reports.student_id,
            dtlms_scientific_reports.period_label,
            dtlms_scientific_reports.report_status,
            dtlms_scientific_reports.review_score,
            dtlms_scientific_reports.updated_at
           FROM dtlms_scientific_reports
          WHERE (dtlms_scientific_reports.is_deleted = false)
          ORDER BY dtlms_scientific_reports.student_id, dtlms_scientific_reports.updated_at DESC
        ), latest_admission AS (
         SELECT DISTINCT ON (dtlms_admission_decisions.application_id) dtlms_admission_decisions.application_id,
            dtlms_admission_decisions.decision_status,
            dtlms_admission_decisions.final_score,
            dtlms_admission_decisions.updated_at
           FROM dtlms_admission_decisions
          ORDER BY dtlms_admission_decisions.application_id, dtlms_admission_decisions.updated_at DESC
        )
 SELECT s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    s.degree_type,
    s.team_name,
    a.full_name AS primary_advisor_name,
    tp.version_no AS training_plan_version,
    tp.plan_status,
    lr.period_label AS latest_report_period,
    lr.report_status AS latest_report_status,
    lr.review_score AS latest_report_score,
    t.title AS thesis_title,
    t.thesis_status,
    t.blind_review_status,
    t.degree_granted
   FROM ((((dtlms_students s
     LEFT JOIN dtlms_advisors a ON ((a.id = s.primary_advisor_id)))
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.version_no,
            dtlms_training_plans.plan_status
           FROM dtlms_training_plans
          WHERE ((dtlms_training_plans.student_id = s.id) AND (dtlms_training_plans.is_deleted = false))
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON (true))
     LEFT JOIN latest_report lr ON ((lr.student_id = s.id)))
     LEFT JOIN LATERAL ( SELECT dtlms_theses.title,
            dtlms_theses.thesis_status,
            dtlms_theses.blind_review_status,
            dtlms_theses.degree_granted
           FROM dtlms_theses
          WHERE ((dtlms_theses.student_id = s.id) AND (dtlms_theses.is_deleted = false))
          ORDER BY dtlms_theses.updated_at DESC
         LIMIT 1) t ON (true))
  WHERE (s.is_deleted = false);
```

### `dtlms_v_training_compliance`

```sql
 SELECT s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    a.full_name AS advisor_name,
    tp.plan_status,
    tp.report_cycle,
    count(sr.id) FILTER (WHERE ((sr.report_status)::text = ANY (ARRAY[('submitted'::character varying)::text, ('reviewed'::character varying)::text]))) AS submitted_report_count,
    count(sr.id) FILTER (WHERE ((sr.report_status)::text = 'pending'::text)) AS pending_report_count,
    count(os.id) FILTER (WHERE ((os.approval_status)::text = ANY (ARRAY[('submitted'::character varying)::text, ('approved'::character varying)::text, ('ongoing'::character varying)::text]))) AS outbound_study_count
   FROM ((((dtlms_students s
     LEFT JOIN dtlms_advisors a ON ((a.id = s.primary_advisor_id)))
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.plan_status,
            dtlms_training_plans.report_cycle
           FROM dtlms_training_plans
          WHERE ((dtlms_training_plans.student_id = s.id) AND (dtlms_training_plans.is_deleted = false))
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON (true))
     LEFT JOIN dtlms_scientific_reports sr ON (((sr.student_id = s.id) AND (sr.is_deleted = false))))
     LEFT JOIN dtlms_outbound_studies os ON (((os.student_id = s.id) AND (os.is_deleted = false))))
  WHERE (s.is_deleted = false)
  GROUP BY s.id, s.student_no, s.full_name, s.current_status, a.full_name, tp.plan_status, tp.report_cycle;
```

## 枚举/复合类型（Enums / Composite Types）

- `dtlms_achievements` (composite)
- `dtlms_admission_decisions` (composite)
- `dtlms_advisor_screening_batches` (composite)
- `dtlms_advisor_screening_items` (composite)
- `dtlms_advisors` (composite)
- `dtlms_application_materials` (composite)
- `dtlms_audit_policies` (composite)
- `dtlms_background_assessments` (composite)
- `dtlms_data_sync_logs` (composite)
- `dtlms_dict_data` (composite)
- `dtlms_dict_types` (composite)
- `dtlms_initial_screening_confirmations` (composite)
- `dtlms_initial_screening_notifications` (composite)
- `dtlms_integrations` (composite)
- `dtlms_interview_groups` (composite)
- `dtlms_interview_schedules` (composite)
- `dtlms_interview_scores` (composite)
- `dtlms_login_logs` (composite)
- `dtlms_material_scores` (composite)
- `dtlms_news_articles` (composite)
- `dtlms_notification_delivery_logs` (composite)
- `dtlms_notification_templates` (composite)
- `dtlms_operation_logs` (composite)
- `dtlms_outbound_studies` (composite)
- `dtlms_permissions` (composite)
- `dtlms_plan_offer` (composite)
- `dtlms_portal_application_achievement_records` (composite)
- `dtlms_portal_application_attachments` (composite)
- `dtlms_portal_application_declarations` (composite)
- `dtlms_portal_application_education_experiences` (composite)
- `dtlms_portal_application_english_proficiencies` (composite)
- `dtlms_portal_application_family_members` (composite)
- `dtlms_portal_application_personal_statements` (composite)
- `dtlms_portal_application_practice_experiences` (composite)
- `dtlms_portal_application_preferences` (composite)
- `dtlms_portal_student_profiles` (composite)
- `dtlms_portal_students` (composite)
- `dtlms_qualification_review_logs` (composite)
- `dtlms_qualification_reviews` (composite)
- `dtlms_recruitment_applications` (composite)
- `dtlms_recruitment_plans` (composite)
- `dtlms_research_fields` (composite)
- `dtlms_research_projects` (composite)
- `dtlms_reviewer_assignments` (composite)
- `dtlms_role_permissions` (composite)
- `dtlms_roles` (composite)
- `dtlms_schema_migrations` (composite)
- `dtlms_scientific_reports` (composite)
- `dtlms_student_advisor_history` (composite)
- `dtlms_student_team_history` (composite)
- `dtlms_students` (composite)
- `dtlms_system_configs` (composite)
- `dtlms_team_advisors` (composite)
- `dtlms_team_leaders` (composite)
- `dtlms_teams` (composite)
- `dtlms_theses` (composite)
- `dtlms_thesis_reviews` (composite)
- `dtlms_training_plan_versions` (composite)
- `dtlms_training_plans` (composite)
- `dtlms_user_profiles` (composite)
- `dtlms_user_roles` (composite)
- `dtlms_users` (composite)
- `dtlms_v_degree_pipeline` (composite)
- `dtlms_v_recruitment_dashboard` (composite)
- `dtlms_v_student_lifecycle_snapshot` (composite)
- `dtlms_v_training_compliance` (composite)
- `dtlms_wf_de_model` (composite)
- `dtlms_wf_hi_actinst` (composite)
- `dtlms_wf_hi_procinst` (composite)
- `dtlms_wf_hi_taskinst` (composite)
- `dtlms_wf_hi_varinst` (composite)
- `dtlms_wf_re_deployment` (composite)
- `dtlms_wf_re_procdef` (composite)
- `dtlms_wf_ru_execution` (composite)
- `dtlms_wf_ru_identitylink` (composite)
- `dtlms_wf_ru_task` (composite)
- `dtlms_wf_ru_variable` (composite)
- `dtlms_written_exam_scores` (composite)

## 序列（Sequences）

- `dtlms_achievements_id_seq` (bigint)
- `dtlms_admission_decisions_id_seq` (bigint)
- `dtlms_advisor_screening_batches_id_seq` (bigint)
- `dtlms_advisor_screening_items_id_seq` (bigint)
- `dtlms_advisors_id_seq` (bigint)
- `dtlms_application_materials_id_seq` (bigint)
- `dtlms_background_assessments_id_seq` (bigint)
- `dtlms_data_sync_logs_id_seq` (bigint)
- `dtlms_dict_data_id_seq` (bigint)
- `dtlms_dict_types_id_seq` (bigint)
- `dtlms_initial_screening_confirmations_id_seq` (bigint)
- `dtlms_initial_screening_notifications_id_seq` (bigint)
- `dtlms_interview_groups_id_seq` (bigint)
- `dtlms_interview_schedules_id_seq` (bigint)
- `dtlms_interview_scores_id_seq` (bigint)
- `dtlms_login_logs_id_seq` (bigint)
- `dtlms_material_scores_id_seq` (bigint)
- `dtlms_news_articles_id_seq` (bigint)
- `dtlms_notification_delivery_logs_id_seq` (bigint)
- `dtlms_notification_templates_id_seq` (bigint)
- `dtlms_operation_logs_id_seq` (bigint)
- `dtlms_outbound_studies_id_seq` (bigint)
- `dtlms_permissions_id_seq` (bigint)
- `dtlms_portal_application_achievement_records_id_seq` (bigint)
- `dtlms_portal_application_attachments_id_seq` (bigint)
- `dtlms_portal_application_education_experiences_id_seq` (bigint)
- `dtlms_portal_application_english_proficiencies_id_seq` (bigint)
- `dtlms_portal_application_family_members_id_seq` (bigint)
- `dtlms_portal_application_practice_experiences_id_seq` (bigint)
- `dtlms_portal_application_preferences_id_seq` (bigint)
- `dtlms_portal_students_id_seq` (bigint)
- `dtlms_qualification_review_logs_id_seq` (bigint)
- `dtlms_qualification_reviews_id_seq` (bigint)
- `dtlms_recruitment_applications_id_seq` (bigint)
- `dtlms_recruitment_plans_id_seq` (bigint)
- `dtlms_research_fields_id_seq` (bigint)
- `dtlms_research_projects_id_seq` (bigint)
- `dtlms_reviewer_assignments_id_seq` (bigint)
- `dtlms_role_permissions_id_seq` (bigint)
- `dtlms_roles_id_seq` (bigint)
- `dtlms_scientific_reports_id_seq` (bigint)
- `dtlms_student_advisor_history_id_seq` (bigint)
- `dtlms_student_team_history_id_seq` (bigint)
- `dtlms_students_id_seq` (bigint)
- `dtlms_system_configs_id_seq` (bigint)
- `dtlms_team_advisors_id_seq` (bigint)
- `dtlms_teams_id_seq` (bigint)
- `dtlms_theses_id_seq` (bigint)
- `dtlms_thesis_reviews_id_seq` (bigint)
- `dtlms_training_plan_versions_id_seq` (bigint)
- `dtlms_training_plans_id_seq` (bigint)
- `dtlms_user_roles_id_seq` (bigint)
- `dtlms_users_id_seq` (bigint)
- `dtlms_wf_ru_identitylink_id__seq` (bigint)
- `dtlms_written_exam_scores_id_seq` (bigint)

## 函数 / 存储过程（Functions）

## 索引（Indexes）

- `dtlms_achievements.dtlms_achievements_pkey`: `CREATE UNIQUE INDEX dtlms_achievements_pkey ON public.dtlms_achievements USING btree (id)`
- `dtlms_admission_decisions.dtlms_admission_decisions_pkey`: `CREATE UNIQUE INDEX dtlms_admission_decisions_pkey ON public.dtlms_admission_decisions USING btree (id)`
- `dtlms_admission_decisions.idx_admission_decision_status`: `CREATE INDEX idx_admission_decision_status ON public.dtlms_admission_decisions USING btree (decision_status)`
- `dtlms_advisor_screening_batches.dtlms_advisor_screening_batches_pkey`: `CREATE UNIQUE INDEX dtlms_advisor_screening_batches_pkey ON public.dtlms_advisor_screening_batches USING btree (id)`
- `dtlms_advisor_screening_batches.idx_advisor_screening_batches_advisor_round`: `CREATE INDEX idx_advisor_screening_batches_advisor_round ON public.dtlms_advisor_screening_batches USING btree (advisor_username, screening_round, submitted_at DESC)`
- `dtlms_advisor_screening_items.dtlms_advisor_screening_items_pkey`: `CREATE UNIQUE INDEX dtlms_advisor_screening_items_pkey ON public.dtlms_advisor_screening_items USING btree (id)`
- `dtlms_advisor_screening_items.idx_advisor_screening_items_application`: `CREATE INDEX idx_advisor_screening_items_application ON public.dtlms_advisor_screening_items USING btree (application_id, screening_round, created_at DESC)`
- `dtlms_advisor_screening_items.idx_advisor_screening_items_batch`: `CREATE INDEX idx_advisor_screening_items_batch ON public.dtlms_advisor_screening_items USING btree (batch_id)`
- `dtlms_advisor_screening_items.idx_advisor_screening_items_business_key`: `CREATE INDEX idx_advisor_screening_items_business_key ON public.dtlms_advisor_screening_items USING btree (business_key)`
- `dtlms_advisor_screening_items.uq_advisor_screening_items_application_round`: `CREATE UNIQUE INDEX uq_advisor_screening_items_application_round ON public.dtlms_advisor_screening_items USING btree (application_id, screening_round)`
- `dtlms_advisor_screening_items.uq_advisor_screening_items_candidate_round`: `CREATE UNIQUE INDEX uq_advisor_screening_items_candidate_round ON public.dtlms_advisor_screening_items USING btree (candidate_no, screening_round)`
- `dtlms_advisors.dtlms_advisors_advisor_no_key`: `CREATE UNIQUE INDEX dtlms_advisors_advisor_no_key ON public.dtlms_advisors USING btree (advisor_no)`
- `dtlms_advisors.dtlms_advisors_pkey`: `CREATE UNIQUE INDEX dtlms_advisors_pkey ON public.dtlms_advisors USING btree (id)`
- `dtlms_advisors.idx_dtlms_advisors_user_id`: `CREATE UNIQUE INDEX idx_dtlms_advisors_user_id ON public.dtlms_advisors USING btree (user_id) WHERE (user_id IS NOT NULL)`
- `dtlms_application_materials.dtlms_application_materials_pkey`: `CREATE UNIQUE INDEX dtlms_application_materials_pkey ON public.dtlms_application_materials USING btree (id)`
- `dtlms_audit_policies.dtlms_audit_policies_pkey`: `CREATE UNIQUE INDEX dtlms_audit_policies_pkey ON public.dtlms_audit_policies USING btree (id)`
- `dtlms_background_assessments.dtlms_background_assessments_application_id_evaluator_usern_key`: `CREATE UNIQUE INDEX dtlms_background_assessments_application_id_evaluator_usern_key ON public.dtlms_background_assessments USING btree (application_id, evaluator_username)`
- `dtlms_background_assessments.dtlms_background_assessments_pkey`: `CREATE UNIQUE INDEX dtlms_background_assessments_pkey ON public.dtlms_background_assessments USING btree (id)`
- `dtlms_background_assessments.idx_background_assessment_application`: `CREATE INDEX idx_background_assessment_application ON public.dtlms_background_assessments USING btree (application_id, assessed_at DESC)`
- `dtlms_background_assessments.idx_background_assessment_result`: `CREATE INDEX idx_background_assessment_result ON public.dtlms_background_assessments USING btree (assessment_result)`
- `dtlms_data_sync_logs.dtlms_data_sync_logs_pkey`: `CREATE UNIQUE INDEX dtlms_data_sync_logs_pkey ON public.dtlms_data_sync_logs USING btree (id)`
- `dtlms_data_sync_logs.idx_sync_logs_source_target`: `CREATE INDEX idx_sync_logs_source_target ON public.dtlms_data_sync_logs USING btree (source_system, target_system, created_at)`
- `dtlms_dict_data.dtlms_dict_data_dict_type_value_key`: `CREATE UNIQUE INDEX dtlms_dict_data_dict_type_value_key ON public.dtlms_dict_data USING btree (dict_type, value)`
- `dtlms_dict_data.dtlms_dict_data_pkey`: `CREATE UNIQUE INDEX dtlms_dict_data_pkey ON public.dtlms_dict_data USING btree (id)`
- `dtlms_dict_data.idx_dtlms_dict_data_type_sort`: `CREATE INDEX idx_dtlms_dict_data_type_sort ON public.dtlms_dict_data USING btree (dict_type, sort_order, id)`
- `dtlms_dict_types.dtlms_dict_types_dict_type_key`: `CREATE UNIQUE INDEX dtlms_dict_types_dict_type_key ON public.dtlms_dict_types USING btree (dict_type)`
- `dtlms_dict_types.dtlms_dict_types_pkey`: `CREATE UNIQUE INDEX dtlms_dict_types_pkey ON public.dtlms_dict_types USING btree (id)`
- `dtlms_initial_screening_confirmations.dtlms_initial_screening_confirmations_pkey`: `CREATE UNIQUE INDEX dtlms_initial_screening_confirmations_pkey ON public.dtlms_initial_screening_confirmations USING btree (id)`
- `dtlms_initial_screening_confirmations.idx_initial_screening_confirmations_application`: `CREATE INDEX idx_initial_screening_confirmations_application ON public.dtlms_initial_screening_confirmations USING btree (application_id, confirmed_at DESC)`
- `dtlms_initial_screening_confirmations.uq_initial_screening_confirmations_application`: `CREATE UNIQUE INDEX uq_initial_screening_confirmations_application ON public.dtlms_initial_screening_confirmations USING btree (application_id)`
- `dtlms_initial_screening_notifications.dtlms_initial_screening_notifications_pkey`: `CREATE UNIQUE INDEX dtlms_initial_screening_notifications_pkey ON public.dtlms_initial_screening_notifications USING btree (id)`
- `dtlms_initial_screening_notifications.idx_initial_screening_notifications_application`: `CREATE INDEX idx_initial_screening_notifications_application ON public.dtlms_initial_screening_notifications USING btree (application_id, created_at DESC)`
- `dtlms_initial_screening_notifications.idx_initial_screening_notifications_status`: `CREATE INDEX idx_initial_screening_notifications_status ON public.dtlms_initial_screening_notifications USING btree (notification_status, notification_channel)`
- `dtlms_integrations.dtlms_integrations_pkey`: `CREATE UNIQUE INDEX dtlms_integrations_pkey ON public.dtlms_integrations USING btree (id)`
- `dtlms_interview_groups.dtlms_interview_groups_pkey`: `CREATE UNIQUE INDEX dtlms_interview_groups_pkey ON public.dtlms_interview_groups USING btree (id)`
- `dtlms_interview_groups.dtlms_interview_groups_plan_id_group_code_key`: `CREATE UNIQUE INDEX dtlms_interview_groups_plan_id_group_code_key ON public.dtlms_interview_groups USING btree (plan_id, group_code)`
- `dtlms_interview_schedules.dtlms_interview_schedules_admission_ticket_no_key`: `CREATE UNIQUE INDEX dtlms_interview_schedules_admission_ticket_no_key ON public.dtlms_interview_schedules USING btree (admission_ticket_no)`
- `dtlms_interview_schedules.dtlms_interview_schedules_pkey`: `CREATE UNIQUE INDEX dtlms_interview_schedules_pkey ON public.dtlms_interview_schedules USING btree (id)`
- `dtlms_interview_schedules.idx_interview_schedule_time`: `CREATE INDEX idx_interview_schedule_time ON public.dtlms_interview_schedules USING btree (starts_at, ends_at)`
- `dtlms_interview_scores.dtlms_interview_scores_pkey`: `CREATE UNIQUE INDEX dtlms_interview_scores_pkey ON public.dtlms_interview_scores USING btree (id)`
- `dtlms_login_logs.dtlms_login_logs_pkey`: `CREATE UNIQUE INDEX dtlms_login_logs_pkey ON public.dtlms_login_logs USING btree (id)`
- `dtlms_material_scores.dtlms_material_scores_pkey`: `CREATE UNIQUE INDEX dtlms_material_scores_pkey ON public.dtlms_material_scores USING btree (id)`
- `dtlms_news_articles.dtlms_news_articles_news_code_key`: `CREATE UNIQUE INDEX dtlms_news_articles_news_code_key ON public.dtlms_news_articles USING btree (news_code)`
- `dtlms_news_articles.dtlms_news_articles_pkey`: `CREATE UNIQUE INDEX dtlms_news_articles_pkey ON public.dtlms_news_articles USING btree (id)`
- `dtlms_news_articles.idx_dtlms_news_articles_deleted_order`: `CREATE INDEX idx_dtlms_news_articles_deleted_order ON public.dtlms_news_articles USING btree (is_deleted, display_order DESC, id DESC)`
- `dtlms_news_articles.idx_dtlms_news_articles_status_published`: `CREATE INDEX idx_dtlms_news_articles_status_published ON public.dtlms_news_articles USING btree (status, published_at DESC, display_order DESC, id DESC) WHERE (is_deleted = false)`
- `dtlms_news_articles.idx_dtlms_news_articles_type_status`: `CREATE INDEX idx_dtlms_news_articles_type_status ON public.dtlms_news_articles USING btree (news_type, status, published_at DESC, id DESC) WHERE (is_deleted = false)`
- `dtlms_notification_delivery_logs.dtlms_notification_delivery_logs_pkey`: `CREATE UNIQUE INDEX dtlms_notification_delivery_logs_pkey ON public.dtlms_notification_delivery_logs USING btree (id)`
- `dtlms_notification_delivery_logs.idx_notification_delivery_logs_channel_time`: `CREATE INDEX idx_notification_delivery_logs_channel_time ON public.dtlms_notification_delivery_logs USING btree (channel, created_at)`
- `dtlms_notification_delivery_logs.idx_notification_delivery_logs_recipient`: `CREATE INDEX idx_notification_delivery_logs_recipient ON public.dtlms_notification_delivery_logs USING btree (recipient)`
- `dtlms_notification_delivery_logs.idx_notification_delivery_logs_status_time`: `CREATE INDEX idx_notification_delivery_logs_status_time ON public.dtlms_notification_delivery_logs USING btree (send_status, created_at)`
- `dtlms_notification_templates.dtlms_notification_templates_pkey`: `CREATE UNIQUE INDEX dtlms_notification_templates_pkey ON public.dtlms_notification_templates USING btree (id)`
- `dtlms_notification_templates.dtlms_notification_templates_template_code_key`: `CREATE UNIQUE INDEX dtlms_notification_templates_template_code_key ON public.dtlms_notification_templates USING btree (template_code)`
- `dtlms_operation_logs.dtlms_operation_logs_pkey`: `CREATE UNIQUE INDEX dtlms_operation_logs_pkey ON public.dtlms_operation_logs USING btree (id)`
- `dtlms_operation_logs.idx_operation_logs_entity`: `CREATE INDEX idx_operation_logs_entity ON public.dtlms_operation_logs USING btree (entity_name, entity_id)`
- `dtlms_operation_logs.idx_operation_logs_module_time`: `CREATE INDEX idx_operation_logs_module_time ON public.dtlms_operation_logs USING btree (module_name, created_at)`
- `dtlms_outbound_studies.dtlms_outbound_studies_pkey`: `CREATE UNIQUE INDEX dtlms_outbound_studies_pkey ON public.dtlms_outbound_studies USING btree (id)`
- `dtlms_outbound_studies.idx_outbound_studies_status`: `CREATE INDEX idx_outbound_studies_status ON public.dtlms_outbound_studies USING btree (approval_status)`
- `dtlms_outbound_studies.ux_dtlms_outbound_studies_business_key`: `CREATE UNIQUE INDEX ux_dtlms_outbound_studies_business_key ON public.dtlms_outbound_studies USING btree (business_key)`
- `dtlms_permissions.dtlms_permissions_permission_code_key`: `CREATE UNIQUE INDEX dtlms_permissions_permission_code_key ON public.dtlms_permissions USING btree (permission_code)`
- `dtlms_permissions.dtlms_permissions_pkey`: `CREATE UNIQUE INDEX dtlms_permissions_pkey ON public.dtlms_permissions USING btree (id)`
- `dtlms_plan_offer.dtlms_plan_offer_pkey`: `CREATE UNIQUE INDEX dtlms_plan_offer_pkey ON public.dtlms_plan_offer USING btree (id)`
- `dtlms_portal_application_achievement_records.dtlms_portal_application_achievement_records_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_achievement_records_pkey ON public.dtlms_portal_application_achievement_records USING btree (id)`
- `dtlms_portal_application_achievement_records.idx_portal_application_achievement_application`: `CREATE INDEX idx_portal_application_achievement_application ON public.dtlms_portal_application_achievement_records USING btree (application_id, achievement_type)`
- `dtlms_portal_application_attachments.dtlms_portal_application_attachments_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_attachments_pkey ON public.dtlms_portal_application_attachments USING btree (id)`
- `dtlms_portal_application_attachments.idx_portal_application_attachment_owner`: `CREATE INDEX idx_portal_application_attachment_owner ON public.dtlms_portal_application_attachments USING btree (application_id, owner_type, owner_id)`
- `dtlms_portal_application_declarations.dtlms_portal_application_declarations_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_declarations_pkey ON public.dtlms_portal_application_declarations USING btree (application_id)`
- `dtlms_portal_application_education_experiences.dtlms_portal_application_education_experiences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_education_experiences_pkey ON public.dtlms_portal_application_education_experiences USING btree (id)`
- `dtlms_portal_application_education_experiences.idx_portal_application_education_application`: `CREATE INDEX idx_portal_application_education_application ON public.dtlms_portal_application_education_experiences USING btree (application_id, sort_order)`
- `dtlms_portal_application_english_proficiencies.dtlms_portal_application_english_proficiencies_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_english_proficiencies_pkey ON public.dtlms_portal_application_english_proficiencies USING btree (id)`
- `dtlms_portal_application_english_proficiencies.idx_portal_application_english_application`: `CREATE INDEX idx_portal_application_english_application ON public.dtlms_portal_application_english_proficiencies USING btree (application_id)`
- `dtlms_portal_application_family_members.dtlms_portal_application_family_members_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_family_members_pkey ON public.dtlms_portal_application_family_members USING btree (id)`
- `dtlms_portal_application_family_members.idx_portal_application_family_application`: `CREATE INDEX idx_portal_application_family_application ON public.dtlms_portal_application_family_members USING btree (application_id)`
- `dtlms_portal_application_family_members.ux_portal_application_family_parent_unique`: `CREATE UNIQUE INDEX ux_portal_application_family_parent_unique ON public.dtlms_portal_application_family_members USING btree (application_id, relation_type) WHERE ((relation_type)::text = ANY (ARRAY[('父亲'::character varying)::text, ('母亲'::character varying)::text]))`
- `dtlms_portal_application_personal_statements.dtlms_portal_application_personal_statements_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_personal_statements_pkey ON public.dtlms_portal_application_personal_statements USING btree (application_id)`
- `dtlms_portal_application_practice_experiences.dtlms_portal_application_practice_experiences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_practice_experiences_pkey ON public.dtlms_portal_application_practice_experiences USING btree (id)`
- `dtlms_portal_application_practice_experiences.idx_portal_application_practice_application`: `CREATE INDEX idx_portal_application_practice_application ON public.dtlms_portal_application_practice_experiences USING btree (application_id)`
- `dtlms_portal_application_preferences.dtlms_portal_application_preferences_pkey`: `CREATE UNIQUE INDEX dtlms_portal_application_preferences_pkey ON public.dtlms_portal_application_preferences USING btree (id)`
- `dtlms_portal_application_preferences.idx_portal_application_preferences_application`: `CREATE INDEX idx_portal_application_preferences_application ON public.dtlms_portal_application_preferences USING btree (application_id, preference_order)`
- `dtlms_portal_application_preferences.uq_portal_application_preferences_order`: `CREATE UNIQUE INDEX uq_portal_application_preferences_order ON public.dtlms_portal_application_preferences USING btree (application_id, preference_order)`
- `dtlms_portal_student_profiles.dtlms_portal_student_profiles_pkey`: `CREATE UNIQUE INDEX dtlms_portal_student_profiles_pkey ON public.dtlms_portal_student_profiles USING btree (portal_student_id)`
- `dtlms_portal_students.dtlms_portal_students_email_key`: `CREATE UNIQUE INDEX dtlms_portal_students_email_key ON public.dtlms_portal_students USING btree (email)`
- `dtlms_portal_students.dtlms_portal_students_id_number_key`: `CREATE UNIQUE INDEX dtlms_portal_students_id_number_key ON public.dtlms_portal_students USING btree (id_number)`
- `dtlms_portal_students.dtlms_portal_students_phone_number_key`: `CREATE UNIQUE INDEX dtlms_portal_students_phone_number_key ON public.dtlms_portal_students USING btree (phone_number)`
- `dtlms_portal_students.dtlms_portal_students_pkey`: `CREATE UNIQUE INDEX dtlms_portal_students_pkey ON public.dtlms_portal_students USING btree (id)`
- `dtlms_portal_students.idx_dtlms_portal_students_selected_team_id`: `CREATE INDEX idx_dtlms_portal_students_selected_team_id ON public.dtlms_portal_students USING btree (selected_team_id) WHERE (selected_team_id IS NOT NULL)`
- `dtlms_qualification_review_logs.dtlms_qualification_review_logs_pkey`: `CREATE UNIQUE INDEX dtlms_qualification_review_logs_pkey ON public.dtlms_qualification_review_logs USING btree (id)`
- `dtlms_qualification_review_logs.idx_qualification_review_logs_application`: `CREATE INDEX idx_qualification_review_logs_application ON public.dtlms_qualification_review_logs USING btree (application_id, reviewed_at DESC)`
- `dtlms_qualification_review_logs.idx_qualification_review_logs_reviewer`: `CREATE INDEX idx_qualification_review_logs_reviewer ON public.dtlms_qualification_review_logs USING btree (reviewer_username, reviewed_at DESC)`
- `dtlms_qualification_reviews.dtlms_qualification_reviews_pkey`: `CREATE UNIQUE INDEX dtlms_qualification_reviews_pkey ON public.dtlms_qualification_reviews USING btree (id)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_candidate_no_key`: `CREATE UNIQUE INDEX dtlms_recruitment_applications_candidate_no_key ON public.dtlms_recruitment_applications USING btree (candidate_no)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_pkey`: `CREATE UNIQUE INDEX dtlms_recruitment_applications_pkey ON public.dtlms_recruitment_applications USING btree (id)`
- `dtlms_recruitment_applications.idx_applications_plan_status`: `CREATE INDEX idx_applications_plan_status ON public.dtlms_recruitment_applications USING btree (plan_id, application_status)`
- `dtlms_recruitment_applications.idx_applications_portal_student`: `CREATE INDEX idx_applications_portal_student ON public.dtlms_recruitment_applications USING btree (portal_student_id)`
- `dtlms_recruitment_applications.idx_dtlms_recruitment_applications_email`: `CREATE INDEX idx_dtlms_recruitment_applications_email ON public.dtlms_recruitment_applications USING btree (email)`
- `dtlms_recruitment_applications.idx_dtlms_recruitment_applications_first_choice_team_id`: `CREATE INDEX idx_dtlms_recruitment_applications_first_choice_team_id ON public.dtlms_recruitment_applications USING btree (first_choice_team_id) WHERE (first_choice_team_id IS NOT NULL)`
- `dtlms_recruitment_applications.idx_dtlms_recruitment_applications_phone_number`: `CREATE INDEX idx_dtlms_recruitment_applications_phone_number ON public.dtlms_recruitment_applications USING btree (phone_number)`
- `dtlms_recruitment_applications.idx_recruitment_applications_advisor_screening_status`: `CREATE INDEX idx_recruitment_applications_advisor_screening_status ON public.dtlms_recruitment_applications USING btree (advisor_screening_status, advisor_screening_round)`
- `dtlms_recruitment_applications.idx_recruitment_applications_initial_screening_status`: `CREATE INDEX idx_recruitment_applications_initial_screening_status ON public.dtlms_recruitment_applications USING btree (initial_screening_status, initial_screening_result)`
- `dtlms_recruitment_applications.ux_dtlms_recruitment_applications_business_key`: `CREATE UNIQUE INDEX ux_dtlms_recruitment_applications_business_key ON public.dtlms_recruitment_applications USING btree (business_key)`
- `dtlms_recruitment_plans.dtlms_recruitment_plans_pkey`: `CREATE UNIQUE INDEX dtlms_recruitment_plans_pkey ON public.dtlms_recruitment_plans USING btree (id)`
- `dtlms_recruitment_plans.dtlms_recruitment_plans_plan_code_key`: `CREATE UNIQUE INDEX dtlms_recruitment_plans_plan_code_key ON public.dtlms_recruitment_plans USING btree (plan_code)`
- `dtlms_research_fields.dtlms_research_fields_field_code_key`: `CREATE UNIQUE INDEX dtlms_research_fields_field_code_key ON public.dtlms_research_fields USING btree (field_code)`
- `dtlms_research_fields.dtlms_research_fields_pkey`: `CREATE UNIQUE INDEX dtlms_research_fields_pkey ON public.dtlms_research_fields USING btree (id)`
- `dtlms_research_projects.dtlms_research_projects_pkey`: `CREATE UNIQUE INDEX dtlms_research_projects_pkey ON public.dtlms_research_projects USING btree (id)`
- `dtlms_research_projects.dtlms_research_projects_project_code_key`: `CREATE UNIQUE INDEX dtlms_research_projects_project_code_key ON public.dtlms_research_projects USING btree (project_code)`
- `dtlms_reviewer_assignments.dtlms_reviewer_assignments_pkey`: `CREATE UNIQUE INDEX dtlms_reviewer_assignments_pkey ON public.dtlms_reviewer_assignments USING btree (id)`
- `dtlms_role_permissions.dtlms_role_permissions_pkey`: `CREATE UNIQUE INDEX dtlms_role_permissions_pkey ON public.dtlms_role_permissions USING btree (id)`
- `dtlms_role_permissions.dtlms_role_permissions_role_id_permission_id_key`: `CREATE UNIQUE INDEX dtlms_role_permissions_role_id_permission_id_key ON public.dtlms_role_permissions USING btree (role_id, permission_id)`
- `dtlms_roles.dtlms_roles_pkey`: `CREATE UNIQUE INDEX dtlms_roles_pkey ON public.dtlms_roles USING btree (id)`
- `dtlms_roles.dtlms_roles_role_code_key`: `CREATE UNIQUE INDEX dtlms_roles_role_code_key ON public.dtlms_roles USING btree (role_code)`
- `dtlms_schema_migrations.dtlms_schema_migrations_pkey`: `CREATE UNIQUE INDEX dtlms_schema_migrations_pkey ON public.dtlms_schema_migrations USING btree (file_name)`
- `dtlms_scientific_reports.dtlms_scientific_reports_pkey`: `CREATE UNIQUE INDEX dtlms_scientific_reports_pkey ON public.dtlms_scientific_reports USING btree (id)`
- `dtlms_scientific_reports.idx_reports_student_period`: `CREATE INDEX idx_reports_student_period ON public.dtlms_scientific_reports USING btree (student_id, period_label)`
- `dtlms_scientific_reports.ux_dtlms_scientific_reports_business_key`: `CREATE UNIQUE INDEX ux_dtlms_scientific_reports_business_key ON public.dtlms_scientific_reports USING btree (business_key)`
- `dtlms_student_advisor_history.dtlms_student_advisor_history_pkey`: `CREATE UNIQUE INDEX dtlms_student_advisor_history_pkey ON public.dtlms_student_advisor_history USING btree (id)`
- `dtlms_student_team_history.dtlms_student_team_history_pkey`: `CREATE UNIQUE INDEX dtlms_student_team_history_pkey ON public.dtlms_student_team_history USING btree (id)`
- `dtlms_students.dtlms_students_pkey`: `CREATE UNIQUE INDEX dtlms_students_pkey ON public.dtlms_students USING btree (id)`
- `dtlms_students.dtlms_students_student_no_key`: `CREATE UNIQUE INDEX dtlms_students_student_no_key ON public.dtlms_students USING btree (student_no)`
- `dtlms_students.idx_dtlms_students_portal_student_id`: `CREATE UNIQUE INDEX idx_dtlms_students_portal_student_id ON public.dtlms_students USING btree (portal_student_id) WHERE (portal_student_id IS NOT NULL)`
- `dtlms_students.idx_students_primary_advisor`: `CREATE INDEX idx_students_primary_advisor ON public.dtlms_students USING btree (primary_advisor_id)`
- `dtlms_students.idx_students_status`: `CREATE INDEX idx_students_status ON public.dtlms_students USING btree (current_status)`
- `dtlms_system_configs.dtlms_system_configs_config_key_key`: `CREATE UNIQUE INDEX dtlms_system_configs_config_key_key ON public.dtlms_system_configs USING btree (config_key)`
- `dtlms_system_configs.dtlms_system_configs_pkey`: `CREATE UNIQUE INDEX dtlms_system_configs_pkey ON public.dtlms_system_configs USING btree (id)`
- `dtlms_team_advisors.dtlms_team_advisors_pkey`: `CREATE UNIQUE INDEX dtlms_team_advisors_pkey ON public.dtlms_team_advisors USING btree (id)`
- `dtlms_team_advisors.idx_dtlms_team_advisors_team_user`: `CREATE INDEX idx_dtlms_team_advisors_team_user ON public.dtlms_team_advisors USING btree (team_id, advisor_user_id) WHERE (advisor_user_id IS NOT NULL)`
- `dtlms_team_leaders.dtlms_team_leaders_pkey`: `CREATE UNIQUE INDEX dtlms_team_leaders_pkey ON public.dtlms_team_leaders USING btree (id)`
- `dtlms_team_leaders.dtlms_team_leaders_team_id_user_id_key`: `CREATE UNIQUE INDEX dtlms_team_leaders_team_id_user_id_key ON public.dtlms_team_leaders USING btree (team_id, user_id)`
- `dtlms_team_leaders.idx_dtlms_team_leaders_team_id`: `CREATE INDEX idx_dtlms_team_leaders_team_id ON public.dtlms_team_leaders USING btree (team_id)`
- `dtlms_team_leaders.idx_dtlms_team_leaders_user_id`: `CREATE INDEX idx_dtlms_team_leaders_user_id ON public.dtlms_team_leaders USING btree (user_id)`
- `dtlms_teams.dtlms_teams_pkey`: `CREATE UNIQUE INDEX dtlms_teams_pkey ON public.dtlms_teams USING btree (id)`
- `dtlms_teams.dtlms_teams_team_code_key`: `CREATE UNIQUE INDEX dtlms_teams_team_code_key ON public.dtlms_teams USING btree (team_code)`
- `dtlms_teams.dtlms_teams_team_name_key`: `CREATE UNIQUE INDEX dtlms_teams_team_name_key ON public.dtlms_teams USING btree (team_name)`
- `dtlms_teams.idx_dtlms_teams_lead_user_id`: `CREATE INDEX idx_dtlms_teams_lead_user_id ON public.dtlms_teams USING btree (lead_user_id) WHERE (lead_user_id IS NOT NULL)`
- `dtlms_theses.dtlms_theses_pkey`: `CREATE UNIQUE INDEX dtlms_theses_pkey ON public.dtlms_theses USING btree (id)`
- `dtlms_theses.idx_thesis_status`: `CREATE INDEX idx_thesis_status ON public.dtlms_theses USING btree (thesis_status)`
- `dtlms_theses.ux_dtlms_theses_business_key`: `CREATE UNIQUE INDEX ux_dtlms_theses_business_key ON public.dtlms_theses USING btree (business_key)`
- `dtlms_thesis_reviews.dtlms_thesis_reviews_pkey`: `CREATE UNIQUE INDEX dtlms_thesis_reviews_pkey ON public.dtlms_thesis_reviews USING btree (id)`
- `dtlms_training_plan_versions.dtlms_training_plan_versions_pkey`: `CREATE UNIQUE INDEX dtlms_training_plan_versions_pkey ON public.dtlms_training_plan_versions USING btree (id)`
- `dtlms_training_plans.dtlms_training_plans_pkey`: `CREATE UNIQUE INDEX dtlms_training_plans_pkey ON public.dtlms_training_plans USING btree (id)`
- `dtlms_training_plans.idx_training_plan_student`: `CREATE INDEX idx_training_plan_student ON public.dtlms_training_plans USING btree (student_id)`
- `dtlms_user_profiles.dtlms_user_profiles_pkey`: `CREATE UNIQUE INDEX dtlms_user_profiles_pkey ON public.dtlms_user_profiles USING btree (username)`
- `dtlms_user_roles.dtlms_user_roles_pkey`: `CREATE UNIQUE INDEX dtlms_user_roles_pkey ON public.dtlms_user_roles USING btree (id)`
- `dtlms_user_roles.dtlms_user_roles_user_id_role_id_key`: `CREATE UNIQUE INDEX dtlms_user_roles_user_id_role_id_key ON public.dtlms_user_roles USING btree (user_id, role_id)`
- `dtlms_users.dtlms_users_pkey`: `CREATE UNIQUE INDEX dtlms_users_pkey ON public.dtlms_users USING btree (id)`
- `dtlms_users.dtlms_users_username_key`: `CREATE UNIQUE INDEX dtlms_users_username_key ON public.dtlms_users USING btree (username)`
- `dtlms_wf_de_model.dtlms_wf_de_model_pkey`: `CREATE UNIQUE INDEX dtlms_wf_de_model_pkey ON public.dtlms_wf_de_model USING btree (id_)`
- `dtlms_wf_hi_actinst.dtlms_wf_hi_actinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_actinst_pkey ON public.dtlms_wf_hi_actinst USING btree (id_)`
- `dtlms_wf_hi_actinst.idx_dtlms_wf_hi_actinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_actinst_proc_inst ON public.dtlms_wf_hi_actinst USING btree (proc_inst_id_)`
- `dtlms_wf_hi_procinst.dtlms_wf_hi_procinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_procinst_pkey ON public.dtlms_wf_hi_procinst USING btree (id_)`
- `dtlms_wf_hi_procinst.dtlms_wf_hi_procinst_proc_inst_id__key`: `CREATE UNIQUE INDEX dtlms_wf_hi_procinst_proc_inst_id__key ON public.dtlms_wf_hi_procinst USING btree (proc_inst_id_)`
- `dtlms_wf_hi_procinst.idx_dtlms_wf_hi_procinst_business_key`: `CREATE INDEX idx_dtlms_wf_hi_procinst_business_key ON public.dtlms_wf_hi_procinst USING btree (business_key_)`
- `dtlms_wf_hi_taskinst.dtlms_wf_hi_taskinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_taskinst_pkey ON public.dtlms_wf_hi_taskinst USING btree (id_)`
- `dtlms_wf_hi_taskinst.idx_dtlms_wf_hi_taskinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_taskinst_proc_inst ON public.dtlms_wf_hi_taskinst USING btree (proc_inst_id_)`
- `dtlms_wf_hi_varinst.dtlms_wf_hi_varinst_pkey`: `CREATE UNIQUE INDEX dtlms_wf_hi_varinst_pkey ON public.dtlms_wf_hi_varinst USING btree (id_)`
- `dtlms_wf_hi_varinst.idx_dtlms_wf_hi_varinst_proc_inst`: `CREATE INDEX idx_dtlms_wf_hi_varinst_proc_inst ON public.dtlms_wf_hi_varinst USING btree (proc_inst_id_)`
- `dtlms_wf_re_deployment.dtlms_wf_re_deployment_pkey`: `CREATE UNIQUE INDEX dtlms_wf_re_deployment_pkey ON public.dtlms_wf_re_deployment USING btree (id_)`
- `dtlms_wf_re_procdef.dtlms_wf_re_procdef_pkey`: `CREATE UNIQUE INDEX dtlms_wf_re_procdef_pkey ON public.dtlms_wf_re_procdef USING btree (id_)`
- `dtlms_wf_re_procdef.idx_dtlms_wf_re_procdef_key`: `CREATE INDEX idx_dtlms_wf_re_procdef_key ON public.dtlms_wf_re_procdef USING btree (key_)`
- `dtlms_wf_ru_execution.dtlms_wf_ru_execution_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_execution_pkey ON public.dtlms_wf_ru_execution USING btree (id_)`
- `dtlms_wf_ru_execution.idx_dtlms_wf_ru_execution_proc_inst`: `CREATE INDEX idx_dtlms_wf_ru_execution_proc_inst ON public.dtlms_wf_ru_execution USING btree (proc_inst_id_)`
- `dtlms_wf_ru_identitylink.dtlms_wf_ru_identitylink_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_identitylink_pkey ON public.dtlms_wf_ru_identitylink USING btree (id_)`
- `dtlms_wf_ru_task.dtlms_wf_ru_task_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_task_pkey ON public.dtlms_wf_ru_task USING btree (id_)`
- `dtlms_wf_ru_task.idx_dtlms_wf_ru_task_business_key`: `CREATE INDEX idx_dtlms_wf_ru_task_business_key ON public.dtlms_wf_ru_task USING btree (business_key_)`
- `dtlms_wf_ru_task.idx_dtlms_wf_ru_task_proc_inst`: `CREATE INDEX idx_dtlms_wf_ru_task_proc_inst ON public.dtlms_wf_ru_task USING btree (proc_inst_id_)`
- `dtlms_wf_ru_variable.dtlms_wf_ru_variable_pkey`: `CREATE UNIQUE INDEX dtlms_wf_ru_variable_pkey ON public.dtlms_wf_ru_variable USING btree (id_)`
- `dtlms_written_exam_scores.dtlms_written_exam_scores_pkey`: `CREATE UNIQUE INDEX dtlms_written_exam_scores_pkey ON public.dtlms_written_exam_scores USING btree (id)`

## 触发器（Triggers）


## 表级约束（Table Constraints）

- `dtlms_achievements.dtlms_achievements_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_achievements.dtlms_achievements_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_admission_decisions.dtlms_admission_decisions_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_admission_decisions.dtlms_admission_decisions_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_advisor_screening_batches.chk_advisor_screening_batches_round` (CHECK): `CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text])))`
- `dtlms_advisor_screening_batches.dtlms_advisor_screening_batches_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_advisor_screening_items.chk_advisor_screening_items_round` (CHECK): `CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text])))`
- `dtlms_advisor_screening_items.chk_advisor_screening_items_score_range` (CHECK): `CHECK (((advisor_score >= (0)::numeric) AND (advisor_score <= (100)::numeric)))`
- `dtlms_advisor_screening_items.dtlms_advisor_screening_items_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_advisor_screening_items.dtlms_advisor_screening_items_batch_id_fkey` (FOREIGN KEY): `FOREIGN KEY (batch_id) REFERENCES dtlms_advisor_screening_batches(id) ON DELETE CASCADE`
- `dtlms_advisor_screening_items.dtlms_advisor_screening_items_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_advisor_screening_items.uq_advisor_screening_items_application_round` (UNIQUE): `UNIQUE (application_id, screening_round)`
- `dtlms_advisor_screening_items.uq_advisor_screening_items_candidate_round` (UNIQUE): `UNIQUE (candidate_no, screening_round)`
- `dtlms_advisors.fk_dtlms_advisors_user_id` (FOREIGN KEY): `FOREIGN KEY (user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_advisors.dtlms_advisors_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_advisors.dtlms_advisors_advisor_no_key` (UNIQUE): `UNIQUE (advisor_no)`
- `dtlms_application_materials.dtlms_application_materials_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_application_materials.dtlms_application_materials_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_audit_policies.dtlms_audit_policies_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_background_assessments.dtlms_background_assessments_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_background_assessments.dtlms_background_assessments_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_background_assessments.dtlms_background_assessments_application_id_evaluator_usern_key` (UNIQUE): `UNIQUE (application_id, evaluator_username)`
- `dtlms_data_sync_logs.dtlms_data_sync_logs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_dict_data.dtlms_dict_data_status_check` (CHECK): `CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))`
- `dtlms_dict_data.dtlms_dict_data_dict_type_id_fkey` (FOREIGN KEY): `FOREIGN KEY (dict_type_id) REFERENCES dtlms_dict_types(id)`
- `dtlms_dict_data.dtlms_dict_data_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_dict_data.dtlms_dict_data_dict_type_value_key` (UNIQUE): `UNIQUE (dict_type, value)`
- `dtlms_dict_types.dtlms_dict_types_status_check` (CHECK): `CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))`
- `dtlms_dict_types.dtlms_dict_types_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_dict_types.dtlms_dict_types_dict_type_key` (UNIQUE): `UNIQUE (dict_type)`
- `dtlms_initial_screening_confirmations.chk_initial_screening_confirmations_result` (CHECK): `CHECK (((confirmation_result)::text = ANY (ARRAY[('passed'::character varying)::text, ('rejected'::character varying)::text])))`
- `dtlms_initial_screening_confirmations.dtlms_initial_screening_confirmations_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_initial_screening_confirmations.dtlms_initial_screening_confirmations_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_initial_screening_confirmations.uq_initial_screening_confirmations_application` (UNIQUE): `UNIQUE (application_id)`
- `dtlms_initial_screening_notifications.chk_initial_screening_notifications_channel` (CHECK): `CHECK (((notification_channel)::text = ANY (ARRAY[('email'::character varying)::text, ('site_message'::character varying)::text])))`
- `dtlms_initial_screening_notifications.chk_initial_screening_notifications_status` (CHECK): `CHECK (((notification_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('sent'::character varying)::text, ('failed'::character varying)::text])))`
- `dtlms_initial_screening_notifications.dtlms_initial_screening_notifications_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_initial_screening_notifications.dtlms_initial_screening_notifications_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_integrations.dtlms_integrations_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_interview_groups.dtlms_interview_groups_plan_id_fkey` (FOREIGN KEY): `FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id)`
- `dtlms_interview_groups.dtlms_interview_groups_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_interview_groups.dtlms_interview_groups_plan_id_group_code_key` (UNIQUE): `UNIQUE (plan_id, group_code)`
- `dtlms_interview_schedules.dtlms_interview_schedules_check` (CHECK): `CHECK ((ends_at >= starts_at))`
- `dtlms_interview_schedules.dtlms_interview_schedules_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_interview_schedules.dtlms_interview_schedules_interview_group_id_fkey` (FOREIGN KEY): `FOREIGN KEY (interview_group_id) REFERENCES dtlms_interview_groups(id)`
- `dtlms_interview_schedules.dtlms_interview_schedules_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_interview_schedules.dtlms_interview_schedules_admission_ticket_no_key` (UNIQUE): `UNIQUE (admission_ticket_no)`
- `dtlms_interview_scores.dtlms_interview_scores_schedule_id_fkey` (FOREIGN KEY): `FOREIGN KEY (schedule_id) REFERENCES dtlms_interview_schedules(id)`
- `dtlms_interview_scores.dtlms_interview_scores_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_login_logs.dtlms_login_logs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_material_scores.dtlms_material_scores_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_material_scores.dtlms_material_scores_reviewer_assignment_id_fkey` (FOREIGN KEY): `FOREIGN KEY (reviewer_assignment_id) REFERENCES dtlms_reviewer_assignments(id)`
- `dtlms_material_scores.dtlms_material_scores_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_news_articles.chk_dtlms_news_articles_status` (CHECK): `CHECK (((status)::text = ANY (ARRAY[('草稿'::character varying)::text, ('待发布'::character varying)::text, ('已发布'::character varying)::text, ('已下线'::character varying)::text])))`
- `dtlms_news_articles.chk_dtlms_news_articles_type` (CHECK): `CHECK (((news_type)::text = ANY (ARRAY[('学生门户通知消息'::character varying)::text, ('学生门户新闻信息'::character varying)::text])))`
- `dtlms_news_articles.dtlms_news_articles_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_news_articles.dtlms_news_articles_news_code_key` (UNIQUE): `UNIQUE (news_code)`
- `dtlms_notification_delivery_logs.dtlms_notification_delivery_logs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_notification_templates.dtlms_notification_templates_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_notification_templates.dtlms_notification_templates_template_code_key` (UNIQUE): `UNIQUE (template_code)`
- `dtlms_operation_logs.dtlms_operation_logs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_outbound_studies.dtlms_outbound_studies_check` (CHECK): `CHECK ((end_date >= start_date))`
- `dtlms_outbound_studies.dtlms_outbound_studies_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_outbound_studies.dtlms_outbound_studies_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_outbound_studies.dtlms_outbound_studies_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_permissions.dtlms_permissions_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_permissions.dtlms_permissions_permission_code_key` (UNIQUE): `UNIQUE (permission_code)`
- `dtlms_plan_offer.dtlms_plan_offer_accepted_check` (CHECK): `CHECK (((accepted IS NULL) OR ((accepted)::text = ANY (ARRAY[('declined'::character varying)::text, ('pending'::character varying)::text, ('accepted_pending_send'::character varying)::text, ('accepted_sent'::character varying)::text, ('accepted_confirmed'::character varying)::text, ('accepted_rejected'::character varying)::text]))))`
- `dtlms_plan_offer.dtlms_plan_offer_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_achievement_records.dtlms_portal_application_achievement_record_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_achievement_records.dtlms_portal_application_achievement_records_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_attachments.dtlms_portal_application_attachments_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_attachments.dtlms_portal_application_attachments_portal_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE`
- `dtlms_portal_application_attachments.dtlms_portal_application_attachments_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_declarations.dtlms_portal_application_declarations_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_declarations.dtlms_portal_application_declarations_pkey` (PRIMARY KEY): `PRIMARY KEY (application_id)`
- `dtlms_portal_application_education_experiences.chk_portal_application_education_sort_order` (CHECK): `CHECK ((sort_order > 0))`
- `dtlms_portal_application_education_experiences.dtlms_portal_application_education_experien_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_education_experiences.dtlms_portal_application_education_experiences_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_english_proficiencies.dtlms_portal_application_english_proficienc_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_english_proficiencies.dtlms_portal_application_english_proficiencies_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_family_members.dtlms_portal_application_family_members_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_family_members.dtlms_portal_application_family_members_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_personal_statements.dtlms_portal_application_personal_statement_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_personal_statements.dtlms_portal_application_personal_statements_pkey` (PRIMARY KEY): `PRIMARY KEY (application_id)`
- `dtlms_portal_application_practice_experiences.dtlms_portal_application_practice_experienc_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_practice_experiences.dtlms_portal_application_practice_experiences_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_preferences.chk_portal_application_preferences_order` (CHECK): `CHECK ((preference_order > 0))`
- `dtlms_portal_application_preferences.dtlms_portal_application_preferences_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE`
- `dtlms_portal_application_preferences.fk_dtlms_portal_application_preferences_advisor_user_id` (FOREIGN KEY): `FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_portal_application_preferences.dtlms_portal_application_preferences_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_application_preferences.uq_portal_application_preferences_order` (UNIQUE): `UNIQUE (application_id, preference_order)`
- `dtlms_portal_student_profiles.dtlms_portal_student_profiles_portal_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE`
- `dtlms_portal_student_profiles.dtlms_portal_student_profiles_pkey` (PRIMARY KEY): `PRIMARY KEY (portal_student_id)`
- `dtlms_portal_students.dtlms_portal_students_selected_plan_id_fkey` (FOREIGN KEY): `FOREIGN KEY (selected_plan_id) REFERENCES dtlms_recruitment_plans(id)`
- `dtlms_portal_students.fk_dtlms_portal_students_selected_advisor_user_id` (FOREIGN KEY): `FOREIGN KEY (selected_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_portal_students.fk_dtlms_portal_students_selected_team_id` (FOREIGN KEY): `FOREIGN KEY (selected_team_id) REFERENCES dtlms_teams(id) NOT VALID`
- `dtlms_portal_students.dtlms_portal_students_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_portal_students.dtlms_portal_students_email_key` (UNIQUE): `UNIQUE (email)`
- `dtlms_portal_students.dtlms_portal_students_id_number_key` (UNIQUE): `UNIQUE (id_number)`
- `dtlms_portal_students.dtlms_portal_students_phone_number_key` (UNIQUE): `UNIQUE (phone_number)`
- `dtlms_qualification_review_logs.dtlms_qualification_review_logs_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_qualification_review_logs.dtlms_qualification_review_logs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_qualification_reviews.dtlms_qualification_reviews_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_qualification_reviews.dtlms_qualification_reviews_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_intended_field_id_fkey` (FOREIGN KEY): `FOREIGN KEY (intended_field_id) REFERENCES dtlms_research_fields(id)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_plan_id_fkey` (FOREIGN KEY): `FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_portal_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id)`
- `dtlms_recruitment_applications.fk_dtlms_recruitment_applications_first_choice_id` (FOREIGN KEY): `FOREIGN KEY (first_choice_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_recruitment_applications.fk_dtlms_recruitment_applications_first_choice_team_id` (FOREIGN KEY): `FOREIGN KEY (first_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID`
- `dtlms_recruitment_applications.fk_dtlms_recruitment_applications_intended_advisor_user_id` (FOREIGN KEY): `FOREIGN KEY (intended_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_recruitment_applications.fk_dtlms_recruitment_applications_second_choice_id` (FOREIGN KEY): `FOREIGN KEY (second_choice_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_recruitment_applications.fk_dtlms_recruitment_applications_second_choice_team_id` (FOREIGN KEY): `FOREIGN KEY (second_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_recruitment_applications.dtlms_recruitment_applications_candidate_no_key` (UNIQUE): `UNIQUE (candidate_no)`
- `dtlms_recruitment_plans.dtlms_recruitment_plans_check` (CHECK): `CHECK ((end_date >= start_date))`
- `dtlms_recruitment_plans.dtlms_recruitment_plans_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_recruitment_plans.dtlms_recruitment_plans_plan_code_key` (UNIQUE): `UNIQUE (plan_code)`
- `dtlms_research_fields.dtlms_research_fields_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_research_fields.dtlms_research_fields_field_code_key` (UNIQUE): `UNIQUE (field_code)`
- `dtlms_research_projects.dtlms_research_projects_principal_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (principal_advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_research_projects.dtlms_research_projects_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_research_projects.dtlms_research_projects_project_code_key` (UNIQUE): `UNIQUE (project_code)`
- `dtlms_reviewer_assignments.dtlms_reviewer_assignments_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_reviewer_assignments.dtlms_reviewer_assignments_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_role_permissions.dtlms_role_permissions_permission_id_fkey` (FOREIGN KEY): `FOREIGN KEY (permission_id) REFERENCES dtlms_permissions(id)`
- `dtlms_role_permissions.dtlms_role_permissions_role_id_fkey` (FOREIGN KEY): `FOREIGN KEY (role_id) REFERENCES dtlms_roles(id)`
- `dtlms_role_permissions.dtlms_role_permissions_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_role_permissions.dtlms_role_permissions_role_id_permission_id_key` (UNIQUE): `UNIQUE (role_id, permission_id)`
- `dtlms_roles.dtlms_roles_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_roles.dtlms_roles_role_code_key` (UNIQUE): `UNIQUE (role_code)`
- `dtlms_schema_migrations.dtlms_schema_migrations_pkey` (PRIMARY KEY): `PRIMARY KEY (file_name)`
- `dtlms_scientific_reports.dtlms_scientific_reports_report_status_check` (CHECK): `CHECK (((report_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('submitted'::character varying)::text, ('reviewing'::character varying)::text, ('reviewed'::character varying)::text, ('rework'::character varying)::text])))`
- `dtlms_scientific_reports.dtlms_scientific_reports_reviewer_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (reviewer_advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_scientific_reports.dtlms_scientific_reports_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_scientific_reports.dtlms_scientific_reports_training_plan_id_fkey` (FOREIGN KEY): `FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id)`
- `dtlms_scientific_reports.dtlms_scientific_reports_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_student_advisor_history.dtlms_student_advisor_history_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_student_advisor_history.dtlms_student_advisor_history_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_student_advisor_history.dtlms_student_advisor_history_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_student_team_history.dtlms_student_team_history_check` (CHECK): `CHECK (((end_date IS NULL) OR (end_date >= start_date)))`
- `dtlms_student_team_history.dtlms_student_team_history_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_student_team_history.dtlms_student_team_history_team_id_fkey` (FOREIGN KEY): `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)`
- `dtlms_student_team_history.dtlms_student_team_history_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_students.dtlms_students_primary_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (primary_advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_students.dtlms_students_team_id_fkey` (FOREIGN KEY): `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)`
- `dtlms_students.fk_dtlms_students_portal_student_id` (FOREIGN KEY): `FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) NOT VALID`
- `dtlms_students.dtlms_students_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_students.dtlms_students_student_no_key` (UNIQUE): `UNIQUE (student_no)`
- `dtlms_system_configs.dtlms_system_configs_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_system_configs.dtlms_system_configs_config_key_key` (UNIQUE): `UNIQUE (config_key)`
- `dtlms_team_advisors.dtlms_team_advisors_team_id_fkey` (FOREIGN KEY): `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)`
- `dtlms_team_advisors.fk_dtlms_team_advisors_advisor_user_id` (FOREIGN KEY): `FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_team_advisors.dtlms_team_advisors_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_team_leaders.fk_dtlms_team_leaders_team_id` (FOREIGN KEY): `FOREIGN KEY (team_id) REFERENCES dtlms_teams(id)`
- `dtlms_team_leaders.fk_dtlms_team_leaders_user_id` (FOREIGN KEY): `FOREIGN KEY (user_id) REFERENCES dtlms_users(id)`
- `dtlms_team_leaders.dtlms_team_leaders_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_team_leaders.dtlms_team_leaders_team_id_user_id_key` (UNIQUE): `UNIQUE (team_id, user_id)`
- `dtlms_teams.dtlms_teams_team_status_check` (CHECK): `CHECK (((team_status)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text, ('planning'::character varying)::text, ('archived'::character varying)::text])))`
- `dtlms_teams.fk_dtlms_teams_lead_user_id` (FOREIGN KEY): `FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID`
- `dtlms_teams.dtlms_teams_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_teams.dtlms_teams_team_code_key` (UNIQUE): `UNIQUE (team_code)`
- `dtlms_teams.dtlms_teams_team_name_key` (UNIQUE): `UNIQUE (team_name)`
- `dtlms_theses.dtlms_theses_plagiarism_rate_check` (CHECK): `CHECK (((plagiarism_rate IS NULL) OR (plagiarism_rate <= (100)::numeric)))`
- `dtlms_theses.dtlms_theses_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_theses.dtlms_theses_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_theses.dtlms_theses_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_thesis_reviews.dtlms_thesis_reviews_thesis_id_fkey` (FOREIGN KEY): `FOREIGN KEY (thesis_id) REFERENCES dtlms_theses(id)`
- `dtlms_thesis_reviews.dtlms_thesis_reviews_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_training_plan_versions.dtlms_training_plan_versions_training_plan_id_fkey` (FOREIGN KEY): `FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id)`
- `dtlms_training_plan_versions.dtlms_training_plan_versions_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_training_plans.dtlms_training_plans_plan_status_check` (CHECK): `CHECK (((plan_status)::text = ANY (ARRAY[('draft'::character varying)::text, ('pending_confirm'::character varying)::text, ('effective'::character varying)::text, ('archived'::character varying)::text])))`
- `dtlms_training_plans.dtlms_training_plans_version_no_check` (CHECK): `CHECK (((version_no)::text <> ''::text))`
- `dtlms_training_plans.dtlms_training_plans_advisor_id_fkey` (FOREIGN KEY): `FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id)`
- `dtlms_training_plans.dtlms_training_plans_student_id_fkey` (FOREIGN KEY): `FOREIGN KEY (student_id) REFERENCES dtlms_students(id)`
- `dtlms_training_plans.dtlms_training_plans_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_user_profiles.dtlms_user_profiles_username_fkey` (FOREIGN KEY): `FOREIGN KEY (username) REFERENCES dtlms_users(username) ON UPDATE CASCADE ON DELETE CASCADE`
- `dtlms_user_profiles.dtlms_user_profiles_pkey` (PRIMARY KEY): `PRIMARY KEY (username)`
- `dtlms_user_roles.dtlms_user_roles_role_id_fkey` (FOREIGN KEY): `FOREIGN KEY (role_id) REFERENCES dtlms_roles(id)`
- `dtlms_user_roles.dtlms_user_roles_user_id_fkey` (FOREIGN KEY): `FOREIGN KEY (user_id) REFERENCES dtlms_users(id)`
- `dtlms_user_roles.dtlms_user_roles_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_user_roles.dtlms_user_roles_user_id_role_id_key` (UNIQUE): `UNIQUE (user_id, role_id)`
- `dtlms_users.dtlms_users_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
- `dtlms_users.dtlms_users_username_key` (UNIQUE): `UNIQUE (username)`
- `dtlms_wf_de_model.dtlms_wf_de_model_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_hi_actinst.dtlms_wf_hi_actinst_proc_def_id__fkey` (FOREIGN KEY): `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)`
- `dtlms_wf_hi_actinst.dtlms_wf_hi_actinst_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_hi_procinst.dtlms_wf_hi_procinst_proc_def_id__fkey` (FOREIGN KEY): `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)`
- `dtlms_wf_hi_procinst.dtlms_wf_hi_procinst_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_hi_procinst.dtlms_wf_hi_procinst_proc_inst_id__key` (UNIQUE): `UNIQUE (proc_inst_id_)`
- `dtlms_wf_hi_taskinst.dtlms_wf_hi_taskinst_proc_def_id__fkey` (FOREIGN KEY): `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)`
- `dtlms_wf_hi_taskinst.dtlms_wf_hi_taskinst_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_hi_varinst.dtlms_wf_hi_varinst_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_re_deployment.dtlms_wf_re_deployment_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_re_procdef.dtlms_wf_re_procdef_deployment_id__fkey` (FOREIGN KEY): `FOREIGN KEY (deployment_id_) REFERENCES dtlms_wf_re_deployment(id_)`
- `dtlms_wf_re_procdef.dtlms_wf_re_procdef_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_ru_execution.dtlms_wf_ru_execution_proc_def_id__fkey` (FOREIGN KEY): `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)`
- `dtlms_wf_ru_execution.dtlms_wf_ru_execution_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_ru_identitylink.dtlms_wf_ru_identitylink_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_ru_task.dtlms_wf_ru_task_exec_id__fkey` (FOREIGN KEY): `FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_)`
- `dtlms_wf_ru_task.dtlms_wf_ru_task_proc_def_id__fkey` (FOREIGN KEY): `FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_)`
- `dtlms_wf_ru_task.dtlms_wf_ru_task_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_wf_ru_variable.dtlms_wf_ru_variable_exec_id__fkey` (FOREIGN KEY): `FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_)`
- `dtlms_wf_ru_variable.dtlms_wf_ru_variable_pkey` (PRIMARY KEY): `PRIMARY KEY (id_)`
- `dtlms_written_exam_scores.dtlms_written_exam_scores_application_id_fkey` (FOREIGN KEY): `FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id)`
- `dtlms_written_exam_scores.dtlms_written_exam_scores_pkey` (PRIMARY KEY): `PRIMARY KEY (id)`
