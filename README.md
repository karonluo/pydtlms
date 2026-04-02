# 博士生生命周期管理系统（DTLMS）

本仓库用于建设博士生生命周期管理系统，覆盖招生、入学、培养、学位、毕业和就业跟踪，并同时沉淀 RBAC、JWT、审计日志、Redis Sentinel、数据驾驶舱和跨系统集成能力。

## 当前交付内容

- `documents/系统详细设计文档.docx`：已根据需求基线生成的详细设计文档。
- `documents/images/`：详细设计文档引用的 SVG 与 PNG 图像资产。
- `documents/baseline/`：从 Markdown、Word、PDF、PPTX 抽取的需求基线文本。
- `backend/`：FastAPI 后端工程，包含配置、JWT/RBAC、模型、SQL 脚本，以及招生管理、学生管理等联调接口。
- `frontend/`：Vue3 + Element Plus 前端工程，已提供驾驶舱、招生管理、学生管理、培养、学位、系统治理六个视图。
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

将 `backend/.env.example` 复制为 `backend/.env` 后按实际环境调整。

### 3. 初始化数据库

推荐直接执行一键初始化脚本，脚本会自动完成建库、建表、视图、RBAC 和模拟数据导入：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py
```

如果只想快速检查导入结果，可执行：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py --summary
```

脚本内部会依次执行以下 SQL 文件：

1. `backend/sql/010_init_schema.sql`
2. `backend/sql/020_views.sql`
3. `backend/sql/030_seed_rbac.sql`
4. `backend/sql/040_runtime_store.sql`

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
- `backend/app/api/v1/`：面向前端联调的认证、驾驶舱、招生、学生、培养、学位与系统治理接口。
- `backend/app/services/management_service.py`：当前统一业务管理服务，优先从 PostgreSQL 读写，并保留本地 JSON 快照。
- `backend/app/services/postgres_state_store.py`：PostgreSQL 运行时持久化、关系表灌数与库初始化实现。
- `backend/app/tasks/reminders.py`：Celery 提醒任务骨架。
- `backend/sql/`：数据库与视图初始化脚本。

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
- `frontend/src/views/students/`：学生主档查询、新增、编辑、删除与状态管理。
- `frontend/src/views/training/`：培养过程、科研报告、外出研修规则视图。
- `frontend/src/views/degree/`：论文、盲审、答辩流水线视图。
- `frontend/src/views/system/`：安全、审计、集成和部署治理视图。

## 当前实现边界

- 已完成初始化项目骨架、数据库脚本、详细设计文档和图像资产生成。
- 已落地招生、学生、培养、学位、流程审批、系统治理等管理页面，并接入统一后端接口。
- 当前业务服务已支持 PostgreSQL 真实持久化，同时保留 JSON 快照作为离线回退与调试副本。
- 已导入一套完整模拟数据到 PostgreSQL，覆盖用户、学生、招生计划、报名申请、培养方案、科研报告、外出研修、论文、审批任务与审计日志。
- CLI 已支持登录、资料维护、学生删除、多模块查询与通用 API 调用；尚未把所有 Web 写操作都做成专用命令，但可通过 `/api` 命令覆盖调用。
- Redis Sentinel、更多外部系统同步、审批引擎细化和自动化测试仍可继续深化。

## 后续研发优先级建议

1. 将 PostgreSQL 运行时持久化继续下沉为完整 ORM Repository，减少整表回写。
2. 将登录日志、操作日志、同步日志全部接入前端可视化与检索。
3. 继续完成 Redis Sentinel、飞书和 OA 的真实消息与同步链路。
4. 补齐 Alembic 迁移、自动化测试和部署流水线。
