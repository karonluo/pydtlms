-- ============================================================
-- 脚本名称: update20260619_2.sql
-- 脚本说明: 将 dtlms_plan_offer 表的 created_at / updated_at 改为
--           NOT NULL DEFAULT CURRENT_TIMESTAMP
-- 作    者: Codex (auto)
-- 创建日期: 2026-06-19
-- ============================================================

BEGIN;

-- 1. 先为已有 NULL 数据兜底（虽然目前没有 NULL，但保持幂等）
UPDATE dtlms_plan_offer
   SET created_at = COALESCE(created_at, CURRENT_TIMESTAMP),
       updated_at = COALESCE(updated_at, CURRENT_TIMESTAMP)
 WHERE created_at IS NULL
    OR updated_at IS NULL;

-- 2. 添加默认值
ALTER TABLE dtlms_plan_offer
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

-- 3. 设置为 NOT NULL
ALTER TABLE dtlms_plan_offer
    ALTER COLUMN created_at SET NOT NULL,
    ALTER COLUMN updated_at SET NOT NULL;

COMMIT;
