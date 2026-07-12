from __future__ import annotations

from dataclasses import dataclass

from cleantext_studio.models import TextBlock, TextBlockType

STRUCTURAL = {
    TextBlockType.TITLE, TextBlockType.HEADING_1, TextBlockType.HEADING_2,
    TextBlockType.HEADING_3, TextBlockType.TABLE, TextBlockType.QUOTE,
}


@dataclass(slots=True, frozen=True)
class ParagraphFormatResult:
    text: str
    removed_blank_lines: int


class ParagraphFormatter:
    """Render blocks with stable, bounded paragraph spacing."""

    def format(self, blocks: list[TextBlock]) -> ParagraphFormatResult:
        active = [block for block in blocks if block.text]
        output: list[str] = []
        for index, block in enumerate(active):
            if index:
                previous = active[index - 1]
                same_compact_structure = previous.type == block.type and block.type in {
                    TextBlockType.LIST_ITEM,
                    TextBlockType.ORDERED_LIST_ITEM,
                    TextBlockType.CODE,
                    TextBlockType.TABLE,
                }
                separator = "\n" if same_compact_structure else "\n\n"
                output.append(separator)
            output.append(block.text)
        text = "".join(output)
        original_blank_lines = sum(1 for block in blocks if block.type == TextBlockType.BLANK)
        retained_boundaries = max(0, len(active) - 1)
        return ParagraphFormatResult(text, max(0, original_blank_lines - retained_boundaries))
