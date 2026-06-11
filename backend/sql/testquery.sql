SELECT
  stu.id AS student_id,
  app.candidate_no,
  stu.full_name,
  app.first_choice,
  app.first_choice_screening_score,
  app.second_choice,
  app.second_choice_screening_score,
  app.first_choice_screening_submitted_at,
  app.second_choice_screening_submitted_at,
  app.application_status
FROM dtlms_portal_students AS stu
LEFT JOIN dtlms_recruitment_applications AS app
  ON app.portal_student_id = stu.id
WHERE app.application_status = 'initial_screening_confirmation'
  AND (
    app.first_choice_screening_score >= 80
    OR app.second_choice_screening_score >= 80
  )
  AND (
    app.first_choice_screening_submitted_at IS NOT NULL
    OR app.second_choice_screening_submitted_at IS NOT NULL
  )
  AND app.is_deleted = FALSE
  AND APP.plan_id =5 