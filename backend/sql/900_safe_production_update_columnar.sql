BEGIN;

-- 0) 本次上线新增结构字段（等价覆盖 057_portal_education_graduation_certificate.sql）
ALTER TABLE IF EXISTS dtlms_portal_application_education_experiences
    ADD COLUMN IF NOT EXISTS graduation_certificate_attachment_url TEXT;

-- 0.1) 既有生产环境字段兜底
ALTER TABLE IF EXISTS dtlms_portal_students
    ADD COLUMN IF NOT EXISTS application_draft JSONB;

ALTER TABLE IF EXISTS dtlms_portal_student_profiles
    ADD COLUMN IF NOT EXISTS id_card_collage_url VARCHAR(255);

-- 1) 门户学生历史数据回填到正式表
WITH runtime_students AS (
    SELECT
        rs.id,
        rs.payload,
        CASE
            WHEN jsonb_typeof(rs.payload -> 'profile') = 'object' THEN rs.payload -> 'profile'
            ELSE '{}'::jsonb
        END AS profile_payload
    FROM dtlms_runtime_portal_students rs
)
INSERT INTO dtlms_portal_students (
    id, full_name, phone_number, email, id_number, account_status, password_hash, gender, birth_date,
    ethnic_group, native_place, marital_status, religious_belief, id_type, mailing_address,
    graduation_school, highest_degree, intended_field, political_status, english_level,
    family_info, education_experience, practice_experience, personal_profile,
    recommendation_notes, personal_statement_text, signed_agreement, selected_plan_id,
    selected_team_name, selected_advisor_name, self_evaluation, application_draft, submitted_at, created_at, updated_at
)
SELECT
    id,
    payload ->> 'full_name',
    payload ->> 'phone_number',
    payload ->> 'email',
    payload ->> 'id_number',
    COALESCE(NULLIF(payload ->> 'account_status', ''), '启用'),
    NULLIF(payload ->> 'password_hash', ''),
    NULLIF(payload ->> 'gender', ''),
    NULLIF(payload ->> 'birth_date', ''),
    NULLIF(payload ->> 'ethnic_group', ''),
    NULLIF(payload ->> 'native_place', ''),
    NULLIF(payload ->> 'marital_status', ''),
    NULLIF(payload ->> 'religious_belief', ''),
    NULLIF(payload ->> 'id_type', ''),
    NULLIF(payload ->> 'mailing_address', ''),
    NULLIF(payload ->> 'graduation_school', ''),
    NULLIF(payload ->> 'highest_degree', ''),
    NULLIF(payload ->> 'intended_field', ''),
    NULLIF(payload ->> 'political_status', ''),
    NULLIF(payload ->> 'english_level', ''),
    NULLIF(payload ->> 'family_info', ''),
    NULLIF(payload ->> 'education_experience', ''),
    NULLIF(payload ->> 'practice_experience', ''),
    NULLIF(payload ->> 'personal_profile', ''),
    NULLIF(payload ->> 'recommendation_notes', ''),
    NULLIF(payload ->> 'personal_statement_text', ''),
    CASE
        WHEN lower(COALESCE(payload ->> 'signed_agreement', 'false')) IN ('true', 't', '1', 'yes', 'y') THEN TRUE
        ELSE FALSE
    END,
    CASE
        WHEN NULLIF(payload ->> 'selected_plan_id', '') IS NULL THEN NULL
        ELSE (payload ->> 'selected_plan_id')::BIGINT
    END,
    NULLIF(payload ->> 'selected_team_name', ''),
    NULLIF(payload ->> 'selected_advisor_name', ''),
    NULLIF(payload ->> 'self_evaluation', ''),
    CASE
        WHEN jsonb_typeof(payload -> 'application_draft') = 'object' THEN payload -> 'application_draft'
        ELSE NULL
    END,
    CASE
        WHEN NULLIF(payload ->> 'submitted_at', '') IS NULL THEN NULL
        ELSE (payload ->> 'submitted_at')::TIMESTAMPTZ
    END,
    COALESCE(
        CASE
            WHEN NULLIF(payload ->> 'created_at', '') IS NULL THEN NULL
            ELSE (payload ->> 'created_at')::TIMESTAMPTZ
        END,
        CURRENT_TIMESTAMP
    ),
    COALESCE(
        CASE
            WHEN NULLIF(payload ->> 'updated_at', '') IS NULL THEN NULL
            ELSE (payload ->> 'updated_at')::TIMESTAMPTZ
        END,
        CURRENT_TIMESTAMP
    )
FROM runtime_students
WHERE NULLIF(payload ->> 'full_name', '') IS NOT NULL
  AND NULLIF(payload ->> 'phone_number', '') IS NOT NULL
  AND NULLIF(payload ->> 'email', '') IS NOT NULL
  AND NULLIF(payload ->> 'id_number', '') IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET full_name = EXCLUDED.full_name,
    phone_number = EXCLUDED.phone_number,
    email = EXCLUDED.email,
    id_number = EXCLUDED.id_number,
    account_status = EXCLUDED.account_status,
    password_hash = EXCLUDED.password_hash,
    gender = EXCLUDED.gender,
    birth_date = EXCLUDED.birth_date,
    ethnic_group = EXCLUDED.ethnic_group,
    native_place = EXCLUDED.native_place,
    marital_status = EXCLUDED.marital_status,
    religious_belief = EXCLUDED.religious_belief,
    id_type = EXCLUDED.id_type,
    mailing_address = EXCLUDED.mailing_address,
    graduation_school = EXCLUDED.graduation_school,
    highest_degree = EXCLUDED.highest_degree,
    intended_field = EXCLUDED.intended_field,
    political_status = EXCLUDED.political_status,
    english_level = EXCLUDED.english_level,
    family_info = EXCLUDED.family_info,
    education_experience = EXCLUDED.education_experience,
    practice_experience = EXCLUDED.practice_experience,
    personal_profile = EXCLUDED.personal_profile,
    recommendation_notes = EXCLUDED.recommendation_notes,
    personal_statement_text = EXCLUDED.personal_statement_text,
    signed_agreement = EXCLUDED.signed_agreement,
    selected_plan_id = EXCLUDED.selected_plan_id,
    selected_team_name = EXCLUDED.selected_team_name,
    selected_advisor_name = EXCLUDED.selected_advisor_name,
    self_evaluation = EXCLUDED.self_evaluation,
    application_draft = COALESCE(EXCLUDED.application_draft, dtlms_portal_students.application_draft),
    submitted_at = EXCLUDED.submitted_at,
    updated_at = EXCLUDED.updated_at;

WITH runtime_students AS (
    SELECT
        rs.id,
        rs.payload,
        CASE
            WHEN jsonb_typeof(rs.payload -> 'profile') = 'object' THEN rs.payload -> 'profile'
            ELSE '{}'::jsonb
        END AS profile_payload
    FROM dtlms_runtime_portal_students rs
), profile_source AS (
    SELECT
        id AS portal_student_id,
        NULLIF(profile_payload ->> 'full_name_pinyin', '') AS full_name_pinyin,
        NULLIF(profile_payload ->> 'profile_photo_url', '') AS profile_photo_url,
        NULLIF(profile_payload ->> 'id_card_collage_url', '') AS id_card_collage_url,
        COALESCE(NULLIF(profile_payload ->> 'gender', ''), NULLIF(payload ->> 'gender', '')) AS gender,
        COALESCE(NULLIF(profile_payload ->> 'birth_date', ''), NULLIF(payload ->> 'birth_date', '')) AS birth_date,
        COALESCE(NULLIF(profile_payload ->> 'ethnic_group', ''), NULLIF(payload ->> 'ethnic_group', '')) AS ethnic_group,
        COALESCE(NULLIF(profile_payload ->> 'native_place', ''), NULLIF(payload ->> 'native_place', '')) AS native_place,
        COALESCE(NULLIF(profile_payload ->> 'political_status', ''), NULLIF(payload ->> 'political_status', '')) AS political_status,
        COALESCE(NULLIF(profile_payload ->> 'marital_status', ''), NULLIF(payload ->> 'marital_status', '')) AS marital_status,
        COALESCE(NULLIF(profile_payload ->> 'religious_belief', ''), NULLIF(payload ->> 'religious_belief', '')) AS religious_belief,
        COALESCE(NULLIF(profile_payload ->> 'id_type', ''), NULLIF(payload ->> 'id_type', '')) AS id_type,
        COALESCE(NULLIF(profile_payload ->> 'mailing_address', ''), NULLIF(payload ->> 'mailing_address', '')) AS mailing_address,
        NULLIF(profile_payload ->> 'emergency_contact_name', '') AS emergency_contact_name,
        NULLIF(profile_payload ->> 'emergency_contact_phone', '') AS emergency_contact_phone
    FROM runtime_students
)
INSERT INTO dtlms_portal_student_profiles (
    portal_student_id, full_name_pinyin, profile_photo_url, id_card_collage_url, gender, birth_date, ethnic_group,
    native_place, political_status, marital_status, religious_belief, id_type,
    mailing_address, emergency_contact_name, emergency_contact_phone
)
SELECT
    portal_student_id,
    full_name_pinyin,
    profile_photo_url,
    id_card_collage_url,
    gender,
    birth_date,
    ethnic_group,
    native_place,
    political_status,
    marital_status,
    religious_belief,
    id_type,
    mailing_address,
    emergency_contact_name,
    emergency_contact_phone
