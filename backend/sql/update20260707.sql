-- =============================================================================
-- 2026-07-07: dtlms_plan_offer 新增字段“发送录取通知日期时间”
--
-- 背景：
--   表上已有 sent_mail_at, 表示“已发送 offer 通知邮件” (学生用这封邮件回复同意/不同意 offer)。
--   本次新增 accepted_notification_sent_at 表示另一封邮件 —— “录取通知” (告诉学生被录取了)。
--   两封邮件语义独立、可空独立。本轮只加字段, 不触发任何业务逻辑, 后续按需求再做利用。
--
-- 字段设计 (与现有 sent_mail_at 风格一致):
--   英文列名  : accepted_notification_sent_at
--   中文显示  : 发送录取通知日期时间
--   类型      : timestamp without time zone
--   可空      : YES (NULL = 未发送录取通知; 非空 = 已发送)
--   默认值    : 无
--   索引      : 初期不加 (查询场景较少)
--
-- 使用说明：
--   1. 本脚本可重复执行: 仅在字段不存在时加列。
--   2. 如果表不在 public schema, 请手动修改 SET search_path。
--   3. 推荐于低峰期执行; 仅加列, 不动现有数据, 不会锁表。
--   4. 本脚本仅修改表结构, 不会改动任何现有记录。
-- =============================================================================

SET search_path TO public;

DO $body$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name   = 'dtlms_plan_offer'
          AND column_name  = 'accepted_notification_sent_at'
    ) THEN
        ALTER TABLE public.dtlms_plan_offer
            ADD COLUMN accepted_notification_sent_at TIMESTAMP WITH TIME ZONE;

        COMMENT ON COLUMN public.dtlms_plan_offer.accepted_notification_sent_at
            IS '发送录取通知日期时间; NULL 表示未发送, 非空表示已发送 (与 sent_mail_at 语义不同)';

        RAISE NOTICE 'Added column dtlms_plan_offer.accepted_notification_sent_at (TIMESTAMP WITHOUT TIME ZONE, NULL allowed)';
    ELSE
        RAISE NOTICE 'Column dtlms_plan_offer.accepted_notification_sent_at already exists, skipped.';
    END IF;
END
$body$;

-- 验证语句: 执行后可以跑以下 SQL 确认
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'dtlms_plan_offer' AND column_name = 'accepted_notification_sent_at';
