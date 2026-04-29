-- 治理、培养、学位与工作流兼容表关系化补齐

ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS department_name VARCHAR(128) NOT NULL DEFAULT '';
ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(32);
ALTER TABLE dtlms_users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMPTZ;
ALTER TABLE dtlms_roles ADD COLUMN IF NOT EXISTS scope_name VARCHAR(128) NOT NULL DEFAULT '系统管理';

CREATE TABLE IF NOT EXISTS dtlms_audit_policies (
    id BIGINT PRIMARY KEY,
    item VARCHAR(128) NOT NULL,
    policy TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT '启用',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS dtlms_integrations (
    id BIGINT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    direction VARCHAR(64) NOT NULL,
    cadence VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT '正常',
    owner VARCHAR(128) NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

WITH runtime_roles_source AS (
    SELECT
        rr.id,
        NULLIF(BTRIM(rr.payload ->> 'role_code'), '') AS role_code,
        COALESCE(NULLIF(BTRIM(rr.payload ->> 'role_name'), ''), NULLIF(BTRIM(rr.payload ->> 'role_code'), ''), CONCAT('ROLE-', rr.id::TEXT)) AS role_name,
        COALESCE(NULLIF(BTRIM(rr.payload ->> 'scope_name'), ''), '系统管理') AS scope_name,
        NULLIF(BTRIM(rr.payload ->> 'description'), '') AS description
    FROM dtlms_runtime_roles rr
    WHERE rr.payload IS NOT NULL
      AND NULLIF(BTRIM(rr.payload ->> 'role_code'), '') IS NOT NULL
), updated_existing_roles AS (
    UPDATE dtlms_roles dr
    SET role_name = src.role_name,
        scope_name = src.scope_name,
        description = src.description,
        is_deleted = FALSE,
        updated_at = CURRENT_TIMESTAMP
    FROM runtime_roles_source src
    WHERE dr.role_code = src.role_code
    RETURNING src.id
)
INSERT INTO dtlms_roles (id, role_code, role_name, scope_name, description, is_deleted)
SELECT
    src.id,
    src.role_code,
    src.role_name,
    src.scope_name,
    src.description,
    FALSE
FROM runtime_roles_source src
LEFT JOIN updated_existing_roles updated ON updated.id = src.id
WHERE updated.id IS NULL
ON CONFLICT (id) DO UPDATE
SET role_code = EXCLUDED.role_code,
    role_name = EXCLUDED.role_name,
    scope_name = EXCLUDED.scope_name,
    description = EXCLUDED.description,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_role_permissions (role_id, permission_id)
SELECT DISTINCT rr.id, p.id
FROM dtlms_runtime_roles rr
JOIN LATERAL jsonb_array_elements_text(
    CASE
        WHEN jsonb_typeof(rr.payload -> 'permissions') = 'array' THEN rr.payload -> 'permissions'
        ELSE '[]'::jsonb
    END
) perm(permission_code) ON TRUE
JOIN dtlms_permissions p ON p.permission_code = perm.permission_code AND p.is_deleted = FALSE
WHERE rr.payload IS NOT NULL
ON CONFLICT (role_id, permission_id) DO NOTHING;

INSERT INTO dtlms_users (
    id, username, full_name, email, department_name, phone_number,
    password_hash, is_active, is_deleted, last_login_at
)
SELECT
    ru.id,
    NULLIF(BTRIM(ru.payload ->> 'username'), ''),
    COALESCE(NULLIF(BTRIM(ru.payload ->> 'full_name'), ''), NULLIF(BTRIM(ru.payload ->> 'username'), '')),
    up.email,
    COALESCE(NULLIF(BTRIM(ru.payload ->> 'department_name'), ''), ''),
    NULLIF(BTRIM(ru.payload ->> 'phone_number'), ''),
    NULLIF(ru.payload ->> 'password_hash', ''),
    CASE COALESCE(NULLIF(BTRIM(ru.payload ->> 'account_status'), ''), '启用') WHEN '停用' THEN FALSE ELSE TRUE END,
    FALSE,
    CASE WHEN NULLIF(BTRIM(ru.payload ->> 'last_login_at'), '') IS NULL THEN NULL ELSE (ru.payload ->> 'last_login_at')::TIMESTAMPTZ END
FROM dtlms_runtime_system_users ru
LEFT JOIN dtlms_user_profiles up ON up.username = NULLIF(BTRIM(ru.payload ->> 'username'), '')
WHERE ru.payload IS NOT NULL
  AND NULLIF(BTRIM(ru.payload ->> 'username'), '') IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET username = EXCLUDED.username,
    full_name = EXCLUDED.full_name,
    email = COALESCE(EXCLUDED.email, dtlms_users.email),
    department_name = EXCLUDED.department_name,
    phone_number = EXCLUDED.phone_number,
    password_hash = COALESCE(EXCLUDED.password_hash, dtlms_users.password_hash),
    is_active = EXCLUDED.is_active,
    is_deleted = FALSE,
    last_login_at = COALESCE(EXCLUDED.last_login_at, dtlms_users.last_login_at),
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_user_roles (user_id, role_id, grant_source)
SELECT DISTINCT ru.id, r.id, 'runtime_sync'
FROM dtlms_runtime_system_users ru
JOIN dtlms_roles r ON r.role_code = NULLIF(BTRIM(ru.payload ->> 'role_code'), '') AND r.is_deleted = FALSE
WHERE ru.payload IS NOT NULL
  AND NULLIF(BTRIM(ru.payload ->> 'username'), '') IS NOT NULL
ON CONFLICT (user_id, role_id) DO UPDATE
SET grant_source = EXCLUDED.grant_source,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_audit_policies (id, item, policy, status, is_deleted)
SELECT
    rap.id,
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'item'), ''), CONCAT('策略-', rap.id::TEXT)),
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'policy'), ''), ''),
    COALESCE(NULLIF(BTRIM(rap.payload ->> 'status'), ''), '启用'),
    FALSE
