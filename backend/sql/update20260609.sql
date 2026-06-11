-- 2026-06-09 招生报名申请补充第一/第二志愿导师 ID 字段
-- 说明：仅新增字段与外键约束，不做删除或重建操作。

BEGIN;

ALTER TABLE IF EXISTS dtlms_recruitment_applications
    ADD COLUMN IF NOT EXISTS first_choice_id BIGINT,
    ADD COLUMN IF NOT EXISTS second_choice_id BIGINT;

DO $$
BEGIN
    IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
       AND NOT EXISTS (
         SELECT 1
         FROM pg_constraint
         WHERE conname = 'fk_dtlms_recruitment_applications_first_choice_id'
           AND conrelid = 'dtlms_recruitment_applications'::regclass
       ) THEN
        ALTER TABLE dtlms_recruitment_applications
            ADD CONSTRAINT fk_dtlms_recruitment_applications_first_choice_id
            FOREIGN KEY (first_choice_id) REFERENCES dtlms_users(id) NOT VALID;
    END IF;

    IF to_regclass('public.dtlms_recruitment_applications') IS NOT NULL
       AND NOT EXISTS (
         SELECT 1
         FROM pg_constraint
         WHERE conname = 'fk_dtlms_recruitment_applications_second_choice_id'
           AND conrelid = 'dtlms_recruitment_applications'::regclass
       ) THEN
        ALTER TABLE dtlms_recruitment_applications
            ADD CONSTRAINT fk_dtlms_recruitment_applications_second_choice_id
            FOREIGN KEY (second_choice_id) REFERENCES dtlms_users(id) NOT VALID;
    END IF;
END
$$;

COMMIT;
