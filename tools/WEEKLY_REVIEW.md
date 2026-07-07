# 每周工作回顾 / 周报起草

每周自动汇总 `D:\pyproj\pydtlms` 仓库上周的 git 提交，起草一则简短的中文状态更新到 `documents\周报\` 目录。

## 产物

| 文件 | 用途 |
| --- | --- |
| `tools\weekly_review.py` | 起草脚本（Python 3.10+ 标准库）。从 `git log` 抽取提交、分类、生成 Markdown。 |
| `tools\weekly_review.cmd` | Windows 任务计划程序要执行的 .cmd 包装（已设置 `PYTHONIOENCODING=utf-8`）。 |
| `tools\weekly_review.task.xml` | 任务计划程序任务定义（每周一 09:00）。 |
| `documents\周报\` | 周报存档目录。每次自动追加 `周报_YYYY-MM-DD_WNN.md`。 |
| `documents\周报\weekly_review.log` | 任务执行日志（追加写）。 |

## 手动使用

在仓库根目录执行：

```
python tools\weekly_review.py                # 在控制台打印上一周周报
python tools\weekly_review.py --days 14      # 拉最近 14 天
python tools\weekly_review.py --week 2026-W27  # 指定 ISO 周
python tools\weekly_review.py --save         # 直接落盘到 documents\周报\
```

## 注册 Windows 任务计划程序

> 当前环境注册调度任务需要管理员权限。请在 **管理员 PowerShell** 中执行：

```
schtasks /Create /TN "pydtlms-weekly-review" /XML "D:\pyproj\pydtlms\tools\weekly_review.task.xml"
```

后续管理命令：

```
schtasks /Run /TN "pydtlms-weekly-review"          # 立即跑一次（验收用）
schtasks /Query /TN "pydtlms-weekly-review" /V /FO LIST
schtasks /Delete /TN "pydtlms-weekly-review" /F
```

也可以直接在「任务计划程序」GUI 导入：`pydtlms-weekly-review` → 操作：`tools\weekly_review.cmd` → 触发器：每周一 09:00。

## 调整频率

修改 `tools\weekly_review.task.xml`：

- 改 `<DaysOfWeek>` 选择星期几
- 改 `<StartBoundary>` 改时间
- 改 `<WeeksInterval>` 改间隔周数

改完重新 `schtasks /Delete` 再 `schtasks /Create` 即可。

## Codex 自动化通道（可选）

如果希望 Codex 桌面 app 在每周一时间到时自动唤醒一个新线程并起草周报，可把本 README 上半段粘贴到 Codex 中由我创建对应 automation。当前 Codex 桌面会话的 `automation_update` / `create_thread` 等线程工具未直接暴露在工具列表中，需切换到具备该工具的会话后再配置。
