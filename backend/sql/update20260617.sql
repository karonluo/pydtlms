-- update20260617.sql
-- Incremental, non-destructive DB changes recorded on 2026-06-17.
-- 本次变更用于新增“入营名单”菜单权限，并授权给平台管理员和书院管理员。

BEGIN;

-- 1) 新增入营名单读写权限点
INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'recruitment_camp_offer:read', '查看入营名单菜单', 'recruitment', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_permissions
    WHERE permission_code = 'recruitment_camp_offer:read'
);

INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'recruitment_camp_offer:write', '维护入营名单数据', 'recruitment', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_permissions
    WHERE permission_code = 'recruitment_camp_offer:write'
);

-- 2) 授权给平台管理员与书院管理员（兼容 academy_admin / AILABMGT 两种角色码）
INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'recruitment_camp_offer:read'
WHERE r.role_code IN ('platform_admin', 'AILABMGT', 'academy_admin')
ON CONFLICT DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'recruitment_camp_offer:write'
WHERE r.role_code IN ('platform_admin', 'AILABMGT', 'academy_admin')
ON CONFLICT DO NOTHING;

COMMIT;
