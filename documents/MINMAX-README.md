# 博士生生命周期管理系统（DTLMS）项目理解文档

> 本文件由 Codex 助手在不修改任何源码的前提下阅读整个仓库后产出，目的在于帮助新成员快速建立项目地图、模块边界、关键流程与代码定位认知。
> 阅读对象：项目经理、新入职研发、运维、AI 代理或对该项目一无所知的协作者。
> 阅读时间：约 30 分钟。
> 仓库根目录：D:\pyproj\pydtlms

---

## 0. 一句话总结

DTLMS 是为上海人工智能实验室联培博士生量身打造的全生命周期管理平台，覆盖招生、培养、学位、毕业全流程，既包含内部管理后台（Vue3 + Element Plus + Pinia），也对外提供学生自助门户（注册、登录、在线填报、附件上传、流程跟踪），技术栈为 FastAPI + SQLAlchemy/psycopg + PostgreSQL + Redis Sentinel + Celery + JWT/RBAC。

仓库不只包含工程代码，还沉淀了一整套完整的软件工程资产：需求基线、SRS/EARS 文档、详细设计、PowerDesigner PDM、CMMI3 过程文件（部署手册、用户手册、单元测试用例、开发计划、发布清单）、AI 领域技能（SKILL.md）以及可直接打包发布的 Windows CLI 工具。

---

## 1. 顶层目录与资产分布

| 目录 | 主要作用 | 关键文件举例 |
| --- | --- | --- |
| `backend/` | FastAPI 后端工程主目录 | `app/main.py`、`app/api/v1/*.py`、`app/services/*.py`、`app/models/*.py`、`app/schemas/*.py`、`app/core/*.py`、`app/tasks/reminders.py`、`sql/`、`tests/`、`scripts/` |
| `frontend/` | Vue3 + Vite 前端工程 | `src/main.ts`、`src/router/index.ts`、`src/layouts/AppLayout.vue`、`src/views/**`、`src/components/**`、`src/api/**`、`src/stores/**`、`src/utils/**`、`vite.config.ts` |
| `documents/` | 文档与设计资产 | `系统详细设计文档.docx`、`产品需求规格说明书(EARS版本).docx`、`软件需求规格说明书(SRS版).docx`、`pydtlms-powerdesigner16_5-complete.pdm`、`portal-recruitment-er-diagram.svg`、`baseline/`、`plan/`、`UI设计/`、`workflow-engine-evolution.md`、`使用条款和隐私政策.md`、`需求覆盖率评估报告.md` |
| `tools/` | 研发/发布辅助工具 | `dtmls_cli.py`（Windows 端 CLI）、`build_dtmls_cli.bat`、`dtmls_cli.spec`、`export_powerdesigner_schema.py`、`extract_schema_from_db*.py`、`generate_design_assets.py`、`generate_srs_docx.py`、`generate_ears_prd_docx.py`、`generate_user_manual.py`、`powerdesigner_*.vbs`、`build/`、`dist/` |
| `CMMI3_Documents/` | CMMI3 级过程产物 | `部署手册.md`、`单元测试用例.md`、`用户手册/`（含截图）、多份日期化开发计划 |
| `需求/` | 原始需求与需求分析 | `原始需求资料/`（PDF、PPTX、XLSX、TXT）、`需求分析报告/` |
| `.github/`、`.vscode/` | 平台与 IDE 配置 |  |
| `.venv/`、`__pycache__/`、`frontend/dist/`、`frontend/node_modules/` | 构建/缓存产物 | 已 gitignored |
| 顶层 | 仓库级元文件 | `README.md`、`init_sql.sql`、`pytest.ini`、`dtmls_cli.spec`、`SQLPDSkill.md`、`start-system.ps1` / `.cmd`、`start-system-static.ps1` / `.cmd`、`start-system-preview.ps1` / `.cmd`、`tmp_origin_postgres_state_store_query.py`、`数据库分页TODO.md`、`数据库及前后端代码优化计划.md`、`修正runtime问题的计划表.md`、`.gitignore` |

> 顶层 .gitignore 已显式忽略 .venv/、.pytest_cache/、__pycache__/、backend/.env、frontend/node_modules/、frontend/dist/、documents/UI设计/、backend/app*.zip 等临时或敏感文件。

---

## 2. 技术栈与运行环境

### 2.1 前端
- Vue 3.5 + `<script setup>` + TypeScript 5.9
- Vite 8 构建，Rollup 自定义 `manualChunks`：把 echarts、@element-plus/icons-vue、element-plus（按 table/form/feedback 等子包）、axios、vue-router/pinia/vue 分别拆 vendor 块，提升首屏加载。
- Element Plus 2.13（自动按需引入：`unplugin-auto-import` + `unplugin-vue-components` + `ElementPlusResolver`）
- Pinia 3（`stores/auth.ts`、`stores/exportJobs.ts`）
- Vue Router 5（History 模式 + 多级权限守卫）
- ECharts 6（按需引入 `echarts/core` + `BarChart` / `PieChart` + 必要 Component）
- Axios 1.x（`api/http.ts` 统一拦截 401 跳登录）
- xlsx 0.18（用于系统用户/注册学生等导出导入解析）
- docx-preview（在线预览 Word 附件）
- 浏览器标题统一为「上海人工智能实验室联培博士生申请系统」
- 前端默认通过 Vite 代理 `/api -> 127.0.0.1:8000`，但生产态会走 FastAPI 静态托管（`main_static.py`）

### 2.2 后端
- Python 3.12、FastAPI、uvicorn（[standard]）
- SQLAlchemy 2.x + Alembic（但当前版本主要使用 `psycopg[binary]` 直连）
- psycopg 3.x（用 `dict_row` 取字典结构）
- pydantic-settings（从 `backend/.env` 加载配置）
- python-jose（JWT）、passlib[bcrypt]（实际多用 pbkdf2_sha256）
- redis 5.x + redis.sentinel（支持 single / sentinel 两种模式，统一 key 前缀 `CTDTLMS_`）
- celery 5.x（broker 与 backend 都用 Redis，队列名 `dtlms-reminders`，时区 `Asia/Shanghai`）
- httpx（前端开发代理）
- loguru（日志）
- openpyxl（Excel 导入导出）
- pypinyin（账号重名时生成拼音账号）
- svglib + reportlab + svgwrite（设计资产脚本里做 SVG ↔ PNG 互转）

### 2.3 数据库 / 缓存
- PostgreSQL 17（`47.117.107.23:15431/db_dtlms`，主库，含正式列式表 + 一组 `dtlms_runtime_*` JSONB 镜像 + 一组 `dtlms_wf_*` 仿 Flowable 兼容表）
- Redis Sentinel（`47.117.107.23:41104~41106`，哨兵名 `mymaster`）或单机模式可切换

