ALTER TABLE IF EXISTS dtlms_portal_student_profiles
    ADD COLUMN IF NOT EXISTS id_card_collage_url VARCHAR(255);

UPDATE dtlms_portal_student_profiles
SET id_card_collage_url = NULLIF(id_card_collage_url, '')
WHERE id_card_collage_url = '';