-- ============================================================
-- 脚本名称: update20260704.sql
-- 脚本说明: 系统字典新增【入取学校】类型及 13 所学校数据
--           业务背景: 黑客松(hackathon)活动结束后,需要为每位学生记录
--                    最终被录取(入取)到的目标学校,作为入营后去向台账。
--                    该字典由业务方指定 13 所顶尖研究型大学,既包含
--                    C9/985 高校,也包含西湖大学、上海科技大学等
--                    新型研究型大学。
--
-- 字典类型:
--           dict_type = 'admission_offered_school'
--           dict_name = '入取学校'
--           备注     = 入取学校字典(黑客松活动最终入取的学校)
--
-- 字典数据(13 项):
--           清华大学、北京大学、上海交通大学、复旦大学、浙江大学、
--           中国科学技术大学、同济大学、西安交通大学、哈尔滨工业大学、
--           南京大学、北京航空航天大学、西湖大学、上海科技大学
--
-- 字段设计:
--           - dict_type_id    通过子查询关联到 dtlms_dict_types.id
--           - label / value   都填学校中文名(参考 985/211 字典的写法)
--           - sort_order      10/20/30/... 递增,按用户给定的顺序
--           - status          '启用'
--           - color_type/css_class/remark  保持 NULL(简化)
--
-- 前置条件:
--           - dtlms_dict_types / dtlms_dict_data 表已存在(由 050_dict_schema.sql 建立)
--           - 业务方已确认 13 所学校的清单
--
-- 后续脚本: 无
--
-- 注意事项:
--           - 本脚本不显式 BEGIN/COMMIT,沿用 psql 默认每文件一个事务的行为,
--             避免与 DO 块中 PL/pgSQL 的 DECLARE/BEGIN 冲突。
--           - 全部使用 ON CONFLICT ... DO UPDATE 保证脚本可重复执行
--           - 执行后请按惯例运行 _extract_schema.py 刷新 database_schema.md
-- ============================================================

-- 1) 写入字典类型 admission_offered_school(如果已存在则更新名称/状态/备注)
INSERT INTO dtlms_dict_types (dict_name, dict_type, status, remark)
VALUES ('入取学校', 'admission_offered_school', '启用', '入取学校字典(黑客松活动最终入取的学校)')
ON CONFLICT (dict_type) DO UPDATE SET
    dict_name = EXCLUDED.dict_name,
    status    = EXCLUDED.status,
    remark    = EXCLUDED.remark,
    updated_at = CURRENT_TIMESTAMP;

-- 2) 写入 13 所学校数据
WITH seed_schools(label, sort_order) AS (
    VALUES
        ('清华大学',           10),
        ('北京大学',           20),
        ('上海交通大学',       30),
        ('复旦大学',           40),
        ('浙江大学',           50),
        ('中国科学技术大学',   60),
        ('同济大学',           70),
        ('西安交通大学',       80),
        ('哈尔滨工业大学',     90),
        ('南京大学',          100),
        ('北京航空航天大学',  110),
        ('西湖大学',          120),
        ('上海科技大学',      130)
)
INSERT INTO dtlms_dict_data (dict_type_id, dict_type, label, value, sort_order, status, color_type, css_class, remark)
SELECT t.id,
       'admission_offered_school',
       s.label,
       s.label,
       s.sort_order,
       '启用',
       NULL,
       NULL,
       NULL
FROM seed_schools s
JOIN dtlms_dict_types t ON t.dict_type = 'admission_offered_school'
ON CONFLICT (dict_type, value) DO UPDATE SET
    label        = EXCLUDED.label,
    sort_order   = EXCLUDED.sort_order,
    status       = EXCLUDED.status,
    color_type   = EXCLUDED.color_type,
    css_class    = EXCLUDED.css_class,
    remark       = EXCLUDED.remark,
    dict_type_id = EXCLUDED.dict_type_id,
    updated_at   = CURRENT_TIMESTAMP;

-- 3) 统计输出(便于人工核对)
DO $$
DECLARE
    v_type_id   BIGINT;
    v_type_name TEXT;
    v_cnt       BIGINT;
BEGIN
    SELECT id, dict_name INTO v_type_id, v_type_name
      FROM dtlms_dict_types
     WHERE dict_type = 'admission_offered_school';
    SELECT COUNT(*) INTO v_cnt
      FROM dtlms_dict_data
     WHERE dict_type = 'admission_offered_school'
       AND is_deleted = FALSE;
    RAISE NOTICE '字典类型: id=%, dict_name=%, dict_type=admission_offered_school', v_type_id, v_type_name;
    RAISE NOTICE '字典数据条数: %(期望 13)', v_cnt;
END $$;

-- ============================================================
-- 脚本名称: update20260704.sql (续)
-- 脚本说明: 为 dtlms_plan_offer 增加字段 admission_offered_school
--           用途: 存储【入取学校】的字典值(value 与 label 一致,
--                即学校中文名,例如 '清华大学' / '西湖大学' 等)
--
-- 字段设计:
--           - admission_offered_school  varchar(64) NULL
--           - 长度 64: 当前 13 项中最长「中国地质大学(武汉)」≈ 11 字符,
--             预留扩展空间(双一流新型高校持续增加的可能)
--           - 允许 NULL: 学生尚未被任何学校入取/未上传学校时为空
--           - 与本脚本上半段创建的 admission_offered_school 字典配套,
--             业务上建议前端下拉只允许选择 dict_data 中 label 与之匹配的值
--
-- 前置条件:
--           - dtlms_plan_offer 表已存在
--           - 上半段字典类型 admission_offered_school 已存在
--
-- 后续脚本: 无
--
-- 注意事项:
--           - 使用 ADD COLUMN IF NOT EXISTS 保证脚本可重复执行
--           - 执行后请按惯例运行 _extract_schema.py 刷新 database_schema.md
-- ============================================================

-- 1) 新增字段(幂等)
ALTER TABLE public.dtlms_plan_offer
  ADD COLUMN IF NOT EXISTS admission_offered_school varchar(64);

-- 2) 添加字段注释(幂等: 用 DO 块判断列注释是否已存在,避免重复抛错)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_catalog.pg_description d
          JOIN pg_catalog.pg_class c ON c.oid = d.objoid
          JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid AND a.attnum = d.objsubid
         WHERE c.relname = 'dtlms_plan_offer'
           AND a.attname = 'admission_offered_school'
    ) THEN
        EXECUTE 'COMMENT ON COLUMN public.dtlms_plan_offer.admission_offered_school
                 IS ''入取学校(字典 admission_offered_school 的 value,通常与 label 一致)''';
    END IF;
END $$;

-- 3) 统计输出
DO $$
DECLARE
    v_type_count BIGINT;
    v_data_count BIGINT;
    v_col_exists BOOLEAN;
BEGIN
    SELECT COUNT(*) INTO v_type_count
      FROM dtlms_dict_types WHERE dict_type = 'admission_offered_school';
    SELECT COUNT(*) INTO v_data_count
      FROM dtlms_dict_data
     WHERE dict_type = 'admission_offered_school' AND is_deleted = FALSE;
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE table_schema = 'public'
           AND table_name   = 'dtlms_plan_offer'
           AND column_name  = 'admission_offered_school'
    ) INTO v_col_exists;
    RAISE NOTICE '字典类型 admission_offered_school 存在: %(期望 1)', (v_type_count >= 1);
    RAISE NOTICE '字典数据条数 admission_offered_school: %(期望 13)', v_data_count;
    RAISE NOTICE '字段 dtlms_plan_offer.admission_offered_school 已存在: %', v_col_exists;
END $$;
