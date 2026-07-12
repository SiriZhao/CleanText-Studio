import re

from cleantext_studio.models import TableData, TextBlock, TextBlockType

SEPARATOR_CELL = re.compile(r"^:?-+:?$")


def split_row(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip().replace(r"\|", "|") for cell in value.split("|")]


def parse_table(lines: list[str]) -> TableData | None:
    """Parse a Markdown table only when the second row is a valid separator."""
    if len(lines) < 2:
        return None
    header = split_row(lines[0])
    separator = split_row(lines[1])
    if (
        len(header) < 2
        or len(separator) != len(header)
        or not all(SEPARATOR_CELL.fullmatch(cell.replace(" ", "")) for cell in separator)
    ):
        return None
    alignments = [
        (
            "center"
            if cell.startswith(":") and cell.endswith(":")
            else "right"
            if cell.endswith(":")
            else "left"
        )
        for cell in separator
    ]
    rows: list[list[str]] = []
    for line in lines[2:]:
        cells = split_row(line)
        cells = (cells + [""] * len(header))[: len(header)]
        rows.append(cells)
    return TableData(header, rows, alignments, "\n".join(lines))


def consolidate_table_blocks(blocks: list[TextBlock]) -> list[TextBlock]:
    output: list[TextBlock] = []
    index = 0
    while index < len(blocks):
        if blocks[index].type != TextBlockType.TABLE:
            output.append(blocks[index])
            index += 1
            continue
        end = index
        while end < len(blocks) and blocks[end].type == TextBlockType.TABLE:
            end += 1
        group = blocks[index:end]
        data = parse_table([block.text for block in group])
        if data:
            first = group[0]
            first.text = data.source
            first.table = data
            first.modified = any(b.modified for b in group)
            output.append(first)
        else:
            output.extend(group)
        index = end
    return output
