-- prerequisite migrations folded into 058 so this script can be the only manual SQL entrypoint.

CREATE TABLE IF NOT EXISTS dtlms_teams (
  id BIGSERIAL PRIMARY KEY,
  team_code VARCHAR(32) NOT NULL UNIQUE,
  team_name VARCHAR(128) NOT NULL UNIQUE,
  department_name VARCHAR(128) NOT NULL DEFAULT '未分配院系',
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

ALTER TABLE dtlms_students
  ADD COLUMN IF NOT EXISTS team_id BIGINT REFERENCES dtlms_teams(id);

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

WITH distinct_team_names AS (
  SELECT DISTINCT BTRIM(s.team_name) AS team_name
  FROM dtlms_students AS s
  WHERE s.team_name IS NOT NULL
    AND BTRIM(s.team_name) <> ''
), missing_team_names AS (
  SELECT d.team_name
  FROM distinct_team_names AS d
  WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_teams AS t
    WHERE t.team_name = d.team_name
  )
)
INSERT INTO dtlms_teams (
  team_code,
  team_name,
  department_name,
  team_status,
  description
)
SELECT
  CONCAT('TEAM-', LPAD(ROW_NUMBER() OVER (ORDER BY m.team_name)::TEXT, 4, '0')),
  m.team_name,
  '未分配院系',
  'active',
  '由学生主档历史 team_name 迁移生成'
FROM missing_team_names AS m;

UPDATE dtlms_students AS s
SET team_id = t.id
FROM dtlms_teams AS t
WHERE s.team_id IS NULL
  AND s.team_name IS NOT NULL
  AND BTRIM(s.team_name) <> ''
  AND t.team_name = s.team_name;

INSERT INTO dtlms_student_team_history (
  student_id,
  team_id,
  start_date,
  change_reason
)
SELECT
  s.id,
  s.team_id,
  CURRENT_DATE,
  '初始化迁移自 dtlms_students.team_name'
FROM dtlms_students AS s
WHERE s.team_id IS NOT NULL
  AND NOT EXISTS (
    SELECT 1
    FROM dtlms_student_team_history AS h
    WHERE h.student_id = s.id
        AND h.team_id = s.team_id
  );

ALTER TABLE dtlms_recruitment_applications
  ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_scientific_reports
  ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_outbound_studies
  ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_theses
  ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

