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

## dtlms_interview_schedules
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_interview_schedules_id_seq'::regclass) |
| application_id | bigint | NO |  |
| interview_group_id | bigint | NO |  |
| admission_ticket_no | character varying | NO |  |
| starts_at | timestamp with time zone | NO |  |
| ends_at | timestamp with time zone | NO |  |
| schedule_status | character varying | NO | 'scheduled'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_interview_schedules_application_id_fkey)
- interview_group_id -> dtlms_interview_groups.id  (dtlms_interview_schedules_interview_group_id_fkey)

## dtlms_interview_scores
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_interview_scores_id_seq'::regclass) |
| schedule_id | bigint | NO |  |
| evaluator_username | character varying | NO |  |
| single_choice_score | numeric | YES |  |
| fill_blank_score | numeric | YES |  |
| coding_score | numeric | YES |  |
| interview_score | numeric | YES |  |
| ideological_score | numeric | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- schedule_id -> dtlms_interview_schedules.id  (dtlms_interview_scores_schedule_id_fkey)

## dtlms_login_logs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_login_logs_id_seq'::regclass) |
| username | character varying | NO |  |
| login_status | character varying | NO |  |
| login_ip | character varying | YES |  |
| user_agent | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_material_scores
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_material_scores_id_seq'::regclass) |
| application_id | bigint | NO |  |
| reviewer_assignment_id | bigint | NO |  |
| material_score | numeric | YES |  |
| recommendation_text | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_material_scores_application_id_fkey)
- reviewer_assignment_id -> dtlms_reviewer_assignments.id  (dtlms_material_scores_reviewer_assignment_id_fkey)

## dtlms_news_articles
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_news_articles_id_seq'::regclass) |
| news_code | character varying | NO |  |
| news_title | character varying | NO |  |
| news_content | text | NO |  |
| news_type | character varying | NO |  |
| publisher_user_id | bigint | YES |  |
| publisher_username | character varying | YES |  |
| publisher_name | character varying | YES |  |
| reviewer_user_id | bigint | YES |  |
| reviewer_username | character varying | YES |  |
| reviewer_name | character varying | YES |  |
| published_at | timestamp with time zone | YES |  |
| status | character varying | NO | '草稿'::character varying |
| is_pinned | boolean | NO | false |
| display_order | integer | NO | 0 |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_notification_delivery_logs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_notification_delivery_logs_id_seq'::regclass) |
| channel | character varying | NO |  |
| template_code | character varying | YES |  |
| recipient | character varying | NO |  |
| subject | character varying | NO |  |
| send_status | character varying | NO |  |
| failure_reason | text | YES |  |
| business_key | character varying | YES |  |
| triggered_by | character varying | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_notification_templates
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_notification_templates_id_seq'::regclass) |
| template_code | character varying | NO |  |
| channel | character varying | NO |  |
| title | character varying | NO |  |
| content_template | text | NO |  |
| variables_schema | jsonb | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_operation_logs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_operation_logs_id_seq'::regclass) |
| operator_username | character varying | NO |  |
| operator_role | character varying | NO |  |
| module_name | character varying | NO |  |
| entity_name | character varying | NO |  |
| entity_id | character varying | NO |  |
| action | character varying | NO |  |
| old_value | jsonb | YES |  |
| new_value | jsonb | YES |  |
| request_ip | character varying | YES |  |
| result | character varying | NO | 'success'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_outbound_studies
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_outbound_studies_id_seq'::regclass) |
| student_id | bigint | NO |  |
| advisor_id | bigint | NO |  |
| study_type | character varying | NO |  |
| destination | character varying | NO |  |
| start_date | date | NO |  |
| end_date | date | NO |  |
| approval_status | character varying | NO | 'submitted'::character varying |
| expected_outcome | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| business_key | character varying | NO |  |
**Primary key:** id
**Foreign keys:**
- advisor_id -> dtlms_advisors.id  (dtlms_outbound_studies_advisor_id_fkey)
- student_id -> dtlms_students.id  (dtlms_outbound_studies_student_id_fkey)

