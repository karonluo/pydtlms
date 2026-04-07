# DTLMS AI Skills

本目录存放面向 AI 代理的领域技能说明，采用标准 SKILL.md 结构组织，内容聚焦当前系统最核心的业务域与维护流程。

当前已提供的 Skills：

- workflow-approval-maintenance：流程驱动审批、角色动作、Flowable 兼容运行态维护
- recruitment-workbench-operations：招生计划与报名申请工作台维护
- student-master-data-and-teams：学生主档、团队与导师归属维护
- training-degree-lifecycle：培养、科研报告、外出研修、论文与学位阶段维护
- system-governance-admin：系统用户、角色、字典、审计与日志治理维护

说明：

- 当前文件按标准 SKILL.md 格式编写，便于后续迁移到任何支持该格式的 AI/Agent 平台。
- 如果后续需要让 GitHub Copilot 按标准路径自动发现，可再镜像一份到 .github/skills/ 目录。
