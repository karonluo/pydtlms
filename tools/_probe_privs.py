import sys
sys.path.insert(0, r'D:\pyproj\pyams\backend\venv\Lib\site-packages')
import psycopg2
conn = psycopg2.connect(host='47.117.107.23',port=15431,user='postgres',password='Pass@@word123!',dbname='test061502',connect_timeout=10)
cur = conn.cursor()
cur.execute("SELECT rolname, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname=current_user")
print(cur.fetchone())
cur.execute("SELECT has_schema_privilege(current_user, 'public', 'CREATE')")
print('public CREATE:', cur.fetchone()[0])
cur.execute("SELECT has_schema_privilege(current_user, 'public', 'USAGE')")
print('public USAGE:', cur.fetchone()[0])
