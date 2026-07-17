"""Weak-reference bindings for widgets that consume catalog keys."""

from __future__ import annotations

import weakref
from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from .service import I18nService


@dataclass(slots=True)
class _Binding:
    widget: weakref.ReferenceType[QWidget]
    key: str
    setter: Callable[[QWidget, str], None]


class TranslatableTextBinding(QObject):
    """Refreshes bound widget text in one place after a locale change."""

    def __init__(self, service: I18nService) -> None:
        super().__init__()
        self._service = service
        self._bindings: list[_Binding] = []
        service.language_changed.connect(self.refresh)

    def bind(self, widget: QWidget, key: str, setter: Callable[[QWidget, str], None]) -> None:
        self._bindings.append(_Binding(weakref.ref(widget), key, setter))
        setter(widget, self._service.tr(key))

    def refresh(self, _locale: str) -> None:
        retained: list[_Binding] = []
        for binding in self._bindings:
            widget = binding.widget()
            if widget is not None:
                binding.setter(widget, self._service.tr(binding.key))
                retained.append(binding)
        self._bindings = retained
