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


























### 4.1 备份策略 (硬约束, 不可绕过)





1. **修改任何代码文件前必须先备份**: 后端 *.py, 前端 *.vue / *.ts, 数据库 *.sql, markdown 文档, xlsx, 一切代码与文档文件.





2. **备份命名规则 (唯一)**:


   原文件名(不含后缀)_日期时间(yyyyMMddHHmmss).原后缀名.bak


   例 1: backend/app/services/foo.py -> backend/app/services/foo_20260707194228.py.bak


   例 2: frontend/src/views/Bar.vue -> frontend/src/views/Bar_20260707194228.vue.bak


   例 3: backend/sql/update20260707.sql -> backend/sql/update20260707_20260707194228.sql.bak





3. **同目录存放**: 备份文件必须放在与原文件相同的目录, 后缀严格按上述格式. 不要用 PowerShell 默认的 Copy-Item 命名 (它会生成 foo.py.20260707193333.bak 似的 .bak, 不是我们要的格式).





4. **操作步骤**:


   a. 修改前, 用 git status --short 列出本轮实际要改的文件路径.


   b. 对清单里每个文件, 生成名为 原文件名(不含后缀)_日期时间(yyyyMMddHHmmss).原后缀名.bak 的备份.


      PowerShell: $stamp = (Get-Date -Format "yyyyMMddHHmmss"); Copy-Item foo.py "foo_$stamp.py.bak"


      Python: import shutil, time; shutil.copy("foo.py", f"foo_{time.strftime("%Y%m%d%H%M%S")}.py.bak")


   c. 改完后用 Get-Item 校验备份大小, 与原文件一致或接近.


   d. 若发现漏备份, 立刻用 git show HEAD:路径 补做, 并在本节末尾追加备忘.





5. **错位备份的纠错**: 若实际改了 A 但只备份了 B, 立刻补做 A 的备份, 在最终消息中明确声明, 不要掩盖.





6. **历史备忘**:


   - 2026-07-07: 之前使用 .YYYYMMDDHHMMSS.bak 命名 (即 foo.py.20260707181359.bak); 今天夜里 19:42 红框修改后, 改用 <name_no_ext>_YYYYMMDDHHMMSS.<ext>.bak 命名 (即 abcd.py -> abcd_20260707194135.py.bak). 后续所有备份按新规则执行.


   - 2026-07-07: 漏备份 management_service_portal.py, 用 git HEAD 补做. 此后任何改动前必须先 git status --short 列清单.





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

### 5.1 is_center_leader 口径 (2026-07-09 备忘)

`dtlms_plan_offer` 改 `accepted` 的"研究中心负责人"权限判断 (`resolve_camp_offer_is_center_leader` 在 `backend/app/services/postgres_state_store_query_recruitment.py`) 的关联表:

- **只需 2 张表**: `dtlms_users` (按 username 查 viewer) ⨝ `dtlms_team_leaders` (按 `user_id` 命中即为中心负责人).
- **不需要 `dtlms_teams`**: 判定"是不是中心负责人"是布尔属性, 无需看 `dtlms_teams.is_deleted` 等.
- **不要因为"dtlms_teams 也有 lead_user_id 字段"就改成走 `dtlms_teams.lead_user_id`**: `dtlms_teams.lead_user_id` 和 `dtlms_team_leaders` 是两套并存的 lead 机制, 当前以 `dtlms_team_leaders` 为准 (与 `resolve_camp_offer_visible_advisor_names` 的 center_leader 分支保持一致).

而"中心负责人能看哪些学生" (`resolve_camp_offer_visible_advisor_names` 的 center_leader 分支) 才需要 3 张表:

```
dtlms_users (viewer) → dtlms_team_leaders (找 viewer 任 lead 的 team_id) 
                    → dtlms_team_advisors (找这些 team_id 下的所有 advisor_user_id) 
                    → dtlms_users (拿到这些 advisor 的 full_name, 用于过滤入营名单 first/second_choice)
```

这两段口径**不一样**, 不要混用 SQL.





### 5.2 dtlms_plan_offer 状态机不变量 (2026-07-09)

`dtlms_plan_offer.accepted` 状态机 + 关联字段同步规则 (链 B 步骤 4-5):

- `accepted_pending_send` (录取未发送): 中心负责人决议结果
- `accepted_sent`        (录取已发送): 书院管理员发邮件后写入, 同时 `accepted_notification_sent_at = now()`, 清空 `student_submitted_offer_at`
- `accepted_confirmed`   (录取已确认): 学生点"接受"后写入, 同时 `student_submitted_offer_at = now()`
- `accepted_rejected`    (录取已拒绝): 学生点"拒绝"后写入, 同时 `student_submitted_offer_at = now()`
- `pending`              (待定): 中心负责人
- `declined`             (未录取): 中心负责人

**不变量**:

1. `student_submitted_offer_at` IS NOT NULL ⇔ `accepted IN ('accepted_confirmed', 'accepted_rejected')` (终态)
2. `student_submitted_offer_at` IS NULL ⇔ `accepted IN ('accepted_pending_send', 'accepted_sent', 'pending', 'declined', NULL)` (非终态)
3. 任何写 `accepted` 终态的 SQL 路径 (无论是 accept 还是 reject), 都必须**同时**写 `student_submitted_offer_at = now()` + `updated_at = now()` (表无 trigger, 显式写)
4. 重发邮件允许 `accepted IN ('accepted_pending_send', 'accepted_confirmed', 'accepted_rejected')` 状态进入 `accepted_sent`, 但**只有终态需要清空 `student_submitted_offer_at`**
5. `declined` / `pending` 状态**不允许**重发录取通知邮件 (业务语义: 已经拒绝了/待定, 不应再发录取)

