-- update20260605.sql
-- Incremental, non-destructive DB changes recorded on 2026-06-05.
-- 指南：开发过程中所有不破坏现有数据的数据库变更，在验证并在开发环境执行后，追加到此文件。
-- 每个语句应使用防重入（idempotent）语法，例如：INSERT ... WHERE NOT EXISTS(...) 或 CREATE TABLE IF NOT EXISTS。

BEGIN;

-- 1) 新增权限点：新闻管理菜单（若已存在则不重复插入）
INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'news_management:read', '查看新闻管理菜单', 'news', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
  SELECT 1 FROM dtlms_permissions WHERE permission_code = 'news_management:read'
);

-- 2) 将新闻管理菜单授权给需要进入招生管理的角色（若已存在则不重复插入）
INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'news_management:read'
WHERE r.role_code IN ('advisor', 'AILABMGT', 'recruit_reviewer', 'interview_officer')
ON CONFLICT DO NOTHING;

COMMIT;

-- 说明：后续的数据库相关改动（非破坏性）请追加到此文件末尾，按时间倒序或逐条注释来源与目的。

-- 3) 新增研究中心查看与维护权限，并授权给导师和书院管理员
BEGIN;

INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'research_center:read', '查看研究中心菜单', 'students', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
  SELECT 1 FROM dtlms_permissions WHERE permission_code = 'research_center:read'
);

INSERT INTO dtlms_permissions (permission_code, permission_name, module_name, is_deleted, created_at, updated_at)
SELECT 'research_center:write', '维护研究中心数据', 'students', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
  SELECT 1 FROM dtlms_permissions WHERE permission_code = 'research_center:write'
);

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'research_center:read'
WHERE r.role_code IN ('advisor', 'AILABMGT')
ON CONFLICT DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON p.permission_code = 'research_center:write'
WHERE r.role_code IN ('AILABMGT')
ON CONFLICT DO NOTHING;

COMMIT;
