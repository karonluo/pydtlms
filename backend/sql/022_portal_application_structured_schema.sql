ALTER TABLE IF EXISTS dtlms_recruitment_applications
    ADD COLUMN IF NOT EXISTS portal_student_id BIGINT REFERENCES dtlms_portal_students(id),
    ADD COLUMN IF NOT EXISTS source_channel VARCHAR(64),
    ADD COLUMN IF NOT EXISTS source_channel_other VARCHAR(255);

CREATE TABLE IF NOT EXISTS dtlms_portal_student_profiles (
    portal_student_id BIGINT PRIMARY KEY REFERENCES dtlms_portal_students(id) ON DELETE CASCADE,
    full_name_pinyin VARCHAR(128),
    profile_photo_url VARCHAR(255),
    id_card_collage_url VARCHAR(255),
    gender VARCHAR(16),
    birth_date VARCHAR(32),
    ethnic_group VARCHAR(64),
    native_place VARCHAR(128),
    political_status VARCHAR(64),
    marital_status VARCHAR(32),
    religious_belief VARCHAR(128),
    id_type VARCHAR(64),
    mailing_address TEXT,
    emergency_contact_name VARCHAR(128),
    emergency_contact_phone VARCHAR(32),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_preferences (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    preference_order INTEGER NOT NULL,
    research_center_name VARCHAR(128) NOT NULL,
    advisor_name VARCHAR(128),
    is_optional BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_portal_application_preferences_order UNIQUE (application_id, preference_order),
    CONSTRAINT chk_portal_application_preferences_order CHECK (preference_order > 0)
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_education_experiences (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    sort_order INTEGER NOT NULL DEFAULT 1,
    education_stage VARCHAR(64) NOT NULL,
    start_month VARCHAR(16),
    end_month VARCHAR(16),
    school_name VARCHAR(255) NOT NULL,
    major_name VARCHAR(255),
    average_score VARCHAR(64),
    gpa VARCHAR(32),
    ranking VARCHAR(64),
    verifier_name VARCHAR(128),
    verifier_phone VARCHAR(32),
    transcript_attachment_url TEXT,
    degree_certificate_attachment_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_portal_application_education_sort_order CHECK (sort_order > 0)
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_practice_experiences (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    start_month VARCHAR(16),
    end_month VARCHAR(16),
    organization_name VARCHAR(255) NOT NULL,
    position_name VARCHAR(128),
    responsibility_text TEXT,
    verifier_name VARCHAR(128),
    verifier_phone VARCHAR(32),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_english_proficiencies (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    exam_name VARCHAR(32) NOT NULL,
    score_text VARCHAR(64) NOT NULL,
    certificate_attachment_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_family_members (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    member_name VARCHAR(64) NOT NULL,
    relation_type VARCHAR(16) NOT NULL,
    employer_name VARCHAR(255),
    job_title VARCHAR(128),
    contact_phone VARCHAR(32),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_achievement_records (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    achievement_type VARCHAR(32) NOT NULL,
    paper_title VARCHAR(255),
    author_order VARCHAR(32),
    journal_or_conference VARCHAR(255),
    publish_or_index_month VARCHAR(16),
    achievement_month VARCHAR(16),
    award_name VARCHAR(255),
    award_rank VARCHAR(64),
    award_certificate_attachment_url VARCHAR(512),
    awarding_organization VARCHAR(255),
    award_level VARCHAR(128),
    award_year VARCHAR(16),
    description_text TEXT,
    responsibility_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_personal_statements (
    application_id BIGINT PRIMARY KEY REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    personal_statement_text TEXT,
    growth_experience_text TEXT,
    program_application_reason_text TEXT,
    career_plan_text TEXT,
    ai_problem_statement TEXT,
    ai_industry_opinion TEXT,
    resume_attachment_url TEXT,
    supporting_material_attachment_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_declarations (
    application_id BIGINT PRIMARY KEY REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    has_read_declaration BOOLEAN NOT NULL DEFAULT FALSE,
    declaration_text TEXT,
    progress_snapshot JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_portal_application_attachments (
    id BIGSERIAL PRIMARY KEY,
    portal_student_id BIGINT REFERENCES dtlms_portal_students(id) ON DELETE CASCADE,
    application_id BIGINT REFERENCES dtlms_recruitment_applications(id) ON DELETE CASCADE,
    owner_type VARCHAR(64) NOT NULL,
    owner_id BIGINT,
    attachment_category VARCHAR(64) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    file_type VARCHAR(32),
    file_size BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_applications_portal_student
    ON dtlms_recruitment_applications (portal_student_id);

CREATE INDEX IF NOT EXISTS idx_portal_application_preferences_application
    ON dtlms_portal_application_preferences (application_id, preference_order);

CREATE INDEX IF NOT EXISTS idx_portal_application_education_application
    ON dtlms_portal_application_education_experiences (application_id, sort_order);

CREATE INDEX IF NOT EXISTS idx_portal_application_practice_application
    ON dtlms_portal_application_practice_experiences (application_id);

CREATE INDEX IF NOT EXISTS idx_portal_application_english_application
    ON dtlms_portal_application_english_proficiencies (application_id);

CREATE INDEX IF NOT EXISTS idx_portal_application_family_application
    ON dtlms_portal_application_family_members (application_id);

CREATE UNIQUE INDEX IF NOT EXISTS ux_portal_application_family_parent_unique
    ON dtlms_portal_application_family_members (application_id, relation_type)
    WHERE relation_type IN ('父亲', '母亲');

CREATE INDEX IF NOT EXISTS idx_portal_application_achievement_application
    ON dtlms_portal_application_achievement_records (application_id, achievement_type);

CREATE INDEX IF NOT EXISTS idx_portal_application_attachment_owner
    ON dtlms_portal_application_attachments (application_id, owner_type, owner_id);

UPDATE dtlms_recruitment_applications AS ra
SET portal_student_id = ps.id
FROM dtlms_portal_students AS ps
WHERE ra.portal_student_id IS NULL
  AND (
        (NULLIF(ra.id_number, '') IS NOT NULL AND ra.id_number = ps.id_number)
     OR (NULLIF(ra.phone_number, '') IS NOT NULL AND ra.phone_number = ps.phone_number)
     OR (NULLIF(ra.email, '') IS NOT NULL AND ra.email = ps.email)
  );

UPDATE dtlms_recruitment_applications
SET source_channel = discovery_channel
WHERE source_channel IS NULL
  AND NULLIF(discovery_channel, '') IS NOT NULL;

INSERT INTO dtlms_portal_student_profiles (
    portal_student_id,
    gender,
    birth_date,
    ethnic_group,
    native_place,
    political_status,
    marital_status,
    religious_belief,
    id_type,
    mailing_address,
    created_at,
    updated_at
)
SELECT
    ps.id,
    ps.gender,
    ps.birth_date,
    ps.ethnic_group,
    ps.native_place,
    ps.political_status,
    ps.marital_status,
    ps.religious_belief,
    ps.id_type,
    ps.mailing_address,
    ps.created_at,
    ps.updated_at
FROM dtlms_portal_students AS ps
ON CONFLICT (portal_student_id) DO UPDATE SET
    gender = EXCLUDED.gender,
    birth_date = EXCLUDED.birth_date,
    ethnic_group = EXCLUDED.ethnic_group,
    native_place = EXCLUDED.native_place,
    political_status = EXCLUDED.political_status,
    marital_status = EXCLUDED.marital_status,
    religious_belief = EXCLUDED.religious_belief,
    id_type = EXCLUDED.id_type,
    mailing_address = EXCLUDED.mailing_address,
    updated_at = EXCLUDED.updated_at;

INSERT INTO dtlms_portal_application_preferences (
    application_id,
    preference_order,
    research_center_name,
    advisor_name,
    is_optional,
    created_at,
    updated_at
)
SELECT
    ra.id,
    1,
    ra.first_choice,
    ra.intended_advisor_name,
    FALSE,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
WHERE NULLIF(ra.first_choice, '') IS NOT NULL
ON CONFLICT (application_id, preference_order) DO UPDATE SET
    research_center_name = EXCLUDED.research_center_name,
    advisor_name = EXCLUDED.advisor_name,
    is_optional = EXCLUDED.is_optional,
    updated_at = EXCLUDED.updated_at;

INSERT INTO dtlms_portal_application_preferences (
    application_id,
    preference_order,
    research_center_name,
    advisor_name,
    is_optional,
    created_at,
    updated_at
)
SELECT
    ra.id,
    2,
    ra.second_choice,
    NULL,
    TRUE,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
WHERE NULLIF(ra.second_choice, '') IS NOT NULL
ON CONFLICT (application_id, preference_order) DO UPDATE SET
    research_center_name = EXCLUDED.research_center_name,
    advisor_name = EXCLUDED.advisor_name,
    is_optional = EXCLUDED.is_optional,
    updated_at = EXCLUDED.updated_at;

INSERT INTO dtlms_portal_application_personal_statements (
    application_id,
    personal_statement_text,
    growth_experience_text,
    program_application_reason_text,
    career_plan_text,
    ai_problem_statement,
    ai_industry_opinion,
    resume_attachment_url,
    supporting_material_attachment_url,
    created_at,
    updated_at
)
SELECT
    ra.id,
    ra.personal_statement_text,
    ra.personal_statement_text,
    ra.research_problem,
    ra.dissenting_view,
    ra.research_problem,
    ra.dissenting_view,
    ra.personal_statement_attachment,
    ra.material_list_attachment,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
WHERE COALESCE(
        NULLIF(ra.personal_statement_text, ''),
        NULLIF(ra.research_problem, ''),
        NULLIF(ra.dissenting_view, ''),
        NULLIF(ra.personal_statement_attachment, ''),
        NULLIF(ra.material_list_attachment, '')
    ) IS NOT NULL
ON CONFLICT (application_id) DO UPDATE SET
    personal_statement_text = EXCLUDED.personal_statement_text,
    growth_experience_text = EXCLUDED.growth_experience_text,
    program_application_reason_text = EXCLUDED.program_application_reason_text,
    career_plan_text = EXCLUDED.career_plan_text,
    ai_problem_statement = EXCLUDED.ai_problem_statement,
    ai_industry_opinion = EXCLUDED.ai_industry_opinion,
    resume_attachment_url = EXCLUDED.resume_attachment_url,
    supporting_material_attachment_url = EXCLUDED.supporting_material_attachment_url,
    updated_at = EXCLUDED.updated_at;

INSERT INTO dtlms_portal_application_declarations (
    application_id,
    has_read_declaration,
    declaration_text,
    progress_snapshot,
    created_at,
    updated_at
)
SELECT
    ra.id,
    COALESCE(ps.signed_agreement, FALSE),
    NULL,
    NULL,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
LEFT JOIN dtlms_portal_students AS ps ON ps.id = ra.portal_student_id
ON CONFLICT (application_id) DO UPDATE SET
    has_read_declaration = EXCLUDED.has_read_declaration,
    updated_at = EXCLUDED.updated_at;

INSERT INTO dtlms_portal_application_attachments (
    portal_student_id,
    application_id,
    owner_type,
    owner_id,
    attachment_category,
    file_name,
    file_url,
    file_type,
    file_size,
    created_at,
    updated_at
)
SELECT
    ra.portal_student_id,
    ra.id,
    'personal_statement',
    ra.id,
    'resume',
    COALESCE(NULLIF(regexp_replace(ra.personal_statement_attachment, '^.*/', ''), ''), 'resume'),
    ra.personal_statement_attachment,
    NULL,
    NULL,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
WHERE NULLIF(ra.personal_statement_attachment, '') IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_portal_application_attachments AS pa
      WHERE pa.application_id = ra.id
        AND pa.attachment_category = 'resume'
        AND pa.file_url = ra.personal_statement_attachment
  );

INSERT INTO dtlms_portal_application_attachments (
    portal_student_id,
    application_id,
    owner_type,
    owner_id,
    attachment_category,
    file_name,
    file_url,
    file_type,
    file_size,
    created_at,
    updated_at
)
SELECT
    ra.portal_student_id,
    ra.id,
    'application',
    ra.id,
    'material_list',
    COALESCE(NULLIF(regexp_replace(ra.material_list_attachment, '^.*/', ''), ''), 'material_list'),
    ra.material_list_attachment,
    NULL,
    NULL,
    ra.created_at,
    ra.updated_at
FROM dtlms_recruitment_applications AS ra
WHERE NULLIF(ra.material_list_attachment, '') IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_portal_application_attachments AS pa
      WHERE pa.application_id = ra.id
        AND pa.attachment_category = 'material_list'
        AND pa.file_url = ra.material_list_attachment
  );

INSERT INTO dtlms_portal_application_attachments (
    portal_student_id,
    application_id,
    owner_type,
    owner_id,
    attachment_category,
    file_name,
    file_url,
    file_type,
    file_size,
    created_at,
    updated_at
)
SELECT
    ra.portal_student_id,
    am.application_id,
    'application_material',
    am.id,
    am.material_type,
    COALESCE(NULLIF(regexp_replace(am.file_url, '^.*/', ''), ''), am.material_type),
    am.file_url,
    NULL,
    NULL,
    am.created_at,
    am.updated_at
FROM dtlms_application_materials AS am
JOIN dtlms_recruitment_applications AS ra ON ra.id = am.application_id
WHERE NULLIF(am.file_url, '') IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_portal_application_attachments AS pa
      WHERE pa.application_id = am.application_id
        AND pa.owner_type = 'application_material'
        AND pa.owner_id = am.id
        AND pa.file_url = am.file_url
  );