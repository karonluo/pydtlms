ALTER TABLE IF EXISTS dtlms_portal_application_achievement_records
    ADD COLUMN IF NOT EXISTS achievement_month VARCHAR(16),
    ADD COLUMN IF NOT EXISTS award_rank VARCHAR(64),
    ADD COLUMN IF NOT EXISTS award_certificate_attachment_url VARCHAR(512),
    ADD COLUMN IF NOT EXISTS description_text TEXT;