BEGIN;

-- 执行前提：
-- 1. 已完成 010/015/023/028/030/040 等基础建表与 RBAC 初始化。
-- 2. 若现网已存在 runtime state，本脚本会同步更新 runtime 表；
--    若 dtlms_runtime_counters 为空，则只写关系表，不主动初始化 runtime state。
-- 3. 导师账号默认密码为 ChangeMe@123，下面是其 pbkdf2_sha256 哈希。

CREATE TEMP TABLE tmp_center_seed (
    seed_order INTEGER PRIMARY KEY,
    center_name VARCHAR(128) NOT NULL,
    director_name VARCHAR(128) NOT NULL,
    advisor_names TEXT[] NOT NULL
) ON COMMIT DROP;

INSERT INTO tmp_center_seed (seed_order, center_name, director_name, advisor_names)
VALUES
    (1, '前沿探索中心', '乔宇', ARRAY['乔宇', '周伯文', '成宇', '石博天', '薛天帆', '蔡品隆', '邹娜', '刘翼豪', '何军军', '陈昕苑', '胡杨', '张超']),
    (2, 'AI For Science中心', '白磊', ARRAY['白磊', '周伯文', '欧阳万里', '张铂', '李玉强', '董楠卿', '宋纯锋', '胡舒悦', '王潚崧', '郝红霞']),
    (3, '大模型中心', '陈恺', ARRAY['陈恺', '周伯文', '林达华', '王利民', '张文蔚', '郭琦鹏', '王毅', '李亦宁', '张超', '张奇']),
    (4, '物理智能中心', '张伟楠', ARRAY['张伟楠', '周伯文', '沈春华', '翟少鹏', '赵斌', '吕照阳', '穆尧', '沈渊']),
    (5, '安全可信AI中心', '胡侠', ARRAY['胡侠', '周伯文', '陆超超', '邵婧', '王迎春', '杨超', '滕妍', '瞿晶晶']),
    (6, '评测中心', '翟广涛', ARRAY['翟广涛', '周伯文', '胡侠']),
    (7, 'Data-CentricAI', '何聪辉', ARRAY['何聪辉', '周伯文', '林达华', '王斌', '吴郦军', '吴江', '邱剑涛']),
    (8, '系统平台中心', '林达华', ARRAY['林达华', '周伯文', '李恒杰']);

CREATE TEMP TABLE tmp_username_seed (
    full_name VARCHAR(128) PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE
) ON COMMIT DROP;

INSERT INTO tmp_username_seed (full_name, username)
VALUES
    ('乔宇', 'qiaoyu'),
    ('周伯文', 'zhoubowen'),
    ('成宇', 'chengyu'),
    ('石博天', 'shibotian'),
    ('薛天帆', 'xuetianfan'),
    ('蔡品隆', 'caipinlong'),
    ('邹娜', 'zouna'),
    ('刘翼豪', 'liuyihao'),
    ('何军军', 'hejunjun'),
    ('陈昕苑', 'chenxinyuan'),
    ('胡杨', 'huyang'),
    ('张超', 'zhangchao'),
    ('白磊', 'bailei'),
    ('欧阳万里', 'ouyangwanli'),
    ('张铂', 'zhangbo'),
    ('李玉强', 'liyuqiang'),
    ('董楠卿', 'dongnanqing'),
    ('宋纯锋', 'songchunfeng'),
    ('胡舒悦', 'hushuyue'),
    ('王潚崧', 'wangsusong'),
    ('郝红霞', 'haohongxia'),
    ('陈恺', 'chenkai'),
    ('林达华', 'lindahua'),
    ('王利民', 'wanglimin'),
    ('张文蔚', 'zhangwenwei'),
    ('郭琦鹏', 'guoqipeng'),
    ('王毅', 'wangyi'),
    ('李亦宁', 'liyining'),
    ('张奇', 'zhangqi'),
    ('张伟楠', 'zhangweinan'),
    ('沈春华', 'shenchunhua'),
    ('翟少鹏', 'dishaopeng'),
    ('赵斌', 'zhaobin'),
    ('吕照阳', 'lvzhaoyang'),
    ('穆尧', 'muyao'),
    ('沈渊', 'shenyuan'),
    ('胡侠', 'huxia'),
    ('陆超超', 'luchaochao'),
    ('邵婧', 'shaojing'),
    ('王迎春', 'wangyingchun'),
    ('杨超', 'yangchao'),
    ('滕妍', 'tengyan'),
    ('瞿晶晶', 'qujingjing'),
    ('翟广涛', 'diguangtao'),
    ('何聪辉', 'heconghui'),
    ('王斌', 'wangbin'),
    ('吴郦军', 'wulijun'),
    ('吴江', 'wujiang'),
    ('邱剑涛', 'qiujiantao'),
    ('李恒杰', 'lihengjie');

