# 博士生生命周期管理系统（DTLMS）

本仓库用于建设博士生生命周期管理系统，覆盖招生、入学、培养、学位、毕业和就业跟踪，并同时沉淀 RBAC、JWT、审计日志、Redis Sentinel、数据驾驶舱和跨系统集成能力。

## 当前交付内容

- `documents/系统详细设计文档.docx`：已根据需求基线生成的详细设计文档。
- `documents/images/`：详细设计文档引用的 SVG 与 PNG 图像资产。
- `documents/baseline/`：从 Markdown、Word、PDF、PPTX 抽取的需求基线文本。
- `backend/`：FastAPI 后端工程，包含配置、JWT/RBAC、模型、SQL 脚本，以及招生管理、学生管理等联调接口。
- `frontend/`：Vue3 + Element Plus 前端工程，已提供驾驶舱、招生管理、学生管理、培养、学位、系统治理六个视图。
- `tools/generate_design_assets.py`：一键再生 SVG、PNG 和详细设计文档的脚本。

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

建议按以下顺序执行 SQL 脚本：

1. `backend/sql/000_create_database.sql`
2. `backend/sql/010_init_schema.sql`
3. `backend/sql/020_views.sql`
4. `backend/sql/030_seed_rbac.sql`

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

前端启动后会自动使用内置演示管理员账号获取 JWT，无需手工登录。默认落地页为“招生管理”。

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

## 后端说明

- `backend/app/main.py`：FastAPI 应用入口。
- `backend/app/core/`：配置、数据库、JWT、RBAC、Redis Sentinel 与日志。
- `backend/app/models/`：系统治理、招生、培养与学位领域模型。
- `backend/app/api/v1/`：面向前端联调的认证、驾驶舱、招生、学生、培养、学位与系统治理接口。
- `backend/app/services/management_service.py`：当前招生计划、报名申请、学生主档的管理服务与示例存储。
- `backend/app/tasks/reminders.py`：Celery 提醒任务骨架。
- `backend/sql/`：数据库与视图初始化脚本。

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
- 已落地招生管理与学生管理两条可操作链路，可直接进行计划、申请、学生主档的新增、编辑、删除和筛选。
- 当前管理数据仍由后端内存服务承载，后续需替换为真实 PostgreSQL 持久化、审批流引擎与外部系统 API。
- 培养、学位、系统治理页面仍需继续按同样方式深化为完整管理链路。

## 后续研发优先级建议

1. 先把 PostgreSQL 实库建好并跑通 SQL 脚本。
2. 将当前内存管理服务替换为真实 ORM 查询与服务层逻辑。
3. 继续完成培养模块、学位模块的端到端联调。
4. 接入 Redis Sentinel、飞书和 OA 的真实消息与同步链路。
5. 补齐自动化测试、迁移脚本和部署流水线。
