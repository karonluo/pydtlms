CREATE TABLE IF NOT EXISTS dtlms_wf_de_model (
    id_ VARCHAR(64) PRIMARY KEY,
    name_ VARCHAR(255) NOT NULL,
    key_ VARCHAR(128) NOT NULL,
    category_ VARCHAR(128),
    version_ INTEGER NOT NULL DEFAULT 1,
    model_type_ INTEGER NOT NULL DEFAULT 0,
    description_ TEXT,
    meta_info_ JSONB,
    created_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tenant_id_ VARCHAR(64),
    deployment_id_ VARCHAR(64),
    resource_name_ VARCHAR(255),
    editor_source_value_ TEXT,
    editor_source_extra_value_ JSONB
);

CREATE TABLE IF NOT EXISTS dtlms_wf_re_deployment (
    id_ VARCHAR(64) PRIMARY KEY,
    name_ VARCHAR(255) NOT NULL,
    category_ VARCHAR(128),
    key_ VARCHAR(128),
    deploy_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_re_procdef (
    id_ VARCHAR(64) PRIMARY KEY,
    key_ VARCHAR(128) NOT NULL,
    version_ INTEGER NOT NULL DEFAULT 1,
    deployment_id_ VARCHAR(64) REFERENCES dtlms_wf_re_deployment(id_),
    resource_name_ VARCHAR(255),
    diagram_resource_name_ VARCHAR(255),
    name_ VARCHAR(255) NOT NULL,
    category_ VARCHAR(128),
    description_ TEXT,
    suspension_state_ INTEGER NOT NULL DEFAULT 1,
    tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_execution (
    id_ VARCHAR(64) PRIMARY KEY,
    proc_inst_id_ VARCHAR(64) NOT NULL,
    proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
    business_key_ VARCHAR(64),
    parent_id_ VARCHAR(64),
    act_id_ VARCHAR(128),
    is_active_ BOOLEAN NOT NULL DEFAULT TRUE,
    is_concurrent_ BOOLEAN NOT NULL DEFAULT FALSE,
    is_scope_ BOOLEAN NOT NULL DEFAULT TRUE,
    start_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    start_user_id_ VARCHAR(64),
    super_exec_ VARCHAR(64),
    tenant_id_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_task (
    id_ VARCHAR(64) PRIMARY KEY,
    exec_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_ru_execution(id_),
    proc_inst_id_ VARCHAR(64) NOT NULL,
    proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
    task_def_key_ VARCHAR(128),
    name_ VARCHAR(255) NOT NULL,
    business_key_ VARCHAR(64),
    assignee_ VARCHAR(64),
    owner_ VARCHAR(64),
    create_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date_ TIMESTAMPTZ,
    claim_time_ TIMESTAMPTZ,
    priority_ INTEGER NOT NULL DEFAULT 50,
    suspension_state_ INTEGER NOT NULL DEFAULT 1,
    tenant_id_ VARCHAR(64),
    form_key_ VARCHAR(255),
    description_ TEXT
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_variable (
    id_ VARCHAR(128) PRIMARY KEY,
    exec_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_ru_execution(id_),
    proc_inst_id_ VARCHAR(64) NOT NULL,
    task_id_ VARCHAR(64),
    name_ VARCHAR(128) NOT NULL,
    var_type_ VARCHAR(32) NOT NULL,
    text_value_ TEXT,
    number_value_ BIGINT,
    json_value_ JSONB,
    create_time_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_wf_ru_identitylink (
    id_ BIGSERIAL PRIMARY KEY,
    task_id_ VARCHAR(64) NOT NULL,
    proc_inst_id_ VARCHAR(64),
    user_id_ VARCHAR(64),
    group_id_ VARCHAR(64),
    link_type_ VARCHAR(32) NOT NULL,
    created_at_ TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_procinst (
    id_ VARCHAR(64) PRIMARY KEY,
    proc_inst_id_ VARCHAR(64) NOT NULL UNIQUE,
    business_key_ VARCHAR(64),
    proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
    start_time_ TIMESTAMPTZ NOT NULL,
    end_time_ TIMESTAMPTZ,
    duration_ms_ BIGINT,
    start_user_id_ VARCHAR(64),
    end_act_id_ VARCHAR(128),
    delete_reason_ VARCHAR(255),
    start_act_id_ VARCHAR(128),
    state_ VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_taskinst (
    id_ VARCHAR(64) PRIMARY KEY,
    task_def_key_ VARCHAR(128),
    proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
    proc_inst_id_ VARCHAR(64) NOT NULL,
    exec_id_ VARCHAR(64),
    name_ VARCHAR(255) NOT NULL,
    business_key_ VARCHAR(64),
    assignee_ VARCHAR(64),
    owner_ VARCHAR(64),
    start_time_ TIMESTAMPTZ NOT NULL,
    claim_time_ TIMESTAMPTZ,
    end_time_ TIMESTAMPTZ,
    duration_ms_ BIGINT,
    due_date_ TIMESTAMPTZ,
    delete_reason_ VARCHAR(255),
    priority_ INTEGER NOT NULL DEFAULT 50,
    category_ VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_actinst (
    id_ VARCHAR(64) PRIMARY KEY,
    proc_def_id_ VARCHAR(64) NOT NULL REFERENCES dtlms_wf_re_procdef(id_),
    proc_inst_id_ VARCHAR(64) NOT NULL,
    exec_id_ VARCHAR(64),
    act_id_ VARCHAR(128) NOT NULL,
    act_name_ VARCHAR(255),
    act_type_ VARCHAR(64) NOT NULL,
    assignee_ VARCHAR(64),
    start_time_ TIMESTAMPTZ NOT NULL,
    end_time_ TIMESTAMPTZ,
    duration_ms_ BIGINT,
    business_key_ VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS dtlms_wf_hi_varinst (
    id_ VARCHAR(128) PRIMARY KEY,
    proc_inst_id_ VARCHAR(64) NOT NULL,
    exec_id_ VARCHAR(64),
    task_id_ VARCHAR(64),
    name_ VARCHAR(128) NOT NULL,
    var_type_ VARCHAR(32) NOT NULL,
    text_value_ TEXT,
    number_value_ BIGINT,
    json_value_ JSONB,
    create_time_ TIMESTAMPTZ NOT NULL,
    last_updated_time_ TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dtlms_wf_re_procdef_key ON dtlms_wf_re_procdef (key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_execution_proc_inst ON dtlms_wf_ru_execution (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_task_proc_inst ON dtlms_wf_ru_task (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_ru_task_business_key ON dtlms_wf_ru_task (business_key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_procinst_business_key ON dtlms_wf_hi_procinst (business_key_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_taskinst_proc_inst ON dtlms_wf_hi_taskinst (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_actinst_proc_inst ON dtlms_wf_hi_actinst (proc_inst_id_);
CREATE INDEX IF NOT EXISTS idx_dtlms_wf_hi_varinst_proc_inst ON dtlms_wf_hi_varinst (proc_inst_id_);