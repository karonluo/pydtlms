# 数据库分页 TODO

## 1. 当前结论

当前后端列表分页**不是数据库分页**，而是典型的“先取全量数据到应用层，再做 Python 内存切片分页”。

核心证据：

- `backend/app/services/management_service.py` 中存在统一分页函数 `_paginate_items()`，实现方式是先计算 `start_index/end_index`，再执行 `items[start_index:end_index]`。
- 多个列表查询方法在完成筛选与组装后，再统一调用 `_paginate_items()` 返回分页结果。
- `backend/app/services/postgres_state_store.py` 当前承担的是运行态装载与整库同步职责，`load_state()` 会把各 runtime 表的 `payload` 整体加载到内存中，而不是在 SQL 层做 `LIMIT/OFFSET` 查询。
- `backend/app/services/dashboard_service.py` 基本只是调用 `store.get_xxx(..., page, page_size)` 的薄包装层，不负责数据库分页逻辑。

结论：

- 当前分页属于应用层分页。
- 当前实现对小数据量可用。
- 随着数据量增长，列表接口会出现不必要的全量读取、全量反序列化与内存切片开销。

## 2. 当前受影响范围

以下模块当前都属于“先取全量，再内存分页”的实现模式：

### 招生模块

- 招生计划列表 `get_recruitment_plans`
- 招生申请列表 `get_recruitment_applications`
- 招生申请导出前还存在 `page_size=10000` 的兜底拉取逻辑

### 学生与团队模块

- 学生主档列表 `get_students`
- 团队列表 `get_teams`

### 培养模块

- 培养方案列表 `get_training_plans`
- 科研报告列表 `get_scientific_reports`
- 外出研修列表 `get_outbound_studies`

### 学位模块

- 论文列表 `get_theses`
- 论文评审列表 `get_thesis_reviews`

### 系统治理模块

- 字典类型列表 `get_dict_types`
- 字典数据列表 `get_dict_data`
- 角色列表 `get_roles`
- 系统用户列表 `get_system_users`
- 审计策略列表 `get_audit_policy_records`
- 集成列表 `get_integrations`
- 操作日志列表 `get_operation_logs`
- 同步日志列表 `get_sync_logs`

### 流程模块

- 工作流任务列表 `get_workflow_tasks`

## 3. 现阶段架构判断

当前服务层结构更接近：

1. `PostgresStateStore` 负责把 runtime 表整批装入内存
2. `ManagementService` 在内存对象集合上做过滤、映射、排序和分页
3. API 层只把 `page/page_size` 透传进去

这套实现的优点：

- 开发快
- 统一逻辑集中
- 在模拟数据和小数据集下可控

这套实现的缺点：

- 无法利用数据库索引直接裁剪结果集
- `total` 的计算依赖全量集合
- 过滤条件越多、数据量越大，CPU 与内存浪费越明显
- 日志、任务、申请等天然高增长数据集后续最容易出现性能瓶颈

## 4. 改造优先级建议

### P0：优先改成数据库分页

这些模块数据增长最快，最容易先出性能问题：

- 工作流任务列表
- 招生申请列表
- 操作日志列表
- 同步日志列表
- 系统用户列表
- 学生主档列表

优先原因：

- 列表访问频率高
- 数据增长持续且明显
- 通常会叠加关键字、状态、时间范围等过滤条件
- 很适合下推到 PostgreSQL 执行

### P1：第二批改造

- 招生计划列表
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_recruitment_plans` 与报名申请聚合计数的关键字、学期分页查询；`backend/app/services/management_service.py` 中 `get_recruitment_plans` 已优先走数据库分页，异常时回退内存分页。
- 团队列表
- 培养方案列表
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_runtime_training_plans` 的关键字、状态、导师、汇报周期分页查询；`backend/app/services/management_service.py` 中 `get_training_plans` 已优先走数据库分页，异常时回退内存分页。
- 科研报告列表
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_runtime_scientific_reports` 的关键字、报告状态、评阅人分页查询；`backend/app/services/management_service.py` 中 `get_scientific_reports` 已优先走数据库分页，异常时回退内存分页。
- 外出研修列表
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_runtime_outbound_studies` 的关键字、审批状态、研修类型、导师分页查询；`backend/app/services/management_service.py` 中 `get_outbound_studies` 已优先走数据库分页，异常时回退内存分页。
- 论文列表
- 论文评审列表

补充说明：团队列表已在第一批数据库分页改造中完成，此处保留仅用于对照第二批原始候选范围。

### P2：最后改造

- 字典类型列表
- 字典数据列表
- 角色列表
- 审计策略列表
- 集成列表

原因：

- 数据量通常相对更小
- 当前性能风险低于业务流水和日志类数据集

## 5. 建议的改造顺序

### 第一阶段：建立通用 PostgreSQL 列表查询基础能力

- 在 `PostgresStateStore` 中新增真正的列表查询方法，而不是只提供整库 `load_state()`。
- 每个列表查询都明确支持：
  - `page`
  - `page_size`
  - 关键字过滤
  - 状态过滤
  - 必要的字段过滤
  - `ORDER BY`
  - `COUNT(*)`
  - `LIMIT/OFFSET`

