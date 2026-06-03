INSERT INTO dtlms_permissions (permission_code, permission_name, module_name)
VALUES
    ('workflow_center_menu:read', '查看流程待办菜单', 'workspace')
ON CONFLICT (permission_code) DO UPDATE
SET permission_name = EXCLUDED.permission_name,
    module_name = EXCLUDED.module_name,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

UPDATE dtlms_permissions
SET permission_name = '查看流程处理数据',
    module_name = 'workflow',
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE
WHERE permission_code = 'workflow:read';


UPDATE dtlms_permissions
SET permission_name = '处理流程任务',
    module_name = 'workflow',
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE
WHERE permission_code = 'workflow:write';