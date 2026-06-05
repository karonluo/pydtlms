import os
import json
from pathlib import Path

# load .env
env_path = Path('backend/.env')
if not env_path.exists():
    print('backend/.env not found:', env_path)
    raise SystemExit(1)

env = {}
with env_path.open('r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip().strip('"')

host = env.get('POSTGRES_HOST', 'localhost')
port = env.get('POSTGRES_PORT', '5432')
db = env.get('POSTGRES_DB')
user = env.get('POSTGRES_USER')
password = env.get('POSTGRES_PASSWORD')

if not db:
    print('POSTGRES_DB not set in backend/.env')
    raise SystemExit(2)

# try psycopg (psycopg3) then psycopg2
conn = None
try:
    import psycopg
    conn = psycopg.connect(host=host, port=port, dbname=db, user=user, password=password)
except Exception:
    try:
        import psycopg2
        conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
    except Exception as e:
        print('failed to import/connect with psycopg/psycopg2:', e)
        raise

cur = conn.cursor()
# get tables in public schema
cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE'
ORDER BY table_name
""")
rows = cur.fetchall()
tables = [r[0] for r in rows]

schema = {}
for t in tables:
    # columns
    cur.execute(
        """
        SELECT column_name, data_type, is_nullable, column_default, ordinal_position
        FROM information_schema.columns
        WHERE table_schema='public' AND table_name=%s
        ORDER BY ordinal_position
        """,
        (t,)
    )
    cols = []
    for col_name, data_type, is_nullable, column_default, ordpos in cur.fetchall():
        cols.append({
            'name': col_name,
            'data_type': data_type,
            'is_nullable': is_nullable,
            'default': column_default
        })
    # primary key
    cur.execute(
        """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema='public' AND tc.table_name=%s
        ORDER BY kcu.ordinal_position
        """,
        (t,)
    )
    pk = [r[0] for r in cur.fetchall()]
    # foreign keys
    cur.execute(
        """
        SELECT
          kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name, tc.constraint_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema='public' AND tc.table_name=%s
        """,
        (t,)
    )
    fks = []
    for col_name, f_table, f_col, constraint in cur.fetchall():
        fks.append({
            'constraint_name': constraint,
            'column': col_name,
            'ref_table': f_table,
            'ref_column': f_col
        })
    schema[t] = {
        'columns': cols,
        'primary_key': pk,
        'foreign_keys': fks
    }

# write json and md
out_json = Path('documents/test25_schema_full.json')
out_md = Path('documents/test25_schema_full.md')
out_json.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding='utf-8')

lines = ['# test25 schema (full export)']
for table, meta in sorted(schema.items()):
    lines.append(f'## {table}')
    lines.append('| Column | Type | Nullable | Default |')
    lines.append('|---|---|---|---|')
    for c in meta['columns']:
        name = c['name'].replace('|', '\\|')
        typ = c['data_type'].replace('|', '\\|')
        nul = c['is_nullable']
        default = '' if c['default'] is None else str(c['default']).replace('|', '\\|')
        lines.append(f'| {name} | {typ} | {nul} | {default} |')
    if meta['primary_key']:
        lines.append('**Primary key:** ' + ', '.join(meta['primary_key']))
    if meta['foreign_keys']:
        lines.append('**Foreign keys:**')
        for fk in meta['foreign_keys']:
            lines.append(f"- {fk['column']} -> {fk['ref_table']}.{fk['ref_column']}  ({fk['constraint_name']})")
    lines.append('')

out_md.write_text('\n'.join(lines), encoding='utf-8')
print('wrote', out_json, 'and', out_md)

cur.close()
conn.close()
