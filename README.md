# 博士生生命周期管理系统（DTLMS）

本仓库用于建设博士生生命周期管理系统，覆盖招生、入学、培养、学位、毕业和就业跟踪，并同时沉淀 RBAC、JWT、审计日志、Redis Sentinel、数据驾驶舱和跨系统集成能力。

## 最新更新（2026-05）

- 招生报名号与流程业务键已统一到新规则：`SH(申请年份+1)NNNN`。服务启动时会先做 PostgreSQL 修复，再把 recruitment 与 workflow 兼容表中的历史业务键一并校正。
- 后端启动流程已调整为“服务启动即完成修复与预热”：`backend/app/main.py` 会在 startup 中执行 PostgreSQL 修复并预热统一管理存储，不再等到首次登录后再冷启动。
- 学生门户在线申请页已固定为 V2 版本：入口仍是 `/portal/application`，对应前端页面为 `StudentPortalApplicationV2View.vue` 与 `applicationv2/` 分段表单组件。
- 浏览器标题已改为“上海人工智能实验室联培博士生申请系统”。
- 门户附件上传超时已统一提升到 5 分钟，降低弱网环境下的大文件上传失败概率。
- 服务端已禁用“启动时自动执行 SQL 脚本”能力；数据库结构更新必须先人工执行 `backend/sql/` 下对应脚本，再启动服务。

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

- 前端：Vue 3、TypeScript、Element Plus、Pinia、Vue Router、ECharts、Vite
- 后端：Python 3.12、FastAPI、psycopg、Pydantic Settings、Celery
- 数据库：PostgreSQL（当前代码以正式关系表 + Flowable 风格 workflow 兼容表为主）
- 缓存：Redis，支持 `single` 与 `sentinel` 两种模式，统一 Key 前缀 `CTDTLMS_`
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

当前代码不会在服务启动时自动执行任何 SQL 文件。推荐按下面顺序初始化：

1. 先人工执行 `backend/sql/` 下目标环境所需的 SQL 脚本。
2. 全新数据库建议按文件名顺序从基础脚本一路执行到当前最新增量脚本；存量数据库只执行尚未落库的增量脚本。
3. 确认正式 schema 已完成后，再执行下面的 Python 脚本灌入关系数据。

用于灌入当前内置演示数据的脚本：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py
```

如果只想快速检查灌数摘要，可执行：

```powershell
.\.venv\Scripts\python.exe backend\scripts\init_postgres.py --summary
```

说明：

- `init_postgres.py` 当前只会调用 `PostgresStateStore.save_state(...)` 向已存在的正式表灌入数据，不负责建表或自动补迁移。
- 如果 schema 未准备好，后端会直接报错并提示先手工执行 SQL。
- 生产或测试环境升级时，请优先执行 `backend/sql/` 中对应的增量脚本，例如当前仓库内的 `update20260506_1.sql`。

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

启动时还会自动执行两件事：

- 校正招生申请与 workflow 兼容表中的历史业务键。
- 预热统一管理存储，减少首次登录或首次打开管理页时的冷启动等待。

### 5. 启动前端

```powershell
Set-Location frontend
npm install
npm run dev
```

默认访问地址：`http://127.0.0.1:5173`

前端启动后进入登录页，可使用以下默认账号：

- 管理员：`admin / Admin@123456`
- 导师：`liu.ya / LiuYa@2026`
- 学位秘书：`zhou.qing / ZhouQing@2026`

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

### 5.1 登录与会话联调说明

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

### 5.2 一键启动脚本

根目录已提供自动化启动脚本，会先检查并清理端口占用，再启动后端和前端资源：

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

1. 默认静态托管模式：`start-system.ps1`
2. 打包预览模式：`start-system-preview.ps1`
3. 后端静态托管模式：`start-system-static.ps1`

#### 默认静态托管模式

`start-system.ps1` 当前默认会先构建 `frontend/dist`，再启动后端并由 FastAPI 直接托管静态前端：

```powershell
.\start-system.ps1
```

或者：

```powershell
.\start-system.cmd
```

特点：

- 默认会构建静态前端，而不是直接启动 Vite 开发服务器。
- 后端仍以 `uvicorn` 启动，并对外提供 API 与静态页面。
- 默认访问端口为后端 `8000`。

如需切换到前端热更新开发模式，请显式增加 `-Frontend` 参数：

```powershell
.\start-system.ps1 -Frontend
```

此时前端会走 `npm run dev`，默认端口为 `5173`。

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
.\.venv\Scripts\python.exe tools\dtmls_cli.py
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
.\.venv\Scripts\python.exe tools\dtmls_cli.py students stats
.\.venv\Scripts\python.exe tools\dtmls_cli.py system users
.\.venv\Scripts\python.exe tools\dtmls_cli.py delete D20240001
.\.venv\Scripts\python.exe tools\dtmls_cli.py show D20240001
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

## 运维章节

本章节面向测试、预发布、生产环境运维，统一说明数据库脚本执行、Linux 部署、代码上线、重启、核验与回滚。更细的长文档仍保留在 `CMMI3_Documents/`，README 这里给出直接可执行的入口。

