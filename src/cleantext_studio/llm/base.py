from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from threading import Event

from .models import OptimizationMode, ProviderConfig
from .schemas import OptimizationResponse


@dataclass(slots=True, frozen=True)
class RequestEstimate:
    characters: int
    chinese_characters: int
    english_words: int
    estimated_chunks: int
    maximum_requests: int


class LLMProvider(ABC):
    def __init__(self, config: ProviderConfig, api_key: str) -> None:
        self.config = config
        self._api_key = api_key
        self._cancelled = Event()

    @abstractmethod
    def test_connection(self) -> None: ...
    @abstractmethod
    def list_models(self) -> list[str]: ...
    @abstractmethod
    def optimize_document(
        self, text: str, mode: OptimizationMode, custom_task: str = ""
    ) -> OptimizationResponse: ...

    def stream_optimization(self, text: str, mode: OptimizationMode) -> Iterator[str]:
        yield self.optimize_document(text, mode).model_dump_json()

    def estimate_request_size(self, text: str, target_size: int = 12_000) -> RequestEstimate:
        import re

        chunks = max(1, (len(text) + target_size - 1) // target_size)
        return RequestEstimate(
            len(text),
            len(re.findall(r"[\u4e00-\u9fff]", text)),
            len(re.findall(r"[A-Za-z]+", text)),
            chunks,
            chunks + 1,
        )

    def cancel(self) -> None:
        self._cancelled.set()
