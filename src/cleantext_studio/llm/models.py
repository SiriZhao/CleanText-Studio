from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ProviderType(StrEnum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"
    OPENAI_COMPATIBLE = "openai_compatible"
    LOCAL = "local"


class OptimizationMode(StrEnum):
    STRUCTURE = "structure"
    LINE_BREAKS = "line_breaks"
    LIGHT_CLEANUP = "light_cleanup"
    LIST_NATURALIZATION = "list_naturalization"
    ACADEMIC_STRUCTURE = "academic_structure"
    CUSTOM = "custom"


class ProviderConfig(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    provider_type: ProviderType
    base_url: str = Field(max_length=500)
    model: str = Field(min_length=1, max_length=200)
    timeout: float = Field(60, ge=5, le=600)
    max_output_tokens: int = Field(4096, ge=128, le=100_000)
    temperature: float = Field(0.1, ge=0, le=2)
    structured_output: bool = True
    custom_headers: dict[str, str] = Field(default_factory=dict)

    @field_validator("base_url")
    @classmethod
    def validate_url(cls, value: str, info: object) -> str:
        if "\r" in value or "\n" in value:
            raise ValueError("Base URL contains invalid newline")
        if not value.startswith(
            ("https://", "http://localhost", "http://127.0.0.1", "http://[::1]")
        ):
            raise ValueError("Only HTTPS or local HTTP endpoints are allowed")
        return value.rstrip("/")

    @field_validator("custom_headers")
    @classmethod
    def validate_headers(cls, value: dict[str, str]) -> dict[str, str]:
        if any("\r" in k + v or "\n" in k + v for k, v in value.items()):
            raise ValueError("Header newline injection rejected")
        forbidden = {"authorization", "cookie", "proxy-authorization"}
        if any(k.lower() in forbidden for k in value):
            raise ValueError("Authentication headers must use the credential store")
        return value
