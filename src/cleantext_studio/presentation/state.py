"""Mutable UI state with stable business values and no translated labels."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .messages import UserMessage


class CleaningState(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class ResultState(StrEnum):
    EMPTY = "empty"
    CURRENT = "current"
    OUTDATED = "outdated"
    EDITED = "edited"


@dataclass(slots=True)
class AppPresentationState:
    current_locale: str = "en_US"
    current_theme: str = "system"
    source_document_name: str = ""
    source_character_count: int = 0
    source_paragraph_count: int = 0
    cleaning_state: CleaningState = CleaningState.IDLE
    result_state: ResultState = ResultState.EMPTY
    selected_preset: str = "standard"
    selected_link_mode: str = "text_only"
    selected_url_mode: str = "preserve"
    selected_paragraph_mode: str = "smart_sections"
    selected_list_mode: str = "keep"
    selected_math_mode: str = "preserve"
    enabled_rules: set[str] = field(default_factory=set)
    notifications: list[UserMessage] = field(default_factory=list)
