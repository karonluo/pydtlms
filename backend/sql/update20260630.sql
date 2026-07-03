-- ============================================================
-- 脚本名称: update20260630.sql
-- 脚本说明: 为 dtlms_plan_offer 增加 3 个字段(黑客松活动)
--           - hackathon_score     numeric(5,2)，夏令营评分
--           - hackathon_comments  text，夏令营评语
--           - accepted            varchar(32)，入取状态(6 个枚举值 + NULL)
--
-- 业务背景:
--           黑客松夏令营(hackathon)是学生入营之后的活动，与"入营邮件
--           接受/拒绝"(is_agree / student_offer_submitted_at)是两套独立
--           的状态机。
--
-- 字段设计:
--           - hackathon_score     与现有 screening_score 等打分字段保持
--                                numeric(5,2) 精度
--           - hackathon_comments  文本，无长度限制
--           - accepted            varchar(32)，CHECK 约束保证只能是
--                                6 个枚举值或 NULL(默认)
--           - 3 个字段均允许为空
--
-- 前置条件:
--           - dtlms_plan_offer 表已存在
--           - accepted 字段已存在且为 varchar(32)
--           - dtlms_dict_types / dtlms_dict_data 表已存在
--
-- 后续脚本: 无
--
-- 注意事项:
--           - 本脚本只新增字段、约束、字典数据，不修改任何现有数据
--           - 执行后请按惯例运行 _extract_schema.py 刷新 database_schema.md
-- ============================================================

BEGIN;

-- 1) 字段如果不存在则补建(幂等)
ALTER TABLE public.dtlms_plan_offer
  ADD COLUMN IF NOT EXISTS hackathon_score     numeric(5,2),
  ADD COLUMN IF NOT EXISTS hackathon_comments  text;

-- 2) accepted 字段长度修正(已是 32 时无影响)
--    如果当前是 16，则扩展为 32(本字段无历史数据，可安全扩展)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.columns
     WHERE table_schema = 'public'
       AND table_name = 'dtlms_plan_offer'
       AND column_name = 'accepted'
       AND character_maximum_length < 32
  ) THEN
    ALTER TABLE public.dtlms_plan_offer
      ALTER COLUMN accepted TYPE varchar(32);
  END IF;
END;
$$;

-- 3) CHECK 约束(限定 6 个枚举值 + NULL，幂等)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.table_constraints
     WHERE constraint_schema = 'public'
       AND table_name = 'dtlms_plan_offer'
       AND constraint_name = 'dtlms_plan_offer_accepted_check'
  ) THEN
    ALTER TABLE public.dtlms_plan_offer
      ADD CONSTRAINT dtlms_plan_offer_accepted_check
      CHECK (accepted IS NULL OR accepted IN (
        'declined',
        'pending',
        'accepted_pending_send',
        'accepted_sent',
        'accepted_confirmed',
        'accepted_rejected'
      ));
  END IF;
END;
$$;

-- 4) 字段说明
COMMENT ON COLUMN public.dtlms_plan_offer.hackathon_score
  IS '夏令营评分(0~100)，与现有评分字段保持 numeric(5,2) 精度';

COMMENT ON COLUMN public.dtlms_plan_offer.hackathon_comments
  IS '夏令营评语，文本类型，无长度限制';

COMMENT ON COLUMN public.dtlms_plan_offer.accepted
  IS '黑客松入取状态: NULL=待录取 / declined=未录取 / pending=待定 / accepted_pending_send=录取未发送 / accepted_sent=录取已发送 / accepted_confirmed=录取已确认 / accepted_rejected=录取已拒绝';

-- 5) 字典类型
INSERT INTO public.dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES ('黑客松入取状态', 'hackathon_accepted_status', '启用', '黑客松夏令营入取状态枚举(用于 dtlms_plan_offer.accepted 字段)')
ON CONFLICT (dict_type) DO NOTHING;

-- 6) 字典数据
--    value 为空字符串 '' 表示"待录取" (NULL)
--    color_type 使用 Element Plus Tag 的 type 取值: success / warning / info / danger / primary
INSERT INTO public.dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, remark)
SELECT t.id, t.dict_type, v.label, v.value, v.sort_order, '启用', v.color_type, v.remark
  FROM public.dtlms_dict_types t
  JOIN (VALUES
    ('待录取',         '',                        1, 'info',    '默认状态，未作任何行动'),
    ('未录取',         'declined',                2, 'danger',  '中心负责人或书院管理员点击【不录取】'),
    ('待定',           'pending',                 3, 'warning', '中心负责人或书院管理员点击【待定】'),
    ('录取未发送',     'accepted_pending_send',   4, 'success', '中心负责人或书院管理员点击【录取】，但未发送录取通知书'),
    ('录取已发送',     'accepted_sent',           5, 'success', '书院管理员发送了录取通知书'),
    ('录取已确认',     'accepted_confirmed',      6, 'success', '学生同意录取通知'),
    ('录取已拒绝',     'accepted_rejected',       7, 'danger',  '学生拒绝录取通知')
  ) AS v(label, value, sort_order, color_type, remark) ON TRUE
 WHERE t.dict_type = 'hackathon_accepted_status'
ON CONFLICT (dict_type, value) DO NOTHING;

COMMIT;

-- 验证(执行后可手动跑一次)
-- 1. 字段验证
-- SELECT column_name, data_type, character_maximum_length, numeric_precision, numeric_scale, is_nullable
--   FROM information_schema.columns
--  WHERE table_schema = 'public' AND table_name = 'dtlms_plan_offer'
--    AND column_name IN ('hackathon_score', 'hackathon_comments', 'accepted')
--  ORDER BY column_name;
--
-- 2. CHECK 约束验证
-- SELECT conname, pg_get_constraintdef(oid)
--   FROM pg_constraint
--  WHERE conrelid = 'public.dtlms_plan_offer'::regclass
--    AND conname = 'dtlms_plan_offer_accepted_check';
--
-- 3. 字典数据验证
-- SELECT d.label, d.value, d.sort_order, d.color_type, d.status
--   FROM dtlms_dict_data d
--   JOIN dtlms_dict_types t ON t.id = d.dict_type_id
--  WHERE t.dict_type = 'hackathon_accepted_status'
--  ORDER BY d.sort_order;