## dtlms_permissions
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_permissions_id_seq'::regclass) |
| permission_code | character varying | NO |  |
| permission_name | character varying | NO |  |
| module_name | character varying | NO |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_portal_application_achievement_records
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_achievement_records_id_seq'::regclass) |
| application_id | bigint | NO |  |
| achievement_type | character varying | NO |  |
| paper_title | character varying | YES |  |
| author_order | character varying | YES |  |
| journal_or_conference | character varying | YES |  |
| publish_or_index_month | character varying | YES |  |
| award_name | character varying | YES |  |
| awarding_organization | character varying | YES |  |
| award_level | character varying | YES |  |
| award_year | character varying | YES |  |
| responsibility_text | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| achievement_month | character varying | YES |  |
| award_rank | character varying | YES |  |
| award_certificate_attachment_url | character varying | YES |  |
| description_text | text | YES |  |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_achievement_record_application_id_fkey)

## dtlms_portal_application_attachments
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_attachments_id_seq'::regclass) |
| portal_student_id | bigint | YES |  |
| application_id | bigint | YES |  |
| owner_type | character varying | NO |  |
| owner_id | bigint | YES |  |
| attachment_category | character varying | NO |  |
| file_name | character varying | NO |  |
| file_url | text | NO |  |
| file_type | character varying | YES |  |
| file_size | bigint | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_attachments_application_id_fkey)
- portal_student_id -> dtlms_portal_students.id  (dtlms_portal_application_attachments_portal_student_id_fkey)

## dtlms_portal_application_declarations
| Column | Type | Nullable | Default |
|---|---|---|---|
| application_id | bigint | NO |  |
| has_read_declaration | boolean | NO | false |
| declaration_text | text | YES |  |
| progress_snapshot | jsonb | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** application_id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_declarations_application_id_fkey)

## dtlms_portal_application_education_experiences
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_education_experiences_id_seq'::regclass) |
| application_id | bigint | NO |  |
| sort_order | integer | NO | 1 |
| education_stage | character varying | NO |  |
| start_month | character varying | YES |  |
| end_month | character varying | YES |  |
| school_name | character varying | NO |  |
| major_name | character varying | YES |  |
| average_score | character varying | YES |  |
| gpa | character varying | YES |  |
| ranking | character varying | YES |  |
| verifier_name | character varying | YES |  |
| verifier_phone | character varying | YES |  |
| transcript_attachment_url | text | YES |  |
| degree_certificate_attachment_url | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| graduation_certificate_attachment_url | text | YES |  |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_education_experien_application_id_fkey)

## dtlms_portal_application_english_proficiencies
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_english_proficiencies_id_seq'::regclass) |
| application_id | bigint | NO |  |
| exam_name | character varying | NO |  |
| score_text | character varying | NO |  |
| certificate_attachment_url | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_english_proficienc_application_id_fkey)

## dtlms_portal_application_family_members
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_family_members_id_seq'::regclass) |
| application_id | bigint | NO |  |
| member_name | character varying | NO |  |
| relation_type | character varying | NO |  |
| employer_name | character varying | YES |  |
| job_title | character varying | YES |  |
| contact_phone | character varying | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_family_members_application_id_fkey)

## dtlms_portal_application_personal_statements
| Column | Type | Nullable | Default |
|---|---|---|---|
| application_id | bigint | NO |  |
| personal_statement_text | text | YES |  |
| ai_problem_statement | text | YES |  |
| ai_industry_opinion | text | YES |  |
| resume_attachment_url | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| growth_experience_text | text | YES |  |
| program_application_reason_text | text | YES |  |
| career_plan_text | text | YES |  |
| supporting_material_attachment_url | text | YES |  |
**Primary key:** application_id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_personal_statement_application_id_fkey)

