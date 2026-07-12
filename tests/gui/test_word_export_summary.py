from cleantext_studio.app import MainWindow
from cleantext_studio.cleaners import clean_text


def test_word_export_structure_summary_counts() -> None:
    blocks = clean_text("## 标题\n\n> 引用\n\n- 列表\n\n|A|B|\n|-|-|\n|1|2|").blocks
    counts = MainWindow._word_structure_counts(blocks)
    assert counts == {"标题": 1, "列表": 1, "表格": 1, "引用": 1, "代码块": 0}
