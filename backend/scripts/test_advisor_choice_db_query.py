import os
import psycopg
from pathlib import Path

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

sql = """
WITH prefs AS (
    SELECT
        pp.preference_order,
        NULLIF(BTRIM(pp.advisor_name), '') AS advisor_name,
        ra.portal_student_id
    FROM dtlms_portal_application_preferences pp
    LEFT JOIN dtlms_recruitment_applications ra ON ra.id = pp.application_id AND ra.is_deleted = FALSE
    LEFT JOIN dtlms_portal_students ps ON ps.id = ra.portal_student_id
        WHERE (ps.submitted_at IS NOT NULL OR COALESCE(ra.application_status, '') = 'returned')
),
counts AS (
    SELECT preference_order, advisor_name, COUNT(*)::int AS student_count
    FROM prefs
    WHERE advisor_name IS NOT NULL AND advisor_name <> ''
    GROUP BY preference_order, advisor_name
),
totals AS (
    SELECT preference_order, SUM(student_count)::int AS total
    FROM counts
    GROUP BY preference_order
)
SELECT c.preference_order, c.advisor_name, c.student_count, COALESCE(t.total, 0) AS total
FROM counts c
LEFT JOIN totals t ON t.preference_order = c.preference_order
ORDER BY c.preference_order ASC, c.student_count DESC, c.advisor_name ASC
"""

try:
    from psycopg.rows import dict_row
    with psycopg.connect(conninfo) as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = [dict(r) for r in cur.fetchall()]
            print(rows)
except Exception as e:
    print('ERROR:', e)
