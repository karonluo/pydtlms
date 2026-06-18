import pathlib
p = pathlib.Path(r"D:\pyproj\pydtlms\tools\dump_public_schema.py")
s = p.read_text(encoding="utf-8")

# 1. Replace the "composites" query to filter relkind='c' (true composite type)
old = '''    out["composites"] = rows(cur, """
        SELECT t.oid, t.typname,
               array_to_json(array(
                 SELECT json_build_object('name', a.attname, 'type', pg_catalog.format_type(a.atttypid, a.atttypmod))
                   FROM pg_attribute a
                  WHERE a.attrelid = t.typrelid AND a.attnum > 0 AND NOT a.attisdropped
                  ORDER BY a.attnum
               )) AS columns
          FROM pg_type t
          JOIN pg_namespace n ON n.oid = t.typnamespace
         WHERE t.typtype = 'c' AND n.nspname = %s
         ORDER BY t.typname
    """, (SCHEMA,))'''
new = '''    out["composites"] = rows(cur, """
        SELECT t.oid, t.typname,
               (SELECT array_agg(json_build_object('name', a.attname,
                                                   'type', pg_catalog.format_type(a.atttypid, a.atttypmod))
                                 ORDER BY a.attnum)
                  FROM pg_attribute a
                 WHERE a.attrelid = t.typrelid
                   AND a.attnum > 0
                   AND NOT a.attisdropped) AS columns
          FROM pg_type t
          JOIN pg_namespace n ON n.oid = t.typnamespace
          JOIN pg_class c ON c.oid = t.typrelid
         WHERE t.typtype = 'c' AND c.relkind = 'c' AND n.nspname = %s
         ORDER BY t.typname
    """, (SCHEMA,))'''
assert old in s, "composites block not found"
s = s.replace(old, new)

# 2. The Section 2a/2b/2c emitters must early-exit when their list is empty.
# They already do (`if cat["domains"]:` etc), but in case the false-positive
# rowtypes are gone, no change needed.

p.write_text(s, encoding="utf-8")
print("patched")
