-- ============================================================================
-- 查询：指定日期（或日期区间）内，被背景评估 2 票否决的学生清单
-- 数据库：PostgreSQL
-- 表依赖：dtlms_background_assessments / dtlms_recruitment_applications /
--         dtlms_portal_students
-- 业务口径（与 backend/scripts/query_bg_assessment_2_reject.py 一致）：
--   1) 评估结果 = '不通过' 视为 1 票否决；
--   2) 同一报名申请 application_id 在窗口内累计 reject >= 2 才算"窗口内 2 票"；
--   3) 同时要求 窗口结束时（含历史）总 reject >= 2，避免把"窗口内 1 票 + 之前 1 票"误判为"窗口内 2 票"；
--   4) 时间字段使用 dtlms_background_assessments.assessed_at（带时区）。
--
-- 用法：
--   方法 A：单日查询（替换 :target_date 为 YYYY-MM-DD，默认 Asia/Shanghai）
--       psql ... -v target_date="2026-05-14" -f query_bg_assessment_2_reject.sql
--   方法 B：区间查询（同时替换 :start_date / :end_date，闭区间）
--       psql ... -v start_date="2026-05-01" -v end_date="2026-05-31" -f query_bg_assessment_2_reject.sql
-- ============================================================================

-- ---------- 参数区（直接修改下面的变量即可，无需 psql -v） ----------
\set target_date ''2026-05-14''         -- 单日模式使用的日期（YYYY-MM-DD）
\set start_date ''2026-05-01''         -- 区间模式起始日（含）
\set end_date   ''2026-05-31''         -- 区间模式结束日（含）
\set use_range  false                  -- true=用 [start_date, end_date] 区间；false=仅用 target_date 单日
\set tz_name    ''Asia/Shanghai''      -- 日期解释时区

-- ---------- 派生：把"本地日期"转成 UTC 区间（与 Python 脚本一致） ----------
WITH params AS (
    SELECT
        :use_range::boolean AS use_range,
        :target_date::date AS target_date,
        :start_date::date  AS start_date,
        :end_date::date    AS end_date,
        :tz_name::text     AS tz_name
),
window_bounds AS (
    SELECT
        (date_trunc('day', target_date::timestamp)   AT TIME ZONE (SELECT tz_name FROM params))::timestamp
            AT TIME ZONE 'UTC' AS single_start_utc,
        ((date_trunc('day', target_date::timestamp)   AT TIME ZONE (SELECT tz_name FROM params))
            + interval '1 day' - interval '1 microsecond')::timestamp
            AT TIME ZONE 'UTC' AS single_end_utc,
        (date_trunc('day', start_date::timestamp)    AT TIME ZONE (SELECT tz_name FROM params))::timestamp
            AT TIME ZONE 'UTC' AS range_start_utc,
        ((date_trunc('day', end_date::timestamp)      AT TIME ZONE (SELECT tz_name FROM params))
            + interval '1 day' - interval '1 microsecond')::timestamp
            AT TIME ZONE 'UTC' AS range_end_utc,
        (SELECT use_range FROM params) AS use_range
    FROM params
),
window_chosen AS (
    SELECT
        CASE WHEN use_range THEN (SELECT range_start_utc FROM window_bounds)
             ELSE (SELECT single_start_utc FROM window_bounds)
        END AS win_start_utc,
        CASE WHEN use_range THEN (SELECT range_end_utc FROM window_bounds)
             ELSE (SELECT single_end_utc FROM window_bounds)
        END AS win_end_utc
    FROM window_bounds
),

-- ---------- 窗口内的 reject 票 ----------
windowed_rejects AS (
    SELECT
        ba.application_id,
        ba.assessed_at,
        ba.evaluator_username,
        ba.evaluator_name,
        ba.evaluator_role_code,
        ba.assessment_result,
        ba.assessment_comment
    FROM dtlms_background_assessments ba
    CROSS JOIN window_chosen wc
    WHERE ba.assessment_result = '不通过'
      AND ba.assessed_at >= wc.win_start_utc
      AND ba.assessed_at <= wc.win_end_utc
),

