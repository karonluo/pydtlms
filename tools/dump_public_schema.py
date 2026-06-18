# -*- coding: utf-8 -*-
"""
Dump PostgreSQL public schema DDL for the test061502 database.

Output: documents/数据库结构/数据库构建详情.sql

Sections (dependency-safe order):
  1. SET search_path + extensions
  2. Custom types (composite, enum, range, domain)
  3. Sequences
  4. Tables (FK topo-sorted) with inlined PK / UNIQUE / CHECK
  5. ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY  (separate ALTER block)
  6. Views / Materialized views
  7. Non-constraint indexes
  8. Functions / procedures
  9. Triggers
 10. Comments (table, column)
"""

from __future__ import annotations

import os
import sys
import textwrap
from collections import defaultdict
from datetime import datetime

import psycopg2
import psycopg2.extras

DB = dict(
    host="47.117.107.23",
    port=15431,
    user="postgres",
    password="Pass@@word123!",
    dbname="test061502",
    connect_timeout=15,
)
SCHEMA = "public"
OUT_PATH = r"D:\pyproj\pydtlms\documents\数据库结构\数据库构建详情.sql"


def wrap(s: str) -> str:
    return "\n".join("-- " + line for line in textwrap.wrap(s, 120)) or "--"


def rows(cur, sql, params=()):
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def unqual(typ: str) -> str:
    """Strip schema qualifier from regclass/regtype output to keep SQL compact."""
    if typ and "." in typ:
        return typ.split(".", 1)[1]
    return typ


# --------------------------------------------------------------------------- #
# Catalog snapshots
# --------------------------------------------------------------------------- #

