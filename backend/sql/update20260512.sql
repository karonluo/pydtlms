DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM dtlms_recruitment_plans
    WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
  ) THEN
    RAISE EXCEPTION '未找到名称为 2027 夏日学术交流日 的招生计划，无法执行 20260512 计划收口更新';
  END IF;
END $$;

DROP TABLE IF EXISTS tmp_target_recruitment_plan;

CREATE TEMP TABLE tmp_target_recruitment_plan (
  target_plan_id BIGINT PRIMARY KEY
);

INSERT INTO tmp_target_recruitment_plan (target_plan_id)
SELECT id
FROM dtlms_recruitment_plans
WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
ORDER BY CASE WHEN COALESCE(is_deleted, FALSE) THEN 1 ELSE 0 END, id
LIMIT 1;

UPDATE dtlms_recruitment_plans AS plan
SET is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE plan.id = target_plan.target_plan_id
  AND (
    plan.is_deleted IS DISTINCT FROM FALSE
    OR plan.updated_at IS NULL
  );

UPDATE dtlms_recruitment_applications AS application
SET plan_id = target_plan.target_plan_id,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE application.plan_id IS DISTINCT FROM target_plan.target_plan_id;

UPDATE dtlms_portal_students AS student
SET selected_plan_id = target_plan.target_plan_id,
    updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE student.selected_plan_id IS DISTINCT FROM target_plan.target_plan_id;

DELETE FROM dtlms_interview_scores
WHERE schedule_id IN (
  SELECT schedule.id
  FROM dtlms_interview_schedules AS schedule
  JOIN dtlms_interview_groups AS grp ON grp.id = schedule.interview_group_id
  CROSS JOIN tmp_target_recruitment_plan AS target_plan
  WHERE grp.plan_id <> target_plan.target_plan_id
);

DELETE FROM dtlms_interview_schedules
WHERE interview_group_id IN (
  SELECT grp.id
  FROM dtlms_interview_groups AS grp
  CROSS JOIN tmp_target_recruitment_plan AS target_plan
  WHERE grp.plan_id <> target_plan.target_plan_id
);

DELETE FROM dtlms_interview_groups
USING tmp_target_recruitment_plan AS target_plan
WHERE dtlms_interview_groups.plan_id <> target_plan.target_plan_id;

DELETE FROM dtlms_recruitment_plans
USING tmp_target_recruitment_plan AS target_plan
WHERE dtlms_recruitment_plans.id <> target_plan.target_plan_id;