ALTER TABLE IF EXISTS dtlms_recruitment_plans
    ADD COLUMN IF NOT EXISTS brochure_image_url VARCHAR(255);

CREATE TABLE IF NOT EXISTS dtlms_portal_students (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(128) NOT NULL,
    phone_number VARCHAR(32) NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    id_number VARCHAR(64) NOT NULL UNIQUE,
    graduation_school VARCHAR(255),
    highest_degree VARCHAR(64),
    intended_field VARCHAR(128),
    political_status VARCHAR(64),
    selected_plan_id BIGINT REFERENCES dtlms_recruitment_plans(id),
    selected_team_name VARCHAR(128),
    selected_advisor_name VARCHAR(128),
    self_evaluation TEXT,
    submitted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_runtime_portal_students (
    id BIGINT PRIMARY KEY,
    payload JSONB NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);