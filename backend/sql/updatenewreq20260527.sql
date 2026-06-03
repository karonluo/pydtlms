-- 2026-05-27 本轮招生初筛需求非破坏性升级脚本
-- 用途：
-- 1. 统一承载本次“导师初筛 + 初筛确认 + 入营面试”相关数据库变更
-- 2. 要求所有后续追加内容保持可重复执行、无破坏性，不删除、不覆盖既有业务数据
-- 3. 仅允许使用 CREATE ... IF NOT EXISTS、ALTER TABLE ... ADD COLUMN IF NOT EXISTS、CREATE INDEX IF NOT EXISTS、
--    以及带保护条件的 UPDATE / INSERT / DO $$ 校验逻辑

BEGIN;

-- 追加规范：
-- 1. 新表：优先使用 CREATE TABLE IF NOT EXISTS。
-- 2. 新字段：优先使用 ALTER TABLE IF EXISTS ... ADD COLUMN IF NOT EXISTS。
-- 3. 新索引：优先使用 CREATE INDEX IF NOT EXISTS。
-- 4. 数据回填：必须带明确 WHERE 条件，只补齐缺失值，不覆盖既有人工数据。
-- 5. 风险操作：禁止 DROP TABLE、DROP COLUMN、TRUNCATE、DELETE 全表、无条件 UPDATE。
-- 6. 若存在强依赖前置数据的场景，使用 DO $$ ... RAISE EXCEPTION ... $$ 做显式校验。

-- ====================================================================
-- Section A. 导师初筛主表 / 中间表
-- ====================================================================
CREATE TABLE IF NOT EXISTS dtlms_advisor_screening_batches (
	id BIGSERIAL PRIMARY KEY,
	advisor_user_id BIGINT,
	advisor_username VARCHAR(64) NOT NULL,
	advisor_name VARCHAR(128),
	advisor_role_code VARCHAR(64) NOT NULL DEFAULT 'advisor',
	screening_round VARCHAR(32) NOT NULL,
	signature_base64 TEXT NOT NULL,
	submitted_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_advisor_screening_batches_round
		CHECK (screening_round IN ('first_choice', 'second_choice'))
);

CREATE TABLE IF NOT EXISTS dtlms_advisor_screening_items (
	id BIGSERIAL PRIMARY KEY,
	batch_id BIGINT NOT NULL REFERENCES dtlms_advisor_screening_batches(id) ON DELETE CASCADE,
	application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
	business_key VARCHAR(64) NOT NULL,
	candidate_no VARCHAR(64) NOT NULL,
	screening_round VARCHAR(32) NOT NULL,
	advisor_score NUMERIC(5, 2) NOT NULL,
	is_passed BOOLEAN NOT NULL,
	screening_status VARCHAR(32) NOT NULL DEFAULT 'submitted',
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_advisor_screening_items_round
		CHECK (screening_round IN ('first_choice', 'second_choice')),
	CONSTRAINT chk_advisor_screening_items_score_range
		CHECK (advisor_score >= 0 AND advisor_score <= 100),
	CONSTRAINT uq_advisor_screening_items_application_round
		UNIQUE (application_id, screening_round),
	CONSTRAINT uq_advisor_screening_items_candidate_round
		UNIQUE (candidate_no, screening_round)
);

CREATE INDEX IF NOT EXISTS idx_advisor_screening_batches_advisor_round
	ON dtlms_advisor_screening_batches(advisor_username, screening_round, submitted_at DESC);

