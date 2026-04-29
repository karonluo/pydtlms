ALTER TABLE IF EXISTS dtlms_portal_application_education_experiences
    ADD COLUMN IF NOT EXISTS graduation_certificate_attachment_url TEXT;