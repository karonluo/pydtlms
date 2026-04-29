WITH runtime_teams AS (
    SELECT id, payload
    FROM dtlms_runtime_teams
    WHERE payload IS NOT NULL
), normalized_teams AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'team_code'), '') AS team_code,
        NULLIF(BTRIM(payload ->> 'team_name'), '') AS team_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'department_name'), ''), '未分配院系') AS department_name,
        NULLIF(BTRIM(payload ->> 'discipline_name'), '') AS discipline_name,
        NULLIF(BTRIM(payload ->> 'lead_advisor_name'), '') AS lead_advisor_name,
        CASE
            WHEN jsonb_typeof(payload -> 'research_directions') = 'array' THEN (
                SELECT string_agg(NULLIF(BTRIM(value), ''), '、' ORDER BY ordinality)
                FROM jsonb_array_elements_text(payload -> 'research_directions') WITH ORDINALITY AS directions(value, ordinality)
                WHERE NULLIF(BTRIM(value), '') IS NOT NULL
            )
            ELSE NULLIF(BTRIM(payload ->> 'research_directions'), '')
        END AS research_directions,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '启用')
            WHEN '停用' THEN 'inactive'
            WHEN '筹建' THEN 'planning'
            WHEN '归档' THEN 'archived'
            ELSE 'active'
        END AS team_status,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(payload ->> 'created_on'), '') IS NOT NULL THEN (payload ->> 'created_on')::DATE END,
            CASE WHEN NULLIF(BTRIM(payload ->> 'established_on'), '') IS NOT NULL THEN (payload ->> 'established_on')::DATE END,
            CURRENT_DATE
        ) AS established_on,
        NULLIF(BTRIM(payload ->> 'description'), '') AS description,
        payload
    FROM runtime_teams
    WHERE NULLIF(BTRIM(payload ->> 'team_name'), '') IS NOT NULL
)
INSERT INTO dtlms_teams (
    id, team_code, team_name, department_name, discipline_name, lead_advisor_id,
    research_directions, team_status, established_on, description, is_deleted
)
SELECT
    nt.id,
    COALESCE(nt.team_code, CONCAT('CENTER-', LPAD(nt.id::TEXT, 3, '0'))),
    nt.team_name,
    nt.department_name,
    nt.discipline_name,
    advisor.id,
    nt.research_directions,
    nt.team_status,
    nt.established_on,
    nt.description,
    FALSE
FROM normalized_teams nt
LEFT JOIN dtlms_advisors advisor ON advisor.full_name = nt.lead_advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET team_code = EXCLUDED.team_code,
    team_name = EXCLUDED.team_name,
    department_name = EXCLUDED.department_name,
    discipline_name = EXCLUDED.discipline_name,
    lead_advisor_id = EXCLUDED.lead_advisor_id,
    research_directions = EXCLUDED.research_directions,
    team_status = EXCLUDED.team_status,
    established_on = EXCLUDED.established_on,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

WITH normalized_teams AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'lead_advisor_name'), '') AS lead_advisor_name,
        payload
    FROM dtlms_runtime_teams
    WHERE payload IS NOT NULL
      AND NULLIF(BTRIM(payload ->> 'team_name'), '') IS NOT NULL
), team_advisors_source AS (
    SELECT DISTINCT
        nt.id AS team_id,
        NULLIF(BTRIM(advisor_name), '') AS advisor_name,
        CASE
            WHEN NULLIF(BTRIM(advisor_name), '') = nt.lead_advisor_name THEN 'lead'
            ELSE 'member'
        END AS advisor_role,
        COALESCE(
            CASE WHEN NULLIF(BTRIM(nt.payload ->> 'created_on'), '') IS NOT NULL THEN (nt.payload ->> 'created_on')::DATE END,
            CASE WHEN NULLIF(BTRIM(nt.payload ->> 'established_on'), '') IS NOT NULL THEN (nt.payload ->> 'established_on')::DATE END,
            CURRENT_DATE
        ) AS joined_on
    FROM normalized_teams nt
    CROSS JOIN LATERAL (
        SELECT value AS advisor_name
        FROM jsonb_array_elements_text(
            CASE
                WHEN jsonb_typeof(nt.payload -> 'advisor_names') = 'array' THEN nt.payload -> 'advisor_names'
                ELSE '[]'::jsonb
            END
        )
        UNION ALL
        SELECT nt.lead_advisor_name
        WHERE nt.lead_advisor_name IS NOT NULL
    ) source
    WHERE NULLIF(BTRIM(advisor_name), '') IS NOT NULL
)
INSERT INTO dtlms_team_advisors (team_id, advisor_id, advisor_role, joined_on, left_on, is_deleted)
SELECT
    tas.team_id,
    advisor.id,
    tas.advisor_role,
    tas.joined_on,
    NULL,
    FALSE