CREATE INDEX IF NOT EXISTS idx_advisor_screening_items_application
	ON dtlms_advisor_screening_items(application_id, screening_round, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_advisor_screening_items_batch
	ON dtlms_advisor_screening_items(batch_id);

CREATE INDEX IF NOT EXISTS idx_advisor_screening_items_business_key
	ON dtlms_advisor_screening_items(business_key);

DO $$
BEGIN
	IF EXISTS (
		SELECT 1
		FROM information_schema.columns
		WHERE table_schema = 'public'
		  AND table_name = 'dtlms_advisor_screening_batches'
		  AND column_name = 'signature_base64'
	) THEN
		EXECUTE 'ALTER TABLE dtlms_advisor_screening_batches ALTER COLUMN signature_base64 SET NOT NULL';
	END IF;
END $$;

-- ====================================================================
-- Section B. 初筛确认字段 / 状态字段
-- ====================================================================
CREATE TABLE IF NOT EXISTS dtlms_initial_screening_confirmations (
	id BIGSERIAL PRIMARY KEY,
	application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
	business_key VARCHAR(64) NOT NULL,
	candidate_no VARCHAR(64) NOT NULL,
	confirmer_user_id BIGINT,
	confirmer_username VARCHAR(64) NOT NULL,
	confirmer_name VARCHAR(128),
	confirmer_role_code VARCHAR(64) NOT NULL,
	confirmation_result VARCHAR(32) NOT NULL,
	confirmation_comment TEXT,
	confirmed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_initial_screening_confirmations_result
		CHECK (confirmation_result IN ('passed', 'rejected')),
	CONSTRAINT uq_initial_screening_confirmations_application
		UNIQUE (application_id)
);

CREATE INDEX IF NOT EXISTS idx_initial_screening_confirmations_application
	ON dtlms_initial_screening_confirmations(application_id, confirmed_at DESC);

ALTER TABLE IF EXISTS dtlms_recruitment_applications
	ADD COLUMN IF NOT EXISTS advisor_screening_status VARCHAR(32) NOT NULL DEFAULT 'pending',
	ADD COLUMN IF NOT EXISTS advisor_screening_round VARCHAR(32) NOT NULL DEFAULT 'first_choice',
	ADD COLUMN IF NOT EXISTS first_choice_screening_batch_id BIGINT,
	ADD COLUMN IF NOT EXISTS second_choice_screening_batch_id BIGINT,
	ADD COLUMN IF NOT EXISTS first_choice_screening_submitted_at TIMESTAMPTZ,
	ADD COLUMN IF NOT EXISTS second_choice_screening_submitted_at TIMESTAMPTZ,
	ADD COLUMN IF NOT EXISTS first_choice_screening_score NUMERIC(5, 2),
	ADD COLUMN IF NOT EXISTS second_choice_screening_score NUMERIC(5, 2),
	ADD COLUMN IF NOT EXISTS initial_screening_status VARCHAR(32) NOT NULL DEFAULT 'pending',
	ADD COLUMN IF NOT EXISTS initial_screening_result VARCHAR(32),
	ADD COLUMN IF NOT EXISTS initial_screening_confirmed_at TIMESTAMPTZ,
	ADD COLUMN IF NOT EXISTS initial_screening_confirmer_username VARCHAR(64),
	ADD COLUMN IF NOT EXISTS initial_screening_confirmer_name VARCHAR(128),
	ADD COLUMN IF NOT EXISTS initial_screening_notification_status VARCHAR(32) NOT NULL DEFAULT 'pending',
	ADD COLUMN IF NOT EXISTS initial_screening_notification_sent_at TIMESTAMPTZ,
	ADD COLUMN IF NOT EXISTS next_stage_name VARCHAR(64);

DO $$
BEGIN
	IF EXISTS (
		SELECT 1
		FROM information_schema.columns
		WHERE table_schema = 'public'
		  AND table_name = 'dtlms_recruitment_applications'
		  AND column_name = 'advisor_screening_round'
	) THEN
		EXECUTE $sql$
			UPDATE dtlms_recruitment_applications
			SET advisor_screening_round = 'first_choice'
			WHERE advisor_screening_round IS NULL OR BTRIM(advisor_screening_round) = ''
		$sql$;
	END IF;

	IF EXISTS (
		SELECT 1
		FROM information_schema.columns
		WHERE table_schema = 'public'
		  AND table_name = 'dtlms_recruitment_applications'
		  AND column_name = 'next_stage_name'
	) THEN
		EXECUTE $sql$
			UPDATE dtlms_recruitment_applications
			SET next_stage_name = '入营面试'
			WHERE initial_screening_result = 'passed'
			  AND (next_stage_name IS NULL OR BTRIM(next_stage_name) = '')
		$sql$;
	END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_recruitment_applications_advisor_screening_status
	ON dtlms_recruitment_applications(advisor_screening_status, advisor_screening_round);

CREATE INDEX IF NOT EXISTS idx_recruitment_applications_initial_screening_status
	ON dtlms_recruitment_applications(initial_screening_status, initial_screening_result);

-- ====================================================================
-- Section C. 通知与审计支撑字段
-- ====================================================================
CREATE TABLE IF NOT EXISTS dtlms_initial_screening_notifications (
	id BIGSERIAL PRIMARY KEY,
	application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
	business_key VARCHAR(64) NOT NULL,
	notification_channel VARCHAR(32) NOT NULL,
	notification_event VARCHAR(64) NOT NULL,
	notification_status VARCHAR(32) NOT NULL DEFAULT 'pending',
	recipient_address VARCHAR(255),
	recipient_user_id BIGINT,
	recipient_username VARCHAR(64),
	payload_json JSONB,
	sent_at TIMESTAMPTZ,
	created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT chk_initial_screening_notifications_channel
		CHECK (notification_channel IN ('email', 'site_message')),
	CONSTRAINT chk_initial_screening_notifications_status
		CHECK (notification_status IN ('pending', 'sent', 'failed'))
);

CREATE INDEX IF NOT EXISTS idx_initial_screening_notifications_application
	ON dtlms_initial_screening_notifications(application_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_initial_screening_notifications_status
	ON dtlms_initial_screening_notifications(notification_status, notification_channel);

-- ====================================================================
-- Section D. 招生初筛链路 RBAC 修补
-- ====================================================================
INSERT INTO dtlms_permissions (permission_code, permission_name, module_name)
VALUES
	('workflow_center_menu:read', '查看流程待办菜单', 'workspace'),
	('recruitment_plan:read', '查看招生计划菜单', 'recruitment'),
	('recruitment_registered_students:read', '查看注册学生菜单', 'recruitment'),
	('recruitment_advisor_screening:read', '查看导师初筛菜单', 'recruitment'),
	('recruitment_initial_screening_confirmation:read', '查看初筛确认菜单', 'recruitment')
ON CONFLICT (permission_code) DO UPDATE
SET permission_name = EXCLUDED.permission_name,
	module_name = EXCLUDED.module_name,
	updated_at = CURRENT_TIMESTAMP,
	is_deleted = FALSE;

UPDATE dtlms_permissions
SET permission_name = '查看流程处理数据',
	module_name = 'workflow',
	updated_at = CURRENT_TIMESTAMP,
	is_deleted = FALSE
WHERE permission_code = 'workflow:read';

INSERT INTO dtlms_roles (role_code, role_name, scope_name, description)
VALUES
	('AILABMGT', '书院管理员', '招生管理', '招生初筛确认与背景评估管理')
ON CONFLICT (role_code) DO UPDATE
SET role_name = EXCLUDED.role_name,
	scope_name = EXCLUDED.scope_name,
	description = EXCLUDED.description,
	updated_at = CURRENT_TIMESTAMP,
	is_deleted = FALSE;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'advisor'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'recruitment:read', 'recruitment:write', 'recruitment_plan:read', 'recruitment_registered_students:read', 'recruitment_advisor_screening:read', 'students:read', 'training:read', 'training:write', 'degree:read', 'workflow:read', 'workflow:write')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'AILABMGT'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'recruitment:read', 'recruitment:write', 'recruitment_plan:read', 'recruitment_registered_students:read', 'recruitment_initial_screening_confirmation:read', 'students:read', 'workflow:read', 'workflow:write')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'recruit_reviewer'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'recruitment:read', 'recruitment_plan:read')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'interview_officer'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'recruitment:read', 'recruitment:write', 'recruitment_plan:read')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'hrbp'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'students:read', 'training:read', 'recruitment_registered_students:read')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT role_row.id, permission_row.id
