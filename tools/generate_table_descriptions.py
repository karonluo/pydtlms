import re
from pathlib import Path

SRC = Path('documents/test25_schema_full.md')
OUT = Path('documents/test25_schema_descriptions_block.md')

def infer_field_meaning(col):
    name = col.lower()
    if name == 'id' or name.endswith('_id') and name.count('_')==1:
        return '主键或外键，引用相关实体的 `id`。'
    if name.endswith('_id'):
        return '外键，引用相关实体的 `id`。'
    if name in ('created_at', 'updated_at', 'applied_at', 'confirmed_at', 'submitted_at', 'sent_at', 'assessed_at', 'last_login_at'):
        return '时间戳，记录事件时间，通常为 `timestamp with time zone`。'
    if name in ('is_deleted','deleted'):
        return '逻辑删除标志，`true` 表示已删除（软删除）。'
    if name in ('business_key', 'businessid'):
        return '业务唯一标识，用于跨系统或幂等性校验。'
    if name in ('username','full_name','full_name_pinyin','advisor_username','reviewer_username','publisher_username'):
        return '用户名或显示名字符串，用于标识用户账户/姓名。'
    if 'email' in name:
        return '电子邮箱地址。'
    if 'phone' in name or 'mobile' in name:
        return '联系电话或移动电话。'
    if name in ('is_active','status','state','result','review_status','application_status','plan_status'):
        return '状态字段，通常为有限枚举值，请参照业务文档或字典表。'
    if name.endswith('_json') or name.endswith('payload_json') or name.endswith('_jsonb') or 'json' in name:
        return 'JSON/JSONB 字段，存放结构化或半结构化数据。'
    if 'url' in name or 'attachment' in name or 'file' in name:
        return '资源或附件的 URL/路径。'
    if 'score' in name or name.endswith('_score'):
        return '数值评分字段，通常为 `numeric` 或 `integer`。'
    if 'count' in name or name.endswith('_count'):
        return '计数字段，整型。'
    if name in ('remark','comment','description','summary','note','policy','review_comment'):
        return '文本说明/备注字段。'
    return '字段名按字面含义，业务语义需由领域方确认。'

def parse_blocks(text):
    parts = re.split(r'^##\s+', text, flags=re.M)
    # first part is header
    header = parts[0]
    tables = []
    for p in parts[1:]:
        lines = p.splitlines()
        title = lines[0].strip()
        body = '\n'.join(lines[1:])
        tables.append((title, body))
    return header, tables

def extract_columns(body):
    cols = []
    in_table = False
    for line in body.splitlines():
        if line.strip().startswith('|') and '---' not in line:
            # column row
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 1:
                col = cells[0]
                cols.append(col)
    return cols

def extract_fks(body):
    fks = []
    m = re.search(r'\*\*Foreign keys:\*\n([\s\S]*)', body)
    if m:
        fk_block = m.group(1)
        for line in fk_block.splitlines():
            line=line.strip()
            if line.startswith('-'):
                fks.append(line[1:].strip())
    return fks

def generate_description(title, cols, fks):
    s = []
    s.append(f'### {title}')
    s.append('')
    s.append(f'- 表用途说明：基于表名 `{title}` 推断，保存与该实体相关的业务记录；具体业务语义请由领域方确认。')
    s.append('')
    s.append('- 字段说明：')
    s.append('')
    for c in cols:
        meaning = infer_field_meaning(c)
        s.append(f'  - `{c}`：{meaning}')
    s.append('')
    if fks:
        s.append('- 关系说明：')
        s.append('')
        for fk in fks:
            s.append(f'  - {fk}。')
        s.append('')
    s.append('\n')
    return '\n'.join(s)

def main():
    txt = SRC.read_text(encoding='utf-8')
    header, tables = parse_blocks(txt)
    out_lines = []
    out_lines.append('<!-- BEGIN auto-generated table descriptions -->')
    out_lines.append('')
    out_lines.append('## 每张表的字段与关系说明（自动生成草稿）')
    out_lines.append('')
    for title, body in tables:
        cols = extract_columns(body)
        fks = extract_fks(body)
        desc = generate_description(title, cols, fks)
        out_lines.append(desc)
    out_lines.append('<!-- END auto-generated table descriptions -->')
    OUT.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'wrote {OUT}')

if __name__ == '__main__':
    main()
