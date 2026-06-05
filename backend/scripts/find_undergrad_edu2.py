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
  e.id AS edu_id,
  e.application_id,
  e.sort_order,
  e.education_stage,
  NULLIF(BTRIM(e.school_name), '') AS school_name,
  ra.id AS recruitment_application_id,
  ra.portal_student_id,
  ps.full_name,
  ps.candidate_no,
  ra.application_status,
  ps.submitted_at,
  ra.applied_at
FROM dtlms_portal_application_education_experiences e
JOIN dtlms_recruitment_applications ra ON ra.id = e.application_id AND ra.is_deleted = FALSE
JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
WHERE e.sort_order = 2
  AND NULLIF(BTRIM(e.education_stage), '') IN ('本科在读', '本科毕业')
  AND NULLIF(BTRIM(e.school_name), '') IS NOT NULL
ORDER BY ra.id DESC
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