FROM profile_source
WHERE full_name_pinyin IS NOT NULL
   OR profile_photo_url IS NOT NULL
    OR id_card_collage_url IS NOT NULL
   OR gender IS NOT NULL
   OR birth_date IS NOT NULL
   OR ethnic_group IS NOT NULL
   OR native_place IS NOT NULL
   OR political_status IS NOT NULL
   OR marital_status IS NOT NULL
   OR religious_belief IS NOT NULL
   OR id_type IS NOT NULL
   OR mailing_address IS NOT NULL
   OR emergency_contact_name IS NOT NULL
   OR emergency_contact_phone IS NOT NULL
ON CONFLICT (portal_student_id) DO UPDATE
SET full_name_pinyin = EXCLUDED.full_name_pinyin,
    profile_photo_url = EXCLUDED.profile_photo_url,
    id_card_collage_url = EXCLUDED.id_card_collage_url,
    gender = EXCLUDED.gender,
    birth_date = EXCLUDED.birth_date,
    ethnic_group = EXCLUDED.ethnic_group,
    native_place = EXCLUDED.native_place,
    political_status = EXCLUDED.political_status,
    marital_status = EXCLUDED.marital_status,
    religious_belief = EXCLUDED.religious_belief,
    id_type = EXCLUDED.id_type,
    mailing_address = EXCLUDED.mailing_address,
    emergency_contact_name = EXCLUDED.emergency_contact_name,
    emergency_contact_phone = EXCLUDED.emergency_contact_phone,
    updated_at = CURRENT_TIMESTAMP;

-- 2) 个人空间 profile 正式列式表
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

INSERT INTO dtlms_user_profiles (
    username,
    full_name,
    role_name,
    department_name,
    phone_number,
    email,
    theme_color
)
SELECT
    rp.username,
    COALESCE(NULLIF(rp.payload ->> 'full_name', ''), u.full_name),
    COALESCE(NULLIF(rp.payload ->> 'role_name', ''), r.role_name, '未分配角色'),
    COALESCE(NULLIF(rp.payload ->> 'department_name', ''), ''),
    NULLIF(rp.payload ->> 'phone_number', ''),
    COALESCE(NULLIF(rp.payload ->> 'email', ''), u.email),
    COALESCE(NULLIF(rp.payload ->> 'theme_color', ''), '#0f4cbd')
FROM dtlms_runtime_profiles rp
LEFT JOIN dtlms_users u ON u.username = rp.username
LEFT JOIN dtlms_user_roles ur ON ur.user_id = u.id
LEFT JOIN dtlms_roles r ON r.id = ur.role_id AND r.is_deleted = FALSE
ON CONFLICT (username) DO UPDATE
SET full_name = EXCLUDED.full_name,
    role_name = EXCLUDED.role_name,
    department_name = EXCLUDED.department_name,
    phone_number = EXCLUDED.phone_number,
    email = EXCLUDED.email,
    theme_color = EXCLUDED.theme_color,
    updated_at = CURRENT_TIMESTAMP;

-- 3) 学生与团队历史 runtime 数据回填到正式表
WITH runtime_teams AS (
    SELECT id, payload
    FROM dtlms_runtime_teams
    WHERE payload IS NOT NULL
), normalized_teams AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'team_code'), '') AS team_code,
        NULLIF(BTRIM(payload ->> 'team_name'), '') AS team_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'department_name'), ''), '未分配院系') AS department_name,
        NULLIF(BTRIM(payload ->> 'discipline_name'), '') AS discipline_name,
        NULLIF(BTRIM(payload ->> 'lead_advisor_name'), '') AS lead_advisor_name,
        CASE
            WHEN jsonb_typeof(payload -> 'research_directions') = 'array' THEN (
                SELECT string_agg(NULLIF(BTRIM(value), ''), '、' ORDER BY ordinality)
                FROM jsonb_array_elements_text(payload -> 'research_directions') WITH ORDINALITY AS directions(value, ordinality)
                WHERE NULLIF(BTRIM(value), '') IS NOT NULL
            )
            ELSE NULLIF(BTRIM(payload ->> 'research_directions'), '')
        END AS research_directions,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '启用')
            WHEN '停用' THEN 'inactive'
            WHEN '筹建' THEN 'planning'
            WHEN '归档' THEN 'archived'
            ELSE 'active'
        END AS team_status,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(payload ->> 'created_on'), '') IS NOT NULL THEN (payload ->> 'created_on')::DATE END,
            CASE WHEN NULLIF(BTRIM(payload ->> 'established_on'), '') IS NOT NULL THEN (payload ->> 'established_on')::DATE END,
            CURRENT_DATE
        ) AS established_on,
        NULLIF(BTRIM(payload ->> 'description'), '') AS description,
        payload
    FROM runtime_teams
    WHERE NULLIF(BTRIM(payload ->> 'team_name'), '') IS NOT NULL
)
INSERT INTO dtlms_teams (
    id, team_code, team_name, department_name, discipline_name, lead_advisor_id,
    research_directions, team_status, established_on, description, is_deleted
)
SELECT
    nt.id,
    COALESCE(nt.team_code, CONCAT('CENTER-', LPAD(nt.id::TEXT, 3, '0'))),
    nt.team_name,
    nt.department_name,
    nt.discipline_name,
    advisor.id,
    nt.research_directions,
    nt.team_status,
    nt.established_on,
    nt.description,
    FALSE
FROM normalized_teams nt
LEFT JOIN dtlms_advisors advisor ON advisor.full_name = nt.lead_advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET team_code = EXCLUDED.team_code,
    team_name = EXCLUDED.team_name,
    department_name = EXCLUDED.department_name,
    discipline_name = EXCLUDED.discipline_name,
    lead_advisor_id = EXCLUDED.lead_advisor_id,
    research_directions = EXCLUDED.research_directions,
    team_status = EXCLUDED.team_status,
    established_on = EXCLUDED.established_on,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

WITH normalized_teams AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'lead_advisor_name'), '') AS lead_advisor_name,
        payload
    FROM dtlms_runtime_teams
    WHERE payload IS NOT NULL
      AND NULLIF(BTRIM(payload ->> 'team_name'), '') IS NOT NULL
), team_advisors_source AS (
    SELECT DISTINCT
        nt.id AS team_id,
        NULLIF(BTRIM(advisor_name), '') AS advisor_name,
        CASE
            WHEN NULLIF(BTRIM(advisor_name), '') = nt.lead_advisor_name THEN 'lead'
            ELSE 'member'
        END AS advisor_role,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(nt.payload ->> 'created_on'), '') IS NOT NULL THEN (nt.payload ->> 'created_on')::DATE END,
            CASE WHEN NULLIF(BTRIM(nt.payload ->> 'established_on'), '') IS NOT NULL THEN (nt.payload ->> 'established_on')::DATE END,
            CURRENT_DATE
        ) AS joined_on
    FROM normalized_teams nt
    CROSS JOIN LATERAL (
        SELECT value AS advisor_name
        FROM jsonb_array_elements_text(
            CASE
                WHEN jsonb_typeof(nt.payload -> 'advisor_names') = 'array' THEN nt.payload -> 'advisor_names'
                ELSE '[]'::jsonb
            END
        )
        UNION ALL
        SELECT nt.lead_advisor_name
        WHERE nt.lead_advisor_name IS NOT NULL
    ) source
    WHERE NULLIF(BTRIM(advisor_name), '') IS NOT NULL
)
INSERT INTO dtlms_team_advisors (team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted)
SELECT
    tas.team_id,
    advisor.id,
    tas.advisor_role,
    tas.joined_on,
    NULL,
    FALSE
