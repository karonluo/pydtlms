SELECT
--   ra.candidate_no,
--   stu.full_name,
--   stu.application_draft #> '{personal_statement,ai_industry_opinion}' AS draft_ai_industry_opinion,
--   stu.application_draft #> '{personal_statement,ai_problem_statement}' AS draft_ai_problem_statement,
--   stu.application_draft #> '{english_proficiencies,exam_name}' AS draft_englisth_exam_name,
--   stu.application_draft #> '{english_proficiencies,score_text}' AS draft_englisth_exam_name,
--   apa.ai_industry_opinion,
--   apa.ai_problem_statement,
--   aep.exam_name,
--   aep.score_text,
--   stu.created_at,
--   stu.updated_at,
--   ra.application_status
ra.application_status,
count(ra.application_status)
FROM
  dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON ra.portal_student_id = stu.
  ID LEFT JOIN dtlms_portal_application_personal_statements AS apa ON apa.application_id = ra.
  ID LEFT JOIN dtlms_portal_application_english_proficiencies AS aep ON aep.application_id = ra.ID 
WHERE
  1 = 1 
AND ra.candidate_no IS NOT NULL 
--AND apa.ai_industry_opinion IS  NULL 
--AND apa.ai_problem_statement IS  NULL
--AND application_draft IS NULL
AND stu.submitted_at IS NOT NULL
-- AND ra.application_status NOT IN ( 'initial_screening_first','initial_screening_second','initial_screening_confirmation')
  
AND aep.score_text = ''
GROUP BY ra.application_status;



SELECT
  ra.candidate_no,
  stu.full_name,
  stu.application_draft #> '{personal_statement,ai_industry_opinion}' AS draft_ai_industry_opinion,
  stu.application_draft #> '{personal_statement,ai_problem_statement}' AS draft_ai_problem_statement,
  stu.application_draft #> '{english_proficiencies,exam_name}' AS draft_englisth_exam_name,
  stu.application_draft #> '{english_proficiencies,score_text}' AS draft_englisth_exam_name,
  apa.ai_industry_opinion,
  apa.ai_problem_statement,
  aep.exam_name,
  aep.score_text,
  stu.created_at,
  stu.updated_at,
  ra.application_status,
  aep.certificate_attachment_url,
  ra.second_choice_screening_submitted_at

FROM
  dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON ra.portal_student_id = stu.
  ID LEFT JOIN dtlms_portal_application_personal_statements AS apa ON apa.application_id = ra.
  ID LEFT JOIN dtlms_portal_application_english_proficiencies AS aep ON aep.application_id = ra.ID 
WHERE
  1 = 1 
AND ra.candidate_no IS NOT NULL 
AND apa.ai_industry_opinion IS  NULL 
--AND apa.ai_problem_statement IS NULL
--AND application_draft IS NULL
AND stu.submitted_at IS NOT NULL
-- AND ra.application_status NOT IN ( 'initial_screening_first','initial_screening_second','initial_screening_confirmation')
-- AND STU.full_name='汤佳宸'
AND aep.score_text = '' 


