import html
import re

import emoji
from bs4 import BeautifulSoup

from cleantext_studio.math.protector import MathProtector
from cleantext_studio.models import LinkMode, ListMode, TableData, TextBlock, TextBlockType

from .markdown_cleaner import MarkdownCleaner

SEPARATOR_CELL = re.compile(r"^:?-+:?$")


def split_row(line: str) -> list[str]:
    value = line.strip().replace("｜", "|")
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    placeholder = "CTSESCAPEDPIPETOKEN"
    value = value.replace(r"\|", placeholder)
    return [cell.strip().replace(placeholder, "|") for cell in value.split("|")]


class TableCellCleaningPipeline:
    """Clean inline presentation syntax without flattening math expressions."""

    def __init__(self) -> None:
        self.markdown = MarkdownCleaner()
        self.math = MathProtector()

    def clean(self, value: str) -> str:
        value = html.unescape(value)
        line_break = "CTSTABLEEXPLICITBREAKTOKEN"
        value = re.sub(r"<br\s*/?>", line_break, value, flags=re.IGNORECASE)
        if re.search(r"</?[A-Za-z][^>]*>", value):
            value = BeautifulSoup(value, "html.parser").get_text(" ")
        protected, formulas = self.math.protect_inline(value)
        cleaned = self.markdown.clean(
            protected,
            link_mode=LinkMode.TEXT_ONLY,
            list_mode=ListMode.KEEP,
        ).text
        cleaned = emoji.replace_emoji(cleaned, replace="")
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\s*\n\s*", " ", cleaned).strip()
        cleaned = cleaned.replace(line_break, "\n")
        return self.math.restore(cleaned, formulas)


class TablePostProcessor:
    """Remove presentation residue and columns made empty by configured cleanup."""

    _decorative_headers = {"", "emoji", "图标", "符号", "icon"}

    def process(self, data: TableData) -> int:
        removable: list[int] = []
        for column, header in enumerate(data.headers):
            values = [row[column].strip() for row in data.rows]
            if header.strip().casefold() in self._decorative_headers and not any(values):
                removable.append(column)
        for column in reversed(removable):
            del data.headers[column]
            del data.alignments[column]
            for row in data.rows:
                del row[column]
        return len(removable)


class TableWidthPlanner:
    """Allocate more page width to descriptive columns than category columns."""

    def proportions(self, data: TableData) -> list[float]:
        if not data.headers:
            return []
        scores: list[float] = []
        for column, header in enumerate(data.headers):
            values = [header, *(row[column] for row in data.rows)]
            average = sum(len(value.replace("\n", "")) for value in values) / len(values)
            numeric = sum(value.replace(".", "").isdigit() for value in values) / len(values)
            score = max(8.0, min(44.0, average))
            if numeric > 0.7:
                score *= 0.7
            scores.append(score)
        total = sum(scores)
        return [score / total for score in scores]


def parse_table(lines: list[str]) -> TableData | None:
    """Parse a Markdown table only when the second row is a valid separator."""
    if len(lines) < 2:
        return None
    cleaner = TableCellCleaningPipeline()
    header = [cleaner.clean(cell) for cell in split_row(lines[0])]
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
    malformed_rows: list[int] = []
    for row_number, line in enumerate(lines[2:], 3):
        cells = [cleaner.clean(cell) for cell in split_row(line)]
        if len(cells) != len(header):
            malformed_rows.append(row_number)
        cells = (cells + [""] * len(header))[: len(header)]
        rows.append(cells)
    data = TableData(header, rows, alignments, "\n".join(lines), malformed_rows)
    removed = TablePostProcessor().process(data)
    if removed:
        data.malformed_rows.append(-removed)
    return data


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