## dtlms_portal_application_practice_experiences
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_practice_experiences_id_seq'::regclass) |
| application_id | bigint | NO |  |
| start_month | character varying | YES |  |
| end_month | character varying | YES |  |
| organization_name | character varying | NO |  |
| position_name | character varying | YES |  |
| responsibility_text | text | YES |  |
| verifier_name | character varying | YES |  |
| verifier_phone | character varying | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_practice_experienc_application_id_fkey)

## dtlms_portal_application_preferences
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_application_preferences_id_seq'::regclass) |
| application_id | bigint | NO |  |
| preference_order | integer | NO |  |
| research_center_name | character varying | YES |  |
| advisor_name | character varying | YES |  |
| is_optional | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| team_id | bigint | YES |  |
| advisor_user_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_portal_application_preferences_application_id_fkey)
- advisor_user_id -> dtlms_users.id  (fk_dtlms_portal_application_preferences_advisor_user_id)
- team_id -> dtlms_teams.id  (fk_dtlms_portal_application_preferences_team_id)

## dtlms_portal_student_profiles
| Column | Type | Nullable | Default |
|---|---|---|---|
| portal_student_id | bigint | NO |  |
| full_name_pinyin | character varying | YES |  |
| gender | character varying | YES |  |
| birth_date | character varying | YES |  |
| ethnic_group | character varying | YES |  |
| native_place | character varying | YES |  |
| political_status | character varying | YES |  |
| marital_status | character varying | YES |  |
| religious_belief | character varying | YES |  |
| id_type | character varying | YES |  |
| mailing_address | text | YES |  |
| emergency_contact_name | character varying | YES |  |
| emergency_contact_phone | character varying | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| profile_photo_url | character varying | YES |  |
| id_card_collage_url | character varying | YES |  |
**Primary key:** portal_student_id
**Foreign keys:**
- portal_student_id -> dtlms_portal_students.id  (dtlms_portal_student_profiles_portal_student_id_fkey)

## dtlms_portal_students
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_portal_students_id_seq'::regclass) |
| full_name | character varying | NO |  |
| phone_number | character varying | NO |  |
| email | character varying | NO |  |
| id_number | character varying | NO |  |
| graduation_school | character varying | YES |  |
| highest_degree | character varying | YES |  |
| intended_field | character varying | YES |  |
| political_status | character varying | YES |  |
| selected_plan_id | bigint | YES |  |
| selected_team_name | character varying | YES |  |
| selected_advisor_name | character varying | YES |  |
| self_evaluation | text | YES |  |
| submitted_at | timestamp with time zone | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| password_hash | character varying | YES |  |
| gender | character varying | YES |  |
| birth_date | character varying | YES |  |
| ethnic_group | character varying | YES |  |
| native_place | character varying | YES |  |
| marital_status | character varying | YES |  |
| religious_belief | character varying | YES |  |
| id_type | character varying | YES |  |
| mailing_address | text | YES |  |
| english_level | character varying | YES |  |
| family_info | text | YES |  |
| education_experience | text | YES |  |
| practice_experience | text | YES |  |
| personal_profile | text | YES |  |
| recommendation_notes | text | YES |  |
| personal_statement_text | text | YES |  |
| signed_agreement | boolean | NO | false |
| account_status | character varying | NO | '启用'::character varying |
| application_draft | jsonb | YES |  |
| selected_team_id | bigint | YES |  |
| selected_advisor_user_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- selected_plan_id -> dtlms_recruitment_plans.id  (dtlms_portal_students_selected_plan_id_fkey)
- selected_advisor_user_id -> dtlms_users.id  (fk_dtlms_portal_students_selected_advisor_user_id)
- selected_team_id -> dtlms_teams.id  (fk_dtlms_portal_students_selected_team_id)

## dtlms_qualification_review_logs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_qualification_review_logs_id_seq'::regclass) |
| application_id | bigint | NO |  |
| reviewer_user_id | bigint | YES |  |
| reviewer_username | character varying | NO |  |
| reviewer_name | character varying | YES |  |
| reviewer_role_code | character varying | YES |  |
| action | character varying | NO |  |
| action_label | character varying | NO |  |
| review_comment | text | YES |  |
| reviewed_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_qualification_review_logs_application_id_fkey)

