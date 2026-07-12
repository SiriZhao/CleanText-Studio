from dataclasses import dataclass, field

from .models import ProviderType


@dataclass(slots=True, frozen=True)
class ProviderPreset:
    id: str
    display_name: str
    provider_type: ProviderType
    default_base_url: str
    api_style: str
    default_models: tuple[str, ...] = ()
    supports_model_listing: bool = True
    supports_structured_output: bool = True
    api_key_required: bool = True
    base_url_editable: bool = False
    help_url: str = ""
    extra_headers: dict[str, str] = field(default_factory=dict)


PRESETS = {
    "openai": ProviderPreset(
        "openai",
        "OpenAI",
        ProviderType.OPENAI,
        "https://api.openai.com/v1",
        "openai",
        ("gpt-4.1", "gpt-4.1-mini"),
        help_url="https://platform.openai.com/docs",
    ),
    "deepseek": ProviderPreset(
        "deepseek",
        "DeepSeek",
        ProviderType.DEEPSEEK,
        "https://api.deepseek.com",
        "openai_compatible",
        ("deepseek-chat", "deepseek-reasoner"),
        help_url="https://api-docs.deepseek.com",
    ),
    "anthropic": ProviderPreset(
        "anthropic",
        "Anthropic Claude",
        ProviderType.ANTHROPIC,
        "https://api.anthropic.com",
        "anthropic",
        ("claude-sonnet-4-5",),
        help_url="https://docs.anthropic.com",
    ),
    "openai_compatible": ProviderPreset(
        "openai_compatible",
        "OpenAI 兼容接口",
        ProviderType.OPENAI_COMPATIBLE,
        "",
        "openai_compatible",
        (),
        api_key_required=False,
        base_url_editable=True,
    ),
    "local": ProviderPreset(
        "local",
        "本地 OpenAI 兼容模型",
        ProviderType.LOCAL,
        "http://localhost:11434/v1",
        "openai_compatible",
        ("qwen3", "llama3.2"),
        supports_model_listing=True,
        api_key_required=False,
        base_url_editable=True,
    ),
}


def get_preset(identifier: str | ProviderType) -> ProviderPreset:
    key = identifier.value if isinstance(identifier, ProviderType) else identifier
    return PRESETS[key]


def all_presets() -> tuple[ProviderPreset, ...]:
    return tuple(PRESETS.values())
