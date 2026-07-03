"""通用 helper: 从 backend/.env 读取数据库连接信息 (避免硬编码)

使用方法 (PowerShell):
    $ts = Get-Date -Format "yyyyMMddHHmmss"
    D:\pyproj\pydtlms\.venv\Scripts\python.exe D:\pyproj\pydtlms\backend\sql\_env_db.py

历史教训:
    2026-07-03 误把 test061502 (旧测试库) 当成 test062601 (实际库) 进行 ALTER
    导致错库被加列。后续所有 DB 读取必须从 .env 读取, 禁止硬编码。
"""
import sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ENV_PATH = Path(r"D:\pyproj\pydtlms\backend\.env")

if not ENV_PATH.exists():
    raise SystemExit(f"ERROR: .env not found at {ENV_PATH}")

env = {}
for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

print("=== Database config from backend/.env ===")
for key in [
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_SCHEMA",
    "POSTGRES_BACKUP_DB",
]:
    val = env.get(key, "(not set)")
    # password 脱敏
    if key == "POSTGRES_PASSWORD" and val != "(not set)":
        val = "***" + val[-3:] if len(val) > 3 else "***"
    print(f"  {key:25s} = {val}")
print()

# 输出一个 Python 代码片段，方便直接复制使用
print("=== Connection snippet (copy-paste) ===")
print("import psycopg")
print(f'conn = psycopg.connect(')
print(f'    host={env.get("POSTGRES_HOST")!r},')
print(f'    port={int(env.get("POSTGRES_PORT", 15431))},')
print(f'    user={env.get("POSTGRES_USER")!r},')
print(f'    password={env.get("POSTGRES_PASSWORD")!r},')
print(f'    dbname={env.get("POSTGRES_DB")!r},')
print(f')')