# 博士生生命周期管理系统（DTLMS）

本仓库用于建设博士生生命周期管理系统，覆盖招生、入学、培养、学位、毕业和就业跟踪，并同时沉淀 RBAC、JWT、审计日志、Redis Sentinel、数据驾驶舱和跨系统集成能力。

## 最新更新（2026-04）

- 新增对外学生门户，面向考生提供注册、登录、找回密码、查看招生计划、选择导师团队和在线填写学生档案能力。
- 学生门户入口已拆分为两个页面：`/portal` 用于注册登录与密码找回，`/portal/application` 用于计划选择与档案填写。
- 学生档案页已升级为科技感表单界面，包含顶部流程箭头、左侧章节导航、可折叠章节面板、右下角快捷目录与回到顶部入口。
- 学生门户报名页已完成结构化改造，教育经历、实践经历、英语能力、家庭成员、论文/获奖、个人陈述与附件上传均已接入结构化 DTO、结构化子表和附件归档表。
- 门户真实端到端链路已完成联调验证：注册、登录、附件上传、提交申请、再次查看与流程发起均已跑通；可直接使用 `backend/scripts/smoke_portal_application.ps1` 做本机烟雾验证。
- 招生计划新增招生简章图片字段 `brochure_image_url`，管理端招生计划维护页已支持展示该字段，学生端会随所选计划展示不同简章图片。
- 前端最新构建已通过；当前仍存在 Vite 大 chunk 告警，但不影响使用。

## 当前交付内容

- `documents/系统详细设计文档.docx`：已根据需求基线生成的详细设计文档。
- `documents/images/`：详细设计文档引用的 SVG 与 PNG 图像资产。
- `documents/baseline/`：从 Markdown、Word、PDF、PPTX 抽取的需求基线文本。
- `backend/`：FastAPI 后端工程，包含配置、JWT/RBAC、模型、SQL 脚本，以及招生管理、学生管理等联调接口。
- `frontend/`：Vue3 + Element Plus 前端工程，已提供驾驶舱、招生管理、学生管理、团队管理、培养、学位、系统治理六个业务视图，以及对外学生门户页面。
- `tools/generate_design_assets.py`：一键再生 SVG、PNG 和详细设计文档的脚本。
- `tools/dtmls_cli.py`：DTLMS 命令行工具，支持登录、查询、删除学生、斜杠命令菜单和通用 API 调用。
- `tools/dist/dtmls_cli.exe`：已编译的 Windows 可执行版 CLI，需与同目录 INI 配置一起使用。

## 目录结构

```text
pydtlms/
├─ backend/
│  ├─ app/
│  ├─ sql/
│  ├─ .env.example
│  └─ requirements.txt
├─ documents/
│  ├─ baseline/
│  ├─ images/
│  └─ 系统详细设计文档.docx
├─ frontend/
├─ tools/
│  ├─ dtmls_cli.py
│  ├─ dtmls_cli.ini
│  ├─ build_dtmls_cli.bat
│  └─ dist/
│  └─ generate_design_assets.py
└─ README.md
```

## 技术栈约定

- 前端：Vue3、TypeScript、Element Plus、Pinia、Vue Router、ECharts
- 后端：Python 3、FastAPI、SQLAlchemy、Pydantic Settings、Celery
- 数据库：PostgreSQL 17 以下版本
- 缓存：Redis 7.4.2 Sentinel，统一 Key 前缀 `CTDTLMS_`
- 权限：RBAC + JWT
- 审计：登录日志、操作日志、同步日志

## 快速开始

### 1. Python 虚拟环境

当前工作区已创建根目录 `.venv`。如需重新安装依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### 2. 后端配置

后端运行时只会读取 `backend/.env` 和 `backend/.env.local`，不会直接读取 `backend/.env.example`。因此修改示例文件后，还需要同步生成实际配置文件。

推荐流程：

```powershell
Copy-Item backend/.env.example backend/.env
```

Redis Sentinel 相关配置示例：

```text
REDIS_HOST_LIST=47.117.107.23:41104,47.117.107.23:41105,47.117.107.23:41106
REDIS_PASSWORD=Pass@@word123!
REDIS_SENTINEL_NAME=mymaster
REDIS_KEY_PREFIX=CTDTLMS_
```

