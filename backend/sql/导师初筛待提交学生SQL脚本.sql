-- 获取待提交清单
SELECT
  stu.ID AS student_id,
  ra.candidate_no, -- 报名号
  ra.business_key,
  stu.full_name, -- 学生姓名
  ra.ID AS application_id,
  ra.first_choice_screening_submitted_at,
  ra.second_choice_screening_submitted_at,
  ra.first_choice,
  ra.first_choice_id,
  ra.first_choice_screening_score,
  ra.second_choice,
  ra.second_choice_id,
  ra.second_choice_screening_score,
  
  '第一志愿' AS choice_name -- 待提交属于哪一个志愿（初筛轮次）
FROM
  dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON stu.ID = ra.portal_student_id 
WHERE
  ( first_choice = {传入当前登录导师姓名} OR first_choice_id = {传入当前登录导师ID} ) 
  AND ( first_choice_screening_submitted_at IS NULL ) 
  AND ra.application_status = 'initial_screening_first'
  UNION ALL
SELECT
  stu.ID AS student_id,
  ra.candidate_no,
  ra.business_key,
  stu.full_name, -- 学生姓名
  ra.ID AS application_id,
  ra.first_choice_screening_submitted_at,
  ra.second_choice_screening_submitted_at,
  ra.first_choice,
  ra.first_choice_id,
  ra.first_choice_screening_score,
  ra.second_choice,
  ra.second_choice_id,
  ra.second_choice_screening_score,
  
  '第二志愿' AS choice_name -- 待提交属于哪一个志愿（初筛轮次）
FROM
  dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON stu.ID = ra.portal_student_id 
WHERE
  ( second_choice = {传入当前登录导师姓名} OR second_choice_id = {传入当前登录导师ID} ) 
  AND ( second_choice_screening_submitted_at IS NULL AND first_choice_screening_submitted_at IS NOT NULL)
  AND ra.application_status = 'initial_screening_second'