### 1. 运维原则

- 服务启动时不会自动执行 `backend/sql/` 下的 SQL 文件。
- 数据库结构更新必须先人工执行目标 SQL，再启动或重启应用。
- 生产执行前必须先备份数据库，并确认本次代码版本与 SQL 脚本匹配。
- 如果本轮发布说明明确写明“无新增 SQL”，则不要额外补跑历史脚本。

### 2. SQL 脚本执行方式

仓库已提供脚本 [backend/scripts/execute_sql_file.py](backend/scripts/execute_sql_file.py)，用于按指定路径执行单个 SQL 文件，默认读取 `backend/.env` 或 `backend/.env.local` 中的 PostgreSQL 连接配置。

Windows 根目录执行示例：

```powershell
.\.venv\Scripts\python.exe backend\scripts\execute_sql_file.py backend\sql\update20260506_1.sql
```

Windows 指定数据库执行示例：

```powershell
.\.venv\Scripts\python.exe backend\scripts\execute_sql_file.py backend\sql\update20260506_1.sql --database test06
```

Linux 在 `backend/` 目录执行示例：

```bash
python3 scripts/execute_sql_file.py sql/update20260506_1.sql
python3 scripts/execute_sql_file.py sql/update20260506_1.sql --database test06
python3 scripts/execute_sql_file.py sql/update20260506_1.sql --dry-run
```

Linux 使用项目虚拟环境执行示例：

```bash
../.venv/bin/python scripts/execute_sql_file.py sql/update20260506_1.sql
```

说明：

- 脚本以单事务执行整份 SQL，执行异常会回滚。
- `--dry-run` 只校验文件可读、目标库名称和连接参数来源，不真正执行 SQL。
- 运行前需确认当前 `backend/.env` 中的 `POSTGRES_HOST`、`POSTGRES_PORT`、`POSTGRES_USER`、`POSTGRES_PASSWORD`、`POSTGRES_DB` 指向正确环境。

### 3. 数据库升级标准步骤

建议运维按以下顺序执行数据库升级：

1. 停止应用写入流量，或选择低峰窗口。
2. 备份目标数据库。
3. 确认当前版本需要执行的唯一 SQL 文件。
4. 使用 [backend/scripts/execute_sql_file.py](backend/scripts/execute_sql_file.py) 或现网标准 SQL 工具执行目标脚本。
5. 先做结构核验，再做数据抽样核验。
6. 核验通过后再启动或重启新版本服务。

如果是全新数据库初始化，建议顺序如下：

1. 先按文件名顺序执行 `backend/sql/` 中所需基础脚本与增量脚本。
2. 再执行 [backend/scripts/init_postgres.py](backend/scripts/init_postgres.py) 灌入关系数据。

### 4. Linux 部署与启动建议

推荐生产环境采用“前端构建产物 + FastAPI 统一托管”模式：

1. 拉取代码到服务器。
2. 在仓库根目录创建 `.venv` 并安装 `backend/requirements.txt`。
3. 在 [frontend](frontend) 执行 `npm install` 和 `npm run build`，生成 `frontend/dist`。
4. 配置 `backend/.env` 或 `backend/.env.local`。
5. 先执行目标 SQL 脚本，再启动后端服务。

Linux 常用命令示例：

```bash
cd /opt/pydtlms/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd frontend
npm install
npm run build

cd ../backend
../.venv/bin/python scripts/execute_sql_file.py sql/update20260506_1.sql --dry-run
../.venv/bin/python -m uvicorn app.main_static:app --app-dir . --host 0.0.0.0 --port 8000
```

如果采用前后端分离部署：

- `frontend/dist` 交由 Nginx 直接托管。
- FastAPI 使用 `app.main:app` 仅提供 API。
- Nginx 将 `/api/` 代理到后端服务。

### 5. 标准代码上线步骤

如果本轮是常规代码发布，建议按以下顺序执行：

1. 确认发布说明里本轮是否包含 SQL 变更。
2. 停止后端服务，必要时暂停外部访问入口。
3. 发布后端代码。
4. 发布前端构建产物，或在服务器重新执行 `frontend` 构建。
5. 如有 SQL 变更，先执行对应 SQL。
6. 启动新版本后端服务。
7. 观察启动日志，确认 PostgreSQL、Redis、workflow 预热与 schema 校验无异常。
8. 按清单完成管理端、门户、审批中心和通知能力核验。

如果发布说明明确属于“无新增 SQL 的代码发布”，则不要额外补跑历史脚本，直接按“发代码 -> 重启 -> 核验”执行即可。

### 6. 上线后核验重点

建议至少核验以下项目：

1. `/health`、`/docs`、管理端首页、学生门户首页均可打开。
2. 登录、退出登录、Redis 会话写入与失效正常。
3. 审批中心能看到待办，关键样本可继续审批。
4. 门户申请草稿保存、附件上传、正式提交正常。
5. 系统治理中的操作日志、通知发送日志、同步日志可正常查询。
6. 若本轮执行过 SQL，至少做一次结构核验和一次数据抽样核验。