## dtlms_qualification_reviews
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_qualification_reviews_id_seq'::regclass) |
| application_id | bigint | NO |  |
| reviewer_username | character varying | NO |  |
| review_status | character varying | NO | 'pending'::character varying |
| review_comment | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_qualification_reviews_application_id_fkey)

## dtlms_recruitment_applications
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_recruitment_applications_id_seq'::regclass) |
| plan_id | bigint | NO |  |
| student_name | character varying | NO |  |
| candidate_no | character varying | NO |  |
| gender | character varying | NO |  |
| graduation_school | character varying | YES |  |
| highest_degree | character varying | YES |  |
| intended_field_id | bigint | YES |  |
| application_status | character varying | NO | 'submitted'::character varying |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| business_key | character varying | NO |  |
| review_round | character varying | YES |  |
| first_choice | character varying | YES |  |
| second_choice | character varying | YES |  |
| political_status | character varying | YES |  |
| marital_status | character varying | YES |  |
| religious_belief | character varying | YES |  |
| native_place | character varying | YES |  |
| phone_number | character varying | YES |  |
| email | character varying | YES |  |
| mailing_address | text | YES |  |
| id_type | character varying | YES |  |
| id_number | character varying | YES |  |
| undergraduate_school | character varying | YES |  |
| accept_adjustment | character varying | YES |  |
| undergraduate_average_score | character varying | YES |  |
| undergraduate_gpa | character varying | YES |  |
| undergraduate_rank | character varying | YES |  |
| undergraduate_major | character varying | YES |  |
| graduate_average_score | character varying | YES |  |
| graduate_gpa | character varying | YES |  |
| graduate_rank | character varying | YES |  |
| graduate_major | character varying | YES |  |
| intended_advisor_name | character varying | YES |  |
| discovery_channel | text | YES |  |
| graduate_school | character varying | YES |  |
| overseas_university_name | character varying | YES |  |
| overseas_master_university_name | character varying | YES |  |
| self_evaluation | text | YES |  |
| applied_at | timestamp with time zone | YES |  |
| research_problem | text | YES |  |
| research_status_analysis | text | YES |  |
| research_impact | text | YES |  |
| ai_society_impact | text | YES |  |
| dissenting_view | text | YES |  |
| family_info | text | YES |  |
| education_experience | text | YES |  |
| practice_experience | text | YES |  |
| personal_statement_text | text | YES |  |
| student_activity_experience | text | YES |  |
| personal_statement_attachment | text | YES |  |
| material_list_attachment | text | YES |  |
| supplementary_profile | text | YES |  |
| portal_student_id | bigint | YES |  |
| source_channel | character varying | YES |  |
| source_channel_other | character varying | YES |  |
| first_choice_team_id | bigint | YES |  |
| second_choice_team_id | bigint | YES |  |
| intended_advisor_user_id | bigint | YES |  |
| advisor_screening_status | character varying | YES | 'pending'::character varying |
| advisor_screening_round | character varying | YES | 'first_choice'::character varying |
| first_choice_screening_batch_id | bigint | YES |  |
| second_choice_screening_batch_id | bigint | YES |  |
| first_choice_screening_submitted_at | timestamp with time zone | YES |  |
| second_choice_screening_submitted_at | timestamp with time zone | YES |  |
| first_choice_screening_score | numeric | YES |  |
| second_choice_screening_score | numeric | YES |  |
| initial_screening_status | character varying | YES | 'pending'::character varying |
| initial_screening_result | character varying | YES |  |
| initial_screening_confirmed_at | timestamp with time zone | YES |  |
| initial_screening_confirmer_username | character varying | YES |  |
| initial_screening_confirmer_name | character varying | YES |  |
| initial_screening_notification_status | character varying | YES | 'pending'::character varying |
| initial_screening_notification_sent_at | timestamp with time zone | YES |  |
| next_stage_name | character varying | YES |  |
**Primary key:** id
**Foreign keys:**
- intended_field_id -> dtlms_research_fields.id  (dtlms_recruitment_applications_intended_field_id_fkey)
- plan_id -> dtlms_recruitment_plans.id  (dtlms_recruitment_applications_plan_id_fkey)
- portal_student_id -> dtlms_portal_students.id  (dtlms_recruitment_applications_portal_student_id_fkey)
- first_choice_team_id -> dtlms_teams.id  (fk_dtlms_recruitment_applications_first_choice_team_id)
- intended_advisor_user_id -> dtlms_users.id  (fk_dtlms_recruitment_applications_intended_advisor_user_id)
- second_choice_team_id -> dtlms_teams.id  (fk_dtlms_recruitment_applications_second_choice_team_id)

