-- 2026-05-21 生产环境非破坏性升级脚本
-- 目标：
-- 1. 新增背景评估明细表，支持多位书院管理员独立评估并累计两票终局
-- 2. 保持脚本可重复执行，不删除、不覆盖既有业务数据

BEGIN;

CREATE TABLE IF NOT EXISTS dtlms_background_assessments (
	id BIGSERIAL PRIMARY KEY,
	application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
	evaluator_user_id BIGINT,
	evaluator_username VARCHAR(64) NOT NULL,
	evaluator_name VARCHAR(128),
	evaluator_role_code VARCHAR(64) NOT NULL,
	assessment_result VARCHAR(32) NOT NULL,
	assessment_comment TEXT,
	assessed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE (application_id, evaluator_username)
);

CREATE INDEX IF NOT EXISTS idx_background_assessment_application
	ON dtlms_background_assessments(application_id, assessed_at DESC);

CREATE INDEX IF NOT EXISTS idx_background_assessment_result
	ON dtlms_background_assessments(assessment_result);

ALTER TABLE IF EXISTS dtlms_portal_application_preferences
	ALTER COLUMN research_center_name DROP NOT NULL;

COMMIT;
