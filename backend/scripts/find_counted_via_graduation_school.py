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
  NULLIF(BTRIM(ps.graduation_school), '') AS graduation_school,
  ra.id AS recruitment_application_id,
  ra.application_status,
  ps.submitted_at
FROM dtlms_portal_students ps
LEFT JOIN LATERAL (
  SELECT ra2.id, ra2.application_status
  FROM dtlms_recruitment_applications ra2
  WHERE ra2.portal_student_id = ps.id AND ra2.is_deleted = FALSE
  ORDER BY COALESCE(ra2.applied_at, ra2.created_at) DESC, ra2.id DESC
  LIMIT 1
) ra ON TRUE
LEFT JOIN LATERAL (
  SELECT NULLIF(BTRIM(e.school_name), '') AS school_name
  FROM dtlms_portal_application_education_experiences e
  JOIN dtlms_recruitment_applications ra3 ON ra3.id = e.application_id
  WHERE ra3.portal_student_id = ps.id
    AND e.sort_order = 2
    AND e.education_stage IN ('本科在读', '本科毕业')
    AND NULLIF(BTRIM(e.school_name), '') IS NOT NULL
  LIMIT 1
) ue ON TRUE
WHERE (ue.school_name IS NULL OR ue.school_name = '')
  AND LOWER(ps.graduation_school) ~ '中学|高中|初中|中专|职业|附属|附中'
  AND (ra.application_status = '驳回重填' OR ps.submitted_at IS NOT NULL)
ORDER BY ps.id DESC
LIMIT 200;
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