当前联调已验证：上述 Sentinel 地址可发现 master `47.117.107.23:41102`，并可完成登录会话的创建、读取与注销。

### 3. 初始化数据库

推荐直接执行一键初始化脚本，脚本会自动完成建库、建表、视图、RBAC 和 PostgreSQL 运行态数据同步：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py
```

如果只想快速检查同步结果，可执行：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py --summary
```

脚本内部会依次执行以下 SQL 文件：

1. `backend/sql/010_init_schema.sql`
2. `backend/sql/015_team_schema_migration.sql`
3. `backend/sql/016_business_key_migration.sql`
4. `backend/sql/017_workflow_flowable_schema.sql`
5. `backend/sql/019_portal_student_and_brochure.sql`
6. `backend/sql/020_views.sql`
7. `backend/sql/030_seed_rbac.sql`
8. `backend/sql/040_runtime_store.sql`
9. `backend/sql/050_dict_schema.sql`

## 流程引擎演进约定

当前审批流程仍由后端内置流程定义驱动，但底层存储已开始向 Flowable 风格靠拢，新增了流程模型、流程定义、运行时执行、运行时任务、运行时变量、身份关联和历史实例等表。

这一层的目标不是马上替换成完整 BPM 引擎，而是先把以下边界稳定下来：

- 流程定义、流程实例、执行实例、任务实例分层存储。
- 业务对象统一通过 `business_key` 与流程实例关联。
- 历史轨迹和运行态分离，便于未来接入 BPMN 设计器与流程审计。
- 后续可以在不推翻现有业务接口的前提下，引入 BPMN.js 做流程建模与发布。

现阶段可将其理解为“Flowable 风格的存储兼容层”，后续如果继续演进，优先顺序建议是：流程模型管理、流程定义发布、节点条件表达式、可视化设计器接入。

### 4. 启动后端

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload
```

启动后可访问：

- OpenAPI：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

### 5. 启动前端

```powershell
Set-Location frontend
npm install
npm run dev
```

默认访问地址：`http://127.0.0.1:5173`

前端启动后进入登录页，可使用以下默认账号：

- 管理员：`admin / Admin@123456`
- 导师：`mentor.demo / Mentor@123456`

### 5.0 学生门户入口

学生门户与管理端前端共用同一套 Vite 服务，入口如下：

- 学生认证页：`http://127.0.0.1:5173/portal`
- 学生申请页：`http://127.0.0.1:5173/portal/application`

当前门户流程说明：

- 新考生可在 `/portal` 完成注册，注册信息为手机号、邮箱、姓名、身份证号和密码。
- 已注册考生可在 `/portal` 登录，也可在同页通过“找回密码”重设密码。
- 登录成功后进入 `/portal/application`，先选择一个正在执行的招生计划，再按章节填写结构化申请内容、上传相关附件并提交申请表。
- 学生申请页右下角已提供“目录”和“回到顶部”快捷入口，适配长表单场景。

本地烟雾联调脚本：

- `backend/scripts/smoke_portal_application.ps1`：用于验证门户注册、登录、计划/团队读取、简历上传、申请提交、再次查看与流程发起。

### 5.2 登录与会话联调说明

本轮认证改造已经接入 Redis 会话存储，前后端联调遵循以下机制：

- 登录成功后，前端优先跳转到 `redirect` 指定页面；如果是会话中断后重新登录，则恢复到中断前页面。
- 路由守卫会在访问受保护页面前记录目标地址，避免登录后只回到默认首页。
- Axios 在收到 `401` 时会清理本地 token，并自动回到登录页，同时保留当前地址用于重新登录后的恢复。
- 后端 `POST /api/v1/auth/logout` 会撤销 Redis 中的会话，旧 token 会立即失效。
- 如果 Redis Sentinel 不可用，登录接口会快速返回 `503 Redis session store unavailable`，不会无限挂起。

本地已完成的 HTTP 级验证包括：

- 管理员账号成功完成用户名密码认证。
- access token 与 refresh token 均可成功签发与解码。
- 注销后再次使用旧 token 访问，立即返回 `401 Session expired, please login again`。

提示：当前工具链可完整验证 HTTP 登录与 Redis 会话失效，但不支持自动点击浏览器控件，因此“登录后页面跳转”和“会话超时回跳”是通过前端路由守卫、拦截器和接口联调共同确认，而不是录制式浏览器自动化。

### 5.1 一键启动脚本

