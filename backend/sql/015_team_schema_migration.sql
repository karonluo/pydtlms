CREATE TABLE IF NOT EXISTS dtlms_teams (
    id BIGSERIAL PRIMARY KEY,
    team_code VARCHAR(32) NOT NULL UNIQUE,
    team_name VARCHAR(128) NOT NULL UNIQUE,
    department_name VARCHAR(128) NOT NULL DEFAULT '未分配院系',
    discipline_name VARCHAR(128),
    lead_advisor_id BIGINT REFERENCES dtlms_advisors(id),
    research_directions TEXT,
    team_status VARCHAR(32) NOT NULL DEFAULT 'active',
    established_on DATE,
    description TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (team_status IN ('active', 'inactive', 'planning', 'archived'))
);

CREATE TABLE IF NOT EXISTS dtlms_team_advisors (
    id BIGSERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL REFERENCES dtlms_teams(id),
    advisor_id BIGINT NOT NULL REFERENCES dtlms_advisors(id),
    advisor_role VARCHAR(32) NOT NULL DEFAULT 'member',
    joined_on DATE,
    left_on DATE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (team_id, advisor_id),
    CHECK (advisor_role IN ('lead', 'member', 'co_advisor')),
    CHECK (left_on IS NULL OR joined_on IS NULL OR left_on >= joined_on)
);

ALTER TABLE dtlms_students
    ADD COLUMN IF NOT EXISTS team_id BIGINT REFERENCES dtlms_teams(id);

CREATE TABLE IF NOT EXISTS dtlms_student_team_history (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES dtlms_students(id),
    team_id BIGINT NOT NULL REFERENCES dtlms_teams(id),
    start_date DATE NOT NULL,
    end_date DATE,
    change_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date IS NULL OR end_date >= start_date)
);

WITH distinct_team_names AS (
    SELECT DISTINCT BTRIM(s.team_name) AS team_name
    FROM dtlms_students AS s
    WHERE s.team_name IS NOT NULL
      AND BTRIM(s.team_name) <> ''
), missing_team_names AS (
    SELECT d.team_name
    FROM distinct_team_names AS d
    WHERE NOT EXISTS (
        SELECT 1
        FROM dtlms_teams AS t
        WHERE t.team_name = d.team_name
    )
)
INSERT INTO dtlms_teams (
    team_code,
    team_name,
    department_name,
    team_status,
    description
)
SELECT
    CONCAT('TEAM-', LPAD(ROW_NUMBER() OVER (ORDER BY m.team_name)::TEXT, 4, '0')),
    m.team_name,
    '未分配院系',
    'active',
    '由学生主档历史 team_name 迁移生成'
FROM missing_team_names AS m;

UPDATE dtlms_students AS s
SET team_id = t.id
FROM dtlms_teams AS t
WHERE s.team_id IS NULL
  AND s.team_name IS NOT NULL
  AND BTRIM(s.team_name) <> ''
  AND t.team_name = s.team_name;

INSERT INTO dtlms_student_team_history (
    student_id,
    team_id,
    start_date,
    change_reason
)
SELECT
    s.id,
    s.team_id,
    CURRENT_DATE,
    '初始化迁移自 dtlms_students.team_name'
FROM dtlms_students AS s
WHERE s.team_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_student_team_history AS h
      WHERE h.student_id = s.id
                AND h.team_id = s.team_id
  );