建议沉淀一个统一的分页查询返回结构：

- `items`
- `total`
- `page`
- `page_size`

### 第二阶段：先替换 P0 列表

- 工作流任务
- 招生申请
- 操作日志
- 同步日志
- 系统用户
- 学生主档

要求：

- 对外 API 契约不变
- 前端无需修改分页协议
- `total` 与当前行为保持一致

### 第三阶段：清理内存分页逻辑

- 逐步减少 `ManagementService` 中对 `_paginate_items()` 的依赖
- 保留该函数只作为临时兼容方案，不再作为主要列表实现
- 等主要列表都切完后，再决定是否删除 `_paginate_items()`

## 6. 单个列表的目标实现模式

以学生主档列表为例，目标实现应变为：

1. API 层接收 `page/page_size/keyword/status/advisor_name/team_name`
2. Service 层调用 `PostgresStateStore.get_students_page(...)`
3. Store 层直接生成 SQL：
   - `WHERE ...`
   - `ORDER BY ...`
   - `LIMIT ... OFFSET ...`
4. 再执行单独的 `COUNT(*)` 查询返回总数

而不是：

1. 全量加载 students runtime 数据
2. Python 过滤
3. Python 切片

## 7. 需要特别注意的点

### 7.1 runtime 表与关系表的取数来源要统一

当前系统存在：

- runtime JSON 表
- 关系表同步结果

改数据库分页前，必须先明确每个列表最终以哪一层为准：

- 继续从 runtime `payload` 表查
- 或直接切到关系表/视图查询

建议：

- 日志、任务、申请、学生主档等高频列表，优先直接查关系表或视图
- runtime 表继续保留给同步与状态恢复使用

### 7.2 排序规则必须固定

数据库分页若没有稳定排序，会出现翻页错乱。

每个列表必须补齐稳定 `ORDER BY`：

- 优先业务时间倒序
- 次级按主键倒序或升序兜底

### 7.3 COUNT 与列表查询条件必须一致

否则前端会出现：

- `items` 数量正确
- `total` 错误
- 分页器页码异常

### 7.4 导出接口不要复用列表分页接口的超大 page_size 方案

当前已有 `page_size=10000` 的导出式拉取痕迹，这只是临时办法。

建议：

- 导出接口走单独查询逻辑
- 列表接口只负责分页视图
- 导出接口再按需要批量流式查询

## 8. 推荐第一批实际落地任务

- [x] 为工作流任务列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持 `status/module/keyword + COUNT(*) + LIMIT/OFFSET`，`backend/app/services/management_service.py` 中 `get_workflow_tasks` 已优先走数据库分页，失败时回退内存分页保持兼容。
- [x] 为招生申请列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于招生申请关系表的分页查询，覆盖计划、状态、关键字过滤，并联取材料状态、审核人、最终成绩；`backend/app/services/management_service.py` 中 `get_recruitment_applications` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [x] 为操作日志列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_operation_logs` 的操作日志分页查询，覆盖关键字、模块、结果过滤；`backend/app/services/management_service.py` 中 `get_operation_logs` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [x] 为同步日志列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_data_sync_logs` 的同步日志分页查询，覆盖关键字、同步状态、源系统过滤；`backend/app/services/management_service.py` 中 `get_sync_logs` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [x] 为系统用户列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_runtime_system_users + dtlms_runtime_roles` 的系统用户分页查询，覆盖关键字、角色、账号状态、部门过滤；`backend/app/services/management_service.py` 中 `get_system_users` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [x] 为学生主档列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_students + dtlms_advisors + dtlms_teams` 的学生主档分页查询，覆盖关键字、状态、导师、团队过滤；`backend/app/services/management_service.py` 中 `get_students` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [x] 为团队列表新增 PostgreSQL 原生分页查询
- 已完成：`backend/app/services/postgres_state_store.py` 已支持基于 `dtlms_teams + dtlms_team_advisors + dtlms_students` 的团队分页查询，覆盖关键字、状态、院系、负责人过滤，并返回成员数与活跃学生数；`backend/app/services/management_service.py` 中 `get_teams` 已优先走数据库分页，异常时回退内存分页保持兼容。
- [ ] 补对应接口测试，验证 `total/page/page_size/items` 一致性
- [ ] 补关键过滤条件测试，验证数据库分页与当前筛选语义一致
- [ ] 明确每个模块究竟以 runtime 表还是关系表/视图作为查询事实来源

## 9. 验收标准

- 列表接口 SQL 层具备 `LIMIT/OFFSET`
- 不再依赖全量 `load_state()` 再内存切片
- `total`、`page`、`page_size`、`items` 返回结构不变
- 关键筛选条件结果与现有逻辑一致
- 前端无需改动即可正常分页
- 日志类与任务类数据集在数据量增长后仍可稳定响应

## 10. 当前建议

短期内不要一次性全量重写所有列表分页，先按 P0 模块逐个切换。

推荐第一刀：

1. 工作流任务列表
2. 招生申请列表
3. 学生主档列表

这三个模块最能直接体现数据库分页改造的收益。