### 2.4 通用约定
- API 前缀：`/api/v1`；Swagger：`/docs`；OpenAPI：`/openapi.json`；健康检查：`/health`
- 权限统一：基于 `dtlms_permissions` + `dtlms_role_permissions` + `dtlms_user_roles`，由 `app/core/rbac.py` 的 `require_permissions` 校验；超级管理员用 `*` 通配
- 审计：所有非 `portal`、`auth` 的后台写请求都会被 `app/main.py` 的 `record_backoffice_operation_audit` 中间件记录到 `dtlms_operation_logs`

---

## 3. 后端架构详解（backend/）

### 3.1 应用入口
- `backend/app/__init__.py`：包标记。
- `backend/app/main.py`（FastAPI 入口）：构建 `app`、挂 CORS（白名单由 `settings.allowed_origins_list` 提供）、按模块挂载 9 个子路由：`auth` / `dashboard` / `news` / `portal` / `recruitment` / `students` / `training` / `degree` / `system` / `workflow`。还实现了 `record_backoffice_operation_audit` 中间件（统一审计）、`handle_database_unavailable_error` 异常处理、可选的 `proxy_frontend_dev_server`（开发期转发到 Vite dev server），以及 `/health` 健康检查与 `on_startup` 启动钩子（仅做日志输出，不再自动执行 SQL 脚本）。
- `backend/app/main_static.py`：把 `frontend/dist` 挂到 `/`，并以 `SPAStaticFiles` 自定义 SPA fallback；把 `/recruitment/news/uploads`、`/portal-attachments`、`/portal-brochures` 三个目录分别挂为静态目录。

### 3.2 配置层（backend/app/core/）
- `config.py`：`Settings`（pydantic-settings），集中读取 `backend/.env(.local)`：应用名、环境、API 前缀、JWT、Postgres、Redis（`single`/`sentinel` 双模式，含 URL 编码、sentinel 节点解析、celery transport options）、SMTP、默认管理员账号、门户相关 URL（`portal_admissions_info_url`、`site_root_url`）等。
- `database.py`：构建 SQLAlchemy `engine` 与 `SessionLocal`，提供 `get_db` 依赖。
- `cache.py`：构造 `Sentinel` 或 `Redis` 客户端，提供 `get_cache_client()` 与 `build_cache_key()`。
- `security.py`：封装 `pbkdf2_sha256` 密码哈希、`OAuth2PasswordBearer`、`create_access_token` / `create_refresh_token` / `create_token_bundle`、`decode_token`（强校验 Redis 会话）、`record_user_login`、`update_system_user_password`、`logout_session`、`authenticate_system_user`、`get_user_principal_context`。
- `session_store.py`：基于 Redis 的 `auth/session/<sid>`、`auth/session/access/<sid>`、`auth/session/refresh/<sid>` 三段 Key，TTL 与 `access_token_expire_minutes` / `refresh_token_expire_minutes` 对齐；提供 `create_login_session`、`get_session_payload`、`validate_session`（刷新 `last_seen_at`）、`revoke_session`。
- `portal_security.py`：门户独立 JWT 签发与解码，`PORTAL_TOKEN_PREFIX = "portal-student:"`，`create_portal_access_token` / `decode_portal_access_token` / `resolve_portal_student_id`。
- `rbac.py`：`get_current_principal`（解码 + 装载 `Principal`）、`require_permissions(*permissions)` 工厂。
- `operation_audit_context.py`：用 `ContextVar` 跟踪已经写过操作日志的请求以避免审计中间件重复落库。
- `exceptions.py`：`DatabaseUnavailableError`（触发 503）。
- `logging.py`：用 `loguru` 输出 INFO 级彩色日志。

### 3.3 ORM 模型（backend/app/models/）
集中定义在 `models/__init__.py`，按业务域拆分：
- `base.py`：`DeclarativeBase`、`TimestampMixin`（`created_at`/`updated_at`）、`SoftDeleteMixin`（`is_deleted`）。
- `recruitment.py`：`RecruitmentPlan` / `ResearchField` / `RecruitmentApplication` / `ApplicationMaterial` / `QualificationReview` / `QualificationReviewLog` / `BackgroundAssessment` / `ReviewerAssignment` / `MaterialScore` / `InterviewGroup` / `InterviewSchedule` / `InterviewScore` / `WrittenExamScore` / `AdmissionDecision`。
- `system.py`：`User` / `Role` / `Permission` / `UserRole` / `RolePermission` / `LoginLog` / `OperationLog` / `DataSyncLog` / `NotificationDeliveryLog` / `NotificationTemplate` / `SystemConfig` / `DictType` / `DictData`。
- `training.py`：`Advisor` / `Team` / `TeamAdvisor` / `Student` / `StudentTeamHistory` / `StudentAdvisorHistory` / `ResearchProject` / `TrainingPlan` / `TrainingPlanVersion` / `ScientificReport` / `OutboundStudy` / `Achievement` / `Thesis` / `ThesisReview`。

> 模型覆盖正式表结构，但实际读写以 `PostgresStateStore`（基于 psycopg 直查）为主；ORM 主要用于声明结构与未来 Alembic 迁移。

