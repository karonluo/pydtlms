import os
import json
from pathlib import Path
import psycopg

# load .env
env_path = Path(__file__).resolve().parents[0] / '..' / '.env'
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
    raise SystemExit('Missing Postgres connection info')

conninfo = f"host={host} port={port} dbname={db} user={user} password={password}"

SQL = r"""
SELECT
  ps.id AS portal_student_id,
  ps.full_name,
  ps.candidate_no,
  ps.graduation_school,
  ps.created_at,
  ps.submitted_at
FROM dtlms_portal_students ps
WHERE ps.graduation_school IS NOT NULL
  AND LOWER(ps.graduation_school) ~ '中学|高中|初中|中专|职业|附属|附中'
ORDER BY ps.created_at DESC NULLS LAST
LIMIT 200
"""

with psycopg.connect(conninfo) as conn:
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(SQL)
        rows = cur.fetchall()
        def serialize_row(r: dict):
          out = {}
          for k, v in r.items():
            if hasattr(v, 'isoformat'):
              try:
                out[k] = v.isoformat()
              except Exception:
                out[k] = str(v)
            else:
              out[k] = v
          return out

        serial = [serialize_row(r) for r in rows]
        print(json.dumps(serial, ensure_ascii=False, indent=2))
