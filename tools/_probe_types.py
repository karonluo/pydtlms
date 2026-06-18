import sys
sys.path.insert(0, r'D:\pyproj\pyams\backend\venv\Lib\site-packages')
import psycopg2
conn = psycopg2.connect(host='47.117.107.23',port=15431,user='postgres',password='Pass@@word123!',dbname='test061502',connect_timeout=10)
cur = conn.cursor()
cur.execute("""
    SELECT t.typtype, count(*)
    FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
    WHERE n.nspname='public' AND t.typtype IN ('c','e','r','d','m')
    GROUP BY t.typtype ORDER BY 1
""")
print('all-incl-rowtype:', cur.fetchall())
cur.execute("""
    SELECT t.typtype, count(*)
    FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
    WHERE n.nspname='public' AND t.typtype IN ('c','e','r','d','m')
      AND t.typisdefined
      AND (t.typrelid=0 OR (SELECT relkind FROM pg_class WHERE oid=t.typrelid) IN ('c','f'))
    GROUP BY t.typtype ORDER BY 1
""")
print('only-true-types:', cur.fetchall())
cur.execute("""
    SELECT t.typname, t.typtype, c.relkind
    FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
    LEFT JOIN pg_class c ON c.oid=t.typrelid
    WHERE n.nspname='public' AND t.typtype IN ('c','e','r','d','m') AND t.typtype='c' AND t.typisdefined
""")
for r in cur.fetchall():
    print('composite row:', r)