### 3.4 Pydantic Schemas（backend/app/schemas/）
- `common.py`：`SelectOption`、`PaginationResponseBase`。
- `auth.py`：`TokenResponse`、`Principal`、`UserProfile` / `UserProfileUpdate` / `PasswordChangeRequest`，带手机号/邮箱字段校验。
- `contact.py`：手机号/邮箱正则、归一化与校验函数（`validate_phone_number` 等）。
- `identity.py`：18 位 / 15 位中国居民身份证校验（含校验位算法、出生日期合法性）。
- `dashboard.py`：`MetricCard`、`DashboardAlert`、`DashboardOverview`、`DashboardUndergraduateSchoolRankingResponse`、`DashboardUndergraduateSchoolGroupDistributionResponse`、`DashboardRecruitmentAdvisorChoiceDistributionResponse`、`DashboardUndergraduateSchoolStudentListResponse`。
- `news.py`：`NewsArticleRecord` / `NewsArticleUpsert` / `NewsArticleListResponse` / `NewsImageUploadResponse`。
- `portal.py`：最复杂的 schema 集合。定义注册/登录/找回密码请求与响应；学生主档 `PortalStudentRecord` 与子模型（教育经历、实践经历、英语能力、家庭成员、成果经历、申请偏好等）；`PortalApplicationUpsert`（V2 申请提交模型，含个人陈述、补充材料、申报说明、志愿偏好等）；`PortalApplicationDraftUpsert` / `PortalApplicationDraftSaveResponse`（草稿持久化）；`PortalApplicationSubmissionResponse`、`PortalImpersonationLaunchResponse` / `PortalImpersonationExchangeRequest`（书院管理员"模拟学生"）；`PortalWorkflowProgressSummary` / `PortalWorkflowStageItem`（门户流程条与方块）；`PortalPublicConfigResponse`、`PortalProfileOptionsResponse`、`PortalPlanListResponse`、`PortalTeamListResponse`、`PortalSessionResponse`；以及若干内联 helper（`_rewrite_portal_attachment_urls`、`_serialize_models` / `_parse_json_list` / `_parse_model_list`、`_normalize_education_items` / `_validate_portal_practice_rules`）负责 JSON ↔ 模型的双向转换。
- `recruitment.py`：招生计划 CRUD、报名申请 CRUD、Excel 导入导出、初始筛查/初筛确认/导师初筛已提交相关记录、下载模板等所有 Pydantic 模型。
- `student.py`：`StudentRecord` / `StudentUpsert` / `StudentLifecycleBoard` / `StudentStateItem` / `RegisteredPortalStudentRecord` / 各类导出任务模型 / 模拟学生相关请求与响应 / 研究中心（`CenterRecord`）的 CRUD 模型。
- `system.py`：系统治理（`RoleRecord` / `RoleUpsert` / `RoleDeletionPreviewResponse`、`SystemUserRecord` / `SystemUserUpsert`、`DictTypeRecord` / `DictDataRecord`、`AuditPolicyRecord`、`IntegrationRecord`、`OperationLogListResponse`、`SyncLogListResponse`、`NotificationDeliveryLogListResponse`、`SystemArchitecture`、`PermissionCatalogResponse`、`SystemStats`、`SystemOptionsResponse`、`BulkActionResponse` / `BulkDeleteRequest` 等）。
- `training.py`：`TrainingTask` / `TrainingWorkbench` / `DegreeWorkbench`、`TrainingPlanRecord` / `TrainingPlanUpsert`、`ScientificReportRecord` / `ScientificReportUpsert`、`OutboundStudyRecord` / `OutboundStudyUpsert`、`ThesisRecord` / `ThesisReviewRecord` / `ThesisReviewUpsert` 等。
- `workflow.py`：`WorkflowActionOption` / `WorkflowTaskRecord` / `WorkflowTaskUpsert` / `WorkflowTaskListResponse` / `WorkflowTaskActionRequest` / `WorkflowTaskActionLog` / `WorkflowTaskDetailResponse` 等。

### 3.5 API 路由（backend/app/api/v1/）
全部使用 `APIRouter`，挂载到 `main.py` 的 `/api/v1`。每个文件基本一致：先 `Depends(require_permissions(...))`，再调 service 层。

- `auth.py`：`POST /auth/token`（OAuth2PasswordRequestForm 登录）、`GET /auth/me`、`GET /auth/profile`、`PUT /auth/profile`、`POST /auth/change-password`、`POST /auth/logout`。
- `dashboard.py`：`/dashboard/overview`、`/dashboard/undergraduate-school-rankings[+ /students]`、`/dashboard/undergraduate-school-group-distribution[+ /students]`、`/dashboard/recruitment-advisor-choice-distribution[+ /students]`。
- `news.py`（路由前缀 `/recruitment/news`）：`/options/news-types`、列表/详情/CRUD、`/batch-publish`、`/batch-offline`、`/image-upload`。
- `recruitment.py`（路由前缀 `/recruitment`）：工作台 `/workbench`、统计 `/stats`、选项 `/options`、计划与申请 CRUD、Excel 导入导出、初筛确认/导师初筛列表、模拟学生导入、Broucher 图片上传等。
- `students.py`（路由前缀 `/students`）：学生生命周期看板 `/lifecycle`、学生主档 `/management`、注册学生 `/portal-registrations`、导出任务管理、研究中心 `/centers`（同步暴露旧路径 `/teams`）、以及 `import`、`import-template`、`export` 等。
- `training.py`：`/workbench`、`/stats`、`/options`、培养方案 `/plans`、科研报告 `/reports`、外出研修 `/outbound-studies`，全部支持批量删除。
- `degree.py`：`/workbench`、`/stats`、`/options`、论文 `/theses`、论文评审 `/reviews`。
- `system.py`：`/stats`、`/options`、`/permissions`、字典、角色、用户、审计策略、集成链路、操作日志、同步日志、通知发送日志、`/architecture`。
- `workflow.py`：`/stats`、`/options`、任务列表/详情/CRUD、`/tasks/{id}/actions`（审批动作）。
- `portal.py`（路由前缀 `/portal`）：门户学生注册/登录/找回/邮箱码登录/模拟学生交换、申请草稿/提交、附件上传/下载（支持多种类别与大小校验）、公开配置、计划/团队/新闻读取、模拟启动等。

