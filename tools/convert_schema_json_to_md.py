import json
import re
from pathlib import Path

src = Path('documents/test25_schema.json')
if not src.exists():
    print('source not found:', src)
    raise SystemExit(1)
text = src.read_text(encoding='utf-8')
# Extract first JSON object in file by finding first '{' and matching last '}'
first = text.find('{')
last = text.rfind('}')
if first == -1 or last == -1:
    print('no JSON object found')
    raise SystemExit(2)
json_text = text[first:last+1]
# Try to fix trailing commas and single quotes (best-effort)
# Replace "None"-like nulls already present. Ensure valid JSON.
# Remove any leading non-json lines already trimmed.
try:
    data = json.loads(json_text)
except Exception as e:
    # attempt to fix common issues: convert single quotes to double where safe
    fixed = json_text.replace("'::character varying", '"')
    fixed = fixed.replace("'ACTIVE'::character varying", '"ACTIVE"')
    fixed = fixed.replace("\'", "\\'")
    try:
        data = json.loads(fixed)
    except Exception as e2:
        print('failed to parse json:', e, e2)
        raise

out_lines = []
out_lines.append('# test25 schema (auto-generated)')
for table, meta in data.items():
    out_lines.append(f'## {table}')
    cols = meta.get('columns', [])
    out_lines.append('| Column | Type | Nullable | Default |')
    out_lines.append('|---|---|---|---|')
    for c in cols:
        name = c.get('name','')
        typ = c.get('data_type','')
        nul = c.get('is_nullable','')
        default = c.get('default')
        default = '' if default is None else str(default)
        # escape pipes
        name = name.replace('|','\|')
        typ = typ.replace('|','\|')
        default = default.replace('|','\|')
        out_lines.append(f'| {name} | {typ} | {nul} | {default} |')
    pk = meta.get('primary_key', [])
    if pk:
        out_lines.append('**Primary key:** ' + ', '.join(pk))
    fks = meta.get('foreign_keys', [])
    if fks:
        out_lines.append('**Foreign keys:**')
        for fk in fks:
            cname = fk.get('column')
            ref_table = fk.get('ref_table')
            ref_col = fk.get('ref_column')
            out_lines.append(f'- {cname} -> {ref_table}.{ref_col}')
    out_lines.append('')

out_path = Path('documents/test25_schema.md')
out_path.write_text('\n'.join(out_lines), encoding='utf-8')
print('wrote', out_path)
