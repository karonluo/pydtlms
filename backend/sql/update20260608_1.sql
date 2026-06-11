-- 2026-06-08 门户填报 preferences 旧列清理补丁
-- 说明：请在 update20260608.sql 已执行后再执行本文件。

BEGIN;

DROP INDEX IF EXISTS idx_portal_application_preferences_team_id;

ALTER TABLE IF EXISTS dtlms_portal_application_preferences
    DROP COLUMN IF EXISTS team_id,
    DROP COLUMN IF EXISTS research_center_name;

COMMIT;