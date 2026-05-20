-- 2026-05-20 生产环境非破坏性升级脚本
-- 目标：
-- 1. 为系统用户资料表补充“介绍”字段
-- 2. 保持脚本可重复执行，不删除、不覆盖既有业务数据

BEGIN;

CREATE TABLE IF NOT EXISTS dtlms_user_profiles (
    username VARCHAR(64) PRIMARY KEY REFERENCES dtlms_users(username) ON DELETE CASCADE,
    full_name VARCHAR(128) NOT NULL,
    role_name VARCHAR(128) NOT NULL,
    department_name VARCHAR(128) NOT NULL,
    introduction TEXT,
    phone_number VARCHAR(32),
    email VARCHAR(128),
    theme_color VARCHAR(32) NOT NULL DEFAULT '#0f4cbd',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS dtlms_user_profiles
    ADD COLUMN IF NOT EXISTS introduction TEXT;

COMMIT;