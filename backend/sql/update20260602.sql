-- 2026-06-02 生产环境系统字典补丁
-- 说明：新增“C9大学”“985大学”“211大学”系统字典及基础数据。

BEGIN;

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES
    ('C9大学', 'system_c9_university', '启用', 'C9大学字典'),
    ('985大学', 'system_985_university', '启用', '985大学字典')
ON CONFLICT (dict_type) DO UPDATE
SET dict_name = EXCLUDED.dict_name,
    status = EXCLUDED.status,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
    VALUES
        ('system_c9_university', '北京大学', '北京大学', 10, '启用', NULL, NULL, NULL),
        ('system_c9_university', '清华大学', '清华大学', 20, '启用', NULL, NULL, NULL),
        ('system_c9_university', '哈尔滨工业大学', '哈尔滨工业大学', 30, '启用', NULL, NULL, NULL),
        ('system_c9_university', '复旦大学', '复旦大学', 40, '启用', NULL, NULL, NULL),
        ('system_c9_university', '上海交通大学', '上海交通大学', 50, '启用', NULL, NULL, NULL),
        ('system_c9_university', '南京大学', '南京大学', 60, '启用', NULL, NULL, NULL),
        ('system_c9_university', '浙江大学', '浙江大学', 70, '启用', NULL, NULL, NULL),
        ('system_c9_university', '中国科学技术大学', '中国科学技术大学', 80, '启用', NULL, NULL, NULL),
        ('system_c9_university', '西安交通大学', '西安交通大学', 90, '启用', NULL, NULL, NULL),
        ('system_985_university', '清华大学', '清华大学', 10, '启用', NULL, NULL, NULL),
        ('system_985_university', '北京大学', '北京大学', 20, '启用', NULL, NULL, NULL),
        ('system_985_university', '中国科学技术大学', '中国科学技术大学', 30, '启用', NULL, NULL, NULL),
        ('system_985_university', '复旦大学', '复旦大学', 40, '启用', NULL, NULL, NULL),
        ('system_985_university', '中国人民大学', '中国人民大学', 50, '启用', NULL, NULL, NULL),
        ('system_985_university', '上海交通大学', '上海交通大学', 60, '启用', NULL, NULL, NULL),
        ('system_985_university', '南京大学', '南京大学', 70, '启用', NULL, NULL, NULL),
        ('system_985_university', '同济大学', '同济大学', 80, '启用', NULL, NULL, NULL),
        ('system_985_university', '浙江大学', '浙江大学', 90, '启用', NULL, NULL, NULL),
        ('system_985_university', '南开大学', '南开大学', 100, '启用', NULL, NULL, NULL),
        ('system_985_university', '北京航空航天大学', '北京航空航天大学', 110, '启用', NULL, NULL, NULL),
        ('system_985_university', '北京师范大学', '北京师范大学', 120, '启用', NULL, NULL, NULL),
        ('system_985_university', '武汉大学', '武汉大学', 130, '启用', NULL, NULL, NULL),
        ('system_985_university', '西安交通大学', '西安交通大学', 140, '启用', NULL, NULL, NULL),
        ('system_985_university', '天津大学', '天津大学', 150, '启用', NULL, NULL, NULL),
        ('system_985_university', '华中科技大学', '华中科技大学', 160, '启用', NULL, NULL, NULL),
        ('system_985_university', '北京理工大学', '北京理工大学', 170, '启用', NULL, NULL, NULL),
        ('system_985_university', '东南大学', '东南大学', 180, '启用', NULL, NULL, NULL),
        ('system_985_university', '中山大学', '中山大学', 190, '启用', NULL, NULL, NULL),
        ('system_985_university', '华东师范大学', '华东师范大学', 200, '启用', NULL, NULL, NULL),
        ('system_985_university', '哈尔滨工业大学', '哈尔滨工业大学', 210, '启用', NULL, NULL, NULL),
        ('system_985_university', '厦门大学', '厦门大学', 220, '启用', NULL, NULL, NULL),
        ('system_985_university', '西北工业大学', '西北工业大学', 230, '启用', NULL, NULL, NULL),
        ('system_985_university', '中南大学', '中南大学', 240, '启用', NULL, NULL, NULL),
        ('system_985_university', '大连理工大学', '大连理工大学', 250, '启用', NULL, NULL, NULL),
        ('system_985_university', '四川大学', '四川大学', 260, '启用', NULL, NULL, NULL),
        ('system_985_university', '电子科技大学', '电子科技大学', 270, '启用', NULL, NULL, NULL),
        ('system_985_university', '华南理工大学', '华南理工大学', 280, '启用', NULL, NULL, NULL),
        ('system_985_university', '吉林大学', '吉林大学', 290, '启用', NULL, NULL, NULL),
        ('system_985_university', '湖南大学', '湖南大学', 300, '启用', NULL, NULL, NULL),
        ('system_985_university', '重庆大学', '重庆大学', 310, '启用', NULL, NULL, NULL),
        ('system_985_university', '山东大学', '山东大学', 320, '启用', NULL, NULL, NULL),
        ('system_985_university', '中国农业大学', '中国农业大学', 330, '启用', NULL, NULL, NULL),
        ('system_985_university', '中国海洋大学', '中国海洋大学', 340, '启用', NULL, NULL, NULL),
        ('system_985_university', '中央民族大学', '中央民族大学', 350, '启用', NULL, NULL, NULL),
        ('system_985_university', '东北大学', '东北大学', 360, '启用', NULL, NULL, NULL),
        ('system_985_university', '兰州大学', '兰州大学', 370, '启用', NULL, NULL, NULL),
        ('system_985_university', '西北农林科技大学', '西北农林科技大学', 380, '启用', NULL, NULL, NULL),
        ('system_985_university', '国防科技大学', '国防科技大学', 390, '启用', NULL, NULL, NULL)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
    dict_type_id = EXCLUDED.dict_type_id,
    label = EXCLUDED.label,
    sort_order = EXCLUDED.sort_order,
    status = EXCLUDED.status,
    color_type = EXCLUDED.color_type,
    css_class = EXCLUDED.css_class,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

