# -*- coding: utf-8 -*-
import html, re
from pathlib import Path

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
body{font-family:'Segoe UI','Microsoft YaHei',sans-serif;max-width:1000px;margin:20px auto;padding:0 20px;color:#1c1c1c;line-height:1.65}
h1{font-size:1.65em;border-bottom:3px solid #2b6cb0;padding-bottom:8px;margin-bottom:6px}
.bar{position:sticky;top:0;background:#fff;z-index:5;padding:8px 0;border-bottom:1px solid #dfe6ee;margin-bottom:10px}
.bar button{background:#2b6cb0;color:#fff;border:none;border-radius:6px;padding:6px 14px;margin-right:8px;cursor:pointer;font-size:.92em}
.bar button:hover{background:#1a4971}
details.chap{margin:10px 0;border:1px solid #d7dee8;border-radius:8px;overflow:hidden;background:#fff}
details.chap>summary{background:#eef4fb;font-weight:700;font-size:1.1em;padding:10px 14px;cursor:pointer;list-style:none}
details.chap>summary::before{content:'\u25b8 ';color:#2b6cb0}
details.chap[open]>summary::before{content:'\u25be ';color:#2b6cb0}
details.chap>summary:hover{background:#e2edf8}
details.sec{margin:6px 12px 6px 16px;border-left:3px solid #c5d5e8;padding-left:10px}
details.sec>summary{font-weight:600;color:#2b6cb0;padding:6px 4px;cursor:pointer;list-style:none}
details.sec>summary::before{content:'\u25b8 ';color:#7f9fc4}
details.sec[open]>summary::before{content:'\u25be ';color:#7f9fc4}
details.sec>summary:hover{color:#1a4971}
table{border-collapse:collapse;margin:8px 0;font-size:.92em;width:100%}
th,td{border:1px solid #c9d2dd;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f0f4f9}
blockquote{border-left:4px solid #9db8d6;margin:8px 0;padding:4px 12px;color:#3d4754;background:#f7fafd}
code{background:#f0f2f5;padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;font-size:.9em}
a{color:#2b6cb0}
ul,ol{margin:6px 0 6px 22px;padding:0}
p{margin:6px 0}
</style>
</head>
<body>
<h1>__TITLE__</h1>
<div class="bar"><button onclick="setAll(true)">全部展开</button><button onclick="setAll(false)">全部收起</button><span style="color:#667;font-size:.85em">　章节默认展开、小节默认收起，点击标题行即可折叠/展开</span></div>
"""

TAIL = """
<script>
function setAll(open){var ds=document.querySelectorAll('details');for(var i=0;i<ds.length;i++){ds[i].open=open;}}
</script>
</body>
</html>
"""

def esc(t):
    return html.escape(t, quote=False)

def inline(t):
    t = esc(t)
    t = re.sub(r'\x60([^\x60]+)\x60', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t

def table_html(head, body):
    rows = ['<tr>' + ''.join('<th>' + inline(c) + '</th>' for c in head) + '</tr>']
    for row in body:
        cells = [row[j] if j < len(row) else '' for j in range(len(head))]
        rows.append('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in cells) + '</tr>')
    return '<table>' + ''.join(rows) + '</table>'

def convert(md_path, out_path):
    lines = open(md_path, encoding='utf-8').read().splitlines()
    title = ''
    out = []
    chapter_open = False
    sec_open = False

    def close_sec():
        nonlocal sec_open
        if sec_open:
            out.append('</details>')
            sec_open = False

    def close_chapter():
        nonlocal chapter_open
        close_sec()
        if chapter_open:
            out.append('</details>')
            chapter_open = False

    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s or s == '---':
            i += 1
            continue
        if s.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            if len(rows) >= 2 and all(re.fullmatch(r':?-{2,}:?', c) for c in rows[1]):
                head, body = rows[0], rows[2:]
            else:
                head, body = rows[0], rows[1:]
            out.append(table_html(head, body))
            continue
        m = re.match(r'^#\s+(.*)$', s)
        if m:
            title = m.group(1)
            i += 1
            continue
        m = re.match(r'^(#{2,4})\s+(.*)$', s)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2))
            if level == 2:
                close_chapter()
                out.append('<details class="chap" open><summary>' + text + '</summary>')
                chapter_open = True
            else:
                close_sec()
                out.append('<details class="sec"><summary>' + text + '</summary>')
                sec_open = True
            i += 1
            continue
        if s.startswith('>'):
            out.append('<blockquote>' + inline(s.lstrip('>').strip()) + '</blockquote>')
            i += 1
            continue
        m = re.match(r'^-\s+(.*)$', s)
        if m:
            items = []
            while i < n:
                mm = re.match(r'^-\s+(.*)$', lines[i].strip())
                if not mm:
                    break
                items.append('<li>' + inline(mm.group(1)) + '</li>')
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>')
            continue
        m = re.match(r'^\d+\.\s+(.*)$', s)
        if m:
            items = []
            while i < n:
                mm = re.match(r'^\d+\.\s+(.*)$', lines[i].strip())
                if not mm:
                    break
                items.append('<li>' + inline(mm.group(1)) + '</li>')
                i += 1
            out.append('<ol>' + ''.join(items) + '</ol>')
            continue
        buf = [s]
        i += 1
        while i < n:
            s2 = lines[i].strip()
            if (not s2 or s2 == '---' or s2.startswith('|') or s2.startswith('>')
                    or s2.startswith('#') or re.match(r'^\d+\.\s', s2)
                    or re.match(r'^-\s', s2)):
                break
            buf.append(s2)
            i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')

    close_chapter()
    body = '\n'.join(out)
    # 相对 md 链接改为折叠版 html 链接
    body = body.replace('href="../how-to/task-fit-and-build.md"', 'href="task-fit-and-build.html"')
    page = HEAD.replace('__TITLE__', title) + body + TAIL
    open(out_path, 'w', encoding='utf-8').write(page)
    return page

jobs = [
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\explanation\agent-architecture.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\agent-architecture.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\how-to\task-fit-and-build.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\task-fit-and-build.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\explanation\agent-vendor-landscape.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\agent-vendor-landscape.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\reference\vendor-source-matrix.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\vendor-source-matrix.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\reference\claims-ledger.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\claims-ledger.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\reference\knowledge-timeline.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\knowledge-timeline.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\reference\conflict-log.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\conflict-log.html'),
    (r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\reference\knowledge-governance.md', r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\knowledge-governance.html'),
]
index_items = []
for src, dst in jobs:
    page = convert(src, dst)
    title_match = re.search(r'<h1>(.*?)</h1>', page)
    title = title_match.group(1) if title_match else Path(dst).stem
    index_items.append((Path(dst).name, title))
    print('OUT:', dst)
    print('  chars:', len(page), '| chapters:', page.count('<details class="chap"'), '| sections:', page.count('<details class="sec"'), '| tables:', page.count('<table>'), '| opens:', page.count('<details'), '| closes:', page.count('</details>'))
index_path = r'D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\html\index.html'
links = '\n'.join(f'<li><a href="{name}">{title}</a></li>' for name, title in index_items)
index_page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>主流 Agent 架构知识库</title>
<style>{HEAD.split('</style>', 1)[0].split('<style>', 1)[1]}</style></head>
<body><h1>主流 Agent 架构知识库</h1>
<p>大厂官方文档、研究、协议、评测、时间线与冲突账本。</p>
<ul>{links}</ul></body></html>
"""
open(index_path, 'w', encoding='utf-8').write(index_page)
print('OUT:', index_path, '| pages:', len(index_items))
print('DONE')
