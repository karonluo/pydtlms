# 修正 runtime 问题的计划表

## 背景

当前系统仍保留一套 `dtlms_runtime_*` JSONB 运行时镜像表。它们最初用于过渡期承载数据和兼容旧逻辑，但现在已经出现两个明显问题：

1. 正式范式表与 runtime 镜像表之间容易发生状态不一致。
2. 页面读取来源、保存来源、审批来源混杂，排障成本高。

本计划的目标不是一次性暴力删除所有 runtime 表，而是先把“读写口径”和“淘汰路径”收敛清楚，逐步完成去 runtime 化。

## 总原则

| 规则 | 说明 |
| --- | --- |
| 禁止新增 runtime 设计 | 后续新功能、字段、实体、关系设计，不允许再新增 `dtlms_runtime_*` 表或新的 JSONB mirror 方案。 |
| Flowable 例外 | Flowable 兼容表、运行时表、历史表继续按 Flowable 规则维护，不纳入本次去 runtime 范围。 |
| 过渡期必须双写 | 在 runtime 尚未完全下线前，凡保留 runtime 镜像的业务，所有保存、提交、审批、删除动作必须同时更新正式范式表和 runtime 表。 |
| 读取优先正式表 | 新改造和排障时，列表、详情、统计、筛选默认优先从正式表读取；runtime 仅作兼容或回放用途。 |
| 每完成一类就补测试 | 每修完一个模块，必须补“正式表已更新”与“页面读取正确”的回归测试。 |

## 当前 runtime 范围盘点

| 分类 | 现状 |
| --- | --- |
| 建表入口 | [backend/sql/040_runtime_store.sql](backend/sql/040_runtime_store.sql) 仍维护 `dtlms_runtime_counters`、`profiles`、`students`、`teams`、`recruitment_plans`、`recruitment_applications`、`training_plans`、`scientific_reports`、`outbound_studies`、`theses`、`thesis_reviews`、`roles`、`system_users`、`audit_policies`、`integrations`、`operation_logs`、`sync_logs`、`workflow_tasks`、`portal_students`。 |
| 历史迁移/回填 | [backend/sql/051_governance_training_degree_columnar.sql](backend/sql/051_governance_training_degree_columnar.sql) 与 [backend/sql/900_safe_production_update_columnar.sql](backend/sql/900_safe_production_update_columnar.sql) 仍包含大量从 runtime 向正式表回填的逻辑。 |
| 写入中心 | [backend/app/services/postgres_state_store.py](backend/app/services/postgres_state_store.py) 仍保留大量 `update_runtime_*`、`delete_runtime_*`、`sync_*` 逻辑。 |
| 调用中心 | [backend/app/services/management_service.py](backend/app/services/management_service.py) 中仍有多处业务动作直接调用 `update_runtime_*` / `insert_runtime_operation_log` / `update_runtime_counter`。 |
| 风险特征 | 同一业务状态可能同时存在于正式表、runtime JSONB、Flowable 兼容表三个位置，最容易出错的是审批状态、提交状态、统计口径。 |

## 分阶段计划表

| 阶段 | 优先级 | 目标 | 作用范围 | 关键动作 | 交付物 | 验证方式 |
| --- | --- | --- | --- | --- | --- | --- |
| Phase 0 | P0 | 先止血，禁止继续扩散 runtime | 全仓库 | 新需求评审时明确禁止新增 runtime；涉及旧模块改动时，先检查是否存在“只写 runtime、不写正式表”的路径。 | 规则落库到仓库记忆与本计划表 | Code review 时逐项核对 |
| Phase 1 | P0 | 建立 runtime 写路径清单 | 后端服务层 | 逐个盘点 `management_service.py` 和 `postgres_state_store.py` 里所有 `update_runtime_*` / `delete_runtime_*` / `sync_*` 调用点，标记对应业务动作。 | 一份“调用点 -> 正式表 -> runtime 表”映射清单 | grep 结果与人工复核 |
| Phase 2 | P0 | 补齐正式表双写缺口 | 招生、门户、系统治理、学生、培养、学位 | 对所有保存、提交、审批、删除动作，确保正式表先正确更新，再同步 runtime；禁止只更新 runtime。 | 一批针对具体缺口的代码修复 | 单测 + 接口回归 + 页面验证 |
| Phase 3 | P1 | 收敛读取口径到正式表 | 列表页、详情页、统计接口 | 逐模块把读取入口改为正式表优先，runtime 只在无正式数据时兜底；清理统计口径混读问题。 | 读取链路收敛改造 | 列表/详情/统计一致性验证 |
| Phase 4 | P1 | 减少 runtime 专用写接口 | `postgres_state_store.py` | 标记废弃 `update_runtime_*`/`delete_runtime_*` 方法；能合并到正式表 sync 的，统一合并。 | 精简后的持久化接口 | 单测 + grep 无新增 runtime 接口 |
| Phase 5 | P2 | 清理迁移脚本和初始化依赖 | SQL 初始化与生产补丁 | 评估 [backend/sql/040_runtime_store.sql](backend/sql/040_runtime_store.sql) 是否仍需默认执行；评估 900 脚本中哪些 runtime 回填段可冻结或删除。 | SQL 调整方案 | 静态检查 + fresh init 验证 |
| Phase 6 | P2 | 下线非 Flowable runtime 表 | 已完全关系化的模块 | 当某一模块已实现“正式表唯一事实来源 + 全量验证通过”后，停止该模块 runtime 双写，并准备删除对应 runtime 表。 | 分模块下线清单 | 迁移脚本 + 回归测试 |