def snapshot(cur):
    out = {}

    out["extensions"] = rows(cur, """
        SELECT e.extname, n.nspname AS schema
          FROM pg_extension e
          JOIN pg_namespace n ON n.oid = e.extnamespace
         WHERE n.nspname NOT IN ('pg_catalog')
         ORDER BY e.extname
    """)

    out["enums"] = rows(cur, """
        SELECT t.oid, t.typname,
               array(
                 SELECT e.enumlabel
                   FROM pg_enum e
                  WHERE e.enumtypid = t.oid
                  ORDER BY e.enumsortorder
               ) AS labels
          FROM pg_type t
          JOIN pg_namespace n ON n.oid = t.typnamespace
         WHERE t.typtype = 'e' AND n.nspname = %s
         ORDER BY t.typname
    """, (SCHEMA,))

    out["composites"] = rows(cur, """
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
    """, (SCHEMA,))

    out["domains"] = rows(cur, """
        SELECT t.oid, t.typname,
               pg_catalog.format_type(t.typbasetype, t.typtypmod) AS basetype,
               t.typnotnull AS notnull,
               t.typdefault AS default_expr,
               (SELECT array_agg(c.contype) FROM pg_constraint c WHERE c.contypid = t.oid) AS constraint_kinds
          FROM pg_type t
          JOIN pg_namespace n ON n.oid = t.typnamespace
         WHERE t.typtype = 'd' AND n.nspname = %s
         ORDER BY t.typname
    """, (SCHEMA,))

    out["sequences"] = rows(cur, """
        SELECT c.relname,
               (SELECT format_type(s.seqtypid, NULL) FROM pg_sequence s WHERE s.seqrelid = c.oid) AS data_type,
               (SELECT s.seqstart FROM pg_sequence s WHERE s.seqrelid = c.oid) AS start_value,
               (SELECT s.seqincrement FROM pg_sequence s WHERE s.seqrelid = c.oid) AS increment_by,
               (SELECT s.seqmax FROM pg_sequence s WHERE s.seqrelid = c.oid) AS max_value,
               (SELECT s.seqmin FROM pg_sequence s WHERE s.seqrelid = c.oid) AS min_value,
               (SELECT s.seqcache FROM pg_sequence s WHERE s.seqrelid = c.oid) AS cache_size,
               (SELECT s.seqcycle FROM pg_sequence s WHERE s.seqrelid = c.oid) AS is_cycled
          FROM pg_class c
          JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE c.relkind = 'S' AND n.nspname = %s
         ORDER BY c.relname
    """, (SCHEMA,))

    out["tables"] = rows(cur, """
        SELECT c.oid, c.relname, c.relkind
          FROM pg_class c
          JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE c.relkind IN ('r', 'p') AND n.nspname = %s
         ORDER BY c.relname
    """, (SCHEMA,))

    out["columns"] = rows(cur, """
        SELECT c.relname AS tablename,
               a.attname,
               a.attnum,
               a.atttypid,
               a.atttypmod,
               a.attnotnull,
               t.typname AS base_typname,
               t.typtype,
               pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
               pg_catalog.pg_get_expr(d.adbin, d.adrelid) AS default_expr,
               t.typname IN ('int2','int4','int8','oid','float4','float8','numeric','serial') AS is_numeric,
               EXISTS (
                 SELECT 1 FROM pg_type sub WHERE sub.typtype IN ('e','c','d') AND sub.oid = a.atttypid
               ) AS is_udt
          FROM pg_attribute a
          JOIN pg_class c      ON c.oid = a.attrelid
          JOIN pg_namespace n  ON n.oid = c.relnamespace
          JOIN pg_type t       ON t.oid = a.atttypid
          LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
         WHERE a.attnum > 0
           AND NOT a.attisdropped
           AND n.nspname = %s
         ORDER BY c.relname, a.attnum
    """, (SCHEMA,))

    out["constraints"] = rows(cur, """
        SELECT con.oid, con.conname, con.contype,
               con.conrelid::regclass::text AS tablename,
               con.confrelid::regclass::text AS fk_target,
               pg_get_constraintdef(con.oid) AS def
          FROM pg_constraint con
          JOIN pg_namespace n ON n.oid = con.connamespace
         WHERE n.nspname = %s
           AND con.contype IN ('p','u','c','f','x')
         ORDER BY con.conrelid::regclass::text,
                  array_position(ARRAY['p'::text,'u'::text,'c'::text,'x'::text,'f'::text], con.contype::text),
                  con.conname
    """, (SCHEMA,))

    out["constraint_cols"] = rows(cur, """
        SELECT con.conname,
               con.contype,
               con.conrelid::regclass::text AS tablename,
               (
                 SELECT array_agg(a.attname ORDER BY array_position(con.conkey, a.attnum))
                   FROM unnest(con.conkey) AS u(attnum)
                   JOIN pg_attribute a ON a.attrelid = con.conrelid AND a.attnum = u.attnum
               ) AS cols,
               (
                 SELECT array_agg(af.attname ORDER BY ord.pos)
                   FROM unnest(con.confkey) WITH ORDINALITY AS ord(attnum, pos)
                   JOIN pg_attribute af ON af.attrelid = con.confrelid AND af.attnum = ord.attnum
                  WHERE con.contype = 'f'
               ) AS fk_cols
          FROM pg_constraint con
          JOIN pg_namespace n ON n.oid = con.connamespace
         WHERE n.nspname = %s
    """, (SCHEMA,))

    out["indexes"] = rows(cur, """
        SELECT n.nspname, c.relname AS indexname,
               t.relname AS tablename,
               pg_get_indexdef(i.indexrelid, 0, true) AS def,
               am.amname AS access_method
          FROM pg_index i
          JOIN pg_class c      ON c.oid = i.indexrelid
          JOIN pg_class t      ON t.oid = i.indrelid
          JOIN pg_namespace n  ON n.oid = c.relnamespace
          JOIN pg_am am        ON am.oid = c.relam
         WHERE n.nspname = %s
           AND NOT EXISTS (SELECT 1 FROM pg_constraint con
                            WHERE con.conindid = i.indexrelid
                              AND con.contype IN ('p','u','x'))
         ORDER BY t.relname, c.relname
    """, (SCHEMA,))

    out["views"] = rows(cur, """
        SELECT c.oid, c.relname, c.relkind
          FROM pg_class c
          JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE c.relkind IN ('v','m') AND n.nspname = %s
         ORDER BY c.relname
    """, (SCHEMA,))

    out["routines"] = rows(cur, """
        SELECT p.oid, p.proname,
               p.prokind,
               pg_get_function_identity_arguments(p.oid) AS identity_args,
               pg_get_functiondef(p.oid) AS body
          FROM pg_proc p
          JOIN pg_namespace n ON n.oid = p.pronamespace
         WHERE n.nspname = %s
           AND p.prokind IN ('f','p')
         ORDER BY p.proname, p.oid::text
    """, (SCHEMA,))

    out["triggers"] = rows(cur, """
        SELECT t.tgname, c.relname AS tablename,
               pg_get_triggerdef(t.oid, true) AS def
          FROM pg_trigger t
          JOIN pg_class c      ON c.oid = t.tgrelid
          JOIN pg_namespace n  ON n.oid = c.relnamespace
         WHERE NOT t.tgisinternal
           AND n.nspname = %s
         ORDER BY c.relname, t.tgname
    """, (SCHEMA,))

    out["table_comments"] = rows(cur, """
        SELECT c.relname, d.description
          FROM pg_class c
          JOIN pg_namespace n ON n.oid = c.relnamespace
          LEFT JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = 0
         WHERE n.nspname = %s AND d.description IS NOT NULL
         ORDER BY c.relname
    """, (SCHEMA,))

    out["column_comments"] = rows(cur, """
        SELECT c.relname AS tablename, a.attname AS columnname, d.description
          FROM pg_description d
          JOIN pg_class c     ON c.oid = d.objoid
          JOIN pg_attribute a ON a.attrelid = d.objoid AND a.attnum = d.objsubid
          JOIN pg_namespace n ON n.oid = c.relnamespace
         WHERE n.nspname = %s
           AND d.objsubid > 0
         ORDER BY c.relname, a.attnum
    """, (SCHEMA,))

    return out


