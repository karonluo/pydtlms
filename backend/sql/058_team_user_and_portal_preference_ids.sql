ALTER TABLE IF EXISTS dtlms_advisors
  ADD COLUMN IF NOT EXISTS user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_teams
  ADD COLUMN IF NOT EXISTS lead_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_team_advisors
  ADD COLUMN IF NOT EXISTS advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_portal_students
  ADD COLUMN IF NOT EXISTS selected_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS selected_advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_recruitment_applications
  ADD COLUMN IF NOT EXISTS first_choice_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS second_choice_team_id BIGINT,
  ADD COLUMN IF NOT EXISTS intended_advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_portal_application_preferences
  ADD COLUMN IF NOT EXISTS team_id BIGINT,
  ADD COLUMN IF NOT EXISTS advisor_user_id BIGINT;

ALTER TABLE IF EXISTS dtlms_students
  ADD COLUMN IF NOT EXISTS portal_student_id BIGINT;

DO $$
BEGIN
  IF to_regclass('public.dtlms_advisors') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_advisors_user_id'
       AND conrelid = 'dtlms_advisors'::regclass
     ) THEN
    ALTER TABLE dtlms_advisors
      ADD CONSTRAINT fk_dtlms_advisors_user_id
      FOREIGN KEY (user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_teams') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_teams_lead_user_id'
       AND conrelid = 'dtlms_teams'::regclass
     ) THEN
    ALTER TABLE dtlms_teams
      ADD CONSTRAINT fk_dtlms_teams_lead_user_id
      FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_team_advisors') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_team_advisors_advisor_user_id'
       AND conrelid = 'dtlms_team_advisors'::regclass
     ) THEN
    ALTER TABLE dtlms_team_advisors
      ADD CONSTRAINT fk_dtlms_team_advisors_advisor_user_id
      FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_students_selected_team_id'
       AND conrelid = 'dtlms_portal_students'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_students
      ADD CONSTRAINT fk_dtlms_portal_students_selected_team_id
      FOREIGN KEY (selected_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_students_selected_advisor_user_id'
       AND conrelid = 'dtlms_portal_students'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_students
      ADD CONSTRAINT fk_dtlms_portal_students_selected_advisor_user_id
      FOREIGN KEY (selected_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_first_choice_team_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_first_choice_team_id
      FOREIGN KEY (first_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_second_choice_team_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_second_choice_team_id
      FOREIGN KEY (second_choice_team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_recruitment_applications_intended_advisor_user_id'
       AND conrelid = 'dtlms_recruitment_applications'::regclass
     ) THEN
    ALTER TABLE dtlms_recruitment_applications
      ADD CONSTRAINT fk_dtlms_recruitment_applications_intended_advisor_user_id
      FOREIGN KEY (intended_advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_application_preferences') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_application_preferences_team_id'
       AND conrelid = 'dtlms_portal_application_preferences'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_application_preferences
      ADD CONSTRAINT fk_dtlms_portal_application_preferences_team_id
      FOREIGN KEY (team_id) REFERENCES dtlms_teams(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_portal_application_preferences') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_portal_application_preferences_advisor_user_id'
       AND conrelid = 'dtlms_portal_application_preferences'::regclass
     ) THEN
    ALTER TABLE dtlms_portal_application_preferences
      ADD CONSTRAINT fk_dtlms_portal_application_preferences_advisor_user_id
      FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
  END IF;

  IF to_regclass('public.dtlms_students') IS NOT NULL
     AND NOT EXISTS (
       SELECT 1
       FROM pg_constraint
       WHERE conname = 'fk_dtlms_students_portal_student_id'
       AND conrelid = 'dtlms_students'::regclass
     ) THEN
    ALTER TABLE dtlms_students
      ADD CONSTRAINT fk_dtlms_students_portal_student_id
      FOREIGN KEY (portal_student_id) REFERENCES dtlms_portal_students(id) NOT VALID;
  END IF;
END $$;

WITH portal_student_candidates AS (
    SELECT
        s.id AS student_id,
        ps.id AS portal_student_id,
        ROW_NUMBER() OVER (PARTITION BY s.id ORDER BY ps.id DESC) AS student_pick,
        ROW_NUMBER() OVER (PARTITION BY ps.id ORDER BY s.id DESC) AS portal_pick
    FROM dtlms_students AS s
    JOIN dtlms_portal_students AS ps
      ON (
        BTRIM(COALESCE(s.full_name, '')) <> ''
        AND BTRIM(COALESCE(s.full_name, '')) = BTRIM(COALESCE(ps.full_name, ''))
        AND BTRIM(COALESCE(s.phone_number, '')) <> ''
        AND BTRIM(COALESCE(s.phone_number, '')) = BTRIM(COALESCE(ps.phone_number, ''))
      )
    WHERE s.portal_student_id IS NULL
      AND COALESCE(s.is_deleted, FALSE) = FALSE
), portal_student_matches AS (
    SELECT student_id, portal_student_id
    FROM portal_student_candidates
    WHERE student_pick = 1 AND portal_pick = 1
)
UPDATE dtlms_students AS s
SET portal_student_id = m.portal_student_id,
    updated_at = CURRENT_TIMESTAMP
FROM portal_student_matches AS m
WHERE s.id = m.student_id
  AND s.portal_student_id IS DISTINCT FROM m.portal_student_id;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_advisors_user_id
    ON dtlms_advisors(user_id)
    WHERE user_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_team_advisors_team_user
    ON dtlms_team_advisors(team_id, advisor_user_id)
    WHERE advisor_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_teams_lead_user_id
    ON dtlms_teams(lead_user_id)
    WHERE lead_user_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_portal_students_selected_team_id
    ON dtlms_portal_students(selected_team_id)
    WHERE selected_team_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_recruitment_applications_first_choice_team_id
    ON dtlms_recruitment_applications(first_choice_team_id)
    WHERE first_choice_team_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_dtlms_portal_application_preferences_team_id
    ON dtlms_portal_application_preferences(team_id)
    WHERE team_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_dtlms_students_portal_student_id
  ON dtlms_students(portal_student_id)
  WHERE portal_student_id IS NOT NULL;

WITH advisor_role_users AS (
    SELECT
        u.id AS user_id,
        u.full_name,
        ROW_NUMBER() OVER (PARTITION BY u.full_name ORDER BY u.id) AS row_num,
        COUNT(*) OVER (PARTITION BY u.full_name) AS same_name_count
    FROM dtlms_users u
    JOIN dtlms_user_roles ur ON ur.user_id = u.id
    JOIN dtlms_roles r ON r.id = ur.role_id
    WHERE u.is_deleted = FALSE
      AND u.is_active = TRUE
      AND r.is_deleted = FALSE
      AND r.role_code = 'advisor'
), unique_advisor_role_users AS (
    SELECT user_id, full_name
    FROM advisor_role_users
    WHERE row_num = 1 AND same_name_count = 1
)
UPDATE dtlms_advisors AS advisor
SET user_id = mapping.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM unique_advisor_role_users AS mapping
WHERE advisor.is_deleted = FALSE
  AND advisor.user_id IS NULL
  AND advisor.full_name = mapping.full_name;

UPDATE dtlms_teams AS team
SET lead_user_id = advisor.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_advisors AS advisor
WHERE team.is_deleted = FALSE
  AND team.lead_advisor_id = advisor.id
  AND advisor.user_id IS NOT NULL
  AND team.lead_user_id IS DISTINCT FROM advisor.user_id;

UPDATE dtlms_team_advisors AS relation
SET advisor_user_id = advisor.user_id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_advisors AS advisor
WHERE relation.advisor_id = advisor.id
  AND advisor.user_id IS NOT NULL
  AND relation.advisor_user_id IS DISTINCT FROM advisor.user_id;

UPDATE dtlms_portal_students AS student
SET selected_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(student.selected_team_name, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(student.selected_team_name)
  AND student.selected_team_id IS DISTINCT FROM team.id;

WITH portal_student_advisor_choice AS (
    SELECT DISTINCT ON (student.id)
        student.id AS portal_student_id,
        relation.advisor_user_id
    FROM dtlms_portal_students AS student
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = student.selected_team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE student.selected_team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(student.selected_advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(student.selected_advisor_name)
    ORDER BY student.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_portal_students AS student
SET selected_advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM portal_student_advisor_choice AS choice
WHERE student.id = choice.portal_student_id
  AND student.selected_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

UPDATE dtlms_recruitment_applications AS application
SET first_choice_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(application.first_choice, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(application.first_choice)
  AND application.first_choice_team_id IS DISTINCT FROM team.id;

UPDATE dtlms_recruitment_applications AS application
SET second_choice_team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(application.second_choice, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(application.second_choice)
  AND application.second_choice_team_id IS DISTINCT FROM team.id;

WITH application_advisor_choice AS (
    SELECT DISTINCT ON (application.id)
        application.id AS application_id,
        relation.advisor_user_id
    FROM dtlms_recruitment_applications AS application
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = application.first_choice_team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE application.first_choice_team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(application.intended_advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(application.intended_advisor_name)
    ORDER BY application.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_recruitment_applications AS application
SET intended_advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM application_advisor_choice AS choice
WHERE application.id = choice.application_id
  AND application.intended_advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

UPDATE dtlms_portal_application_preferences AS preference
SET team_id = team.id,
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_teams AS team
WHERE team.is_deleted = FALSE
  AND NULLIF(BTRIM(COALESCE(preference.research_center_name, '')), '') IS NOT NULL
  AND team.team_name = BTRIM(preference.research_center_name)
  AND preference.team_id IS DISTINCT FROM team.id;

WITH preference_advisor_choice AS (
    SELECT DISTINCT ON (preference.id)
        preference.id AS preference_id,
        relation.advisor_user_id
    FROM dtlms_portal_application_preferences AS preference
    JOIN dtlms_team_advisors AS relation
        ON relation.team_id = preference.team_id
       AND relation.is_deleted = FALSE
    JOIN dtlms_advisors AS advisor
        ON advisor.id = relation.advisor_id
       AND advisor.is_deleted = FALSE
    WHERE preference.team_id IS NOT NULL
      AND relation.advisor_user_id IS NOT NULL
      AND NULLIF(BTRIM(COALESCE(preference.advisor_name, '')), '') IS NOT NULL
      AND advisor.full_name = BTRIM(preference.advisor_name)
    ORDER BY preference.id, CASE WHEN relation.advisor_role = 'lead' THEN 0 ELSE 1 END, relation.id
)
UPDATE dtlms_portal_application_preferences AS preference
SET advisor_user_id = choice.advisor_user_id,
    updated_at = CURRENT_TIMESTAMP
FROM preference_advisor_choice AS choice
WHERE preference.id = choice.preference_id
  AND preference.advisor_user_id IS DISTINCT FROM choice.advisor_user_id;

DROP TABLE IF EXISTS tmp_recruitment_application_number_mapping;

CREATE TEMP TABLE tmp_recruitment_application_number_mapping (
  application_id BIGINT PRIMARY KEY,
  old_workflow_key TEXT,
  new_business_key TEXT NOT NULL
) ON COMMIT DROP;

INSERT INTO tmp_recruitment_application_number_mapping (application_id, old_workflow_key, new_business_key)
WITH application_key_basis AS (
  SELECT
    application.id AS application_id,
    COALESCE(application.applied_at, application.created_at, CURRENT_TIMESTAMP) AS sort_at,
    TO_CHAR(COALESCE(application.applied_at, application.created_at, CURRENT_TIMESTAMP), 'YYYY') AS business_year,
    CASE
      WHEN BTRIM(COALESCE(application.business_key, '')) ~ '^SH[0-9]{8}$' THEN BTRIM(application.business_key)
      WHEN BTRIM(COALESCE(application.candidate_no, '')) ~ '^SH[0-9]{8}$' THEN BTRIM(application.candidate_no)
      ELSE NULL
    END AS preserved_business_key,
    COALESCE(
      NULLIF(BTRIM(COALESCE(application.business_key, '')), ''),
      NULLIF(BTRIM(COALESCE(application.candidate_no, '')), '')
    ) AS old_workflow_key,
    BTRIM(COALESCE(application.business_key, '')) AS current_business_key,
    BTRIM(COALESCE(application.candidate_no, '')) AS current_candidate_no
  FROM dtlms_recruitment_applications AS application
  WHERE application.is_deleted = FALSE
), existing_year_sequences AS (
  SELECT
    business_year,
    MAX(SUBSTRING(preserved_business_key FROM 7 FOR 4)::INTEGER) AS max_sequence
  FROM application_key_basis
  WHERE preserved_business_key IS NOT NULL
  GROUP BY business_year
), generated_business_keys AS (
  SELECT
    basis.application_id,
    'SH' || basis.business_year || LPAD(
      (
        COALESCE(existing_year_sequences.max_sequence, 0)
        + ROW_NUMBER() OVER (PARTITION BY basis.business_year ORDER BY basis.sort_at, basis.application_id)
      )::TEXT,
      4,
      '0'
    ) AS new_business_key
  FROM application_key_basis AS basis
  LEFT JOIN existing_year_sequences
    ON existing_year_sequences.business_year = basis.business_year
  WHERE basis.preserved_business_key IS NULL
), normalized_business_keys AS (
  SELECT
    basis.application_id,
    basis.old_workflow_key,
    COALESCE(basis.preserved_business_key, generated.new_business_key) AS new_business_key,
    basis.current_business_key,
    basis.current_candidate_no
  FROM application_key_basis AS basis
  LEFT JOIN generated_business_keys AS generated
    ON generated.application_id = basis.application_id
)
SELECT
  normalized.application_id,
  normalized.old_workflow_key,
  normalized.new_business_key
FROM normalized_business_keys AS normalized
WHERE normalized.new_business_key IS NOT NULL
  AND (
    normalized.current_business_key IS DISTINCT FROM normalized.new_business_key
    OR normalized.current_candidate_no IS DISTINCT FROM normalized.new_business_key
  );

UPDATE dtlms_recruitment_applications AS application
SET business_key = mapping.new_business_key,
  candidate_no = mapping.new_business_key,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE application.id = mapping.application_id
  AND (
    application.business_key IS DISTINCT FROM mapping.new_business_key
    OR application.candidate_no IS DISTINCT FROM mapping.new_business_key
  );

DO $$
BEGIN
  IF to_regclass('public.dtlms_runtime_recruitment_applications') IS NOT NULL THEN
    UPDATE dtlms_runtime_recruitment_applications AS runtime_application
    SET payload = jsonb_set(
        jsonb_set(
          COALESCE(runtime_application.payload, '{}'::jsonb),
          '{business_key}',
          to_jsonb(mapping.new_business_key::TEXT),
          TRUE
        ),
        '{candidate_no}',
        to_jsonb(mapping.new_business_key::TEXT),
        TRUE
      ),
      updated_at = CURRENT_TIMESTAMP
    FROM tmp_recruitment_application_number_mapping AS mapping
    WHERE runtime_application.id = mapping.application_id
      AND (
        COALESCE(runtime_application.payload ->> 'business_key', '') IS DISTINCT FROM mapping.new_business_key
        OR COALESCE(runtime_application.payload ->> 'candidate_no', '') IS DISTINCT FROM mapping.new_business_key
      );
  END IF;
END $$;

DO $$
BEGIN
  IF to_regclass('public.dtlms_runtime_workflow_tasks') IS NOT NULL THEN
    UPDATE dtlms_runtime_workflow_tasks AS runtime_task
    SET payload = jsonb_set(
        jsonb_set(
          COALESCE(runtime_task.payload, '{}'::jsonb),
          '{business_key}',
          to_jsonb(mapping.new_business_key::TEXT),
          TRUE
        ),
        '{form_summary}',
        to_jsonb(
          regexp_replace(
            COALESCE(runtime_task.payload ->> 'form_summary', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      ),
      updated_at = CURRENT_TIMESTAMP
    FROM tmp_recruitment_application_number_mapping AS mapping
    WHERE (
        COALESCE(runtime_task.payload ->> 'flow_code', '') = 'recruitment_application'
        OR COALESCE(runtime_task.payload ->> 'business_dataset', '') = 'recruitment_applications'
      )
      AND (
        COALESCE(runtime_task.payload ->> 'entity_id', '') = mapping.application_id::TEXT
        OR (
          mapping.old_workflow_key IS NOT NULL
          AND COALESCE(runtime_task.payload ->> 'business_key', '') = mapping.old_workflow_key
        )
      )
      AND (
        COALESCE(runtime_task.payload ->> 'business_key', '') IS DISTINCT FROM mapping.new_business_key
        OR COALESCE(runtime_task.payload ->> 'form_summary', '') LIKE '业务编号：%'
      );
  END IF;
END $$;

UPDATE dtlms_wf_hi_procinst AS procinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND procinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_hi_taskinst AS taskinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND taskinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_hi_actinst AS actinst
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND actinst.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_ru_execution AS execution
SET business_key_ = mapping.new_business_key
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND execution.business_key_ = mapping.old_workflow_key;

UPDATE dtlms_wf_ru_task AS runtime_task
SET business_key_ = mapping.new_business_key,
  form_key_ = CASE
    WHEN runtime_task.form_key_ = mapping.old_workflow_key THEN mapping.new_business_key
    ELSE runtime_task.form_key_
  END,
  description_ = CASE
    WHEN COALESCE(runtime_task.description_, '') LIKE '业务编号：%'
      THEN regexp_replace(runtime_task.description_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE runtime_task.description_
  END
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    runtime_task.business_key_ = mapping.old_workflow_key
    OR runtime_task.form_key_ = mapping.old_workflow_key
  );

UPDATE dtlms_wf_ru_variable AS runtime_variable
SET text_value_ = CASE
    WHEN runtime_variable.name_ = 'businessKey' THEN mapping.new_business_key
    WHEN runtime_variable.name_ = 'formSummary' AND COALESCE(runtime_variable.text_value_, '') LIKE '业务编号：%'
      THEN regexp_replace(runtime_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE runtime_variable.text_value_
  END,
  json_value_ = CASE
    WHEN runtime_variable.name_ = 'businessKey'
      THEN jsonb_set(COALESCE(runtime_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
    WHEN runtime_variable.name_ = 'formSummary'
      THEN jsonb_set(
        COALESCE(runtime_variable.json_value_, '{}'::jsonb),
        '{value}',
        to_jsonb(
          regexp_replace(
            COALESCE(runtime_variable.json_value_ ->> 'value', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      )
    ELSE runtime_variable.json_value_
  END
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    (runtime_variable.name_ = 'businessKey' AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
    OR (
      runtime_variable.name_ = 'formSummary'
      AND COALESCE(runtime_variable.text_value_, runtime_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
    )
  );

UPDATE dtlms_wf_hi_varinst AS history_variable
SET text_value_ = CASE
    WHEN history_variable.name_ = 'businessKey' THEN mapping.new_business_key
    WHEN history_variable.name_ = 'formSummary' AND COALESCE(history_variable.text_value_, '') LIKE '业务编号：%'
      THEN regexp_replace(history_variable.text_value_, '^业务编号：[^；]*；', '业务编号：' || mapping.new_business_key || '；')
    ELSE history_variable.text_value_
  END,
  json_value_ = CASE
    WHEN history_variable.name_ = 'businessKey'
      THEN jsonb_set(COALESCE(history_variable.json_value_, '{}'::jsonb), '{value}', to_jsonb(mapping.new_business_key::TEXT), TRUE)
    WHEN history_variable.name_ = 'formSummary'
      THEN jsonb_set(
        COALESCE(history_variable.json_value_, '{}'::jsonb),
        '{value}',
        to_jsonb(
          regexp_replace(
            COALESCE(history_variable.json_value_ ->> 'value', ''),
            '^业务编号：[^；]*；',
            '业务编号：' || mapping.new_business_key || '；'
          )::TEXT
        ),
        TRUE
      )
    ELSE history_variable.json_value_
  END,
  last_updated_time_ = CURRENT_TIMESTAMP
FROM tmp_recruitment_application_number_mapping AS mapping
WHERE mapping.old_workflow_key IS NOT NULL
  AND mapping.old_workflow_key IS DISTINCT FROM mapping.new_business_key
  AND (
    (history_variable.name_ = 'businessKey' AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') = mapping.old_workflow_key)
    OR (
      history_variable.name_ = 'formSummary'
      AND COALESCE(history_variable.text_value_, history_variable.json_value_ ->> 'value', '') LIKE '业务编号：' || mapping.old_workflow_key || '；%'
    )
  );

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM dtlms_recruitment_plans
    WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
  ) THEN
    RAISE EXCEPTION '未找到名称为 2027 夏日学术交流日 的招生计划，无法执行 058 中的计划收口更新';
  END IF;
END $$;

DROP TABLE IF EXISTS tmp_target_recruitment_plan;

CREATE TEMP TABLE tmp_target_recruitment_plan (
  target_plan_id BIGINT PRIMARY KEY
) ON COMMIT DROP;

INSERT INTO tmp_target_recruitment_plan (target_plan_id)
SELECT id
FROM dtlms_recruitment_plans
WHERE BTRIM(plan_name) = '2027 夏日学术交流日'
ORDER BY CASE WHEN is_deleted THEN 1 ELSE 0 END, id
LIMIT 1;

UPDATE dtlms_recruitment_plans AS plan
SET is_deleted = FALSE,
  updated_at = CURRENT_TIMESTAMP
FROM tmp_target_recruitment_plan AS target_plan
WHERE plan.id = target_plan.target_plan_id
  AND plan.is_deleted IS DISTINCT FROM FALSE;

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

UPDATE dtlms_portal_students
SET application_draft = NULL,
    updated_at = CURRENT_TIMESTAMP
WHERE application_draft IS NOT NULL;

DROP TABLE IF EXISTS tmp_liaodiao_portal_students;

CREATE TEMP TABLE tmp_liaodiao_portal_students (
  portal_student_id BIGINT PRIMARY KEY
) ON COMMIT DROP;

INSERT INTO tmp_liaodiao_portal_students (portal_student_id)
SELECT ps.id
FROM dtlms_portal_students AS ps
WHERE BTRIM(COALESCE(ps.full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
  OR LOWER(BTRIM(COALESCE(ps.email, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(ps.email, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(ps.phone_number, '')) IN ('13800009999', '13800009998')
   OR UPPER(BTRIM(COALESCE(ps.id_number, ''))) IN ('32000019990101123X', '32000019990101124X');

DROP TABLE IF EXISTS tmp_liaodiao_recruitment_applications;

CREATE TEMP TABLE tmp_liaodiao_recruitment_applications (
  application_id BIGINT PRIMARY KEY,
  business_key TEXT,
  candidate_no TEXT
) ON COMMIT DROP;

INSERT INTO tmp_liaodiao_recruitment_applications (application_id, business_key, candidate_no)
SELECT ra.id, ra.business_key, ra.candidate_no
FROM dtlms_recruitment_applications AS ra
LEFT JOIN tmp_liaodiao_portal_students AS ps
  ON ps.portal_student_id = ra.portal_student_id
WHERE ps.portal_student_id IS NOT NULL
  OR BTRIM(COALESCE(ra.student_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
  OR LOWER(BTRIM(COALESCE(ra.email, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(ra.email, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(ra.phone_number, '')) IN ('13800009999', '13800009998')
   OR UPPER(BTRIM(COALESCE(ra.id_number, ''))) IN ('32000019990101123X', '32000019990101124X');

DROP TABLE IF EXISTS tmp_liaodiao_workflow_keys;

CREATE TEMP TABLE tmp_liaodiao_workflow_keys (
  business_key TEXT PRIMARY KEY
) ON COMMIT DROP;

INSERT INTO tmp_liaodiao_workflow_keys (business_key)
SELECT DISTINCT key_value
FROM (
  SELECT NULLIF(BTRIM(COALESCE(application.business_key, '')), '') AS key_value
  FROM tmp_liaodiao_recruitment_applications AS application
  UNION ALL
  SELECT NULLIF(BTRIM(COALESCE(application.candidate_no, '')), '') AS key_value
  FROM tmp_liaodiao_recruitment_applications AS application
) AS keys
WHERE key_value IS NOT NULL;

DROP TABLE IF EXISTS tmp_liaodiao_procinst;

CREATE TEMP TABLE tmp_liaodiao_procinst (
  proc_inst_id TEXT PRIMARY KEY
) ON COMMIT DROP;

INSERT INTO tmp_liaodiao_procinst (proc_inst_id)
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_hi_procinst
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_ru_execution
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_hi_taskinst
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys)
UNION
SELECT DISTINCT proc_inst_id_
FROM dtlms_wf_ru_task
WHERE business_key_ IN (SELECT business_key FROM tmp_liaodiao_workflow_keys);

DELETE FROM dtlms_interview_scores
WHERE schedule_id IN (
  SELECT schedule.id
  FROM dtlms_interview_schedules AS schedule
  WHERE schedule.application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
);

DELETE FROM dtlms_material_scores
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
   OR reviewer_assignment_id IN (
     SELECT assignment.id
     FROM dtlms_reviewer_assignments AS assignment
     WHERE assignment.application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications)
   );

DELETE FROM dtlms_written_exam_scores
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_admission_decisions
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_interview_schedules
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_qualification_reviews
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_application_materials
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_reviewer_assignments
WHERE application_id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_wf_ru_identitylink
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst)
   OR task_id_ IN (
     SELECT id_ FROM dtlms_wf_ru_task WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst)
   );

DELETE FROM dtlms_wf_ru_variable
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_varinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_actinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_taskinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_hi_procinst
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_ru_task
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_wf_ru_execution
WHERE proc_inst_id_ IN (SELECT proc_inst_id FROM tmp_liaodiao_procinst);

DELETE FROM dtlms_recruitment_applications
WHERE id IN (SELECT application_id FROM tmp_liaodiao_recruitment_applications);

DELETE FROM dtlms_portal_students
WHERE id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students);

DELETE FROM dtlms_student_team_history
WHERE student_id IN (
  SELECT id
  FROM dtlms_students
  WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
     OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
);

DELETE FROM dtlms_student_advisor_history
WHERE student_id IN (
  SELECT id
  FROM dtlms_students
  WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
     OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生')
);

DELETE FROM dtlms_students
WHERE portal_student_id IN (SELECT portal_student_id FROM tmp_liaodiao_portal_students)
   OR BTRIM(COALESCE(full_name, '')) IN ('联调考生', '邮件联调考生', '驳回联调考生');

DELETE FROM dtlms_login_logs
WHERE LOWER(BTRIM(COALESCE(username, ''))) LIKE '%@example.com'
  OR LOWER(BTRIM(COALESCE(username, ''))) LIKE '%@mail.example.com'
   OR BTRIM(COALESCE(username, '')) IN (
     '13800009999',
     '13800009998'
   );

DELETE FROM dtlms_operation_logs
WHERE entity_id IN (
    SELECT application_id::TEXT FROM tmp_liaodiao_recruitment_applications
    UNION
    SELECT portal_student_id::TEXT FROM tmp_liaodiao_portal_students
  )
   OR COALESCE(new_value ->> 'summary', '') LIKE '%联调考生%';

WITH latest_portal_application_status AS (
    SELECT DISTINCT ON (ra.portal_student_id)
        ra.portal_student_id,
        BTRIM(COALESCE(ra.application_status, '')) AS application_status
    FROM dtlms_recruitment_applications AS ra
    WHERE ra.portal_student_id IS NOT NULL
      AND COALESCE(ra.is_deleted, FALSE) = FALSE
    ORDER BY ra.portal_student_id, COALESCE(ra.applied_at, ra.updated_at, ra.created_at) DESC, ra.id DESC
)
UPDATE dtlms_portal_students AS ps
SET submitted_at = NULL,
    application_draft = CASE
        WHEN ps.application_draft IS NULL THEN NULL
        WHEN jsonb_typeof(ps.application_draft) = 'object'
            THEN jsonb_set(ps.application_draft, '{submitted_at}', 'null'::jsonb, TRUE)
        ELSE ps.application_draft
    END,
    updated_at = CURRENT_TIMESTAMP
FROM latest_portal_application_status AS latest
WHERE ps.id = latest.portal_student_id
  AND latest.application_status IN ('returned', 'rejected', '驳回重填', '不录取')
  AND ps.submitted_at IS NOT NULL;

-- runtime 历史表在生产补丁尾部统一物理删除；此前的业务修复语句已完成对 runtime 数据的最后一次读取/改写。
DROP TABLE IF EXISTS dtlms_runtime_portal_students;
DROP TABLE IF EXISTS dtlms_runtime_workflow_tasks;
DROP TABLE IF EXISTS dtlms_runtime_sync_logs;
DROP TABLE IF EXISTS dtlms_runtime_operation_logs;
DROP TABLE IF EXISTS dtlms_runtime_integrations;
DROP TABLE IF EXISTS dtlms_runtime_audit_policies;
DROP TABLE IF EXISTS dtlms_runtime_system_users;
DROP TABLE IF EXISTS dtlms_runtime_roles;
DROP TABLE IF EXISTS dtlms_runtime_thesis_reviews;
DROP TABLE IF EXISTS dtlms_runtime_theses;
DROP TABLE IF EXISTS dtlms_runtime_outbound_studies;
DROP TABLE IF EXISTS dtlms_runtime_scientific_reports;
DROP TABLE IF EXISTS dtlms_runtime_training_plans;
DROP TABLE IF EXISTS dtlms_runtime_recruitment_applications;
DROP TABLE IF EXISTS dtlms_runtime_recruitment_plans;
DROP TABLE IF EXISTS dtlms_runtime_students;
DROP TABLE IF EXISTS dtlms_runtime_teams;
DROP TABLE IF EXISTS dtlms_runtime_profiles;
DROP TABLE IF EXISTS dtlms_runtime_counters;