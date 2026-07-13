from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import TextBlockType


def test_math_is_protected_from_markdown() -> None:
    source = (
        "**公式：** $x * y$\n\n$$\na^2 + b^2 = c^2\n$$\n\n价格为 $199。\n路径 C:\\Users\\Test。"
    )
    result = clean_text(source)
    assert "$x * y$" in result.text
    assert "a^2 + b^2 = c^2" in result.text
    assert "$199" in result.text
    assert r"C:\Users\Test" in result.text
    assert any(block.type == TextBlockType.DISPLAY_MATH for block in result.blocks)
    assert result.stats.formulas_detected == 2


def test_math_cleaning_is_idempotent() -> None:
    source = "公式 $ x ^ 2+y _ 1 $\n\n\\[\n\\frac {a}{b}\n\\]"
    once = clean_text(source).text
    assert clean_text(once).text == once