FROM team_advisors_source tas
JOIN dtlms_advisors advisor ON advisor.full_name = tas.advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (team_id, advisor_id) DO UPDATE
SET advisor_role = EXCLUDED.advisor_role,
    joined_on = EXCLUDED.joined_on,
    left_on = NULL,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_students AS (
    SELECT id, payload
    FROM dtlms_runtime_students
    WHERE payload IS NOT NULL
), normalized_students AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'student_no'), '') AS student_no,
        NULLIF(BTRIM(payload ->> 'full_name'), '') AS full_name,
        NULLIF(BTRIM(payload ->> 'political_status'), '') AS political_status,
        NULLIF(BTRIM(payload ->> 'phone_number'), '') AS phone_number,
        CONCAT('ID-', COALESCE(NULLIF(BTRIM(payload ->> 'student_no'), ''), id::TEXT)) AS identity_no,
        COALESCE(NULLIF(BTRIM(payload ->> 'enrollment_year'), ''), '0')::INTEGER AS enrollment_year,
        NULLIF(BTRIM(payload ->> 'degree_type'), '') AS degree_type,
        NULLIF(BTRIM(payload ->> 'team_name'), '') AS team_name,
        NULLIF(BTRIM(payload ->> 'advisor_name'), '') AS advisor_name,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '在校')
            WHEN '外出研修' THEN 'outbound'
            WHEN '学位论文阶段' THEN 'thesis'
            WHEN '实习中' THEN 'internship'
            ELSE 'enrolled'
        END AS current_status
    FROM runtime_students
    WHERE NULLIF(BTRIM(payload ->> 'student_no'), '') IS NOT NULL
      AND NULLIF(BTRIM(payload ->> 'full_name'), '') IS NOT NULL
)
INSERT INTO dtlms_students (
    id, student_no, full_name, gender, political_status, phone_number, identity_no,
    enrollment_year, degree_type, team_id, current_status, primary_advisor_id, is_deleted
)
SELECT
    ns.id,
    ns.student_no,
    ns.full_name,
    '未知',
    ns.political_status,
    ns.phone_number,
    ns.identity_no,
    ns.enrollment_year,
    COALESCE(ns.degree_type, '博士'),
    team.id,
    ns.current_status,
    advisor.id,
    FALSE
FROM normalized_students ns
LEFT JOIN dtlms_teams team ON team.team_name = ns.team_name AND team.is_deleted = FALSE
LEFT JOIN dtlms_advisors advisor ON advisor.full_name = ns.advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET student_no = EXCLUDED.student_no,
    full_name = EXCLUDED.full_name,
    political_status = EXCLUDED.political_status,
    phone_number = EXCLUDED.phone_number,
    identity_no = EXCLUDED.identity_no,
    enrollment_year = EXCLUDED.enrollment_year,
    degree_type = EXCLUDED.degree_type,
    team_id = EXCLUDED.team_id,
    current_status = EXCLUDED.current_status,
    primary_advisor_id = EXCLUDED.primary_advisor_id,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

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
    '初始化迁移自 dtlms_runtime_students'
FROM dtlms_students s
WHERE s.is_deleted = FALSE
  AND s.team_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_student_team_history h
      WHERE h.student_id = s.id
        AND h.team_id = s.team_id
  );

-- 4) 系统治理关系化补齐
ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS department_name VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(32);
ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMPTZ;
ALTER TABLE dtlms_roles ADD COLUMN IF NOT EXISTS scope_name VARCHAR(128) NOT NULL DEFAULT '系统管理';

CREATE TABLE IF NOT EXISTS dtlms_audit_policies (
    id BIGINT PRIMARY KEY,
    item VARCHAR(128) NOT NULL,
    policy TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT '启用',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS dtlms_integrations (
    id BIGINT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    direction VARCHAR(64) NOT NULL,
    cadence VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT '正常',
    owner VARCHAR(128) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

WITH runtime_roles_source AS (
    SELECT DISTINCT ON (NULLIF(BTRIM(rr.payload ->> 'role_code'), ''))
        rr.id,
        NULLIF(BTRIM(rr.payload ->> 'role_code'), '') AS role_code,
        COALESCE(NULLIF(BTRIM(rr.payload ->> 'role_name'), ''), NULLIF(BTRIM(rr.payload ->> 'role_code'), ''), CONCAT('ROLE-', rr.id::TEXT)) AS role_name,
        COALESCE(NULLIF(BTRIM(rr.payload ->> 'scope_name'), ''), '系统管理') AS scope_name,
        NULLIF(BTRIM(rr.payload ->> 'description'), '') AS description
    FROM dtlms_runtime_roles rr
    WHERE rr.payload IS NOT NULL
      AND NULLIF(BTRIM(rr.payload ->> 'role_code'), '') IS NOT NULL
    ORDER BY NULLIF(BTRIM(rr.payload ->> 'role_code'), ''), rr.id
), updated_existing_roles AS (
    UPDATE dtlms_roles dr
    SET role_name = src.role_name,
        scope_name = src.scope_name,
        description = src.description,
        is_deleted = FALSE,
        updated_at = CURRENT_TIMESTAMP
    FROM runtime_roles_source src
    WHERE dr.role_code = src.role_code
    RETURNING src.id
)
INSERT INTO dtlms_roles (id, role_code, role_name, scope_name, description, is_deleted)
SELECT
    src.id,
    src.role_code,
    src.role_name,
    src.scope_name,
    src.description,
    FALSE
FROM runtime_roles_source src
LEFT JOIN updated_existing_roles updated ON updated.id = src.id
WHERE updated.id IS NULL
ON CONFLICT (id) DO UPDATE
SET role_code = EXCLUDED.role_code,
    role_name = EXCLUDED.role_name,
    scope_name = EXCLUDED.scope_name,
    description = EXCLUDED.description,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_roles_source AS (
    SELECT DISTINCT ON (NULLIF(BTRIM(rr.payload ->> 'role_code'), ''))
        rr.id,
        NULLIF(BTRIM(rr.payload ->> 'role_code'), '') AS role_code,
        rr.payload
    FROM dtlms_runtime_roles rr
    WHERE rr.payload IS NOT NULL
      AND NULLIF(BTRIM(rr.payload ->> 'role_code'), '') IS NOT NULL
    ORDER BY NULLIF(BTRIM(rr.payload ->> 'role_code'), ''), rr.id
)
INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT DISTINCT
    dr.id,
    p.id
FROM runtime_roles_source rr
JOIN dtlms_roles dr ON dr.role_code = rr.role_code AND dr.is_deleted = FALSE
JOIN LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(rr.payload -> 'permissions') = 'array' THEN rr.payload -> 'permissions'
        ELSE '[]'::jsonb
    END
) perm(permission_code) ON TRUE
JOIN dtlms_permissions p ON p.permission_code = perm.permission_code AND p.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_users (
    id, username, full_name, email, department_name, phone_number,
    password_hash, is_active, is_deleted, last_login_at
)
SELECT
    ru.id,
    NULLIF(BTRIM(ru.payload ->> 'username'), ''),
    COALESCE(NULLIF(BTRIM(ru.payload ->> 'full_name'), ''), NULLIF(BTRIM(ru.payload ->> 'username'), '')),
    up.email,
    COALESCE(NULLIF(BTRIM(ru.payload ->> 'department_name'), ''), ''),
    NULLIF(BTRIM(ru.payload ->> 'phone_number'), ''),
    NULLIF(ru.payload ->> 'password_hash', ''),
    CASE COALESCE(NULLIF(BTRIM(ru.payload ->> 'account_status'), ''), '启用')
        WHEN '停用' THEN FALSE
        ELSE TRUE
    END,
    FALSE,
    CASE WHEN NULLIF(BTRIM(ru.payload ->> 'last_login_at'), '') IS NULL THEN NULL ELSE (ru.payload ->> 'last_login_at')::TIMESTAMPTZ END
FROM dtlms_runtime_system_users ru
LEFT JOIN dtlms_user_profiles up ON up.username = NULLIF(BTRIM(ru.payload ->> 'username'), '')
WHERE ru.payload IS NOT NULL
  AND NULLIF(BTRIM(ru.payload ->> 'username'), '') IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET username = EXCLUDED.username,
    full_name = EXCLUDED.full_name,
    email = COALESCE(EXCLUDED.email, dtlms_users.email),
    department_name = EXCLUDED.department_name,
    phone_number = EXCLUDED.phone_number,
    password_hash = COALESCE(EXCLUDED.password_hash, dtlms_users.password_hash),
    is_active = EXCLUDED.is_active,
    is_deleted = FALSE,
    last_login_at = COALESCE(EXCLUDED.last_login_at, dtlms_users.last_login_at),
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
SELECT DISTINCT
    ru.id,
    r.id,
    'runtime_sync'
FROM dtlms_runtime_system_users ru
JOIN dtlms_roles r ON r.role_code = NULLIF(BTRIM(ru.payload ->> 'role_code'), '') AND r.is_deleted = FALSE
WHERE ru.payload IS NOT NULL
  AND NULLIF(BTRIM(ru.payload ->> 'username'), '') IS NOT NULL
ON CONFLICT (user_id, role_id) DO UPDATE
SET grant_source = EXCLUDED.grant_source,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_audit_policies (id, item, policy, status, is_deleted)
SELECT
    rap.id,
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'item'), ''), CONCAT('策略-', rap.id::TEXT)),
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'policy'), ''), ''),
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'status'), ''), '启用'),
    FALSE
