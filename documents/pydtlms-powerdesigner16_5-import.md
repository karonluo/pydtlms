# PowerDesigner 16.5 导入说明

已提供文件：
- documents/pydtlms-powerdesigner16_5-complete.pdm
- documents/pydtlms-powerdesigner16_5-reverse-engineering.sql

内容来源：
- 数据库：test18
- public schema 下的 dtlms_* 物理表，共 65 张表，外键 74 条
- 已排除 dtlms_runtime_* 与 dtlms_schema_migrations

优先使用原生 .pdm：
1. 在 PowerDesigner 16.5 中选择 File -> Open Model。
2. 打开 documents/pydtlms-powerdesigner16_5-complete.pdm。
3. 进入 MainDiagram 查看表和关系线；如布局需要，可再执行 Auto Layout 微调。

如果你仍想走 SQL 逆向：
1. File -> Reverse Engineer -> Database。
2. DBMS 选择 PostgreSQL 对应版本。
3. Input 选择 Script files。
4. 选中 documents/pydtlms-powerdesigner16_5-reverse-engineering.sql。

说明：
- 已使用本机安装的 PowerDesigner 16.5 实际打开 documents/pydtlms-powerdesigner16_5-complete.pdm，验证可正常识别模型。
- 实际打开验证结果：65 张表、74 条关系、1 张 Physical Diagram。
- 同时做了 XML 结构校验，确保表数量与外键数量和数据库一致。
- .pdm 为主交付，SQL 保留作为备用逆向来源。