## dtlms_recruitment_plans
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_recruitment_plans_id_seq'::regclass) |
| plan_code | character varying | NO |  |
| plan_name | character varying | NO |  |
| academic_year | character varying | NO |  |
| semester | character varying | NO |  |
| start_date | timestamp with time zone | NO |  |
| end_date | timestamp with time zone | NO |  |
| target_quota | integer | NO | 0 |
| plan_status | character varying | NO | 'draft'::character varying |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| brochure_image_url | character varying | YES |  |
| plan_description | text | YES |  |
**Primary key:** id

## dtlms_research_fields
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_research_fields_id_seq'::regclass) |
| field_code | character varying | NO |  |
| field_name | character varying | NO |  |
| description | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_research_projects
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_research_projects_id_seq'::regclass) |
| project_code | character varying | NO |  |
| project_name | character varying | NO |  |
| principal_advisor_id | bigint | YES |  |
| funding_amount | numeric | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- principal_advisor_id -> dtlms_advisors.id  (dtlms_research_projects_principal_advisor_id_fkey)

## dtlms_reviewer_assignments
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_reviewer_assignments_id_seq'::regclass) |
| application_id | bigint | NO |  |
| reviewer_username | character varying | NO |  |
| reviewer_role | character varying | NO |  |
| assignment_status | character varying | NO | 'assigned'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- application_id -> dtlms_recruitment_applications.id  (dtlms_reviewer_assignments_application_id_fkey)

## dtlms_role_permissions
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_role_permissions_id_seq'::regclass) |
| role_id | bigint | NO |  |
| permission_id | bigint | NO |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- permission_id -> dtlms_permissions.id  (dtlms_role_permissions_permission_id_fkey)
- role_id -> dtlms_roles.id  (dtlms_role_permissions_role_id_fkey)

## dtlms_roles
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_roles_id_seq'::regclass) |
| role_code | character varying | NO |  |
| role_name | character varying | NO |  |
| description | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| scope_name | character varying | NO | '系统管理'::character varying |
**Primary key:** id

## dtlms_schema_migrations
| Column | Type | Nullable | Default |
|---|---|---|---|
| file_name | character varying | NO |  |
| applied_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** file_name

## dtlms_scientific_reports
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_scientific_reports_id_seq'::regclass) |
| student_id | bigint | NO |  |
| training_plan_id | bigint | NO |  |
| period_label | character varying | NO |  |
| report_status | character varying | NO | 'pending'::character varying |
| summary | text | NO |  |
| attachment_url | character varying | YES |  |
| reviewer_advisor_id | bigint | YES |  |
| review_score | numeric | YES |  |
| review_comment | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| business_key | character varying | NO |  |
**Primary key:** id
**Foreign keys:**
- reviewer_advisor_id -> dtlms_advisors.id  (dtlms_scientific_reports_reviewer_advisor_id_fkey)
- student_id -> dtlms_students.id  (dtlms_scientific_reports_student_id_fkey)
- training_plan_id -> dtlms_training_plans.id  (dtlms_scientific_reports_training_plan_id_fkey)

