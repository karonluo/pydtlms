import os
import re
import json
from pathlib import Path

import psycopg

# Load simple .env-like file
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
    raise SystemExit('Missing Postgres connection info in backend/.env or environment variables')

conninfo = f"host={host} port={port} dbname={db} user={user} password={password}"

SQL = r"""
SELECT
  e.id AS edu_id,
  e.application_id,
  e.sort_order,
  e.education_stage,
  e.school_name,
  ra.id AS recruitment_application_id,
  ra.portal_student_id AS ra_portal_student_id,
  ra.application_status,
  ps.id AS portal_student_id,
  ps.full_name,
  ps.candidate_no,
  ps.created_at AS student_created_at,
  ps.submitted_at
FROM dtlms_portal_application_education_experiences e
LEFT JOIN dtlms_recruitment_applications ra ON ra.id = e.application_id
LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
WHERE e.sort_order = 2
  AND e.school_name IS NOT NULL
  AND LOWER(e.school_name) ~ '中学|高中|初中|中专|职业|附属'
ORDER BY ra.id DESC NULLS LAST
LIMIT 200
"""

with psycopg.connect(conninfo) as conn:
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(SQL)
        rows = cur.fetchall()
        print(json.dumps(rows, ensure_ascii=False, indent=2))
