CREATE TABLE IF NOT EXISTS dtlms_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    full_name VARCHAR(128) NOT NULL,
    email VARCHAR(128),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_roles (
    id BIGSERIAL PRIMARY KEY,
    role_code VARCHAR(64) NOT NULL UNIQUE,
    role_name VARCHAR(128) NOT NULL,
    description TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_permissions (
    id BIGSERIAL PRIMARY KEY,
    permission_code VARCHAR(128) NOT NULL UNIQUE,
    permission_name VARCHAR(128) NOT NULL,
    module_name VARCHAR(64) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_user_roles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES dtlms_users(id),
    role_id BIGINT NOT NULL REFERENCES dtlms_roles(id),
    grant_source VARCHAR(64) NOT NULL DEFAULT 'bootstrap',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS dtlms_role_permissions (
    id BIGSERIAL PRIMARY KEY,
    role_id BIGINT NOT NULL REFERENCES dtlms_roles(id),
    permission_id BIGINT NOT NULL REFERENCES dtlms_permissions(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS dtlms_advisors (
    id BIGSERIAL PRIMARY KEY,
    advisor_no VARCHAR(32) NOT NULL UNIQUE,
    full_name VARCHAR(128) NOT NULL,
    title VARCHAR(64) NOT NULL,
    organization_name VARCHAR(128) NOT NULL,
    research_direction VARCHAR(255) NOT NULL,
    annual_quota INTEGER NOT NULL DEFAULT 0,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_teams (
    id BIGSERIAL PRIMARY KEY,
    team_code VARCHAR(32) NOT NULL UNIQUE,
    team_name VARCHAR(128) NOT NULL UNIQUE,
    department_name VARCHAR(128) NOT NULL,
    discipline_name VARCHAR(128),
    lead_advisor_id BIGINT REFERENCES dtlms_advisors(id),
    research_directions TEXT,
    team_status VARCHAR(32) NOT NULL DEFAULT 'active',
    established_on DATE,
    description TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (team_status IN ('active', 'inactive', 'planning', 'archived'))
);

CREATE TABLE IF NOT EXISTS dtlms_team_advisors (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL REFERENCES dtlms_teams(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    advisor_role VARCHAR(32) NOT NULL DEFAULT 'member',
    joined_on DATE,
    left_on DATE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (team_id, advisor_id),
    CHECK (advisor_role IN ('lead', 'member', 'co_advisor')),
    CHECK (left_on IS NULL OR joined_on IS NULL OR left_on >= joined_on)
);

CREATE TABLE IF NOT EXISTS dtlms_students (
    id BIGSERIAL PRIMARY KEY,
    student_no VARCHAR(32) NOT NULL UNIQUE,
    full_name VARCHAR(128) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    political_status VARCHAR(32),
    phone_number VARCHAR(32),
    identity_no VARCHAR(64),
    enrollment_year INTEGER NOT NULL,
    degree_type VARCHAR(32) NOT NULL,
    team_id BIGINT REFERENCES dtlms_teams(id),
    current_status VARCHAR(32) NOT NULL DEFAULT 'enrolled',
    primary_advisor_id BIGINT REFERENCES dtlms_advisors(id),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_student_team_history (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    team_id BIGINT NOT NULL REFERENCES dtlms_teams(id),
    start_date DATE NOT NULL,
    end_date DATE,
    change_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS dtlms_student_advisor_history (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    relation_type VARCHAR(32) NOT NULL DEFAULT 'primary',
    start_date DATE NOT NULL,
    end_date DATE,
    change_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_research_projects (
    id BIGSERIAL PRIMARY KEY,
    project_code VARCHAR(64) NOT NULL UNIQUE,
    project_name VARCHAR(255) NOT NULL,
    principal_advisor_id BIGINT REFERENCES dtlms_advisors(id),
    funding_amount NUMERIC(12, 2),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_training_plans (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    version_no VARCHAR(16) NOT NULL DEFAULT 'v1.0',
    report_cycle VARCHAR(32) NOT NULL,
    plan_status VARCHAR(32) NOT NULL DEFAULT 'draft',
    scientific_goal TEXT NOT NULL,
    assessment_rule TEXT NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (version_no <> ''),
    CHECK (plan_status IN ('draft', 'pending_confirm', 'effective', 'archived'))
);

CREATE TABLE IF NOT EXISTS dtlms_training_plan_versions (
    id BIGSERIAL PRIMARY KEY,
    training_plan_id BIGINT NOT NULL REFERENCES dtlms_training_plans(id),
    version_no VARCHAR(16) NOT NULL,
    change_reason TEXT,
    plan_snapshot TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_scientific_reports (
    id BIGSERIAL PRIMARY KEY,
    business_key VARCHAR(64) NOT NULL UNIQUE,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    training_plan_id BIGINT NOT NULL REFERENCES dtlms_training_plans(id),
    period_label VARCHAR(32) NOT NULL,
    report_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    summary TEXT NOT NULL,
    attachment_url VARCHAR(255),
    reviewer_advisor_id BIGINT REFERENCES dtlms_advisors(id),
    review_score NUMERIC(5, 2),
    review_comment TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (report_status IN ('pending', 'submitted', 'reviewing', 'reviewed', 'rework'))
);

CREATE TABLE IF NOT EXISTS dtlms_outbound_studies (
    id BIGSERIAL PRIMARY KEY,
    business_key VARCHAR(64) NOT NULL UNIQUE,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    study_type VARCHAR(64) NOT NULL,
    destination VARCHAR(128) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    approval_status VARCHAR(32) NOT NULL DEFAULT 'submitted',
    expected_outcome TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS dtlms_achievements (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    achievement_type VARCHAR(32) NOT NULL,
    title VARCHAR(255) NOT NULL,
    published_at DATE,
    publisher_name VARCHAR(255),
    ranking_text VARCHAR(64),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_theses (
    id BIGSERIAL PRIMARY KEY,
    business_key VARCHAR(64) NOT NULL UNIQUE,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    title VARCHAR(255) NOT NULL,
    plagiarism_rate NUMERIC(5, 2),
    thesis_status VARCHAR(32) NOT NULL DEFAULT 'draft',
    blind_review_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    defense_date DATE,
    degree_granted VARCHAR(32) NOT NULL DEFAULT 'pending',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (plagiarism_rate IS NULL OR plagiarism_rate <= 100)
);

CREATE TABLE IF NOT EXISTS dtlms_thesis_reviews (
    id BIGSERIAL PRIMARY KEY,
    thesis_id BIGINT NOT NULL REFERENCES dtlms_theses(id),
    expert_name VARCHAR(128) NOT NULL,
    review_score NUMERIC(5, 2),
    review_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    review_comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_recruitment_plans (
    id BIGSERIAL PRIMARY KEY,
    plan_code VARCHAR(64) NOT NULL UNIQUE,
    plan_name VARCHAR(255) NOT NULL,
    academic_year VARCHAR(16) NOT NULL,
    semester VARCHAR(16) NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    target_quota INTEGER NOT NULL DEFAULT 0,
    plan_status VARCHAR(32) NOT NULL DEFAULT 'draft',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS dtlms_research_fields (
    id BIGSERIAL PRIMARY KEY,
    field_code VARCHAR(64) NOT NULL UNIQUE,
    field_name VARCHAR(128) NOT NULL,
    description TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_recruitment_applications (
    id BIGSERIAL PRIMARY KEY,
    plan_id BIGINT NOT NULL REFERENCES dtlms_recruitment_plans(id),
    business_key VARCHAR(64) NOT NULL UNIQUE,
    student_name VARCHAR(128) NOT NULL,
    candidate_no VARCHAR(64) NOT NULL UNIQUE,
    gender VARCHAR(16) NOT NULL,
    graduation_school VARCHAR(255),
    highest_degree VARCHAR(64),
    intended_field_id BIGINT REFERENCES dtlms_research_fields(id),
    application_status VARCHAR(32) NOT NULL DEFAULT 'submitted',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_application_materials (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    material_type VARCHAR(64) NOT NULL,
    material_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    file_url VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_qualification_reviews (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    reviewer_username VARCHAR(64) NOT NULL,
    review_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    review_comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_reviewer_assignments (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    reviewer_username VARCHAR(64) NOT NULL,
    reviewer_role VARCHAR(32) NOT NULL,
    assignment_status VARCHAR(32) NOT NULL DEFAULT 'assigned',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_material_scores (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    reviewer_assignment_id BIGINT NOT NULL REFERENCES dtlms_reviewer_assignments(id),
    material_score NUMERIC(5, 2),
    recommendation_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_interview_groups (
    id BIGSERIAL PRIMARY KEY,
    plan_id BIGINT NOT NULL REFERENCES dtlms_recruitment_plans(id),
    group_code VARCHAR(64) NOT NULL,
    group_name VARCHAR(128) NOT NULL,
    interview_mode VARCHAR(32) NOT NULL DEFAULT 'offline',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (plan_id, group_code)
);

CREATE TABLE IF NOT EXISTS dtlms_interview_schedules (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    interview_group_id BIGINT NOT NULL REFERENCES dtlms_interview_groups(id),
    admission_ticket_no VARCHAR(64) NOT NULL UNIQUE,
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    schedule_status VARCHAR(32) NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (ends_at >= starts_at)
);

CREATE TABLE IF NOT EXISTS dtlms_interview_scores (
    id BIGSERIAL PRIMARY KEY,
    schedule_id BIGINT NOT NULL REFERENCES dtlms_interview_schedules(id),
    evaluator_username VARCHAR(64) NOT NULL,
    single_choice_score NUMERIC(5, 2),
    fill_blank_score NUMERIC(5, 2),
    coding_score NUMERIC(5, 2),
    interview_score NUMERIC(5, 2),
    ideological_score NUMERIC(5, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_written_exam_scores (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    exam_date DATE,
    exam_score NUMERIC(5, 2),
    import_batch_no VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_admission_decisions (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    decision_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    rank_no INTEGER,
    final_score NUMERIC(5, 2),
    transfer_option VARCHAR(64),
    decision_comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_login_logs (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    login_status VARCHAR(32) NOT NULL,
    login_ip VARCHAR(64),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_operation_logs (
    id BIGSERIAL PRIMARY KEY,
    operator_username VARCHAR(64) NOT NULL,
    operator_role VARCHAR(64) NOT NULL,
    module_name VARCHAR(64) NOT NULL,
    entity_name VARCHAR(64) NOT NULL,
    entity_id VARCHAR(64) NOT NULL,
    action VARCHAR(32) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    request_ip VARCHAR(64),
    result VARCHAR(32) NOT NULL DEFAULT 'success',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_data_sync_logs (
    id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(64) NOT NULL,
    target_system VARCHAR(64) NOT NULL,
    sync_status VARCHAR(32) NOT NULL,
    record_count INTEGER NOT NULL DEFAULT 0,
    failure_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_notification_templates (
    id BIGSERIAL PRIMARY KEY,
    template_code VARCHAR(64) NOT NULL UNIQUE,
    channel VARCHAR(32) NOT NULL,
    title VARCHAR(128) NOT NULL,
    content_template TEXT NOT NULL,
    variables_schema JSONB,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_system_configs (
    id BIGSERIAL PRIMARY KEY,
    config_key VARCHAR(128) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_students_status ON dtlms_students(current_status);
CREATE INDEX IF NOT EXISTS idx_students_primary_advisor ON dtlms_students(primary_advisor_id);
CREATE INDEX IF NOT EXISTS idx_reports_student_period ON dtlms_scientific_reports(student_id, period_label);
CREATE INDEX IF NOT EXISTS idx_training_plan_student ON dtlms_training_plans(student_id);
CREATE INDEX IF NOT EXISTS idx_outbound_studies_status ON dtlms_outbound_studies(approval_status);
CREATE INDEX IF NOT EXISTS idx_thesis_status ON dtlms_theses(thesis_status);
CREATE INDEX IF NOT EXISTS idx_applications_plan_status ON dtlms_recruitment_applications(plan_id, application_status);
CREATE INDEX IF NOT EXISTS idx_interview_schedule_time ON dtlms_interview_schedules(starts_at, ends_at);
CREATE INDEX IF NOT EXISTS idx_admission_decision_status ON dtlms_admission_decisions(decision_status);
CREATE INDEX IF NOT EXISTS idx_operation_logs_module_time ON dtlms_operation_logs(module_name, created_at);
CREATE INDEX IF NOT EXISTS idx_operation_logs_entity ON dtlms_operation_logs(entity_name, entity_id);
CREATE INDEX IF NOT EXISTS idx_sync_logs_source_target ON dtlms_data_sync_logs(source_system, target_system, created_at);
