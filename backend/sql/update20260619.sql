-- update20260619.sql
-- Incremental, non-destructive DB changes recorded on 2026-06-19.
-- 本次变更为“导师(advisor)”角色授予“查看入营名单菜单”权限。
-- 配合后端 list_camp_offers_page / get_camp_offer_detail / export_camp_offers 的可见性过滤，
-- 导师仅能查看自己（或所负责中心下成员）的第一/第二志愿学生入营名单。
-- 注意：advisor 角色不授予 recruitment_camp_offer:write，所有写操作（新增、编辑、删除、
-- 导入、发送通知邮件、模板管理）维持后端 403。

BEGIN;

-- 1) 给 advisor 角色授权 recruitment_camp_offer:read
INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'recruitment_camp_offer:read'
WHERE r.role_code = 'advisor'
ON CONFLICT DO NOTHING;

-- 2) 兜底：如果未来 advisor 角色在历史环境里被错误地授予了 :write，则回收。
DELETE FROM dtlms_role_permissions rp
USING dtlms_roles r, dtlms_permissions p
WHERE rp.role_id = r.id
  AND rp.permission_id = p.id
  AND r.role_code = 'advisor'
  AND p.permission_code = 'recruitment_camp_offer:write';

COMMIT;