FROM dtlms_runtime_audit_policies rap
WHERE rap.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET item = EXCLUDED.item,
    policy = EXCLUDED.policy,
    status = EXCLUDED.status,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_integrations (id, name, direction, cadence, status, owner, is_deleted)
SELECT
    ri.id,
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'name'), ''), CONCAT('集成-', ri.id::TEXT)),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'direction'), ''), '单向'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'cadence'), ''), '按需'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'status'), ''), '正常'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'owner'), ''), ''),
    FALSE
FROM dtlms_runtime_integrations ri
WHERE ri.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
    direction = EXCLUDED.direction,
    cadence = EXCLUDED.cadence,
    status = EXCLUDED.status,
    owner = EXCLUDED.owner,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

-- 5) 培养与学位数据关系化回填
WITH runtime_training_plans AS (
    SELECT id, payload
    FROM dtlms_runtime_training_plans
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_training_plans (
    id, student_id, advisor_id, version_no, report_cycle, plan_status,
    scientific_goal, assessment_rule, is_deleted
)
SELECT
    rtp.id,
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'version_no'), ''), 'v1.0'),
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'report_cycle'), ''), '每学期'),
    CASE COALESCE(NULLIF(BTRIM(rtp.payload ->> 'plan_status'), ''), '待学生确认')
        WHEN '执行中' THEN 'active'
        WHEN '已归档' THEN 'archived'
        ELSE 'draft'
    END,
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'scientific_goal'), ''), ''),
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'assessment_rule'), ''), ''),
    FALSE
FROM runtime_training_plans rtp
JOIN LATERAL (
    SELECT student.id
    FROM dtlms_students student
    WHERE student.student_no = NULLIF(BTRIM(rtp.payload ->> 'student_no'), '')
      AND student.is_deleted = FALSE
    ORDER BY student.id
    LIMIT 1
) s ON TRUE
JOIN LATERAL (
    SELECT advisor.id
    FROM dtlms_advisors advisor
    WHERE advisor.full_name = NULLIF(BTRIM(rtp.payload ->> 'advisor_name'), '')
      AND advisor.is_deleted = FALSE
    ORDER BY advisor.id
    LIMIT 1
) a ON TRUE
ON CONFLICT (id) DO UPDATE
SET student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    version_no = EXCLUDED.version_no,
    report_cycle = EXCLUDED.report_cycle,
    plan_status = EXCLUDED.plan_status,
    scientific_goal = EXCLUDED.scientific_goal,
    assessment_rule = EXCLUDED.assessment_rule,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_training_plan_versions (training_plan_id, version_no, change_reason, plan_snapshot)
SELECT
    tp.id,
    tp.version_no,
    '生产环境关系化回填',
    tp.scientific_goal
FROM dtlms_training_plans tp
WHERE tp.is_deleted = FALSE
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_training_plan_versions tpv
      WHERE tpv.training_plan_id = tp.id
        AND tpv.version_no = tp.version_no
  );

WITH runtime_reports AS (
    SELECT id, payload
    FROM dtlms_runtime_scientific_reports
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_scientific_reports (
    id, business_key, student_id, training_plan_id, period_label, report_status,
    summary, attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
)
SELECT
    rr.id,
    NULLIF(BTRIM(rr.payload ->> 'business_key'), ''),
    s.id,
    tp.id,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'period_label'), ''), ''),
    CASE COALESCE(NULLIF(BTRIM(rr.payload ->> 'report_status'), ''), '待导师审阅')
        WHEN '已归档' THEN 'archived'
        WHEN '已通过' THEN 'approved'
        WHEN '退回修改' THEN 'returned'
        ELSE 'submitted'
    END,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'summary'), ''), ''),
    CONCAT('/reports/', rr.payload ->> 'student_no', '/', COALESCE(NULLIF(BTRIM(rr.payload ->> 'period_label'), ''), 'report'), '.pdf'),
    reviewer.id,
    CASE WHEN NULLIF(BTRIM(rr.payload ->> 'review_score'), '') IS NULL THEN NULL ELSE (rr.payload ->> 'review_score')::NUMERIC(5,2) END,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'review_comment'), ''), NULLIF(BTRIM(rr.payload ->> 'latest_comment'), '')),
    FALSE
FROM runtime_reports rr
JOIN LATERAL (
    SELECT student.id
    FROM dtlms_students student
    WHERE student.student_no = NULLIF(BTRIM(rr.payload ->> 'student_no'), '')
      AND student.is_deleted = FALSE
    ORDER BY student.id
    LIMIT 1
) s ON TRUE
JOIN LATERAL (
    SELECT training_plan.id
    FROM dtlms_training_plans training_plan
    WHERE training_plan.student_id = s.id
      AND training_plan.is_deleted = FALSE
    ORDER BY training_plan.id
    LIMIT 1
) tp ON TRUE
LEFT JOIN LATERAL (
    SELECT advisor.id
    FROM dtlms_advisors advisor
    WHERE advisor.full_name = NULLIF(BTRIM(rr.payload ->> 'reviewer_name'), '')
      AND advisor.is_deleted = FALSE
    ORDER BY advisor.id
    LIMIT 1
) reviewer ON TRUE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    training_plan_id = EXCLUDED.training_plan_id,
    period_label = EXCLUDED.period_label,
    report_status = EXCLUDED.report_status,
    summary = EXCLUDED.summary,
    attachment_url = EXCLUDED.attachment_url,
    reviewer_advisor_id = EXCLUDED.reviewer_advisor_id,
    review_score = EXCLUDED.review_score,
    review_comment = EXCLUDED.review_comment,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_outbound AS (
    SELECT id, payload
    FROM dtlms_runtime_outbound_studies
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_outbound_studies (
    id, business_key, student_id, advisor_id, study_type, destination,
    start_date, end_date, approval_status, expected_outcome, is_deleted
)
SELECT
    ros.id,
    NULLIF(BTRIM(ros.payload ->> 'business_key'), ''),
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(ros.payload ->> 'study_type'), ''), ''),
    COALESCE(NULLIF(BTRIM(ros.payload ->> 'destination'), ''), ''),
    CASE WHEN NULLIF(BTRIM(ros.payload ->> 'start_date'), '') IS NULL THEN NULL ELSE (ros.payload ->> 'start_date')::DATE END,
    CASE WHEN NULLIF(BTRIM(ros.payload ->> 'end_date'), '') IS NULL THEN NULL ELSE (ros.payload ->> 'end_date')::DATE END,
    CASE COALESCE(NULLIF(BTRIM(ros.payload ->> 'approval_status'), ''), '审批中')
        WHEN '已完成' THEN 'completed'
        WHEN '已驳回' THEN 'rejected'
        WHEN '研修中' THEN 'approved'
        ELSE 'submitted'
    END,
    NULLIF(BTRIM(ros.payload ->> 'expected_outcome'), ''),
    FALSE