### 3.6 Service 层（backend/app/services/）
- `management_service.py`：对外暴露的 `store` 是 `LazyRuntimeManagementStore`，第一次访问属性时通过 `Lock` 双重检查锁定构造 `RuntimeManagementStore` 单例；该单例由 8 个 Mixin 组合而成（`SystemMixin` / `AcademicMixin` / `StudentsMixin` / `RecruitmentMixin` / `PortalMixin` / `WorkflowMixin` / `CoreMixin`）。
- `management_service_shared.py`：跨 Mixin 共享的常量、helper、密码哈希、缓存 helper、字典 helper、Excel helper、邮件 helper 装载点。
- `management_service_core.py`：`__init__`、`_load_state`、`_record_operation_event` 等。
- `management_service_system.py`：系统治理相关业务（用户/角色/字典/审计/集成/同步）。
- `management_service_academic.py`：培训/学位工作台与统计、读 runtime 数据。
- `management_service_students.py`：学生主档、注册学生、研究中心、模拟学生、注册学生异步导出任务、Excel 导出模板。
- `management_service_recruitment.py`：招生计划、报名申请、导师初筛/初筛确认、报名材料、背景评估相关逻辑。
- `management_service_portal.py`：门户注册/登录/找回/草稿/提交/附件/邮箱码/模拟学生/个人空间相关。
- `management_service_workflow.py`：基于 `business_key` 的业务对象 → 流程动作映射，定义 `WORKFLOW_REQUIRED_PERMISSIONS`、`WORKFLOW_ROLE_ALIASES`，按角色放行审批动作并落 `WorkflowTaskActionLog`。
- `advisor_screening_submitted_service.py`：`list_advisor_screening_submitted_applications`，基于 PostgreSQL 直查"已提交"列表（仅支持关键词、报名号、姓名）。
- `initial_screening_confirmation_service.py`：`list_initial_screening_confirmation_applications`，基于 PostgreSQL 直查"初筛确认"列表。
- `dashboard_service.py`：薄包装层——把 service 里复杂方法转成 API 友好的同步函数。包含驾驶舱、注册学生导出任务、所有 CRUD、门户申请等函数。
- `email_service.py`：`NotificationEmailService`，封装 SMTP 发送；提供注册成功、注册验证码、登录验证码、改密通知、初筛通过/不通过、终止等模板；可异步派发；写 `dtlms_notification_delivery_logs`。
- `recruitment_excel_service.py` 与 `system_user_excel_service.py`：基于 `openpyxl` 的导入模板、导出模板、解析函数（处理表头、列名映射、拼音生成、列合并等）。
- `bootstrap_data.py` 与 `runtime_seed_data.py`：构建驾驶舱、训练工作台、注册学生模板等假数据。
- `postgres_state_store.py`：4 个 Mixin 组合的 `PostgresStateStore`（`Core` + `Seed` + `Sync` + `Query`）。
  - `postgres_state_store_core.py`：连接管理（`ensure_database` / `ensure_schema` / `_connect` / `_build_dsn`），禁用自动 SQL 初始化（schema 不存在时直接抛 `RuntimeError`，要求人工先执行 `backend/sql/` 下的脚本）；`save_state` 仅写正式表；`load_state` 默认返回 `None`（冷启动不再整库装载）。
  - `postgres_state_store_seed.py` 与 `sync.py`：种子数据回填、运行态同步相关代码。
  - `postgres_state_store_query.py` 及其 `_base` / `_dashboard` / `_recruitment` / `_students` / `_system` / `_training_degree` / `_workflow` / `_news` 子模块：分模块提供基于 psycopg 的查询函数（部分承担"数据库分页"改造的入口）。
  - 临时迁移脚本 `tmp_origin_postgres_state_store_query.py`（仓库根目录）：原查询逻辑的全量备份（仅供对比阅读）。
- `tasks/reminders.py`：Celery 应用 `pydtlms`，任务名 `dtlms.dispatch_deadline_reminder`（占位实现，返回 `{module, entity, status: 'queued'}`）。

### 3.7 异步任务
- `app/tasks/reminders.py`：定义 Celery 应用。仓库当前只在生产路径里"声明"了 Celery，实际可调度任务仍是占位。

### 3.8 SQL 脚本（backend/sql/）
按主题编号，从 `000_` 到 `060_`，并含若干日期化补丁。
- `000_create_database.sql`：创建 `db_dtlms`。
- `010_init_schema.sql`：核心表（用户/角色/权限/学生/团队/导师/培养/学位等）。
- `015_team_schema_migration.sql`、`016_business_key_migration.sql`、`017_workflow_flowable_schema.sql`、`018_recruitment_application_profile.sql`、`019_portal_student_and_brochure.sql`、`020_views.sql`（含 `dtlms_v_student_lifecycle_snapshot` 等视图）、`021_portal_auth_and_profile_fields.sql`、`022_portal_application_structured_schema.sql`、`023_runtime_team_store.sql`、`024_recruitment_plan_description.sql`、`025_portal_student_account_status.sql`、`026_portal_profile_photo_and_ethnic_dict.sql`、`027_portal_student_runtime_backfill.sql`、`028_user_profiles_relational.sql`、`029_student_team_runtime_backfill.sql`、`030_seed_rbac.sql`（10 个角色、24 个权限、角色↔权限矩阵）、`040_runtime_store.sql`（一组 `dtlms_runtime_*` JSONB 镜像表 + `dtlms_wf_*` 仿 Flowable 兼容表）、`050_dict_schema.sql`（字典主表 + CHECK 约束）、`051_governance_training_degree_columnar.sql`（治理、培养、学位列式化补齐，含 `dtlms_audit_policies` 等）、`052_portal_id_card_collage.sql`、`053_portal_application_draft_persistence.sql`（已废弃，但保留文件作为历史标记）、`054_portal_achievement_records_v2.sql`、`055_portal_personal_statement_v2.sql`、`056_seed_research_centers_and_advisors.sql`、`057_portal_education_graduation_certificate.sql`、`059_drop_runtime_tables.sql`（按反向顺序删除 runtime 镜像表）、`060_portal_student_candidate_no.sql`（`candidate_no` 不可变 trigger）、`060_workflow_menu_permission_split.sql`（新增 `workflow_center_menu:read`，调整 `workflow:read` 文案与模块）。
- `导师初筛已提交学生SQL脚本.sql`、`初筛确认SQL脚本.sql`：已纳入业务服务的查询 SQL 基线。
- `20260508update.sql`、`update20260506_1.sql`、`update20260506.sql`、`update20260511.sql` … `update20260612.sql` 等：日期化补丁记录每个上线窗口的数据库变更。
- `testquery.sql`：测试查询。
- `20260608.explicit.sql` / `20260608.sql` / `20260608_1.sql` 等：同日多次调整的细分版本。

### 3.9 单元 / 接口测试（backend/tests/）
`pytest.ini` 显式 `testpaths = backend/tests`。
- `conftest.py`：把 `BACKEND_DIR` 加入 `sys.path`。
- `tests/api/`：
  - `test_auth_dashboard_permissions.py`：基于 `monkeypatch` 替换 RBAC，验证 `*` 通配 / 缺权限拒绝。
  - `test_backoffice_operation_audit.py`：验证后台写操作自动落 `dtlms_operation_logs`。
  - `test_portal_api.py`：用 `TestClient` + `fake_rbac_decode_token` + 自定义 `RuntimeManagementStore` 单测门户注册、登录、改密、申请草稿等。
  - `test_recruitment_import_export.py`：Excel 导入/导出 模板。
  - `test_registered_portal_advisor_choices.py`：注册学生第一/第二志愿查询与导出。
  - `test_student_export.py`：学生导出。
  - `test_system_operation_logs_api.py`：操作日志 API。
  - `test_system_user_import_api.py`：系统用户 Excel 导入。
- `tests/unit/`：
  - `test_initial_screening_confirmation_service.py`
  - `test_management_service.py`
  - `test_postgres_state_store.py`
  - `test_rbac.py`
  - `test_recruitment_excel_service.py`
  - `test_redis_config.py`
  - `test_seed_research_centers_and_advisors.py`（含"欧阳万里→ouyangwanli"等拼音账号断言）
  - `test_system_user_excel_service.py`

