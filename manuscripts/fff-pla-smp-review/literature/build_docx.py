#!/usr/bin/env python3
"""Assemble the review chapters into an APA-styled Word document."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
CORPUS = ROOT / "literature" / "corpus_final.json"
OUT = ROOT / "Process-Structure-Property-Relationships-FFF-SMP-PLA.docx"


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.casefold()


def sort_citation_group(group: str) -> str:
    parts = [p.strip() for p in group.split(";")]
    if len(parts) < 2:
        return group

    def key(part: str) -> str:
        author = part.split(",")[0]
        return fold(author)

    return "; ".join(sorted(parts, key=key))


def normalize_citations(text: str) -> str:
    def repl(match: re.Match) -> str:
        inner = match.group(1)
        if not re.search(r"\d{4}", inner):
            return match.group(0)
        if ";" not in inner:
            return match.group(0)
        return "(" + sort_citation_group(inner) + ")"

    return re.sub(r"\(([^)]+)\)", repl, text)


def cited_records(text: str, rows: list[dict]) -> list[dict]:
    chosen = []
    for row in rows:
        family = (row["authors"][0]["family"] if row.get("authors") else "")
        year = str(row["year_label"])
        if not family:
            continue
        for match in re.finditer(re.escape(family), text):
            window = text[match.start() : match.start() + 90]
            if year in window:
                chosen.append(row)
                break
    chosen.sort(key=lambda row: fold(row["apa"]))
    return chosen


def set_run_font(run, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def format_paragraph(paragraph, *, align="left", indent=True, space_after=0, hanging=False):
    pf = paragraph.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 2.0
    if align == "center":
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Inches(0)
        pf.left_indent = Inches(0)
    elif hanging:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)
    elif indent:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Inches(0.5)
        pf.left_indent = Inches(0)
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Inches(0)
        pf.left_indent = Inches(0)


def add_rich(paragraph, text: str, *, size=12, bold=False, italic=False):
    parts = re.split(r"(\*[^*]+\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("*") and part.endswith("*") and len(part) > 2:
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, size=size, bold=bold, italic=True)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, size=size, bold=bold, italic=italic)


def add_heading_paragraph(document, text: str, level: int):
    paragraph = document.add_paragraph()
    if level == 1:
        format_paragraph(paragraph, align="center", indent=False, space_after=0)
        add_rich(paragraph, text, bold=True)
    elif level == 2:
        format_paragraph(paragraph, align="left", indent=False)
        add_rich(paragraph, text, bold=True)
    else:
        format_paragraph(paragraph, align="left", indent=False)
        add_rich(paragraph, text, bold=True, italic=True)
    return paragraph


def configure(document: Document) -> None:
    for section in document.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        from docx.oxml import OxmlElement

        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = " PAGE "
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        run = footer.add_run()
        set_run_font(run, size=12)
        run._r.append(begin)
        run._r.append(instr)
        run._r.append(end)
    style = document.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")


def main() -> None:
    rows = json.loads(CORPUS.read_text())
    chunks = []
    for path in sorted(CHAPTERS.glob("*.md")):
        if path.name.startswith("08"):
            continue
        chunks.append(normalize_citations(path.read_text()))
    body = "\n".join(chunks)
    records = cited_records(body, rows)

    document = Document()
    configure(document)

    title = document.add_paragraph()
    format_paragraph(title, align="center", indent=False)
    add_rich(
        title,
        "Process–Structure–Property Relationships in Fused Filament Fabricated Shape Memory Polymers: A Focus on Fiber-Reinforced PLA Composites",
        bold=True,
    )
    author = document.add_paragraph()
    format_paragraph(author, align="center", indent=False)
    add_rich(author, "Selva Kumaran")
    meta = document.add_paragraph()
    format_paragraph(meta, align="center", indent=False)
    add_rich(meta, "Review article")
    blank = document.add_paragraph()
    format_paragraph(blank, align="left", indent=False)

    for block in chunks:
        lines = block.splitlines()
        paragraph_buf: list[str] = []
        in_abstract = False

        def flush():
            text = " ".join(s.strip() for s in paragraph_buf).strip()
            paragraph_buf.clear()
            if not text:
                return
            paragraph = document.add_paragraph()
            format_paragraph(paragraph, align="left", indent=not in_abstract)
            add_rich(paragraph, text)

        for line in lines:
            if line.startswith("#"):
                flush()
                level = len(line) - len(line.lstrip("#"))
                heading = line[level:].strip()
                in_abstract = heading.lower() == "abstract"
                add_heading_paragraph(document, heading, level)
            elif not line.strip():
                flush()
            else:
                paragraph_buf.append(line)
        flush()

    add_heading_paragraph(document, "References", 1)
    for row in records:
        paragraph = document.add_paragraph()
        format_paragraph(paragraph, hanging=True)
        add_rich(paragraph, row["apa"])

    document.save(OUT)
    print(f"cited {len(records)} -> {OUT}")
    missing_years = []
    for row in records:
        if str(row["year_label"]) not in row["apa"]:
            missing_years.append(row["sid"])
    print("year label missing from apa", missing_years)


if __name__ == "__main__":
    main()
