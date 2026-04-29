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
    selected_team_name, selected_advisor_name, self_evaluation, submitted_at, created_at, updated_at
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