-- ---------- 窗口内累计 reject 计数 + 首/末票时间 ----------
rejects_in_window AS (
    SELECT
        wr.application_id,
        COUNT(*)::int                                                AS window_reject_count,
        MIN(wr.assessed_at)                                          AS first_window_reject_at,
        MAX(wr.assessed_at)                                          AS second_window_reject_at
    FROM windowed_rejects wr
    GROUP BY wr.application_id
    HAVING COUNT(*) >= 2
),

-- ---------- 报名维度 + 总票数（不受窗口限制） ----------
total_reject_counts AS (
    SELECT
        ba.application_id,
        COUNT(*)::int                                                                AS total_reject_count,
        COUNT(*) FILTER (WHERE ba.assessed_at <= (SELECT win_end_utc FROM window_chosen))::int
            AS reject_count_up_to_end
    FROM dtlms_background_assessments ba
    WHERE ba.assessment_result = '不通过'
    GROUP BY ba.application_id
)

SELECT
    riw.application_id,
    ra.portal_student_id,
    stu.full_name,
    stu.phone_number,
    stu.email,
    stu.id_number,
    stu.candidate_no                              AS portal_candidate_no,
    ra.candidate_no                               AS application_candidate_no,
    ra.business_key,
    ra.plan_id,
    ra.application_status,
    ra.initial_screening_status,
    ra.initial_screening_result,
    ra.first_choice,
    ra.first_choice_id,
    ra.second_choice,
    ra.second_choice_id,
    ra.updated_at                                 AS application_updated_at,

    riw.window_reject_count                       AS reject_vote_count_in_window,
    riw.first_window_reject_at                    AS first_reject_at_in_window,
    riw.second_window_reject_at                   AS second_reject_at_in_window,

    trc.total_reject_count                        AS reject_vote_count_total,
    trc.reject_count_up_to_end                    AS reject_vote_count_up_to_window_end,

    -- 第二票（按 assessed_at 升序取最后一票）详细评估人信息
    last_reject.assessed_at                       AS second_reject_assessed_at,
    last_reject.evaluator_username                AS second_reject_evaluator_username,
    last_reject.evaluator_name                    AS second_reject_evaluator_name,
    last_reject.evaluator_role_code               AS second_reject_evaluator_role_code,
    last_reject.assessment_comment                AS second_reject_comment,

    -- 窗口内全部 reject 票（按时间升序）
    (SELECT json_agg(json_build_object(
            'assessed_at',         b.assessed_at,
            'evaluator_username',  b.evaluator_username,
            'evaluator_name',      b.evaluator_name,
            'evaluator_role_code', b.evaluator_role_code,
            'assessment_comment',  b.assessment_comment
          ) ORDER BY b.assessed_at ASC)
     FROM dtlms_background_assessments b
     WHERE b.application_id = riw.application_id
       AND b.assessment_result = '不通过'
       AND b.assessed_at <= riw.second_window_reject_at
    )                                             AS window_reject_history
FROM rejects_in_window riw
JOIN total_reject_counts trc
  ON trc.application_id = riw.application_id
JOIN dtlms_recruitment_applications ra
  ON ra.id = riw.application_id
LEFT JOIN dtlms_portal_students stu
  ON stu.id = ra.portal_student_id
-- 取窗口内最后一票（assessed_at 最大）作为"第二票"详情
LEFT JOIN LATERAL (
    SELECT b.assessed_at, b.evaluator_username, b.evaluator_name,
           b.evaluator_role_code, b.assessment_comment
    FROM dtlms_background_assessments b
    WHERE b.application_id = riw.application_id
      AND b.assessment_result = '不通过'
      AND b.assessed_at <= riw.second_window_reject_at
    ORDER BY b.assessed_at DESC, b.id DESC
    LIMIT 1
) last_reject ON TRUE
WHERE ra.is_deleted = FALSE
  AND trc.reject_count_up_to_end >= 2
ORDER BY riw.second_window_reject_at ASC, riw.application_id ASC
;
