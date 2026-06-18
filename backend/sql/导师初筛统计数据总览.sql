

-- 作为第一志愿导师数据分析概述
SELECT
count(application_status) as reson_count,
CASE 
 WHEN application_status = 'terminated' THEN '已终止报名'
 WHEN application_status = 'background_review' THEN '等待背景评估,未到您处理。'
 WHEN application_status = 'initial_screening_second' THEN '已提交, 分数不足已到第二志愿导师处。'
 WHEN application_status = 'initial_screening_confirmation'  THEN '已提交, 等待初筛确认。'
END AS application_state FROM dtlms_recruitment_applications WHERE 1=1 
AND first_choice={传入的导师姓名}
GROUP BY application_status;

-- 作为第二志愿导师数据分析概述
SELECT
count(application_status) as reson_count,
CASE 
 WHEN (application_status = 'terminated') THEN '已终止报名'
 WHEN application_status = 'background_review' THEN '等待背景评估'
 WHEN application_status = 'initial_screening_first' THEN '等待第一志愿导师评分'
 WHEN application_status = 'initial_screening_confirmation'  THEN '已提交到等待初筛确认'
END AS application_state
FROM dtlms_recruitment_applications WHERE 1=1 
AND second_choice={传入的导师姓名}
GROUP BY application_status