### 3.10 一次性脚本（backend/scripts/）
按用途归类：
- 回填类：`backfill_missing_portal_attachment_urls.py`、`backfill_non_advisor_choice_advisors.py`、`backfill_portal_application_drafts.py`、`backfill_portal_choice_advisor_ids.py`、`backfill_portal_personal_statement_ai_fields.py`、`backfill_portal_students_to_relational.py`、`backfill_students_and_teams_to_relational.py`。
- 修复类：`check_portal_attachment_urls.py`、`cleanup_official_centers_and_advisors.py`、`fill_missing_english_certificate_urls.py`、`find_counted_via_graduation_school.py`、`find_k12_in_students.py`、`find_undergrad_edu2.py`、`fix_wrong_english_certificate_urls.py`、`locate_edu2_k12.py`、`report_missing_portal_attachment_gaps.py`。
- 数据生成 / 模拟：`generate_completed_thesis_sample.py`、`simulate_managed_workflows.py`。
- 同步 / 移植：`sync_advisor_profiles_from_test_to_prod.py`、`update_portal_student_fix_production.ps1`、`update_student_team_fix_production.ps1`。
- 查询 / 体检：`init_postgres.py`、`list_background_assessment_residuals.py`、`list_recruitment_applications_missing_choice_ids.py`、`normalize_recruitment_application_business_keys.py`、`get_registered_student_profile.py`、`get_school_students.py`、`get_undergrad_by_type.py`、`get_undergrad_school_rankings.py`、`execute_sql_file.py`、`query_sql_file.py`、`test_advisor_choice_db_query.py`、`test_registered_portal_advisor_choices.py`、`verify_advisor_choice_dashboard_consistency.py`、`seed_research_centers_and_advisors.py`。
- 烟雾脚本：`smoke_portal_application.ps1`。

> 仓库根目录还有 `tmp_origin_postgres_state_store_query.py` 和 `list_background_assessment_residuals.py`（这两个是 `backend/scripts/` 同名文件的早期版本/变体，便于回看）。

### 3.11 关键业务流（由代码反推）

1. 登录与会话
   - 前端 `LoginView.vue` → `authStore.login()` → `POST /api/v1/auth/token`。
   - 后端 `authenticate_system_user` → `record_user_login` → `create_token_bundle`（创建 Redis 会话 + JWT access/refresh）。
   - 退出时 `POST /auth/logout` → `decode_token` 校验 → `revoke_session`。
2. 管理端写操作审计
   - `main.py` 中 `record_backoffice_operation_audit` 中间件：除 `portal/*`、`auth/*` 之外的所有非 GET/HEAD/OPTIONS 请求都会在响应返回前自动写入 `dtlms_operation_logs`，并尝试匹配"导出注册学生"、"发布新闻"等业务化描述。
3. 数据库分页改造
   - 业务侧"已优先走数据库分页"的列表包括：workflow 任务、招生申请、操作日志、同步日志、系统用户、学生主档、团队、招生计划、培养方案、科研报告、外出研修。详见 `数据库分页TODO.md`。
4. 运行时 / 正式表双写收敛
   - `修正runtime问题的计划表.md` 列出 R-001~R-005：例如"招生申请审核不通过后注册学生列表状态不一致"（R-001）已修复；角色删除前的预览与阻断（已修复）；后台写操作统一审计（已修复）。
5. 门户申请（V2）
   - 学生进入 `/portal/application` → `StudentPortalApplicationV2View` 渲染流程条 + `PortalApplicationV2Form` + 8 个分段 section。
   - 每段支持本地增删；保存草稿走 `POST /api/v1/portal/applications/draft`；最终提交走 `POST /api/v1/portal/applications`。
   - 附件上传走 `POST /api/v1/portal/attachments/...`，`PORTAL_ATTACHMENT_*_TIMEOUT_SECONDS = 300`，`PORTAL_AUTH_TIMEOUT_SECONDS = 10`，`PORTAL_FORM_TIMEOUT_SECONDS = 60`。
   - 书院管理员可以通过"模拟学生"动作生成一次性模拟码（`PortalImpersonationLaunchResponse`），再在新窗口完成"模拟码→真实 portal token"的交换（`consume_portal_impersonation_code`）。
6. Flowable 兼容
   - `dtlms_wf_*` 表由 `017_workflow_flowable_schema.sql` 一次性创建；`documents/workflow-engine-evolution.md` 描述"未来可视化建模 + 兼容层"的演进路径。
7. 去 runtime 化
   - `059_drop_runtime_tables.sql` 已提供清理脚本；计划表 `修正runtime问题的计划表.md` 中以 Phase 0~6 推进。

---

## 4. 前端架构详解（frontend/）

### 4.1 关键文件
- `package.json`：vue 3.5、vue-router 5、pinia 3、element-plus 2.13、echarts 6、axios 1.14、xlsx 0.18、docx-preview；脚本 `dev` / `build` / `preview`。
- `vite.config.ts`：插件、auto-import、components 解析器、manualChunks（echarts/element-plus 子包/vendor-axios/vendor-vue 拆分），dev 与 preview 都代理 `/api → 127.0.0.1:8000`。
- `tsconfig.json` / `tsconfig.app.json` / `tsconfig.node.json`：TS 5.9 复合配置。
- `index.html`：标题为「上海人工智能实验室联培博士生申请系统」。
- `src/main.ts`：注册 Pinia、Router；启动时尝试 `authStore.hydrateSession()`，完成后再 `app.mount('#app')`。
- `src/App.vue`：仅一个 `<router-view />`。
- `src/style.css`：定义 CSS 变量（`--brand`、`--brand-strong`、`--bg` 等）、统一按钮 / 表格 / 对话框 / 表单 / 抽屉 / 分页样式，强制覆盖 Element Plus 主题色。
- `.env.example`：`VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1`。
- `dist/`：构建产物，已 gitignored。

### 4.2 路由与权限（src/router/）
- `router/index.ts`：
  - 公开路由：`/login`、`/portal`、`/portal/home`、`/portal/application`（其中 `applicationv2` 路径重定向到 `application`）。
  - 受保护路由：放在 `AppLayout` 下，包含驾驶舱、招生、注册学生、学生主档、研究中心、培训、学位、流程中心、字典、系统治理、用户、角色、审计、集成、操作日志、通知日志、同步日志、个人空间等。
  - `beforeEach` 守卫：
    1. 根路径 `/` 重定向到 `/portal`。
    2. 门户 token 校验：调用 `getPortalProfile()` 验证；未登录跳到 `/portal`；并支持 `impersonation_code` 模拟登录。
    3. 后台 token 校验：未登录则跳 `/login?redirect=...`。
    4. 权限检查 `hasGrantedPermission`，通配符 `*` 通过。
  - `afterEach` 把 `document.title` 改为 `<系统名>-<页面名>`。
- `router/menuAccess.ts`：列出所有菜单路径与所需权限，提供 `hasGrantedPermission` / `resolveFirstAccessibleMenuPath` / `resolveAccessibleRoutePath`。