FROM dtlms_runtime_audit_policies rap
WHERE rap.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET item = EXCLUDED.item,
    policy = EXCLUDED.policy,
    status = EXCLUDED.status,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_integrations (id, name, direction, cadence, status, owner, is_deleted)
SELECT
    ri.id,
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'name'), ''), CONCAT('集成-', ri.id::TEXT)),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'direction'), ''), '单向'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'cadence'), ''), '按需'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'status'), ''), '正常'),
    COALESCE(NULLIF(BTRIM(ri.payload ->> 'owner'), ''), ''),
    FALSE
FROM dtlms_runtime_integrations ri
WHERE ri.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
    direction = EXCLUDED.direction,
    cadence = EXCLUDED.cadence,
    status = EXCLUDED.status,
    owner = EXCLUDED.owner,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_training_plans AS (
    SELECT id, payload FROM dtlms_runtime_training_plans WHERE payload IS NOT NULL
)
INSERT INTO dtlms_training_plans (
    id, student_id, advisor_id, version_no, report_cycle, plan_status,
    scientific_goal, assessment_rule, is_deleted
)
SELECT
    rtp.id,
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'version_no'), ''), 'v1.0'),
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'report_cycle'), ''), '每学期'),
    CASE COALESCE(NULLIF(BTRIM(rtp.payload ->> 'plan_status'), ''), '待学生确认') WHEN '执行中' THEN 'active' WHEN '已归档' THEN 'archived' ELSE 'draft' END,
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'scientific_goal'), ''), ''),
    COALESCE(NULLIF(BTRIM(rtp.payload ->> 'assessment_rule'), ''), ''),
    FALSE
FROM runtime_training_plans rtp
JOIN dtlms_students s ON s.student_no = NULLIF(BTRIM(rtp.payload ->> 'student_no'), '') AND s.is_deleted = FALSE
JOIN dtlms_advisors a ON a.full_name = NULLIF(BTRIM(rtp.payload ->> 'advisor_name'), '') AND a.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    version_no = EXCLUDED.version_no,
    report_cycle = EXCLUDED.report_cycle,
    plan_status = EXCLUDED.plan_status,
    scientific_goal = EXCLUDED.scientific_goal,
    assessment_rule = EXCLUDED.assessment_rule,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_training_plan_versions (training_plan_id, version_no, change_reason, plan_snapshot)
