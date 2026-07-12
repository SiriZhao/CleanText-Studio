from .anthropic_provider import AnthropicProvider
from .base import LLMProvider
from .models import ProviderConfig, ProviderType
from .openai_provider import OpenAIProvider


def create_provider(config: ProviderConfig, api_key: str) -> LLMProvider:
    if config.provider_type == ProviderType.ANTHROPIC:
        return AnthropicProvider(config, api_key)
    return OpenAIProvider(config, api_key)