FROM team_advisors_source tas
JOIN dtlms_advisors advisor ON advisor.full_name = tas.advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (team_id, advisor_id) DO UPDATE
SET advisor_role = EXCLUDED.advisor_role,
    joined_on = EXCLUDED.joined_on,
    left_on = NULL,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_students AS (
    SELECT id, payload
    FROM dtlms_runtime_students
    WHERE payload IS NOT NULL
), normalized_students AS (
    SELECT
        id,
        NULLIF(BTRIM(payload ->> 'student_no'), '') AS student_no,
        NULLIF(BTRIM(payload ->> 'full_name'), '') AS full_name,
        NULLIF(BTRIM(payload ->> 'political_status'), '') AS political_status,
        NULLIF(BTRIM(payload ->> 'phone_number'), '') AS phone_number,
        CONCAT('ID-', COALESCE(NULLIF(BTRIM(payload ->> 'student_no'), ''), id::TEXT)) AS identity_no,
        COALESCE(NULLIF(BTRIM(payload ->> 'enrollment_year'), ''), '0')::INTEGER AS enrollment_year,
        NULLIF(BTRIM(payload ->> 'degree_type'), '') AS degree_type,
        NULLIF(BTRIM(payload ->> 'team_name'), '') AS team_name,
        NULLIF(BTRIM(payload ->> 'advisor_name'), '') AS advisor_name,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '在校')
            WHEN '外出研修' THEN 'outbound'
            WHEN '学位论文阶段' THEN 'thesis'
            WHEN '实习中' THEN 'internship'
            ELSE 'enrolled'
        END AS current_status
    FROM runtime_students
    WHERE NULLIF(BTRIM(payload ->> 'student_no'), '') IS NOT NULL
      AND NULLIF(BTRIM(payload ->> 'full_name'), '') IS NOT NULL
)
INSERT INTO dtlms_students (
    id, student_no, full_name, gender, political_status, phone_number, identity_no,
    enrollment_year, degree_type, team_id, current_status, primary_advisor_id, is_deleted
)
SELECT
    ns.id,
    ns.student_no,
    ns.full_name,
    '未知',
    ns.political_status,
    ns.phone_number,
    ns.identity_no,
    ns.enrollment_year,
    COALESCE(ns.degree_type, '博士'),
    team.id,
    ns.current_status,
    advisor.id,
    FALSE
FROM normalized_students ns
LEFT JOIN dtlms_teams team ON team.team_name = ns.team_name AND team.is_deleted = FALSE
LEFT JOIN dtlms_advisors advisor ON advisor.full_name = ns.advisor_name AND advisor.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET student_no = EXCLUDED.student_no,
    full_name = EXCLUDED.full_name,
    political_status = EXCLUDED.political_status,
    phone_number = EXCLUDED.phone_number,
    identity_no = EXCLUDED.identity_no,
    enrollment_year = EXCLUDED.enrollment_year,
    degree_type = EXCLUDED.degree_type,
    team_id = EXCLUDED.team_id,
    current_status = EXCLUDED.current_status,
    primary_advisor_id = EXCLUDED.primary_advisor_id,
    updated_at = CURRENT_TIMESTAMP,
    is_deleted = FALSE;

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
    '初始化迁移自 dtlms_runtime_students'
FROM dtlms_students s
WHERE s.is_deleted = FALSE
  AND s.team_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM dtlms_student_team_history h
      WHERE h.student_id = s.id
        AND h.team_id = s.team_id
  );