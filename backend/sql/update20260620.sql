-- ============================================================
-- 脚本名称: update20260620.sql
-- 脚本说明: camp-offers 第二志愿范围过滤规则升级（应用层代码改动）
--           - 涉及文件: backend/app/services/postgres_state_store_query_recruitment.py
--           - 函数: _build_camp_offer_where (L825-850)
--           - 涉及表结构: 无
--           - 涉及数据: 无
--           - 涉及范围: 仅 camp-offers 列表/详情/导出
--                       统计接口 (count_camp_offer_stats / get_camp_offer_stats)
--                       不受影响（未传 principal, 走全量统计）
--
-- 业务背景:
--           客户要求: 若第一志愿 >= 80 分, 则该学生不会流转到第二志愿打分,
--           此时 second_choice_screening_submitted_at IS NULL,
--           第二志愿的导师不应该看到该学生.
--           反过来说: 第二志愿的导师能看到该学生, 必须满足
--           (a) 第一/第二志愿选的是同一个导师（自己看自己）
--           或 (b) second_choice_screening_submitted_at IS NOT NULL
--                AND second_choice_screening_score >= 80
--
--           第一志愿范围过滤保持原样（first_choice = ANY(visible_advisor_names)）,
--           不受本次改动影响.
--
-- 作    者: Codex (auto)
-- 创建日期: 2026-06-20
-- ============================================================

-- ============================================================
-- 0. 完整性自检（部署前/后均可执行, 仅查询, 不修改数据）
-- ============================================================

-- 0.1 业务不变量校验:
--     如果 second_choice_screening_submitted_at IS NOT NULL
--     那么必然 first_choice_screening_score < 80
--     预期结果: 不一致行数应为 0
SELECT
    COUNT(*) FILTER (
        WHERE second_choice_screening_submitted_at IS NOT NULL
          AND (
              first_choice_screening_score IS NULL
              OR first_choice_screening_score >= 80
          )
    ) AS invariant_violations_should_be_zero
  FROM public.dtlms_recruitment_applications
 WHERE is_deleted = FALSE;

-- ============================================================
-- 1. 部署前/后数据快照（用于回归对比）
-- ============================================================

-- 1.1 [会被新规则隐藏的行] 第二志愿命中 + second_submitted_at IS NULL
--     部署前执行: 记录此行数 N1
--     部署后执行: 任何 advisor 角色登录后, 列表中不应再出现这些 second_choice = 他自己 的行
SELECT
    COUNT(*) AS would_be_hidden_by_new_rule
  FROM public.dtlms_recruitment_applications app
  JOIN public.dtlms_plan_offer offer
    ON offer.candidate_no = app.candidate_no
 WHERE app.is_deleted = FALSE
   AND COALESCE(app.second_choice_screening_submitted_at, '1970-01-01'::timestamptz)
       = '1970-01-01'::timestamptz
   AND NULLIF(BTRIM(COALESCE(app.second_choice, '')), '') IS NOT NULL
   AND COALESCE(NULLIF(BTRIM(app.first_choice), ''), '')
    <> COALESCE(NULLIF(BTRIM(app.second_choice), ''), '');

-- 1.2 [会被新规则保留显示的行] 第二志愿命中 + second_submitted_at IS NOT NULL + second_score >= 80
SELECT
    COUNT(*) AS kept_visible_by_new_rule
  FROM public.dtlms_recruitment_applications app
  JOIN public.dtlms_plan_offer offer
    ON offer.candidate_no = app.candidate_no
 WHERE app.is_deleted = FALSE
   AND app.second_choice_screening_submitted_at IS NOT NULL
   AND app.second_choice_screening_score >= 80
   AND NULLIF(BTRIM(COALESCE(app.second_choice, '')), '') IS NOT NULL;

-- 1.3 [参考: 同人志愿行] 第二志愿命中 + 第一/第二志愿是同一个人
SELECT
    COUNT(*) AS same_advisor_first_second_choice_rows
  FROM public.dtlms_recruitment_applications app
  JOIN public.dtlms_plan_offer offer
    ON offer.candidate_no = app.candidate_no
 WHERE app.is_deleted = FALSE
   AND NULLIF(BTRIM(COALESCE(app.first_choice, '')), '') IS NOT NULL
   AND NULLIF(BTRIM(COALESCE(app.first_choice, '')), '')
    = NULLIF(BTRIM(COALESCE(app.second_choice, '')), '');

-- ============================================================
-- 2. 样本（前 20 条, 用于人工核对）
-- ============================================================

-- 2.1 会被新规则隐藏的样本（按 plan_id, candidate_no 排序）
SELECT
    offer.id            AS offer_id,
    offer.plan_id,
    offer.candidate_no,
    app.first_choice,
    app.first_choice_screening_score,
    app.second_choice,
    app.second_choice_screening_submitted_at,
    app.second_choice_screening_score
  FROM public.dtlms_recruitment_applications app
  JOIN public.dtlms_plan_offer offer
    ON offer.candidate_no = app.candidate_no
 WHERE app.is_deleted = FALSE
   AND COALESCE(app.second_choice_screening_submitted_at, '1970-01-01'::timestamptz)
       = '1970-01-01'::timestamptz
   AND NULLIF(BTRIM(COALESCE(app.second_choice, '')), '') IS NOT NULL
   AND COALESCE(NULLIF(BTRIM(app.first_choice), ''), '')
    <> COALESCE(NULLIF(BTRIM(app.second_choice), ''), '')
 ORDER BY offer.plan_id DESC, offer.candidate_no
 LIMIT 20;

-- 2.2 会被新规则保留显示的样本
SELECT
    offer.id            AS offer_id,
    offer.plan_id,
    offer.candidate_no,
    app.first_choice,
    app.first_choice_screening_score,
    app.second_choice,
    app.second_choice_screening_submitted_at,
    app.second_choice_screening_score
  FROM public.dtlms_recruitment_applications app
  JOIN public.dtlms_plan_offer offer
    ON offer.candidate_no = app.candidate_no
 WHERE app.is_deleted = FALSE
   AND app.second_choice_screening_submitted_at IS NOT NULL
   AND app.second_choice_screening_score >= 80
   AND NULLIF(BTRIM(COALESCE(app.second_choice, '')), '') IS NOT NULL
 ORDER BY offer.plan_id DESC, offer.candidate_no
 LIMIT 20;

-- ============================================================
-- 3. 说明
-- ============================================================
-- 本脚本仅做查询, 不会修改任何数据.
-- 无需 BEGIN/COMMIT 包裹.
-- 执行完毕请归档到 backend/sql/ 目录作为本次变更的留底文件.