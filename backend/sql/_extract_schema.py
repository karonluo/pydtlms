import sys, pathlib
import psycopg

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / "backend" / ".env"
OUT = pathlib.Path(__file__).resolve().parent / "database_schema.md"

def _parse_env(path: pathlib.Path) -> dict:
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg

env = _parse_env(ENV_PATH)
host = env.get("POSTGRES_HOST", "127.0.0.1")
port = int(env.get("POSTGRES_PORT", "5432"))
user = env.get("POSTGRES_USER", "postgres")
password = env.get("POSTGRES_PASSWORD", "")
dbname = env.get("POSTGRES_DB", "postgres")
schema = env.get("POSTGRES_SCHEMA", "public")

def main():
    with psycopg.connect(host=host, port=port, user=user, password=password, dbname=dbname) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name,
                       obj_description((%s || '.' || table_name)::regclass, 'pg_class') AS comment
                FROM information_schema.tables
                WHERE table_schema = %s AND table_type = 'BASE TABLE'
                ORDER BY table_name
                """,
                (schema, schema),
            )
            tables = cur.fetchall()

            cur.execute(
                """
                SELECT table_name,
                       obj_description((%s || '.' || table_name)::regclass, 'pg_class') AS comment
                FROM information_schema.views
                WHERE table_schema = %s
                ORDER BY table_name
                """,
                (schema, schema),
            )
            views = cur.fetchall()

            cur.execute(
                """
                SELECT p.proname,
                       pg_get_function_identity_arguments(p.oid) AS args,
                       pg_get_function_result(p.oid) AS rettype,
                       obj_description(p.oid, 'pg_proc') AS comment
                FROM pg_proc p
                JOIN pg_namespace n ON n.oid = p.pronamespace
                WHERE n.nspname = %s
                ORDER BY p.proname
                """,
                (schema,),
            )
            funcs = cur.fetchall()

            cur.execute(
                """
                SELECT sequence_name, data_type
                FROM information_schema.sequences
                WHERE sequence_schema = %s
                ORDER BY sequence_name
                """,
                (schema,),
            )
            seqs = cur.fetchall()

            cur.execute(
                """
                SELECT t.typname, t.typtype,
                       array_agg(e.enumlabel ORDER BY e.enumsortorder) AS labels
                FROM pg_type t
                LEFT JOIN pg_enum e ON e.enumtypid = t.oid
                JOIN pg_namespace n ON n.oid = t.typnamespace
                WHERE n.nspname = %s
                  AND t.typtype IN ('e', 'c')
                GROUP BY t.typname, t.typtype
                ORDER BY t.typname
                """,
                (schema,),
            )
            enums = cur.fetchall()

            cur.execute(
                """
                SELECT tablename, indexname, indexdef
                FROM pg_indexes
                WHERE schemaname = %s
                ORDER BY tablename, indexname
                """,
                (schema,),
            )
            idxs = cur.fetchall()

            cur.execute(
                """
                SELECT event_object_table, trigger_name,
                       action_timing, event_manipulation, action_statement
                FROM information_schema.triggers
                WHERE event_object_schema = %s
                ORDER BY event_object_table, trigger_name
                """,
                (schema,),
            )
            trigs = cur.fetchall()

            cur.execute(
                """
                SELECT tc.table_name, tc.constraint_name, tc.constraint_type,
                       pg_get_constraintdef(c.oid) AS definition
                FROM information_schema.table_constraints tc
                JOIN pg_constraint c ON c.conname = tc.constraint_name
                WHERE tc.table_schema = %s
                ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name
                """,
                (schema,),
            )
            cons = cur.fetchall()

            cons_by_table = {}
            for tname, cname, ctype, cdef in cons:
                cons_by_table.setdefault(tname, []).append((cname, ctype, cdef))

            idx_by_table = {}
            for tbl, iname, idef in idxs:
                idx_by_table.setdefault(tbl, []).append((iname, idef))

            trig_by_table = {}
            for et, tn, at, em, st in trigs:
                trig_by_table.setdefault(et, []).append((tn, at, em, st))

            L = []
            L.append("# 数据库 Schema 文档")
            L.append("")
            L.append("> 自动生成，请勿手工修改。下次数据库结构变更后再次运行 `backend/sql/_extract_schema.py` 重新生成。")
            L.append("")
            L.append(f"- 数据源: `host={host} port={port} dbname={dbname}`")
            L.append(f"- Schema: `{schema}`")
            L.append(f"- 表格数量: {len(tables)}")
            L.append(f"- 视图数量: {len(views)}")
            L.append(f"- 函数/存储过程数量: {len(funcs)}")
            L.append(f"- 序列数量: {len(seqs)}")
            L.append(f"- 索引数量: {len(idxs)}")
            L.append("")
            L.append("## 目录")
            L.append("")
            L.append("- [表（Tables）](#表tables)")
            L.append("- [视图（Views）](#视图views)")
            L.append("- [枚举/复合类型（Enums / Composite Types）](#枚举复合类型enums--composite-types)")
            L.append("- [序列（Sequences）](#序列sequences)")
            L.append("- [函数 / 存储过程（Functions）](#函数--存储过程functions)")
            L.append("- [索引（Indexes）](#索引indexes)")
            L.append("- [触发器（Triggers）](#触发器triggers)")
            L.append("- [表级约束（Table Constraints）](#表级约束table-constraints)")
            L.append("")

            L.append("## 表（Tables）")
            L.append("")
            for tname, comment in tables:
                L.append(f"### `{tname}`")
                L.append("")
                if comment:
                    L.append(f"> {comment}")
                    L.append("")
                cur.execute(
                    """
                    SELECT a.attname,
                           pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                           (NOT a.attnotnull) AS is_nullable,
                           pg_get_expr(d.adbin, d.adrelid) AS column_default,
                           col_description(a.attrelid, a.attnum) AS column_comment
                    FROM pg_attribute a
                    LEFT JOIN pg_attrdef d
                      ON d.adrelid = a.attrelid AND d.adnum = a.attnum
                    WHERE a.attrelid = (pg_catalog.quote_ident(%s) || '.' || pg_catalog.quote_ident(%s))::regclass
                      AND a.attnum > 0
                      AND NOT a.attisdropped
                    ORDER BY a.attnum
                    """,
                    (schema, tname),
                )
                cols = cur.fetchall()
                L.append("| 列名 | 数据类型 | 可空 | 默认值 | 说明 |")
                L.append("|------|----------|------|--------|------|")
                for cname, ctype, nullable, cdef, ccomment in cols:
                    # pg_format_type 已带 (length)/(precision,scale), 无需二次加工
                    dt = ctype or ''
                    nullable_mark = 'YES' if nullable else 'NO'
                    # Markdown 表格里换行 / 竖线 / 反引号要转义, 避免破表
                    safe_comment = (ccomment or '').replace('|', '\\|').replace(chr(13), ' ').replace(chr(10), ' ')
                    safe_default = (cdef or '').replace('|', '\\|').replace(chr(13), ' ').replace(chr(10), ' ')
                    L.append(f"| `{cname}` | {dt} | {nullable_mark} | {safe_default} | {safe_comment} |")
                L.append("")
                cur.execute(
                    """
                    SELECT a.attname
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                    WHERE i.indrelid = (%s || '.' || %s)::regclass AND i.indisprimary
                    ORDER BY array_position(i.indkey, a.attnum)
                    """,
                    (schema, tname),
                )
                pk_rows = [r[0] for r in cur.fetchall()]
                if pk_rows:
                    L.append(f"**主键**: ({', '.join('`'+c+'`' for c in pk_rows)})")
                if tname in cons_by_table:
                    L.append("")
                    L.append("**约束**")
                    L.append("")
                    L.append("| 名称 | 类型 | 定义 |")
                    L.append("|------|------|------|")
                    for cname, ctype, cdef in cons_by_table[tname]:
                        cdef_short = cdef.replace("\n", " ")
                        L.append(f"| `{cname}` | {ctype} | `{cdef_short}` |")
                if tname in idx_by_table:
                    L.append("")
                    L.append("**索引**")
                    L.append("")
                    for iname, idef in idx_by_table[tname]:
                        L.append(f"- `{iname}`: `{idef}`")
                if tname in trig_by_table:
                    L.append("")
                    L.append("**触发器**")
                    L.append("")
                    for tn, at, em, st in trig_by_table[tname]:
                        st_short = st.replace("EXECUTE FUNCTION", "→")
                        L.append(f"- `{tn}` ({at} {em}): `{st_short}`")
                L.append("")

            L.append("## 视图（Views）")
            L.append("")
            for vname, comment in views:
                L.append(f"### `{vname}`")
                L.append("")
                if comment:
                    L.append(f"> {comment}")
                    L.append("")
                cur.execute(
                    """
                    SELECT view_definition
                    FROM information_schema.views
                    WHERE table_schema = %s AND table_name = %s
                    """,
                    (schema, vname),
                )
                row = cur.fetchone()
                if row:
                    L.append("```sql")
                    L.append(row[0])
                    L.append("```")
                L.append("")

            L.append("## 枚举/复合类型（Enums / Composite Types）")
            L.append("")
            for tname, typtype, labels in enums:
                if typtype == 'e':
                    L.append(f"- `{tname}` (enum): {', '.join(labels or [])}")
                else:
                    L.append(f"- `{tname}` (composite)")
            L.append("")

            L.append("## 序列（Sequences）")
            L.append("")
            for sname, dtype in seqs:
                L.append(f"- `{sname}` ({dtype})")
            L.append("")

            L.append("## 函数 / 存储过程（Functions）")
            L.append("")
            for fname, args, rettype, comment in funcs:
                L.append(f"### `{fname}({args})` → `{rettype}`")
                L.append("")
                if comment:
                    L.append(f"> {comment}")
                    L.append("")
                cur.execute(
                    """
                    SELECT pg_get_functiondef(p.oid)
                    FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
                    WHERE n.nspname = %s AND p.proname = %s
                      AND pg_get_function_identity_arguments(p.oid) = %s
                    LIMIT 1
                    """,
                    (schema, fname, args),
                )
                row = cur.fetchone()
                if row:
                    L.append("```sql")
                    L.append(row[0])
                    L.append("```")
                L.append("")

            L.append("## 索引（Indexes）")
            L.append("")
            for tbl, iname, idef in idxs:
                L.append(f"- `{tbl}.{iname}`: `{idef}`")
            L.append("")

            L.append("## 触发器（Triggers）")
            L.append("")
            for et, tn, at, em, st in trigs:
                L.append(f"- `{et}.{tn}`: {at} {em} → `{st}`")
            L.append("")

            L.append("## 表级约束（Table Constraints）")
            L.append("")
            for tname, cname, ctype, cdef in cons:
                cdef_short = cdef.replace("\n", " ")
                L.append(f"- `{tname}.{cname}` ({ctype}): `{cdef_short}`")
            L.append("")

    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
