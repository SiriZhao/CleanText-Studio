from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters.files import DocxRenderer


def test_docx_uses_native_math_and_does_not_duplicate_ordered_markers() -> None:
    result = clean_text(
        "1. Prime theorem: \\pi(x) \\sim \\frac{x}{\\ln x}\n"
        "2. Linear regression: y=\\mathbf{w}^{\\top}\\mathbf{x}+b"
    )
    document = DocxRenderer().render(result.blocks)
    target = BytesIO()
    document.save(target)
    with ZipFile(target) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "m:oMath" in xml
    assert "\\pi" not in xml
    assert "\\mathbf" not in xml
    assert "1. Prime theorem" not in xml
    assert "2. Linear regression" not in xml