# --------------------------------------------------------------------------- #
# Emitters
# --------------------------------------------------------------------------- #

def emit_extensions(buf, cat):
    if not cat["extensions"]:
        return
    buf.append(wrap("Section 1: Required PostgreSQL extensions."))
    for e in cat["extensions"]:
        buf.append(f"CREATE EXTENSION IF NOT EXISTS {e['extname']} WITH SCHEMA {e['schema']};")
    buf.append("")


def emit_types(buf, cat):
    if cat["domains"]:
        buf.append(wrap("Section 2a: DOMAINs (must be created before columns that use them)."))
        for d in cat["domains"]:
            null = " NOT NULL" if d["notnull"] else ""
            default = f" DEFAULT {d['default_expr']}" if d["default_expr"] else ""
            buf.append(f"CREATE DOMAIN {d['typname']} AS {unqual(d['basetype'])}{null}{default};")
        buf.append("")
    if cat["enums"]:
        buf.append(wrap("Section 2b: ENUM types."))
        for e in cat["enums"]:
            labels = ", ".join(f"'{l.replace(chr(39), chr(39)+chr(39))}'" for l in e["labels"])
            buf.append(f"CREATE TYPE {e['typname']} AS ENUM ({labels});")
        buf.append("")
    if cat["composites"]:
        buf.append(wrap("Section 2c: Composite types."))
        import json
        for c in cat["composites"]:
            cols = ", ".join(f"{col['name']} {unqual(col['type'])}" for col in c["columns"])
            buf.append(f"CREATE TYPE {c['typname']} AS ({cols});")
        buf.append("")


