-- 2026-06-04 注册学生主表报名号补丁
-- 说明：dtlms_portal_students 是注册学生主表；为其增加可空报名号 candidate_no，建立索引，并回填历史已提交记录。

BEGIN;

ALTER TABLE IF EXISTS dtlms_portal_students
    ADD COLUMN IF NOT EXISTS candidate_no VARCHAR(64);

ALTER TABLE IF EXISTS dtlms_portal_students
  DROP COLUMN IF EXISTS application_draft;

ALTER TABLE IF EXISTS dtlms_portal_application_preferences
  DROP COLUMN IF EXISTS is_optional;

CREATE INDEX IF NOT EXISTS idx_dtlms_portal_students_candidate_no
  ON dtlms_portal_students (candidate_no)
  WHERE candidate_no IS NOT NULL AND BTRIM(candidate_no) <> '';

CREATE OR REPLACE FUNCTION dtlms_portal_students_candidate_no_immutable()
RETURNS TRIGGER AS $$
BEGIN
  IF COALESCE(OLD.candidate_no, '') <> ''
     AND COALESCE(NEW.candidate_no, '') IS DISTINCT FROM OLD.candidate_no THEN
    RAISE EXCEPTION 'candidate_no is immutable once assigned for dtlms_portal_students id=%', OLD.id;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_dtlms_portal_students_candidate_no_immutable ON dtlms_portal_students;
CREATE TRIGGER trg_dtlms_portal_students_candidate_no_immutable
BEFORE UPDATE OF candidate_no ON dtlms_portal_students
FOR EACH ROW
EXECUTE FUNCTION dtlms_portal_students_candidate_no_immutable();

WITH latest_application AS (
    SELECT DISTINCT ON (ra.portal_student_id)
        ra.portal_student_id,
        NULLIF(BTRIM(COALESCE(ra.candidate_no, ra.business_key)), '') AS candidate_no
    FROM dtlms_recruitment_applications ra
    WHERE ra.is_deleted = FALSE
      AND NULLIF(BTRIM(COALESCE(ra.candidate_no, ra.business_key)), '') IS NOT NULL
    ORDER BY ra.portal_student_id, ra.created_at DESC, ra.id DESC
)
UPDATE dtlms_portal_students AS ps
SET candidate_no = latest_application.candidate_no,
    updated_at = CURRENT_TIMESTAMP
FROM latest_application
WHERE latest_application.portal_student_id = ps.id
  AND (ps.candidate_no IS NULL OR BTRIM(ps.candidate_no) = '');

COMMIT;
