-- 2026-05-11 生产环境非破坏性升级脚本
-- 目标：
-- 1. 确保系统账号资料表可承载邮箱/手机号等资料字段
-- 2. 非破坏性补齐 dtlms_user_profiles 中缺失的账号资料

BEGIN;

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

ALTER TABLE IF EXISTS dtlms_user_profiles
    ADD COLUMN IF NOT EXISTS phone_number VARCHAR(32),
    ADD COLUMN IF NOT EXISTS email VARCHAR(128),
    ADD COLUMN IF NOT EXISTS theme_color VARCHAR(32) NOT NULL DEFAULT '#0f4cbd',
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;

WITH profile_source AS (
    SELECT
        u.username,
        COALESCE(NULLIF(BTRIM(u.full_name), ''), u.username) AS full_name,
        COALESCE(NULLIF(BTRIM(r.role_name), ''), '系统用户') AS role_name,
        COALESCE(BTRIM(u.department_name), '') AS department_name,
        NULLIF(BTRIM(u.phone_number), '') AS phone_number,
        NULLIF(BTRIM(u.email), '') AS email
    FROM dtlms_users AS u
    LEFT JOIN dtlms_user_roles AS ur ON ur.user_id = u.id
    LEFT JOIN dtlms_roles AS r ON r.id = ur.role_id AND r.is_deleted = FALSE
    WHERE u.is_deleted = FALSE
)
INSERT INTO dtlms_user_profiles (
    username,
    full_name,
    role_name,
    department_name,
    phone_number,
    email,
    theme_color,
    created_at,
    updated_at
)
SELECT
    src.username,
    src.full_name,
    src.role_name,
    src.department_name,
    src.phone_number,
    src.email,
    '#0f4cbd',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM profile_source AS src
ON CONFLICT (username) DO NOTHING;

WITH profile_source AS (
    SELECT
        u.username,
        COALESCE(NULLIF(BTRIM(u.full_name), ''), u.username) AS full_name,
        COALESCE(NULLIF(BTRIM(r.role_name), ''), '系统用户') AS role_name,
        COALESCE(BTRIM(u.department_name), '') AS department_name,
        NULLIF(BTRIM(u.phone_number), '') AS phone_number,
        NULLIF(BTRIM(u.email), '') AS email
    FROM dtlms_users AS u
    LEFT JOIN dtlms_user_roles AS ur ON ur.user_id = u.id
    LEFT JOIN dtlms_roles AS r ON r.id = ur.role_id AND r.is_deleted = FALSE
    WHERE u.is_deleted = FALSE
)
UPDATE dtlms_user_profiles AS up
SET full_name = CASE
        WHEN COALESCE(BTRIM(up.full_name), '') = '' THEN src.full_name
        ELSE up.full_name
    END,
    role_name = CASE
        WHEN COALESCE(BTRIM(up.role_name), '') = '' THEN src.role_name
        ELSE up.role_name
    END,
    department_name = CASE
        WHEN COALESCE(BTRIM(up.department_name), '') = '' THEN src.department_name
        ELSE up.department_name
    END,
    phone_number = COALESCE(NULLIF(BTRIM(up.phone_number), ''), src.phone_number),
    email = COALESCE(NULLIF(BTRIM(up.email), ''), src.email),
    updated_at = CURRENT_TIMESTAMP
FROM profile_source AS src
WHERE up.username = src.username
  AND (
      COALESCE(BTRIM(up.full_name), '') = ''
      OR COALESCE(BTRIM(up.role_name), '') = ''
      OR COALESCE(BTRIM(up.department_name), '') = ''
      OR (COALESCE(BTRIM(up.phone_number), '') = '' AND src.phone_number IS NOT NULL)
      OR (COALESCE(BTRIM(up.email), '') = '' AND src.email IS NOT NULL)
  );

COMMIT;