FROM runtime_outbound ros
JOIN LATERAL (
    SELECT student.id
    FROM dtlms_students student
    WHERE student.student_no = NULLIF(BTRIM(ros.payload ->> 'student_no'), '')
      AND student.is_deleted = FALSE
    ORDER BY student.id
    LIMIT 1
) s ON TRUE
JOIN LATERAL (
    SELECT advisor.id
    FROM dtlms_advisors advisor
    WHERE advisor.full_name = NULLIF(BTRIM(ros.payload ->> 'advisor_name'), '')
      AND advisor.is_deleted = FALSE
    ORDER BY advisor.id
    LIMIT 1
) a ON TRUE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    study_type = EXCLUDED.study_type,
    destination = EXCLUDED.destination,
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    approval_status = EXCLUDED.approval_status,
    expected_outcome = EXCLUDED.expected_outcome,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_theses AS (
    SELECT id, payload
    FROM dtlms_runtime_theses
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_theses (
    id, business_key, student_id, advisor_id, title, plagiarism_rate,
    thesis_status, blind_review_status, defense_date, degree_granted, is_deleted
)
SELECT
    rt.id,
    NULLIF(BTRIM(rt.payload ->> 'business_key'), ''),
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(rt.payload ->> 'title'), ''), ''),
    CASE WHEN NULLIF(BTRIM(rt.payload ->> 'plagiarism_rate'), '') IS NULL THEN NULL ELSE (rt.payload ->> 'plagiarism_rate')::NUMERIC(5,2) END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'thesis_status'), ''), '待查重')
        WHEN '已完成' THEN 'completed'
        WHEN '撰写中' THEN 'drafting'
        WHEN '查重中' THEN 'plagiarism_check'
        ELSE 'draft'
    END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'blind_review_status'), ''), '未送审')
        WHEN '通过' THEN 'passed'
        WHEN '未通过' THEN 'failed'
        WHEN '进行中' THEN 'in_review'
        ELSE 'not_started'
    END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'defense_status'), ''), '未进入')
        WHEN '已完成' THEN CURRENT_DATE
        ELSE NULL
    END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'degree_status'), ''), '待申请')
        WHEN '已授位' THEN TRUE
        ELSE FALSE
    END,
    FALSE
FROM runtime_theses rt
JOIN LATERAL (
    SELECT student.id
    FROM dtlms_students student
    WHERE student.student_no = NULLIF(BTRIM(rt.payload ->> 'student_no'), '')
      AND student.is_deleted = FALSE
    ORDER BY student.id
    LIMIT 1
) s ON TRUE
JOIN LATERAL (
    SELECT advisor.id
    FROM dtlms_advisors advisor
    WHERE advisor.full_name = NULLIF(BTRIM(rt.payload ->> 'advisor_name'), '')
      AND advisor.is_deleted = FALSE
    ORDER BY advisor.id
    LIMIT 1
) a ON TRUE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    title = EXCLUDED.title,
    plagiarism_rate = EXCLUDED.plagiarism_rate,
    thesis_status = EXCLUDED.thesis_status,
    blind_review_status = EXCLUDED.blind_review_status,
    defense_date = EXCLUDED.defense_date,
    degree_granted = EXCLUDED.degree_granted,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_thesis_reviews (id, thesis_id, expert_name, review_score, review_status, review_comment)
SELECT
    tr.id,
    COALESCE((tr.payload ->> 'thesis_id')::BIGINT, 0),
    COALESCE(NULLIF(BTRIM(tr.payload ->> 'expert_name'), ''), ''),
    CASE WHEN NULLIF(BTRIM(tr.payload ->> 'review_score'), '') IS NULL THEN NULL ELSE (tr.payload ->> 'review_score')::NUMERIC(5,2) END,
    CASE COALESCE(NULLIF(BTRIM(tr.payload ->> 'review_status'), ''), '待提交')
        WHEN '已退回' THEN 'returned'
        WHEN '已完成' THEN 'completed'
        ELSE 'pending'
    END,
    NULLIF(BTRIM(tr.payload ->> 'review_comment'), '')
FROM dtlms_runtime_thesis_reviews tr
WHERE tr.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET thesis_id = EXCLUDED.thesis_id,
    expert_name = EXCLUDED.expert_name,
    review_score = EXCLUDED.review_score,
    review_status = EXCLUDED.review_status,
    review_comment = EXCLUDED.review_comment,
    updated_at = CURRENT_TIMESTAMP;

-- 6) 工作流兼容表回填，支撑审批中心改读 Flowable 兼容表
WITH runtime_tasks AS (
    SELECT id, payload
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
), normalized_tasks AS (
    SELECT
        id,
        payload,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_node'), ''), '待处理') AS current_node,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(NULLIF(BTRIM(payload ->> 'applicant_name'), ''), '未知申请人') AS applicant_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_handler'), ''), '待分派') AS current_handler,
        NULLIF(BTRIM(payload ->> 'form_summary'), '') AS form_summary,
        NULLIF(BTRIM(payload ->> 'latest_comment'), '') AS latest_comment,
        CASE WHEN NULLIF(BTRIM(payload ->> 'entity_id'), '') IS NULL THEN 0 ELSE (payload ->> 'entity_id')::BIGINT END AS entity_id,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END,
            CURRENT_TIMESTAMP
        ) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中')
            WHEN '低' THEN 25
            WHEN '高' THEN 75
            WHEN '紧急' THEN 100
            ELSE 50
        END AS priority_value,
        CASE
            WHEN jsonb_typeof(payload -> 'candidate_groups') = 'array' THEN payload -> 'candidate_groups'
            ELSE '[]'::jsonb
        END AS candidate_groups,
        CASE
            WHEN jsonb_typeof(payload -> 'history') = 'array' THEN payload -> 'history'
            ELSE '[]'::jsonb
        END AS history_entries,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('DEPLOY-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow')) AS deployment_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM runtime_tasks
)
INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_)
SELECT DISTINCT
    deployment_id,
    workflow_name,
    business_module,
    flow_code,
    created_at
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET name_ = EXCLUDED.name_,
    category_ = EXCLUDED.category_,
    key_ = EXCLUDED.key_,
    deploy_time_ = EXCLUDED.deploy_time_;

WITH normalized_tasks AS (
    SELECT
        id,
        payload,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('DEPLOY-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow')) AS deployment_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_re_procdef (
    id_, key_, version_, deployment_id_, resource_name_, diagram_resource_name_, name_, category_, description_, suspension_state_
)
SELECT DISTINCT
    proc_def_id,
    flow_code,
    1,
    deployment_id,
    CONCAT(flow_code, '.bpmn20.xml'),
    CONCAT(flow_code, '.png'),
    workflow_name,
    business_module,
    CONCAT(workflow_name, ' 定义'),
    1
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET key_ = EXCLUDED.key_,
    deployment_id_ = EXCLUDED.deployment_id_,
    resource_name_ = EXCLUDED.resource_name_,
    diagram_resource_name_ = EXCLUDED.diagram_resource_name_,
    name_ = EXCLUDED.name_,
    category_ = EXCLUDED.category_,
    description_ = EXCLUDED.description_;

WITH normalized_tasks AS (
    SELECT
        id,
        payload,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_node'), ''), '待处理') AS current_node,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(NULLIF(BTRIM(payload ->> 'applicant_name'), ''), '未知申请人') AS applicant_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_handler'), ''), '待分派') AS current_handler,
        NULLIF(BTRIM(payload ->> 'form_summary'), '') AS form_summary,
        NULLIF(BTRIM(payload ->> 'latest_comment'), '') AS latest_comment,
        CASE WHEN NULLIF(BTRIM(payload ->> 'entity_id'), '') IS NULL THEN 0 ELSE (payload ->> 'entity_id')::BIGINT END AS entity_id,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END,
            CURRENT_TIMESTAMP
        ) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中')
            WHEN '低' THEN 25
            WHEN '高' THEN 75
            WHEN '紧急' THEN 100
            ELSE 50
        END AS priority_value,
        CASE
            WHEN jsonb_typeof(payload -> 'candidate_groups') = 'array' THEN payload -> 'candidate_groups'
            ELSE '[]'::jsonb
        END AS candidate_groups,
        CASE
            WHEN jsonb_typeof(payload -> 'history') = 'array' THEN payload -> 'history'
            ELSE '[]'::jsonb
        END AS history_entries,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_hi_procinst (
    id_, proc_inst_id_, business_key_, proc_def_id_, start_time_, end_time_, duration_ms_,
    start_user_id_, end_act_id_, delete_reason_, start_act_id_, state_
)
SELECT DISTINCT
    proc_inst_id,
    proc_inst_id,
    business_key,
    proc_def_id,
    created_at,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN COALESCE(due_at, created_at) ELSE NULL END,
    NULL,
    NULL,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN node_key ELSE NULL END,
    CASE WHEN task_status = '已驳回' THEN 'rejected' ELSE NULL END,
    'startEvent',
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN 'COMPLETED' ELSE 'ACTIVE' END
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET business_key_ = EXCLUDED.business_key_,
    proc_def_id_ = EXCLUDED.proc_def_id_,
    start_time_ = EXCLUDED.start_time_,
    end_time_ = EXCLUDED.end_time_,
    end_act_id_ = EXCLUDED.end_act_id_,
    delete_reason_ = EXCLUDED.delete_reason_,
    state_ = EXCLUDED.state_;

