ALTER TABLE IF EXISTS dtlms_portal_students
    ADD COLUMN IF NOT EXISTS account_status VARCHAR(32) NOT NULL DEFAULT '启用';

UPDATE dtlms_portal_students
SET account_status = '停用'
WHERE account_status = '已注销';
