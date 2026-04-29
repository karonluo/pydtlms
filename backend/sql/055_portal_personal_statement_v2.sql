ALTER TABLE dtlms_portal_application_personal_statements
    ADD COLUMN IF NOT EXISTS growth_experience_text TEXT,
    ADD COLUMN IF NOT EXISTS program_application_reason_text TEXT,
    ADD COLUMN IF NOT EXISTS career_plan_text TEXT,
    ADD COLUMN IF NOT EXISTS supporting_material_attachment_url TEXT;

UPDATE dtlms_portal_application_personal_statements
SET growth_experience_text = COALESCE(NULLIF(growth_experience_text, ''), NULLIF(personal_statement_text, '')),
    program_application_reason_text = COALESCE(NULLIF(program_application_reason_text, ''), NULLIF(ai_problem_statement, '')),
    career_plan_text = COALESCE(NULLIF(career_plan_text, ''), NULLIF(ai_industry_opinion, '')),
    supporting_material_attachment_url = COALESCE(
        NULLIF(supporting_material_attachment_url, ''),
        (
            SELECT NULLIF(ra.material_list_attachment, '')
            FROM dtlms_recruitment_applications AS ra
            WHERE ra.id = dtlms_portal_application_personal_statements.application_id
        )
    )
WHERE growth_experience_text IS NULL
   OR growth_experience_text = ''
   OR program_application_reason_text IS NULL
   OR program_application_reason_text = ''
   OR career_plan_text IS NULL
   OR career_plan_text = ''
   OR supporting_material_attachment_url IS NULL
   OR supporting_material_attachment_url = '';

UPDATE dtlms_portal_application_personal_statements
SET personal_statement_text = CONCAT_WS(
        E'\n\n',
        CASE WHEN NULLIF(growth_experience_text, '') IS NOT NULL THEN '个人成长经历：' || growth_experience_text END,
        CASE WHEN NULLIF(program_application_reason_text, '') IS NOT NULL THEN '为何申报本项目或本专业：' || program_application_reason_text END,
        CASE WHEN NULLIF(career_plan_text, '') IS NOT NULL THEN '未来职业发展规划：' || career_plan_text END
    )
WHERE COALESCE(NULLIF(personal_statement_text, ''), '') = ''
  AND (
        NULLIF(growth_experience_text, '') IS NOT NULL
        OR NULLIF(program_application_reason_text, '') IS NOT NULL
        OR NULLIF(career_plan_text, '') IS NOT NULL
    );
