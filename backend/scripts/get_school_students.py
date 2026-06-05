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

SQL_TEMPLATE = r"""
WITH student_schools AS (
  SELECT DISTINCT ON (ps.id)
    ps.id AS portal_student_id,
    ps.full_name AS student_name,
    ps.phone_number,
    ps.email,
    ps.created_at AS registered_at,
    ps.candidate_no,
    COALESCE(ue.school_name, NULLIF(BTRIM(ps.graduation_school), '')) AS school_name
  FROM dtlms_portal_students ps
  LEFT JOIN LATERAL (
    SELECT ra.id, ra.application_status, ra.created_at AS applied_at
    FROM dtlms_recruitment_applications ra
    WHERE ra.portal_student_id = ps.id AND ra.is_deleted = FALSE
    ORDER BY ra.created_at DESC, ra.id DESC
    LIMIT 1
  ) ra ON TRUE
  LEFT JOIN LATERAL (
    SELECT NULLIF(BTRIM(e.school_name), '') AS school_name, e.education_stage
    FROM dtlms_portal_application_education_experiences e
    WHERE e.application_id = ra.id
      AND e.sort_order = 2
      AND NULLIF(BTRIM(e.school_name), '') IS NOT NULL
    LIMIT 1
  ) ue ON TRUE
  WHERE (ra.application_status = '驳回重填' OR ps.submitted_at IS NOT NULL)
)
SELECT
  ss.portal_student_id,
  ss.student_name,
  ss.school_name,
  ss.candidate_no,
  ss.registered_at,
  ss.phone_number,
  ss.email,
  CASE WHEN LOWER(ss.school_name) ~ '中学|高中|初中|中专|职业|附属|附中' THEN true ELSE false END AS is_k12
FROM student_schools ss
WHERE ss.school_name LIKE %s
ORDER BY ss.registered_at DESC NULLS LAST
LIMIT 200
"""

def run_for(school_prefix: str):
    with psycopg.connect(conninfo) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(SQL_TEMPLATE, (f"{school_prefix}%",))
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
            print(f"--- Results for: {school_prefix} ---")
            print(json.dumps([serialize_row(r) for r in rows], ensure_ascii=False, indent=2))

if __name__ == '__main__':
    run_for('西安交通大学')
    run_for('上海交通大学')
