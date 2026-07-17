"""Stable combo-box model entries with translated labels."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QComboBox

from .service import I18nService


@dataclass(frozen=True, slots=True)
class TranslatedEnumItem:
    value: object
    label_key: str
    description_key: str | None = None
    enabled: bool = True


class TranslatedEnumModel:
    """Repopulates presentation labels while preserving a stable selected value."""

    def __init__(self, service: I18nService, items: tuple[TranslatedEnumItem, ...]) -> None:
        self.service = service
        self.items = items

    def populate(self, combo: QComboBox, selected: object | None = None) -> None:
        current = combo.currentData() if selected is None else selected
        combo.blockSignals(True)
        combo.clear()
        for item in self.items:
            combo.addItem(self.service.tr(item.label_key), item.value)
        index = combo.findData(current)
        combo.setCurrentIndex(index if index >= 0 else 0)
        combo.blockSignals(False)

    def bind(self, combo: QComboBox) -> None:
        self.populate(combo)
        self.service.language_changed.connect(lambda _locale: self.populate(combo))
