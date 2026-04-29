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