### 4.3 状态管理（src/stores/）
- `auth.ts`：Pinia store，封装登录/登出/会话恢复、theme_color 持久化（localStorage）、post-login 重定向、当前用户/权限/角色。
- `exportJobs.ts`：轮询注册学生异步导出任务（10 秒间隔），维护任务列表、已读/未读计数、下载中状态。

### 4.4 公共 API 客户端（src/api/）
- `http.ts`：axios 实例，默认 baseURL `VITE_API_BASE_URL`、默认超时 30 分钟，请求拦截注入 `dtlms-access-token`，响应拦截捕获 401 跳 `/login`。
- `common.ts`：通用类型 `SelectOption`、`PaginationParams`、`PagedResponse`。
- `auth.ts` / `dashboard.ts` / `degree.ts` / `news.ts` / `portal.ts` / `recruitment.ts` / `students.ts` / `system.ts` / `training.ts` / `workflow.ts`：每个文件按业务域提供 `xxx(params)` 函数与对应 TS 类型。门户单独使用 5 分钟附件上传超时（`PORTAL_ATTACHMENT_UPLOAD_TIMEOUT = 300000`）。

### 4.5 工具与组合式（src/utils/、src/composables/）
- `chinaResidentId.ts`：与后端 `schemas/identity.py` 对应的前端校验（含 18 位校验位计算）。
- `contactValidation.ts`：手机号/邮箱校验、归一化、错误信息。
- `dictTag.ts`：构建 `value/color` 映射，决定 el-tag 颜色。
- `portalAlerts.ts`：在学生门户使用自定义 alert/confirm 样式，注入 `portal-alert-styles` 全局样式。
- `composables/useServerPagination.ts`：服务端分页状态（currentPage、pageSize、total），提供 `reset` / `sync(total)` / `handleCurrentChange` / `handleSizeChange`。

### 4.6 布局与组件
- `layouts/AppLayout.vue`：左侧侧边栏（按权限隐藏菜单）、顶部用户区、面包屑、消息铃铛（注册学生导出任务），是整个管理后台的壳。
- `components/dashboard/KpiCard.vue`：指标卡。
- `components/common/AttachmentPreviewActions.vue`：统一附件查看/下载/缩放/全屏按钮 + docx-preview 在线预览。
- `components/recruitment/RecruitmentApplicationReviewDrawer.vue`：管理端招生申请审核抽屉。
- `components/recruitment/RecruitmentPortalApplicationDrawer.vue`：门户端招生申请详情抽屉。
- `components/table/TableRowActions.vue`：通用行操作下拉菜单（主要/更多两组）。

### 4.7 业务视图（src/views/）
- `auth/LoginView.vue`：登录。
- `dashboard/DashboardView.vue`：驾驶舱（生命周期、招生、培养、学位、流程指标卡 + 本科院校排名/分布 + 招生志愿分布的 ECharts 图）。
- `recruitment/RecruitmentWorkbenchView.vue`：管理端"招生工作台"，根据 `route.meta.section` 切换到招生计划/申请池/导师初筛/初筛确认。
- `recruitment/AdvisorScreeningSubmittedView.vue`：导师初筛已提交列表（新增独立页面）。
- `recruitment/NewsManagementView.vue`：新闻管理（增/删/改/查、批量发布/下线、富文本编辑器、图片上传）。
- `students/StudentsView.vue`：根据 `section` 切换"学生主档"/"注册学生管理"/"研究中心管理"。
- `training/TrainingView.vue`：根据 `section` 切换培养方案/科研报告/外出研修。
- `degree/DegreeView.vue`：根据 `section` 切换论文/盲审。
- `workflow/WorkflowCenterView.vue`：审批中心（任务列表 + 详情抽屉 + 动作执行）。
- `system/SystemView.vue`：系统治理（用户/角色/审计策略/集成/操作日志/通知日志/同步日志）。
- `system/DictView.vue`：字典类型/字典数据。
- `portal/StudentPortalAuthView.vue`：门户注册/登录/找回/模拟码交换。
- `portal/StudentPortalApplicationV2View.vue`：V2 申请页（流程条 + 表单壳 + 阶段摘要）。
- `portal/applicationv2/PortalApplicationV2Form.vue`：表单主控组件。
- `portal/applicationv2/sections/PortalBasicSection.vue`、`PortalApplicationSection.vue`、`PortalEducationSection.vue`、`PortalPracticeSection.vue`、`PortalEnglishSection.vue`、`PortalFamilySection.vue`、`PortalAchievementSection.vue`、`PortalStatementSection.vue`：8 个分段章节。
- `home/PortalHomeView.vue`：门户首页（方块加箭头展示申请阶段 + 计划列表 + 公告）。
- `profile/ProfileView.vue`：个人空间（基础信息/修改密码/主题色）。

### 4.8 前端约定的关键术语
- 门户 = 公开的学生自助申请网站；与管理后台走两套 token、两套 RBAC。
- 注册学生 = 在门户注册过账号但还没完成申请的学生；和学生主档是不同概念。
- 研究中心 = 同时也叫团队（`teams` 别名路由），后端统一以 `dtlms_teams` 存储。
- AILABMGT = 内部角色编码；用户可见页面统一显示为"书院管理员"。
- 候选人号 candidate_no 一旦生成不可二次修改（trigger 保证）。
- 业务键 business_key 是 `recruitment_application` / `scientific_report` / `outbound_study` / `thesis` 与流程实例的连接键。

---

## 5. 工具链（tools/）

- `dtmls_cli.py` + `dtmls_cli.spec` + `build_dtmls_cli.bat` + `dtmls_cli.ini` + `dtmls_cli.session.json` + `dist/dtmls_cli.exe`：基于 `psycopg` + `urllib` 的 Windows 端命令行客户端，支持：
  - 登录（带密码安全输入，Windows 用 `msvcrt`）
  - `/help`、`/login`、`/logout`、`/whoami`、`/profile`、`/profile set`、`/passwd`
  - `/students stats|list|show|delete`
  - `/recruitment stats|plans|applications`
  - `/training stats|plans|reports|outbound`
  - `/degree stats|theses|reviews`
  - `/workflow stats|tasks`
  - `/system stats|users|roles|audit-policies|integrations|operation-logs|sync-logs|architecture`
  - 通用 `/api METHOD PATH [key=value ...]`
  - 已通过 PyInstaller 单文件打包为 `dist/dtmls_cli.exe`。