COMMIT;

BEGIN;

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES ('211大学', 'system_211_university', '启用', '211大学字典')
ON CONFLICT (dict_type) DO UPDATE
SET dict_name = EXCLUDED.dict_name,
    status = EXCLUDED.status,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

WITH seed_labels(label, sort_order) AS (
    VALUES
        ('清华大学', 10),
        ('北京大学', 20),
        ('中国科学技术大学', 30),
        ('复旦大学', 40),
        ('中国人民大学', 50),
        ('上海交通大学', 60),
        ('南京大学', 70),
        ('同济大学', 80),
        ('浙江大学', 90),
        ('上海财经大学', 100),
        ('南开大学', 110),
        ('北京航空航天大学', 120),
        ('中央财经大学', 130),
        ('北京师范大学', 140),
        ('武汉大学', 150),
        ('对外经济贸易大学', 160),
        ('西安交通大学', 170),
        ('天津大学', 180),
        ('华中科技大学', 190),
        ('北京理工大学', 200),
        ('东南大学', 210),
        ('北京外国语大学', 220),
        ('中山大学', 230),
        ('中国政法大学', 240),
        ('华东师范大学', 250),
        ('哈尔滨工业大学', 260),
        ('北京邮电大学', 270),
        ('厦门大学', 280),
        ('上海外国语大学', 290),
        ('西北工业大学', 300),
        ('西南财经大学', 310),
        ('中南大学', 320),
        ('大连理工大学', 330),
        ('中国传媒大学', 340),
        ('四川大学', 350),
        ('电子科技大学', 360),
        ('中南财经政法大学', 370),
        ('华南理工大学', 380),
        ('吉林大学', 390),
        ('南京航空航天大学', 400),
        ('湖南大学', 410),
        ('重庆大学', 420),
        ('北京科技大学', 430),
        ('北京交通大学', 440),
        ('山东大学', 450),
        ('华东理工大学', 460),
        ('西安电子科技大学', 470),
        ('天津医科大学', 480),
        ('南京理工大学', 490),
        ('中国农业大学', 500),
        ('华中师范大学', 510),
        ('中国海洋大学', 520),
        ('哈尔滨工程大学', 530),
        ('中央民族大学', 540),
        ('华北电力大学', 550),
        ('北京中医药大学', 560),
        ('暨南大学', 570),
        ('苏州大学', 580),
        ('武汉理工大学', 590),
        ('东北大学', 600),
        ('兰州大学', 610),
        ('中国药科大学', 620),
        ('东华大学', 630),
        ('河海大学', 640),
        ('北京林业大学', 650),
        ('河北工业大学', 660),
        ('北京工业大学', 670),
        ('江南大学', 680),
        ('北京化工大学', 690),
        ('西南交通大学', 700),
        ('上海大学', 710),
        ('南京师范大学', 720),
        ('中国地质大学（武汉）', 730),
        ('中国地质大学（北京）', 740),
        ('西北大学', 750),
        ('东北师范大学', 760),
        ('长安大学', 770),
        ('中国矿业大学（北京）', 780),
        ('华中农业大学', 790),
        ('合肥工业大学', 800),
        ('广西大学', 810),
        ('中国石油大学（华东）', 820),
        ('陕西师范大学', 830),
        ('南京农业大学', 840),
        ('湖南师范大学', 850),
        ('福州大学', 860),
        ('大连海事大学', 870),
        ('西北农林科技大学', 880),
        ('西南大学', 890),
        ('中国矿业大学', 900),
        ('云南大学', 910),
        ('太原理工大学', 920),
        ('华南师范大学', 930),
        ('北京体育大学', 940),
        ('中国石油大学（北京）', 950),
        ('安徽大学', 960),
        ('东北林业大学', 970),
        ('东北农业大学', 980),
        ('辽宁大学', 990),
        ('南昌大学', 1000),
        ('延边大学', 1010),
        ('内蒙古大学', 1020),
        ('四川农业大学', 1030),
        ('海南大学', 1040),
        ('贵州大学', 1050),
        ('郑州大学', 1060),
        ('新疆大学', 1070),
        ('宁夏大学', 1080),
        ('石河子大学', 1090),
        ('青海大学', 1100),
        ('国防科技大学', 1110),
        ('中央音乐学院', 1120),
        ('第二军医大学', 1130),
        ('第四军医大学', 1140),
        ('西藏大学', 1150)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, 'system_211_university', s.label, s.label, s.sort_order, '启用', NULL, NULL, NULL
FROM seed_labels s
JOIN dtlms_dict_types t ON t.dict_type = 'system_211_university'
ON CONFLICT (dict_type, value) DO UPDATE SET
    dict_type_id = EXCLUDED.dict_type_id,
    label = EXCLUDED.label,
    sort_order = EXCLUDED.sort_order,
    status = EXCLUDED.status,
    color_type = EXCLUDED.color_type,
    css_class = EXCLUDED.css_class,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

COMMIT;

BEGIN;

-- 平台管理员退回到资料审核/背景评估时，需要清空后续环节字段。
-- 这些字段不能保持 NOT NULL，否则退回会在增量落库时失败并触发接口卡顿。
ALTER TABLE IF EXISTS dtlms_recruitment_applications
    ALTER COLUMN advisor_screening_status DROP NOT NULL,
    ALTER COLUMN advisor_screening_round DROP NOT NULL,
    ALTER COLUMN initial_screening_status DROP NOT NULL,
    ALTER COLUMN initial_screening_notification_status DROP NOT NULL;

COMMIT;

BEGIN;

CREATE TABLE IF NOT EXISTS dtlms_qualification_review_logs (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL REFERENCES dtlms_recruitment_applications(id),
    reviewer_user_id BIGINT,
    reviewer_username VARCHAR(64) NOT NULL,
    reviewer_name VARCHAR(128),
    reviewer_role_code VARCHAR(64),
    action VARCHAR(32) NOT NULL,
    action_label VARCHAR(64) NOT NULL,
    review_comment TEXT,
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_qualification_review_logs_application
    ON dtlms_qualification_review_logs(application_id, reviewed_at DESC);

CREATE INDEX IF NOT EXISTS idx_qualification_review_logs_reviewer
    ON dtlms_qualification_review_logs(reviewer_username, reviewed_at DESC);

COMMIT;