from cleantext_studio.cleaners.residuals import detect_block_residuals
from cleantext_studio.models import TextBlock, TextBlockType


def test_protected_code_is_not_reported_but_plain_markdown_is() -> None:
    blocks = [
        TextBlock(TextBlockType.CODE, "# code", "# code", 0, protected=True),
        TextBlock(TextBlockType.PARAGRAPH, "**残留**", "**残留**", 1, block_id="b1"),
    ]
    warnings = detect_block_residuals(blocks, "# code\n**残留**")
    assert len(warnings) == 1
    assert warnings[0].block_id == "b1" and warnings[0].warning_type == "markdown_emphasis"
