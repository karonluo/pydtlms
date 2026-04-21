ALTER TABLE IF EXISTS dtlms_recruitment_plans
    ADD COLUMN IF NOT EXISTS plan_description TEXT;