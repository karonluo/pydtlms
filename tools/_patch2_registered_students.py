import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\frontend\src\views\students\RegisteredStudentsView.vue")
s = p.read_text(encoding="utf-8")

old = """.table-panel {
  padding: 10px 14px 12px;
  min-height: 0;
}"""
new = """.table-panel {
  padding: 10px 14px 12px;
  min-height: 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
}"""
assert old in s, "table-panel block not found"
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("patched table-panel")
