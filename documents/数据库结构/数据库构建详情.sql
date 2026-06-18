===============================================================================
-- DTLMS public schema  --  generated 2026-06-17 10:18:34
-- Server : PostgreSQL 17.4 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, 64-bit
-- Database: test061502
-- Schema  : public
===============================================================================

SET search_path = public, pg_catalog;

-- Section 3: Sequences (CREATE SEQUENCE statements).
CREATE SEQUENCE dtlms_achievements_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_admission_decisions_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_advisor_screening_batches_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_advisor_screening_items_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_advisors_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_application_materials_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_background_assessments_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_data_sync_logs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_dict_data_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_dict_types_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_initial_screening_confirmations_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_initial_screening_notifications_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_interview_groups_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_interview_schedules_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_interview_scores_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_login_logs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_material_scores_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_news_articles_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_notification_delivery_logs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_notification_templates_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_operation_logs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_outbound_studies_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_permissions_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_achievement_records_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_attachments_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_education_experiences_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_english_proficiencies_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_family_members_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_practice_experiences_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_application_preferences_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_portal_students_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_qualification_review_logs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_qualification_reviews_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_recruitment_applications_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_recruitment_plans_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_research_fields_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_research_projects_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_reviewer_assignments_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_role_permissions_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_roles_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_scientific_reports_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_student_advisor_history_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_student_team_history_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_students_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_system_configs_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_team_advisors_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_teams_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_theses_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_thesis_reviews_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_training_plan_versions_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_training_plans_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_user_roles_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_users_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_wf_ru_identitylink_id__seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;
CREATE SEQUENCE dtlms_written_exam_scores_id_seq
    AS bigint
    INCREMENT BY 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START WITH 1
    CACHE 1
    NO CYCLE;

-- Section 4: Tables (FK dependency order). PK / UNIQUE / CHECK constraints inlined; FK emitted later as ALTER TABLE.
CREATE TABLE dtlms_recruitment_plans (
    id bigint NOT NULL DEFAULT nextval('dtlms_recruitment_plans_id_seq'::regclass),
    plan_code character varying(64) NOT NULL,
    plan_name character varying(255) NOT NULL,
    academic_year character varying(16) NOT NULL,
    semester character varying(16) NOT NULL,
    start_date timestamp(6) with time zone NOT NULL,
    end_date timestamp(6) with time zone NOT NULL,
    target_quota integer NOT NULL DEFAULT 0,
    plan_status character varying(32) NOT NULL DEFAULT 'draft'::character varying,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    brochure_image_url character varying(255),
    plan_description text,
    PRIMARY KEY (id),
    UNIQUE (plan_code),
    CHECK ((end_date >= start_date))
);

CREATE TABLE dtlms_users (
    id bigint NOT NULL DEFAULT nextval('dtlms_users_id_seq'::regclass),
    username character varying(64) NOT NULL,
    full_name character varying(128) NOT NULL,
    email character varying(128),
    password_hash character varying(255) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    department_name character varying(128) NOT NULL DEFAULT ''::character varying,
    phone_number character varying(32),
    last_login_at timestamp with time zone,
    PRIMARY KEY (id),
    UNIQUE (username)
);

CREATE TABLE dtlms_teams (
    id bigint NOT NULL DEFAULT nextval('dtlms_teams_id_seq'::regclass),
    team_code character varying(32) NOT NULL,
    team_name character varying(128) NOT NULL,
    department_name character varying(128) NOT NULL,
    discipline_name character varying(128),
    research_directions text,
    team_status character varying(32) NOT NULL DEFAULT 'active'::character varying,
    established_on date,
    description text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lead_user_id bigint,
    PRIMARY KEY (id),
    UNIQUE (team_code),
    UNIQUE (team_name),
    CHECK (((team_status)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text, ('planning'::character varying)::text, ('archived'::character varying)::text])))
);

CREATE TABLE dtlms_portal_students (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_students_id_seq'::regclass),
    full_name character varying(128) NOT NULL,
    phone_number character varying(32) NOT NULL,
    email character varying(128) NOT NULL,
    id_number character varying(64) NOT NULL,
    graduation_school character varying(255),
    highest_degree character varying(64),
    intended_field character varying(128),
    political_status character varying(64),
    selected_plan_id bigint,
    selected_team_name character varying(128),
    selected_advisor_name character varying(128),
    self_evaluation text,
    submitted_at timestamp(6) with time zone,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    password_hash character varying(255),
    gender character varying(16),
    birth_date character varying(32),
    ethnic_group character varying(64),
    native_place character varying(128),
    marital_status character varying(32),
    religious_belief character varying(128),
    id_type character varying(64),
    mailing_address text,
    english_level character varying(128),
    family_info text,
    education_experience text,
    practice_experience text,
    personal_profile text,
    recommendation_notes text,
    personal_statement_text text,
    signed_agreement boolean NOT NULL DEFAULT false,
    account_status character varying(32) NOT NULL DEFAULT '启用'::character varying,
    application_draft jsonb,
    selected_team_id bigint,
    selected_advisor_user_id bigint,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (id_number),
    UNIQUE (phone_number)
);

CREATE TABLE dtlms_advisors (
    id bigint NOT NULL DEFAULT nextval('dtlms_advisors_id_seq'::regclass),
    advisor_no character varying(32) NOT NULL,
    full_name character varying(128) NOT NULL,
    title character varying(64) NOT NULL,
    organization_name character varying(128) NOT NULL,
    research_direction character varying(255) NOT NULL,
    annual_quota integer NOT NULL DEFAULT 0,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id bigint,
    PRIMARY KEY (id),
    UNIQUE (advisor_no)
);

CREATE TABLE dtlms_students (
    id bigint NOT NULL DEFAULT nextval('dtlms_students_id_seq'::regclass),
    student_no character varying(32) NOT NULL,
    full_name character varying(128) NOT NULL,
    gender character varying(16) NOT NULL,
    political_status character varying(32),
    phone_number character varying(32),
    identity_no character varying(64),
    enrollment_year integer NOT NULL,
    degree_type character varying(32) NOT NULL,
    team_name character varying(128),
    current_status character varying(32) NOT NULL DEFAULT 'enrolled'::character varying,
    primary_advisor_id bigint,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    team_id bigint,
    portal_student_id bigint,
    PRIMARY KEY (id),
    UNIQUE (student_no)
);

