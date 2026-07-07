# AGENTS.md —— pydtlms 项目协作约束



本文件约束整个仓库目录树。子目录下的 AGENTS.md 会覆盖/细化这里的规则。



## 1. 文件编码：全程 UTF-8



本仓库所有源代码文件均为 UTF-8 编码。修改或新增任何文件时，必须保持 UTF-8。



### 1.1 Python 读写

- 读：`open(path, encoding="utf-8")`

- 写：`open(path, "w", encoding="utf-8")`

- 控制台需要直显中文时：

  ```python

  import sys, io

  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

  ```



### 1.2 PowerShell 写文件

- 不要使用 `>`/`Out-File`/`Set-Content`（默认编码为系统 ANSI/GBK）写带中文的文件。

- 如必须用 PowerShell：

  - `Set-Content -Encoding UTF8`

  - `[System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))`

- 涉及多字节字符或大段中文 patch 时，优先改用 Python 脚本（见 1.3），避免 here-string 转义陷阱。



### 1.3 复杂中文 patch 策略

- 一律用 Python 脚本以 UTF-8 落盘：

  - 用 `chr(0xXXXX)` 或 Python 字符串字面量构造中文

  - `open(path, "w", encoding="utf-8").write(content)`

- 提交前用 `python -m py_compile <file>`（Python 文件）或对应编译/类型检查命令验证未损坏。



### 1.4 常见字符陷阱

- 中文 “已” 的正确 Unicode 是 `0x5df2`，**不是** `0x6628`（`0x6628` 是 “昨”）。任何写盘后必须验证。

- 中文 “是/否” 不要写成 “已/否”（语义错误）。

- 修改含中文的 SQL/Python/Vue 文件后，必须重新读出原文核对，避免静默的编码替换错误。



## 2. 代码改动通用规范

- 修改完成后，必须至少跑一次：

  - Python：`python -m py_compile <file>`

  - 前端：在 wsl/bash 下 `node node_modules/vue-tsc/bin/vue-tsc.js -p tsconfig.app.json --noEmit`（PowerShell 运行 vue-tsc 会卡住）

- 不要在编码层面绕弯：发现乱码或字符替换错误，先修编码再继续功能工作。







## 3. 功能改动后同步文档



任何功能性改动 (新增页面 / 接口 / 字段 / 导入逻辑 / 表单等) 完成后, 必须同步更新两个文档。



### 3.1 修改文件

- **AGENTS.md** (本文件): 如有新的全局约束 / 过程约定, 在此追加一节 (例如 “功能改动后同步文档”、“代码改动前先备份”等)。

- **`documents/博士生生命周期管理功能模块说明.xlsx`** (功能模块说明表): 追加本轮改动涉及的功能点。



### 3.2 xlsx 追加规则

- **不要重写** 原表, 只追加新行。

- **不要改动** 原表的列顺序 / 合并单元格 / 样式。

- **顺序号** 按“最低级别功能”连续编号 (与原表末尾接齐), 不要重复、不要跳号。

- **完成状态** 仅使用三个值: `已完成` / `未完成` / `进行中`。

- **不使用** Excel 公式 / VBA / 完全匿名 / 外部链接 (不要在 xlsx 里用 README 表面讲没有的列头)。

- 表顶保持原状: 序号 | 一级模块 | 二级功能 | 三级功能 | 功能说明 | 完成状态。



### 3.3 修改前先备份

- 任何改动 .py / .vue / .ts / .sql 等代码文件前, **先备份** 一份到同目录 `<file>.YYYYMMDDHHMMSS.bak` (UTF-8 复制, 保留原文件时间戳)。

- 例: `Copy-Item D:\pyproj\pydtlms\backend\app\services\camp_offer_import_service.py D:\pyproj\pydtlms\backend\app\services\camp_offer_import_service.py.20260706182357.bak`

- 验证: 改动后跑 `python -m py_compile <file>` (后端) 或 `vue-tsc --noEmit` (前端, 在 wsl/bash 下) 。



### 3.4 步骤顺序 (以次出现为例)

1. 备份 → 2. 改后端 (schema / service / API) → 3. 改前端 (TS / Vue) → 4. 验证 (编译 / typecheck) → 5. 追加 xlsx 行 → 6. 如有全局约束变更, 同步更新 AGENTS.md。



## 4. 代码改动前先备份 (明确要求)



每次修改代码文件前必须备份。本条与 3.3 重复, 但作为独立章节明确出来, 避免被志愿者心理默认选项过滤掉。


## 5. 入营名单 /recruitment/camp-offers 的字段可扩展约定

- 后端 store 层在 dtlms_plan_offer 表上新增过滤/统计字段时, 应同时更新:
  1. `backend/app/services/postgres_state_store_query_recruitment.py` 的 `_build_camp_offer_where` (用于 list_camp_offers_page + count_camp_offer_stats 共享 where)
  2. `count_camp_offer_stats` 的 base 子查询 (把字段 SELECT 出来) 与聚合 SELECT (加 COUNT(*) FILTER)
  3. `backend/app/services/management_service_recruitment.py` 的 `get_camp_offers` / `count_camp_offer_stats` / `export_camp_offers` 签名与转发
  4. `backend/app/services/dashboard_service.py` 的 `get_camp_offer_list` / `get_camp_offer_stats` 签名与转发
  5. `backend/app/schemas/recruitment.py` 的 `CampOfferStats` 字段 + docstring
  6. `backend/app/api/v1/recruitment.py` 的 `/camp-offers` + `/camp-offers/stats` + `/camp-offers/export` 三个 endpoint 的 Query 参数
- 前端 TypeScript 类型 (`frontend/src/api/recruitment.ts`) 必须同步更新:
  - `CampOfferStats` 类型
  - `listCampOffers` / `getCampOfferStats` / `exportCampOffers` 函数 params 类型
- 前端视图 (`frontend/src/views/recruitment/CampOfferListView.vue`):
  - `FilterState` 类型与 `filters` reactive 初值同步加字段
  - `buildFilterParams` / `handleResetFilters` / `handleExportList` 同步把字段加入/重置
  - 筛选区 UI 同步加 <el-form-item> (位置跟随需求变更)
  - KPI `CampOfferKpi.key` 联合类型 + `KPI_DEFINITIONS` 数组同步加卡
  - KPI 栅格 `grid-template-columns` 列数按卡片总数取最大公约数 (1/2/4/5/...) 排布, 多余格留空
- 修改后按 3.4 顺序执行: 备份 → 后端 → 前端 → 验证 (py_compile + vue-tsc) → 追加 xlsx 行 → 必要时同步 AGENTS.md。
