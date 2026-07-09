-- =============================================================================
-- 2026-07-09: dtlms_plan_offer 新增字段"学生提交offer日期时间"
--
-- ★★★ 重要: dtlms_plan_offer 上与"录取流程"相关的字段, 实际属于两条平行的业务链, 互不依赖。
--
-- 链 A: 学生门户端"申请进度"阶段显示 (portal /portal/home 右上角 workflow stages)
--   - is_agree                  是否同意入营 (学生本人 / 早期标志)
--   - is_in_camp_selection      是否已进入夏令营选拔环节 (书院管理员手工导入)
--   ↑ 这两个字段仅影响 portal 端学生看到的"当前阶段"是哪一站,
--     与管理端 /recruitment/camp-offers 的"录取决议 → 发邮件 → 学生签"流程 完全无关。
--   (参考: backend/app/services/management_service_portal.py 中 _portal_workflow_summary,
--    在初筛中的学生看 is_in_camp_selection: True → 阶段进入"夏令营选拔" / False → 停留"背景评估")
--
-- 链 B: 管理端"录取全流程" (recruitment / camp-offers)
--
--   ┌─────────────────────────────────────────────────────────────────────────┐
--   │ 1) 学生入营 (is_agree=true) → 入营名单出现在 /recruitment/camp-offers │
--   └─────────────────────────────────────────────────────────────────────────┘
--                              │
--                              ▼
--   ┌─────────────────────────────────────────────────────────────────────────┐
--   │ 2) 书院管理员 (AILABMGT / 平台管理员):                                 │
--   │    从入营名单中圈出"进入夏令营选拔"的学生 (写 is_in_camp_selection,  │
--   │    用于链 A 的阶段显示; 中心负责人对 is_in_camp_selection 无感)       │
--   │    + 把导师线下打分的 Excel 整理后批量导入系统                         │
--   │      → hackathon_score    入营评分 (0~100)                            │
--   │      → hackathon_comments 入营评语                                    │
--   └─────────────────────────────────────────────────────────────────────────┘
--                              │
--                              ▼
--   ┌─────────────────────────────────────────────────────────────────────────┐
--   │ 3) 研究中心负责人 (advisor 角色 + dtlms_team_leaders 中任一 lead):     │
--   │    可见范围 = 自己 + 自己任 lead 的中心的所有 dtlms_team_advisors      │
--   │    (resolve_camp_offer_visible_advisor_names: 按 first/second_choice   │
--   │     命中的"导师姓名"过滤, 与 is_in_camp_selection 无关)                │
--   │    前置条件: hackathon_score 与 hackathon_comments 均已由书院管理员    │
--   │    权限: 2026-07-09 收紧, 仅 is_center_leader=True (研究中心负责人)   │
--   │    或 is_unrestricted=True (书院/平台) 可改; 普通 advisor 完全不允许,  │
--   │    中心负责人对自己可见列表里所有学生均可改 (不再要求是学生具体导师)   │
--   │    在步骤 2 导入; 若任一字段缺失, 前端会隐藏"录取/不录取/待定"按钮   │
--   │    (后端是否做硬拦截 待定; 当前只靠前端隐藏)                           │
--   │    对可见范围内的入营学生做"录取/不录取/待定"决议                      │
--   │    → dtlms_plan_offer.accepted = ''accepted_pending_send'' (录取未发送)│
--   │    → dtlms_plan_offer.accepted = ''declined''              (未录取)   │
--   │    → dtlms_plan_offer.accepted = ''pending''               (待定)     │
--   │    (普通 advisor 完全无 can_change_accepted 权限, 2026-07-09 收紧后取消)   │
--   └─────────────────────────────────────────────────────────────────────────┘
--                              │
--                              ▼
--   ┌─────────────────────────────────────────────────────────────────────────┐
--   │ 4) 书院管理员 (AILABMGT / 平台管理员):                                 │
--   │    从 accepted_pending_send 的学生中选中学生, 发送"录取通知书"邮件   │
--   │    → dtlms_plan_offer.accepted = ''accepted_sent'' (枚举值, 不是字段) │
--   │    → dtlms_plan_offer.accepted_notification_sent_at = now()           │
--   │    (本步骤是从 2026-07-07 起新增的"录取通知书"邮件, 与 sent_mail_at   │
--   │     语义不同: sent_mail_at = offer 通知邮件 (学生回信用),              │
--   │                  accepted_notification_sent_at = 录取通知邮件 (本邮件)) │
--   └─────────────────────────────────────────────────────────────────────────┘
--                              │
--                              ▼
--   ┌─────────────────────────────────────────────────────────────────────────┐
--   │ 5) 学生 (portal /portal/home/offer): 收到邮件 → 看到"录取通知书"      │
--   │    → 点"接受录取":                                                     │
--   │        dtlms_plan_offer.accepted = ''accepted_confirmed'' (枚举值)    │
--   │        student_submitted_offer_at = now()  ★ 本字段在此写入             │
--   │    → 点"拒绝录取":                                                     │
--   │        dtlms_plan_offer.accepted = ''accepted_rejected''  (枚举值)     │
--   │        student_submitted_offer_at = now()  ★ 本字段在此写入             │
--   └─────────────────────────────────────────────────────────────────────────┘
--
-- 表上已有的时间戳字段 (用于对照):
--   - submitted_at                学生提交日期时间 (申请阶段, 链 A 入口)
--   - sent_mail_at                已发送 offer 通知邮件的时间 (学生用这封邮件回信同意/不同意)
--   - accepted_notification_sent_at  发送录取通知日期时间 (链 B 步骤 4, 学校发"你被录取了"邮件)
--   - timeout_datetime            超时日期时间
--   - created_at / updated_at     数据创建 / 更新
--
-- 本次新增 student_submitted_offer_at:
--   - 英文列名    : student_submitted_offer_at
--   - 中文显示    : 学生提交offer日期时间
--   - 类型        : timestamp with time zone
--   - 可空        : YES (NULL = 学生尚未在 portal 提交过 offer 决定)
--   - 默认值      : 无
--   - 索引        : 初期不加
--   - 写入主体    : 学生本人 (portal 端, 链 B 步骤 5)
--   - 与 accepted 联动:
--       accepted 进入终态 accepted_confirmed  → 本字段由后端写入
--       accepted 进入终态 accepted_rejected   → 本字段由后端写入
--       accepted 停留在 accepted_pending_send / accepted_sent / pending / declined → 本字段为 NULL
--
-- 使用说明:
--   1. 本脚本可重复执行: 仅在字段不存在时加列。
--   2. 如果表不在 public schema, 请手动修改 SET search_path。
--   3. 推荐于低峰期执行; 仅加列, 不动现有数据, 不会锁表。
--   4. 本脚本仅修改表结构, 不会改动任何现有记录。
--   5. 本字段的写入逻辑 (链 B 步骤 5 中由 portal 端触发) 由后续业务代码实现, 本脚本不做。
-- =============================================================================