CREATE TABLE dtlms_achievements (
    id bigint NOT NULL DEFAULT nextval('dtlms_achievements_id_seq'::regclass),
    student_id bigint NOT NULL,
    achievement_type character varying(32) NOT NULL,
    title character varying(255) NOT NULL,
    published_at date,
    publisher_name character varying(255),
    ranking_text character varying(64),
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_research_fields (
    id bigint NOT NULL DEFAULT nextval('dtlms_research_fields_id_seq'::regclass),
    field_code character varying(64) NOT NULL,
    field_name character varying(128) NOT NULL,
    description text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (field_code)
);

CREATE TABLE dtlms_recruitment_applications (
    id bigint NOT NULL DEFAULT nextval('dtlms_recruitment_applications_id_seq'::regclass),
    plan_id bigint NOT NULL,
    student_name character varying(128) NOT NULL,
    candidate_no character varying(64) NOT NULL,
    gender character varying(16) NOT NULL,
    graduation_school character varying(255),
    highest_degree character varying(64),
    intended_field_id bigint,
    application_status character varying(32) NOT NULL DEFAULT 'submitted'::character varying,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    business_key character varying(64) NOT NULL,
    review_round character varying(64),
    first_choice character varying(255),
    second_choice character varying(255),
    political_status character varying(64),
    marital_status character varying(32),
    religious_belief character varying(128),
    native_place character varying(128),
    phone_number character varying(64),
    email character varying(255),
    mailing_address text,
    id_type character varying(64),
    id_number character varying(128),
    undergraduate_school character varying(255),
    accept_adjustment character varying(16),
    undergraduate_average_score character varying(64),
    undergraduate_gpa character varying(64),
    undergraduate_rank character varying(64),
    undergraduate_major character varying(255),
    graduate_average_score character varying(64),
    graduate_gpa character varying(64),
    graduate_rank character varying(64),
    graduate_major character varying(255),
    intended_advisor_name character varying(128),
    discovery_channel text,
    graduate_school character varying(255),
    overseas_university_name character varying(255),
    overseas_master_university_name character varying(255),
    self_evaluation text,
    applied_at timestamp(6) with time zone,
    research_problem text,
    research_status_analysis text,
    research_impact text,
    ai_society_impact text,
    dissenting_view text,
    family_info text,
    education_experience text,
    practice_experience text,
    personal_statement_text text,
    student_activity_experience text,
    personal_statement_attachment text,
    material_list_attachment text,
    supplementary_profile text,
    portal_student_id bigint,
    source_channel character varying(64),
    source_channel_other character varying(255),
    first_choice_team_id bigint,
    second_choice_team_id bigint,
    intended_advisor_user_id bigint,
    advisor_screening_status character varying(32) DEFAULT 'pending'::character varying,
    advisor_screening_round character varying(32) DEFAULT 'first_choice'::character varying,
    first_choice_screening_batch_id bigint,
    second_choice_screening_batch_id bigint,
    first_choice_screening_submitted_at timestamp with time zone,
    second_choice_screening_submitted_at timestamp with time zone,
    first_choice_screening_score numeric(5,2),
    second_choice_screening_score numeric(5,2),
    initial_screening_status character varying(32) DEFAULT 'pending'::character varying,
    initial_screening_result character varying(32),
    initial_screening_confirmed_at timestamp with time zone,
    initial_screening_confirmer_username character varying(64),
    initial_screening_confirmer_name character varying(128),
    initial_screening_notification_status character varying(32) DEFAULT 'pending'::character varying,
    initial_screening_notification_sent_at timestamp with time zone,
    next_stage_name character varying(64),
    first_choice_id bigint,
    second_choice_id bigint,
    PRIMARY KEY (id),
    UNIQUE (candidate_no)
);

CREATE TABLE dtlms_admission_decisions (
    id bigint NOT NULL DEFAULT nextval('dtlms_admission_decisions_id_seq'::regclass),
    application_id bigint NOT NULL,
    decision_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    rank_no integer,
    final_score numeric(5,2),
    transfer_option character varying(64),
    decision_comment text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_advisor_screening_batches (
    id bigint NOT NULL DEFAULT nextval('dtlms_advisor_screening_batches_id_seq'::regclass),
    advisor_user_id bigint,
    advisor_username character varying(64) NOT NULL,
    advisor_name character varying(128),
    advisor_role_code character varying(64) NOT NULL DEFAULT 'advisor'::character varying,
    screening_round character varying(32) NOT NULL,
    signature_base64 text NOT NULL,
    submitted_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text])))
);

CREATE TABLE dtlms_advisor_screening_items (
    id bigint NOT NULL DEFAULT nextval('dtlms_advisor_screening_items_id_seq'::regclass),
    batch_id bigint NOT NULL,
    application_id bigint NOT NULL,
    business_key character varying(64) NOT NULL,
    candidate_no character varying(64) NOT NULL,
    screening_round character varying(32) NOT NULL,
    advisor_score numeric(5,2) NOT NULL,
    is_passed boolean NOT NULL,
    screening_status character varying(32) NOT NULL DEFAULT 'submitted'::character varying,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (application_id, screening_round),
    UNIQUE (candidate_no, screening_round),
    CHECK (((screening_round)::text = ANY (ARRAY[('first_choice'::character varying)::text, ('second_choice'::character varying)::text]))),
    CHECK (((advisor_score >= (0)::numeric) AND (advisor_score <= (100)::numeric)))
);

CREATE TABLE dtlms_application_materials (
    id bigint NOT NULL DEFAULT nextval('dtlms_application_materials_id_seq'::regclass),
    application_id bigint NOT NULL,
    material_type character varying(64) NOT NULL,
    material_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    file_url character varying(255) NOT NULL,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_audit_policies (
    id bigint NOT NULL,
    item character varying(128) NOT NULL,
    policy text NOT NULL,
    status character varying(32) NOT NULL DEFAULT '启用'::character varying,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted boolean NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_background_assessments (
    id bigint NOT NULL DEFAULT nextval('dtlms_background_assessments_id_seq'::regclass),
    application_id bigint NOT NULL,
    evaluator_user_id bigint,
    evaluator_username character varying(64) NOT NULL,
    evaluator_name character varying(128),
    evaluator_role_code character varying(64) NOT NULL,
    assessment_result character varying(32) NOT NULL,
    assessment_comment text,
    assessed_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (application_id, evaluator_username)
);

CREATE TABLE dtlms_data_sync_logs (
    id bigint NOT NULL DEFAULT nextval('dtlms_data_sync_logs_id_seq'::regclass),
    source_system character varying(64) NOT NULL,
    target_system character varying(64) NOT NULL,
    sync_status character varying(32) NOT NULL,
    record_count integer NOT NULL DEFAULT 0,
    failure_reason text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_dict_types (
    id bigint NOT NULL DEFAULT nextval('dtlms_dict_types_id_seq'::regclass),
    dict_name character varying(100) NOT NULL,
    dict_type character varying(100) NOT NULL,
    status character varying(32) NOT NULL DEFAULT '启用'::character varying,
    remark text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (dict_type),
    CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))
);

CREATE TABLE dtlms_dict_data (
    id bigint NOT NULL DEFAULT nextval('dtlms_dict_data_id_seq'::regclass),
    dict_type_id bigint NOT NULL,
    dict_type character varying(100) NOT NULL,
    label character varying(100) NOT NULL,
    value character varying(100) NOT NULL,
    sort_order integer NOT NULL DEFAULT 0,
    status character varying(32) NOT NULL DEFAULT '启用'::character varying,
    color_type character varying(32),
    css_class character varying(128),
    remark text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (dict_type, value),
    CHECK (((status)::text = ANY (ARRAY[('启用'::character varying)::text, ('停用'::character varying)::text])))
);

CREATE TABLE dtlms_initial_screening_confirmations (
    id bigint NOT NULL DEFAULT nextval('dtlms_initial_screening_confirmations_id_seq'::regclass),
    application_id bigint NOT NULL,
    business_key character varying(64) NOT NULL,
    candidate_no character varying(64) NOT NULL,
    confirmer_user_id bigint,
    confirmer_username character varying(64) NOT NULL,
    confirmer_name character varying(128),
    confirmer_role_code character varying(64) NOT NULL,
    confirmation_result character varying(32) NOT NULL,
    confirmation_comment text,
    confirmed_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (application_id),
    CHECK (((confirmation_result)::text = ANY (ARRAY[('passed'::character varying)::text, ('rejected'::character varying)::text])))
);

CREATE TABLE dtlms_initial_screening_notifications (
    id bigint NOT NULL DEFAULT nextval('dtlms_initial_screening_notifications_id_seq'::regclass),
    application_id bigint NOT NULL,
    business_key character varying(64) NOT NULL,
    notification_channel character varying(32) NOT NULL,
    notification_event character varying(64) NOT NULL,
    notification_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    recipient_address character varying(255),
    recipient_user_id bigint,
    recipient_username character varying(64),
    payload_json jsonb,
    sent_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CHECK (((notification_channel)::text = ANY (ARRAY[('email'::character varying)::text, ('site_message'::character varying)::text]))),
    CHECK (((notification_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('sent'::character varying)::text, ('failed'::character varying)::text])))
);