WITH normalized_tasks AS (
    SELECT
        id,
        payload,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END,
            CURRENT_TIMESTAMP
        ) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中')
            WHEN '低' THEN 25
            WHEN '高' THEN 75
            WHEN '紧急' THEN 100
            ELSE 50
        END AS priority_value,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_hi_taskinst (
    id_, task_def_key_, proc_def_id_, proc_inst_id_, exec_id_, name_, business_key_, assignee_, owner_,
    start_time_, claim_time_, end_time_, duration_ms_, due_date_, delete_reason_, priority_, category_
)
SELECT
    CONCAT('TASK-', id::TEXT),
    node_key,
    proc_def_id,
    proc_inst_id,
    exec_id,
    task_title,
    business_key,
    NULL,
    NULL,
    created_at,
    NULL,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN COALESCE(due_at, created_at) ELSE NULL END,
    NULL,
    due_at,
    CASE WHEN task_status = '已驳回' THEN 'rejected' ELSE NULL END,
    priority_value,
    business_module
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET task_def_key_ = EXCLUDED.task_def_key_,
    proc_def_id_ = EXCLUDED.proc_def_id_,
    proc_inst_id_ = EXCLUDED.proc_inst_id_,
    exec_id_ = EXCLUDED.exec_id_,
    name_ = EXCLUDED.name_,
    business_key_ = EXCLUDED.business_key_,
    start_time_ = EXCLUDED.start_time_,
    end_time_ = EXCLUDED.end_time_,
    due_date_ = EXCLUDED.due_date_,
    priority_ = EXCLUDED.priority_,
    category_ = EXCLUDED.category_;

WITH normalized_tasks AS (
    SELECT
        id,
        payload,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_node'), ''), '待处理') AS current_node,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'applicant_name'), ''), '未知申请人') AS applicant_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_handler'), ''), '待分派') AS current_handler,
        NULLIF(BTRIM(payload ->> 'form_summary'), '') AS form_summary,
        NULLIF(BTRIM(payload ->> 'latest_comment'), '') AS latest_comment,
        CASE WHEN NULLIF(BTRIM(payload ->> 'entity_id'), '') IS NULL THEN 0 ELSE (payload ->> 'entity_id')::BIGINT END AS entity_id,
        CASE
            WHEN jsonb_typeof(payload -> 'candidate_groups') = 'array' THEN payload -> 'candidate_groups'
            ELSE '[]'::jsonb
        END AS candidate_groups,
        CASE
            WHEN jsonb_typeof(payload -> 'history') = 'array' THEN payload -> 'history'
            ELSE '[]'::jsonb
        END AS history_entries,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
), variable_rows AS (
    SELECT CONCAT('HVAR-', nt.id::TEXT, '-businessKey') AS id_, nt.proc_inst_id, nt.exec_id, 'businessKey' AS name_, 'string' AS var_type_, to_jsonb(nt.business_key) AS json_value_, nt.business_key AS text_value_ FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-workflowName'), nt.proc_inst_id, nt.exec_id, 'workflowName', 'string', to_jsonb(nt.workflow_name), nt.workflow_name FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-businessModule'), nt.proc_inst_id, nt.exec_id, 'businessModule', 'string', to_jsonb(nt.business_module), nt.business_module FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-applicantName'), nt.proc_inst_id, nt.exec_id, 'applicantName', 'string', to_jsonb(nt.applicant_name), nt.applicant_name FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-currentHandler'), nt.proc_inst_id, nt.exec_id, 'currentHandler', 'string', to_jsonb(nt.current_handler), nt.current_handler FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-currentNode'), nt.proc_inst_id, nt.exec_id, 'currentNode', 'string', to_jsonb(nt.current_node), nt.current_node FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-nodeKey'), nt.proc_inst_id, nt.exec_id, 'nodeKey', 'string', to_jsonb(nt.node_key), nt.node_key FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-taskStatus'), nt.proc_inst_id, nt.exec_id, 'taskStatus', 'string', to_jsonb(nt.task_status), nt.task_status FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-formSummary'), nt.proc_inst_id, nt.exec_id, 'formSummary', 'string', to_jsonb(nt.form_summary), nt.form_summary FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-latestComment'), nt.proc_inst_id, nt.exec_id, 'latestComment', 'string', to_jsonb(nt.latest_comment), nt.latest_comment FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-flowCode'), nt.proc_inst_id, nt.exec_id, 'flowCode', 'string', to_jsonb(nt.flow_code), nt.flow_code FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-entityId'), nt.proc_inst_id, nt.exec_id, 'entityId', 'long', to_jsonb(nt.entity_id), nt.entity_id::TEXT FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-candidateGroups'), nt.proc_inst_id, nt.exec_id, 'candidateGroups', 'json', nt.candidate_groups, NULL FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-historyEntries'), nt.proc_inst_id, nt.exec_id, 'historyEntries', 'json', nt.history_entries, NULL FROM normalized_tasks nt
)
INSERT INTO dtlms_wf_hi_varinst (id_, proc_inst_id_, exec_id_, name_, var_type_, text_value_, json_value_, create_time_, last_updated_time_)
SELECT
    vr.id_,
    vr.proc_inst_id,
    vr.exec_id,
    vr.name_,
    vr.var_type_,
    vr.text_value_,
    vr.json_value_,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM variable_rows vr
ON CONFLICT (id_) DO UPDATE
SET text_value_ = EXCLUDED.text_value_,
    json_value_ = EXCLUDED.json_value_,
    last_updated_time_ = CURRENT_TIMESTAMP;

-- 7) 门户 3.8 成果经历结构补齐
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'dtlms_portal_application_achievement_records'
    ) THEN
        ALTER TABLE public.dtlms_portal_application_achievement_records
            ADD COLUMN IF NOT EXISTS achievement_month VARCHAR(16),
            ADD COLUMN IF NOT EXISTS award_rank VARCHAR(64),
            ADD COLUMN IF NOT EXISTS award_certificate_attachment_url VARCHAR(512),
            ADD COLUMN IF NOT EXISTS description_text TEXT;
    END IF;
END $$;

-- 8) 门户 3.9 个人陈述与附件结构补齐
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'dtlms_portal_application_personal_statements'
    ) THEN
        ALTER TABLE public.dtlms_portal_application_personal_statements
            ADD COLUMN IF NOT EXISTS growth_experience_text TEXT,
            ADD COLUMN IF NOT EXISTS program_application_reason_text TEXT,
            ADD COLUMN IF NOT EXISTS career_plan_text TEXT,
            ADD COLUMN IF NOT EXISTS supporting_material_attachment_url TEXT;

        UPDATE public.dtlms_portal_application_personal_statements AS ps
        SET growth_experience_text = COALESCE(NULLIF(ps.growth_experience_text, ''), NULLIF(ps.personal_statement_text, '')),
            program_application_reason_text = COALESCE(NULLIF(ps.program_application_reason_text, ''), NULLIF(ps.ai_problem_statement, '')),
            career_plan_text = COALESCE(NULLIF(ps.career_plan_text, ''), NULLIF(ps.ai_industry_opinion, '')),
            supporting_material_attachment_url = COALESCE(
                NULLIF(ps.supporting_material_attachment_url, ''),
                (
                    SELECT NULLIF(ra.material_list_attachment, '')
                    FROM public.dtlms_recruitment_applications AS ra
                    WHERE ra.id = ps.application_id
                )
            )
        WHERE ps.growth_experience_text IS NULL
           OR ps.growth_experience_text = ''
           OR ps.program_application_reason_text IS NULL
           OR ps.program_application_reason_text = ''
           OR ps.career_plan_text IS NULL
           OR ps.career_plan_text = ''
           OR ps.supporting_material_attachment_url IS NULL
           OR ps.supporting_material_attachment_url = '';

        UPDATE public.dtlms_portal_application_personal_statements AS ps
        SET personal_statement_text = CONCAT_WS(
                E'\n\n',
                CASE WHEN NULLIF(ps.growth_experience_text, '') IS NOT NULL THEN '个人成长经历：' || ps.growth_experience_text END,
                CASE WHEN NULLIF(ps.program_application_reason_text, '') IS NOT NULL THEN '为何申报本项目或本专业：' || ps.program_application_reason_text END,
                CASE WHEN NULLIF(ps.career_plan_text, '') IS NOT NULL THEN '未来职业发展规划：' || ps.career_plan_text END
            )
        WHERE COALESCE(NULLIF(ps.personal_statement_text, ''), '') = ''
          AND (
                NULLIF(ps.growth_experience_text, '') IS NOT NULL
                OR NULLIF(ps.program_application_reason_text, '') IS NOT NULL
                OR NULLIF(ps.career_plan_text, '') IS NOT NULL
            );
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'dtlms_portal_application_declarations'
    ) THEN
        UPDATE public.dtlms_portal_application_declarations
        SET declaration_text = '本表及证明材料仅作为申请上海人工智能实验室联培博士项目的参考依据，并承诺提交材料的所有内容均真实、准确、完整。所提供的材料中如有任何不实信息，将被取消录取资格。'
        WHERE declaration_text IS NULL
           OR declaration_text = ''
           OR declaration_text = '我已同意并仔细阅读使用条款和隐私政策。';
    END IF;