根目录已提供自动化启动脚本，会先检查并清理端口占用，再分别启动后端和前端：

```powershell
.\start-system.ps1
```

或者直接使用：

```powershell
.\start-system.cmd
```

默认检查并清理以下端口：

- 后端：`8000`
- 前端：`5173`

如需首次安装依赖，可执行：

```powershell
.\start-system.ps1 -InstallDependencies
```

当前根目录一共提供三种启动模式：

1. 开发模式：`start-system.ps1`
2. 打包预览模式：`start-system-preview.ps1`
3. 后端静态托管模式：`start-system-static.ps1`

#### 开发模式

用于日常开发，前端走 `npm run dev`，后端走 `uvicorn --reload`：

```powershell
.\start-system.ps1
```

或者：

```powershell
.\start-system.cmd
```

特点：

- 前端为 Vite 开发服务器，支持热更新。
- 后端为 FastAPI 开发模式，代码改动后自动重载。
- 默认端口：前端 `5173`，后端 `8000`。

#### 打包预览模式

用于验证 `frontend/dist` 的实际运行效果，会先执行前端构建，再启动后端和 `vite preview`：

```powershell
.\start-system-preview.ps1
```

或者：

```powershell
.\start-system-preview.cmd
```

可选参数：

- `-InstallDependencies`：首次安装依赖。
- `-SkipFrontendBuild`：跳过前端重新构建，直接预览现有 `dist`。
- `-BackendPort`：修改后端端口，默认 `8000`。
- `-FrontendPort`：修改预览端口，默认 `4173`。

示例：

```powershell
.\start-system-preview.ps1 -SkipFrontendBuild
.\start-system-preview.ps1 -FrontendPort 4174
```

特点：

- 前端运行的是打包产物，不再是开发服务器。
- 无需 Nginx，即可本机验证 `dist`。
- 默认前端预览地址：`http://127.0.0.1:4173`

#### 后端静态托管模式

用于用单一服务同时提供 API 和前端静态页面。脚本会先构建 `frontend/dist`，再由 FastAPI 直接托管：

```powershell
.\start-system-static.ps1
```

或者：

```powershell
.\start-system-static.cmd
```

可选参数：

- `-InstallDependencies`：首次安装依赖。
- `-SkipFrontendBuild`：跳过前端重新构建。
- `-Port`：修改统一访问端口，默认 `8000`。

示例：

```powershell
.\start-system-static.ps1 -SkipFrontendBuild
.\start-system-static.ps1 -Port 8080
```

特点：

- 前后端共用同一个端口。
- 应用首页和学生门户页面都由 FastAPI 直接提供静态文件。
- 默认应用地址：`http://127.0.0.1:8000`
- OpenAPI 仍可通过：`http://127.0.0.1:8000/docs`

### 6. 重新生成详细设计文档与图像

```powershell
.\.venv\Scripts\python.exe tools\generate_design_assets.py
```

### 7. 使用 CLI 工具

CLI 配置文件与可执行文件应放在同一个目录中。仓库中已提供：

- Python 版本：[tools/dtmls_cli.py](tools/dtmls_cli.py)
- INI 配置：[tools/dtmls_cli.ini](tools/dtmls_cli.ini)
- Windows 可执行版：[tools/dist/dtmls_cli.exe](tools/dist/dtmls_cli.exe)
- 可执行版配置：[tools/dist/dtmls_cli.ini](tools/dist/dtmls_cli.ini)

直接运行 Python 版：

```powershell
\.venv\Scripts\python.exe tools\dtmls_cli.py
```

直接运行 exe 版：

```powershell
Set-Location tools\dist
.\dtmls_cli.exe
```

如需重新打包 exe：

```powershell
Set-Location tools
.\build_dtmls_cli.bat
```

CLI 当前已实现的能力包括：

- 交互式 REPL，直接启动后会持续等待输入命令。
- 直接启动 exe 或 Python 脚本后，会一直停留在命令提示符等待输入，直到执行退出命令。
- 在交互模式下按下 `/` 无需回车，会立即弹出快捷菜单。
- 快捷菜单支持使用上下方向键移动选中项，按回车立即执行当前命令，按 Esc 返回命令输入。
- 登录、退出登录、查看当前身份、查看和修改个人资料、修改密码。
- 学生、招生、培养、学位、流程、系统管理等模块的只读查询与统计。
- 支持直达删除命令：`delete 学号`。
- `/student delete 学号`：已登录时优先走后端 API，未登录时回退数据库直删。
- `dtmls_cli 空格命令 空格参数` 可直接执行，例如 `dtmls_cli students stats`、`dtmls_cli system users`。
- `api METHOD PATH [key=value ...]`：通用接口透传，可覆盖尚未做成专用子命令的 Web 操作。

