import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\frontend\src\views\students\RegisteredStudentsView.vue")
s = p.read_text(encoding="utf-8")

# Revert the el-table__fixed-right position:sticky -- el-table 自身已经用 position:absolute
# 将 fixed 列贴右。改为在 .el-table__body-wrapper 上加 overflow-x:auto，并把
# 整个内层容器 (inner-wrapper) 限制其位置；不动 fixed 包装的 position。
old = """.table-host :deep(.el-table__body-wrapper) {
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
new = """.table-host :deep(.el-table__body-wrapper) {
  overflow-x: auto !important;
  overflow-y: auto !important;
}

.table-host :deep(.el-table__inner-wrapper) {
  overflow: visible !important;
}

.table-host :deep(.el-table__fixed-right),
.table-host :deep(.el-table__fixed) {
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}"""
assert old in s, "block 1 not found"
s = s.replace(old, new)

# 同样将 fixed-right-wrapper 的 position:sticky 移除，让 el-table 自带的 absolute 起作用
old2 = """.table-host :deep(.el-table__fixed-right-wrapper),
.table-host :deep(.el-table__fixed-right) {
  position: sticky !important;
  right: 0 !important;
  left: auto !important;
  z-index: 9;
  background-color: #ffffff;
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}"""
new2 = """.table-host :deep(.el-table__fixed-right-wrapper),
.table-host :deep(.el-table__fixed-right) {
  z-index: 9;
  background-color: #ffffff;
  box-shadow: -8px 0 10px -8px rgba(15, 23, 42, 0.28);
}"""
assert old2 in s, "block 2 not found"
s = s.replace(old2, new2)

p.write_text(s, encoding="utf-8")
print("patched")
