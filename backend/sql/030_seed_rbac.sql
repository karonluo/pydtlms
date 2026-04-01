INSERT INTO dtlms_roles (role_code, role_name, description)
VALUES
    ('platform_admin', '平台管理员', '系统级配置与全链路治理'),
    ('student', '博士生', '个人学习、培养与学位办理'),
    ('advisor', '导师', '培养方案制定、报告审阅、答辩指导'),
    ('recruit_reviewer', '评分人', '招生材料评审与推荐'),
    ('interview_officer', '面试官', '面试分组、评分与校算'),
    ('hrbp', '中心HRBP', '实习状态确认与过程监督'),
    ('dormitory_guard', '公寓保障', '住宿与在离校状态配合'),
    ('party_affairs', '党群负责人', '思政考核与资助资格审查')
ON CONFLICT (role_code) DO NOTHING;

INSERT INTO dtlms_permissions (permission_code, permission_name, module_name)
VALUES
    ('dashboard:read', '查看驾驶舱', 'dashboard'),
    ('recruitment:read', '查看招生工作台', 'recruitment'),
    ('recruitment:write', '维护招生流程', 'recruitment'),
    ('students:read', '查看学生主数据', 'students'),
    ('students:write', '维护学生主数据', 'students'),
    ('training:read', '查看培养过程', 'training'),
    ('training:write', '维护培养过程', 'training'),
    ('degree:read', '查看学位过程', 'degree'),
    ('degree:write', '维护学位过程', 'degree'),
    ('audit:read', '查看审计日志与同步策略', 'system')
ON CONFLICT (permission_code) DO NOTHING;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM dtlms_roles r
JOIN dtlms_permissions p ON (
    (r.role_code = 'platform_admin') OR
    (r.role_code = 'student' AND p.permission_code IN ('dashboard:read')) OR
    (r.role_code = 'advisor' AND p.permission_code IN ('dashboard:read', 'students:read', 'training:read', 'degree:read')) OR
    (r.role_code = 'recruit_reviewer' AND p.permission_code IN ('dashboard:read', 'recruitment:read')) OR
    (r.role_code = 'interview_officer' AND p.permission_code IN ('dashboard:read', 'recruitment:read')) OR
    (r.role_code = 'hrbp' AND p.permission_code IN ('dashboard:read', 'students:read', 'training:read')) OR
    (r.role_code = 'party_affairs' AND p.permission_code IN ('dashboard:read', 'students:read', 'audit:read'))
)
ON CONFLICT DO NOTHING;

INSERT INTO dtlms_system_configs (config_key, config_value, description)
VALUES
    ('report_overdue_days', '7', '科研报告逾期提醒阈值'),
    ('report_escalation_days', '14', '科研报告升级提醒阈值'),
    ('training_plan_edit_limit', '3', '培养方案每学年最大修改次数'),
    ('thesis_plagiarism_threshold', '20', '学位论文查重率阈值'),
    ('blind_review_pass_score', '75', '盲审平均通过分'),
    ('redis_key_prefix', 'CTDTLMS_', 'Redis 统一前缀')
ON CONFLICT (config_key) DO NOTHING;