## 建议修复顺序

| 顺序 | 模块 | 原因 | 当前关注点 |
| --- | --- | --- | --- |
| 1 | 招生 / 门户 | 用户当前高频使用，且最近已经暴露出“审批后列表状态不一致”问题。 | `recruitment_applications`、`portal_students`、`workflow_tasks` 的保存/提交/审批双写一致性 |
| 2 | 系统治理 | 角色、用户、profile 仍有 runtime 写入与 backfill 逻辑。 | `roles`、`system_users`、`profiles`、`audit_policies`、`integrations` |
| 3 | 学生 / 团队 | 仍有 runtime team/student 回填与批量修正脚本依赖。 | `students`、`teams` 与关联关系 |
| 4 | 培养 / 学位 | 结构已大体关系化，但 runtime mirror 仍保留。 | `training_plans`、`scientific_reports`、`outbound_studies`、`theses`、`thesis_reviews` |
| 5 | operation_logs / sync_logs / counters | 偏基础设施，适合最后收敛。 | 是否需要保留 JSONB 镜像，还是直接以正式日志表为准 |

## 每一项修复的执行模板

| 步骤 | 要求 |
| --- | --- |
| 1 | 先定位该动作当前写了哪些正式表、哪些 runtime 表。 |
| 2 | 明确该页面/接口读取的是哪张正式表，确认是否存在“页面读正式表、保存只写 runtime”的缺口。 |
| 3 | 先修正式表写入，再保留 runtime 同步，避免再次出现只改镜像不改主表的问题。 |
| 4 | 补两类测试：一类断言正式表字段已变；一类断言列表/详情接口返回正确。 |
| 5 | 如果涉及生产存量修复，再决定是否追加到 [backend/sql/900_safe_production_update_columnar.sql](backend/sql/900_safe_production_update_columnar.sql)。 |

## 当前已知第一批问题

| 编号 | 问题 | 状态 | 备注 |
| --- | --- | --- | --- |
| R-001 | 招生申请“审核不通过”后，注册学生列表仍显示“报名已提交” | 已修复 | 根因是只更新了 `dtlms_runtime_recruitment_applications`，未同步更新正式表 `dtlms_recruitment_applications`。 |
| R-002 | 招生工作台申请池审批对话框样式与注册学生不一致 | 已修复 | 已改为统一使用正式 `el-dialog` 审核对话框。 |
| R-003 | 其他保存/提交/审批入口是否仍存在“只写 runtime”路径 | 待排查 | 下一步按本计划表逐项清理。 |

## 完成标准

当满足以下条件时，才认为某一模块已经完成去 runtime 化：

1. 列表、详情、统计全部以正式表为唯一事实来源。
2. 保存、提交、审批、删除不再依赖 runtime 作为主写入目标。
3. 若仍保留 runtime，仅作为临时兼容镜像，且双写路径有测试覆盖。
4. 该模块对应 runtime 表已停止新增业务依赖。
5. 如果可以安全下线，则补充迁移脚本并移除初始化依赖。

## 备注

- 本计划默认“逐模块收敛”，不做一次性大爆炸删除。
- Flowable 兼容表不在本次去 runtime 清理范围内。
- 后续每完成一项修复，应把进度回填到本文件的“当前已知第一批问题”或新增问题编号中，持续滚动维护。