def emit_sequences(buf, cat):
    if not cat["sequences"]:
        return
    buf.append(wrap("Section 3: Sequences (CREATE SEQUENCE statements)."))
    for s in cat["sequences"]:
        cyc = "CYCLE" if s["is_cycled"] else "NO CYCLE"
        buf.append(
            f"CREATE SEQUENCE {s['relname']}\n"
            f"    AS {unqual(s['data_type'])}\n"
            f"    INCREMENT BY {s['increment_by']}\n"
            f"    MINVALUE {s['min_value']}\n"
            f"    MAXVALUE {s['max_value']}\n"
            f"    START WITH {s['start_value']}\n"
            f"    CACHE {s['cache_size']}\n"
            f"    {cyc};"
        )
    buf.append("")


def topo_tables(cat):
    table_names = [t["relname"] for t in cat["tables"]]
    fk_deps = defaultdict(set)
    for c in cat["constraints"]:
        if c["contype"] != "f":
            continue
        child = unqual(c["tablename"])
        parent = unqual(c["fk_target"]) if c["fk_target"] else None
        if not parent or parent == child:
            continue
        fk_deps[child].add(parent)

    out, visited, in_stack = [], set(), set()
    def visit(n):
        if n in visited or n in in_stack:
            return
        in_stack.add(n)
        for p in fk_deps.get(n, ()):
            if p in table_names:
                visit(p)
        in_stack.discard(n)
        visited.add(n)
        out.append(n)
    for t in table_names:
        visit(t)
    return out


def fmt_default(col, con_cols):
    """Build the column line for CREATE TABLE."""
    pieces = [col["attname"], col["data_type"]]
    if not col["is_udt"] and "." in col["data_type"]:
        pieces[1] = unqual(col["data_type"])
    if col["attnotnull"]:
        pieces.append("NOT NULL")
    if col["default_expr"]:
        pieces.append(f"DEFAULT {col['default_expr']}")
    return " ".join(pieces)


def emit_tables(buf, cat):
    table_order = topo_tables(cat)
    if not table_order:
        return
    buf.append(wrap("Section 4: Tables (FK dependency order). PK / UNIQUE / CHECK constraints inlined; FK emitted later as ALTER TABLE."))

    cols_by_table: dict[str, list[dict]] = defaultdict(list)
    for c in cat["columns"]:
        cols_by_table[c["tablename"]].append(c)
    cons_by_table: dict[str, list[dict]] = defaultdict(list)
    for c in cat["constraints"]:
        cons_by_table[c["tablename"]].append(c)

    for tname in table_order:
        cols = cols_by_table.get(tname, [])
        if not cols:
            continue
        lines = [f"CREATE TABLE {tname} ("]
        col_lines = []
        for c in cols:
            col_lines.append("    " + fmt_default(c, None))
        for k in cons_by_table.get(tname, []):
            if k["contype"] in ("p", "u", "c", "x"):
                col_lines.append("    " + k["def"])
        # strip final comma; keep it inside the join below
        body = ",\n".join(col_lines)
        lines.append(body)
        lines.append(");")
        buf.append("\n".join(lines))
        buf.append("")
    buf.append("")


def emit_fks(buf, cat):
    fks = [k for k in cat["constraints"] if k["contype"] == "f"]
    if not fks:
        return
    buf.append(wrap("Section 5: Foreign key constraints (ALTER TABLE)."))
    for k in fks:
        buf.append(f"ALTER TABLE {unqual(k['tablename'])} ADD CONSTRAINT {k['conname']} {k['def']};")
    buf.append("")


def emit_views(buf, cat):
    if not cat["views"]:
        return
    buf.append(wrap("Section 6: Views and materialized views."))
    for v in cat["views"]:
        cur.execute("SELECT pg_catalog.pg_get_viewdef(%s::oid, true)", (v["oid"],))
        body = cur.fetchone()[0]
        keyword = "CREATE MATERIALIZED VIEW" if v["relkind"] == "m" else "CREATE VIEW"
        buf.append(f"{keyword} {v['relname']} AS")
        buf.append(body.rstrip().rstrip(";") + ";")
        buf.append("")