END $$;

COMMIT;

-- 9) 研究中心 / 导师 / 导师账号增量补录（合并自 056_seed_research_centers_and_advisors.sql）
BEGIN;

-- 执行前提：
-- 1. 已完成 010/015/023/028/030/040 等基础建表与 RBAC 初始化。
-- 2. 若现网已存在 runtime state，本脚本会同步更新 runtime 表；
--    若 dtlms_runtime_counters 为空，则只写关系表，不主动初始化 runtime state。
-- 3. 导师账号默认密码为 ChangeMe@123，下面是其 pbkdf2_sha256 哈希。

CREATE TEMP TABLE tmp_center_seed (
    seed_order INTEGER PRIMARY KEY,
    center_name VARCHAR(128) NOT NULL,
    director_name VARCHAR(128) NOT NULL,
    advisor_names TEXT[] NOT NULL
) ON COMMIT DROP;

INSERT INTO tmp_center_seed (seed_order, center_name, director_name, advisor_names)
VALUES
    (1, '前沿探索中心', '乔宇', ARRAY['乔宇', '周伯文', '成宇', '石博天', '薛天帆', '蔡品隆', '邹娜', '刘翼豪', '何军军', '陈昕苑', '胡杨', '张超']),
    (2, 'AI For Science中心', '白磊', ARRAY['白磊', '周伯文', '欧阳万里', '张铂', '李玉强', '董楠卿', '宋纯锋', '胡舒悦', '王潚崧', '郝红霞']),
    (3, '大模型中心', '陈恺', ARRAY['陈恺', '周伯文', '林达华', '王利民', '张文蔚', '郭琦鹏', '王毅', '李亦宁', '张超', '张奇']),
    (4, '物理智能中心', '张伟楠', ARRAY['张伟楠', '周伯文', '沈春华', '翟少鹏', '赵斌', '吕照阳', '穆尧', '沈渊']),
    (5, '安全可信AI中心', '胡侠', ARRAY['胡侠', '周伯文', '陆超超', '邵婧', '王迎春', '杨超', '滕妍', '瞿晶晶']),
    (6, '评测中心', '翟广涛', ARRAY['翟广涛', '周伯文', '胡侠']),
    (7, 'Data-CentricAI', '何聪辉', ARRAY['何聪辉', '周伯文', '林达华', '王斌', '吴郦军', '吴江', '邱剑涛']),
    (8, '系统平台中心', '林达华', ARRAY['林达华', '周伯文', '李恒杰']);

CREATE TEMP TABLE tmp_username_seed (
    full_name VARCHAR(128) PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE
) ON COMMIT DROP;

INSERT INTO tmp_username_seed (full_name, username)
VALUES
    ('乔宇', 'qiaoyu'),
    ('周伯文', 'zhoubowen'),
    ('成宇', 'chengyu'),
    ('石博天', 'shibotian'),
    ('薛天帆', 'xuetianfan'),
    ('蔡品隆', 'caipinlong'),
    ('邹娜', 'zouna'),
    ('刘翼豪', 'liuyihao'),
    ('何军军', 'hejunjun'),
    ('陈昕苑', 'chenxinyuan'),
    ('胡杨', 'huyang'),
    ('张超', 'zhangchao'),
    ('白磊', 'bailei'),
    ('欧阳万里', 'ouyangwanli'),
    ('张铂', 'zhangbo'),
    ('李玉强', 'liyuqiang'),
    ('董楠卿', 'dongnanqing'),
    ('宋纯锋', 'songchunfeng'),
    ('胡舒悦', 'hushuyue'),
    ('王潚崧', 'wangsusong'),
    ('郝红霞', 'haohongxia'),
    ('陈恺', 'chenkai'),
    ('林达华', 'lindahua'),
    ('王利民', 'wanglimin'),
    ('张文蔚', 'zhangwenwei'),
    ('郭琦鹏', 'guoqipeng'),
    ('王毅', 'wangyi'),
    ('李亦宁', 'liyining'),
    ('张奇', 'zhangqi'),
    ('张伟楠', 'zhangweinan'),
    ('沈春华', 'shenchunhua'),
    ('翟少鹏', 'dishaopeng'),
    ('赵斌', 'zhaobin'),
    ('吕照阳', 'lvzhaoyang'),
    ('穆尧', 'muyao'),
    ('沈渊', 'shenyuan'),
    ('胡侠', 'huxia'),
    ('陆超超', 'luchaochao'),
    ('邵婧', 'shaojing'),
    ('王迎春', 'wangyingchun'),
    ('杨超', 'yangchao'),
    ('滕妍', 'tengyan'),
    ('瞿晶晶', 'qujingjing'),
    ('翟广涛', 'diguangtao'),
    ('何聪辉', 'heconghui'),
    ('王斌', 'wangbin'),
    ('吴郦军', 'wulijun'),
    ('吴江', 'wujiang'),
    ('邱剑涛', 'qiujiantao'),
    ('李恒杰', 'lihengjie');

CREATE TEMP TABLE tmp_advisor_seed ON COMMIT DROP AS
WITH expanded AS (
    SELECT DISTINCT
        c.seed_order,
        c.center_name,
        c.director_name,
        advisor_name
    FROM tmp_center_seed AS c
    CROSS JOIN LATERAL unnest(c.advisor_names) AS advisor_name
), center_agg AS (
    SELECT
        advisor_name AS full_name,
        array_agg(center_name ORDER BY seed_order) AS center_names,
        array_agg(center_name ORDER BY seed_order) FILTER (WHERE advisor_name = director_name) AS lead_center_names
    FROM expanded
    GROUP BY advisor_name
)
SELECT
    u.full_name,
    u.username,
    CASE
        WHEN COALESCE(array_length(ca.lead_center_names, 1), 0) > 0 THEN ca.lead_center_names[1]
        WHEN COALESCE(array_length(ca.center_names, 1), 0) = 1 THEN ca.center_names[1]
        ELSE '多中心联合'
    END AS department_name,
    array_to_string(ca.center_names, '、') AS research_direction
FROM tmp_username_seed AS u
JOIN center_agg AS ca ON ca.full_name = u.full_name;

INSERT INTO dtlms_roles (role_code, role_name, scope_name, description, is_deleted)
VALUES ('advisor', '导师', '培养与学位', '培养方案制定、报告审阅、答辩指导', FALSE)
ON CONFLICT (role_code) DO UPDATE
SET role_name = EXCLUDED.role_name,
    scope_name = EXCLUDED.scope_name,
    description = EXCLUDED.description,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

UPDATE dtlms_advisors AS a
SET title = '导师',
    organization_name = s.department_name,
    research_direction = s.research_direction,
    annual_quota = 0,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
WHERE a.full_name = s.full_name;

WITH advisor_no_base AS (
    SELECT COALESCE(MAX(CAST(SUBSTRING(advisor_no FROM 4) AS INTEGER)), 0) AS max_no
    FROM dtlms_advisors
    WHERE advisor_no ~ '^ADV[0-9]+$'
), missing_advisors AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (ORDER BY s.full_name) AS rn
    FROM tmp_advisor_seed AS s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dtlms_advisors AS a
        WHERE a.full_name = s.full_name
    )
)
INSERT INTO dtlms_advisors (
    advisor_no,
    full_name,
    title,
    organization_name,
    research_direction,
    annual_quota,
    is_deleted
)
SELECT
    CONCAT('ADV', LPAD((b.max_no + m.rn)::TEXT, 3, '0')),
    m.full_name,
    '导师',
    m.department_name,
    m.research_direction,
    0,
    FALSE
FROM missing_advisors AS m
CROSS JOIN advisor_no_base AS b;

UPDATE dtlms_users AS u
SET full_name = s.full_name,
    email = COALESCE(NULLIF(u.email, ''), CONCAT(s.username, '@dtlms.local')),
    department_name = s.department_name,
    password_hash = COALESCE(NULLIF(u.password_hash, ''), '$pbkdf2-sha256$29000$ESIkZKwVorQ2Ziyl9N77Xw$FkNpUi.BNeyqPLVId/t5Lz8zI0V1H7AbVTwDtfY.CNM'),
    is_active = TRUE,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
WHERE u.username = s.username;

