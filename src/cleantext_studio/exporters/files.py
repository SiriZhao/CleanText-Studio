from __future__ import annotations

import os
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from cleantext_studio.models import DocumentTemplate


def export_txt(text: str, path: Path, encoding: str = "utf-8", newline: str = "\r\n") -> None:
    data = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)
    path.write_text(data, encoding=encoding, newline="")


def _font(run: object, name: str, size: float) -> None:
    run.font.name = name  # type: ignore[attr-defined]
    run.font.size = Pt(size)  # type: ignore[attr-defined]
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)  # type: ignore[attr-defined]


def export_docx(text: str, path: Path, template: DocumentTemplate | None = None) -> None:
    template = template or DocumentTemplate(
        title_size=22, body_size=12, line_spacing=1.5, first_line_chars=2, margin_cm=2.54
    )
    doc = Document()
    section = doc.sections[0]
    section.top_margin = section.bottom_margin = section.left_margin = section.right_margin = Cm(
        template.margin_cm
    )
    for line in text.splitlines():
        if not line:
            continue
        is_heading = len(line) < 40 and (
            line.endswith(("：", ":"))
            or line.startswith(("一、", "二、", "三、", "第一章", "第二章"))
        )
        paragraph = doc.add_paragraph(style="Heading 1" if is_heading else None)
        run = paragraph.add_run(line)
        _font(
            run,
            template.title_font if is_heading else template.body_font,
            template.title_size if is_heading else template.body_size,
        )
        paragraph.paragraph_format.line_spacing = template.line_spacing
        if is_heading:
            paragraph.paragraph_format.keep_with_next = True
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            paragraph.paragraph_format.first_line_indent = Pt(
                template.body_size * template.first_line_chars
            )
    if template.header:
        run = section.header.paragraphs[0].add_run(template.header)
        _font(run, template.body_font, 9)
    if template.page_numbers:
        paragraph = section.footer.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        paragraph._p.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(suffix=".docx", dir=path.parent)
    os.close(fd)
    temp = Path(temp_name)
    try:
        doc.save(str(temp))
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
