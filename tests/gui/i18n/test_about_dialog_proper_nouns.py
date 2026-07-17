"""About facts must not be changed by localization."""

from __future__ import annotations

from PySide6.QtCore import QSettings

from cleantext_studio import __version__
from cleantext_studio.about_dialog import REPOSITORY, AboutDialog, version_information
from cleantext_studio.about_view_model import COPYRIGHT, DEVELOPER, LICENSE_NAME, PRODUCT_NAME
from cleantext_studio.i18n import I18nService

LOCALES = ("zh_CN", "en_US", "zh_TW", "ja_JP", "ko_KR", "es_ES", "fr_FR", "de_DE", "pt_BR", "ru_RU", "ar", "hi_IN")


def test_about_dialog_keeps_project_facts_constant_in_every_locale(qtbot: object) -> None:
    service = I18nService(QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "CleanTextStudioTests", "about-proper-nouns"))
    dialog = AboutDialog(service)
    qtbot.addWidget(dialog)  # type: ignore[attr-defined]

    for locale in LOCALES:
        service.set_language(locale)
        visible = "\n".join((dialog.title.text(), dialog.subtitle.text(), dialog.facts.text(), dialog.explanation.text()))
        assert PRODUCT_NAME in visible
        assert DEVELOPER in visible
        assert f"v{__version__}" in visible
        assert LICENSE_NAME in visible
        assert REPOSITORY in visible
        assert COPYRIGHT in visible
        assert "赵思雨" not in visible
        assert "麻省理工学院许可证" not in visible


def test_copied_version_information_uses_localized_labels_only() -> None:
    service = I18nService(QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "CleanTextStudioTests", "about-copy"))
    service.set_language("zh_CN")
    copied = version_information(service)
    for fact in (PRODUCT_NAME, DEVELOPER, LICENSE_NAME, REPOSITORY, f"v{__version__}"):
        assert fact in copied
