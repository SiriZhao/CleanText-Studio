from pathlib import Path

from docx import Document

from cleantext_studio.exporters import export_docx, export_txt
from cleantext_studio.importers import import_file


def test_txt_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "中文 file.txt"
    export_txt("你好\n世界", path)
    assert "你好" in import_file(path)


def test_docx_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "out.docx"
    export_docx("一、标题\n正文内容。", path)
    assert path.exists()
    assert "正文内容" in "\n".join(p.text for p in Document(path).paragraphs)
