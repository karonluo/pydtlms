import json
from pathlib import Path
import re

src = Path('documents/test25_schema.json')
text = src.read_text(encoding='utf-8')

# find occurrences of "tablename": {
pattern = re.compile(r'"([A-Za-z0-9_]+)"\s*:\s*\{')
matches = list(pattern.finditer(text))
if not matches:
    print('no table matches')
    raise SystemExit(1)

data = {}
for m in matches:
    name = m.group(1)
    start = m.end() - 1  # position of '{'
    # find matching brace
    i = start
    depth = 0
    in_string = False
    esc = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        i += 1
    else:
        print('no matching brace for', name)
        continue
    snippet = text[start:end+1]
    # try to load snippet as json
    try:
        obj = json.loads(snippet)
    except Exception as e:
        # attempt small fixes
        s = snippet
        s = s.replace("'::character varying", '"')
        try:
            obj = json.loads(s)
        except Exception as e2:
            print('failed parse for', name, e, e2)
            continue
    data[name] = obj

# generate markdown
lines = ['# test25 schema (auto-generated)']
for table, meta in sorted(data.items()):
    lines.append(f'## {table}')
    cols = meta.get('columns', [])
    lines.append('| Column | Type | Nullable | Default |')
    lines.append('|---|---|---|---|')
    for c in cols:
        name = c.get('name','')
        typ = c.get('data_type','')
        nul = c.get('is_nullable','')
        default = c.get('default')
        default = '' if default is None else str(default)
        name = name.replace('|','\\|')
        typ = typ.replace('|','\\|')
        default = default.replace('|','\\|')
        lines.append(f'| {name} | {typ} | {nul} | {default} |')
    pk = meta.get('primary_key', [])
    if pk:
        lines.append('**Primary key:** ' + ', '.join(pk))
    fks = meta.get('foreign_keys', [])
    if fks:
        lines.append('**Foreign keys:**')
        for fk in fks:
            cname = fk.get('column')
            ref_table = fk.get('ref_table')
            ref_col = fk.get('ref_column')
            lines.append(f'- {cname} -> {ref_table}.{ref_col}')
    lines.append('')

out = Path('documents/test25_schema.md')
out.write_text('\n'.join(lines), encoding='utf-8')
print('wrote', out)
