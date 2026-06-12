SELECT
  ra.candidate_no,
  stu.full_name,
  stu.application_draft #>'{personal_statement,ai_industry_opinion}' AS draft_ai_industry_opinion,
  stu.application_draft #>'{personal_statement,ai_problem_statement}' AS draft_ai_problem_statement,
  apa.ai_industry_opinion,
  apa.ai_problem_statement,
  stu.created_at,
  stu.updated_at
FROM
  dtlms_portal_students AS stu
  LEFT JOIN dtlms_recruitment_applications AS ra ON ra.portal_student_id = stu.ID 
  LEFT JOIN dtlms_portal_application_personal_statements AS apa ON apa.application_id = ra.ID
  
WHERE
  1 = 1 
  AND ra.candidate_no IS NOT NULL 
  AND apa.ai_industry_opinion IS  NULL 
  AND apa.ai_problem_statement IS  NULL
  --AND application_draft IS NOT NULL