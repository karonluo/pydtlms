ALTER TABLE IF EXISTS dtlms_portal_students
    ADD COLUMN IF NOT EXISTS application_draft JSONB;

UPDATE dtlms_portal_students AS ps
SET application_draft = rs.payload -> 'application_draft',
    updated_at = CURRENT_TIMESTAMP
FROM dtlms_runtime_portal_students AS rs
WHERE rs.id = ps.id
  AND jsonb_typeof(rs.payload -> 'application_draft') = 'object'
  AND (
      ps.application_draft IS NULL
      OR ps.application_draft = '{}'::jsonb
  );