SELECT tp.id, tp.version_no, '自动迁移回填', tp.scientific_goal
FROM dtlms_training_plans tp
WHERE tp.is_deleted = FALSE
  AND NOT EXISTS (
      SELECT 1 FROM dtlms_training_plan_versions tpv WHERE tpv.training_plan_id = tp.id AND tpv.version_no = tp.version_no
  );

WITH runtime_reports AS (
    SELECT id, payload FROM dtlms_runtime_scientific_reports WHERE payload IS NOT NULL
)
INSERT INTO dtlms_scientific_reports (
    id, business_key, student_id, training_plan_id, period_label, report_status,
    summary, attachment_url, reviewer_advisor_id, review_score, review_comment, is_deleted
)
SELECT
    rr.id,
    NULLIF(BTRIM(rr.payload ->> 'business_key'), ''),
    s.id,
    tp.id,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'period_label'), ''), ''),
    CASE COALESCE(NULLIF(BTRIM(rr.payload ->> 'report_status'), ''), '待导师审阅') WHEN '已归档' THEN 'archived' WHEN '已通过' THEN 'approved' WHEN '退回修改' THEN 'returned' ELSE 'submitted' END,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'summary'), ''), ''),
    CONCAT('/reports/', rr.payload ->> 'student_no', '/', COALESCE(NULLIF(BTRIM(rr.payload ->> 'period_label'), ''), 'report'), '.pdf'),
    reviewer.id,
    CASE WHEN NULLIF(BTRIM(rr.payload ->> 'review_score'), '') IS NULL THEN NULL ELSE (rr.payload ->> 'review_score')::NUMERIC(5,2) END,
    COALESCE(NULLIF(BTRIM(rr.payload ->> 'review_comment'), ''), NULLIF(BTRIM(rr.payload ->> 'latest_comment'), '')),
    FALSE
FROM runtime_reports rr
JOIN dtlms_students s ON s.student_no = NULLIF(BTRIM(rr.payload ->> 'student_no'), '') AND s.is_deleted = FALSE
JOIN dtlms_training_plans tp ON tp.student_id = s.id AND tp.is_deleted = FALSE
LEFT JOIN dtlms_advisors reviewer ON reviewer.full_name = NULLIF(BTRIM(rr.payload ->> 'reviewer_name'), '') AND reviewer.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    training_plan_id = EXCLUDED.training_plan_id,
    period_label = EXCLUDED.period_label,
    report_status = EXCLUDED.report_status,
    summary = EXCLUDED.summary,
    attachment_url = EXCLUDED.attachment_url,
    reviewer_advisor_id = EXCLUDED.reviewer_advisor_id,
    review_score = EXCLUDED.review_score,
    review_comment = EXCLUDED.review_comment,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_outbound AS (
    SELECT id, payload FROM dtlms_runtime_outbound_studies WHERE payload IS NOT NULL
)
INSERT INTO dtlms_outbound_studies (
    id, business_key, student_id, advisor_id, study_type, destination,
    start_date, end_date, approval_status, expected_outcome, is_deleted
)
SELECT
    ros.id,
    NULLIF(BTRIM(ros.payload ->> 'business_key'), ''),
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(ros.payload ->> 'study_type'), ''), ''),
    COALESCE(NULLIF(BTRIM(ros.payload ->> 'destination'), ''), ''),
    CASE WHEN NULLIF(BTRIM(ros.payload ->> 'start_date'), '') IS NULL THEN NULL ELSE (ros.payload ->> 'start_date')::DATE END,
    CASE WHEN NULLIF(BTRIM(ros.payload ->> 'end_date'), '') IS NULL THEN NULL ELSE (ros.payload ->> 'end_date')::DATE END,
    CASE COALESCE(NULLIF(BTRIM(ros.payload ->> 'approval_status'), ''), '审批中') WHEN '已完成' THEN 'completed' WHEN '已驳回' THEN 'rejected' WHEN '研修中' THEN 'approved' ELSE 'submitted' END,
    NULLIF(BTRIM(ros.payload ->> 'expected_outcome'), ''),
    FALSE
