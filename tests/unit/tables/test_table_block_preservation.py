from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import TextBlockType


def test_table_survives_deep_cleaning() -> None:
    result = clean_text("## 表格\n\n|模块|功能|\n|-|-|\n|识别|诊断|")
    tables = [block for block in result.blocks if block.type == TextBlockType.TABLE]
    assert len(tables) == 1 and tables[0].table is not None
    assert tables[0].table.rows == [["识别", "诊断"]]
