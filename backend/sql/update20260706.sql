-- =============================================================================
-- 2026-07-06: dtlms_plan_offer 新增字段“已进入夏令营选拔”
--
-- 背景：
--   现有 is_sent_mail / is_agree 等都是 boolean，补充业务类别于
--   “accepted”（字典状态）、“hackathon_score”（评分）的个体选拔标志。
--
-- 字段设计（与现有 is_sent_mail 同风格）：
--   英文列名  : is_in_camp_selection
--   中文显示  : 已进入夏令营选拔
--   类型            : BOOLEAN
--   可空            : NO
--   默认值      : FALSE（与 is_sent_mail 一致）
--   索引            : 初期不加（查询场景较少）
--
-- 使用说明：
--   1. 本脚本可重复执行：仅在字段不存在时加列。
--   2. 如果表不在 public schema，请手动修改 SET search_path。
--   3. 推荐于低峰期执行；仅加列、不动现有数据，不会锁表。
--   4. 本脚本仅修改表结构与默认值，不会改动现有记录的
--      is_sent_mail / accepted / hackathon_score 等字段。
-- =============================================================================

SET search_path TO public;

DO $body$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name   = 'dtlms_plan_offer'
          AND column_name  = 'is_in_camp_selection'
    ) THEN
        ALTER TABLE public.dtlms_plan_offer
            ADD COLUMN is_in_camp_selection BOOLEAN;

        ALTER TABLE public.dtlms_plan_offer
            ALTER COLUMN is_in_camp_selection SET DEFAULT FALSE;

        -- 先把现有行补充为 FALSE，避免 NOT NULL 加列失败
        UPDATE public.dtlms_plan_offer
        SET is_in_camp_selection = FALSE
        WHERE is_in_camp_selection IS NULL;

        ALTER TABLE public.dtlms_plan_offer
            ALTER COLUMN is_in_camp_selection SET NOT NULL;

        RAISE NOTICE 'Added column dtlms_plan_offer.is_in_camp_selection (BOOLEAN, NOT NULL, DEFAULT FALSE)';
    ELSE
        RAISE NOTICE 'Column dtlms_plan_offer.is_in_camp_selection already exists, skipped.';
    END IF;
END
$body$;

-- 验证语句：执行后可以跑以下 SQL 确认
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'dtlms_plan_offer' AND column_name = 'is_in_camp_selection';