UPDATE dtlms_recruitment_applications
SET business_key = COALESCE(NULLIF(BTRIM(business_key), ''), candidate_no)
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_scientific_reports
SET business_key = CONCAT('KYBG-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_outbound_studies
SET business_key = CONCAT('WCYX-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_theses
SET business_key = CONCAT('LWZD-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

ALTER TABLE dtlms_recruitment_applications
  ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_scientific_reports
  ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_outbound_studies
  ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_theses
  ALTER COLUMN business_key SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_recruitment_applications_business_key
  ON dtlms_recruitment_applications (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_scientific_reports_business_key
  ON dtlms_scientific_reports (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_outbound_studies_business_key
  ON dtlms_outbound_studies (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_theses_business_key
  ON dtlms_theses (business_key);

CREATE TABLE IF NOT EXISTS dtlms_wf_de_model (
  id_ VARCHAR(64) PRIMARY KEY,
  name_ VARCHAR(255) NOT NULL,
  key_ VARCHAR(128) NOT NULL,
  category_ VARCHAR(128),
  version_ INTEGER NOT NULL DEFAULT 1,
  model_type_ INTEGER NOT NULL DEFAULT 0,
  description_ TEXT,
  meta_info_ JSONB,
  created_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_updated_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id_ VARCHAR(64),
  deployment_id_ VARCHAR(64),
  resource_name_ VARCHAR(255),
  editor_source_value_ TEXT,
  editor_source_extra_value_ JSONB
);

CREATE TABLE IF NOT EXISTS dtlms_wf_re_deployment (
  id_ VARCHAR(64) PRIMARY KEY,
  name_ VARCHAR(255) NOT NULL,
  category_ VARCHAR(128),
  key_ VARCHAR(128),
  deploy_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_re_procdef (
  id_ VARCHAR(64) PRIMARY KEY,
  key_ VARCHAR(128) NOT NULL,
  version_ INTEGER NOT NULL DEFAULT 1,
  deployment_id_ VARCHAR(64) REFERENCES dtlms_wf_re_deployment(id_),
  resource_name_ VARCHAR(255),
  diagram_resource_name_ VARCHAR(255),
  name_ VARCHAR(255) NOT NULL,
  category_ VARCHAR(128),
  description_ TEXT,
  suspension_state_ INTEGER NOT NULL DEFAULT 1,
  tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_execution (
  id_ VARCHAR(64) PRIMARY KEY,
  proc_inst_id_ VARCHAR(64) NOT NULL,
  proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
  business_key_ VARCHAR(64),
  parent_id_ VARCHAR(64),
  act_id_ VARCHAR(128),
  is_active_ BOOLEAN NOT NULL DEFAULT TRUE,
  is_concurrent_ BOOLEAN NOT NULL DEFAULT FALSE,
  is_scope_ BOOLEAN NOT NULL DEFAULT TRUE,
  start_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  start_user_id_ VARCHAR(64),
  super_exec_ VARCHAR(64),
  tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_task (
  id_ VARCHAR(64) PRIMARY KEY,
  exec_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_ru_execution(id_),
  proc_inst_id_ VARCHAR(64) NOT NULL,
  proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
  task_def_key_ VARCHAR(128),
  name_ VARCHAR(255) NOT NULL,
  business_key_ VARCHAR(64),
  assignee_ VARCHAR(64),
  owner_ VARCHAR(64),
  create_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_date_ TIMESTAMPTZ,
  claim_time_ TIMESTAMPTZ,
  priority_ INTEGER NOT NULL DEFAULT 50,
  suspension_state_ INTEGER NOT NULL DEFAULT 1,
  tenant_id_ VARCHAR(64),
  form_key_ VARCHAR(255),
  description_ TEXT
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_variable (
  id_ VARCHAR(128) PRIMARY KEY,
  exec_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_ru_execution(id_),
  proc_inst_id_ VARCHAR(64) NOT NULL,
  task_id_ VARCHAR(64),
  name_ VARCHAR(128) NOT NULL,
  var_type_ VARCHAR(32) NOT NULL,
  text_value_ TEXT,
  number_value_ BIGINT,
  json_value_ JSONB,
  create_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_identitylink (
  id_ BIGSERIAL PRIMARY KEY,
  task_id_ VARCHAR(64) NOT NULL,
  proc_inst_id_ VARCHAR(64),
  user_id_ VARCHAR(64),
  group_id_ VARCHAR(64),
  link_type_ VARCHAR(32) NOT NULL,
  created_at_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_procinst (
  id_ VARCHAR(64) PRIMARY KEY,
  proc_inst_id_ VARCHAR(64) NOT NULL UNIQUE,
  business_key_ VARCHAR(64),
  proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
  start_time_ TIMESTAMPTZ NOT NULL,
  end_time_ TIMESTAMPTZ,
  duration_ms_ BIGINT,
  start_user_id_ VARCHAR(64),
  end_act_id_ VARCHAR(128),
  delete_reason_ VARCHAR(255),
  start_act_id_ VARCHAR(128),
  state_ VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_taskinst (
  id_ VARCHAR(64) PRIMARY KEY,
  task_def_key_ VARCHAR(128),
  proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
  proc_inst_id_ VARCHAR(64) NOT NULL,
  exec_id_ VARCHAR(64),
  name_ VARCHAR(255) NOT NULL,
  business_key_ VARCHAR(64),
  assignee_ VARCHAR(64),
  owner_ VARCHAR(64),
  start_time_ TIMESTAMPTZ NOT NULL,
  claim_time_ TIMESTAMPTZ,
  end_time_ TIMESTAMPTZ,
  duration_ms_ BIGINT,
  due_date_ TIMESTAMPTZ,
  delete_reason_ VARCHAR(255),
  priority_ INTEGER NOT NULL DEFAULT 50,
  category_ VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_actinst (
  id_ VARCHAR(64) PRIMARY KEY,
  proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
  proc_inst_id_ VARCHAR(64) NOT NULL,
  exec_id_ VARCHAR(64),
  act_id_ VARCHAR(128) NOT NULL,
  act_name_ VARCHAR(255),
  act_type_ VARCHAR(64) NOT NULL,
  assignee_ VARCHAR(64),
  start_time_ TIMESTAMPTZ NOT NULL,
  end_time_ TIMESTAMPTZ,
  duration_ms_ BIGINT,
  business_key_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_varinst (
  id_ VARCHAR(128) PRIMARY KEY,
  proc_inst_id_ VARCHAR(64) NOT NULL,
  exec_id_ VARCHAR(64),
  task_id_ VARCHAR(64),
  name_ VARCHAR(128) NOT NULL,
  var_type_ VARCHAR(32) NOT NULL,
  text_value_ TEXT,
  number_value_ BIGINT,
  json_value_ JSONB,
  create_time_ TIMESTAMPTZ NOT NULL,
  last_updated_time_ TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dtlms_wf_re_procdef_key ON dtlms_wf_re_procdef (key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_execution_proc_inst ON dtlms_wf_ru_execution (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_task_proc_inst ON dtlms_wf_ru_task (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_task_business_key ON dtlms_wf_ru_task (business_key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_procinst_business_key ON dtlms_wf_hi_procinst (business_key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_taskinst_proc_inst ON dtlms_wf_hi_taskinst (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_actinst_proc_inst ON dtlms_wf_hi_actinst (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_varinst_proc_inst ON dtlms_wf_hi_varinst (proc_inst_id_);

ALTER TABLE dtlms_recruitment_applications
  ADD COLUMN IF NOT EXISTS review_round VARCHAR(64),
  ADD COLUMN IF NOT EXISTS first_choice VARCHAR(255),
  ADD COLUMN IF NOT EXISTS second_choice VARCHAR(255),
  ADD COLUMN IF NOT EXISTS political_status VARCHAR(64),
  ADD COLUMN IF NOT EXISTS marital_status VARCHAR(32),
  ADD COLUMN IF NOT EXISTS religious_belief VARCHAR(128),
  ADD COLUMN IF NOT EXISTS native_place VARCHAR(128),
  ADD COLUMN IF NOT EXISTS phone_number VARCHAR(64),
  ADD COLUMN IF NOT EXISTS email VARCHAR(255),
  ADD COLUMN IF NOT EXISTS mailing_address TEXT,
  ADD COLUMN IF NOT EXISTS id_type VARCHAR(64),
  ADD COLUMN IF NOT EXISTS id_number VARCHAR(128),
  ADD COLUMN IF NOT EXISTS undergraduate_school VARCHAR(255),
  ADD COLUMN IF NOT EXISTS accept_adjustment VARCHAR(16),
  ADD COLUMN IF NOT EXISTS undergraduate_average_score VARCHAR(64),
  ADD COLUMN IF NOT EXISTS undergraduate_gpa VARCHAR(64),
  ADD COLUMN IF NOT EXISTS undergraduate_rank VARCHAR(64),
  ADD COLUMN IF NOT EXISTS undergraduate_major VARCHAR(255),
  ADD COLUMN IF NOT EXISTS graduate_average_score VARCHAR(64),
  ADD COLUMN IF NOT EXISTS graduate_gpa VARCHAR(64),
  ADD COLUMN IF NOT EXISTS graduate_rank VARCHAR(64),
  ADD COLUMN IF NOT EXISTS graduate_major VARCHAR(255),
  ADD COLUMN IF NOT EXISTS intended_advisor_name VARCHAR(128),
  ADD COLUMN IF NOT EXISTS discovery_channel TEXT,
  ADD COLUMN IF NOT EXISTS graduate_school VARCHAR(255),
  ADD COLUMN IF NOT EXISTS overseas_university_name VARCHAR(255),
  ADD COLUMN IF NOT EXISTS overseas_master_university_name VARCHAR(255),
  ADD COLUMN IF NOT EXISTS self_evaluation TEXT,
  ADD COLUMN IF NOT EXISTS applied_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS research_problem TEXT,
  ADD COLUMN IF NOT EXISTS research_status_analysis TEXT,
  ADD COLUMN IF NOT EXISTS research_impact TEXT,
  ADD COLUMN IF NOT EXISTS ai_society_impact TEXT,
  ADD COLUMN IF NOT EXISTS dissenting_view TEXT,
  ADD COLUMN IF NOT EXISTS family_info TEXT,
  ADD COLUMN IF NOT EXISTS education_experience TEXT,
  ADD COLUMN IF NOT EXISTS practice_experience TEXT,
  ADD COLUMN IF NOT EXISTS personal_statement_text TEXT,
  ADD COLUMN IF NOT EXISTS student_activity_experience TEXT,
  ADD COLUMN IF NOT EXISTS personal_statement_attachment TEXT,
  ADD COLUMN IF NOT EXISTS material_list_attachment TEXT,
  ADD COLUMN IF NOT EXISTS supplementary_profile TEXT;

CREATE INDEX IF NOT EXISTS idx_dtlms_recruitment_applications_phone_number
  ON dtlms_recruitment_applications (phone_number);

CREATE INDEX IF NOT EXISTS idx_dtlms_recruitment_applications_email
  ON dtlms_recruitment_applications (email);

ALTER TABLE IF EXISTS dtlms_portal_students
  ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255),
  ADD COLUMN IF NOT EXISTS gender VARCHAR(16),
  ADD COLUMN IF NOT EXISTS birth_date VARCHAR(32),
  ADD COLUMN IF NOT EXISTS ethnic_group VARCHAR(64),
  ADD COLUMN IF NOT EXISTS native_place VARCHAR(128),
  ADD COLUMN IF NOT EXISTS marital_status VARCHAR(32),
  ADD COLUMN IF NOT EXISTS religious_belief VARCHAR(128),
  ADD COLUMN IF NOT EXISTS id_type VARCHAR(64),
  ADD COLUMN IF NOT EXISTS mailing_address TEXT,
  ADD COLUMN IF NOT EXISTS english_level VARCHAR(128),
  ADD COLUMN IF NOT EXISTS family_info TEXT,
  ADD COLUMN IF NOT EXISTS education_experience TEXT,
  ADD COLUMN IF NOT EXISTS practice_experience TEXT,
  ADD COLUMN IF NOT EXISTS personal_profile TEXT,
  ADD COLUMN IF NOT EXISTS recommendation_notes TEXT,
  ADD COLUMN IF NOT EXISTS personal_statement_text TEXT,
  ADD COLUMN IF NOT EXISTS signed_agreement BOOLEAN NOT NULL DEFAULT FALSE;

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
  graduation_certificate_attachment_url TEXT,
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

ALTER TABLE IF EXISTS dtlms_recruitment_plans
  ADD COLUMN IF NOT EXISTS plan_description TEXT;

ALTER TABLE IF EXISTS dtlms_portal_students
  ADD COLUMN IF NOT EXISTS account_status VARCHAR(32) NOT NULL DEFAULT '启用';

UPDATE dtlms_portal_students
SET account_status = '停用'
WHERE account_status = '已注销';

CREATE TABLE IF NOT EXISTS dtlms_dict_types (
  id BIGSERIAL PRIMARY KEY,
  dict_name VARCHAR(100) NOT NULL,
  dict_type VARCHAR(100) NOT NULL UNIQUE,
  status VARCHAR(32) NOT NULL DEFAULT '启用',
  remark TEXT,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (status IN ('启用', '停用'))
);

CREATE TABLE IF NOT EXISTS dtlms_dict_data (
  id BIGSERIAL PRIMARY KEY,
  dict_type_id BIGINT NOT NULL REFERENCES dtlms_dict_types(id),
  dict_type VARCHAR(100) NOT NULL,
  label VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(32) NOT NULL DEFAULT '启用',
  color_type VARCHAR(32),
  css_class VARCHAR(128),
  remark TEXT,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (dict_type, value),
  CHECK (status IN ('启用', '停用'))
);

CREATE INDEX IF NOT EXISTS idx_dtlms_dict_data_type_sort ON dtlms_dict_data(dict_type, sort_order, id);

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES
  ('账号状态', 'system_account_status', '启用', '系统账号状态字典'),
  ('角色范围', 'system_role_scope', '启用', '系统角色范围字典'),
  ('集成方向', 'system_integration_direction', '启用', '系统集成方向字典'),
  ('集成频率', 'system_integration_cadence', '启用', '系统集成频率字典'),
  ('集成状态', 'system_integration_status', '启用', '系统集成状态字典'),
  ('审计策略状态', 'system_audit_status', '启用', '审计策略状态字典'),
  ('操作结果', 'system_operation_result', '启用', '操作日志结果字典'),
  ('同步状态', 'system_sync_status', '启用', '同步日志状态字典'),
  ('学生状态', 'student_status', '启用', '学生生命周期状态字典'),
  ('学位类型', 'student_degree_type', '启用', '博士类型字典'),
  ('团队状态', 'student_team_status', '启用', '团队状态字典'),
  ('民族', 'student_ethnic_group', '启用', '学生民族字典'),
  ('政治面貌', 'student_political_status', '启用', '学生政治面貌字典'),
  ('招生学期', 'recruitment_semester', '启用', '招生学期字典'),
  ('招生计划阶段', 'recruitment_plan_stage', '启用', '招生计划阶段字典'),
  ('报考学历', 'recruitment_degree', '启用', '招生学历字典'),
  ('材料状态', 'recruitment_material_status', '启用', '材料状态字典'),
  ('申请状态', 'recruitment_application_status', '启用', '申请状态字典'),
  ('培养方案状态', 'training_plan_status', '启用', '培养方案状态字典'),
  ('科研报告周期', 'training_report_cycle', '启用', '科研报告周期字典'),
  ('科研报告状态', 'training_report_status', '启用', '科研报告状态字典'),
  ('外出研修类型', 'training_outbound_study_type', '启用', '外出研修类型字典'),
  ('外出研修审批状态', 'training_outbound_approval_status', '启用', '外出研修审批状态字典'),
  ('论文状态', 'degree_thesis_status', '启用', '论文流程状态字典'),
  ('盲审状态', 'degree_blind_review_status', '启用', '盲审状态字典'),
  ('答辩状态', 'degree_defense_status', '启用', '答辩状态字典'),
  ('授位状态', 'degree_status', '启用', '授位状态字典'),
  ('评审状态', 'degree_review_status', '启用', '评审状态字典'),
  ('流程优先级', 'workflow_priority', '启用', '审批优先级字典'),
  ('流程状态', 'workflow_status', '启用', '审批状态字典')
ON CONFLICT (dict_type) DO UPDATE SET
  dict_name = EXCLUDED.dict_name,
  status = EXCLUDED.status,
  remark = EXCLUDED.remark,
  updated_at = CURRENT_TIMESTAMP;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
  VALUES
    ('system_account_status', '启用', '启用', 10, '启用', 'success', NULL, NULL),
    ('system_account_status', '停用', '停用', 20, '启用', 'info', NULL, NULL),
    ('system_account_status', '锁定', '锁定', 30, '启用', 'danger', NULL, NULL),
    ('system_role_scope', '系统治理', '系统治理', 10, '启用', NULL, NULL, NULL),
    ('system_role_scope', '招生管理', '招生管理', 20, '启用', NULL, NULL, NULL),
    ('system_role_scope', '学生管理', '学生管理', 30, '启用', NULL, NULL, NULL),
    ('system_role_scope', '培养与学位', '培养与学位', 40, '启用', NULL, NULL, NULL),
    ('system_role_scope', '学位管理', '学位管理', 50, '启用', NULL, NULL, NULL),
    ('system_role_scope', '跨部门协同', '跨部门协同', 60, '启用', NULL, NULL, NULL),
    ('system_integration_direction', '主数据导入 / 录取回传', '主数据导入 / 录取回传', 10, '启用', NULL, NULL, NULL),
    ('system_integration_direction', '考勤 / 门禁 / 请假同步', '考勤 / 门禁 / 请假同步', 20, '启用', NULL, NULL, NULL),
    ('system_integration_direction', '待办通知 / 审批提醒 / 回执', '待办通知 / 审批提醒 / 回执', 30, '启用', NULL, NULL, NULL),
    ('system_integration_direction', '双向同步', '双向同步', 40, '启用', NULL, NULL, NULL),
    ('system_integration_direction', '主数据下发', '主数据下发', 50, '启用', NULL, NULL, NULL),
    ('system_integration_cadence', '实时', '实时', 10, '启用', NULL, NULL, NULL),
    ('system_integration_cadence', '实时 + 每日对账', '实时 + 每日对账', 20, '启用', NULL, NULL, NULL),
    ('system_integration_cadence', '实时事件 + 定时补偿', '实时事件 + 定时补偿', 30, '启用', NULL, NULL, NULL),
    ('system_integration_cadence', '每小时', '每小时', 40, '启用', NULL, NULL, NULL),
    ('system_integration_cadence', '每日', '每日', 50, '启用', NULL, NULL, NULL),
    ('system_integration_status', '正常', '正常', 10, '启用', 'success', NULL, NULL),
    ('system_integration_status', '告警', '告警', 20, '启用', 'warning', NULL, NULL),
    ('system_integration_status', '停用', '停用', 30, '启用', 'info', NULL, NULL),
    ('system_audit_status', '启用', '启用', 10, '启用', 'success', NULL, NULL),
    ('system_audit_status', '停用', '停用', 20, '启用', 'info', NULL, NULL),
    ('system_operation_result', '成功', 'success', 10, '启用', 'success', NULL, NULL),
    ('system_operation_result', '失败', 'failed', 20, '启用', 'danger', NULL, NULL),
    ('system_sync_status', '成功', 'success', 10, '启用', 'success', NULL, NULL),
    ('system_sync_status', '失败', 'failed', 20, '启用', 'danger', NULL, NULL),
    ('student_status', '在校', '在校', 10, '启用', 'success', NULL, NULL),
    ('student_status', '实习中', '实习中', 20, '启用', 'warning', NULL, NULL),
    ('student_status', '外出研修', '外出研修', 30, '启用', 'warning', NULL, NULL),
    ('student_status', '请假中', '请假中', 40, '启用', 'danger', NULL, NULL),
    ('student_status', '学位论文阶段', '学位论文阶段', 50, '启用', 'success', NULL, NULL),
    ('student_status', '已毕业', '已毕业', 60, '启用', 'info', NULL, NULL),
    ('student_degree_type', '工程博士', '工程博士', 10, '启用', NULL, NULL, NULL),
    ('student_degree_type', '学术博士', '学术博士', 20, '启用', NULL, NULL, NULL),
    ('student_team_status', '启用', '启用', 10, '启用', 'success', NULL, NULL),
    ('student_team_status', '筹建', '筹建', 20, '启用', 'warning', NULL, NULL),
    ('student_team_status', '停用', '停用', 30, '启用', 'info', NULL, NULL),
    ('student_ethnic_group', '汉族', '汉族', 10, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '蒙古族', '蒙古族', 20, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '回族', '回族', 30, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '藏族', '藏族', 40, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '维吾尔族', '维吾尔族', 50, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '苗族', '苗族', 60, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '彝族', '彝族', 70, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '壮族', '壮族', 80, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '布依族', '布依族', 90, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '朝鲜族', '朝鲜族', 100, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '满族', '满族', 110, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '侗族', '侗族', 120, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '瑶族', '瑶族', 130, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '白族', '白族', 140, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '土家族', '土家族', 150, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '哈尼族', '哈尼族', 160, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '哈萨克族', '哈萨克族', 170, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '傣族', '傣族', 180, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '黎族', '黎族', 190, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '傈僳族', '傈僳族', 200, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '佤族', '佤族', 210, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '畲族', '畲族', 220, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '高山族', '高山族', 230, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '拉祜族', '拉祜族', 240, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '水族', '水族', 250, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '东乡族', '东乡族', 260, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '纳西族', '纳西族', 270, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '景颇族', '景颇族', 280, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '柯尔克孜族', '柯尔克孜族', 290, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '土族', '土族', 300, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '达斡尔族', '达斡尔族', 310, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '仫佬族', '仫佬族', 320, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '羌族', '羌族', 330, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '布朗族', '布朗族', 340, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '撒拉族', '撒拉族', 350, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '毛南族', '毛南族', 360, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '仡佬族', '仡佬族', 370, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '锡伯族', '锡伯族', 380, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '阿昌族', '阿昌族', 390, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '普米族', '普米族', 400, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '塔吉克族', '塔吉克族', 410, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '怒族', '怒族', 420, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '乌孜别克族', '乌孜别克族', 430, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '俄罗斯族', '俄罗斯族', 440, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '鄂温克族', '鄂温克族', 450, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '德昂族', '德昂族', 460, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '保安族', '保安族', 470, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '裕固族', '裕固族', 480, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '京族', '京族', 490, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '塔塔尔族', '塔塔尔族', 500, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '独龙族', '独龙族', 510, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '鄂伦春族', '鄂伦春族', 520, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '赫哲族', '赫哲族', 530, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '门巴族', '门巴族', 540, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '珞巴族', '珞巴族', 550, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '基诺族', '基诺族', 560, '启用', NULL, NULL, NULL),
    ('student_political_status', '中共党员', '中共党员', 10, '启用', NULL, NULL, NULL),
    ('student_political_status', '中共预备党员', '中共预备党员', 20, '启用', NULL, NULL, NULL),
    ('student_political_status', '共青团员', '共青团员', 30, '启用', NULL, NULL, NULL),
    ('student_political_status', '民革党员', '民革党员', 40, '启用', NULL, NULL, NULL),
    ('student_political_status', '民盟盟员', '民盟盟员', 50, '启用', NULL, NULL, NULL),
    ('student_political_status', '民建会员', '民建会员', 60, '启用', NULL, NULL, NULL),
    ('student_political_status', '民进会员', '民进会员', 70, '启用', NULL, NULL, NULL),
    ('student_political_status', '农工党党员', '农工党党员', 80, '启用', NULL, NULL, NULL),
    ('student_political_status', '致公党党员', '致公党党员', 90, '启用', NULL, NULL, NULL),
    ('student_political_status', '九三学社社员', '九三学社社员', 100, '启用', NULL, NULL, NULL),
    ('student_political_status', '台盟盟员', '台盟盟员', 110, '启用', NULL, NULL, NULL),
    ('student_political_status', '无党派人士', '无党派人士', 120, '启用', NULL, NULL, NULL),
    ('student_political_status', '群众', '群众', 130, '启用', NULL, NULL, NULL),
    ('recruitment_semester', '春', '春', 10, '启用', NULL, NULL, NULL),
    ('recruitment_semester', '秋', '秋', 20, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '报名配置', '报名配置', 10, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '资格审核', '资格审核', 20, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '评分推荐', '评分推荐', 30, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '材料评分', '材料评分', 40, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '面试执行', '面试执行', 50, '启用', NULL, NULL, NULL),
    ('recruitment_plan_stage', '预录取', '预录取', 60, '启用', NULL, NULL, NULL),
    ('recruitment_degree', '本科', '本科', 10, '启用', NULL, NULL, NULL),
    ('recruitment_degree', '硕士', '硕士', 20, '启用', NULL, NULL, NULL),
    ('recruitment_degree', '博士', '博士', 30, '启用', NULL, NULL, NULL),
    ('recruitment_material_status', '材料齐全', '材料齐全', 10, '启用', 'success', NULL, NULL),
    ('recruitment_material_status', '待补材料', '待补材料', 20, '启用', 'warning', NULL, NULL),
    ('recruitment_material_status', '已退回修改', '已退回修改', 30, '启用', 'danger', NULL, NULL),
    ('recruitment_application_status', '报名已提交', '报名已提交', 10, '启用', 'info', NULL, NULL),
    ('recruitment_application_status', '资格审核通过', '资格审核通过', 20, '启用', 'warning', NULL, NULL),
    ('recruitment_application_status', '材料评分中', '材料评分中', 30, '启用', 'warning', NULL, NULL),
    ('recruitment_application_status', '面试待安排', '面试待安排', 40, '启用', 'warning', NULL, NULL),
    ('recruitment_application_status', '面试完成', '面试完成', 50, '启用', 'warning', NULL, NULL),
    ('recruitment_application_status', '预录取', '预录取', 60, '启用', 'success', NULL, NULL),
    ('recruitment_application_status', '同意录取', '同意录取', 70, '启用', 'success', NULL, NULL),
    ('recruitment_application_status', '不录取', '不录取', 80, '启用', 'danger', NULL, NULL),
    ('training_plan_status', '待学生确认', '待学生确认', 10, '启用', 'warning', NULL, NULL),
    ('training_plan_status', '执行中', '执行中', 20, '启用', 'success', NULL, NULL),
    ('training_plan_status', '已归档', '已归档', 30, '启用', 'info', NULL, NULL),
    ('training_report_cycle', '月度', '月度', 10, '启用', NULL, NULL, NULL),
    ('training_report_cycle', '双月', '双月', 20, '启用', NULL, NULL, NULL),
    ('training_report_cycle', '季度', '季度', 30, '启用', NULL, NULL, NULL),
    ('training_report_cycle', '半年度', '半年度', 40, '启用', NULL, NULL, NULL),
    ('training_report_status', '待导师审阅', '待导师审阅', 10, '启用', 'warning', NULL, NULL),
    ('training_report_status', '已通过', '已通过', 20, '启用', 'success', NULL, NULL),
    ('training_report_status', '退回修改', '退回修改', 30, '启用', 'danger', NULL, NULL),
    ('training_outbound_study_type', '联合培养', '联合培养', 10, '启用', NULL, NULL, NULL),
    ('training_outbound_study_type', '企业研修', '企业研修', 20, '启用', NULL, NULL, NULL),
    ('training_outbound_study_type', '访学交流', '访学交流', 30, '启用', NULL, NULL, NULL),
    ('training_outbound_study_type', '学术会议', '学术会议', 40, '启用', NULL, NULL, NULL),
    ('training_outbound_approval_status', '审批中', '审批中', 10, '启用', 'warning', NULL, NULL),
    ('training_outbound_approval_status', '已批准', '已批准', 20, '启用', 'success', NULL, NULL),
    ('training_outbound_approval_status', '研修中', '研修中', 30, '启用', 'success', NULL, NULL),
    ('training_outbound_approval_status', '已结束', '已结束', 40, '启用', 'info', NULL, NULL),
    ('training_outbound_approval_status', '已驳回', '已驳回', 50, '启用', 'danger', NULL, NULL),
    ('degree_thesis_status', '待查重', '待查重', 10, '启用', 'warning', NULL, NULL),
    ('degree_thesis_status', '查重中', '查重中', 20, '启用', 'warning', NULL, NULL),
    ('degree_thesis_status', '查重通过', '查重通过', 30, '启用', 'success', NULL, NULL),
    ('degree_thesis_status', '退回修改', '退回修改', 40, '启用', 'danger', NULL, NULL),
    ('degree_thesis_status', '盲审通过', '盲审通过', 50, '启用', 'success', NULL, NULL),
    ('degree_blind_review_status', '待送审', '待送审', 10, '启用', 'warning', NULL, NULL),
    ('degree_blind_review_status', '未送审', '未送审', 20, '启用', 'info', NULL, NULL),
    ('degree_blind_review_status', '进行中', '进行中', 30, '启用', 'warning', NULL, NULL),
    ('degree_blind_review_status', '已通过', '已通过', 40, '启用', 'success', NULL, NULL),
    ('degree_blind_review_status', '未通过', '未通过', 50, '启用', 'danger', NULL, NULL),
    ('degree_defense_status', '未进入', '未进入', 10, '启用', 'info', NULL, NULL),
    ('degree_defense_status', '待安排', '待安排', 20, '启用', 'warning', NULL, NULL),
    ('degree_defense_status', '预答辩完成', '预答辩完成', 30, '启用', 'success', NULL, NULL),
    ('degree_defense_status', '正式答辩完成', '正式答辩完成', 40, '启用', 'success', NULL, NULL),
    ('degree_status', '待申请', '待申请', 10, '启用', 'info', NULL, NULL),
    ('degree_status', '未授位', '未授位', 20, '启用', 'danger', NULL, NULL),
    ('degree_status', '授位审批中', '授位审批中', 30, '启用', 'warning', NULL, NULL),
    ('degree_status', '待正式答辩', '待正式答辩', 40, '启用', 'warning', NULL, NULL),
    ('degree_status', '已授位', '已授位', 50, '启用', 'success', NULL, NULL),
    ('degree_review_status', '待反馈', '待反馈', 10, '启用', 'warning', NULL, NULL),
    ('degree_review_status', '已提交', '已提交', 20, '启用', 'info', NULL, NULL),
    ('degree_review_status', '已通过', '已通过', 30, '启用', 'success', NULL, NULL),
    ('degree_review_status', '需修改', '需修改', 40, '启用', 'danger', NULL, NULL),
    ('workflow_priority', '高', '高', 10, '启用', 'danger', NULL, NULL),
    ('workflow_priority', '中', '中', 20, '启用', 'warning', NULL, NULL),
    ('workflow_priority', '低', '低', 30, '启用', 'info', NULL, NULL),
    ('workflow_status', '待处理', '待处理', 10, '启用', 'warning', NULL, NULL),
    ('workflow_status', '处理中', '处理中', 20, '启用', 'warning', NULL, NULL),
    ('workflow_status', '已通过', '已通过', 30, '启用', 'success', NULL, NULL),
    ('workflow_status', '已驳回', '已驳回', 40, '启用', 'danger', NULL, NULL)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
  label = EXCLUDED.label,
  sort_order = EXCLUDED.sort_order,
  status = EXCLUDED.status,
  color_type = EXCLUDED.color_type,
  css_class = EXCLUDED.css_class,
  remark = EXCLUDED.remark,
  dict_type_id = EXCLUDED.dict_type_id,
  updated_at = CURRENT_TIMESTAMP;

ALTER TABLE IF EXISTS dtlms_portal_student_profiles
  ADD COLUMN IF NOT EXISTS profile_photo_url VARCHAR(255);

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES
  ('民族', 'student_ethnic_group', '启用', '学生民族字典')
ON CONFLICT (dict_type) DO UPDATE SET
  dict_name = EXCLUDED.dict_name,
  status = EXCLUDED.status,
  remark = EXCLUDED.remark,
  updated_at = CURRENT_TIMESTAMP;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
  VALUES
    ('student_ethnic_group', '汉族', '汉族', 10, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '蒙古族', '蒙古族', 20, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '回族', '回族', 30, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '藏族', '藏族', 40, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '维吾尔族', '维吾尔族', 50, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '苗族', '苗族', 60, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '彝族', '彝族', 70, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '壮族', '壮族', 80, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '布依族', '布依族', 90, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '朝鲜族', '朝鲜族', 100, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '满族', '满族', 110, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '侗族', '侗族', 120, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '瑶族', '瑶族', 130, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '白族', '白族', 140, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '土家族', '土家族', 150, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '哈尼族', '哈尼族', 160, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '哈萨克族', '哈萨克族', 170, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '傣族', '傣族', 180, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '黎族', '黎族', 190, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '傈僳族', '傈僳族', 200, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '佤族', '佤族', 210, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '畲族', '畲族', 220, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '高山族', '高山族', 230, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '拉祜族', '拉祜族', 240, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '水族', '水族', 250, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '东乡族', '东乡族', 260, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '纳西族', '纳西族', 270, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '景颇族', '景颇族', 280, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '柯尔克孜族', '柯尔克孜族', 290, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '土族', '土族', 300, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '达斡尔族', '达斡尔族', 310, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '仫佬族', '仫佬族', 320, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '羌族', '羌族', 330, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '布朗族', '布朗族', 340, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '撒拉族', '撒拉族', 350, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '毛南族', '毛南族', 360, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '仡佬族', '仡佬族', 370, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '锡伯族', '锡伯族', 380, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '阿昌族', '阿昌族', 390, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '普米族', '普米族', 400, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '塔吉克族', '塔吉克族', 410, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '怒族', '怒族', 420, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '乌孜别克族', '乌孜别克族', 430, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '俄罗斯族', '俄罗斯族', 440, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '鄂温克族', '鄂温克族', 450, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '德昂族', '德昂族', 460, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '保安族', '保安族', 470, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '裕固族', '裕固族', 480, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '京族', '京族', 490, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '塔塔尔族', '塔塔尔族', 500, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '独龙族', '独龙族', 510, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '鄂伦春族', '鄂伦春族', 520, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '赫哲族', '赫哲族', 530, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '门巴族', '门巴族', 540, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '珞巴族', '珞巴族', 550, '启用', NULL, NULL, NULL),
    ('student_ethnic_group', '基诺族', '基诺族', 560, '启用', NULL, NULL, NULL),
    ('student_political_status', '民革党员', '民革党员', 40, '启用', NULL, NULL, NULL),
    ('student_political_status', '民盟盟员', '民盟盟员', 50, '启用', NULL, NULL, NULL),
    ('student_political_status', '民建会员', '民建会员', 60, '启用', NULL, NULL, NULL),
    ('student_political_status', '民进会员', '民进会员', 70, '启用', NULL, NULL, NULL),
    ('student_political_status', '农工党党员', '农工党党员', 80, '启用', NULL, NULL, NULL),
    ('student_political_status', '致公党党员', '致公党党员', 90, '启用', NULL, NULL, NULL),
    ('student_political_status', '九三学社社员', '九三学社社员', 100, '启用', NULL, NULL, NULL),
    ('student_political_status', '台盟盟员', '台盟盟员', 110, '启用', NULL, NULL, NULL),
    ('student_political_status', '无党派人士', '无党派人士', 120, '启用', NULL, NULL, NULL),
    ('student_political_status', '群众', '群众', 130, '启用', NULL, NULL, NULL)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
  label = EXCLUDED.label,
  sort_order = EXCLUDED.sort_order,
  status = EXCLUDED.status,
  color_type = EXCLUDED.color_type,
  css_class = EXCLUDED.css_class,
  remark = EXCLUDED.remark,
  dict_type_id = EXCLUDED.dict_type_id,
  updated_at = CURRENT_TIMESTAMP;

CREATE TABLE IF NOT EXISTS dtlms_user_profiles (
  username VARCHAR(64) PRIMARY KEY REFERENCES dtlms_users(username) ON DELETE CASCADE,
  full_name VARCHAR(128) NOT NULL,
  role_name VARCHAR(128) NOT NULL,
  department_name VARCHAR(128) NOT NULL,
  phone_number VARCHAR(32),
  email VARCHAR(128),
  theme_color VARCHAR(32) NOT NULL DEFAULT '#0f4cbd',
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS dtlms_portal_student_profiles
  ADD COLUMN IF NOT EXISTS id_card_collage_url VARCHAR(255);

UPDATE dtlms_portal_student_profiles
SET id_card_collage_url = NULLIF(id_card_collage_url, '')
WHERE id_card_collage_url = '';

ALTER TABLE IF EXISTS dtlms_portal_application_achievement_records
  ADD COLUMN IF NOT EXISTS achievement_month VARCHAR(16),
  ADD COLUMN IF NOT EXISTS award_rank VARCHAR(64),
  ADD COLUMN IF NOT EXISTS award_certificate_attachment_url VARCHAR(512),
  ADD COLUMN IF NOT EXISTS description_text TEXT;

ALTER TABLE dtlms_portal_application_personal_statements
  ADD COLUMN IF NOT EXISTS growth_experience_text TEXT,
  ADD COLUMN IF NOT EXISTS program_application_reason_text TEXT,
  ADD COLUMN IF NOT EXISTS career_plan_text TEXT,
  ADD COLUMN IF NOT EXISTS supporting_material_attachment_url TEXT;

UPDATE dtlms_portal_application_personal_statements
SET growth_experience_text = COALESCE(NULLIF(growth_experience_text, ''), NULLIF(personal_statement_text, '')),
  program_application_reason_text = COALESCE(NULLIF(program_application_reason_text, ''), NULLIF(ai_problem_statement, '')),
  career_plan_text = COALESCE(NULLIF(career_plan_text, ''), NULLIF(ai_industry_opinion, '')),
  supporting_material_attachment_url = COALESCE(
    NULLIF(supporting_material_attachment_url, ''),
    (
      SELECT NULLIF(ra.material_list_attachment, '')
      FROM dtlms_recruitment_applications AS ra
      WHERE ra.id = dtlms_portal_application_personal_statements.application_id
    )
  )
WHERE growth_experience_text IS NULL
   OR growth_experience_text = ''
   OR program_application_reason_text IS NULL
   OR program_application_reason_text = ''
   OR career_plan_text IS NULL
   OR career_plan_text = ''
   OR supporting_material_attachment_url IS NULL
   OR supporting_material_attachment_url = '';

UPDATE dtlms_portal_application_personal_statements
SET personal_statement_text = CONCAT_WS(
    E'\n\n',
    CASE WHEN NULLIF(growth_experience_text, '') IS NOT NULL THEN '个人成长经历：' || growth_experience_text END,
    CASE WHEN NULLIF(program_application_reason_text, '') IS NOT NULL THEN '为何申报本项目或本专业：' || program_application_reason_text END,
    CASE WHEN NULLIF(career_plan_text, '') IS NOT NULL THEN '未来职业发展规划：' || career_plan_text END
  )
WHERE COALESCE(NULLIF(personal_statement_text, ''), '') = ''
  AND (
    NULLIF(growth_experience_text, '') IS NOT NULL
    OR NULLIF(program_application_reason_text, '') IS NOT NULL
    OR NULLIF(career_plan_text, '') IS NOT NULL
  );

ALTER TABLE IF EXISTS dtlms_portal_application_education_experiences
  ADD COLUMN IF NOT EXISTS graduation_certificate_attachment_url TEXT;

ALTER TABLE IF EXISTS dtlms_advisors
  ADD COLUMN IF NOT EXISTS user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_teams
  ADD COLUMN IF NOT EXISTS lead_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_team_advisors
  ADD COLUMN IF NOT EXISTS advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_portal_students
  ADD COLUMN IF NOT EXISTS selected_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS selected_advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_recruitment_applications
  ADD COLUMN IF NOT EXISTS first_choice_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS second_choice_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS intended_advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_portal_application_preferences
  ADD COLUMN IF NOT EXISTS team_id BIGINT,
  ADD COLUMN IF NOT EXISTS advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_students
  ADD COLUMN IF NOT EXISTS portal_student_id BIGINT;

DO $$
BEGIN
  IF to_regclass('public.dtlms_advisors') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_advisors_user_id'
       AND conrelid = 'dtlms_advisors'::regclass
     ) THEN
    ALTER TABLE dtlms_advisors
      ADD CONSTRAINT fk_dtlms_advisors_user_id
      FOREIGN KEY (user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_teams') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_teams_lead_user_id'
       AND conrelid = 'dtlms_teams'::regclass
     ) THEN
    ALTER TABLE dtlms_teams
      ADD CONSTRAINT fk_dtlms_teams_lead_user_id
      FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_team_advisors') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_team_advisors_advisor_user_id'
       AND conrelid = 'dtlms_team_advisors'::regclass
     ) THEN
    ALTER TABLE dtlms_team_advisors
      ADD CONSTRAINT fk_dtlms_team_advisors_advisor_user_id
      FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_students_selected_team_id'
       AND conrelid = 'dtlms_portal_students'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_students
      ADD CONSTRAINT fk_dtlms_portal_students_selected_team_id
      FOREIGN KEY (selected_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_students_selected_advisor_user_id'
       AND conrelid = 'dtlms_portal_students'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_students
      ADD CONSTRAINT fk_dtlms_portal_students_selected_advisor_user_id
      FOREIGN KEY (selected_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_first_choice_team_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_first_choice_team_id
      FOREIGN KEY (first_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_second_choice_team_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_second_choice_team_id
      FOREIGN KEY (second_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_intended_advisor_user_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_intended_advisor_user_id
      FOREIGN KEY (intended_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_application_preferences') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_application_preferences_team_id'
       AND conrelid = 'dtlms_portal_application_preferences'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_application_preferences
      ADD CONSTRAINT fk_dtlms_portal_application_preferences_team_id
      FOREIGN KEY (team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_application_preferences') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_application_preferences_advisor_user_id'
       AND conrelid = 'dtlms_portal_application_preferences'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_application_preferences
      ADD CONSTRAINT fk_dtlms_portal_application_preferences_advisor_user_id
      FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_students_portal_student_id'
       AND conrelid = 'dtlms_students'::regclass
     ) THEN
    ALTER TABLE dtlms_students
      ADD CONSTRAINT fk_dtlms_students_portal_student_id
      FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) NOT VALID;
  END IF;
END $$;

WITH portal_student_candidates AS (
    SELECT
        s.id AS student_id,
        ps.id AS portal_student_id,
        ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY ps.id DESC) AS student_pick,
        ROW_NUMBER() OVER (PARTITION BY ps.id ORDER BY s.id DESC) AS portal_pick
    FROM dtlms_students AS s
    JOIN dtlms_portal_students AS ps
      ON (
        BTRIM(COALESCE(s.full_name, '')) <> ''
        AND BTRIM(COALESCE(s.full_name, '')) = BTRIM(COALESCE(ps.full_name, ''))
        AND BTRIM(COALESCE(s.phone_number, '')) <> ''
        AND BTRIM(COALESCE(s.phone_number, '')) = BTRIM(COALESCE(ps.phone_number, ''))
      )
    WHERE s.portal_student_id IS NULL
      AND COALESCE(s.is_deleted, FALSE) = FALSE
), portal_student_matches AS (
    SELECT student_id, portal_student_id
    FROM portal_student_candidates
    WHERE student_pick = 1 AND portal_pick = 1
)
UPDATE dtlms_students AS s
SET portal_student_id = m.portal_student_id,
    updated_at = CURRENT_TIMESTAMP
FROM portal_student_matches AS m
WHERE s.id = m.student_id
  AND s.portal_student_id IS DISTINCT FROM m.portal_student_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_advisors_user_id
    ON dtlms_advisors(user_id)
    WHERE user_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_team_advisors_team_user
    ON dtlms_team_advisors(team_id, advisor_user_id)
    WHERE advisor_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_teams_lead_user_id
    ON dtlms_teams(lead_user_id)
    WHERE lead_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_portal_students_selected_team_id
    ON dtlms_portal_students(selected_team_id)
    WHERE selected_team_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_recruitment_applications_first_choice_team_id
    ON dtlms_recruitment_applications(first_choice_team_id)
    WHERE first_choice_team_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_portal_application_preferences_team_id
    ON dtlms_portal_application_preferences(team_id)
    WHERE team_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_students_portal_student_id
  ON dtlms_students(portal_student_id)
  WHERE portal_student_id IS NOT NULL;

WITH advisor_role_users AS (
    SELECT
        u.id AS user_id,
        u.full_name,
        ROW_NUMBER() OVER (PARTITION BY u.full_name ORDER BY u.id) AS row_num,
        COUNT(*) OVER (PARTITION BY u.full_name) AS same_name_count
    FROM dtlms_users u
    JOIN dtlms_user_roles ur ON ur.user_id = u.id
    JOIN dtlms_roles r ON r.id = ur.role_id
    WHERE u.is_deleted = FALSE
      AND u.is_active = TRUE
      AND r.is_deleted = FALSE
      AND r.role_code = 'advisor'
), unique_advisor_role_users AS (
    SELECT user_id, full_name
    FROM advisor_role_users
    WHERE row_num = 1 AND same_name_count = 1
)
UPDATE dtlms_advisors AS advisor
SET user_id = mapping.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM unique_advisor_role_users AS mapping
WHERE advisor.is_deleted = FALSE
  AND advisor.user_id IS NULL
  AND advisor.full_name = mapping.full_name;

UPDATE dtlms_teams AS team
SET lead_user_id = advisor.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_advisors AS advisor
WHERE team.is_deleted = FALSE
  AND team.lead_advisor_id = advisor.id
  AND advisor.user_id IS NOT NULL
  AND team.lead_user_id IS DISTINCT FROM advisor.user_id;

UPDATE dtlms_team_advisors AS relation
SET advisor_user_id = advisor.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_advisors AS advisor
WHERE relation.advisor_id = advisor.id
  AND advisor.user_id IS NOT NULL
  AND relation.advisor_user_id IS DISTINCT FROM advisor.user_id;

UPDATE dtlms_portal_students AS student
SET selected_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(student.selected_team_name, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(student.selected_team_name)
  AND student.selected_team_id IS DISTINCT FROM team.id;

WITH portal_student_advisor_choice AS (
    SELECT DISTINCT ON (student.id)
        student.id AS portal_student_id,
        relation.advisor_user_id
    FROM dtlms_portal_students AS student
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = student.selected_team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE student.selected_team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(student.selected_advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(student.selected_advisor_name)
    ORDER BY student.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_portal_students AS student
SET selected_advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM portal_student_advisor_choice AS choice
WHERE student.id = choice.portal_student_id
  AND student.selected_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

UPDATE dtlms_recruitment_applications AS application
SET first_choice_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(application.first_choice, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(application.first_choice)
  AND application.first_choice_team_id IS DISTINCT FROM team.id;

UPDATE dtlms_recruitment_applications AS application
SET second_choice_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(application.second_choice, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(application.second_choice)
  AND application.second_choice_team_id IS DISTINCT FROM team.id;

WITH application_advisor_choice AS (
    SELECT DISTINCT ON (application.id)
        application.id AS application_id,
        relation.advisor_user_id
    FROM dtlms_recruitment_applications AS application
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = application.first_choice_team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE application.first_choice_team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(application.intended_advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(application.intended_advisor_name)
    ORDER BY application.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_recruitment_applications AS application
SET intended_advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM application_advisor_choice AS choice
WHERE application.id = choice.application_id
  AND application.intended_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

UPDATE dtlms_portal_application_preferences AS preference
SET team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(preference.research_center_name, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(preference.research_center_name)
  AND preference.team_id IS DISTINCT FROM team.id;

WITH preference_advisor_choice AS (
    SELECT DISTINCT ON (preference.id)
        preference.id AS preference_id,
        relation.advisor_user_id
    FROM dtlms_portal_application_preferences AS preference
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = preference.team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE preference.team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(preference.advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(preference.advisor_name)
    ORDER BY preference.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_portal_application_preferences AS preference
SET advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM preference_advisor_choice AS choice
WHERE preference.id = choice.preference_id
  AND preference.advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

DROP TABLE IF EXISTS tmp_recruitment_application_number_mapping;

CREATE TEMP TABLE tmp_recruitment_application_number_mapping (
  application_id BIGINT PRIMARY KEY,
  old_workflow_key TEXT,
  new_business_key TEXT NOT NULL
);

INSERT INTO tmp_recruitment_application_number_mapping (application_id, old_workflow_key, new_business_key)
WITH application_key_basis AS (
  SELECT
    application.id AS application_id,
    COALESCE(application.applied_at, application.created_at, CURRENT_TIMESTAMP) AS sort_at,
    TO_CHAR(COALESCE(application.applied_at, application.created_at, CURRENT_TIMESTAMP), 'YYYY') AS business_year,
    CASE
      WHEN BTRIM(COALESCE(application.business_key, '')) ~ '^SH[0-9]{8}$' THEN BTRIM(application.business_key)
      WHEN BTRIM(COALESCE(application.candidate_no, '')) ~ '^SH[0-9]{8}$' THEN BTRIM(application.candidate_no)
      ELSE NULL
    END AS preserved_business_key,
    COALESCE(
      NULLIF(BTRIM(COALESCE(application.business_key, '')), ''),
      NULLIF(BTRIM(COALESCE(application.candidate_no, '')), '')
    ) AS old_workflow_key,
    BTRIM(COALESCE(application.business_key, '')) AS current_business_key,
    BTRIM(COALESCE(application.candidate_no, '')) AS current_candidate_no
  FROM dtlms_recruitment_applications AS application
  WHERE application.is_deleted = FALSE
), existing_year_sequences AS (
  SELECT
    business_year,
    MAX(SUBSTRING(preserved_business_key FROM 7 FOR 4)::INTEGER) AS max_sequence
  FROM application_key_basis
  WHERE preserved_business_key IS NOT NULL
  GROUP BY business_year
), generated_business_keys AS (
  SELECT
    basis.application_id,
    'SH' || basis.business_year || LPAD(
      (
        COALESCE(existing_year_sequences.max_sequence, 0)
        + ROW_NUMBER() OVER (PARTITION BY basis.business_year ORDER BY basis.sort_at, basis.application_id)
      )::TEXT,
      4,
      '0'
    ) AS new_business_key
  FROM application_key_basis AS basis
  LEFT JOIN existing_year_sequences
    ON existing_year_sequences.business_year = basis.business_year
  WHERE basis.preserved_business_key IS NULL
), normalized_business_keys AS (
  SELECT
    basis.application_id,
    basis.old_workflow_key,
    COALESCE(basis.preserved_business_key, generated.new_business_key) AS new_business_key,
    basis.current_business_key,
    basis.current_candidate_no
  FROM application_key_basis AS basis
  LEFT JOIN generated_business_keys AS generated
    ON generated.application_id = basis.application_id
)
SELECT
  normalized.application_id,
  normalized.old_workflow_key,
  normalized.new_business_key
FROM normalized_business_keys AS normalized
WHERE normalized.new_business_key IS NOT NULL
  AND (
    normalized.current_business_key IS DISTINCT FROM normalized.new_business_key
    OR normalized.current_candidate_no IS DISTINCT FROM normalized.new_business_key
  );

UPDATE dtlms_recruitment_applications AS application
SET business_key = mapping.new_business_key,
  candidate_no = mapping.new_business_key,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE application.id = mapping.application_id
  AND (
    application.business_key IS DISTINCT FROM mapping.new_business_key
    OR application.candidate_no IS DISTINCT FROM mapping.new_business_key
  );

DO $$
BEGIN
  IF to_regclass('public.dtlms_runtime_recruitment_applications') IS NOT NULL THEN
    UPDATE dtlms_runtime_recruitment_applications AS runtime_application
    SET payload = jsonb_set(
        jsonb_set(
          COALESCE(runtime_application.payload, '{}'::jsonb),
          '{business_key}',
          to_jsonb(mapping.new_business_key::TEXT),
          TRUE
        ),
        '{candidate_no}',
        to_jsonb(mapping.new_business_key::TEXT),
        TRUE
      ),
      updated_at = CURRENT_TIMESTAMP
    FROM tmp_recruitment_application_number_mapping AS mapping
    WHERE runtime_application.id = mapping.application_id
      AND (
        COALESCE(runtime_application.payload ->> 'business_key', '') IS DISTINCT FROM mapping.new_business_key
        OR COALESCE(runtime_application.payload ->> 'candidate_no', '') IS DISTINCT FROM mapping.new_business_key
      );
  END IF;
END $$;

DO $$
BEGIN
  IF to_regclass('public.dtlms_runtime_workflow_tasks') IS NOT NULL THEN
    UPDATE dtlms_runtime_workflow_tasks AS runtime_task
    SET payload = jsonb_set(
        jsonb_set(
          COALESCE(runtime_task.payload, '{}'::jsonb),
          '{business_key}',
          to_jsonb(mapping.new_business_key::TEXT),
          TRUE
        ),
        '{form_summary}',
        to_jsonb(
          regexp_replace(
            COALESCE(runtime_task.payload ->> 'form_summary', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      ),
      updated_at = CURRENT_TIMESTAMP
    FROM tmp_recruitment_application_number_mapping AS mapping
    WHERE (
        COALESCE(runtime_task.payload ->> 'flow_code', '') = 'recruitment_application'
        OR COALESCE(runtime_task.payload ->> 'business_dataset', '') = 'recruitment_applications'
      )
      AND (
        COALESCE(runtime_task.payload ->> 'entity_id', '') = mapping.application_id::TEXT
        OR (
          mapping.old_workflow_key IS NOT NULL
          AND COALESCE(runtime_task.payload ->> 'business_key', '') = mapping.old_workflow_key
        )
      )
      AND (
        COALESCE(runtime_task.payload ->> 'business_key', '') IS DISTINCT FROM mapping.new_business_key
        OR COALESCE(runtime_task.payload ->> 'form_summary', '') LIKE '业务编号：%'
      );
  END IF;
END $$;

UPDATE dtlms_wf_hi_procinst AS procinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND procinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_hi_taskinst AS taskinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND taskinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_hi_actinst AS actinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND actinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_ru_execution AS execution
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND execution.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_ru_task AS runtime_task
SET business_key_ = mapping.new_business_key,
  form_key_ = CASE
    WHEN runtime_task.form_key_ = mapping.old_workflow_key THEN mapping.new_business_key
    ELSE runtime_task.form_key_
  END,
  description_ = CASE
    WHEN COALESCE(runtime_task.description_, '') LIKE '业务编号：%'
      THEN regexp_replace(runtime_task.description_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE runtime_task.description_
  END
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    runtime_task.business_key_ = mapping.old_workflow_key
    OR runtime_task.form_key_ = mapping.old_workflow_key
  );

UPDATE dtlms_wf_ru_variable AS runtime_variable
SET text_value_ = CASE
    WHEN runtime_variable.name_ = 'businessKey' THEN mapping.new_business_key
    WHEN runtime_variable.name_ = 'formSummary' AND COALESCE(runtime_variable.text_value_, '') LIKE '业务编号：%'
      THEN regexp_replace(runtime_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE runtime_variable.text_value_
  END,
  json_value_ = CASE
    WHEN runtime_variable.name_ = 'businessKey'
      THEN jsonb_set(COALESCE(runtime_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
    WHEN runtime_variable.name_ = 'formSummary'
      THEN jsonb_set(
        COALESCE(runtime_variable.json_value_, '{}'::jsonb),
        '{value}',
        to_jsonb(
          regexp_replace(
            COALESCE(runtime_variable.json_value_ ->> 'value', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      )
    ELSE runtime_variable.json_value_
  END
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    (runtime_variable.name_ = 'businessKey' AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
    OR (
      runtime_variable.name_ = 'formSummary'
      AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
    )
  );

UPDATE dtlms_wf_hi_varinst AS history_variable
SET text_value_ = CASE
    WHEN history_variable.name_ = 'businessKey' THEN mapping.new_business_key
    WHEN history_variable.name_ = 'formSummary' AND COALESCE(history_variable.text_value_, '') LIKE '业务编号：%'
      THEN regexp_replace(history_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE history_variable.text_value_
  END,
  json_value_ = CASE
    WHEN history_variable.name_ = 'businessKey'
      THEN jsonb_set(COALESCE(history_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
    WHEN history_variable.name_ = 'formSummary'
      THEN jsonb_set(
        COALESCE(history_variable.json_value_, '{}'::jsonb),
        '{value}',
        to_jsonb(
          regexp_replace(
            COALESCE(history_variable.json_value_ ->> 'value', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      )
    ELSE history_variable.json_value_
  END,
  last_updated_time_ = CURRENT_TIMESTAMP
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    (history_variable.name_ = 'businessKey' AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
    OR (
      history_variable.name_ = 'formSummary'
      AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
    )
  );

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM dtlms_recruitment_plans
    WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
  ) THEN
    RAISE EXCEPTION '未找到名称为 2027 夏日学术交流日 的招生计划，无法执行 058 中的计划收口更新';
  END IF;
END $$;

DROP TABLE IF EXISTS tmp_target_recruitment_plan;

CREATE TEMP TABLE tmp_target_recruitment_plan (
  target_plan_id BIGINT PRIMARY KEY
);

INSERT INTO tmp_target_recruitment_plan (target_plan_id)
SELECT id
FROM dtlms_recruitment_plans
WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
ORDER BY CASE WHEN is_deleted THEN 1 ELSE 0 END, id
LIMIT 1;

UPDATE dtlms_recruitment_plans AS plan
SET is_deleted = FALSE,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE plan.id = target_plan.target_plan_id
  AND plan.is_deleted IS DISTINCT FROM FALSE;

UPDATE dtlms_recruitment_applications AS application
SET plan_id = target_plan.target_plan_id,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE application.plan_id IS DISTINCT FROM target_plan.target_plan_id;

UPDATE dtlms_portal_students AS student
SET selected_plan_id = target_plan.target_plan_id,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE student.selected_plan_id IS DISTINCT FROM target_plan.target_plan_id;

DELETE FROM dtlms_interview_scores
WHERE schedule_id IN (
  SELECT schedule.id
  FROM dtlms_interview_schedules AS schedule
  JOIN dtlms_interview_groups AS grp ON grp.id = schedule.interview_group_id
  CROSS JOIN tmp_target_recruitment_plan AS target_plan
  WHERE grp.plan_id <> target_plan.target_plan_id
);

DELETE FROM dtlms_interview_schedules
WHERE interview_group_id IN (
  SELECT grp.id
  FROM dtlms_interview_groups AS grp
  CROSS JOIN tmp_target_recruitment_plan AS target_plan
  WHERE grp.plan_id <> target_plan.target_plan_id
);

DELETE FROM dtlms_interview_groups
USING tmp_target_recruitment_plan AS target_plan
WHERE dtlms_interview_groups.plan_id <> target_plan.target_plan_id;

DELETE FROM dtlms_recruitment_plans
USING tmp_target_recruitment_plan AS target_plan
WHERE dtlms_recruitment_plans.id <> target_plan.target_plan_id;

UPDATE dtlms_portal_students
SET application_draft = NULL,
    updated_at = CURRENT_TIMESTAMP
WHERE application_draft IS NOT NULL;

DROP TABLE IF EXISTS tmp_liaodiao_portal_students;

CREATE TEMP TABLE tmp_liaodiao_portal_students (
  portal_student_id BIGINT PRIMARY KEY
);

INSERT INTO tmp_liaodiao_portal_students (portal_student_id)
SELECT ps.id
FROM dtlms_portal_students AS ps
WHERE BTRIM(COALESCE(ps.full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
  OR LOWER(BTRIM(COALESCE(ps.email, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(ps.email, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(ps.phone_number, '')) IN ('13800009999', '13800009998')
   OR UPPER(BTRIM(COALESCE(ps.id_number, ''))) IN ('32000019990101123X', '32000019990101124X');

DROP TABLE IF EXISTS tmp_liaodiao_recruitment_applications;

CREATE TEMP TABLE tmp_liaodiao_recruitment_applications (
  application_id BIGINT PRIMARY KEY,
  business_key TEXT,
  candidate_no TEXT
);

INSERT INTO tmp_liaodiao_recruitment_applications (application_id, business_key, candidate_no)
SELECT ra.id, ra.business_key, ra.candidate_no
FROM dtlms_recruitment_applications AS ra
LEFT JOIN tmp_liaodiao_portal_students AS ps
  ON ps.portal_student_id = ra.portal_student_id
WHERE ps.portal_student_id IS NOT NULL
  OR BTRIM(COALESCE(ra.student_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
  OR LOWER(BTRIM(COALESCE(ra.email, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(ra.email, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(ra.phone_number, '')) IN ('13800009999', '13800009998')
   OR UPPER(BTRIM(COALESCE(ra.id_number, ''))) IN ('32000019990101123X', '32000019990101124X');

DROP TABLE IF EXISTS tmp_liaodiao_workflow_keys;

CREATE TEMP TABLE tmp_liaodiao_workflow_keys (
  business_key TEXT PRIMARY KEY
);

INSERT INTO tmp_liaodiao_workflow_keys (business_key)
SELECT DISTINCT key_value
FROM (
  SELECT NULLIF(BTRIM(COALESCE(application.business_key, '')), '') AS key_value
  FROM tmp_liaodiao_recruitment_applications AS application
  UNION ALL
  SELECT NULLIF(BTRIM(COALESCE(application.candidate_no, '')), '') AS key_value
  FROM tmp_liaodiao_recruitment_applications AS application
) AS keys
WHERE key_value IS NOT NULL;

DROP TABLE IF EXISTS tmp_liaodiao_procinst;

CREATE TEMP TABLE tmp_liaodiao_procinst (
  proc_inst_id TEXT PRIMARY KEY
);

INSERT INTO tmp_liaodiao_procinst (proc_inst_id)
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_hi_procinst
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_ru_execution
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_hi_taskinst
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_ru_task
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys);

DELETE FROM dtlms_interview_scores
WHERE schedule_id IN (
  SELECT schedule.id
  FROM dtlms_interview_schedules AS schedule
  WHERE schedule.application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
);

DELETE FROM dtlms_material_scores
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
   OR reviewer_assignment_id IN (
     SELECT assignment.id
     FROM dtlms_reviewer_assignments AS assignment
     WHERE assignment.application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
   );

DELETE FROM dtlms_written_exam_scores
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_admission_decisions
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_interview_schedules
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_qualification_reviews
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_application_materials
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_reviewer_assignments
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_wf_ru_identitylink
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst)
   OR task_id_ IN (
     SELECT id_ FROM dtlms_wf_ru_task WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst)
   );

DELETE FROM dtlms_wf_ru_variable
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_varinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_actinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_taskinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_procinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_ru_task
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_ru_execution
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_recruitment_applications
WHERE id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_portal_students
WHERE id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students);

DELETE FROM dtlms_student_team_history
WHERE student_id IN (
  SELECT id
  FROM dtlms_students
  WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
     OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
);

DELETE FROM dtlms_student_advisor_history
WHERE student_id IN (
  SELECT id
  FROM dtlms_students
  WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
     OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
);

DELETE FROM dtlms_students
WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
   OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生');

DELETE FROM dtlms_login_logs
WHERE LOWER(BTRIM(COALESCE(username, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(username, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(username, '')) IN (
     '13800009999',
     '13800009998'
   );

DELETE FROM dtlms_operation_logs
WHERE entity_id IN (
    SELECT application_id::TEXT FROM tmp_liaodiao_recruitment_applications
    UNION
    SELECT portal_student_id::TEXT FROM tmp_liaodiao_portal_students
  )
   OR COALESCE(new_value ->> 'summary', '') LIKE '%联调考生%';

WITH latest_portal_application_status AS (
    SELECT DISTINCT ON (ra.portal_student_id)
        ra.portal_student_id,
        BTRIM(COALESCE(ra.application_status, '')) AS application_status
    FROM dtlms_recruitment_applications AS ra
    WHERE ra.portal_student_id IS NOT NULL
      AND COALESCE(ra.is_deleted, FALSE) = FALSE
    ORDER BY ra.portal_student_id, COALESCE(ra.applied_at, ra.updated_at, ra.created_at) DESC, ra.id DESC
)
UPDATE dtlms_portal_students AS ps
SET submitted_at = NULL,
    application_draft = CASE
        WHEN ps.application_draft IS NULL THEN NULL
        WHEN jsonb_typeof(ps.application_draft) = 'object'
            THEN jsonb_set(ps.application_draft, '{submitted_at}', 'null'::jsonb, TRUE)
        ELSE ps.application_draft
    END,
    updated_at = CURRENT_TIMESTAMP
FROM latest_portal_application_status AS latest
WHERE ps.id = latest.portal_student_id
  AND latest.application_status IN ('returned', 'rejected', '驳回重填', '不录取')
  AND ps.submitted_at IS NOT NULL;

-- 尾部增量修复：补齐唯一可推导的导师主档/团队导师关系，并按现有申请状态重建缺失的招生 workflow 兼容待办。
WITH advisor_role_users AS (
  SELECT
    u.id AS user_id,
    BTRIM(u.full_name) AS full_name,
    ROW_NUMBER() OVER (PARTITION BY BTRIM(u.full_name) ORDER BY u.id) AS row_num,
    COUNT(*) OVER (PARTITION BY BTRIM(u.full_name)) AS same_name_count
  FROM dtlms_users AS u
  JOIN dtlms_user_roles AS ur ON ur.user_id = u.id
  JOIN dtlms_roles AS r ON r.id = ur.role_id
  LEFT JOIN dtlms_advisors AS advisor
    ON advisor.user_id = u.id
   AND advisor.is_deleted = FALSE
  WHERE u.is_deleted = FALSE
    AND u.is_active = TRUE
    AND r.is_deleted = FALSE
    AND r.role_code = 'advisor'
    AND advisor.id IS NULL
    AND NULLIF(BTRIM(COALESCE(u.full_name, '')), '') IS NOT NULL
), unique_missing_advisor_users AS (
  SELECT user_id, full_name
  FROM advisor_role_users
  WHERE row_num = 1 AND same_name_count = 1
)
INSERT INTO dtlms_advisors (
  advisor_no,
  full_name,
  title,
  organization_name,
  research_direction,
  annual_quota,
  user_id,
  is_deleted
)
SELECT
  'ADV-U' || LPAD(user_id::TEXT, 6, '0'),
  full_name,
  '待补充',
  '待补充',
  '待补充',
  0,
  user_id,
  FALSE
FROM unique_missing_advisor_users;

DROP TABLE IF EXISTS tmp_portal_team_advisor_relation_backfill;

CREATE TEMP TABLE tmp_portal_team_advisor_relation_backfill (
  team_id BIGINT NOT NULL,
  advisor_id BIGINT NOT NULL,
  advisor_user_id BIGINT NOT NULL,
  advisor_name TEXT NOT NULL,
  PRIMARY KEY (team_id, advisor_user_id)
);

INSERT INTO tmp_portal_team_advisor_relation_backfill (team_id, advisor_id, advisor_user_id, advisor_name)
WITH missing_portal_pairs AS (
  SELECT DISTINCT
    ps.selected_team_id AS team_id,
    BTRIM(ps.selected_advisor_name) AS advisor_name
  FROM dtlms_portal_students AS ps
  WHERE ps.selected_team_id IS NOT NULL
    AND NULLIF(BTRIM(COALESCE(ps.selected_advisor_name, '')), '') IS NOT NULL
    AND ps.selected_advisor_user_id IS NULL
), advisor_candidates AS (
  SELECT
    pair.team_id,
    advisor.id AS advisor_id,
    advisor.user_id AS advisor_user_id,
    pair.advisor_name
  FROM missing_portal_pairs AS pair
  JOIN dtlms_advisors AS advisor
    ON advisor.is_deleted = FALSE
   AND advisor.user_id IS NOT NULL
   AND advisor.full_name = pair.advisor_name
)
SELECT
  candidate.team_id,
  candidate.advisor_id,
  candidate.advisor_user_id,
  candidate.advisor_name
FROM advisor_candidates AS candidate
WHERE NOT EXISTS (
  SELECT 1
  FROM dtlms_team_advisors AS relation
  WHERE relation.team_id = candidate.team_id
    AND relation.is_deleted = FALSE
    AND COALESCE(relation.advisor_user_id, 0) = candidate.advisor_user_id
);

INSERT INTO dtlms_team_advisors (
  team_id,
  advisor_id,
  advisor_role,
  joined_on,
  is_deleted,
  advisor_user_id
)
SELECT
  team_id,
  advisor_id,
  'member',
  CURRENT_DATE,
  FALSE,
  advisor_user_id
FROM tmp_portal_team_advisor_relation_backfill;

WITH portal_student_advisor_choice AS (
  SELECT DISTINCT ON (student.id)
    student.id AS portal_student_id,
    relation.advisor_user_id
  FROM dtlms_portal_students AS student
  JOIN dtlms_team_advisors AS relation
    ON relation.team_id = student.selected_team_id
     AND relation.is_deleted = FALSE
  JOIN dtlms_advisors AS advisor
    ON advisor.id = relation.advisor_id
     AND advisor.is_deleted = FALSE
  WHERE student.selected_team_id IS NOT NULL
    AND relation.advisor_user_id IS NOT NULL
    AND NULLIF(BTRIM(COALESCE(student.selected_advisor_name, '')), '') IS NOT NULL
    AND advisor.full_name = BTRIM(student.selected_advisor_name)
  ORDER BY student.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_portal_students AS student
SET selected_advisor_user_id = choice.advisor_user_id,
  updated_at = CURRENT_TIMESTAMP
FROM portal_student_advisor_choice AS choice
WHERE student.id = choice.portal_student_id
  AND student.selected_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

WITH application_advisor_choice AS (
  SELECT DISTINCT ON (application.id)
    application.id AS application_id,
    relation.advisor_user_id
  FROM dtlms_recruitment_applications AS application
  JOIN dtlms_team_advisors AS relation
    ON relation.team_id = application.first_choice_team_id
     AND relation.is_deleted = FALSE
  JOIN dtlms_advisors AS advisor
    ON advisor.id = relation.advisor_id
     AND advisor.is_deleted = FALSE
  WHERE application.first_choice_team_id IS NOT NULL
    AND relation.advisor_user_id IS NOT NULL
    AND NULLIF(BTRIM(COALESCE(application.intended_advisor_name, '')), '') IS NOT NULL
    AND advisor.full_name = BTRIM(application.intended_advisor_name)
  ORDER BY application.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_recruitment_applications AS application
SET intended_advisor_user_id = choice.advisor_user_id,
  updated_at = CURRENT_TIMESTAMP
FROM application_advisor_choice AS choice
WHERE application.id = choice.application_id
  AND application.intended_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

DROP TABLE IF EXISTS tmp_recruitment_workflow_repairs;

CREATE TEMP TABLE tmp_recruitment_workflow_repairs (
  application_id BIGINT PRIMARY KEY,
  business_key TEXT NOT NULL,
  task_key TEXT NOT NULL,
  process_instance_id TEXT NOT NULL,
  execution_id TEXT NOT NULL,
  process_definition_id TEXT NOT NULL,
  deployment_id TEXT NOT NULL,
  task_definition_key TEXT NOT NULL,
  title TEXT NOT NULL,
  applicant_name TEXT NOT NULL,
  current_node TEXT NOT NULL,
  current_handler TEXT NOT NULL,
  task_status TEXT NOT NULL,
  start_time TIMESTAMPTZ NOT NULL,
  due_date TIMESTAMPTZ NOT NULL,
  form_summary TEXT NOT NULL
);

INSERT INTO tmp_recruitment_workflow_repairs (
  application_id,
  business_key,
  task_key,
  process_instance_id,
  execution_id,
  process_definition_id,
  deployment_id,
  task_definition_key,
  title,
  applicant_name,
  current_node,
  current_handler,
  task_status,
  start_time,
  due_date,
  form_summary
)
WITH active_recruitment_applications AS (
  SELECT
    ra.id AS application_id,
    BTRIM(COALESCE(ra.business_key, '')) AS business_key,
    BTRIM(COALESCE(ra.student_name, '未知申请人')) AS applicant_name,
    COALESCE(ra.applied_at, ra.updated_at, ra.created_at, CURRENT_TIMESTAMP) AS start_time,
    COALESCE(rf.field_name, NULLIF(BTRIM(COALESCE(ra.first_choice, '')), ''), '-') AS intended_field_name,
    '待补材料' AS material_status_label,
    CASE ra.application_status
      WHEN 'submitted' THEN 'qualification_review'
      WHEN 'qualified' THEN 'qualification_passed'
      WHEN 'scoring' THEN 'interview_arrangement'
      WHEN 'interviewed' THEN 'admission_confirmation'
      ELSE NULL
    END AS task_definition_key,
    CASE ra.application_status
      WHEN 'submitted' THEN '资格审核'
      WHEN 'qualified' THEN '评分准备'
      WHEN 'scoring' THEN '面试安排'
      WHEN 'interviewed' THEN '录取确认'
      ELSE NULL
    END AS current_node,
    CASE ra.application_status
      WHEN 'submitted' THEN '待处理'
      ELSE '处理中'
    END AS task_status,
    CASE ra.application_status
      WHEN 'submitted' THEN INTERVAL '1 day'
      WHEN 'qualified' THEN INTERVAL '1 day'
      WHEN 'scoring' THEN INTERVAL '2 days'
      WHEN 'interviewed' THEN INTERVAL '2 days'
      ELSE INTERVAL '1 day'
    END AS due_interval,
    hi.id_ AS existing_hi_task_key,
    hi.proc_inst_id_ AS existing_hi_proc_inst_id,
    hi.exec_id_ AS existing_hi_exec_id,
    ru.id_ AS existing_ru_task_key,
    ru.proc_inst_id_ AS existing_ru_proc_inst_id,
    ru.exec_id_ AS existing_ru_exec_id,
    CASE WHEN hi.id_ IS NOT NULL THEN 1 ELSE 0 END AS has_hi_task,
    CASE WHEN ru.id_ IS NOT NULL THEN 1 ELSE 0 END AS has_ru_task
  FROM dtlms_recruitment_applications AS ra
  LEFT JOIN dtlms_research_fields AS rf ON rf.id = ra.intended_field_id
  LEFT JOIN LATERAL (
    SELECT id_, proc_inst_id_, exec_id_
    FROM dtlms_wf_hi_taskinst
    WHERE business_key_ = ra.business_key
    ORDER BY start_time_ DESC, id_ DESC
    LIMIT 1
  ) AS hi ON TRUE
  LEFT JOIN LATERAL (
    SELECT id_, proc_inst_id_, exec_id_
    FROM dtlms_wf_ru_task
    WHERE business_key_ = ra.business_key
    ORDER BY create_time_ DESC, id_ DESC
    LIMIT 1
  ) AS ru ON TRUE
  WHERE COALESCE(ra.is_deleted, FALSE) = FALSE
    AND ra.application_status IN ('submitted', 'qualified', 'scoring', 'interviewed')
    AND NULLIF(BTRIM(COALESCE(ra.business_key, '')), '') IS NOT NULL
    AND (hi.id_ IS NULL OR ru.id_ IS NULL)
), normalized_active_repairs AS (
  SELECT
    repair.application_id,
    repair.business_key,
    COALESCE(
      repair.existing_hi_task_key,
      repair.existing_ru_task_key,
      'TASK-' || (580000000 + repair.application_id)::TEXT
    ) AS task_key,
    COALESCE(
      repair.existing_hi_proc_inst_id,
      repair.existing_ru_proc_inst_id,
      'procinst-recruitmenta-'
        || SUBSTRING(LOWER(regexp_replace(repair.business_key, '[^a-zA-Z0-9]', '', 'g')) FROM 1 FOR 18)
        || '-'
        || SUBSTRING(md5('recruitment_application::' || repair.business_key || '::process-instance') FROM 1 FOR 10)
    ) AS process_instance_id,
    repair.task_definition_key,
    repair.applicant_name || '报名审核' AS title,
    repair.applicant_name,
    repair.current_node,
    '学合管理员' AS current_handler,
    repair.task_status,
    repair.start_time,
    repair.start_time + repair.due_interval AS due_date,
    '业务编号：' || repair.business_key || '；研究方向：' || repair.intended_field_name || '；材料状态：' || repair.material_status_label AS form_summary
  FROM active_recruitment_applications AS repair
  WHERE repair.task_definition_key IS NOT NULL
)
SELECT
  repair.application_id,
  repair.business_key,
  repair.task_key,
  repair.process_instance_id,
  'exec-'
    || SUBSTRING(LOWER(regexp_replace(repair.task_definition_key, '[^a-zA-Z0-9]', '', 'g')) FROM 1 FOR 18)
    || '-'
    || SUBSTRING(md5(repair.process_instance_id || '::' || repair.task_definition_key || '::execution') FROM 1 FOR 10) AS execution_id,
  'procdef-recruitmentapp-v1-' || SUBSTRING(md5('recruitment_application::process-definition') FROM 1 FOR 8) AS process_definition_id,
  'dep-recruitmentapp-' || SUBSTRING(md5('recruitment_application::deployment') FROM 1 FOR 8) AS deployment_id,
  repair.task_definition_key,
  repair.title,
  repair.applicant_name,
  repair.current_node,
  repair.current_handler,
  repair.task_status,
  repair.start_time,
  repair.due_date,
  repair.form_summary
FROM normalized_active_repairs AS repair;

DELETE FROM dtlms_wf_ru_identitylink
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs)
   OR task_id_ IN (SELECT task_key FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_ru_variable
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs)
   OR task_id_ IN (SELECT task_key FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_ru_task
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs)
   OR id_ IN (SELECT task_key FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_ru_execution
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_hi_varinst
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_hi_actinst
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_hi_taskinst
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs)
   OR id_ IN (SELECT task_key FROM tmp_recruitment_workflow_repairs);

DELETE FROM dtlms_wf_hi_procinst
WHERE proc_inst_id_ IN (SELECT process_instance_id FROM tmp_recruitment_workflow_repairs);

INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_)
SELECT
  repair.deployment_id,
  '招生录取审批',
  '招生管理',
  'recruitment_application',
  MIN(repair.start_time)
FROM tmp_recruitment_workflow_repairs AS repair
GROUP BY repair.deployment_id
ON CONFLICT (id_) DO UPDATE
SET name_ = EXCLUDED.name_,
  category_ = EXCLUDED.category_,
  key_ = EXCLUDED.key_,
  deploy_time_ = EXCLUDED.deploy_time_;

INSERT INTO dtlms_wf_re_procdef (
  id_,
  key_,
  version_,
  deployment_id_,
  resource_name_,
  diagram_resource_name_,
  name_,
  category_,
  description_,
  suspension_state_
)
SELECT
  repair.process_definition_id,
  'recruitment_application',
  1,
  repair.deployment_id,
  'recruitment_application.bpmn20.xml',
  'recruitment_application.png',
  '招生录取审批',
  '招生管理',
  '招生录取审批 定义',
  1
FROM tmp_recruitment_workflow_repairs AS repair
GROUP BY repair.process_definition_id, repair.deployment_id
ON CONFLICT (id_) DO UPDATE
SET key_ = EXCLUDED.key_,
  version_ = EXCLUDED.version_,
  deployment_id_ = EXCLUDED.deployment_id_,
  resource_name_ = EXCLUDED.resource_name_,
  diagram_resource_name_ = EXCLUDED.diagram_resource_name_,
  name_ = EXCLUDED.name_,
  category_ = EXCLUDED.category_,
  description_ = EXCLUDED.description_,
  suspension_state_ = EXCLUDED.suspension_state_;

INSERT INTO dtlms_wf_hi_procinst (
  id_,
  proc_inst_id_,
  business_key_,
  proc_def_id_,
  start_time_,
  end_time_,
  duration_ms_,
  start_user_id_,
  end_act_id_,
  delete_reason_,
  start_act_id_,
  state_
)
SELECT
  repair.process_instance_id,
  repair.process_instance_id,
  repair.business_key,
  repair.process_definition_id,
  repair.start_time,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  'startEvent',
  'ACTIVE'
FROM tmp_recruitment_workflow_repairs AS repair;

INSERT INTO dtlms_wf_hi_taskinst (
  id_,
  task_def_key_,
  proc_def_id_,
  proc_inst_id_,
  exec_id_,
  name_,
  business_key_,
  assignee_,
  owner_,
  start_time_,
  claim_time_,
  end_time_,
  duration_ms_,
  due_date_,
  delete_reason_,
  priority_,
  category_
)
SELECT
  repair.task_key,
  repair.task_definition_key,
  repair.process_definition_id,
  repair.process_instance_id,
  repair.execution_id,
  repair.title,
  repair.business_key,
  NULL,
  NULL,
  repair.start_time,
  NULL,
  NULL,
  NULL,
  repair.due_date,
  NULL,
  50,
  '招生管理'
FROM tmp_recruitment_workflow_repairs AS repair;

INSERT INTO dtlms_wf_hi_varinst (
  id_,
  proc_inst_id_,
  exec_id_,
  task_id_,
  name_,
  var_type_,
  text_value_,
  number_value_,
  json_value_,
  create_time_,
  last_updated_time_
)
SELECT
  'HVAR-' || repair.process_instance_id || '-' || variable.name_,
  repair.process_instance_id,
  repair.execution_id,
  NULL,
  variable.name_,
  variable.var_type_,
  variable.text_value_,
  variable.number_value_,
  variable.json_value_,
  repair.start_time,
  repair.start_time
FROM tmp_recruitment_workflow_repairs AS repair
CROSS JOIN LATERAL (
  VALUES
    ('businessKey', 'string', repair.business_key, NULL::BIGINT, jsonb_build_object('value', repair.business_key)),
    ('workflowName', 'string', '招生录取审批', NULL::BIGINT, jsonb_build_object('value', '招生录取审批')),
    ('businessModule', 'string', '招生管理', NULL::BIGINT, jsonb_build_object('value', '招生管理')),
    ('applicantName', 'string', repair.applicant_name, NULL::BIGINT, jsonb_build_object('value', repair.applicant_name)),
    ('currentHandler', 'string', repair.current_handler, NULL::BIGINT, jsonb_build_object('value', repair.current_handler)),
    ('flowCode', 'string', 'recruitment_application', NULL::BIGINT, jsonb_build_object('value', 'recruitment_application')),
    ('entityId', 'number', NULL::TEXT, repair.application_id, jsonb_build_object('value', repair.application_id)),
    ('currentNode', 'string', repair.current_node, NULL::BIGINT, jsonb_build_object('value', repair.current_node)),
    ('nodeKey', 'string', repair.task_definition_key, NULL::BIGINT, jsonb_build_object('value', repair.task_definition_key)),
    ('taskStatus', 'string', repair.task_status, NULL::BIGINT, jsonb_build_object('value', repair.task_status)),
    ('formSummary', 'string', repair.form_summary, NULL::BIGINT, jsonb_build_object('value', repair.form_summary)),
    ('latestComment', 'string', '', NULL::BIGINT, jsonb_build_object('value', '')),
    ('candidateGroups', 'json', NULL::TEXT, NULL::BIGINT, '["platform_admin"]'::jsonb),
    ('historyEntries', 'json', NULL::TEXT, NULL::BIGINT, '[]'::jsonb)
) AS variable(name_, var_type_, text_value_, number_value_, json_value_);

INSERT INTO dtlms_wf_ru_execution (
  id_,
  proc_inst_id_,
  proc_def_id_,
  business_key_,
  parent_id_,
  act_id_,
  is_active_,
  is_concurrent_,
  is_scope_,
  start_time_,
  start_user_id_
)
SELECT
  repair.execution_id,
  repair.process_instance_id,
  repair.process_definition_id,
  repair.business_key,
  NULL,
  repair.task_definition_key,
  TRUE,
  FALSE,
  TRUE,
  repair.start_time,
  NULL
FROM tmp_recruitment_workflow_repairs AS repair;

INSERT INTO dtlms_wf_ru_task (
  id_,
  exec_id_,
  proc_inst_id_,
  proc_def_id_,
  task_def_key_,
  name_,
  business_key_,
  assignee_,
  owner_,
  create_time_,
  due_date_,
  claim_time_,
  priority_,
  suspension_state_,
  form_key_,
  description_
)
SELECT
  repair.task_key,
  repair.execution_id,
  repair.process_instance_id,
  repair.process_definition_id,
  repair.task_definition_key,
  repair.title,
  repair.business_key,
  NULL,
  NULL,
  repair.start_time,
  repair.due_date,
  NULL,
  50,
  1,
  repair.business_key,
  repair.form_summary
FROM tmp_recruitment_workflow_repairs AS repair;

INSERT INTO dtlms_wf_ru_identitylink (task_id_, proc_inst_id_, user_id_, group_id_, link_type_)
SELECT
  repair.task_key,
  repair.process_instance_id,
  NULL,
  'platform_admin',
  'candidate'
FROM tmp_recruitment_workflow_repairs AS repair;

INSERT INTO dtlms_wf_ru_variable (
  id_,
  exec_id_,
  proc_inst_id_,
  task_id_,
  name_,
  var_type_,
  text_value_,
  number_value_,
  json_value_,
  create_time_
)
SELECT
  'RVAR-' || repair.process_instance_id || '-' || variable.name_,
  repair.execution_id,
  repair.process_instance_id,
  NULL,
  variable.name_,
  variable.var_type_,
  variable.text_value_,
  variable.number_value_,
  variable.json_value_,
  repair.start_time
FROM tmp_recruitment_workflow_repairs AS repair
CROSS JOIN LATERAL (
  VALUES
    ('businessKey', 'string', repair.business_key, NULL::BIGINT, jsonb_build_object('value', repair.business_key)),
    ('workflowName', 'string', '招生录取审批', NULL::BIGINT, jsonb_build_object('value', '招生录取审批')),
    ('businessModule', 'string', '招生管理', NULL::BIGINT, jsonb_build_object('value', '招生管理')),
    ('applicantName', 'string', repair.applicant_name, NULL::BIGINT, jsonb_build_object('value', repair.applicant_name)),
    ('currentHandler', 'string', repair.current_handler, NULL::BIGINT, jsonb_build_object('value', repair.current_handler)),
    ('flowCode', 'string', 'recruitment_application', NULL::BIGINT, jsonb_build_object('value', 'recruitment_application')),
    ('entityId', 'number', NULL::TEXT, repair.application_id, jsonb_build_object('value', repair.application_id)),
    ('currentNode', 'string', repair.current_node, NULL::BIGINT, jsonb_build_object('value', repair.current_node)),
    ('nodeKey', 'string', repair.task_definition_key, NULL::BIGINT, jsonb_build_object('value', repair.task_definition_key)),
    ('taskStatus', 'string', repair.task_status, NULL::BIGINT, jsonb_build_object('value', repair.task_status)),
    ('formSummary', 'string', repair.form_summary, NULL::BIGINT, jsonb_build_object('value', repair.form_summary)),
    ('latestComment', 'string', '', NULL::BIGINT, jsonb_build_object('value', '')),
    ('candidateGroups', 'json', NULL::TEXT, NULL::BIGINT, '["platform_admin"]'::jsonb),
    ('historyEntries', 'json', NULL::TEXT, NULL::BIGINT, '[]'::jsonb)
) AS variable(name_, var_type_, text_value_, number_value_, json_value_);

-- runtime 历史表在生产补丁尾部统一物理删除；此前的业务修复语句已完成对 runtime 数据的最后一次读取/改写。
DROP TABLE IF EXISTS dtlms_runtime_portal_students;
DROP TABLE IF EXISTS dtlms_runtime_workflow_tasks;
DROP TABLE IF EXISTS dtlms_runtime_sync_logs;
DROP TABLE IF EXISTS dtlms_runtime_operation_logs;
DROP TABLE IF EXISTS dtlms_runtime_integrations;
DROP TABLE IF EXISTS dtlms_runtime_audit_policies;
DROP TABLE IF EXISTS dtlms_runtime_system_users;
DROP TABLE IF EXISTS dtlms_runtime_roles;
DROP TABLE IF EXISTS dtlms_runtime_thesis_reviews;
DROP TABLE IF EXISTS dtlms_runtime_theses;
DROP TABLE IF EXISTS dtlms_runtime_outbound_studies;
DROP TABLE IF EXISTS dtlms_runtime_scientific_reports;
DROP TABLE IF EXISTS dtlms_runtime_training_plans;
DROP TABLE IF EXISTS dtlms_runtime_recruitment_applications;
DROP TABLE IF EXISTS dtlms_runtime_recruitment_plans;
DROP TABLE IF EXISTS dtlms_runtime_students;
DROP TABLE IF EXISTS dtlms_runtime_teams;
DROP TABLE IF EXISTS dtlms_runtime_profiles;
DROP TABLE IF EXISTS dtlms_runtime_counters;

DO $$
BEGIN
  IF to_regclass('public.dtlms_teams') IS NULL
     OR to_regclass('public.dtlms_team_advisors') IS NULL
     OR to_regclass('public.dtlms_student_team_history') IS NULL THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 015_team_schema_migration.sql 所需结构，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_recruitment_applications'
        AND column_name = 'business_key'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_scientific_reports'
        AND column_name = 'business_key'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_outbound_studies'
        AND column_name = 'business_key'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_theses'
        AND column_name = 'business_key'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 016_business_key_migration.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF to_regclass('public.dtlms_wf_re_procdef') IS NULL
     OR to_regclass('public.dtlms_wf_ru_task') IS NULL
     OR to_regclass('public.dtlms_wf_hi_taskinst') IS NULL THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 017_workflow_flowable_schema.sql 所需结构，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_recruitment_applications'
        AND column_name = 'review_round'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_recruitment_applications'
        AND column_name = 'supplementary_profile'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 018_recruitment_application_profile.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_students'
        AND column_name = 'password_hash'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_students'
        AND column_name = 'signed_agreement'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 021_portal_auth_and_profile_fields.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF to_regclass('public.dtlms_portal_student_profiles') IS NULL
     OR to_regclass('public.dtlms_portal_application_preferences') IS NULL
     OR to_regclass('public.dtlms_portal_application_education_experiences') IS NULL
     OR to_regclass('public.dtlms_portal_application_personal_statements') IS NULL THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 022_portal_application_structured_schema.sql 所需结构，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_recruitment_plans'
        AND column_name = 'plan_description'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 024_recruitment_plan_description.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_students'
        AND column_name = 'account_status'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 025_portal_student_account_status.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_student_profiles'
        AND column_name = 'profile_photo_url'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 026_portal_profile_photo_and_ethnic_dict.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF to_regclass('public.dtlms_user_profiles') IS NULL THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 028_user_profiles_relational.sql 所需结构，请勿仅封口迁移';
  END IF;

  IF to_regclass('public.dtlms_dict_types') IS NULL
     OR to_regclass('public.dtlms_dict_data') IS NULL THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 050_dict_schema.sql 所需结构，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_student_profiles'
        AND column_name = 'id_card_collage_url'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 052_portal_id_card_collage.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_application_achievement_records'
        AND column_name = 'achievement_month'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_application_achievement_records'
        AND column_name = 'award_certificate_attachment_url'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 054_portal_achievement_records_v2.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_application_personal_statements'
        AND column_name = 'growth_experience_text'
    )
    OR NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_application_personal_statements'
        AND column_name = 'supporting_material_attachment_url'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 055_portal_personal_statement_v2.sql 所需字段，请勿仅封口迁移';
  END IF;

  IF NOT EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'dtlms_portal_application_education_experiences'
        AND column_name = 'graduation_certificate_attachment_url'
    ) THEN
    RAISE EXCEPTION '058 前置校验失败：缺少 057_portal_education_graduation_certificate.sql 所需字段，请勿仅封口迁移';
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS dtlms_schema_migrations (
  file_name VARCHAR(255) PRIMARY KEY,
  applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dtlms_schema_migrations (file_name)
VALUES
  ('015_team_schema_migration.sql'),
  ('016_business_key_migration.sql'),
  ('017_workflow_flowable_schema.sql'),
  ('018_recruitment_application_profile.sql'),
  ('021_portal_auth_and_profile_fields.sql'),
  ('022_portal_application_structured_schema.sql'),
  ('024_recruitment_plan_description.sql'),
  ('025_portal_student_account_status.sql'),
  ('026_portal_profile_photo_and_ethnic_dict.sql'),
  ('028_user_profiles_relational.sql'),
  ('050_dict_schema.sql'),
  ('052_portal_id_card_collage.sql'),
  ('054_portal_achievement_records_v2.sql'),
  ('055_portal_personal_statement_v2.sql'),
  ('057_portal_education_graduation_certificate.sql'),
  ('059_drop_runtime_tables.sql')
ON CONFLICT (file_name) DO NOTHING;