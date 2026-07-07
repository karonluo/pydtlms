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


-- =============================================================================
-- 2026-07-07 (二): 字典 dtlms_dict_types / dtlms_dict_data 增加
--   dict_type='student_signed_offer_timeout_hours'
--   dict_name='学生签署录取通知超时小时'
--
-- 用途:
--   /portal/home/offer 录取通知书卡片右上角"剩余确认时间"的小时数阈值.
--   实际语义: 学生收到录取通知 (dtlms_plan_offer.accepted_notification_sent_at) 后
--             N 小时内必须在 portal 完成接受/拒绝操作; 超过 N 小时视为超时.
--   计算口径:
--     deadline = accepted_notification_sent_at + N 小时
--     若 accepted_notification_sent_at IS NULL, 则 deadline = now + N 小时
--   N 由本条 dict_data.value 决定, 单位小时, 类型整型 (在 dict_data.value 中以字符串存储).
--
-- 兜底:
--   前端读不到字典 / value 非整型时, 默认按 24 小时渲染.
--
-- 使用说明:
--   1. 本脚本可重复执行: 仅在 (dict_type, value) 不存在时插行.
--   2. 仅 DML (INSERT), 不改表结构; 与上一个 ALTER 互不影响.
--   3. 若以后要修改超时小时, 走"字典管理"页编辑 dict_data.value, 不要再修改本脚本.
-- =============================================================================

SET search_path TO public;

DO $dict$
DECLARE
    v_type_id bigint;
BEGIN
    -- 1) dict_type 插入 (若不存在)
    -- 2026-07-07: dtlms_dict_types 实际表有 dict_name NOT NULL 列 (虽然 database_schema.md 未列出),
    --              这里显式补上, 与 dict_type 同名.
    IF NOT EXISTS (
        SELECT 1 FROM dtlms_dict_types WHERE dict_type = 'student_signed_offer_timeout_hours'
    ) THEN
        INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
        VALUES (
            '学生签署录取通知超时小时',
            'student_signed_offer_timeout_hours',
            '启用',
            '2026-07-07: Offer 签署页超时阈值配置, 单位小时, 整型'
        )
        RETURNING id INTO v_type_id;
    ELSE
        SELECT id INTO v_type_id FROM dtlms_dict_types WHERE dict_type = 'student_signed_offer_timeout_hours';
    END IF;

    -- 2) dict_data 插入 (value='24', label='24 小时')
    IF NOT EXISTS (
        SELECT 1 FROM dtlms_dict_data
        WHERE dict_type = 'student_signed_offer_timeout_hours' AND value = '24'
    ) THEN
        INSERT INTO dtlms_dict_data (
            dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark, is_deleted
        ) VALUES (
            v_type_id,
            'student_signed_offer_timeout_hours',
            '24 小时',
            '24',
            0,
            '启用',
            NULL,
            NULL,
            '2026-07-07: Offer 签署超时阈值初始值',
            FALSE
        );
        RAISE NOTICE 'Inserted dict_data: student_signed_offer_timeout_hours=24 小时';
    ELSE
        RAISE NOTICE 'dict_data student_signed_offer_timeout_hours value=24 already exists, skipped.';
    END IF;
END
$dict$;

-- 验证语句: 执行后可以跑以下 SQL 确认
-- SELECT t.dict_type, t.status, d.value, d.label, d.status
-- FROM dtlms_dict_types t
-- LEFT JOIN dtlms_dict_data d ON d.dict_type = t.dict_type
-- WHERE t.dict_type = 'student_signed_offer_timeout_hours';