CREATE TEMP TABLE tmp_advisor_seed ON COMMIT DROP AS
WITH expanded AS (
    SELECT DISTINCT
        c.seed_order,
        c.center_name,
        c.director_name,
        advisor_name
    FROM tmp_center_seed AS c
    CROSS JOIN LATERAL unnest(c.advisor_names) AS advisor_name
), center_agg AS (
    SELECT
        advisor_name AS full_name,
        array_agg(center_name ORDER BY seed_order) AS center_names,
        array_agg(center_name ORDER BY seed_order) FILTER (WHERE advisor_name = director_name) AS lead_center_names
    FROM expanded
    GROUP BY advisor_name
)
SELECT
    u.full_name,
    u.username,
    CASE
        WHEN COALESCE(array_length(ca.lead_center_names, 1), 0) > 0 THEN ca.lead_center_names[1]
        WHEN COALESCE(array_length(ca.center_names, 1), 0) = 1 THEN ca.center_names[1]
        ELSE '多中心联合'
    END AS department_name,
    array_to_string(ca.center_names, '、') AS research_direction
FROM tmp_username_seed AS u
JOIN center_agg AS ca ON ca.full_name = u.full_name;

INSERT INTO dtlms_roles (role_code, role_name, scope_name, description, is_deleted)
VALUES ('advisor', '导师', '培养与学位', '培养方案制定、报告审阅、答辩指导', FALSE)
ON CONFLICT (role_code) DO UPDATE
SET role_name = EXCLUDED.role_name,
    scope_name = EXCLUDED.scope_name,
    description = EXCLUDED.description,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

UPDATE dtlms_advisors AS a
SET title = '导师',
    organization_name = s.department_name,
    research_direction = s.research_direction,
    annual_quota = 0,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
WHERE a.full_name = s.full_name;

WITH advisor_no_base AS (
    SELECT COALESCE(MAX(CAST(SUBSTRING(advisor_no FROM 4) AS INTEGER)), 0) AS max_no
    FROM dtlms_advisors
    WHERE advisor_no ~ '^ADV[0-9]+$'
), missing_advisors AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (ORDER BY s.full_name) AS rn
    FROM tmp_advisor_seed AS s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dtlms_advisors AS a
        WHERE a.full_name = s.full_name
    )
)
INSERT INTO dtlms_advisors (
    advisor_no,
    full_name,
    title,
    organization_name,
    research_direction,
    annual_quota,
    is_deleted
)
SELECT
    CONCAT('ADV', LPAD((b.max_no + m.rn)::TEXT, 3, '0')),
    m.full_name,
    '导师',
    m.department_name,
    m.research_direction,
    0,
    FALSE
FROM missing_advisors AS m
CROSS JOIN advisor_no_base AS b;

UPDATE dtlms_users AS u
SET full_name = s.full_name,
    email = COALESCE(NULLIF(u.email, ''), CONCAT(s.username, '@dtlms.local')),
    department_name = s.department_name,
    password_hash = COALESCE(NULLIF(u.password_hash, ''), '$pbkdf2-sha256$29000$ESIkZKwVorQ2Ziyl9N77Xw$FkNpUi.BNeyqPLVId/t5Lz8zI0V1H7AbVTwDtfY.CNM'),
    is_active = TRUE,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
WHERE u.username = s.username;

INSERT INTO dtlms_users (
    username,
    full_name,
    email,
    department_name,
    phone_number,
    password_hash,
    is_active,
    is_deleted,
    last_login_at
)
SELECT
    s.username,
    s.full_name,
    CONCAT(s.username, '@dtlms.local'),
    s.department_name,
    NULL,
    '$pbkdf2-sha256$29000$ESIkZKwVorQ2Ziyl9N77Xw$FkNpUi.BNeyqPLVId/t5Lz8zI0V1H7AbVTwDtfY.CNM',
    TRUE,
    FALSE,
    NULL