FROM (
	SELECT id
	FROM dtlms_roles
	WHERE role_code = 'party_affairs'
	  AND is_deleted = FALSE
) AS role_row
JOIN dtlms_permissions AS permission_row
	ON permission_row.permission_code IN ('dashboard:read', 'students:read', 'audit:read', 'recruitment_registered_students:read')
	AND permission_row.is_deleted = FALSE
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- ====================================================================
-- Section E. 历史报名申请状态回填
-- 说明：
-- 1. 仅回填 dtlms_recruitment_applications.application_status，绝不修改 candidate_no / business_key。
-- 2. 仅把旧口径状态映射到本次冻结的新口径，不触碰 advisor_screening_* / initial_screening_* / workflow 字段。
-- 3. “中心考核”已在本轮需求中整体替换为“导师初筛 + 初筛确认 + 入营面试”，因此历史 center_assessment 映射到导师初筛。
-- ====================================================================
UPDATE dtlms_recruitment_applications
SET application_status = CASE application_status
	WHEN 'submitted' THEN '报名已提交'
	WHEN 'returned' THEN '驳回重填'
	WHEN 'qualified' THEN '待背景评估'
	WHEN 'background_review' THEN '待背景评估'
	WHEN 'scoring' THEN '待背景评估'
	WHEN '资格审核通过' THEN '待背景评估'
	WHEN '材料评分中' THEN '待背景评估'
	WHEN 'initial_screening' THEN '待导师初筛-第一志愿'
	WHEN 'initial_screening_first' THEN '待导师初筛-第一志愿'
	WHEN 'center_assessment' THEN '待导师初筛-第一志愿'
	WHEN 'center_assessment_first' THEN '待导师初筛-第一志愿'
	WHEN '待中心考核' THEN '待导师初筛-第一志愿'
	WHEN '待中心考核-第一志愿' THEN '待导师初筛-第一志愿'
	WHEN 'initial_screening_second' THEN '待导师初筛-第二志愿'
	WHEN 'center_assessment_second' THEN '待导师初筛-第二志愿'
	WHEN '待中心考核-第二志愿' THEN '待导师初筛-第二志愿'
	WHEN 'initial_screening_confirmation' THEN '待初筛确认'
	WHEN 'camp_interview' THEN '入营面试'
	WHEN 'terminated' THEN '报名终止'
	WHEN 'rejected' THEN '报名终止'
	ELSE application_status