- `export_powerdesigner_schema.py`：从 PostgreSQL 拉取 `public.dtlms_*` 表（排除 `dtlms_runtime_*` 与 `dtlms_schema_migrations`），生成 PowerDesigner 16.5 原生 `.pdm`、`reverse-engineering.sql`、导入说明（详见 `documents/pydtlms-powerdesigner16_5-*`）。
- `extract_schema_from_db.py` / `extract_schema_from_db_v3.py`：早期/新版 schema 抽取脚本。
- `convert_schema_json_to_md.py` / `convert_schema_json_to_md_v2.py`：JSON → Markdown。
- `generate_table_descriptions.py`：在已有 schema markdown 上推断字段含义。
- `generate_design_assets.py`：用 `svgwrite` + `reportlab` + `PIL` 生成 SVG 流程图并转 PNG，再嵌入到设计文档。
- `generate_srs_docx.py` / `generate_ears_prd_docx.py`：基于现有 Markdown 自动生成 Word 格式的 SRS / EARS PRD。
- `generate_user_manual.py`：用 Selenium + Edge 截图各页面，最终生成《用户手册》docx（已存在 `CMMI3_Documents/用户手册/` 下）。
- `powerdesigner_create_sample_pdm.vbs` / `powerdesigner_validate_model.vbs`：PowerDesigner 自动化脚本（生成最小样本 PDM、打开 PDM 校验）。
- `build/`、`dist/`：构建与发布产物。
- `__pycache__/`：解释器缓存。

---

## 6. AI 领域技能（backend/ai/skills/）

每个 skill 都是一个独立的 `SKILL.md`（YAML frontmatter + Markdown 正文），便于迁移到任何支持 SKILL 格式的 AI/Agent 平台。

- `README.md`：本目录总览。
- `backend-management-dialog-style/SKILL.md`：后台对话框、确认框、提醒框的统一样式。
- `recruitment-workbench-operations/SKILL.md`：招生计划、报名申请、资格审核、面试安排、录取决策工作台维护。
- `student-master-data-and-teams/SKILL.md`：学生主档、团队、导师归属、状态板维护。
- `training-degree-lifecycle/SKILL.md`：培养方案、科研报告、外出研修、论文主档、盲审意见、学位阶段维护。
- `workflow-approval-maintenance/SKILL.md`：基于 `business_key` 的审批流驱动，Flowable 兼容运行态维护。
- `system-governance-admin/SKILL.md`：系统用户、角色、字典、审计、集成、日志治理。
- `sql-powerdesigner-pdm-generation/SKILL.md`：根据 PostgreSQL schema 生成 PowerDesigner 16.5 PDM 文档并校验。

> 仓库根 `SQLPDSkill.md` 是该 skill 的快捷入口说明。

---

## 7. 文档资产（documents/ 与 CMMI3_Documents/）

### 7.1 顶层 documents/
- `系统详细设计文档.docx`、`产品需求规格说明书(EARS版本).docx`、`产品需求规格说明书(EARS版本)-更新版.docx`、`软件需求规格说明书(SRS版).docx`：由 `tools/generate_design_assets.py`、`generate_ears_prd_docx.py`、`generate_srs_docx.py` 自动生成的设计与规格文档。
- `portal-recruitment-er-diagram.svg`：门户-招生 ER 图。
- `pydtlms-powerdesigner16_5-complete.pdm` / `.pdb` / `pydtlms-powerdesigner16_5-import.md` / `pydtlms-powerdesigner16_5-reverse-engineering.sql`：PowerDesigner 设计产物。
- `baseline/`：从 Word / PDF / PPTX 抽取的需求基线文本（含 6 个 `*.extracted.md` + `requirements_manifest.md` + `招生模块_media/`）。
- `images/`、`EARS_IMAGES/`、`SRS_IMAGES/`、`UI设计/`（已 gitignored）：各类插图与原 UI 设计稿。
- `plan/完成博士生招生环节开发计划.md`：分阶段开发计划。
- `GPT5mini.md`：AI 自动生成的项目概览（含 .env 的 `POSTGRES_DB=test25` 提醒）。
- `使用条款和隐私政策.md`：隐私政策。
- `需求覆盖率评估报告.md`：按 10 大功能模块评估当前覆盖率约 70%。
- `workflow-engine-evolution.md`：流程引擎演进说明（Flowable 兼容层的当前与未来）。
- `test25_schema.json` / `test25_schema.md` / `test25_schema_full.json` / `test25_schema_full.md` / `test25_schema_descriptions_block.md`：历史 schema 抽取/转换产物。

### 7.2 CMMI3_Documents/
- `部署手册.md`：Linux systemd + Nginx 部署指南，包含默认（FastAPI 统一托管）与前后端分离两种模式。
- `单元测试用例.md`：本轮缺陷修复/关键增强的单元测试用例清单。
- `解决性能问题计划.md`：首轮性能扫描结论与整改计划（如门户忘记密码/改密从 `_save()` 整库写到单条 upsert，提速约 90 倍）。
- `填报功能研发计划.md`：门户在线申请 V2 拆段填报表单的研发阶段清单。
- `数据库列式化改造清单.md`：列出 13+ 张正在使用或已计划下线的 runtime JSONB 表。
- `产品需求跟踪表.xlsx`、`需求跟踪表20260522.xlsx`、`需求跟踪表20260522说明.docx` / `.md`：需求与交付跟踪表。
- `20260427学生填报需求开发计划.md` / `20260429生产数据库更新执行清单.md` / `20260506本轮发布非SQL上线清单.md` / `20260514学生申请全流程开发计划.md` / `20260527导师初筛需求开发计划.md` / `20260603新闻信息管理开发计划.md` / `20260606_志愿字段两阶段收敛记录.md` / `20260611_application_draft_attachment_backfill_plan.md` / `20260611_initial_screening_confirmation_query_plan.md` / `20260612导师初筛已提交标签开发计划.md`：按时间顺序的开发计划 / 发布清单 / 字段收敛记录。
- `生产环境门户学生数据修复上线步骤.md` / `生产环境学生模块列式化改造上线步骤.md`：上线步骤文档。
- `image/20260429生产数据库更新执行清单/`、`image/20260514学生申请全流程开发计划/`、`image/解决性能问题计划/`：各文档引用的截图。
- `用户手册/博士生生命周期管理系统用户手册.docx` + `用户手册/images/`（按角色：admin / advisor / reviewer / hrbp / party / secretary / dormitory_guard / interviewer / login 等 30+ 张截图）。