INSERT INTO dtlms_users (
    username,
    full_name,
    email,
    department_name,
    phone_number,
    password_hash,
    is_active,
    is_deleted,
    last_login_at
)
SELECT
    s.username,
    s.full_name,
    CONCAT(s.username, '@dtlms.local'),
    s.department_name,
    NULL,
    '$pbkdf2-sha256$29000$ESIkZKwVorQ2Ziyl9N77Xw$FkNpUi.BNeyqPLVId/t5Lz8zI0V1H7AbVTwDtfY.CNM',
    TRUE,
    FALSE,
    NULL
FROM tmp_advisor_seed AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_users AS u
    WHERE u.username = s.username
);

WITH advisor_role AS (
    SELECT id
    FROM dtlms_roles
    WHERE role_code = 'advisor'
      AND is_deleted = FALSE
    ORDER BY id
    LIMIT 1
)
INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
SELECT
    u.id,
    r.id,
    'seed_research_centers'
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
CROSS JOIN advisor_role AS r
ON CONFLICT (user_id, role_id) DO UPDATE
SET grant_source = EXCLUDED.grant_source,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_user_profiles (
    username,
    full_name,
    role_name,
    department_name,
    phone_number,
    email,
    theme_color
)
SELECT
    u.username,
    s.full_name,
    '导师',
    s.department_name,
    u.phone_number,
    COALESCE(NULLIF(up.email, ''), NULLIF(u.email, ''), CONCAT(u.username, '@dtlms.local')),
    '#13795b'
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
ON CONFLICT (username) DO UPDATE
SET full_name = EXCLUDED.full_name,
    role_name = EXCLUDED.role_name,
    department_name = EXCLUDED.department_name,
    phone_number = COALESCE(dtlms_user_profiles.phone_number, EXCLUDED.phone_number),
    email = COALESCE(dtlms_user_profiles.email, EXCLUDED.email),
    theme_color = EXCLUDED.theme_color,
    updated_at = CURRENT_TIMESTAMP;

UPDATE dtlms_teams AS t
SET department_name = s.center_name,
    discipline_name = COALESCE(NULLIF(t.discipline_name, ''), '未分配学科'),
    lead_advisor_id = a.id,
    research_directions = NULL,
    team_status = 'active',
    established_on = COALESCE(t.established_on, CURRENT_DATE),
    description = '按研究中心主数据维护需求批量导入。',
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_center_seed AS s
LEFT JOIN dtlms_advisors AS a
    ON a.full_name = s.director_name
   AND a.is_deleted = FALSE
WHERE t.team_name = s.center_name;

WITH team_code_base AS (
    SELECT COALESCE(MAX(CAST(SUBSTRING(team_code FROM 8) AS INTEGER)), 0) AS max_no
    FROM dtlms_teams
    WHERE team_code ~ '^CENTER-[0-9]+$'
), missing_teams AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (ORDER BY s.seed_order) AS rn
    FROM tmp_center_seed AS s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dtlms_teams AS t
        WHERE t.team_name = s.center_name
    )
)
INSERT INTO dtlms_teams (
    team_code,
    team_name,
    department_name,
    discipline_name,
    lead_advisor_id,
    research_directions,
    team_status,
    established_on,
    description,
    is_deleted
)
SELECT
    CONCAT('CENTER-', LPAD((b.max_no + m.rn)::TEXT, 3, '0')),
    m.center_name,
    m.center_name,
    '未分配学科',
    a.id,
    NULL,
    'active',
    CURRENT_DATE,
    '按研究中心主数据维护需求批量导入。',
    FALSE
FROM missing_teams AS m
CROSS JOIN team_code_base AS b
LEFT JOIN dtlms_advisors AS a
    ON a.full_name = m.director_name
   AND a.is_deleted = FALSE;

DELETE FROM dtlms_team_advisors AS ta
USING dtlms_teams AS t, tmp_center_seed AS s
WHERE ta.team_id = t.id
  AND t.team_name = s.center_name;

INSERT INTO dtlms_team_advisors (
    team_id,
    advisor_id,
    advisor_role,
    joined_on,
    left_on,
    is_deleted
)
SELECT
    t.id,
    a.id,
    CASE
        WHEN names.advisor_name = s.director_name THEN 'lead'
        ELSE 'member'
    END,
    COALESCE(t.established_on, CURRENT_DATE),
    NULL,
    FALSE
FROM tmp_center_seed AS s
JOIN dtlms_teams AS t ON t.team_name = s.center_name
CROSS JOIN LATERAL unnest(s.advisor_names) AS names(advisor_name)
JOIN dtlms_advisors AS a
    ON a.full_name = names.advisor_name
   AND a.is_deleted = FALSE
ON CONFLICT (team_id, advisor_id) DO UPDATE
SET advisor_role = EXCLUDED.advisor_role,
    joined_on = EXCLUDED.joined_on,
    left_on = NULL,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_roles (id, payload, updated_at)
SELECT
    r.id,
    jsonb_build_object(
        'id', r.id,
        'role_code', r.role_code,
        'role_name', r.role_name,
        'scope_name', COALESCE(r.scope_name, '培养与学位'),
        'description', COALESCE(r.description, ''),
        'permissions', to_jsonb(
            COALESCE(
                (
                    SELECT array_agg(p.permission_code ORDER BY p.permission_code)
                    FROM dtlms_role_permissions AS rp
                    JOIN dtlms_permissions AS p
                        ON p.id = rp.permission_id
                       AND p.is_deleted = FALSE
                    WHERE rp.role_id = r.id
                ),
                ARRAY[]::VARCHAR[]
            )
        )
    ),
    CURRENT_TIMESTAMP
FROM dtlms_roles AS r
WHERE r.role_code = 'advisor'
  AND r.is_deleted = FALSE
  AND EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_system_users (id, payload, updated_at)
SELECT
    u.id,
    jsonb_build_object(
        'id', u.id,
        'username', u.username,
        'full_name', u.full_name,
        'role_code', 'advisor',
        'department_name', COALESCE(up.department_name, u.department_name, ''),
        'phone_number', COALESCE(up.phone_number, u.phone_number),
        'account_status', CASE WHEN u.is_active THEN '启用' ELSE '停用' END,
        'last_login_at', CASE WHEN u.last_login_at IS NULL THEN NULL ELSE TO_CHAR(u.last_login_at, 'YYYY-MM-DD HH24:MI:SS') END,
        'password_hash', u.password_hash
    ),
    CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_profiles (username, payload, updated_at)
SELECT
    u.username,
    jsonb_build_object(
        'username', u.username,
        'full_name', u.full_name,
        'role_name', '导师',
        'department_name', COALESCE(up.department_name, u.department_name, ''),
        'phone_number', COALESCE(up.phone_number, u.phone_number),
        'email', COALESCE(NULLIF(up.email, ''), NULLIF(u.email, ''), CONCAT(u.username, '@dtlms.local')),
        'theme_color', '#13795b'
    ),
    CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (username) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_teams (id, payload, updated_at)
SELECT
    t.id,
    jsonb_build_object(
        'id', t.id,
        'team_code', t.team_code,
        'team_name', s.center_name,
        'department_name', COALESCE(t.department_name, s.center_name),
        'discipline_name', COALESCE(NULLIF(t.discipline_name, ''), '未分配学科'),
        'lead_advisor_name', s.director_name,
        'advisor_names', to_jsonb(s.advisor_names),
        'research_directions', '[]'::jsonb,
        'status', '启用',
        'created_on', TO_CHAR(COALESCE(t.established_on, CURRENT_DATE), 'YYYY-MM-DD'),
        'established_on', TO_CHAR(COALESCE(t.established_on, CURRENT_DATE), 'YYYY-MM-DD'),
        'description', COALESCE(t.description, '按研究中心主数据维护需求批量导入。')
    ),
    CURRENT_TIMESTAMP
FROM tmp_center_seed AS s
JOIN dtlms_teams AS t ON t.team_name = s.center_name
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_counters (counter_name, counter_value, updated_at)
SELECT
    x.counter_name,
    x.counter_value,
    CURRENT_TIMESTAMP
FROM (
    VALUES
        (
            'roles',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_roles), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_roles WHERE is_deleted = FALSE), 0)
            )
        ),
        (
            'system_users',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_system_users), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_users WHERE is_deleted = FALSE), 0)
            )
        ),
        (
            'teams',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_teams), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_teams WHERE is_deleted = FALSE), 0)
            )
        )
) AS x(counter_name, counter_value)
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (counter_name) DO UPDATE
SET counter_value = GREATEST(dtlms_runtime_counters.counter_value, EXCLUDED.counter_value),
    updated_at = CURRENT_TIMESTAMP;

COMMIT;
