# -*- coding: utf-8 -*-
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn

SRC = r"D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\docs\explanation\agent-architecture.md"
OUT = r"D:\AI工具\02-本质层\04-知识库\08-人工智能与智能体\主流Agent架构\exports\docx\agent-architecture.docx"
CJK = "Microsoft YaHei"
MONO = "Consolas"
GRAY = (0x60, 0x60, 0x60)

doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.2)

normal = doc.styles["Normal"]
normal.font.name = CJK
normal.font.size = Pt(10.5)
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), CJK)
normal.paragraph_format.space_after = Pt(4)

def style_run(r, size=None, bold=None, color=None, mono=False):
    r.font.name = MONO if mono else CJK
    rpr = r._element.get_or_add_rPr()
    rpr.get_or_add_rFonts().set(qn("w:eastAsia"), CJK)
    if size: r.font.size = Pt(size)
    if bold is not None: r.bold = bold
    if color: r.font.color.rgb = RGBColor(*color)

TOKEN = re.compile(r"(\*\*.+?\*\*|\x60[^\x60]+\x60|\[[^\]]+\]\([^)]+\))")

def add_inline(p, text, base=10.5, urls=True, cell=False):
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            r = p.add_run(part[2:-2]); style_run(r, base, bold=True)
        elif part.startswith("\x60") and part.endswith("\x60") and len(part) > 2:
            r = p.add_run(part[1:-1]); style_run(r, base - 1.5, mono=True)
        elif part.startswith("[") and part.endswith(")"):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part)
            if m:
                r = p.add_run(m.group(1)); style_run(r, base)
                if urls and not cell:
                    r2 = p.add_run("（" + m.group(2) + "）"); style_run(r2, 8, color=GRAY)
                continue
            r = p.add_run(part); style_run(r, base)
        else:
            r = p.add_run(part); style_run(r, base)

def clean_cell(s):
    return s.replace("\x60", "").strip()

lines = open(SRC, encoding="utf-8").read().splitlines()
i, n = 0, len(lines)
while i < n:
    s = lines[i].strip()
    if not s or s == "---":
        i += 1; continue
    if s.startswith("|"):
        rows = []
        while i < n and lines[i].strip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        if len(rows) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in rows[1]):
            header, body = rows[0], rows[2:]
        else:
            header, body = rows[0], rows[1:]
        table = doc.add_table(rows=1, cols=len(header))
        table.style = "Table Grid"
        for j, h in enumerate(header):
            p = table.rows[0].cells[j].paragraphs[0]
            add_inline(p, clean_cell(h), base=9, urls=False, cell=True)
            for r in p.runs:
                r.bold = True; r.font.size = Pt(9)
        for row in body:
            cells = table.add_row().cells
            for j in range(len(header)):
                txt = row[j] if j < len(row) else ""
                p = cells[j].paragraphs[0]
                add_inline(p, clean_cell(txt), base=9, urls=False, cell=True)
                for r in p.runs:
                    r.font.size = Pt(9)
        continue
    m = re.match(r"^(#{1,4})\s+(.*)$", s)
    if m:
        level = len(m.group(1))
        h = doc.add_heading("", level=level)
        add_inline(h, m.group(2), base={1: 16, 2: 14, 3: 12, 4: 11}.get(level, 11))
        for r in h.runs:
            if r.font.color and r.font.color.rgb == RGBColor(*GRAY):
                continue
            r.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
            r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), CJK)
        i += 1; continue
    if s.startswith(">"):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        add_inline(p, s.lstrip(">").strip(), base=9.5)
        for r in p.runs:
            if r.font.color and r.font.color.rgb == RGBColor(*GRAY):
                continue
            r.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
            if not r.bold:
                r.italic = True
        i += 1; continue
    m = re.match(r"^-\s+(.*)$", s)
    if m:
        p = doc.add_paragraph(style="List Bullet")
        add_inline(p, m.group(1))
        i += 1; continue
    m = re.match(r"^\d+\.\s+(.*)$", s)
    if m:
        p = doc.add_paragraph(style="List Number")
        add_inline(p, m.group(1))
        i += 1; continue
    p = doc.add_paragraph()
    add_inline(p, s)
    i += 1

doc.core_properties.title = "主流 Agent 架构整理（官方来源版）"
doc.save(OUT)
print("saved:", OUT)
print("paragraphs:", len(doc.paragraphs), "tables:", len(doc.tables))