## dtlms_student_advisor_history
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_student_advisor_history_id_seq'::regclass) |
| student_id | bigint | NO |  |
| advisor_id | bigint | NO |  |
| relation_type | character varying | NO | 'primary'::character varying |
| start_date | date | NO |  |
| end_date | date | YES |  |
| change_reason | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- advisor_id -> dtlms_advisors.id  (dtlms_student_advisor_history_advisor_id_fkey)
- student_id -> dtlms_students.id  (dtlms_student_advisor_history_student_id_fkey)

## dtlms_student_team_history
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_student_team_history_id_seq'::regclass) |
| student_id | bigint | NO |  |
| team_id | bigint | NO |  |
| start_date | date | NO |  |
| end_date | date | YES |  |
| change_reason | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- student_id -> dtlms_students.id  (dtlms_student_team_history_student_id_fkey)
- team_id -> dtlms_teams.id  (dtlms_student_team_history_team_id_fkey)

## dtlms_students
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_students_id_seq'::regclass) |
| student_no | character varying | NO |  |
| full_name | character varying | NO |  |
| gender | character varying | NO |  |
| political_status | character varying | YES |  |
| phone_number | character varying | YES |  |
| identity_no | character varying | YES |  |
| enrollment_year | integer | NO |  |
| degree_type | character varying | NO |  |
| team_name | character varying | YES |  |
| current_status | character varying | NO | 'enrolled'::character varying |
| primary_advisor_id | bigint | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| team_id | bigint | YES |  |
| portal_student_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- primary_advisor_id -> dtlms_advisors.id  (dtlms_students_primary_advisor_id_fkey)
- team_id -> dtlms_teams.id  (dtlms_students_team_id_fkey)
- portal_student_id -> dtlms_portal_students.id  (fk_dtlms_students_portal_student_id)

## dtlms_system_configs
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_system_configs_id_seq'::regclass) |
| config_key | character varying | NO |  |
| config_value | text | NO |  |
| description | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id

## dtlms_team_advisors
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_team_advisors_id_seq'::regclass) |
| team_id | bigint | NO |  |
| advisor_id | bigint | NO |  |
| advisor_role | character varying | NO | 'member'::character varying |
| joined_on | date | YES |  |
| left_on | date | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| advisor_user_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- advisor_id -> dtlms_advisors.id  (dtlms_team_advisors_advisor_id_fkey)
- team_id -> dtlms_teams.id  (dtlms_team_advisors_team_id_fkey)
- advisor_user_id -> dtlms_users.id  (fk_dtlms_team_advisors_advisor_user_id)

## dtlms_teams
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_teams_id_seq'::regclass) |
| team_code | character varying | NO |  |
| team_name | character varying | NO |  |
| department_name | character varying | NO |  |
| discipline_name | character varying | YES |  |
| lead_advisor_id | bigint | YES |  |
| research_directions | text | YES |  |
| team_status | character varying | NO | 'active'::character varying |
| established_on | date | YES |  |
| description | text | YES |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| lead_user_id | bigint | YES |  |
**Primary key:** id
**Foreign keys:**
- lead_advisor_id -> dtlms_advisors.id  (dtlms_teams_lead_advisor_id_fkey)
- lead_user_id -> dtlms_users.id  (fk_dtlms_teams_lead_user_id)

## dtlms_theses
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_theses_id_seq'::regclass) |
| student_id | bigint | NO |  |
| advisor_id | bigint | NO |  |
| title | character varying | NO |  |
| plagiarism_rate | numeric | YES |  |
| thesis_status | character varying | NO | 'draft'::character varying |
| blind_review_status | character varying | NO | 'pending'::character varying |
| defense_date | date | YES |  |
| degree_granted | character varying | NO | 'pending'::character varying |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| business_key | character varying | NO |  |
**Primary key:** id
**Foreign keys:**
- advisor_id -> dtlms_advisors.id  (dtlms_theses_advisor_id_fkey)
- student_id -> dtlms_students.id  (dtlms_theses_student_id_fkey)

## dtlms_thesis_reviews
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_thesis_reviews_id_seq'::regclass) |
| thesis_id | bigint | NO |  |
| expert_name | character varying | NO |  |
| review_score | numeric | YES |  |
| review_status | character varying | NO | 'pending'::character varying |
| review_comment | text | YES |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- thesis_id -> dtlms_theses.id  (dtlms_thesis_reviews_thesis_id_fkey)

