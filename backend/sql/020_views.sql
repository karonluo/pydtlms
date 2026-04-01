CREATE OR REPLACE VIEW dtlms_v_student_lifecycle_snapshot AS
WITH latest_report AS (
    SELECT DISTINCT ON (student_id)
        student_id,
        period_label,
        report_status,
        review_score,
        updated_at
    FROM dtlms_scientific_reports
    WHERE is_deleted = FALSE
    ORDER BY student_id, updated_at DESC
), latest_admission AS (
    SELECT DISTINCT ON (application_id)
        application_id,
        decision_status,
        final_score,
        updated_at
    FROM dtlms_admission_decisions
    ORDER BY application_id, updated_at DESC
)
SELECT
    s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    s.degree_type,
    s.team_name,
    a.full_name AS primary_advisor_name,
    tp.version_no AS training_plan_version,
    tp.plan_status,
    lr.period_label AS latest_report_period,
    lr.report_status AS latest_report_status,
    lr.review_score AS latest_report_score,
    t.title AS thesis_title,
    t.thesis_status,
    t.blind_review_status,
    t.degree_granted
FROM dtlms_students s
LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
LEFT JOIN LATERAL (
    SELECT version_no, plan_status
    FROM dtlms_training_plans
    WHERE student_id = s.id AND is_deleted = FALSE
    ORDER BY updated_at DESC
    LIMIT 1
) tp ON TRUE
LEFT JOIN latest_report lr ON lr.student_id = s.id
LEFT JOIN LATERAL (
    SELECT title, thesis_status, blind_review_status, degree_granted
    FROM dtlms_theses
    WHERE student_id = s.id AND is_deleted = FALSE
    ORDER BY updated_at DESC
    LIMIT 1
) t ON TRUE
WHERE s.is_deleted = FALSE;

CREATE OR REPLACE VIEW dtlms_v_recruitment_dashboard AS
SELECT
    rp.id AS plan_id,
    rp.plan_code,
    rp.plan_name,
    rp.academic_year,
    rp.semester,
    rp.plan_status,
    COUNT(DISTINCT ra.id) AS application_total,
    COUNT(DISTINCT CASE WHEN ra.application_status = 'qualified' THEN ra.id END) AS qualified_total,
    COUNT(DISTINCT CASE WHEN ra.application_status = 'interviewing' THEN ra.id END) AS interviewing_total,
    COUNT(DISTINCT CASE WHEN ad.decision_status IN ('pre_admitted', 'accepted') THEN ad.id END) AS admitted_total,
    AVG(ms.material_score) AS avg_material_score
FROM dtlms_recruitment_plans rp
LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id AND ra.is_deleted = FALSE
LEFT JOIN dtlms_material_scores ms ON ms.application_id = ra.id
LEFT JOIN dtlms_admission_decisions ad ON ad.application_id = ra.id
WHERE rp.is_deleted = FALSE
GROUP BY rp.id, rp.plan_code, rp.plan_name, rp.academic_year, rp.semester, rp.plan_status;

CREATE OR REPLACE VIEW dtlms_v_training_compliance AS
SELECT
    s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    a.full_name AS advisor_name,
    tp.plan_status,
    tp.report_cycle,
    COUNT(sr.id) FILTER (WHERE sr.report_status IN ('submitted', 'reviewed')) AS submitted_report_count,
    COUNT(sr.id) FILTER (WHERE sr.report_status = 'pending') AS pending_report_count,
    COUNT(os.id) FILTER (WHERE os.approval_status IN ('submitted', 'approved', 'ongoing')) AS outbound_study_count
FROM dtlms_students s
LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
LEFT JOIN LATERAL (
    SELECT plan_status, report_cycle
    FROM dtlms_training_plans
    WHERE student_id = s.id AND is_deleted = FALSE
    ORDER BY updated_at DESC
    LIMIT 1
) tp ON TRUE
LEFT JOIN dtlms_scientific_reports sr ON sr.student_id = s.id AND sr.is_deleted = FALSE
LEFT JOIN dtlms_outbound_studies os ON os.student_id = s.id AND os.is_deleted = FALSE
WHERE s.is_deleted = FALSE
GROUP BY s.id, s.student_no, s.full_name, s.current_status, a.full_name, tp.plan_status, tp.report_cycle;

CREATE OR REPLACE VIEW dtlms_v_degree_pipeline AS
SELECT
    t.id AS thesis_id,
    s.student_no,
    s.full_name,
    a.full_name AS advisor_name,
    t.title,
    t.plagiarism_rate,
    t.thesis_status,
    t.blind_review_status,
    t.defense_date,
    t.degree_granted,
    COUNT(tr.id) AS review_count,
    AVG(tr.review_score) AS avg_review_score
FROM dtlms_theses t
JOIN dtlms_students s ON s.id = t.student_id
JOIN dtlms_advisors a ON a.id = t.advisor_id
LEFT JOIN dtlms_thesis_reviews tr ON tr.thesis_id = t.id
WHERE t.is_deleted = FALSE
GROUP BY t.id, s.student_no, s.full_name, a.full_name, t.title, t.plagiarism_rate, t.thesis_status, t.blind_review_status, t.defense_date, t.degree_granted;
