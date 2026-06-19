-- ============================================================
-- 脚本名称: update20260619_4.sql
-- 脚本说明: 从 dtlms_teams.lead_user_id 灌入 dtlms_team_leaders
--           - 跳过 is_deleted=true 的用户 / 中心
--           - 跳过 is_active=false 的用户
--           - ON CONFLICT (team_id, user_id) DO NOTHING 去重
--           - 暂不动 dtlms_teams.lead_user_id 字段
-- 作    者: Codex (auto)
-- 创建日期: 2026-06-19
-- ============================================================

BEGIN;

INSERT INTO public.dtlms_team_leaders (team_id, user_id)
SELECT t.id, t.lead_user_id
  FROM public.dtlms_teams t
  JOIN public.dtlms_users u ON u.id = t.lead_user_id
 WHERE t.lead_user_id IS NOT NULL
   AND t.is_deleted = false
   AND u.is_deleted = false
   AND u.is_active = true
ON CONFLICT (team_id, user_id) DO NOTHING;

-- 验证：本次写入条数与目标团队数
SELECT
    (SELECT COUNT(*) FROM public.dtlms_team_leaders) AS total_rows,
    (SELECT COUNT(*) FROM public.dtlms_teams WHERE lead_user_id IS NOT NULL) AS source_rows;

COMMIT;
