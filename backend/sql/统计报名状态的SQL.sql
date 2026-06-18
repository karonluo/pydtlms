select 
CASE 
 WHEN application_status = 'terminated' THEN '报名已经终止'
 WHEN application_status = 'submitted' THEN '报名已提交未审核'
 WHEN application_status = 'returned' THEN '驳回重填'
 WHEN application_status = 'background_review' THEN '等待背景评估'
 WHEN application_status = 'initial_screening_first' THEN '等待第一志愿导师评分'
 WHEN application_status = 'initial_screening_second' THEN '等待第二志愿导师评分'
 WHEN application_status = 'initial_screening_confirmation' THEN '等待初筛确认'
END AS application_status_state
,count(application_status) from dtlms_recruitment_applications group by application_status;