SET search_path TO public;

DO $body$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name   = 'dtlms_plan_offer'
          AND column_name  = 'student_submitted_offer_at'
    ) THEN
        ALTER TABLE public.dtlms_plan_offer
            ADD COLUMN student_submitted_offer_at TIMESTAMP WITH TIME ZONE;

        COMMENT ON COLUMN public.dtlms_plan_offer.student_submitted_offer_at
            IS '学生提交offer日期时间, NULL 表示学生尚未在 portal 提交过 offer 决定, 非空表示已提交. 与 accepted 字段联动: 当 accepted 进入终态 (accepted_confirmed / accepted_rejected) 时, 本字段由后端写入; accepted 停留在中间态 (accepted_pending_send / accepted_sent) 或前置态 (pending / declined) 时为 NULL. 写入主体: 学生本人 (portal 端). 写入时机: 学生在 /portal/home/offer 卡片上点接受/拒绝时.';

        RAISE NOTICE 'Added column dtlms_plan_offer.student_submitted_offer_at (TIMESTAMP WITH TIME ZONE, NULL allowed)';
    ELSE
        RAISE NOTICE 'Column dtlms_plan_offer.student_submitted_offer_at already exists, skipped.';
    END IF;
END
$body$;

-- 验证语句: 执行后可以跑以下 SQL 确认
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_name = 'dtlms_plan_offer' AND column_name = 'student_submitted_offer_at';