FROM runtime_outbound ros
JOIN dtlms_students s ON s.student_no = NULLIF(BTRIM(ros.payload ->> 'student_no'), '') AND s.is_deleted = FALSE
JOIN dtlms_advisors a ON a.full_name = NULLIF(BTRIM(ros.payload ->> 'advisor_name'), '') AND a.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    study_type = EXCLUDED.study_type,
    destination = EXCLUDED.destination,
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    approval_status = EXCLUDED.approval_status,
    expected_outcome = EXCLUDED.expected_outcome,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

WITH runtime_theses AS (
    SELECT id, payload FROM dtlms_runtime_theses WHERE payload IS NOT NULL
)
INSERT INTO dtlms_theses (
    id, business_key, student_id, advisor_id, title, plagiarism_rate,
    thesis_status, blind_review_status, defense_date, degree_granted, is_deleted
)
SELECT
    rt.id,
    NULLIF(BTRIM(rt.payload ->> 'business_key'), ''),
    s.id,
    a.id,
    COALESCE(NULLIF(BTRIM(rt.payload ->> 'title'), ''), ''),
    CASE WHEN NULLIF(BTRIM(rt.payload ->> 'plagiarism_rate'), '') IS NULL THEN NULL ELSE (rt.payload ->> 'plagiarism_rate')::NUMERIC(5,2) END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'thesis_status'), ''), '待查重') WHEN '已完成' THEN 'completed' WHEN '撰写中' THEN 'drafting' WHEN '查重中' THEN 'plagiarism_check' ELSE 'draft' END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'blind_review_status'), ''), '未送审') WHEN '通过' THEN 'passed' WHEN '未通过' THEN 'failed' WHEN '进行中' THEN 'in_review' ELSE 'not_started' END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'defense_status'), ''), '未进入') WHEN '已完成' THEN CURRENT_DATE ELSE NULL END,
    CASE COALESCE(NULLIF(BTRIM(rt.payload ->> 'degree_status'), ''), '待申请') WHEN '已授位' THEN TRUE ELSE FALSE END,
    FALSE
FROM runtime_theses rt
JOIN dtlms_students s ON s.student_no = NULLIF(BTRIM(rt.payload ->> 'student_no'), '') AND s.is_deleted = FALSE
JOIN dtlms_advisors a ON a.full_name = NULLIF(BTRIM(rt.payload ->> 'advisor_name'), '') AND a.is_deleted = FALSE
ON CONFLICT (id) DO UPDATE
SET business_key = EXCLUDED.business_key,
    student_id = EXCLUDED.student_id,
    advisor_id = EXCLUDED.advisor_id,
    title = EXCLUDED.title,
    plagiarism_rate = EXCLUDED.plagiarism_rate,
    thesis_status = EXCLUDED.thesis_status,
    blind_review_status = EXCLUDED.blind_review_status,
    defense_date = EXCLUDED.defense_date,
    degree_granted = EXCLUDED.degree_granted,
    is_deleted = FALSE,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO dtlms_thesis_reviews (id, thesis_id, expert_name, review_score, review_status, review_comment)
SELECT
    tr.id,
    COALESCE((tr.payload ->> 'thesis_id')::BIGINT, 0),
    COALESCE(NULLIF(BTRIM(tr.payload ->> 'expert_name'), ''), ''),
    CASE WHEN NULLIF(BTRIM(tr.payload ->> 'review_score'), '') IS NULL THEN NULL ELSE (tr.payload ->> 'review_score')::NUMERIC(5,2) END,
    CASE COALESCE(NULLIF(BTRIM(tr.payload ->> 'review_status'), ''), '待提交') WHEN '已退回' THEN 'returned' WHEN '已完成' THEN 'completed' ELSE 'pending' END,
    NULLIF(BTRIM(tr.payload ->> 'review_comment'), '')
