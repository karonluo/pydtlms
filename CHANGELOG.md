# CHANGELOG

> 重大变更与功能说明。新增放在最上面，按时间倒序。
> 本文件由 Codex 在重大功能/字段变更后维护。

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
