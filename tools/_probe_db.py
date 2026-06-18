import sys
sys.path.insert(0, r'D:\pyproj\pyams\backend\venv\Lib\site-packages')
import psycopg2
conn = psycopg2.connect(host='47.117.107.23',port=15431,user='postgres',password='Pass@@word123!',dbname='test061502',connect_timeout=10)
cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database WHERE datname IN ('test35','postgres')")
print(cur.fetchall())