FROM dtlms_runtime_thesis_reviews tr
WHERE tr.payload IS NOT NULL
ON CONFLICT (id) DO UPDATE
SET thesis_id = EXCLUDED.thesis_id,
    expert_name = EXCLUDED.expert_name,
    review_score = EXCLUDED.review_score,
    review_status = EXCLUDED.review_status,
    review_comment = EXCLUDED.review_comment,
    updated_at = CURRENT_TIMESTAMP;

WITH normalized_tasks AS (
    SELECT
        id,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_node'), ''), '待处理') AS current_node,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(NULLIF(BTRIM(payload ->> 'applicant_name'), ''), '未知申请人') AS applicant_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_handler'), ''), '待分派') AS current_handler,
        NULLIF(BTRIM(payload ->> 'form_summary'), '') AS form_summary,
        NULLIF(BTRIM(payload ->> 'latest_comment'), '') AS latest_comment,
        CASE WHEN NULLIF(BTRIM(payload ->> 'entity_id'), '') IS NULL THEN 0 ELSE (payload ->> 'entity_id')::BIGINT END AS entity_id,
        CASE WHEN jsonb_typeof(payload -> 'candidate_groups') = 'array' THEN payload -> 'candidate_groups' ELSE '[]'::jsonb END AS candidate_groups,
        CASE WHEN jsonb_typeof(payload -> 'history') = 'array' THEN payload -> 'history' ELSE '[]'::jsonb END AS history_entries,
        COALESCE(CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END, CURRENT_TIMESTAMP) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中') WHEN '低' THEN 25 WHEN '高' THEN 75 WHEN '紧急' THEN 100 ELSE 50 END AS priority_value,
        CONCAT('DEPLOY-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow')) AS deployment_id,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_re_deployment (id_, name_, category_, key_, deploy_time_)
SELECT DISTINCT deployment_id, workflow_name, business_module, flow_code, created_at
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET name_ = EXCLUDED.name_,
    category_ = EXCLUDED.category_,
    key_ = EXCLUDED.key_,
    deploy_time_ = EXCLUDED.deploy_time_;

WITH normalized_tasks AS (
    SELECT DISTINCT
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        CONCAT('DEPLOY-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow')) AS deployment_id,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_re_procdef (
    id_, key_, version_, deployment_id_, resource_name_, diagram_resource_name_, name_, category_, description_, suspension_state_
)
SELECT proc_def_id, flow_code, 1, deployment_id, CONCAT(flow_code, '.bpmn20.xml'), CONCAT(flow_code, '.png'), workflow_name, business_module, CONCAT(workflow_name, ' 定义'), 1
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET key_ = EXCLUDED.key_,
    deployment_id_ = EXCLUDED.deployment_id_,
    resource_name_ = EXCLUDED.resource_name_,
    diagram_resource_name_ = EXCLUDED.diagram_resource_name_,
    name_ = EXCLUDED.name_,
    category_ = EXCLUDED.category_,
    description_ = EXCLUDED.description_;

WITH normalized_tasks AS (
    SELECT
        id,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END, CURRENT_TIMESTAMP) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中') WHEN '低' THEN 25 WHEN '高' THEN 75 WHEN '紧急' THEN 100 ELSE 50 END AS priority_value,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_hi_procinst (
    id_, proc_inst_id_, business_key_, proc_def_id_, start_time_, end_time_, duration_ms_,
    start_user_id_, end_act_id_, delete_reason_, start_act_id_, state_
)
SELECT
    proc_inst_id,
    proc_inst_id,
    business_key,
    proc_def_id,
    created_at,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN COALESCE(due_at, created_at) ELSE NULL END,
    NULL,
    NULL,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN node_key ELSE NULL END,
    CASE WHEN task_status = '已驳回' THEN 'rejected' ELSE NULL END,
    'startEvent',
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN 'COMPLETED' ELSE 'ACTIVE' END
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET business_key_ = EXCLUDED.business_key_,
    proc_def_id_ = EXCLUDED.proc_def_id_,
    start_time_ = EXCLUDED.start_time_,
    end_time_ = EXCLUDED.end_time_,
    end_act_id_ = EXCLUDED.end_act_id_,
    delete_reason_ = EXCLUDED.delete_reason_,
    state_ = EXCLUDED.state_;

