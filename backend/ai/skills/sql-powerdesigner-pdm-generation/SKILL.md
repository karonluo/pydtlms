---
name: sql-powerdesigner-pdm-generation
description: 'Use when generating, refreshing, debugging, or validating a PowerDesigner 16.5 PDM file from a PostgreSQL schema in the current workspace, including SQL reverse-engineering output, native .pdm generation, and optional real open-model verification in PowerDesigner.'
argument-hint: 'Describe the target repository, database/schema scope, existing generator or metadata files, desired output location, and whether real PowerDesigner open-model validation is required'
user-invocable: true
disable-model-invocation: false
---

# SQL PowerDesigner PDM Generation

## When to Use
- 需要根据当前仓库中的 PostgreSQL 物理库结构重新生成 PowerDesigner 16.5 可打开的 `.pdm`。
- 需要同时导出 SQL 逆向脚本和原生 `.pdm`，用于数据库设计交付或迁移到其他仓库。
- PowerDesigner 打开 `.pdm` 报 `Invalid file`，需要修复 XML 结构或图形节点。
- 需要验证 `.pdm` 是否真的能被本机安装的 PowerDesigner 16.5 打开，而不是只做 XML 静态校验。

## Core Files
- 当前仓库中的 PDM 生成脚本，或需要新建的导出脚本。
- 当前仓库中的数据库连接配置文件，例如 `.env`、`backend/.env`、`config/*.env`。
- 当前仓库中的输出目录，例如 `documents/`、`docs/`、`design/`。
- 若仓库已有 PowerDesigner 说明文档、SQL 逆向脚本或历史 `.pdm`，优先复用而不是重新发明命名。

## Environment Prerequisites
- PostgreSQL 连接信息应来自当前仓库已有配置，而不是预设某个固定路径。
- PowerDesigner 安装目录应动态探测，例如常见安装目录、注册表、现有脚本或用户提供的信息。
- PowerDesigner COM ProgID 在当前机器上应优先尝试 `PowerDesigner.Application.16.5`，若环境不同再按实际版本调整。
- 若仓库无法做实机验证，也要明确说明只完成了静态校验，不能把“未验证”写成“已验证”。

## Working Rules
1. 不要把仓库名、脚本路径、输出文件名、schema 前缀、数据库名写死在 skill 里，必须先按当前仓库实际结构解析。
2. 若仓库已有命名约定或目录结构，优先沿用仓库现状，而不是强行套用 `pydtlms`、`documents/` 或 `dtlms_*`。
3. `.pdm` 必须优先按 PowerDesigner 官方样例结构生成，不能只凭 XML 猜测拼接。
4. 若要声明“可用”，必须至少满足两类校验：
   - 脚本内的 XML/数量一致性校验。
   - PowerDesigner 16.5 `OpenModel` 实机打开校验。
5. 若 `.pdm` 文件正被 PowerDesigner 占用，脚本允许跳过覆盖写入并提示关闭文件后重跑，不能直接崩溃退出。
6. 若修改 `.pdm` 生成结构，同步更新导入说明，避免文档仍保留旧的“未验证”表述。

## Procedure
1. 先扫描当前仓库，确认以下锚点：
   - 数据库连接配置文件在哪里。
   - 是否已有导出脚本、历史 `.pdm`、SQL 逆向脚本或导入说明。
   - 输出目录和命名约定是什么。
2. 明确本次导出的 schema 范围、表名前缀和排除规则；这些规则必须来自当前仓库，而不是默认套用某个旧项目。
3. 运行当前仓库已有的导出脚本；若仓库没有脚本，再新增最小可用生成脚本。
4. 检查生成结果，至少确认：
   - 原生 `.pdm`
   - SQL 逆向脚本
   - 导入或验证说明
5. 若需要实机验证，用 PowerShell 调 COM，并通过工作区相对路径拼出待打开的 `.pdm` 实际位置：
   - 创建对象：`New-Object -ComObject 'PowerDesigner.Application.16.5'`
   - 打开模型：`$pd.OpenModel((Resolve-Path '<generated-pdm-path>').Path)`
6. 记录并确认 PowerDesigner 返回的模型统计：`Tables.Count`、`References.Count`、`PhysicalDiagrams.Count`。
7. 若打开失败为 `Invalid file`，优先对照 PowerDesigner 安装目录中的官方样例和 PostgreSQL DBMS 定义；安装目录要先动态确认，再读取其中的 `ShellNew`、`Examples`、`Resource Files/DBMS`。

## Repository Mapping Example
- 在当前 pydtlms 仓库中，现有映射是：
- 生成脚本：`tools/export_powerdesigner_schema.py`
- 连接配置：`backend/.env`
- 输出目录：`documents/`
- 当前导出范围：`public.dtlms_*`，排除 `dtlms_runtime_*` 与 `dtlms_schema_migrations`
- 当前产物文件名：`pydtlms-powerdesigner16_5-complete.pdm`、`pydtlms-powerdesigner16_5-reverse-engineering.sql`、`pydtlms-powerdesigner16_5-import.md`
- 如果迁移到 OpenClaw 或其他仓库，应只保留上面的流程规则，把脚本路径、schema 前缀、输出目录和文件名替换为目标仓库自己的约定。

## Validation Checklist
- 脚本成功生成当前仓库约定位置下的 SQL 与导入说明。
- `.pdm` 文件能被目标环境中的 PowerDesigner COM `OpenModel` 成功打开，或明确注明未做实机验证。
- 打开结果中的表数、关系数与数据库统计一致。
- 至少存在 1 张 `PhysicalDiagram`。
- 当前仓库的导入说明中，验证描述与当前真实状态一致。

## Troubleshooting
- 如果 `OpenModel` 返回 `Invalid file`：说明 `.pdm` 结构仍不符合 PowerDesigner 真实格式，优先核对文件头、`DBMS`、`TargetModels`、`DefaultGroups`、`References`、`TableSymbol`、`ReferenceSymbol`。
- 如果固定的 COM ProgID 无法创建对象：先枚举或确认本机实际 PowerDesigner 版本，再替换为正确 ProgID，不要假设所有机器都和当前仓库开发机一致。
- 如果脚本提示 `.pdm` 文件被锁定：先关闭 PowerDesigner 中打开的模型，再重新执行导出脚本。
- 如果只需要备用逆向来源，可保留 SQL 逆向脚本，但主交付应优先使用原生 `.pdm`。