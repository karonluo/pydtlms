BEGIN;

DO $$
DECLARE
    v_application_id BIGINT := 34;
    v_portal_student_id BIGINT := 756;
    v_business_key TEXT := 'SH20270374';
    v_candidate_no TEXT := 'SH20270374';
    v_proc_inst_id TEXT := 'procinst-recruitmentappli-sh20270374-d44d1c706c';
    v_actual_application_id BIGINT;
    v_actual_portal_student_id BIGINT;
    v_actual_business_key TEXT;
    v_actual_candidate_no TEXT;
BEGIN
    SELECT
        ra.id,
        ra.portal_student_id,
        ra.business_key,
        ra.candidate_no
    INTO
        v_actual_application_id,
        v_actual_portal_student_id,
        v_actual_business_key,
        v_actual_candidate_no
    FROM dtlms_recruitment_applications ra
    WHERE ra.id = v_application_id
      AND ra.is_deleted = FALSE
    LIMIT 1;

    IF v_actual_application_id IS NULL THEN
        RAISE EXCEPTION '未找到目标报名申请，application_id=%', v_application_id;
    END IF;

    IF v_actual_portal_student_id IS DISTINCT FROM v_portal_student_id THEN
        RAISE EXCEPTION 'portal_student_id 不匹配，expected=%, actual=%', v_portal_student_id, v_actual_portal_student_id;
    END IF;

    IF v_actual_business_key IS DISTINCT FROM v_business_key THEN
        RAISE EXCEPTION 'business_key 不匹配，expected=%, actual=%', v_business_key, v_actual_business_key;
    END IF;

    IF v_actual_candidate_no IS DISTINCT FROM v_candidate_no THEN
        RAISE EXCEPTION 'candidate_no 不匹配，expected=%, actual=%', v_candidate_no, v_actual_candidate_no;
    END IF;

    DELETE FROM dtlms_material_scores
    WHERE reviewer_assignment_id IN (
        SELECT id
        FROM dtlms_reviewer_assignments
        WHERE application_id = v_application_id
    );

    DELETE FROM dtlms_interview_scores
    WHERE schedule_id IN (
        SELECT id
        FROM dtlms_interview_schedules
        WHERE application_id = v_application_id
    );

    DELETE FROM dtlms_admission_decisions
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_written_exam_scores
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_interview_schedules
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_reviewer_assignments
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_background_assessments
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_qualification_reviews
    WHERE application_id = v_application_id;

    DELETE FROM dtlms_wf_ru_identitylink
    WHERE proc_inst_id_ = v_proc_inst_id
       OR task_id_ IN (
            SELECT id_
            FROM dtlms_wf_ru_task
            WHERE proc_inst_id_ = v_proc_inst_id
               OR business_key_ = v_business_key
       );

    DELETE FROM dtlms_wf_ru_variable
    WHERE proc_inst_id_ = v_proc_inst_id;

    DELETE FROM dtlms_wf_ru_task
    WHERE proc_inst_id_ = v_proc_inst_id
       OR business_key_ = v_business_key;

    DELETE FROM dtlms_wf_ru_execution
    WHERE proc_inst_id_ = v_proc_inst_id
       OR business_key_ = v_business_key;

    DELETE FROM dtlms_wf_hi_varinst
    WHERE proc_inst_id_ = v_proc_inst_id;

    DELETE FROM dtlms_wf_hi_actinst
    WHERE proc_inst_id_ = v_proc_inst_id
       OR business_key_ = v_business_key;

    DELETE FROM dtlms_wf_hi_taskinst
    WHERE proc_inst_id_ = v_proc_inst_id
       OR business_key_ = v_business_key
       OR id_ = 'TASK-74';

    DELETE FROM dtlms_wf_hi_procinst
    WHERE proc_inst_id_ = v_proc_inst_id
       OR business_key_ = v_business_key;

    UPDATE dtlms_recruitment_applications
    SET application_status = 'returned',
        applied_at = NULL,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = v_application_id
      AND is_deleted = FALSE;

    UPDATE dtlms_portal_students
    SET submitted_at = NULL,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = v_portal_student_id;
END $$;

-- 说明：
-- 1. 保留 dtlms_recruitment_applications 主档以及 dtlms_portal_application_* 结构化填报内容。
-- 2. 保留 dtlms_portal_application_attachments / personal statements 等附件与材料引用。
-- 3. 将申请状态回写为 returned（门户显示为“驳回重填”），学生可重新编辑并提交。
-- 4. 下次重新提交会复用现有申请主档，因此报名号 SH20270374 不会变化。

SELECT
    ra.id AS application_id,
    ra.portal_student_id,
    ra.business_key,
    ra.candidate_no,
    ra.application_status,
    ra.applied_at,
    ps.submitted_at
FROM dtlms_recruitment_applications ra
JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
WHERE ra.id = 34;

SELECT COUNT(*) AS remaining_runtime_tasks
FROM dtlms_wf_ru_task
WHERE business_key_ = 'SH20270374';

SELECT COUNT(*) AS remaining_history_tasks
FROM dtlms_wf_hi_taskinst
WHERE business_key_ = 'SH20270374';

COMMIT;