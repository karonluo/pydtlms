import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\tools\dump_public_schema.py")
s = p.read_text(encoding="utf-8")
s = s.replace(
    'cols = ", ".join(f"{col[\'name\']} {unqual(col[\'type\'])}" for col in json.loads(c["columns"]))',
    'cols = ", ".join(f"{col[\'name\']} {unqual(col[\'type\'])}" for col in c["columns"])',
)
p.write_text(s, encoding="utf-8")
print("patched")
