import json
from pathlib import Path

from platformdirs import user_config_path

from .models import ProviderConfig


class ProviderConfigStore:
    """Persist provider metadata only; API keys are intentionally excluded."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or user_config_path("CleanText Studio") / "providers.json"

    def load(self) -> list[ProviderConfig]:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [ProviderConfig.model_validate(item) for item in data.get("providers", [])]

    def save(self, providers: list[ProviderConfig]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "providers": [item.model_dump(mode="json") for item in providers],
        }
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.path)

    def export_without_keys(self, path: Path, providers: list[ProviderConfig]) -> None:
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "providers": [item.model_dump(mode="json") for item in providers],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