## dtlms_training_plan_versions
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_training_plan_versions_id_seq'::regclass) |
| training_plan_id | bigint | NO |  |
| version_no | character varying | NO |  |
| change_reason | text | YES |  |
| plan_snapshot | text | NO |  |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- training_plan_id -> dtlms_training_plans.id  (dtlms_training_plan_versions_training_plan_id_fkey)

## dtlms_training_plans
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_training_plans_id_seq'::regclass) |
| student_id | bigint | NO |  |
| advisor_id | bigint | NO |  |
| version_no | character varying | NO | 'v1.0'::character varying |
| report_cycle | character varying | NO |  |
| plan_status | character varying | NO | 'draft'::character varying |
| scientific_goal | text | NO |  |
| assessment_rule | text | NO |  |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- advisor_id -> dtlms_advisors.id  (dtlms_training_plans_advisor_id_fkey)
- student_id -> dtlms_students.id  (dtlms_training_plans_student_id_fkey)

## dtlms_user_profiles
| Column | Type | Nullable | Default |
|---|---|---|---|
| username | character varying | NO |  |
| full_name | character varying | NO |  |
| role_name | character varying | NO |  |
| department_name | character varying | NO |  |
| phone_number | character varying | YES |  |
| email | character varying | YES |  |
| theme_color | character varying | NO | '#0f4cbd'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| introduction | text | YES |  |
**Primary key:** username
**Foreign keys:**
- username -> dtlms_users.username  (dtlms_user_profiles_username_fkey)

## dtlms_user_roles
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_user_roles_id_seq'::regclass) |
| user_id | bigint | NO |  |
| role_id | bigint | NO |  |
| grant_source | character varying | NO | 'bootstrap'::character varying |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
**Primary key:** id
**Foreign keys:**
- role_id -> dtlms_roles.id  (dtlms_user_roles_role_id_fkey)
- user_id -> dtlms_users.id  (dtlms_user_roles_user_id_fkey)

## dtlms_users
| Column | Type | Nullable | Default |
|---|---|---|---|
| id | bigint | NO | nextval('dtlms_users_id_seq'::regclass) |
| username | character varying | NO |  |
| full_name | character varying | NO |  |
| email | character varying | YES |  |
| password_hash | character varying | NO |  |
| is_active | boolean | NO | true |
| is_deleted | boolean | NO | false |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| updated_at | timestamp with time zone | NO | CURRENT_TIMESTAMP |
| department_name | character varying | NO | ''::character varying |
| phone_number | character varying | YES |  |
| last_login_at | timestamp with time zone | YES |  |
**Primary key:** id

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
- proc_def_id_ -> dtlms_wf_re_procdef.id_  (dtlms_wf_hi_actinst_proc_def_id__fkey)

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
- proc_def_id_ -> dtlms_wf_re_procdef.id_  (dtlms_wf_hi_procinst_proc_def_id__fkey)

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
- proc_def_id_ -> dtlms_wf_re_procdef.id_  (dtlms_wf_hi_taskinst_proc_def_id__fkey)

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
- deployment_id_ -> dtlms_wf_re_deployment.id_  (dtlms_wf_re_procdef_deployment_id__fkey)

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
- proc_def_id_ -> dtlms_wf_re_procdef.id_  (dtlms_wf_ru_execution_proc_def_id__fkey)

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
- exec_id_ -> dtlms_wf_ru_execution.id_  (dtlms_wf_ru_task_exec_id__fkey)
- proc_def_id_ -> dtlms_wf_re_procdef.id_  (dtlms_wf_ru_task_proc_def_id__fkey)

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
- exec_id_ -> dtlms_wf_ru_execution.id_  (dtlms_wf_ru_variable_exec_id__fkey)

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
- application_id -> dtlms_recruitment_applications.id  (dtlms_written_exam_scores_application_id_fkey)
