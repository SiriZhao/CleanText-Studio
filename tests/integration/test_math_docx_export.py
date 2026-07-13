from zipfile import ZipFile

from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters import export_docx_blocks


def test_docx_contains_native_office_math(tmp_path) -> None:
    result = clean_text("行内 $x^2$。\n\n$$\n\\frac{a}{b}\n$$")
    path = tmp_path / "math.docx"
    export_docx_blocks(result.blocks, path)
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "<m:oMath" in xml
    assert "<m:f>" in xml
