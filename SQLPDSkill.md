# SQLPDSkill

本文件是 `sql-powerdesigner-pdm-generation` skill 的快捷入口说明。它现在按“通用流程 + 当前仓库示例”组织，不再把 pydtlms 的路径当成所有仓库都必须照搬的固定前提。

标准 skill 发现路径：

- `backend/ai/skills/sql-powerdesigner-pdm-generation/SKILL.md`
- `.github/skills/sql-powerdesigner-pdm-generation/SKILL.md`

建议优先使用上述标准路径，因为更容易被支持 Skill 发现机制的 AI 或 Agent 自动识别。

## Skill Purpose

用于从当前仓库中的 PostgreSQL 物理表结构生成 PowerDesigner 16.5 可打开的原生 `.pdm` 文档，并附带 SQL 逆向脚本和导入或验证说明。

## Portable Rules

- 先扫描当前仓库，定位数据库连接配置、已有导出脚本、输出目录和现有命名约定。
- 不要把仓库名、脚本路径、schema 前缀、输出文件名或数据库名写死在 skill 里。
- 如果仓库里已经有脚本或历史产物，优先复用；只有不存在时才新增最小可用实现。
- PowerDesigner 安装路径要动态探测，或直接使用用户已提供的安装信息。
- 只有在真实执行过 `OpenModel` 时，才能声明 `.pdm` 已完成实机验证。

## Current Repository Mapping

下面这些只是 pydtlms 当前仓库的映射示例，不是 skill 的固定要求：

- 生成脚本：`tools/export_powerdesigner_schema.py`
- 连接配置：`backend/.env`
- 主产物：`documents/pydtlms-powerdesigner16_5-complete.pdm`
- 备用 SQL：`documents/pydtlms-powerdesigner16_5-reverse-engineering.sql`
- 说明文档：`documents/pydtlms-powerdesigner16_5-import.md`
- 当前导出范围：`public.dtlms_*`，排除 `dtlms_runtime_*` 与 `dtlms_schema_migrations`

如果换到 OpenClaw，应该把上面这些映射替换成 OpenClaw 自己的脚本、env、schema 范围和输出命名，而不是继续沿用 pydtlms 文件名。

## How To Invoke

可以把下面这类任务直接交给支持 Skill 的 AI：

- “请使用 sql-powerdesigner-pdm-generation skill，先扫描当前仓库里的数据库配置和已有导出脚本，再生成 PowerDesigner PDM。”
- “请使用 sql-powerdesigner-pdm-generation skill，基于当前仓库的 PostgreSQL schema 重新生成 `.pdm`，并把输出文件放到仓库现有文档目录。”
- “请使用 sql-powerdesigner-pdm-generation skill，检查这个仓库有没有硬编码的 pydtlms 路径，如果有就改成当前仓库可复用的写法。”

## Example Command Pattern

下面是通用命令模式，不再写死工作区绝对路径：

```powershell
Set-Location <workspace-root>
<python-executable> <workspace-export-script>
```

在当前 pydtlms 仓库里，对应示例才是：

```powershell
Set-Location .
.\.venv\Scripts\python.exe tools\export_powerdesigner_schema.py
```

## Notes

- 如果 `.pdm` 当前正被 PowerDesigner 打开，脚本应跳过覆盖写入并提示先关闭文件后再重跑。
- 如果其他 AI 平台不支持标准 Skill 发现，也可以直接把 `SQLPDSkill.md` 连同标准 `SKILL.md` 内容一起作为上下文提供。
