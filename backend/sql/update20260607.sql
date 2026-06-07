-- update20260607.sql
-- Incremental, non-destructive DB changes recorded on 2026-06-07.
-- 本次变更仅涉及权限字典与角色授权，不包含物理表结构变更。
-- 所有语句均使用幂等写法，便于生产环境重复执行或回放。

BEGIN;

-- 1) 新增注册学生退回环节权限点
INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'recruitment_registered_students:write', '退回注册学生环节', 'recruitment', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_permissions
    WHERE permission_code = 'recruitment_registered_students:write'
);

-- 2) 将该权限授予书院管理员
INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'recruitment_registered_students:write'
WHERE r.role_code = 'AILABMGT'
ON CONFLICT DO NOTHING;

COMMIT;
