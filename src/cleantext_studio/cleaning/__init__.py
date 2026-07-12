"""UI-independent structured cleaning API.

The compatibility ``cleaners`` package remains public, while this namespace
exposes the unified document model used by preview and exporters.
"""

from cleantext_studio.cleaners import clean_text
from cleantext_studio.models import (
    CleaningChange,
    CleanOptions,
    CleanResult,
    ResidualWarning,
    TableData,
    TextBlock,
    TextBlockType,
)

DocumentBlock = TextBlock
BlockType = TextBlockType
TableBlockData = TableData

__all__ = [
    "BlockType",
    "CleaningChange",
    "CleanOptions",
    "CleanResult",
    "DocumentBlock",
    "ResidualWarning",
    "TableBlockData",
    "clean_text",
]
