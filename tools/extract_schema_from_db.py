import os
import json
from pathlib import Path
import psycopg

# load .env from backend/.env
env_path = Path(__file__).resolve().parents[1] / 'backend' / '.env'
env = {}
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip().strip('"')

host = env.get('POSTGRES_HOST') or os.environ.get('POSTGRES_HOST')
port = env.get('POSTGRES_PORT') or os.environ.get('POSTGRES_PORT', '5432')
user = env.get('POSTGRES_USER') or os.environ.get('POSTGRES_USER')
password = env.get('POSTGRES_PASSWORD') or os.environ.get('POSTGRES_PASSWORD')
db = env.get('POSTGRES_DB') or os.environ.get('POSTGRES_DB')

if not (host and port and user and password and db):
    print(json.dumps({"error": "Missing Postgres connection info"}, ensure_ascii=False))
    raise SystemExit(1)

conninfo = f"host={host} port={port} dbname={db} user={user} password={password}"

query_tables = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name
"""

query_columns = """
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = %s
ORDER BY ordinal_position
"""

# foreign keys from pg_catalog
query_fks = """
SELECT
  tc.constraint_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public' AND tc.table_name = %s
"""

result = {"tables": {}}

try:
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(query_tables)
            tables = [r[0] for r in cur.fetchall()]
            for t in tables:
                cur.execute(query_columns, (t,))
                cols = []
                for col in cur.fetchall():
                    cols.append({
                        "name": col[0],
                        "data_type": col[1],
                        "is_nullable": col[2],
                        "default": col[3],
                    })
                cur.execute("SELECT kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema='public' AND tc.table_name=%s", (t,))
                pks = [r[0] for r in cur.fetchall()]
                cur.execute(query_fks, (t,))
                fks = []
                for fk in cur.fetchall():
                    fks.append({
                        "constraint_name": fk[0],
                        "column": fk[1],
                        "ref_table": fk[2],
                        "ref_column": fk[3],
                    })
                result["tables"][t] = {
                    "columns": cols,
                    "primary_key": pks,
                    "foreign_keys": fks,
                }
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e)} , ensure_ascii=False))
    raise