FROM tmp_advisor_seed AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM dtlms_users AS u
    WHERE u.username = s.username
);

WITH advisor_role AS (
    SELECT id
    FROM dtlms_roles
    WHERE role_code = 'advisor'
      AND is_deleted = FALSE
    ORDER BY id
    LIMIT 1
)
INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
SELECT
    u.id,
    r.id,
    'seed_research_centers'
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
CROSS JOIN advisor_role AS r
ON CONFLICT (user_id, role_id) DO UPDATE
SET grant_source = EXCLUDED.grant_source,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_user_profiles (
    username,
    full_name,
    role_name,
    department_name,
    phone_number,
    email,
    theme_color
)
SELECT
    u.username,
    s.full_name,
    '导师',
    s.department_name,
    u.phone_number,
    COALESCE(NULLIF(up.email, ''), NULLIF(u.email, ''), CONCAT(u.username, '@dtlms.local')),
    '#13795b'
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
ON CONFLICT (username) DO UPDATE
SET full_name = EXCLUDED.full_name,
    role_name = EXCLUDED.role_name,
    department_name = EXCLUDED.department_name,
    phone_number = COALESCE(dtlms_user_profiles.phone_number, EXCLUDED.phone_number),
    email = COALESCE(dtlms_user_profiles.email, EXCLUDED.email),
    theme_color = EXCLUDED.theme_color,
    updated_at = CURRENT_TIMESTAMP;

UPDATE dtlms_teams AS t
SET department_name = s.center_name,
    discipline_name = COALESCE(NULLIF(t.discipline_name, ''), '未分配学科'),
    lead_advisor_id = a.id,
    research_directions = NULL,
    team_status = 'active',
    established_on = COALESCE(t.established_on, CURRENT_DATE),
    description = '按研究中心主数据维护需求批量导入。',
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_center_seed AS s
LEFT JOIN dtlms_advisors AS a
    ON a.full_name = s.director_name
   AND a.is_deleted = FALSE
WHERE t.team_name = s.center_name;

WITH team_code_base AS (
    SELECT COALESCE(MAX(CAST(SUBSTRING(team_code FROM 8) AS INTEGER)), 0) AS max_no
    FROM dtlms_teams
    WHERE team_code ~ '^CENTER-[0-9]+$'
), missing_teams AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (ORDER BY s.seed_order) AS rn
    FROM tmp_center_seed AS s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dtlms_teams AS t
        WHERE t.team_name = s.center_name
    )
)
INSERT INTO dtlms_teams (
    team_code,
    team_name,
    department_name,
    discipline_name,
    lead_advisor_id,
    research_directions,
    team_status,
    established_on,
    description,
    is_deleted
)
SELECT
    CONCAT('CENTER-', LPAD((b.max_no + m.rn)::TEXT, 3, '0')),
    m.center_name,
    m.center_name,
    '未分配学科',
    a.id,
    NULL,
    'active',
    CURRENT_DATE,
    '按研究中心主数据维护需求批量导入。',
    FALSE
FROM missing_teams AS m
CROSS JOIN team_code_base AS b
LEFT JOIN dtlms_advisors AS a
    ON a.full_name = m.director_name
   AND a.is_deleted = FALSE;

DELETE FROM dtlms_team_advisors AS ta
USING dtlms_teams AS t, tmp_center_seed AS s
WHERE ta.team_id = t.id
  AND t.team_name = s.center_name;

INSERT INTO dtlms_team_advisors (
    team_id,
    advisor_id,
    advisor_role,
    joined_on,
    left_on,
    is_deleted
)
SELECT
    t.id,
    a.id,
    CASE
        WHEN names.advisor_name = s.director_name THEN 'lead'
        ELSE 'member'
    END,
    COALESCE(t.established_on, CURRENT_DATE),
    NULL,
    FALSE
FROM tmp_center_seed AS s
JOIN dtlms_teams AS t ON t.team_name = s.center_name
CROSS JOIN LATERAL unnest(s.advisor_names) AS names(advisor_name)
JOIN dtlms_advisors AS a
    ON a.full_name = names.advisor_name
   AND a.is_deleted = FALSE
ON CONFLICT (team_id, advisor_id) DO UPDATE
SET advisor_role = EXCLUDED.advisor_role,
    joined_on = EXCLUDED.joined_on,
    left_on = NULL,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_roles (id, payload, updated_at)
