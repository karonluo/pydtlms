  SELECT 
  rp.plan_name,
  ra.candidate_no, 
  ra.student_name, 
  ra.plan_id, 
  ra.first_choice, 
  ra.second_choice,
  ra.application_status,
  CASE 
    WHEN ra.application_status = 'submitted' THEN '已提交报名'
    WHEN ra.application_status = 'initial_screening_first' THEN '第一志愿初筛'
    WHEN ra.application_status = 'initial_screening_second' THEN '第二志愿初筛'
    WHEN ra.application_status = 'terminated' THEN '报名终止'
    WHEN ra.application_status = 'initial_screening_confirmation' THEN '初筛确认'
    WHEN ra.application_status = 'returned' THEN '驳回重填'
    WHEN ra.application_status = 'background_review' THEN '背景评估'
  END AS current_status,
  
  ra.intended_advisor_name,
  ra.first_choice_screening_submitted_at, --第一志愿导师提交日期
  ra.second_choice_screening_submitted_at --第二志愿导师提交日期
  FROM dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON ra.portal_student_id = stu.id
  LEFT JOIN dtlms_recruitment_plans AS rp ON ra.plan_id = rp.id
  WHERE 1=1 
  AND ra.candidate_no != ''
  AND ra.is_deleted = FALSE
  ORDER BY ra.candidate_no DESC