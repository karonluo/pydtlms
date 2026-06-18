import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\frontend\src\views\students\RegisteredStudentsView.vue")
s = p.read_text(encoding="utf-8")

# Ensure the grid container also doesn't let the column blow out to 1880px.
old = """.registered-students-page {
  display: grid;
  gap: 12px;
  min-height: 0;
}"""
new = """.registered-students-page {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
  min-height: 0;
  width: 100%;
  min-width: 0;
}"""
assert old in s, "registered-students-page not found"
s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("patched")