### 7. 回滚建议

如上线后发现严重异常，建议按以下顺序回滚：

1. 停止当前新版本服务。
2. 回滚后端代码到上一个稳定版本。
3. 回滚前端静态资源到上一个稳定版本。
4. 启动旧版本服务。
5. 如果本轮包含数据库结构变更，不要直接整库回退，优先依据上线前备份和具体变更范围制定数据库回退方案。

### 8. 参考运维文档

更完整的运维说明可继续查看以下文档：

- [CMMI3_Documents/部署手册.md](CMMI3_Documents/部署手册.md)
- [CMMI3_Documents/20260429生产数据库更新执行清单.md](CMMI3_Documents/20260429生产数据库更新执行清单.md)
- [CMMI3_Documents/20260506本轮发布非SQL上线清单.md](CMMI3_Documents/20260506本轮发布非SQL上线清单.md)

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
- `backend/app/main_static.py`：静态前端托管入口，会挂载 `frontend/dist`、`portal-attachments` 和 `portal-brochures`。
- `backend/app/core/`：配置、数据库、JWT、RBAC、Redis Sentinel 与日志。
- `backend/app/models/`：系统治理、招生、培养与学位领域模型。
- `backend/app/api/v1/`：面向前端联调的认证、驾驶舱、招生、学生、培养、学位、系统治理与学生门户接口。
- `backend/app/services/management_service.py`：统一业务管理服务，启动时会延迟构造 `RuntimeManagementStore`，并提供 startup 修复与预热入口。
- `backend/app/services/postgres_state_store.py`：PostgreSQL 正式表/流程兼容表的查询、同步与灌数实现；当前不再负责自动执行 SQL 文件。
- `backend/app/tasks/reminders.py`：Celery 提醒任务骨架。
- `backend/sql/`：数据库与视图初始化脚本。

当前与学生门户直接相关的核心文件包括：

- `backend/app/api/v1/portal.py`：门户注册、登录、密码找回、计划列表、团队列表、申请保存/提交与附件上传接口。
- `backend/app/schemas/portal.py`：门户账号与学生档案契约。
- `backend/app/core/portal_security.py`：门户 JWT 签发与校验。
- `backend/sql/055_portal_personal_statement_v2.sql`：门户 V2 个人陈述与附件结构脚本。

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
- `frontend/src/views/portal/StudentPortalApplicationV2View.vue`：学生门户 V2 申请页入口。
- `frontend/src/views/portal/applicationv2/`：门户 V2 分段表单、章节校验与附件交互。
- `frontend/src/api/portal.ts`：学生门户前端 API、token 管理与长请求/附件上传超时配置。

## 当前实现边界

- 已完成初始化项目骨架、数据库脚本、详细设计文档和图像资产生成。
- 已落地招生、学生、培养、学位、流程审批、系统治理等管理页面，并接入统一后端接口。
- 已新增对外学生门户，支持学生自助注册、登录、找回密码、浏览招生计划、选择导师团队并在线填报档案。
- 学生门户当前采用“认证页 + 申请页”两段式流程，申请页支持科技感流程条、分组导航、折叠章节、快捷目录和回到顶部操作。
- 招生计划已补充 `brochure_image_url` 字段，学生端会根据选定计划展示对应招生简章图片。
- 当前业务服务以 PostgreSQL 正式表为唯一事实来源，并同步维护 Flowable 风格 workflow 兼容表。
- 已导入一套完整模拟数据到 PostgreSQL，覆盖用户、学生、招生计划、报名申请、培养方案、科研报告、外出研修、论文、审批任务与审计日志。
- 学生管理已补充团队主数据实体，学生新增/编辑时的导师和团队改为受控选择，并通过团队-导师约束避免脏数据。
- 团队主数据支持团队编码、负责人导师、团队导师集合、研究方向、团队状态、学生归属统计等治理能力。
- CLI 已支持登录、资料维护、学生删除、多模块查询与通用 API 调用；尚未把所有 Web 写操作都做成专用命令，但可通过 `/api` 命令覆盖调用。
- 认证链路已接入 Redis Sentinel 会话，支持登录、登出、会话失效校验与 401 回登录页。
- 培养管理模块已升级为治理页交互，覆盖培养方案、科研报告、外出研修的筛选、字典项、业务化按钮与批量删除。
- 学生门户当前以 V2 结构化申请为主，教育经历、实践经历、英语能力、家庭成员、成果经历、个人陈述与附件均走结构化 DTO。
- 门户附件上传当前采用 5 分钟超时配置，更适合弱网和大文件场景。
- Redis Sentinel、更多外部系统同步、审批引擎细化和自动化测试仍可继续深化。

## 后续研发优先级建议

1. 将 PostgreSQL 运行时持久化继续下沉为完整 ORM Repository，减少整表回写。
2. 将登录日志、操作日志、同步日志全部接入前端可视化与检索。
3. 继续完成 Redis Sentinel、飞书和 OA 的真实消息与同步链路。
4. 补齐 Alembic 迁移、自动化测试和部署流水线。