CREATE TABLE dtlms_integrations (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    direction character varying(64) NOT NULL,
    cadence character varying(64) NOT NULL,
    status character varying(32) NOT NULL DEFAULT '正常'::character varying,
    owner character varying(128) NOT NULL DEFAULT ''::character varying,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted boolean NOT NULL DEFAULT false,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_interview_groups (
    id bigint NOT NULL DEFAULT nextval('dtlms_interview_groups_id_seq'::regclass),
    plan_id bigint NOT NULL,
    group_code character varying(64) NOT NULL,
    group_name character varying(128) NOT NULL,
    interview_mode character varying(32) NOT NULL DEFAULT 'offline'::character varying,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (plan_id, group_code)
);

CREATE TABLE dtlms_interview_schedules (
    id bigint NOT NULL DEFAULT nextval('dtlms_interview_schedules_id_seq'::regclass),
    application_id bigint NOT NULL,
    interview_group_id bigint NOT NULL,
    admission_ticket_no character varying(64) NOT NULL,
    starts_at timestamp(6) with time zone NOT NULL,
    ends_at timestamp(6) with time zone NOT NULL,
    schedule_status character varying(32) NOT NULL DEFAULT 'scheduled'::character varying,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (admission_ticket_no),
    CHECK ((ends_at >= starts_at))
);

CREATE TABLE dtlms_interview_scores (
    id bigint NOT NULL DEFAULT nextval('dtlms_interview_scores_id_seq'::regclass),
    schedule_id bigint NOT NULL,
    evaluator_username character varying(64) NOT NULL,
    single_choice_score numeric(5,2),
    fill_blank_score numeric(5,2),
    coding_score numeric(5,2),
    interview_score numeric(5,2),
    ideological_score numeric(5,2),
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_login_logs (
    id bigint NOT NULL DEFAULT nextval('dtlms_login_logs_id_seq'::regclass),
    username character varying(64) NOT NULL,
    login_status character varying(32) NOT NULL,
    login_ip character varying(64),
    user_agent text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_reviewer_assignments (
    id bigint NOT NULL DEFAULT nextval('dtlms_reviewer_assignments_id_seq'::regclass),
    application_id bigint NOT NULL,
    reviewer_username character varying(64) NOT NULL,
    reviewer_role character varying(32) NOT NULL,
    assignment_status character varying(32) NOT NULL DEFAULT 'assigned'::character varying,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_material_scores (
    id bigint NOT NULL DEFAULT nextval('dtlms_material_scores_id_seq'::regclass),
    application_id bigint NOT NULL,
    reviewer_assignment_id bigint NOT NULL,
    material_score numeric(5,2),
    recommendation_text text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_news_articles (
    id bigint NOT NULL DEFAULT nextval('dtlms_news_articles_id_seq'::regclass),
    news_code character varying(64) NOT NULL,
    news_title character varying(255) NOT NULL,
    news_content text NOT NULL,
    news_type character varying(100) NOT NULL,
    publisher_user_id bigint,
    publisher_username character varying(64),
    publisher_name character varying(128),
    reviewer_user_id bigint,
    reviewer_username character varying(64),
    reviewer_name character varying(128),
    published_at timestamp with time zone,
    status character varying(32) NOT NULL DEFAULT '草稿'::character varying,
    is_pinned boolean NOT NULL DEFAULT false,
    display_order integer NOT NULL DEFAULT 0,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (news_code),
    CHECK (((status)::text = ANY (ARRAY[('草稿'::character varying)::text, ('待发布'::character varying)::text, ('已发布'::character varying)::text, ('已下线'::character varying)::text]))),
    CHECK (((news_type)::text = ANY (ARRAY[('学生门户通知消息'::character varying)::text, ('学生门户新闻信息'::character varying)::text])))
);

CREATE TABLE dtlms_notification_delivery_logs (
    id bigint NOT NULL DEFAULT nextval('dtlms_notification_delivery_logs_id_seq'::regclass),
    channel character varying(32) NOT NULL,
    template_code character varying(64),
    recipient character varying(255) NOT NULL,
    subject character varying(255) NOT NULL,
    send_status character varying(32) NOT NULL,
    failure_reason text,
    business_key character varying(64),
    triggered_by character varying(64),
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_notification_templates (
    id bigint NOT NULL DEFAULT nextval('dtlms_notification_templates_id_seq'::regclass),
    template_code character varying(64) NOT NULL,
    channel character varying(32) NOT NULL,
    title character varying(128) NOT NULL,
    content_template text NOT NULL,
    variables_schema jsonb,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (template_code)
);

CREATE TABLE dtlms_operation_logs (
    id bigint NOT NULL DEFAULT nextval('dtlms_operation_logs_id_seq'::regclass),
    operator_username character varying(64) NOT NULL,
    operator_role character varying(64) NOT NULL,
    module_name character varying(64) NOT NULL,
    entity_name character varying(64) NOT NULL,
    entity_id character varying(64) NOT NULL,
    action character varying(32) NOT NULL,
    old_value jsonb,
    new_value jsonb,
    request_ip character varying(64),
    result character varying(32) NOT NULL DEFAULT 'success'::character varying,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_outbound_studies (
    id bigint NOT NULL DEFAULT nextval('dtlms_outbound_studies_id_seq'::regclass),
    student_id bigint NOT NULL,
    advisor_id bigint NOT NULL,
    study_type character varying(64) NOT NULL,
    destination character varying(128) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    approval_status character varying(32) NOT NULL DEFAULT 'submitted'::character varying,
    expected_outcome text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    business_key character varying(64) NOT NULL,
    PRIMARY KEY (id),
    CHECK ((end_date >= start_date))
);

CREATE TABLE dtlms_permissions (
    id bigint NOT NULL DEFAULT nextval('dtlms_permissions_id_seq'::regclass),
    permission_code character varying(128) NOT NULL,
    permission_name character varying(128) NOT NULL,
    module_name character varying(64) NOT NULL,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (permission_code)
);

CREATE TABLE dtlms_portal_application_achievement_records (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_achievement_records_id_seq'::regclass),
    application_id bigint NOT NULL,
    achievement_type character varying(32) NOT NULL,
    paper_title character varying(255),
    author_order character varying(32),
    journal_or_conference character varying(255),
    publish_or_index_month character varying(16),
    award_name character varying(255),
    awarding_organization character varying(255),
    award_level character varying(128),
    award_year character varying(16),
    responsibility_text text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    achievement_month character varying(16),
    award_rank character varying(64),
    award_certificate_attachment_url character varying(512),
    description_text text,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_portal_application_attachments (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_attachments_id_seq'::regclass),
    portal_student_id bigint,
    application_id bigint,
    owner_type character varying(64) NOT NULL,
    owner_id bigint,
    attachment_category character varying(64) NOT NULL,
    file_name character varying(255) NOT NULL,
    file_url text NOT NULL,
    file_type character varying(32),
    file_size bigint,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_portal_application_declarations (
    application_id bigint NOT NULL,
    has_read_declaration boolean NOT NULL DEFAULT false,
    declaration_text text,
    progress_snapshot jsonb,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (application_id)
);

CREATE TABLE dtlms_portal_application_education_experiences (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_education_experiences_id_seq'::regclass),
    application_id bigint NOT NULL,
    sort_order integer NOT NULL DEFAULT 1,
    education_stage character varying(64) NOT NULL,
    start_month character varying(16),
    end_month character varying(16),
    school_name character varying(255) NOT NULL,
    major_name character varying(255),
    average_score character varying(64),
    gpa character varying(32),
    ranking character varying(64),
    verifier_name character varying(128),
    verifier_phone character varying(32),
    transcript_attachment_url text,
    degree_certificate_attachment_url text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    graduation_certificate_attachment_url text,
    PRIMARY KEY (id),
    CHECK ((sort_order > 0))
);

CREATE TABLE dtlms_portal_application_english_proficiencies (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_english_proficiencies_id_seq'::regclass),
    application_id bigint NOT NULL,
    exam_name character varying(32) NOT NULL,
    score_text character varying(64) NOT NULL,
    certificate_attachment_url text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_portal_application_family_members (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_family_members_id_seq'::regclass),
    application_id bigint NOT NULL,
    member_name character varying(64) NOT NULL,
    relation_type character varying(16) NOT NULL,
    employer_name character varying(255),
    job_title character varying(128),
    contact_phone character varying(32),
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_portal_application_personal_statements (
    application_id bigint NOT NULL,
    personal_statement_text text,
    ai_problem_statement text,
    ai_industry_opinion text,
    resume_attachment_url text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    growth_experience_text text,
    program_application_reason_text text,
    career_plan_text text,
    supporting_material_attachment_url text,
    PRIMARY KEY (application_id)
);

CREATE TABLE dtlms_portal_application_practice_experiences (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_practice_experiences_id_seq'::regclass),
    application_id bigint NOT NULL,
    start_month character varying(16),
    end_month character varying(16),
    organization_name character varying(255) NOT NULL,
    position_name character varying(128),
    responsibility_text text,
    verifier_name character varying(128),
    verifier_phone character varying(32),
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_portal_application_preferences (
    id bigint NOT NULL DEFAULT nextval('dtlms_portal_application_preferences_id_seq'::regclass),
    application_id bigint NOT NULL,
    preference_order integer NOT NULL,
    advisor_name character varying(128),
    is_optional boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    advisor_user_id bigint,
    PRIMARY KEY (id),
    UNIQUE (application_id, preference_order),
    CHECK ((preference_order > 0))
);

CREATE TABLE dtlms_portal_student_profiles (
    portal_student_id bigint NOT NULL,
    full_name_pinyin character varying(128),
    gender character varying(16),
    birth_date character varying(32),
    ethnic_group character varying(64),
    native_place character varying(128),
    political_status character varying(64),
    marital_status character varying(32),
    religious_belief character varying(128),
    id_type character varying(64),
    mailing_address text,
    emergency_contact_name character varying(128),
    emergency_contact_phone character varying(32),
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    profile_photo_url character varying(255),
    id_card_collage_url character varying(255),
    PRIMARY KEY (portal_student_id)
);

CREATE TABLE dtlms_qualification_review_logs (
    id bigint NOT NULL DEFAULT nextval('dtlms_qualification_review_logs_id_seq'::regclass),
    application_id bigint NOT NULL,
    reviewer_user_id bigint,
    reviewer_username character varying(64) NOT NULL,
    reviewer_name character varying(128),
    reviewer_role_code character varying(64),
    action character varying(32) NOT NULL,
    action_label character varying(64) NOT NULL,
    review_comment text,
    reviewed_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_qualification_reviews (
    id bigint NOT NULL DEFAULT nextval('dtlms_qualification_reviews_id_seq'::regclass),
    application_id bigint NOT NULL,
    reviewer_username character varying(64) NOT NULL,
    review_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    review_comment text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_research_projects (
    id bigint NOT NULL DEFAULT nextval('dtlms_research_projects_id_seq'::regclass),
    project_code character varying(64) NOT NULL,
    project_name character varying(255) NOT NULL,
    principal_advisor_id bigint,
    funding_amount numeric(12,2),
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (project_code)
);

CREATE TABLE dtlms_roles (
    id bigint NOT NULL DEFAULT nextval('dtlms_roles_id_seq'::regclass),
    role_code character varying(64) NOT NULL,
    role_name character varying(128) NOT NULL,
    description text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scope_name character varying(128) NOT NULL DEFAULT '系统管理'::character varying,
    PRIMARY KEY (id),
    UNIQUE (role_code)
);

CREATE TABLE dtlms_role_permissions (
    id bigint NOT NULL DEFAULT nextval('dtlms_role_permissions_id_seq'::regclass),
    role_id bigint NOT NULL,
    permission_id bigint NOT NULL,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (role_id, permission_id)
);

CREATE TABLE dtlms_schema_migrations (
    file_name character varying(255) NOT NULL,
    applied_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (file_name)
);

CREATE TABLE dtlms_training_plans (
    id bigint NOT NULL DEFAULT nextval('dtlms_training_plans_id_seq'::regclass),
    student_id bigint NOT NULL,
    advisor_id bigint NOT NULL,
    version_no character varying(16) NOT NULL DEFAULT 'v1.0'::character varying,
    report_cycle character varying(32) NOT NULL,
    plan_status character varying(32) NOT NULL DEFAULT 'draft'::character varying,
    scientific_goal text NOT NULL,
    assessment_rule text NOT NULL,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CHECK (((plan_status)::text = ANY (ARRAY[('draft'::character varying)::text, ('pending_confirm'::character varying)::text, ('effective'::character varying)::text, ('archived'::character varying)::text]))),
    CHECK (((version_no)::text <> ''::text))
);

CREATE TABLE dtlms_scientific_reports (
    id bigint NOT NULL DEFAULT nextval('dtlms_scientific_reports_id_seq'::regclass),
    student_id bigint NOT NULL,
    training_plan_id bigint NOT NULL,
    period_label character varying(32) NOT NULL,
    report_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    summary text NOT NULL,
    attachment_url character varying(255),
    reviewer_advisor_id bigint,
    review_score numeric(5,2),
    review_comment text,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    business_key character varying(64) NOT NULL,
    PRIMARY KEY (id),
    CHECK (((report_status)::text = ANY (ARRAY[('pending'::character varying)::text, ('submitted'::character varying)::text, ('reviewing'::character varying)::text, ('reviewed'::character varying)::text, ('rework'::character varying)::text])))
);

CREATE TABLE dtlms_student_advisor_history (
    id bigint NOT NULL DEFAULT nextval('dtlms_student_advisor_history_id_seq'::regclass),
    student_id bigint NOT NULL,
    advisor_id bigint NOT NULL,
    relation_type character varying(32) NOT NULL DEFAULT 'primary'::character varying,
    start_date date NOT NULL,
    end_date date,
    change_reason text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_student_team_history (
    id bigint NOT NULL DEFAULT nextval('dtlms_student_team_history_id_seq'::regclass),
    student_id bigint NOT NULL,
    team_id bigint NOT NULL,
    start_date date NOT NULL,
    end_date date,
    change_reason text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CHECK (((end_date IS NULL) OR (end_date >= start_date)))
);

CREATE TABLE dtlms_system_configs (
    id bigint NOT NULL DEFAULT nextval('dtlms_system_configs_id_seq'::regclass),
    config_key character varying(128) NOT NULL,
    config_value text NOT NULL,
    description text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (config_key)
);

CREATE TABLE dtlms_team_advisors (
    id bigint NOT NULL DEFAULT nextval('dtlms_team_advisors_id_seq'::regclass),
    team_id bigint NOT NULL,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    advisor_user_id bigint,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_theses (
    id bigint NOT NULL DEFAULT nextval('dtlms_theses_id_seq'::regclass),
    student_id bigint NOT NULL,
    advisor_id bigint NOT NULL,
    title character varying(255) NOT NULL,
    plagiarism_rate numeric(5,2),
    thesis_status character varying(32) NOT NULL DEFAULT 'draft'::character varying,
    blind_review_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    defense_date date,
    degree_granted character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    is_deleted boolean NOT NULL DEFAULT false,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    business_key character varying(64) NOT NULL,
    PRIMARY KEY (id),
    CHECK (((plagiarism_rate IS NULL) OR (plagiarism_rate <= (100)::numeric)))
);

CREATE TABLE dtlms_thesis_reviews (
    id bigint NOT NULL DEFAULT nextval('dtlms_thesis_reviews_id_seq'::regclass),
    thesis_id bigint NOT NULL,
    expert_name character varying(128) NOT NULL,
    review_score numeric(5,2),
    review_status character varying(32) NOT NULL DEFAULT 'pending'::character varying,
    review_comment text,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_training_plan_versions (
    id bigint NOT NULL DEFAULT nextval('dtlms_training_plan_versions_id_seq'::regclass),
    training_plan_id bigint NOT NULL,
    version_no character varying(16) NOT NULL,
    change_reason text,
    plan_snapshot text NOT NULL,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE dtlms_user_profiles (
    username character varying(64) NOT NULL,
    full_name character varying(128) NOT NULL,
    role_name character varying(128) NOT NULL,
    department_name character varying(128) NOT NULL,
    phone_number character varying(32),
    email character varying(128),
    theme_color character varying(32) NOT NULL DEFAULT '#0f4cbd'::character varying,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    introduction text,
    PRIMARY KEY (username)
);

CREATE TABLE dtlms_user_roles (
    id bigint NOT NULL DEFAULT nextval('dtlms_user_roles_id_seq'::regclass),
    user_id bigint NOT NULL,
    role_id bigint NOT NULL,
    grant_source character varying(64) NOT NULL DEFAULT 'bootstrap'::character varying,
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (user_id, role_id)
);

CREATE TABLE dtlms_wf_de_model (
    id_ character varying(64) NOT NULL,
    name_ character varying(255) NOT NULL,
    key_ character varying(128) NOT NULL,
    category_ character varying(128),
    version_ integer NOT NULL DEFAULT 1,
    model_type_ integer NOT NULL DEFAULT 0,
    description_ text,
    meta_info_ jsonb,
    created_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tenant_id_ character varying(64),
    deployment_id_ character varying(64),
    resource_name_ character varying(255),
    editor_source_value_ text,
    editor_source_extra_value_ jsonb,
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_re_deployment (
    id_ character varying(64) NOT NULL,
    name_ character varying(255) NOT NULL,
    category_ character varying(128),
    key_ character varying(128),
    deploy_time_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tenant_id_ character varying(64),
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_re_procdef (
    id_ character varying(64) NOT NULL,
    key_ character varying(128) NOT NULL,
    version_ integer NOT NULL DEFAULT 1,
    deployment_id_ character varying(64),
    resource_name_ character varying(255),
    diagram_resource_name_ character varying(255),
    name_ character varying(255) NOT NULL,
    category_ character varying(128),
    description_ text,
    suspension_state_ integer NOT NULL DEFAULT 1,
    tenant_id_ character varying(64),
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_hi_actinst (
    id_ character varying(64) NOT NULL,
    proc_def_id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    exec_id_ character varying(64),
    act_id_ character varying(128) NOT NULL,
    act_name_ character varying(255),
    act_type_ character varying(64) NOT NULL,
    assignee_ character varying(64),
    start_time_ timestamp(6) with time zone NOT NULL,
    end_time_ timestamp(6) with time zone,
    duration_ms_ bigint,
    business_key_ character varying(64),
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_hi_procinst (
    id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    business_key_ character varying(64),
    proc_def_id_ character varying(64) NOT NULL,
    start_time_ timestamp(6) with time zone NOT NULL,
    end_time_ timestamp(6) with time zone,
    duration_ms_ bigint,
    start_user_id_ character varying(64),
    end_act_id_ character varying(128),
    delete_reason_ character varying(255),
    start_act_id_ character varying(128),
    state_ character varying(32) NOT NULL DEFAULT 'ACTIVE'::character varying,
    PRIMARY KEY (id_),
    UNIQUE (proc_inst_id_)
);

CREATE TABLE dtlms_wf_hi_taskinst (
    id_ character varying(64) NOT NULL,
    task_def_key_ character varying(128),
    proc_def_id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    exec_id_ character varying(64),
    name_ character varying(255) NOT NULL,
    business_key_ character varying(64),
    assignee_ character varying(64),
    owner_ character varying(64),
    start_time_ timestamp(6) with time zone NOT NULL,
    claim_time_ timestamp(6) with time zone,
    end_time_ timestamp(6) with time zone,
    duration_ms_ bigint,
    due_date_ timestamp(6) with time zone,
    delete_reason_ character varying(255),
    priority_ integer NOT NULL DEFAULT 50,
    category_ character varying(128),
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_hi_varinst (
    id_ character varying(128) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    exec_id_ character varying(64),
    task_id_ character varying(64),
    name_ character varying(128) NOT NULL,
    var_type_ character varying(32) NOT NULL,
    text_value_ text,
    number_value_ bigint,
    json_value_ jsonb,
    create_time_ timestamp(6) with time zone NOT NULL,
    last_updated_time_ timestamp(6) with time zone NOT NULL,
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_ru_execution (
    id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    proc_def_id_ character varying(64) NOT NULL,
    business_key_ character varying(64),
    parent_id_ character varying(64),
    act_id_ character varying(128),
    is_active_ boolean NOT NULL DEFAULT true,
    is_concurrent_ boolean NOT NULL DEFAULT false,
    is_scope_ boolean NOT NULL DEFAULT true,
    start_time_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    start_user_id_ character varying(64),
    super_exec_ character varying(64),
    tenant_id_ character varying(64),
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_ru_identitylink (
    id_ bigint NOT NULL DEFAULT nextval('dtlms_wf_ru_identitylink_id__seq'::regclass),
    task_id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64),
    user_id_ character varying(64),
    group_id_ character varying(64),
    link_type_ character varying(32) NOT NULL,
    created_at_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_ru_task (
    id_ character varying(64) NOT NULL,
    exec_id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    proc_def_id_ character varying(64) NOT NULL,
    task_def_key_ character varying(128),
    name_ character varying(255) NOT NULL,
    business_key_ character varying(64),
    assignee_ character varying(64),
    owner_ character varying(64),
    create_time_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date_ timestamp(6) with time zone,
    claim_time_ timestamp(6) with time zone,
    priority_ integer NOT NULL DEFAULT 50,
    suspension_state_ integer NOT NULL DEFAULT 1,
    tenant_id_ character varying(64),
    form_key_ character varying(255),
    description_ text,
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_wf_ru_variable (
    id_ character varying(128) NOT NULL,
    exec_id_ character varying(64) NOT NULL,
    proc_inst_id_ character varying(64) NOT NULL,
    task_id_ character varying(64),
    name_ character varying(128) NOT NULL,
    var_type_ character varying(32) NOT NULL,
    text_value_ text,
    number_value_ bigint,
    json_value_ jsonb,
    create_time_ timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_)
);

CREATE TABLE dtlms_written_exam_scores (
    id bigint NOT NULL DEFAULT nextval('dtlms_written_exam_scores_id_seq'::regclass),
    application_id bigint NOT NULL,
    exam_date date,
    exam_score numeric(5,2),
    import_batch_no character varying(64),
    created_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(6) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


-- Section 5: Foreign key constraints (ALTER TABLE).
ALTER TABLE dtlms_achievements ADD CONSTRAINT dtlms_achievements_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_admission_decisions ADD CONSTRAINT dtlms_admission_decisions_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_advisor_screening_items ADD CONSTRAINT dtlms_advisor_screening_items_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_advisor_screening_items ADD CONSTRAINT dtlms_advisor_screening_items_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES dtlms_advisor_screening_batches(id) ON DELETE CASCADE;
ALTER TABLE dtlms_advisors ADD CONSTRAINT fk_dtlms_advisors_user_id FOREIGN KEY (user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_application_materials ADD CONSTRAINT dtlms_application_materials_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_background_assessments ADD CONSTRAINT dtlms_background_assessments_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_dict_data ADD CONSTRAINT dtlms_dict_data_dict_type_id_fkey FOREIGN KEY (dict_type_id) REFERENCES dtlms_dict_types(id);
ALTER TABLE dtlms_initial_screening_confirmations ADD CONSTRAINT dtlms_initial_screening_confirmations_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_initial_screening_notifications ADD CONSTRAINT dtlms_initial_screening_notifications_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_interview_groups ADD CONSTRAINT dtlms_interview_groups_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id);
ALTER TABLE dtlms_interview_schedules ADD CONSTRAINT dtlms_interview_schedules_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_interview_schedules ADD CONSTRAINT dtlms_interview_schedules_interview_group_id_fkey FOREIGN KEY (interview_group_id) REFERENCES dtlms_interview_groups(id);
ALTER TABLE dtlms_interview_scores ADD CONSTRAINT dtlms_interview_scores_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES dtlms_interview_schedules(id);
ALTER TABLE dtlms_material_scores ADD CONSTRAINT dtlms_material_scores_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_material_scores ADD CONSTRAINT dtlms_material_scores_reviewer_assignment_id_fkey FOREIGN KEY (reviewer_assignment_id) REFERENCES dtlms_reviewer_assignments(id);
ALTER TABLE dtlms_outbound_studies ADD CONSTRAINT dtlms_outbound_studies_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_outbound_studies ADD CONSTRAINT dtlms_outbound_studies_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_portal_application_achievement_records ADD CONSTRAINT dtlms_portal_application_achievement_record_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_attachments ADD CONSTRAINT dtlms_portal_application_attachments_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_attachments ADD CONSTRAINT dtlms_portal_application_attachments_portal_student_id_fkey FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_declarations ADD CONSTRAINT dtlms_portal_application_declarations_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_education_experiences ADD CONSTRAINT dtlms_portal_application_education_experien_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_english_proficiencies ADD CONSTRAINT dtlms_portal_application_english_proficienc_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_family_members ADD CONSTRAINT dtlms_portal_application_family_members_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_personal_statements ADD CONSTRAINT dtlms_portal_application_personal_statement_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_practice_experiences ADD CONSTRAINT dtlms_portal_application_practice_experienc_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_preferences ADD CONSTRAINT dtlms_portal_application_preferences_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_application_preferences ADD CONSTRAINT fk_dtlms_portal_application_preferences_advisor_user_id FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_portal_student_profiles ADD CONSTRAINT dtlms_portal_student_profiles_portal_student_id_fkey FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) ON DELETE CASCADE;
ALTER TABLE dtlms_portal_students ADD CONSTRAINT dtlms_portal_students_selected_plan_id_fkey FOREIGN KEY (selected_plan_id) REFERENCES dtlms_recruitment_plans(id);
ALTER TABLE dtlms_portal_students ADD CONSTRAINT fk_dtlms_portal_students_selected_advisor_user_id FOREIGN KEY (selected_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_portal_students ADD CONSTRAINT fk_dtlms_portal_students_selected_team_id FOREIGN KEY (selected_team_id) REFERENCES dtlms_teams(id) NOT VALID;
ALTER TABLE dtlms_qualification_review_logs ADD CONSTRAINT dtlms_qualification_review_logs_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_qualification_reviews ADD CONSTRAINT dtlms_qualification_reviews_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT dtlms_recruitment_applications_intended_field_id_fkey FOREIGN KEY (intended_field_id) REFERENCES dtlms_research_fields(id);
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT dtlms_recruitment_applications_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES dtlms_recruitment_plans(id);
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT dtlms_recruitment_applications_portal_student_id_fkey FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id);
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT fk_dtlms_recruitment_applications_first_choice_id FOREIGN KEY (first_choice_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT fk_dtlms_recruitment_applications_first_choice_team_id FOREIGN KEY (first_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT fk_dtlms_recruitment_applications_intended_advisor_user_id FOREIGN KEY (intended_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT fk_dtlms_recruitment_applications_second_choice_id FOREIGN KEY (second_choice_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_recruitment_applications ADD CONSTRAINT fk_dtlms_recruitment_applications_second_choice_team_id FOREIGN KEY (second_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
ALTER TABLE dtlms_research_projects ADD CONSTRAINT dtlms_research_projects_principal_advisor_id_fkey FOREIGN KEY (principal_advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_reviewer_assignments ADD CONSTRAINT dtlms_reviewer_assignments_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);
ALTER TABLE dtlms_role_permissions ADD CONSTRAINT dtlms_role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES dtlms_permissions(id);
ALTER TABLE dtlms_role_permissions ADD CONSTRAINT dtlms_role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES dtlms_roles(id);
ALTER TABLE dtlms_scientific_reports ADD CONSTRAINT dtlms_scientific_reports_reviewer_advisor_id_fkey FOREIGN KEY (reviewer_advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_scientific_reports ADD CONSTRAINT dtlms_scientific_reports_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_scientific_reports ADD CONSTRAINT dtlms_scientific_reports_training_plan_id_fkey FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id);
ALTER TABLE dtlms_student_advisor_history ADD CONSTRAINT dtlms_student_advisor_history_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_student_advisor_history ADD CONSTRAINT dtlms_student_advisor_history_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_student_team_history ADD CONSTRAINT dtlms_student_team_history_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_student_team_history ADD CONSTRAINT dtlms_student_team_history_team_id_fkey FOREIGN KEY (team_id) REFERENCES dtlms_teams(id);
ALTER TABLE dtlms_students ADD CONSTRAINT dtlms_students_primary_advisor_id_fkey FOREIGN KEY (primary_advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_students ADD CONSTRAINT dtlms_students_team_id_fkey FOREIGN KEY (team_id) REFERENCES dtlms_teams(id);
ALTER TABLE dtlms_students ADD CONSTRAINT fk_dtlms_students_portal_student_id FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) NOT VALID;
ALTER TABLE dtlms_team_advisors ADD CONSTRAINT dtlms_team_advisors_team_id_fkey FOREIGN KEY (team_id) REFERENCES dtlms_teams(id);
ALTER TABLE dtlms_team_advisors ADD CONSTRAINT fk_dtlms_team_advisors_advisor_user_id FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_teams ADD CONSTRAINT fk_dtlms_teams_lead_user_id FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID;
ALTER TABLE dtlms_theses ADD CONSTRAINT dtlms_theses_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_theses ADD CONSTRAINT dtlms_theses_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_thesis_reviews ADD CONSTRAINT dtlms_thesis_reviews_thesis_id_fkey FOREIGN KEY (thesis_id) REFERENCES dtlms_theses(id);
ALTER TABLE dtlms_training_plan_versions ADD CONSTRAINT dtlms_training_plan_versions_training_plan_id_fkey FOREIGN KEY (training_plan_id) REFERENCES dtlms_training_plans(id);
ALTER TABLE dtlms_training_plans ADD CONSTRAINT dtlms_training_plans_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES dtlms_advisors(id);
ALTER TABLE dtlms_training_plans ADD CONSTRAINT dtlms_training_plans_student_id_fkey FOREIGN KEY (student_id) REFERENCES dtlms_students(id);
ALTER TABLE dtlms_user_profiles ADD CONSTRAINT dtlms_user_profiles_username_fkey FOREIGN KEY (username) REFERENCES dtlms_users(username) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE dtlms_user_roles ADD CONSTRAINT dtlms_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES dtlms_roles(id);
ALTER TABLE dtlms_user_roles ADD CONSTRAINT dtlms_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES dtlms_users(id);
ALTER TABLE dtlms_wf_hi_actinst ADD CONSTRAINT dtlms_wf_hi_actinst_proc_def_id__fkey FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_);
ALTER TABLE dtlms_wf_hi_procinst ADD CONSTRAINT dtlms_wf_hi_procinst_proc_def_id__fkey FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_);
ALTER TABLE dtlms_wf_hi_taskinst ADD CONSTRAINT dtlms_wf_hi_taskinst_proc_def_id__fkey FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_);
ALTER TABLE dtlms_wf_re_procdef ADD CONSTRAINT dtlms_wf_re_procdef_deployment_id__fkey FOREIGN KEY (deployment_id_) REFERENCES dtlms_wf_re_deployment(id_);
ALTER TABLE dtlms_wf_ru_execution ADD CONSTRAINT dtlms_wf_ru_execution_proc_def_id__fkey FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_);
ALTER TABLE dtlms_wf_ru_task ADD CONSTRAINT dtlms_wf_ru_task_exec_id__fkey FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_);
ALTER TABLE dtlms_wf_ru_task ADD CONSTRAINT dtlms_wf_ru_task_proc_def_id__fkey FOREIGN KEY (proc_def_id_) REFERENCES dtlms_wf_re_procdef(id_);
ALTER TABLE dtlms_wf_ru_variable ADD CONSTRAINT dtlms_wf_ru_variable_exec_id__fkey FOREIGN KEY (exec_id_) REFERENCES dtlms_wf_ru_execution(id_);
ALTER TABLE dtlms_written_exam_scores ADD CONSTRAINT dtlms_written_exam_scores_application_id_fkey FOREIGN KEY (application_id) REFERENCES dtlms_recruitment_applications(id);

-- Section 6: Views and materialized views.
CREATE VIEW dtlms_v_degree_pipeline AS
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
   FROM dtlms_theses t
     JOIN dtlms_students s ON s.id = t.student_id
     JOIN dtlms_advisors a ON a.id = t.advisor_id
     LEFT JOIN dtlms_thesis_reviews tr ON tr.thesis_id = t.id
  WHERE t.is_deleted = false
  GROUP BY t.id, s.student_no, s.full_name, a.full_name, t.title, t.plagiarism_rate, t.thesis_status, t.blind_review_status, t.defense_date, t.degree_granted;

CREATE VIEW dtlms_v_recruitment_dashboard AS
 SELECT rp.id AS plan_id,
    rp.plan_code,
    rp.plan_name,
    rp.academic_year,
    rp.semester,
    rp.plan_status,
    count(DISTINCT ra.id) AS application_total,
    count(DISTINCT
        CASE
            WHEN ra.application_status::text = 'qualified'::text THEN ra.id
            ELSE NULL::bigint
        END) AS qualified_total,
    count(DISTINCT
        CASE
            WHEN ra.application_status::text = 'interviewing'::text THEN ra.id
            ELSE NULL::bigint
        END) AS interviewing_total,
    count(DISTINCT
        CASE
            WHEN ad.decision_status::text = ANY (ARRAY['pre_admitted'::character varying::text, 'accepted'::character varying::text]) THEN ad.id
            ELSE NULL::bigint
        END) AS admitted_total,
    avg(ms.material_score) AS avg_material_score
   FROM dtlms_recruitment_plans rp
     LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id AND ra.is_deleted = false
     LEFT JOIN dtlms_material_scores ms ON ms.application_id = ra.id
     LEFT JOIN dtlms_admission_decisions ad ON ad.application_id = ra.id
  WHERE rp.is_deleted = false
  GROUP BY rp.id, rp.plan_code, rp.plan_name, rp.academic_year, rp.semester, rp.plan_status;

CREATE VIEW dtlms_v_student_lifecycle_snapshot AS
 WITH latest_report AS (
         SELECT DISTINCT ON (dtlms_scientific_reports.student_id) dtlms_scientific_reports.student_id,
            dtlms_scientific_reports.period_label,
            dtlms_scientific_reports.report_status,
            dtlms_scientific_reports.review_score,
            dtlms_scientific_reports.updated_at
           FROM dtlms_scientific_reports
          WHERE dtlms_scientific_reports.is_deleted = false
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
   FROM dtlms_students s
     LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.version_no,
            dtlms_training_plans.plan_status
           FROM dtlms_training_plans
          WHERE dtlms_training_plans.student_id = s.id AND dtlms_training_plans.is_deleted = false
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON true
     LEFT JOIN latest_report lr ON lr.student_id = s.id
     LEFT JOIN LATERAL ( SELECT dtlms_theses.title,
            dtlms_theses.thesis_status,
            dtlms_theses.blind_review_status,
            dtlms_theses.degree_granted
           FROM dtlms_theses
          WHERE dtlms_theses.student_id = s.id AND dtlms_theses.is_deleted = false
          ORDER BY dtlms_theses.updated_at DESC
         LIMIT 1) t ON true
  WHERE s.is_deleted = false;

CREATE VIEW dtlms_v_training_compliance AS
 SELECT s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    a.full_name AS advisor_name,
    tp.plan_status,
    tp.report_cycle,
    count(sr.id) FILTER (WHERE sr.report_status::text = ANY (ARRAY['submitted'::character varying::text, 'reviewed'::character varying::text])) AS submitted_report_count,
    count(sr.id) FILTER (WHERE sr.report_status::text = 'pending'::text) AS pending_report_count,
    count(os.id) FILTER (WHERE os.approval_status::text = ANY (ARRAY['submitted'::character varying::text, 'approved'::character varying::text, 'ongoing'::character varying::text])) AS outbound_study_count
   FROM dtlms_students s
     LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.plan_status,
            dtlms_training_plans.report_cycle
           FROM dtlms_training_plans
          WHERE dtlms_training_plans.student_id = s.id AND dtlms_training_plans.is_deleted = false
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON true
     LEFT JOIN dtlms_scientific_reports sr ON sr.student_id = s.id AND sr.is_deleted = false
     LEFT JOIN dtlms_outbound_studies os ON os.student_id = s.id AND os.is_deleted = false
  WHERE s.is_deleted = false
  GROUP BY s.id, s.student_no, s.full_name, s.current_status, a.full_name, tp.plan_status, tp.report_cycle;

-- Section 7: Non-constraint indexes (PK/UNIQUE indexes are emitted as part of the table definition).
CREATE INDEX idx_admission_decision_status ON dtlms_admission_decisions USING btree (decision_status);
CREATE INDEX idx_advisor_screening_batches_advisor_round ON dtlms_advisor_screening_batches USING btree (advisor_username, screening_round, submitted_at DESC);
CREATE INDEX idx_advisor_screening_items_application ON dtlms_advisor_screening_items USING btree (application_id, screening_round, created_at DESC);
CREATE INDEX idx_advisor_screening_items_batch ON dtlms_advisor_screening_items USING btree (batch_id);
CREATE INDEX idx_advisor_screening_items_business_key ON dtlms_advisor_screening_items USING btree (business_key);
CREATE UNIQUE INDEX idx_dtlms_advisors_user_id ON dtlms_advisors USING btree (user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_background_assessment_application ON dtlms_background_assessments USING btree (application_id, assessed_at DESC);
CREATE INDEX idx_background_assessment_result ON dtlms_background_assessments USING btree (assessment_result);
CREATE INDEX idx_sync_logs_source_target ON dtlms_data_sync_logs USING btree (source_system, target_system, created_at);
CREATE INDEX idx_dtlms_dict_data_type_sort ON dtlms_dict_data USING btree (dict_type, sort_order, id);
CREATE INDEX idx_initial_screening_confirmations_application ON dtlms_initial_screening_confirmations USING btree (application_id, confirmed_at DESC);
CREATE INDEX idx_initial_screening_notifications_application ON dtlms_initial_screening_notifications USING btree (application_id, created_at DESC);
CREATE INDEX idx_initial_screening_notifications_status ON dtlms_initial_screening_notifications USING btree (notification_status, notification_channel);
CREATE INDEX idx_interview_schedule_time ON dtlms_interview_schedules USING btree (starts_at, ends_at);
CREATE INDEX idx_dtlms_news_articles_deleted_order ON dtlms_news_articles USING btree (is_deleted, display_order DESC, id DESC);
CREATE INDEX idx_dtlms_news_articles_status_published ON dtlms_news_articles USING btree (status, published_at DESC, display_order DESC, id DESC) WHERE is_deleted = false;
CREATE INDEX idx_dtlms_news_articles_type_status ON dtlms_news_articles USING btree (news_type, status, published_at DESC, id DESC) WHERE is_deleted = false;
CREATE INDEX idx_notification_delivery_logs_channel_time ON dtlms_notification_delivery_logs USING btree (channel, created_at);
CREATE INDEX idx_notification_delivery_logs_recipient ON dtlms_notification_delivery_logs USING btree (recipient);
CREATE INDEX idx_notification_delivery_logs_status_time ON dtlms_notification_delivery_logs USING btree (send_status, created_at);
CREATE INDEX idx_operation_logs_entity ON dtlms_operation_logs USING btree (entity_name, entity_id);
CREATE INDEX idx_operation_logs_module_time ON dtlms_operation_logs USING btree (module_name, created_at);
CREATE INDEX idx_outbound_studies_status ON dtlms_outbound_studies USING btree (approval_status);
CREATE UNIQUE INDEX ux_dtlms_outbound_studies_business_key ON dtlms_outbound_studies USING btree (business_key);
CREATE INDEX idx_portal_application_achievement_application ON dtlms_portal_application_achievement_records USING btree (application_id, achievement_type);
CREATE INDEX idx_portal_application_attachment_owner ON dtlms_portal_application_attachments USING btree (application_id, owner_type, owner_id);
CREATE INDEX idx_portal_application_education_application ON dtlms_portal_application_education_experiences USING btree (application_id, sort_order);
CREATE INDEX idx_portal_application_english_application ON dtlms_portal_application_english_proficiencies USING btree (application_id);
CREATE INDEX idx_portal_application_family_application ON dtlms_portal_application_family_members USING btree (application_id);
CREATE UNIQUE INDEX ux_portal_application_family_parent_unique ON dtlms_portal_application_family_members USING btree (application_id, relation_type) WHERE relation_type::text = ANY (ARRAY['父亲'::character varying::text, '母亲'::character varying::text]);
CREATE INDEX idx_portal_application_practice_application ON dtlms_portal_application_practice_experiences USING btree (application_id);
CREATE INDEX idx_portal_application_preferences_application ON dtlms_portal_application_preferences USING btree (application_id, preference_order);
CREATE INDEX idx_dtlms_portal_students_selected_team_id ON dtlms_portal_students USING btree (selected_team_id) WHERE selected_team_id IS NOT NULL;
CREATE INDEX idx_qualification_review_logs_application ON dtlms_qualification_review_logs USING btree (application_id, reviewed_at DESC);
CREATE INDEX idx_qualification_review_logs_reviewer ON dtlms_qualification_review_logs USING btree (reviewer_username, reviewed_at DESC);
CREATE INDEX idx_applications_plan_status ON dtlms_recruitment_applications USING btree (plan_id, application_status);
CREATE INDEX idx_applications_portal_student ON dtlms_recruitment_applications USING btree (portal_student_id);
CREATE INDEX idx_dtlms_recruitment_applications_email ON dtlms_recruitment_applications USING btree (email);
CREATE INDEX idx_dtlms_recruitment_applications_first_choice_team_id ON dtlms_recruitment_applications USING btree (first_choice_team_id) WHERE first_choice_team_id IS NOT NULL;
CREATE INDEX idx_dtlms_recruitment_applications_phone_number ON dtlms_recruitment_applications USING btree (phone_number);
CREATE INDEX idx_recruitment_applications_advisor_screening_status ON dtlms_recruitment_applications USING btree (advisor_screening_status, advisor_screening_round);
CREATE INDEX idx_recruitment_applications_initial_screening_status ON dtlms_recruitment_applications USING btree (initial_screening_status, initial_screening_result);
CREATE UNIQUE INDEX ux_dtlms_recruitment_applications_business_key ON dtlms_recruitment_applications USING btree (business_key);
CREATE INDEX idx_reports_student_period ON dtlms_scientific_reports USING btree (student_id, period_label);
CREATE UNIQUE INDEX ux_dtlms_scientific_reports_business_key ON dtlms_scientific_reports USING btree (business_key);
CREATE UNIQUE INDEX idx_dtlms_students_portal_student_id ON dtlms_students USING btree (portal_student_id) WHERE portal_student_id IS NOT NULL;
CREATE INDEX idx_students_primary_advisor ON dtlms_students USING btree (primary_advisor_id);
CREATE INDEX idx_students_status ON dtlms_students USING btree (current_status);
CREATE INDEX idx_dtlms_team_advisors_team_user ON dtlms_team_advisors USING btree (team_id, advisor_user_id) WHERE advisor_user_id IS NOT NULL;
CREATE INDEX idx_dtlms_teams_lead_user_id ON dtlms_teams USING btree (lead_user_id) WHERE lead_user_id IS NOT NULL;
CREATE INDEX idx_thesis_status ON dtlms_theses USING btree (thesis_status);
CREATE UNIQUE INDEX ux_dtlms_theses_business_key ON dtlms_theses USING btree (business_key);
CREATE INDEX idx_training_plan_student ON dtlms_training_plans USING btree (student_id);
CREATE INDEX idx_dtlms_wf_hi_actinst_proc_inst ON dtlms_wf_hi_actinst USING btree (proc_inst_id_);
CREATE INDEX idx_dtlms_wf_hi_procinst_business_key ON dtlms_wf_hi_procinst USING btree (business_key_);
CREATE INDEX idx_dtlms_wf_hi_taskinst_proc_inst ON dtlms_wf_hi_taskinst USING btree (proc_inst_id_);
CREATE INDEX idx_dtlms_wf_hi_varinst_proc_inst ON dtlms_wf_hi_varinst USING btree (proc_inst_id_);
CREATE INDEX idx_dtlms_wf_re_procdef_key ON dtlms_wf_re_procdef USING btree (key_);
CREATE INDEX idx_dtlms_wf_ru_execution_proc_inst ON dtlms_wf_ru_execution USING btree (proc_inst_id_);
CREATE INDEX idx_dtlms_wf_ru_task_business_key ON dtlms_wf_ru_task USING btree (business_key_);
CREATE INDEX idx_dtlms_wf_ru_task_proc_inst ON dtlms_wf_ru_task USING btree (proc_inst_id_);