### 7.3 需求/
- `原始需求资料/2026.04.27 需求会议单.txt` / `博士生招生环节流程.txt` / `招生模块.pptx` / `招生系统字段.xlsx` / `资料审核名单.xlsx` / `专项博士生管理系统平台建设方案-1212.pdf`：原始需求材料。
- `需求分析报告/博士生生命周期管理系统分析报告.docx` / `.md` / `.pdf`：基于斯坦福七步法 + Ontology + Palantir 方法论的需求分析报告（含 10 类核心实体、8 项主流程、3 类审批链、6 类角色、6 项量化指标）。
- `需求分析报告/博士生生命周期管理系统_功能模块清单.xlsx`：10 个一级模块的清单。
- `需求分析报告/招生系统-学生填报内容.md`：学生填报字段结构化分析的开发基线。

---

## 8. 启动 / 部署 / 工具脚本

- 顶层 `start-system.ps1`（最通用）：可启动 FastAPI 开发模式 + Vite dev server，并支持 `InstallDependencies` / `UseStaticFrontend` / `EnableBackendFrontendProxy` 等开关；可自动清理端口占用、输出本机/局域网访问地址。
- `start-system-static.ps1`：只构建 `frontend/dist` 并用 `app.main_static` 启动。
- `start-system-preview.ps1`：构建 + `app.main`（带 reload）+ Vite `preview`。
- 三个 `.cmd` 包装上述 `.ps1`，便于 Windows 一键启动。
- `pytest.ini`：`testpaths = backend/tests`。
- `dtmls_cli.spec`：PyInstaller 单文件打包配置。

---

## 9. 重要约定与注意事项

1. 不再自动执行 SQL 脚本：`ensure_schema()` 在 `public.dtlms_users` 不存在时会直接报错，要求人工先执行 `backend/sql/` 下对应脚本。运维需按 `CMMI3_Documents/20260429生产数据库更新执行清单.md` 等文档的顺序逐次升级。
2. 数据库分页改造：`数据库分页TODO.md` 列出已切换为数据库分页与待切换的列表，当前是数据库分页 + 内存分页并存的过渡期，未来需进一步收敛。
3. 运行时镜像 / 正式表：现阶段正式表与 `dtlms_runtime_*` JSONB 表并存，目标是正式表为唯一事实来源。`修正runtime问题的计划表.md` 与 `数据库列式化改造清单.md` 提供执行路线。`059_drop_runtime_tables.sql` 提供最终清理脚本。
4. 审计日志：
   - 后台写请求（除 portal/auth）走 `record_backoffice_operation_audit` 中间件。
   - 门户 API 走 `_record_portal_api_operation`（位于 `api/v1/portal.py` 内），操作人记为 `portal-student-<id>`。
   - 业务代码里若已经手动写过 `OperationLog`，应通过 `operation_audit_context.mark_manual_operation_log()` 通知中间件跳过重复落库。
5. JWT 与 Redis Sentinel：
   - `JWT_SECRET_KEY`、`ALLOWED_ORIGINS` 必须从 `.env` 注入；`REDIS_MODE=sentinel` 时必须配置 `REDIS_HOST_LIST`。
   - 会话包含 access/refresh 两段 Redis Key，TTL 与 `ACCESS_TOKEN_EXPIRE_MINUTES` / `REFRESH_TOKEN_EXPIRE_MINUTES` 对齐。
6. 候选人号（candidate_no）：
   - 一旦写入不可修改（`060_portal_student_candidate_no.sql` 提供 trigger）。
   - 业务键 `business_key` 与 `candidate_no` 历史上同义，`016_business_key_migration.sql` 已统一。
7. 菜单权限矩阵：在 `030_seed_rbac.sql` 内一次写入；新增权限需要：
   - 1) 更新 SQL；
   - 2) 更新 `frontend/src/router/menuAccess.ts`；
   - 3) 更新后端权限字符串（`require_permissions`）。
8. CMMI3 过程资产：
   - 发布前要跑完 `CMMI3_Documents/部署手册.md` + `CMMI3_Documents/单元测试用例.md` + `pytest backend/tests`。
   - 上线清单按日期目录 `2026MMDD*.md` 维护。
9. AI Skill 入口：根目录 `SQLPDSkill.md` 是 `sql-powerdesigner-pdm-generation` 的快速入口，标准入口是 `backend/ai/skills/*/SKILL.md` 或 `.github/skills/*/SKILL.md`。
10. DTLMS CLI（`dtmls_cli.exe`）：
    - 与后端同源（PostgreSQL + HTTP API）但更轻量；可用于排障、批量删除学生、快速查询统计。
    - `dtmls_cli.ini` 与可执行文件必须放同目录；当前仓库已带一份示例 `tools/dtmls_cli.ini` + `tools/dist/dtmls_cli.exe`。
11. UI 资源：
    - `frontend/dist/` 是构建产物，gitignored。
    - `documents/UI设计/` 是历史 UI 设计稿，gitignored。
    - 静态上传目录 `frontend/public/portal-attachments/`、`frontend/public/recruitment/news/uploads/` 也是 gitignored 的运行时产物。

---

## 10. 推荐阅读路径

1. 理解业务：先读 `README.md` → `需求/需求分析报告/博士生生命周期管理系统分析报告.md` → `documents/使用条款和隐私政策.md`。
2. 理解数据：`init_sql.sql`（仓库根的 Navicat 完整 dump）→ `backend/sql/010_init_schema.sql` → `backend/sql/020_views.sql` → `documents/pydtlms-powerdesigner16_5-complete.pdm`（PowerDesigner 设计）。
3. 理解后端：`backend/app/main.py` → `app/core/*` → `app/api/v1/*` → `app/services/management_service.py` → `app/services/postgres_state_store*.py`。
4. 理解前端：`frontend/src/main.ts` → `router/index.ts` → `layouts/AppLayout.vue` → `views/dashboard/DashboardView.vue` → `views/portal/StudentPortalApplicationV2View.vue`。
5. 理解过程：`CMMI3_Documents/部署手册.md` + `CMMI3_Documents/单元测试用例.md` + 日期化 `2026MMDD*.md`。
6. 理解演化方向：`documents/workflow-engine-evolution.md` + `数据库分页TODO.md` + `数据库及前后端代码优化计划.md` + `修正runtime问题的计划表.md`。

---

## 11. 一句话复述：仓库能给谁解决什么问题？

> 给上海人工智能实验室提供一个能完整跑通"招生计划发布 → 候选人注册并在线填报（V2 分段结构 + 附件 + 邮箱码） → 资料审核/背景评估/导师初筛/初筛确认/入营面试 → 录取/学位授予"全流程的可观测、可治理的数字化平台，配套管理后台（RBAC + 操作审计 + 字典 + 流程中心 + 系统治理）、学生自助门户、CMMI3 过程资产、PowerDesigner 数据库设计、AI 领域技能、Windows 端 CLI 与完整 SQL 演进脚本，能在 PostgreSQL + Redis Sentinel 之上独立完成开发、联调、上线和日常运维。
