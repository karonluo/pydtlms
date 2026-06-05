# test25 schema (auto-generated)
## dtlms_wf_de_model
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| name_ | character varying | NO |  |
| key_ | character varying | NO |  |
| category_ | character varying | YES |  |
| version_ | integer | NO | 1 |
| model_type_ | integer | NO | 0 |
| description_ | text | YES |  |
| meta_info_ | jsonb | YES |  |
| created_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| last_updated_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| tenant_id_ | character varying | YES |  |
| deployment_id_ | character varying | YES |  |
| resource_name_ | character varying | YES |  |
| editor_source_value_ | text | YES |  |
| editor_source_extra_value_ | jsonb | YES |  |
**Primary key:** id_

## dtlms_wf_hi_actinst
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| proc_def_id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| exec_id_ | character varying | YES |  |
| act_id_ | character varying | NO |  |
| act_name_ | character varying | YES |  |
| act_type_ | character varying | NO |  |
| assignee_ | character varying | YES |  |
| start_time_ | timestamp with time zone | NO |  |
| end_time_ | timestamp with time zone | YES |  |
| duration_ms_ | bigint | YES |  |
| business_key_ | character varying | YES |  |
**Primary key:** id_
**Foreign keys:**
- proc_def_id_ -> dtlms_wf_re_procdef.id_

## dtlms_wf_hi_procinst
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| business_key_ | character varying | YES |  |
| proc_def_id_ | character varying | NO |  |
| start_time_ | timestamp with time zone | NO |  |
| end_time_ | timestamp with time zone | YES |  |
| duration_ms_ | bigint | YES |  |
| start_user_id_ | character varying | YES |  |
| end_act_id_ | character varying | YES |  |
| delete_reason_ | character varying | YES |  |
| start_act_id_ | character varying | YES |  |
| state_ | character varying | NO | 'ACTIVE'::character varying |
**Primary key:** id_
**Foreign keys:**
- proc_def_id_ -> dtlms_wf_re_procdef.id_

## dtlms_wf_hi_taskinst
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| task_def_key_ | character varying | YES |  |
| proc_def_id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| exec_id_ | character varying | YES |  |
| name_ | character varying | NO |  |
| business_key_ | character varying | YES |  |
| assignee_ | character varying | YES |  |
| owner_ | character varying | YES |  |
| start_time_ | timestamp with time zone | NO |  |
| claim_time_ | timestamp with time zone | YES |  |
| end_time_ | timestamp with time zone | YES |  |
| duration_ms_ | bigint | YES |  |
| due_date_ | timestamp with time zone | YES |  |
| delete_reason_ | character varying | YES |  |
| priority_ | integer | NO | 50 |
| category_ | character varying | YES |  |
**Primary key:** id_
**Foreign keys:**
- proc_def_id_ -> dtlms_wf_re_procdef.id_

## dtlms_wf_hi_varinst
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| exec_id_ | character varying | YES |  |
| task_id_ | character varying | YES |  |
| name_ | character varying | NO |  |
| var_type_ | character varying | NO |  |
| text_value_ | text | YES |  |
| number_value_ | bigint | YES |  |
| json_value_ | jsonb | YES |  |
| create_time_ | timestamp with time zone | NO |  |
| last_updated_time_ | timestamp with time zone | NO |  |
**Primary key:** id_

## dtlms_wf_re_deployment
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| name_ | character varying | NO |  |
| category_ | character varying | YES |  |
| key_ | character varying | YES |  |
| deploy_time_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| tenant_id_ | character varying | YES |  |
**Primary key:** id_

## dtlms_wf_re_procdef
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| key_ | character varying | NO |  |
| version_ | integer | NO | 1 |
| deployment_id_ | character varying | YES |  |
| resource_name_ | character varying | YES |  |
| diagram_resource_name_ | character varying | YES |  |
| name_ | character varying | NO |  |
| category_ | character varying | YES |  |
| description_ | text | YES |  |
| suspension_state_ | integer | NO | 1 |
| tenant_id_ | character varying | YES |  |
**Primary key:** id_
**Foreign keys:**
- deployment_id_ -> dtlms_wf_re_deployment.id_

## dtlms_wf_ru_execution
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| proc_def_id_ | character varying | NO |  |
| business_key_ | character varying | YES |  |
| parent_id_ | character varying | YES |  |
| act_id_ | character varying | YES |  |
| is_active_ | boolean | NO | true |
| is_concurrent_ | boolean | NO | false |
| is_scope_ | boolean | NO | true |
| start_time_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| start_user_id_ | character varying | YES |  |
| super_exec_ | character varying | YES |  |
| tenant_id_ | character varying | YES |  |
**Primary key:** id_
**Foreign keys:**
- proc_def_id_ -> dtlms_wf_re_procdef.id_

## dtlms_wf_ru_identitylink
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | bigint | NO | nextval('dtlms_wf_ru_identitylink_id__seq'::regclass) |
| task_id_ | character varying | NO |  |
| proc_inst_id_ | character varying | YES |  |
| user_id_ | character varying | YES |  |
| group_id_ | character varying | YES |  |
| link_type_ | character varying | NO |  |
| created_at_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id_

## dtlms_wf_ru_task
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| exec_id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| proc_def_id_ | character varying | NO |  |
| task_def_key_ | character varying | YES |  |
| name_ | character varying | NO |  |
| business_key_ | character varying | YES |  |
| assignee_ | character varying | YES |  |
| owner_ | character varying | YES |  |
| create_time_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| due_date_ | timestamp with time zone | YES |  |
| claim_time_ | timestamp with time zone | YES |  |
| priority_ | integer | NO | 50 |
| suspension_state_ | integer | NO | 1 |
| tenant_id_ | character varying | YES |  |
| form_key_ | character varying | YES |  |
| description_ | text | YES |  |
**Primary key:** id_
**Foreign keys:**
- exec_id_ -> dtlms_wf_ru_execution.id_
- proc_def_id_ -> dtlms_wf_re_procdef.id_

## dtlms_wf_ru_variable
| Column | Type | Nullable | Default |
|---|---|---|---|
| id_ | character varying | NO |  |
| exec_id_ | character varying | NO |  |
| proc_inst_id_ | character varying | NO |  |
| task_id_ | character varying | YES |  |
| name_ | character varying | NO |  |
| var_type_ | character varying | NO |  |
| text_value_ | text | YES |  |
| number_value_ | bigint | YES |  |
| json_value_ | jsonb | YES |  |
| create_time_ | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id_
**Foreign keys:**
- exec_id_ -> dtlms_wf_ru_execution.id_

## dtlms_written_exam_scores
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_written_exam_scores_id_seq'::regclass) |
| application_id | bigint | NO |  |
| exam_date | date | YES |  |
| exam_score | numeric | YES |  |
| import_batch_no | character varying | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id
