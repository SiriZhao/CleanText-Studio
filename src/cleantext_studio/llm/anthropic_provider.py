import anthropic

from .base import LLMProvider
from .exceptions import (
    AuthenticationError,
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


class AnthropicProvider(LLMProvider):
    def __init__(self, config: ProviderConfig, api_key: str) -> None:
        super().__init__(config, api_key)
        self.client = anthropic.Anthropic(
            api_key=api_key, base_url=config.base_url, timeout=config.timeout
        )

    def _translate(self, exc: Exception) -> Exception:
        if isinstance(exc, anthropic.AuthenticationError):
            return AuthenticationError("API authentication failed")
        if isinstance(exc, anthropic.PermissionDeniedError):
            return PermissionDeniedError("API permission denied")
        if isinstance(exc, anthropic.RateLimitError):
            return RateLimitError("Provider rate limit reached")
        if isinstance(exc, anthropic.APITimeoutError):
            return RequestTimeoutError("Provider request timed out")
        if isinstance(exc, anthropic.APIConnectionError):
            return NetworkError("Provider network connection failed")
        return ProviderServerError("Provider request failed")

    def test_connection(self) -> None:
        self.optimize_document("test", OptimizationMode.STRUCTURE)

    def list_models(self) -> list[str]:
        return []

    def optimize_document(
        self, text: str, mode: OptimizationMode, custom_task: str = ""
    ) -> OptimizationResponse:
        if self._cancelled.is_set():
            raise UserCancelledError("Operation cancelled")
        system, user = build_messages(text, mode, custom_task)
        try:
            response = self.client.messages.create(
                model=self.config.model,
                system=system,
                messages=[{"role": "user", "content": user}],
                max_tokens=self.config.max_output_tokens,
                temperature=self.config.temperature,
            )
            content = "".join(str(getattr(block, "text", "")) for block in response.content)
            return parse_response(content)
        except Exception as exc:
            if exc.__class__.__module__.startswith("anthropic"):
                raise self._translate(exc) from exc
            raise