默认联调账号：

- 用户名：admin
- 密码：Admin@123456

常用示例：

```text
按下 /
使用 ↑ ↓ 选择菜单项
回车执行
login admin
whoami
students stats
students list status=在校
student show D20240001
student delete D20240001
recruitment plans
workflow tasks status=待处理
system users
api GET /system/users
api POST /students/management student_no=D20260001 full_name=张三 status=在校 advisor_name=刘亚 team_name=智能制造团队 degree_type=工程博士 enrollment_year=2026
```

非交互兼容方式：

```powershell
\.venv\Scripts\python.exe tools\dtmls_cli.py students stats
\.venv\Scripts\python.exe tools\dtmls_cli.py system users
\.venv\Scripts\python.exe tools\dtmls_cli.py delete D20240001
\.venv\Scripts\python.exe tools\dtmls_cli.py show D20240001
Set-Location tools\dist
.\dtmls_cli.exe students stats
.\dtmls_cli.exe system users
```

说明：

- `delete 学号` 会先显示学生信息，再要求输入 `Y/N` 二次确认。
- exe 版会优先从 exe 所在目录读取 `dtmls_cli.ini`。
- 登录相关命令依赖后端接口可访问，因此需要先启动 FastAPI 服务。
- 数据库直删命令不依赖后端服务，但会直接修改 PostgreSQL 中的学生与关联记录。
- Windows 可执行文件位置为 [tools/dist/dtmls_cli.exe](tools/dist/dtmls_cli.exe)。

## CLI 交互约定（供后续系统和 AI 协作复用）

后续如果要为其他系统继续开发同类 CLI，可以默认沿用以下交互约定：

1. 启动程序且不带参数时，进入常驻交互模式，持续等待用户输入命令。
2. 在交互模式下，按下 `/` 不需要回车，立即弹出命令快捷菜单。
3. 快捷菜单必须支持上下方向键选择、回车执行、Esc 返回，避免只输出一段静态帮助文字。
4. 常用查询和管理动作应同时支持直达命令模式，即 `程序名 空格 命令 空格 参数` 可直接执行。
5. 交互模式和直达命令模式应尽量共用同一套命令分发逻辑，避免两套实现不一致。
6. 对高风险操作，例如删除，必须保留二次确认。
7. 对未封装成专用命令的 Web 功能，可保留一个通用 `api METHOD PATH [key=value ...]` 入口作为兜底能力。

## 后端说明

- `backend/app/main.py`：FastAPI 应用入口。
- `backend/app/core/`：配置、数据库、JWT、RBAC、Redis Sentinel 与日志。
- `backend/app/models/`：系统治理、招生、培养与学位领域模型。
- `backend/app/api/v1/`：面向前端联调的认证、驾驶舱、招生、学生、培养、学位、系统治理与学生门户接口。
- `backend/app/services/management_service.py`：当前统一业务管理服务，优先从 PostgreSQL 读写，并保留本地 JSON 快照。
- `backend/app/services/postgres_state_store.py`：PostgreSQL 运行时持久化、关系表灌数与库初始化实现。
- `backend/app/tasks/reminders.py`：Celery 提醒任务骨架。
- `backend/sql/`：数据库与视图初始化脚本。

当前与学生门户直接相关的核心文件包括：

- `backend/app/api/v1/portal.py`：门户注册、登录、密码找回、计划列表、团队列表、申请提交接口。
- `backend/app/schemas/portal.py`：门户账号与学生档案契约。
- `backend/app/core/portal_security.py`：门户 JWT 签发与校验。
- `backend/sql/019_portal_student_and_brochure.sql`：门户学生表与招生简章图片字段迁移脚本。

## CLI 命令概览

