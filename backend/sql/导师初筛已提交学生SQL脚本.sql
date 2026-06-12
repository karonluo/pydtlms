
SELECT 
stu.id AS student_id,
ra.candidate_no,
ra.business_key,
stu.full_name,
ra.id AS application_id,
ra.candidate_no,
ra.first_choice_screening_submitted_at,
ra.second_choice_screening_submitted_at,
ra.first_choice,
ra.first_choice_id,
ra.second_choice,
ra.second_choice_id,

CASE
  WHEN(ra.first_choice_screening_score IS NOT NULL) THEN ra.first_choice_screening_score
  WHEN(ra.second_choice_screening_score IS NOT NULL) THEN ra.second_choice_screening_score
END AS choice_score,

CASE 
  WHEN (first_choice_screening_submitted_at IS NOT NULL) THEN '第一志愿' 
  WHEN (second_choice_screening_submitted_at IS NOT NULL) THEN '第二志愿'
END AS choice_name
 FROM 
dtlms_portal_students AS stu 
LEFT JOIN dtlms_recruitment_applications AS ra ON stu.id=ra.portal_student_id
WHERE 
(first_choice = {当前登录导师姓名} OR first_choice_id={当前登录导师ID} OR second_choice = {当前登录导师姓名} OR second_choice_id={当前登录导师ID}) AND 
(first_choice_screening_submitted_at IS NOT NULL OR second_choice_screening_submitted_at is not NULL)