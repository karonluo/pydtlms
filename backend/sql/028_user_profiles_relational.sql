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