ALTER TABLE dtlms_recruitment_applications
    ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_scientific_reports
    ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_outbound_studies
    ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

ALTER TABLE dtlms_theses
    ADD COLUMN IF NOT EXISTS business_key VARCHAR(64);

UPDATE dtlms_recruitment_applications
SET business_key = COALESCE(NULLIF(BTRIM(business_key), ''), candidate_no)
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_scientific_reports
SET business_key = CONCAT('KYBG-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_outbound_studies
SET business_key = CONCAT('WCYX-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

UPDATE dtlms_theses
SET business_key = CONCAT('LWZD-', LPAD(id::TEXT, 6, '0'))
WHERE business_key IS NULL OR BTRIM(business_key) = '';

ALTER TABLE dtlms_recruitment_applications
    ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_scientific_reports
    ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_outbound_studies
    ALTER COLUMN business_key SET NOT NULL;

ALTER TABLE dtlms_theses
    ALTER COLUMN business_key SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_recruitment_applications_business_key
    ON dtlms_recruitment_applications (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_scientific_reports_business_key
    ON dtlms_scientific_reports (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_outbound_studies_business_key
    ON dtlms_outbound_studies (business_key);

CREATE UNIQUE INDEX IF NOT EXISTS ux_dtlms_theses_business_key
    ON dtlms_theses (business_key);