SELECT
    r.id,
    jsonb_build_object(
        'id', r.id,
        'role_code', r.role_code,
        'role_name', r.role_name,
        'scope_name', COALESCE(r.scope_name, '培养与学位'),
        'description', COALESCE(r.description, ''),
        'permissions', to_jsonb(
            COALESCE(
                (
                    SELECT array_agg(p.permission_code ORDER BY p.permission_code)
                    FROM dtlms_role_permissions AS rp
                    JOIN dtlms_permissions AS p
                        ON p.id = rp.permission_id
                       AND p.is_deleted = FALSE
                    WHERE rp.role_id = r.id
                ),
                ARRAY[]::VARCHAR[]
            )
        )
    ),
    CURRENT_TIMESTAMP
FROM dtlms_roles AS r
WHERE r.role_code = 'advisor'
  AND r.is_deleted = FALSE
  AND EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_system_users (id, payload, updated_at)
SELECT
    u.id,
    jsonb_build_object(
        'id', u.id,
        'username', u.username,
        'full_name', u.full_name,
        'role_code', 'advisor',
        'department_name', COALESCE(up.department_name, u.department_name, ''),
        'phone_number', COALESCE(up.phone_number, u.phone_number),
        'account_status', CASE WHEN u.is_active THEN '启用' ELSE '停用' END,
        'last_login_at', CASE WHEN u.last_login_at IS NULL THEN NULL ELSE TO_CHAR(u.last_login_at, 'YYYY-MM-DD HH24:MI:SS') END,
        'password_hash', u.password_hash
    ),
    CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_profiles (username, payload, updated_at)
SELECT
    u.username,
    jsonb_build_object(
        'username', u.username,
        'full_name', u.full_name,
        'role_name', '导师',
        'department_name', COALESCE(up.department_name, u.department_name, ''),
        'phone_number', COALESCE(up.phone_number, u.phone_number),
        'email', COALESCE(NULLIF(up.email, ''), NULLIF(u.email, ''), CONCAT(u.username, '@dtlms.local')),
        'theme_color', '#13795b'
    ),
    CURRENT_TIMESTAMP
FROM tmp_advisor_seed AS s
JOIN dtlms_users AS u ON u.username = s.username
LEFT JOIN dtlms_user_profiles AS up ON up.username = u.username
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (username) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_teams (id, payload, updated_at)
SELECT
    t.id,
    jsonb_build_object(
        'id', t.id,
        'team_code', t.team_code,
        'team_name', s.center_name,
        'department_name', COALESCE(t.department_name, s.center_name),
        'discipline_name', COALESCE(NULLIF(t.discipline_name, ''), '未分配学科'),
        'lead_advisor_name', s.director_name,
        'advisor_names', to_jsonb(s.advisor_names),
        'research_directions', '[]'::jsonb,
        'status', '启用',
        'created_on', TO_CHAR(COALESCE(t.established_on, CURRENT_DATE), 'YYYY-MM-DD'),
        'established_on', TO_CHAR(COALESCE(t.established_on, CURRENT_DATE), 'YYYY-MM-DD'),
        'description', COALESCE(t.description, '按研究中心主数据维护需求批量导入。')
    ),
    CURRENT_TIMESTAMP
FROM tmp_center_seed AS s
JOIN dtlms_teams AS t ON t.team_name = s.center_name
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (id) DO UPDATE
SET payload = EXCLUDED.payload,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_runtime_counters (counter_name, counter_value, updated_at)
SELECT
    x.counter_name,
    x.counter_value,
    CURRENT_TIMESTAMP
FROM (
    VALUES
        (
            'roles',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_roles), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_roles WHERE is_deleted = FALSE), 0)
            )
        ),
        (
            'system_users',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_system_users), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_users WHERE is_deleted = FALSE), 0)
            )
        ),
        (
            'teams',
            GREATEST(
                COALESCE((SELECT MAX(id) FROM dtlms_runtime_teams), 0),
                COALESCE((SELECT MAX(id) FROM dtlms_teams WHERE is_deleted = FALSE), 0)
            )
        )
) AS x(counter_name, counter_value)
WHERE EXISTS (SELECT 1 FROM dtlms_runtime_counters)
ON CONFLICT (counter_name) DO UPDATE
SET counter_value = GREATEST(dtlms_runtime_counters.counter_value, EXCLUDED.counter_value),
    updated_at = CURRENT_TIMESTAMP;

COMMIT;
