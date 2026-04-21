ALTER TABLE IF EXISTS dtlms_portal_student_profiles
    ADD COLUMN IF NOT EXISTS profile_photo_url VARCHAR(255);

INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES
    ('民族', 'student_ethnic_group', '启用', '学生民族字典')
ON CONFLICT (dict_type) DO UPDATE SET
    dict_name = EXCLUDED.dict_name,
    status = EXCLUDED.status,
    remark = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP;

WITH seed_data(dict_type, label, value, sort_order, status, color_type, css_class, remark) AS (
    VALUES
        ('student_ethnic_group', '汉族', '汉族', 10, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '蒙古族', '蒙古族', 20, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '回族', '回族', 30, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '藏族', '藏族', 40, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '维吾尔族', '维吾尔族', 50, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '苗族', '苗族', 60, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '彝族', '彝族', 70, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '壮族', '壮族', 80, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '布依族', '布依族', 90, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '朝鲜族', '朝鲜族', 100, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '满族', '满族', 110, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '侗族', '侗族', 120, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '瑶族', '瑶族', 130, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '白族', '白族', 140, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '土家族', '土家族', 150, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '哈尼族', '哈尼族', 160, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '哈萨克族', '哈萨克族', 170, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '傣族', '傣族', 180, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '黎族', '黎族', 190, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '傈僳族', '傈僳族', 200, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '佤族', '佤族', 210, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '畲族', '畲族', 220, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '高山族', '高山族', 230, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '拉祜族', '拉祜族', 240, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '水族', '水族', 250, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '东乡族', '东乡族', 260, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '纳西族', '纳西族', 270, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '景颇族', '景颇族', 280, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '柯尔克孜族', '柯尔克孜族', 290, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '土族', '土族', 300, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '达斡尔族', '达斡尔族', 310, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '仫佬族', '仫佬族', 320, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '羌族', '羌族', 330, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '布朗族', '布朗族', 340, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '撒拉族', '撒拉族', 350, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '毛南族', '毛南族', 360, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '仡佬族', '仡佬族', 370, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '锡伯族', '锡伯族', 380, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '阿昌族', '阿昌族', 390, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '普米族', '普米族', 400, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '塔吉克族', '塔吉克族', 410, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '怒族', '怒族', 420, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '乌孜别克族', '乌孜别克族', 430, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '俄罗斯族', '俄罗斯族', 440, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '鄂温克族', '鄂温克族', 450, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '德昂族', '德昂族', 460, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '保安族', '保安族', 470, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '裕固族', '裕固族', 480, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '京族', '京族', 490, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '塔塔尔族', '塔塔尔族', 500, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '独龙族', '独龙族', 510, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '鄂伦春族', '鄂伦春族', 520, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '赫哲族', '赫哲族', 530, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '门巴族', '门巴族', 540, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '珞巴族', '珞巴族', 550, '启用', NULL, NULL, NULL),
        ('student_ethnic_group', '基诺族', '基诺族', 560, '启用', NULL, NULL, NULL),
        ('student_political_status', '民革党员', '民革党员', 40, '启用', NULL, NULL, NULL),
        ('student_political_status', '民盟盟员', '民盟盟员', 50, '启用', NULL, NULL, NULL),
        ('student_political_status', '民建会员', '民建会员', 60, '启用', NULL, NULL, NULL),
        ('student_political_status', '民进会员', '民进会员', 70, '启用', NULL, NULL, NULL),
        ('student_political_status', '农工党党员', '农工党党员', 80, '启用', NULL, NULL, NULL),
        ('student_political_status', '致公党党员', '致公党党员', 90, '启用', NULL, NULL, NULL),
        ('student_political_status', '九三学社社员', '九三学社社员', 100, '启用', NULL, NULL, NULL),
        ('student_political_status', '台盟盟员', '台盟盟员', 110, '启用', NULL, NULL, NULL),
        ('student_political_status', '无党派人士', '无党派人士', 120, '启用', NULL, NULL, NULL),
        ('student_political_status', '群众', '群众', 130, '启用', NULL, NULL, NULL)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id, s.dict_type, s.label, s.value, s.sort_order, s.status, s.color_type, s.css_class, s.remark
FROM seed_data s
JOIN dtlms_dict_types t ON t.dict_type = s.dict_type
ON CONFLICT (dict_type, value) DO UPDATE SET
    label = EXCLUDED.label,
    sort_order = EXCLUDED.sort_order,
    status = EXCLUDED.status,
    color_type = EXCLUDED.color_type,
    css_class = EXCLUDED.css_class,
    remark = EXCLUDED.remark,
    dict_type_id = EXCLUDED.dict_type_id,
    updated_at = CURRENT_TIMESTAMP;