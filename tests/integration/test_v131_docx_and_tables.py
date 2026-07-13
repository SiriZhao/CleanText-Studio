from zipfile import ZipFile

from cleantext_studio.cleaners import clean_text
from cleantext_studio.exporters import export_docx_blocks


def test_table_cells_are_clean_and_formula_is_native_omml(tmp_path) -> None:
    source = """| **特征维度** | **公式** |
| :--- | ---: |
| **能量** | $E=mc^2$ |
"""
    result = clean_text(source)
    table = next(block.table for block in result.blocks if block.table)
    assert table.headers == ["特征维度", "公式"]
    assert table.rows == [["能量", "$E=mc^2$"]]

    path = tmp_path / "table-math.docx"
    export_docx_blocks(result.blocks, path)
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "<w:tbl" in xml
    assert "<m:oMath" in xml
    assert "<m:sSup" in xml
    assert "**" not in xml
    assert "| ---" not in xml


def test_supported_formula_document_has_no_raw_latex(tmp_path) -> None:
    source = r"""# 公式验收
行内公式：\( E = mc^2 \)。

\[
S = k_B \ln \Omega
\]

\[
P(A\mid B)=\frac{P(AB)}{P(B)}
\]

\[
\sum_{i=1}^{n}x_i
\]

\[
\int_0^1x^2\,dx
\]
"""
    result = clean_text(source)
    path = tmp_path / "formula.docx"
    export_docx_blocks(result.blocks, path)
    with ZipFile(path) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    for residue in (r"\[", r"\]", r"\(", r"\)", r"\frac", r"\sum", r"\int", r"\Omega"):
        assert residue not in xml
    assert "<m:oMath" in xml
    assert "<m:oMathPara" in xml
    assert "<m:f>" in xml
    assert "<m:nary>" in xml
    assert "Ω" in xml
