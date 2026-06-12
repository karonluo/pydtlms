# application_draft 附件回填与单向同步修改计划

## 背景

当前问题不是“提交成功后显式清空 application_draft”，而更像是“保存/提交时用一份不完整的草稿对象覆盖了原有草稿”，导致简历附件 URL、个人陈述中的两个补充问题、英文成绩附件等字段丢失。

本次修改只做一件事：

- 正式表作为最终可信来源。
- `application_draft` 只负责补缺，不负责反向覆盖正式表。
- 当 `application_draft` 为空或缺字段时，用正式表回填缺失项。

## 修改目标

1. 保住简历附件 URL、个人陈述补充问题、英文成绩附件等字段。
2. 避免提交后 draft 中的缺失值把正式表数据抹掉。
3. 让读取时和写入时的规则一致，减少“看起来有值，落库后变空”的情况。

## 修改范围

- [backend/app/services/management_service_portal.py](../backend/app/services/management_service_portal.py)
- [backend/app/schemas/portal.py](../backend/app/schemas/portal.py)
- [backend/app/services/postgres_state_store_core.py](../backend/app/services/postgres_state_store_core.py)

## 修改步骤

### 第 1 步：确认草稿写入时保留旧值

怎么做：

- 在 `management_service_portal.py` 里找到 `_build_portal_application_draft_payload(...)`。
- 在构建新 draft 前，先读取学生原有 `application_draft`。
- 构建结果不要直接用新 payload 覆盖旧 draft，而是先保留旧 draft，再用新 payload 覆盖用户本次确实填写的字段。

为什么这样做：

- 这样可以避免用户这次提交没有带上某些附件字段时，把历史上的有效值冲掉。

确认点：

- 如果当前 payload 没传 `resume_attachment_url`，旧 draft 里有值，则最终 draft 仍应保留旧值。

### 第 2 步：增加正式表到 draft 的缺项回填

怎么做：

- 在 `portal.py` 的个人陈述回填逻辑里，继续沿用现有的附件兜底模式。
- 补充一层“正式表字段优先回填 draft 缺项”的逻辑，重点处理：
  - `personal_statement.resume_attachment_url`
  - `personal_statement.supporting_material_attachment_url`
  - 个人陈述两个文本问题对应字段
  - 英文成绩附件/英文成绩列表
- 如果 `application_draft` 为空，就直接从正式表重建一个可用 draft。

为什么这样做：

- 读接口和写接口要遵守同一规则：draft 只是快照，不是唯一真相。

确认点：

- 当 draft 缺少附件字段时，详情页仍能显示正式表里的附件 URL。

### 第 3 步：禁止 draft 反向覆盖正式表

怎么做：

- 在 `management_service_portal.py` 的保存和提交流程里，检查正式表字段更新逻辑。
- 明确只允许表单输入写正式表，不允许用 draft 中的空值回写正式表。
- 如果某字段在正式表里已有值，而当前 draft 为空，则保持正式表不变。

为什么这样做：

- 你提到的风险是对的：提交后 draft 可能被清理或不完整，因此不能再让它回头污染正式表。

确认点：

- 提交后，即使 draft 中某些字段为空，正式表里的附件仍然保留。

### 第 4 步：把 draft 合并逻辑改成“浅合并 + 缺项补齐”

怎么做：

- 在 `postgres_state_store_core.py` 的 `_merge_portal_application_draft(...)` 附近，检查是否需要扩展为字段级补齐。
- 对 `personal_statement`、`declaration`、`preferences` 这类嵌套对象，避免简单整块覆盖。
- 对附件字段，优先保留已有非空值，再用正式表补缺。

为什么这样做：

- 现在的覆盖方式太粗，任何一个空对象都可能把已有附件信息吞掉。

确认点：

- 旧 draft 中存在的附件字段不会因为新 draft 里缺失同名字段而消失。

### 第 5 步：补验证用例

怎么做：

- 增加一条用例：草稿里没有简历附件，但正式表里有，读取详情时必须显示正式表值。
- 增加一条用例：提交时 payload 没有英文成绩附件，最终正式表不能被清空。
- 增加一条用例：`application_draft` 为空时，能从正式表重建出可用结构。

为什么这样做：

- 这次问题本质上是数据回填方向错误，必须用测试锁住方向。

确认点：

- 三条用例都通过后再考虑上线。

## 执行顺序建议

1. 先改保存/提交路径的 draft 合并逻辑。
2. 再改读取路径的正式表回填逻辑。
3. 最后补测试。

## 我建议的最小落地方案

如果你想先做最小改动，我建议只改两处：

1. `management_service_portal.py`：避免提交时用不完整 draft 覆盖旧值。
2. `portal.py`：在读取时用正式表补齐附件缺项。
3. 忽略 `research_center_name` / `team_id` 的数据处理，需求上已经与学生报名整个流程环节暂时无关了。

这样可以先止血，再决定要不要把 `postgres_state_store_core.py` 的合并逻辑也做深一点。

## 待你确认的点

- 是否按“最小落地方案”先做两处修改。
- 是否把英文成绩附件也纳入同一套回填规则。
- 是否需要我把上述内容再拆成开发任务清单。
