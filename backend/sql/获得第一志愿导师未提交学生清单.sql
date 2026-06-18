
SELECT ra.id as application_id, ra.candidate_no, stu.full_name FROM dtlms_portal_students stu
LEFT JOIN dtlms_recruitment_applications ra on stu.id = ra.portal_student_id 
WHERE 1=1 
AND ra.first_choice_screening_submitted_at IS NULL
AND (ra.first_choice = {传入的导师姓名} OR ra.first_choice_id = {传入的导师ID} )
AND ra.application_status='initial_screening_first'
AND ra.candidate_no IS NOT NULL 