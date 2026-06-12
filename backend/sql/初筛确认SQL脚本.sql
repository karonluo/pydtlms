-- 初筛确认 SQL 查询模板
-- 参数说明：
-- :plan_id   招聘计划 ID
-- :limit     分页大小
-- :offset    分页偏移
SELECT
  app.id AS application_id,
  stu.id AS student_id,
  app.plan_id,
  app.candidate_no,
  stu.full_name,
  app.first_choice,
  app.first_choice_screening_score,
  app.second_choice,
  app.second_choice_screening_score,
  app.first_choice_screening_submitted_at,
  app.second_choice_screening_submitted_at,
  app.application_status,
  app.intended_advisor_name
FROM dtlms_portal_students AS stu
LEFT JOIN dtlms_recruitment_applications AS app
  ON app.portal_student_id = stu.id
WHERE app.application_status = 'initial_screening_confirmation'
  AND app.plan_id = :plan_id
  AND app.is_deleted = FALSE
  AND (
    app.first_choice_screening_score >= 80
    OR app.second_choice_screening_score >= 80
  )
  AND (
    app.first_choice_screening_submitted_at IS NOT NULL
    OR app.second_choice_screening_submitted_at IS NOT NULL
  )
ORDER BY app.id DESC
LIMIT :limit OFFSET :offset