END,
	updated_at = CURRENT_TIMESTAMP
WHERE application_status IN (
	'submitted',
	'returned',
	'qualified',
	'background_review',
	'scoring',
	'资格审核通过',
	'材料评分中',
	'initial_screening',
	'initial_screening_first',
	'center_assessment',
	'center_assessment_first',
	'待中心考核',
	'待中心考核-第一志愿',
	'initial_screening_second',
	'center_assessment_second',
	'待中心考核-第二志愿',
	'initial_screening_confirmation',
	'camp_interview',
	'terminated',
	'rejected'
);

-- ====================================================================
-- Section F. 招生申请状态字典补齐
-- ====================================================================
INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES ('申请状态', 'recruitment_application_status', '启用', '申请状态字典')
ON CONFLICT (dict_type) DO UPDATE
SET dict_name = EXCLUDED.dict_name,
	status = EXCLUDED.status,
	remark = EXCLUDED.remark,
	updated_at = CURRENT_TIMESTAMP,
	is_deleted = FALSE;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
	VALUES
		('recruitment_application_status', '报名已提交', '报名已提交', 10, '启用', 'info', NULL, '申请已提交，等待资格审核'),
		('recruitment_application_status', '驳回重填', '驳回重填', 15, '启用', 'danger', NULL, '申请被退回，需要补充后重新提交'),
		('recruitment_application_status', '待背景评估', '待背景评估', 25, '启用', 'warning', NULL, '等待背景评估处理'),
		('recruitment_application_status', '待导师初筛-第一志愿', '待导师初筛-第一志愿', 36, '启用', 'warning', NULL, '等待第一志愿导师初筛'),
		('recruitment_application_status', '待导师初筛-第二志愿', '待导师初筛-第二志愿', 37, '启用', 'warning', NULL, '等待第二志愿导师初筛'),
		('recruitment_application_status', '待初筛确认', '待初筛确认', 38, '启用', 'warning', NULL, '等待书院管理员完成初筛确认'),
		('recruitment_application_status', '入营面试', '入营面试', 45, '启用', 'warning', NULL, '已进入入营面试环节'),
		('recruitment_application_status', '报名终止', '报名终止', 90, '启用', 'danger', NULL, '报名流程已终止')
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
	dict_type_id = EXCLUDED.dict_type_id,
	label = EXCLUDED.label,
	sort_order = EXCLUDED.sort_order,
	status = EXCLUDED.status,
	color_type = EXCLUDED.color_type,
	css_class = EXCLUDED.css_class,
	remark = EXCLUDED.remark,
	updated_at = CURRENT_TIMESTAMP,
	is_deleted = FALSE;

UPDATE dtlms_dict_data
SET status = '停用',
	is_deleted = TRUE,
	updated_at = CURRENT_TIMESTAMP
WHERE dict_type = 'recruitment_application_status'
	AND value NOT IN ('报名已提交', '驳回重填', '待背景评估', '待导师初筛-第一志愿', '待导师初筛-第二志愿', '待初筛确认', '入营面试', '报名终止')
	AND COALESCE(is_deleted, FALSE) = FALSE;

COMMIT;