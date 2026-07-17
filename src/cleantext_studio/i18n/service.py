"""Public, presentation-focused localization service."""

from __future__ import annotations

from PySide6.QtCore import QSettings

from .manager import I18nManager
from .validation import validate_catalogs


class I18nService(I18nManager):
    """Adds atomic catalog validation to the existing Qt signal service."""

    def __init__(self, settings: QSettings | None = None) -> None:
        super().__init__(settings)
        self._active = self._validated_locale(self._active)

    def catalog_is_complete(self, locale: str) -> bool:
        return validate_catalogs().get(locale, False)

    def set_language(self, code: str) -> None:
        """Switch as one catalog transaction; never apply a per-key fallback."""
        if code not in {item.code for item in self.languages()}:
            code = "system"
        self._preference = code
        self.settings.setValue("language", code)
        active = self._validated_locale(self.resolve(code))
        if active != self._active or code == "system":
            self._active = active
            self.language_changed.emit(active)

    def _validated_locale(self, locale: str) -> str:
        return locale if self.catalog_is_complete(locale) else "en_US"