WITH normalized_tasks AS (
    SELECT
        id,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'title'), ''), '未命名任务') AS task_title,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(CASE WHEN NULLIF(BTRIM(payload ->> 'created_at'), '') IS NULL THEN NULL ELSE (payload ->> 'created_at')::TIMESTAMPTZ END, CURRENT_TIMESTAMP) AS created_at,
        CASE WHEN NULLIF(BTRIM(payload ->> 'due_at'), '') IS NULL THEN NULL ELSE (payload ->> 'due_at')::TIMESTAMPTZ END AS due_at,
        CASE COALESCE(NULLIF(BTRIM(payload ->> 'priority'), ''), '中') WHEN '低' THEN 25 WHEN '高' THEN 75 WHEN '紧急' THEN 100 ELSE 50 END AS priority_value,
        CONCAT('PROCDEF-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-v1') AS proc_def_id,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
)
INSERT INTO dtlms_wf_hi_taskinst (
    id_, task_def_key_, proc_def_id_, proc_inst_id_, exec_id_, name_, business_key_, assignee_, owner_,
    start_time_, claim_time_, end_time_, duration_ms_, due_date_, delete_reason_, priority_, category_
)
SELECT
    CONCAT('TASK-', id::TEXT),
    node_key,
    proc_def_id,
    proc_inst_id,
    exec_id,
    task_title,
    business_key,
    NULL,
    NULL,
    created_at,
    NULL,
    CASE WHEN task_status IN ('已通过', '已驳回', '已完成') THEN COALESCE(due_at, created_at) ELSE NULL END,
    NULL,
    due_at,
    CASE WHEN task_status = '已驳回' THEN 'rejected' ELSE NULL END,
    priority_value,
    business_module
FROM normalized_tasks
ON CONFLICT (id_) DO UPDATE
SET task_def_key_ = EXCLUDED.task_def_key_,
    proc_def_id_ = EXCLUDED.proc_def_id_,
    proc_inst_id_ = EXCLUDED.proc_inst_id_,
    exec_id_ = EXCLUDED.exec_id_,
    name_ = EXCLUDED.name_,
    business_key_ = EXCLUDED.business_key_,
    start_time_ = EXCLUDED.start_time_,
    end_time_ = EXCLUDED.end_time_,
    due_date_ = EXCLUDED.due_date_,
    priority_ = EXCLUDED.priority_,
    category_ = EXCLUDED.category_;

