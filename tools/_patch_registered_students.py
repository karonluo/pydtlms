import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\frontend\src\views\students\RegisteredStudentsView.vue")
s = p.read_text(encoding="utf-8")

# ---- 1) 第一行 4 个项：让 4 个项能跟同行 ----
# 原因：filter-item--wide 占太宽将其他三项换行。
old = """.filter-item--wide {
  flex: 1 1 280px;
  min-width: 260px;
}

.filter-item--compact {
  flex: 0 0 180px;
}

.filter-item--toggle {
  flex: 0 0 auto;
}

.filter-item--multi {
  flex: 1 1 220px;
  min-width: 220px;
}"""
new = """.filter-item--wide {
  flex: 1 1 220px;
  min-width: 200px;
  max-width: 320px;
}

.filter-item--compact {
  flex: 0 0 180px;
}

.filter-item--toggle {
  flex: 0 0 auto;
}

.filter-item--multi {
  flex: 1 1 200px;
  min-width: 200px;
}"""
assert old in s, "filter-item widths block not found"
s = s.replace(old, new)

# ---- 2) 表格：宽度由 min-width 改为 width，迫使其溢出 ----
old2 = """.table-host {
  flex: 1;
  min-height: 0;
  overflow-x: auto !important;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  width: 100%;
}

.table-host :deep(.el-table) {
  width: auto;
  min-width: 1880px;
}"""
new2 = """.table-host {
  flex: 1;
  min-height: 0;
  overflow-x: auto !important;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  width: 100%;
}

.table-host :deep(.el-table) {
  width: 1880px;
  table-layout: fixed;
}"""
assert old2 in s, "table-host block not found"
s = s.replace(old2, new2)

# ---- 3) 操作列浮动：清理 el-table 内部 wrapper 上的 overflow，并强化 sticky 优先级 ----
# 之前是 .el-table__body-wrapper { overflow: visible !important; } 会让 fixed right 的内容在越出表格时显示，
# 但 x 方向产生滚动的依然是 .el-table__inner-wrapper。Element Plus 在 2.x 中 fixed right 在 .el-table__fixed-right
# 容器中独立滚动；为了产生“列表区滚动、操作列始终贴右”需要：
#  (a) 去掉 internal fixed wrapper 的 overflow-y:hidden，保留 overflow-x:hidden 让 X 滚动。
#  (b) 用 position:sticky（贴在 .table-host 滚区右侧）作为补充。
old3 = """.table-host :deep(.el-table__body-wrapper) {
  overflow: visible !important;
}"""
new3 = """.table-host :deep(.el-table__body-wrapper) {
  overflow-x: hidden !important;
  overflow-y: auto !important;
}

.table-host :deep(.el-table__inner-wrapper) {
  overflow: visible !important;
}

.table-host :deep(.el-table__fixed-right),
.table-host :deep(.el-table__fixed) {
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}"""
assert old3 in s, "body-wrapper block not found"
s = s.replace(old3, new3)

# ---- 4) 操作列：使用 position:sticky 贴到滚动容器右侧（更可靠） ----
# 注意：el-table 的 fixed="right" 已经把该列渲染在 .el-table__fixed-right 包装里，
# 这个包装本身就是 position:absolute; right:0; top:0，靠 .table-host 滚动时这个
# 包装位置不变即可“贴右”。但 el-table__fixed-right 默认的 position 依赖父层
# 滚动。我们已经在 .table-host 放 overflow-x:auto，这个包装会随横滚。
# 这里加上 :deep(.el-table__fixed-right) 与 .el-table__fixed-right-wrapper 兜底。
old4 = """/* 操作列浮动效果 */
.table-host :deep(.operation-column.el-table__cell) {
  position: sticky;
  right: 0;
  z-index: 9;
  background-color: white;
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}

.table-host :deep(.el-table__header th.operation-column.el-table__cell) {
  position: sticky;
  right: 0;
  z-index: 11;
  background-color: #f5f7fa;
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}

.table-host :deep(tbody tr:hover .operation-column.el-table__cell) {
  background-color: #f5f7fa;
}"""
new4 = """/* 操作列浮动效果：fixed="right" 已由 element-plus 渲染在 .el-table__fixed-right
   包装中。下面主要确保该包装贴右、随竖滚且 z-index 高于普通单元。 */
.table-host :deep(.el-table__fixed-right-patch) {
  background-color: #f5f7fa;
}

.table-host :deep(.el-table__fixed-right-wrapper),
.table-host :deep(.el-table__fixed-right) {
  position: sticky !important;
  right: 0 !important;
  left: auto !important;
  z-index: 9;
  background-color: #ffffff;
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}

.table-host :deep(.el-table__fixed-right-wrapper .el-table__header-wrapper),
.table-host :deep(.el-table__fixed-right .el-table__header-wrapper) {
  z-index: 11;
  background-color: #f5f7fa;
}

.table-host :deep(.el-table__fixed-right-wrapper tbody tr:hover td),
.table-host :deep(.el-table__fixed-right tbody tr:hover td) {
  background-color: #f5f7fa !important;
}

/* 备用：以防某个版本中 el-table 没有生成 fixed 包装，
   给 operation-column 单元加 sticky 作为兜底。 */
.table-host :deep(.el-table .operation-column.el-table__cell) {
  position: sticky;
  right: 0;
  z-index: 5;
  background-color: inherit;
}

.table-host :deep(.el-table th.operation-column.el-table__cell) {
  z-index: 6;
  background-color: #f5f7fa;
}"""
assert old4 in s, "operation column block not found"
s = s.replace(old4, new4)

p.write_text(s, encoding="utf-8")
print("patched")