def emit_indexes(buf, cat):
    if not cat["indexes"]:
        return
    buf.append(wrap("Section 7: Non-constraint indexes (PK/UNIQUE indexes are emitted as part of the table definition)."))
    for ix in cat["indexes"]:
        buf.append(ix["def"].rstrip().rstrip(";") + ";")
    buf.append("")


def emit_routines(buf, cat):
    if not cat["routines"]:
        return
    buf.append(wrap("Section 8: Functions and procedures."))
    for r in cat["routines"]:
        buf.append(r["body"].rstrip())
        kind = "FUNCTION" if r["prokind"] == "f" else "PROCEDURE"
        args = r["identity_args"] or ""
        buf.append(f"ALTER {kind} {r['proname']}({args}) SET search_path = public, pg_catalog;")
        buf.append("")


def emit_triggers(buf, cat):
    if not cat["triggers"]:
        return
    buf.append(wrap("Section 9: Triggers."))
    for t in cat["triggers"]:
        buf.append(t["def"].rstrip().rstrip(";") + ";")
    buf.append("")


def emit_comments(buf, cat):
    if cat["table_comments"]:
        buf.append(wrap("Section 10a: Table comments."))
        for c in cat["table_comments"]:
            d = c["description"].replace("'", "''")
            buf.append(f"COMMENT ON TABLE {c['relname']} IS '{d}';")
        buf.append("")
    if cat["column_comments"]:
        buf.append(wrap("Section 10b: Column comments."))
        for c in cat["column_comments"]:
            if c["description"] is None:
                continue
            d = c["description"].replace("'", "''")
            buf.append(f"COMMENT ON COLUMN {c['tablename']}.{c['columnname']} IS '{d}';")
        buf.append("")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    global cur
    conn = psycopg2.connect(**DB)
    conn.set_session(readonly=True, autocommit=True)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT version(), current_database(), current_schema()")
    pg_version, cur_db, cur_schema = cur.fetchone()
    assert cur_schema == SCHEMA, f"connected to schema {cur_schema!r}"

    cat = snapshot(cur)

    buf: list[str] = []
    buf.append("=" * 79)
    buf.append(f"-- DTLMS public schema  --  generated {datetime.now():%Y-%m-%d %H:%M:%S}")
    buf.append(f"-- Server : {pg_version}")
    buf.append(f"-- Database: {cur_db}")
    buf.append(f"-- Schema  : {SCHEMA}")
    buf.append("=" * 79)
    buf.append("")
    buf.append("SET search_path = public, pg_catalog;")
    buf.append("")

    emit_extensions(buf, cat)
    emit_types(buf, cat)
    emit_sequences(buf, cat)
    emit_tables(buf, cat)
    emit_fks(buf, cat)
    emit_views(buf, cat)
    emit_indexes(buf, cat)
    emit_routines(buf, cat)
    emit_triggers(buf, cat)
    emit_comments(buf, cat)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    final_sql = "\n".join(buf) + "\n"
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(final_sql)

    print(f"tables      : {len(cat['tables'])}")
    print(f"views       : {sum(1 for v in cat['views'] if v['relkind']=='v')}")
    print(f"mat_views   : {sum(1 for v in cat['views'] if v['relkind']=='m')}")
    print(f"indexes     : {len(cat['indexes'])}")
    print(f"constraints : {len(cat['constraints'])}")
    print(f"triggers    : {len(cat['triggers'])}")
    print(f"routines    : {len(cat['routines'])}")
    print(f"types       : {len(cat['enums']) + len(cat['composites']) + len(cat['domains'])}")
    print(f"sequences   : {len(cat['sequences'])}")
    print(f"out_path    : {OUT_PATH}")
    print(f"out_bytes   : {os.path.getsize(OUT_PATH)}")
    print(f"out_lines   : {final_sql.count(chr(10))+1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

