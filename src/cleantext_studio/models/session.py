from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import CleanOptions
from .core import CleanStats, ResidualWarning, TextBlock


@dataclass(slots=True)
class DocumentSession:
    source_text: str = ""
    source_blocks: list[TextBlock] = field(default_factory=list)
    local_result_text: str = ""
    result_blocks: list[TextBlock] = field(default_factory=list)
    edited_result_text: str = ""
    cleaning_options: CleanOptions = field(default_factory=CleanOptions)
    cleaning_stats: CleanStats | None = None
    residual_warnings: list[ResidualWarning] = field(default_factory=list)
    source_modified: bool = False
    result_modified: bool = False
    result_outdated: bool = False
    current_file: Path | None = None
    encoding: str = "UTF-8"
    processing_state: str = "idle"
