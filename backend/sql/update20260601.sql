-- 2026-06-01 生产环境配置节点补丁
-- 说明：本脚本只维护权限配置节点，不写入任何角色授权关系。
-- 角色是否拥有“流程待办”菜单，请上线后在系统管理 > 权限配置 > 角色管理中手工勾选。

BEGIN;

INSERT INTO dtlms_permissions (permission_code, permission_name, module_name)
VALUES
    ('dashboard:read', '查看经营总览', 'workspace'),
    ('workflow_center_menu:read', '查看流程待办菜单', 'workspace'),
    ('workflow:read', '查看流程处理数据', 'workflow'),
    ('workflow:write', '处理流程任务', 'workflow')
ON CONFLICT (permission_code) DO UPDATE
SET permission_name = EXCLUDED.permission_name,
    module_name = EXCLUDED.module_name,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

COMMIT;