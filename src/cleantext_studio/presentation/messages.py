"""Locale-independent user-visible message descriptions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class MessageSeverity(StrEnum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class UserMessage:
    """A translated message is rendered by the UI, never by business code."""

    message_id: str
    severity: MessageSeverity = MessageSeverity.INFO
    parameters: Mapping[str, object] = field(default_factory=dict)
    context: str | None = None
    action_ids: tuple[str, ...] = ()
