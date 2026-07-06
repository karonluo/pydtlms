# CHANGELOG

> 重大变更与功能说明。新增放在最上面，按时间倒序。
> 本文件由 Codex 在重大功能/字段变更后维护。

## [2026-07-06] 修复字典写接口缺失导入的 bug

### 问题
ackend/app/api/v1/system.py 的 导入列表里缺失 create_dict_type 与 create_dict_data，导致 POST /api/v1/system/dict-types 与 POST /api/v1/system/dict-data 调用时报 NameError: name 'create_dict_type' / 'create_dict_data' is not defined。该 bug 在本代码仓库中原就存在，与上一条审计增量改动无关。

### 修复
- 在 rom app.services.dashboard_service import (...) 块中按字母顺序补入 create_dict_data 与 create_dict_type，其他函数保持不变

### 验证
- pytest backend/tests/api/test_backoffice_operation_audit.py 3/3 仍然 PASS

### 备份
- ackend/app/api/v1/system_20260706153311.py.bak（本文件被 .gitignore 中 *.bak 忽略）

## [2026-07-06] 字典管理写操作增量审计

### 背景
字典管理（/api/v1/system/dict-types、/api/v1/system/dict-data）之前的写操作仅靠 
ecord_backoffice_operation_audit 中间件兑底记录，summary 是机械的接口路径文案，不友好且无法区分 "字典类型" 与 "字典数据"。本次为字典写接口加入业务审计描述器。

### 后端变更
- ackend/app/main.py
  - 解决业务审计描述器 (_resolve_business_audit_descriptor) 新增 6 个字典路径分支：
    - POST /system/dict-types -> 模块="系统治理"，实体=dict-types，动作="新增"，summary=""新增 dict-types - POST /api/v1/system/dict-types""
    - PUT /system/dict-types/{id} -> "编辑 dict-types id={id} - PUT /api/v1/system/dict-types/{id}""
    - DELETE /system/dict-types/{id} -> "删除 dict-types id={id} - DELETE /api/v1/system/dict-types/{id}""
    - POST /system/dict-data / PUT /system/dict-data/{id} / DELETE /system/dict-data/{id} 同上，实体=dict-data
  - summary 同时保留 method+path，以保证现有 	est_backoffice_write_request_records_operation_log 等约束仍然成立
  - 不动 dashboard_service.py / pi/v1/system.py：业务函数仍由中间件兑底，原有 业务函数已写手工日志 -> 中间件不重复 约束保持生效

### 验证
- pytest backend/tests/api/test_backoffice_operation_audit.py 全 3 个用例全部 PASS：
  - 	est_backoffice_write_request_records_operation_log 验证总结为“系统治理 / dict-types / 1 / 编辑”，operator=admin，result=success，summary 包含 PUT /api/v1/system/dict-types/1
  - 	est_auth_post_request_is_excluded_from_backoffice_audit 仍然排除 /auth/token
  - 	est_backoffice_write_request_keeps_single_log_when_manual_log_exists 仍然保证“业务已写手工日志中间件不重复”约束不受影响

### 备份
- 本次只改动一个源文件：ackend/app/main.py
- 备份文件：ackend/app/main_20260706150250.py.bak（本文件在 .gitignore 中被 § *.bak 忽略，不会提交到版本控制）

### 本期不做（后续迭代）
- [ ] 字典写接口在 dtlms_operation_logs 中填写详细的 old_value / new_value JSONB
- [ ] 为字典选项读接口加入 Redis 缓存，写后自动失效
- [ ] 字典写接口在失败时（如类型下还有子数据无法删除）也记一条 result=failed 的审计日志

## [2026-07-01] 黑客松夏令营（hackathon）入取流程

### 业务背景
黑客松夏令营是学生入营之后的活动，与"入营邮件接受/拒绝"(`is_agree` / `student_offer_submitted_at`)是两套独立的状态机。本期新增的 `accepted` 字段专门用于"黑客松入取"环节。

### 数据库变更
- 表 `dtlms_plan_offer` 新增 3 个字段:
  - `hackathon_score`    `numeric(5,2)`  夏令营评分（0~100）
  - `hackathon_comments` `text`           夏令营评语
  - `accepted`           `varchar(32)`    黑客松入取状态枚举（CHECK 约束限定 6 个值 + NULL）
- 新增字典类型 `hackathon_accepted_status`，7 个字典项:
  - `待录取`            (value=空字符串 '' 对应 NULL)
  - `未录取`            `declined`
  - `待定`              `pending`
  - `录取未发送`        `accepted_pending_send`
  - `录取已发送`        `accepted_sent`
  - `录取已确认`        `accepted_confirmed`
  - `录取已拒绝`        `accepted_rejected`
- 数据库脚本: `backend/sql/update20260630.sql`

### 后端变更
- `app/schemas/recruitment.py`
  - `CampOfferRecord` / `CampOfferUpsert` 新增 3 字段
  - 新增常量 `HACKATHON_ACCEPTED_VALUES` (6 个有效值)
  - 新增 3 个 `field_validator`:
    - `validate_hackathon_score` 范围 0~100，2 位小数
    - `validate_hackathon_comments` 自动 trim
    - `validate_accepted` 必须在字典允许值内（NULL/空允许）
- `app/services/postgres_state_store_query_recruitment.py`
  - 列表 SQL SELECT 增加 `hackathon_score` / `hackathon_comments` / `accepted` 3 列
- `app/services/postgres_state_store_sync.py`
  - `create_camp_offer` INSERT 增加 3 列 + 3 占位符
  - `update_camp_offer` UPDATE SET 增加 3 列 + 3 占位符

### 前端变更
- `frontend/src/api/recruitment.ts`
  - `CampOfferRecord` / `CampOfferUpsert` 新增 3 字段
- `frontend/src/views/recruitment/CampOfferListView.vue`
  - 列表新增 3 列：夏令营评分 / 夏令营评语 / 入取状态（位于"学生姓名"之后）
  - 入取状态列使用 el-tag 颜色显示（颜色取自字典 `color_type`）
  - 新增/编辑弹窗新增 3 个字段
  - 入取状态下拉项从字典 `hackathon_accepted_status` 加载

### 本期不做（后续迭代）
- [ ] 单行 [录取/不录取/待定] 操作按钮 + 二次确认弹窗
- [ ] 批量操作按钮 + 批量二次确认
- [ ] 状态变更自动写入时间戳/操作人 (`accepted_at` / `accepted_by` / `notified_at` / `responded_at`)
- [ ] 发送录取通知 UI（书院管理员）
- [ ] 学生端接受/拒绝 portal UI
- [ ] 状态机后端业务校验（仅前端校验，目前后端只做格式校验）

### 注意事项
- 本次改动 **后端**+**前端** 全部代码已备份，备份规则 `原文件名_yyyyMMddHHmmss.原后缀名.bak`
- 改数据库结构后请运行 `_extract_schema.py` 刷新 `database_schema.md`
