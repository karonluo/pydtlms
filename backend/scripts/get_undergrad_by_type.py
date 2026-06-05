import os
import sys
import json
from pathlib import Path
import psycopg

if len(sys.argv) < 2:
    print('Usage: python get_undergrad_by_type.py <dict_type>')
    sys.exit(2)

dict_type = sys.argv[1]

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

SQL = f"""
WITH dictionary_schools AS (
  SELECT NULLIF(BTRIM(d.label), '') AS school_name, d.sort_order
  FROM dtlms_dict_types t
  JOIN dtlms_dict_data d ON d.dict_type_id = t.id AND d.dict_type = t.dict_type
  WHERE t.dict_type = %s AND d.status = '启用' AND NULLIF(BTRIM(d.label),'') IS NOT NULL
),
student_schools AS (
  SELECT DISTINCT ON (ps.id)
    ps.id AS portal_student_id,
    ps.full_name,
    ps.candidate_no,
    ps.created_at,
    ps.submitted_at,
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
    SELECT NULLIF(BTRIM(e.school_name), '') AS school_name
    FROM dtlms_portal_application_education_experiences e
    WHERE e.application_id = ra.id
      AND e.sort_order = 2
      AND NULLIF(BTRIM(e.education_stage), '') IN ('本科在读', '本科毕业')
      AND NULLIF(BTRIM(e.school_name), '') IS NOT NULL
    LIMIT 1
  ) ue ON TRUE
  WHERE (ra.application_status = '驳回重填' OR ps.submitted_at IS NOT NULL)
),
school_counts AS (
  SELECT ds.school_name, ds.sort_order, COUNT(ss.portal_student_id)::int AS student_count
  FROM dictionary_schools ds
  LEFT JOIN student_schools ss ON ss.school_name LIKE ds.school_name || '%%' 
    AND NOT (
      ss.school_name ILIKE '%%中学%%' OR ss.school_name ILIKE '%%高中%%' OR ss.school_name ILIKE '%%初中%%' OR ss.school_name ILIKE '%%中专%%' OR ss.school_name ILIKE '%%职业学校%%'
    )
  GROUP BY ds.school_name, ds.sort_order
)
SELECT sc.school_name, sc.student_count
FROM school_counts sc
ORDER BY sc.student_count DESC, sc.sort_order ASC, sc.school_name ASC
LIMIT 20;
"""

with psycopg.connect(conninfo) as conn:
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(SQL, (dict_type,))
        rows = cur.fetchall()
        print(json.dumps(rows, ensure_ascii=False, indent=2))
