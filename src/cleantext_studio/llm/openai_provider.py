from __future__ import annotations

import openai

from .base import LLMProvider
from .exceptions import (
    AuthenticationError,
    ModelNotFoundError,
    NetworkError,
    PermissionDeniedError,
    ProviderServerError,
    RateLimitError,
    RequestTimeoutError,
    UserCancelledError,
)
from .models import OptimizationMode, ProviderConfig
from .prompts import build_messages
from .response_parser import parse_response
from .schemas import OptimizationResponse


class OpenAIProvider(LLMProvider):
    def __init__(self, config: ProviderConfig, api_key: str) -> None:
        super().__init__(config, api_key)
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            default_headers=config.custom_headers,
        )

    def _translate(self, exc: Exception) -> Exception:
        if isinstance(exc, openai.AuthenticationError):
            return AuthenticationError("API authentication failed")
        if isinstance(exc, openai.PermissionDeniedError):
            return PermissionDeniedError("API permission denied")
        if isinstance(exc, openai.NotFoundError):
            return ModelNotFoundError("Model or endpoint not found")
        if isinstance(exc, openai.RateLimitError):
            return RateLimitError("Provider rate limit reached")
        if isinstance(exc, openai.APITimeoutError):
            return RequestTimeoutError("Provider request timed out")
        if isinstance(exc, openai.APIConnectionError):
            return NetworkError("Provider network connection failed")
        if isinstance(exc, openai.InternalServerError):
            return ProviderServerError("Provider server error")
        return ProviderServerError("Provider request failed")

    def test_connection(self) -> None:
        try:
            self.client.models.list()
        except Exception as exc:
            raise self._translate(exc) from exc

    def list_models(self) -> list[str]:
        try:
            return [item.id for item in self.client.models.list().data]
        except Exception as exc:
            raise self._translate(exc) from exc

    def optimize_document(
        self, text: str, mode: OptimizationMode, custom_task: str = ""
    ) -> OptimizationResponse:
        if self._cancelled.is_set():
            raise UserCancelledError("Operation cancelled")
        system, user = build_messages(text, mode, custom_task)
        kwargs: dict[str, object] = {
            "model": self.config.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "max_tokens": self.config.max_output_tokens,
            "temperature": self.config.temperature,
        }
        if self.config.structured_output:
            kwargs["response_format"] = {"type": "json_object"}
        try:
            response = self.client.chat.completions.create(**kwargs)  # type: ignore[call-overload]
            content = response.choices[0].message.content or ""
            return parse_response(content)
        except Exception as exc:
            if isinstance(exc, (AuthenticationError, UserCancelledError)):
                raise
            if exc.__class__.__module__.startswith("openai"):
                raise self._translate(exc) from exc
            raise