WITH normalized_tasks AS (
    SELECT
        id,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)) AS business_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'workflow_name'), ''), '未命名流程') AS workflow_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'business_module'), ''), '流程中心') AS business_module,
        COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow') AS flow_code,
        COALESCE(NULLIF(BTRIM(payload ->> 'node_key'), ''), 'manual_task') AS node_key,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_node'), ''), '待处理') AS current_node,
        COALESCE(NULLIF(BTRIM(payload ->> 'status'), ''), '待处理') AS task_status,
        COALESCE(NULLIF(BTRIM(payload ->> 'applicant_name'), ''), '未知申请人') AS applicant_name,
        COALESCE(NULLIF(BTRIM(payload ->> 'current_handler'), ''), '待分派') AS current_handler,
        NULLIF(BTRIM(payload ->> 'form_summary'), '') AS form_summary,
        NULLIF(BTRIM(payload ->> 'latest_comment'), '') AS latest_comment,
        CASE WHEN NULLIF(BTRIM(payload ->> 'entity_id'), '') IS NULL THEN 0 ELSE (payload ->> 'entity_id')::BIGINT END AS entity_id,
        CASE WHEN jsonb_typeof(payload -> 'candidate_groups') = 'array' THEN payload -> 'candidate_groups' ELSE '[]'::jsonb END AS candidate_groups,
        CASE WHEN jsonb_typeof(payload -> 'history') = 'array' THEN payload -> 'history' ELSE '[]'::jsonb END AS history_entries,
        CONCAT('PROC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', md5(COALESCE(NULLIF(BTRIM(payload ->> 'business_key'), ''), CONCAT('TASK-', id::TEXT)))) AS proc_inst_id,
        CONCAT('EXEC-', COALESCE(NULLIF(BTRIM(payload ->> 'flow_code'), ''), 'adhoc_workflow'), '-', id::TEXT) AS exec_id
    FROM dtlms_runtime_workflow_tasks
    WHERE payload IS NOT NULL
), variable_rows AS (
    SELECT CONCAT('HVAR-', nt.id::TEXT, '-businessKey') AS id_, nt.proc_inst_id, nt.exec_id, 'businessKey' AS name_, 'string' AS var_type_, to_jsonb(nt.business_key) AS json_value_, nt.business_key AS text_value_ FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-workflowName'), nt.proc_inst_id, nt.exec_id, 'workflowName', 'string', to_jsonb(nt.workflow_name), nt.workflow_name FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-businessModule'), nt.proc_inst_id, nt.exec_id, 'businessModule', 'string', to_jsonb(nt.business_module), nt.business_module FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-applicantName'), nt.proc_inst_id, nt.exec_id, 'applicantName', 'string', to_jsonb(nt.applicant_name), nt.applicant_name FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-currentHandler'), nt.proc_inst_id, nt.exec_id, 'currentHandler', 'string', to_jsonb(nt.current_handler), nt.current_handler FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-currentNode'), nt.proc_inst_id, nt.exec_id, 'currentNode', 'string', to_jsonb(nt.current_node), nt.current_node FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-nodeKey'), nt.proc_inst_id, nt.exec_id, 'nodeKey', 'string', to_jsonb(nt.node_key), nt.node_key FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-taskStatus'), nt.proc_inst_id, nt.exec_id, 'taskStatus', 'string', to_jsonb(nt.task_status), nt.task_status FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-formSummary'), nt.proc_inst_id, nt.exec_id, 'formSummary', 'string', to_jsonb(nt.form_summary), nt.form_summary FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-latestComment'), nt.proc_inst_id, nt.exec_id, 'latestComment', 'string', to_jsonb(nt.latest_comment), nt.latest_comment FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-flowCode'), nt.proc_inst_id, nt.exec_id, 'flowCode', 'string', to_jsonb(nt.flow_code), nt.flow_code FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-entityId'), nt.proc_inst_id, nt.exec_id, 'entityId', 'long', to_jsonb(nt.entity_id), nt.entity_id::TEXT FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-candidateGroups'), nt.proc_inst_id, nt.exec_id, 'candidateGroups', 'json', nt.candidate_groups, NULL FROM normalized_tasks nt
    UNION ALL SELECT CONCAT('HVAR-', nt.id::TEXT, '-historyEntries'), nt.proc_inst_id, nt.exec_id, 'historyEntries', 'json', nt.history_entries, NULL FROM normalized_tasks nt
)
INSERT INTO dtlms_wf_hi_varinst (id_, proc_inst_id_, exec_id_, name_, var_type_, text_value_, json_value_, create_time_, last_updated_time_)
SELECT
    vr.id_,
    vr.proc_inst_id,
    vr.exec_id,
    vr.name_,
    vr.var_type_,
    vr.text_value_,
    vr.json_value_,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM variable_rows vr
ON CONFLICT (id_) DO UPDATE
SET text_value_ = EXCLUDED.text_value_,
    json_value_ = EXCLUDED.json_value_,
    last_updated_time_ = CURRENT_TIMESTAMP;