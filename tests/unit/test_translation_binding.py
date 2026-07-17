from PySide6.QtWidgets import QLabel

from cleantext_studio.i18n.bindings import TranslatableTextBinding
from cleantext_studio.i18n.service import I18nService


def test_binding_refreshes_widget_after_language_signal(qtbot) -> None:
    label = QLabel()
    qtbot.addWidget(label)
    service = I18nService()
    registry = TranslatableTextBinding(service)
    registry.bind(label, "action.clean", lambda widget, text: widget.setText(text))
    assert label.text() == service.tr("action.clean")
    service.set_language("en_US")
    assert label.text() == "Clean"