**SQL 守门**:
- 学生 accept/reject 端点: `WHERE candidate_no = ? AND plan_id = ? AND accepted = 'accepted_sent'` 防止并发覆盖
- 书院管理员发邮件: `WHERE candidate_no = ? AND plan_id = ? AND accepted = ?` (expected_current_accepted) 同样防并发

### 5.3 录取通知邮件测试邮箱 (2026-07-09)

`/recruitment/camp-offers` "发送录取通知" 弹窗发邮件时, 实际收件人**统一替换为 `lk139@126.com`** (写死, 不论学生原本邮箱是啥), 写在 `backend/app/services/email_service.py` 的 `send_admission_offer_letter` 内部 `TEST_OVERRIDE_RECIPIENT` 常量.

**目的**: 测试期间避免真发邮件到学生真实邮箱, 等客户正式文案定稿 + SMTP 配置改 `real` 模式后, 把这个常量改成读 `student_email` 即可.

**Email 主题**: `【上海人工智能实验室】录取通知书 - {admission_offered_school}`

**Email 模板变量** (与 portal /portal/home/offer 卡片同源):
- `student_name` (暂用报名号占位, 后续从 portal_student 取 full_name)
- `admission_offered_school`
- `accepted_notification_sent_at_ymd`
- `offer_timeout_hours` (从字典 `student_signed_offer_timeout_hours` 读, fallback 24)
- `portal_offer_url` (固定 `/portal/home/offer`)

### 5.4 Portal 登录后跳转 /portal/home/offer (2026-07-09)

学生在 `/portal/home` 页面 onMounted 时, 调 `GET /portal/offer` 查 `accepted` 字段, 若处于以下**任一**终态则自动跳到 `/portal/home/offer`:

- `accepted_sent`       (录取已发送, 未签)
- `accepted_confirmed`  (录取已确认, 已签)
- `accepted_rejected`   (录取已拒绝, 已拒)

跳转实现: `frontend/src/views/home/PortalHomeView.vue` 的 `tryRedirectToOfferIfNeeded()`, 在 `loadPortalHome()` 之后异步调用 (不阻塞主页加载).

### 5.5 备份失误备忘 (2026-07-09 18:00)

**问题**: 用 PowerShell `Get-ChildItem -Recurse -Filter *.py -File` 时, `-Filter` 只支持单值, 不能一次过滤多个扩展名, 导致漏备前端 .vue / .ts / .xlsx 文件. 之后又用 `Where-Object` 加白名单时, 因为 `\` 转义嵌套问题导致正则匹配失败, **错删了一部分后端备份**.

**纠正**:
1. 备份脚本要用 `-Include` 数组 + `-Recurse` 组合, 不能 `-Filter` 多扩展名
2. 删备份前必须**先列白名单**, 不要"先全删再补"

后续若再有备份, 用 `Copy-Item` 显式列表 (本轮末尾已用此方式补建前端 + xlsx 备份).

## 6. 每周工作回顾 / 周报起草





本仓库内置每周自动起草周报的工具链，配套文档见 `tools\WEEKLY_REVIEW.md`。





- 脚本：`tools\weekly_review.py`（Python 3.10+ 标准库）。从 `git log` 抽取上周提交，按 feat/fix/docs/test/chore 自动分类，输出 Markdown。


- 包装：`tools\weekly_review.cmd`（已设 `PYTHONIOENCODING=utf-8`，可被任务计划程序直接调用）。


- 任务定义：`tools\weekly_review.task.xml`（每周一 09:00，本机需管理员权限用 `schtasks /Create` 导入）。


- 存档目录：`documents\周报\周报_YYYY-MM-DD_WNN.md`，每次追加一份。


- 日志：`documents\周报\weekly_review.log`。





### 6.1 注册方式（管理员 PowerShell）





```


schtasks /Create /TN "pydtlms-weekly-review" /XML "D:\pyproj\pydtlms\tools\weekly_review.task.xml"


```





管理：`schtasks /Run`、`/Query /V /FO LIST`、`/Delete /F`。





### 6.2 手动调试





```


python tools\weekly_review.py                # 控制台打印上一周


python tools\weekly_review.py --days 14      # 最近 14 天


python tools\weekly_review.py --week 2026-W27  # 指定 ISO 周


python tools\weekly_review.py --save         # 落盘到 documents\周报\


```





### 6.3 维护约束





- 修改 `tools\weekly_review.py` 前必须备份 `<file>.YYYYMMDDHHMMSS.bak`，改完跑 `python -m py_compile`。


- 周报标题、目录命名沿用中文（与 `CHANGELOG.md` 风格一致）。


- 任务计划程序时间改动：编辑 `tools\weekly_review.task.xml` 的 `<StartBoundary>` 与 `<DaysOfWeek>` 后重新导入。


- 不要把 `documents\周报\weekly_review.log` / `*.bak` 提交：仓库 `.gitignore` 已忽略 `*.bak`；新增的 `weekly_review.log` 如不希望入库，追加到 `.gitignore`：`documents/周报/weekly_review.log`。


