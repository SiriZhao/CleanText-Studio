from dataclasses import dataclass

from cleantext_studio.models import ParagraphBreakMode, TextBlock, TextBlockType

STRUCTURAL = {
    TextBlockType.TITLE,
    TextBlockType.HEADING_1,
    TextBlockType.HEADING_2,
    TextBlockType.HEADING_3,
    TextBlockType.LIST_ITEM,
    TextBlockType.ORDERED_LIST_ITEM,
    TextBlockType.QUOTE,
    TextBlockType.CODE,
    TextBlockType.TABLE,
    TextBlockType.DISPLAY_MATH,
    TextBlockType.MATH_PARAGRAPH,
    TextBlockType.EQUATION_GROUP,
}


@dataclass(slots=True, frozen=True)
class LayoutResult:
    text: str
    removed_breaks: int


class ParagraphLayoutEngine:
    def render(self, blocks: list[TextBlock], mode: ParagraphBreakMode) -> LayoutResult:
        output: list[str] = []
        removed = 0
        nonblank = [block for block in blocks if block.type != TextBlockType.BLANK or block.text]
        for index, block in enumerate(nonblank):
            if not output:
                output.append(block.text)
                continue
            previous = nonblank[index - 1]
            if (
                mode == ParagraphBreakMode.COMPACT
                and previous.type == block.type == TextBlockType.PARAGRAPH
            ) or (
                mode == ParagraphBreakMode.SMART_SECTIONS
                and previous.type == block.type == TextBlockType.PARAGRAPH
                and not previous.text.endswith(("。", "！", "？", ".", "!", "?"))
            ):
                output[-1] = self._join(output[-1], block.text)
                removed += 1
            else:
                separator = (
                    "\n\n"
                    if mode != ParagraphBreakMode.COMPACT
                    and (previous.type in STRUCTURAL or block.type in STRUCTURAL)
                    else "\n"
                )
                output.append(separator + block.text)
        return LayoutResult("".join(output), removed)

    @staticmethod
    def _join(left: str, right: str) -> str:
        if (
            left[-1:].isascii()
            and right[:1].isascii()
            and left[-1:].isalnum()
            and right[:1].isalnum()
        ):
            return left + " " + right
        return left + right
