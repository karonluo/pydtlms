-- 20260616 研究中心三表口径收敛
-- 目标：将研究中心主表与关系表切换为基于 dtlms_users 的导师用户模型，去除 dtlms_advisors 依赖。

ALTER TABLE dtlms_teams
    DROP COLUMN IF EXISTS lead_advisor_id;

ALTER TABLE dtlms_teams
    ADD COLUMN IF NOT EXISTS lead_user_id BIGINT;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_dtlms_teams_lead_user_id'
          AND conrelid = 'dtlms_teams'::regclass
    ) THEN
        ALTER TABLE dtlms_teams
            ADD CONSTRAINT fk_dtlms_teams_lead_user_id
            FOREIGN KEY (lead_user_id) REFERENCES dtlms_users(id) NOT VALID;
    END IF;
END
$$;

ALTER TABLE dtlms_team_advisors
    DROP COLUMN IF EXISTS advisor_role;

ALTER TABLE dtlms_team_advisors
    DROP COLUMN IF EXISTS joined_on;

ALTER TABLE dtlms_team_advisors
    DROP COLUMN IF EXISTS left_on;

ALTER TABLE dtlms_team_advisors
    DROP COLUMN IF EXISTS advisor_id;

ALTER TABLE dtlms_team_advisors
    ADD COLUMN IF NOT EXISTS advisor_user_id BIGINT;

UPDATE dtlms_team_advisors
SET advisor_user_id = advisor_user_id
WHERE advisor_user_id IS NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_dtlms_team_advisors_advisor_user_id'
          AND conrelid = 'dtlms_team_advisors'::regclass
    ) THEN
        ALTER TABLE dtlms_team_advisors
            ADD CONSTRAINT fk_dtlms_team_advisors_advisor_user_id
            FOREIGN KEY (advisor_user_id) REFERENCES dtlms_users(id) NOT VALID;
    END IF;
END
$$;

DROP INDEX IF EXISTS idx_dtlms_teams_lead_user_id;
CREATE INDEX IF NOT EXISTS idx_dtlms_teams_lead_user_id
    ON dtlms_teams(lead_user_id)
    WHERE lead_user_id IS NOT NULL;

DROP INDEX IF EXISTS idx_dtlms_team_advisors_team_user;
CREATE INDEX IF NOT EXISTS idx_dtlms_team_advisors_team_user
    ON dtlms_team_advisors(team_id, advisor_user_id)
    WHERE advisor_user_id IS NOT NULL;