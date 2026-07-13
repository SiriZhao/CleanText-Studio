from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import InlineRunType


def test_chinese_inline_formula_sequence_is_preserved() -> None:
    source = "这里，\\( O \\) 表示有序度，\\( I \\) 表示输入，\\( \\lambda \\) 是系数，而 \\( \\xi(t) \\) 是冲击。"
    paragraph = next(block for block in clean_text(source).blocks if block.text)
    assert [run.type for run in paragraph.runs] == [
        InlineRunType.TEXT,
        InlineRunType.INLINE_MATH,
        InlineRunType.TEXT,
        InlineRunType.INLINE_MATH,
        InlineRunType.TEXT,
        InlineRunType.INLINE_MATH,
        InlineRunType.TEXT,
        InlineRunType.INLINE_MATH,
        InlineRunType.TEXT,
    ]
    assert [run.math.expression_source for run in paragraph.runs if run.math] == [
        "O",
        "I",
        r"\lambda",
        r"\xi(t)",
    ]