- `/help`：显示命令菜单。
- `/login [用户名]`：登录，密码会安全输入。
- `/logout`：清除本地会话文件。
- `/whoami`：查看当前登录身份。
- `/profile`：查看个人资料。
- `/profile set key=value ...`：更新个人资料，支持 `full_name`、`phone_number`、`email`、`theme_color`。
- `/passwd`：交互修改当前用户密码。
- `/students stats`：查看学生统计。
- `/students list [keyword=] [status=] [advisor=]`：列出学生。
- `/student show 学号`：查看指定学生。
- `/student delete 学号`：删除指定学生。
- `/recruitment stats|plans|applications`：查询招生模块。
- `/training stats|plans|reports|outbound`：查询培养模块。
- `/degree stats|theses|reviews`：查询学位模块。
- `/workflow stats|tasks`：查询流程待办模块。
- `/system stats|users|roles|audit-policies|integrations|operation-logs|sync-logs|architecture`：查询系统治理模块。
- `/api METHOD PATH [key=value ...]`：通用接口调用。

## 前端说明

- `frontend/src/layouts/AppLayout.vue`：整体框架、侧边导航、顶部状态区。
- `frontend/src/views/dashboard/`：数据驾驶舱与指标总览。
- `frontend/src/views/recruitment/`：招生计划、报名申请、状态筛选、计划维护与申请维护。
- `frontend/src/views/students/`：学生主档与团队主数据治理页，支持学生新增编辑时的导师/团队受控选择、团队维护、负责人配置与批量删除。
- `frontend/src/views/training/`：培养方案、科研报告、外出研修三类治理页，支持查询、状态筛选、字典选择、单删与批量删除。
- `frontend/src/views/degree/`：论文、盲审、答辩流水线视图。
- `frontend/src/views/system/`：安全、审计、集成和部署治理视图。
- `frontend/src/views/portal/StudentPortalAuthView.vue`：学生门户注册、登录、找回密码页面。
- `frontend/src/views/portal/StudentPortalApplicationView.vue`：学生门户申请表页面，含计划选择、导师团队选择、分段档案填写、快捷目录和回到顶部交互。
- `frontend/src/api/portal.ts`：学生门户前端 API 与 token 管理。

## 当前实现边界

- 已完成初始化项目骨架、数据库脚本、详细设计文档和图像资产生成。
- 已落地招生、学生、培养、学位、流程审批、系统治理等管理页面，并接入统一后端接口。
- 已新增对外学生门户，支持学生自助注册、登录、找回密码、浏览招生计划、选择导师团队并在线填报档案。
- 学生门户当前采用“认证页 + 申请页”两段式流程，申请页支持科技感流程条、分组导航、折叠章节、快捷目录和回到顶部操作。
- 招生计划已补充 `brochure_image_url` 字段，学生端会根据选定计划展示对应招生简章图片。
- 当前业务服务已支持 PostgreSQL 真实持久化，同时保留 JSON 快照作为离线回退与调试副本。
- 已导入一套完整模拟数据到 PostgreSQL，覆盖用户、学生、招生计划、报名申请、培养方案、科研报告、外出研修、论文、审批任务与审计日志。
- 学生管理已补充团队主数据实体，学生新增/编辑时的导师和团队改为受控选择，并通过团队-导师约束避免脏数据。
- 团队主数据支持团队编码、负责人导师、团队导师集合、研究方向、团队状态、学生归属统计等治理能力。
- CLI 已支持登录、资料维护、学生删除、多模块查询与通用 API 调用；尚未把所有 Web 写操作都做成专用命令，但可通过 `/api` 命令覆盖调用。
- 认证链路已接入 Redis Sentinel 会话，支持登录、登出、会话失效校验与 401 回登录页。
- 培养管理模块已升级为治理页交互，覆盖培养方案、科研报告、外出研修的筛选、字典项、业务化按钮与批量删除。
- 学生门户相关接口测试与前端构建已通过，但学生门户档案字段目前仍以门户申请场景为主，尚未完全替代管理端完整学生主档治理流程。
- Redis Sentinel、更多外部系统同步、审批引擎细化和自动化测试仍可继续深化。

## 后续研发优先级建议

1. 将 PostgreSQL 运行时持久化继续下沉为完整 ORM Repository，减少整表回写。
2. 将登录日志、操作日志、同步日志全部接入前端可视化与检索。
3. 继续完成 Redis Sentinel、飞书和 OA 的真实消息与同步链路。
4. 补齐 Alembic 迁移、自动化测试和部署流水线。
