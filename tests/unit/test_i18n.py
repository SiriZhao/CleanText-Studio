from PySide6.QtCore import QSettings

from cleantext_studio.i18n import I18nManager


def _manager() -> I18nManager:
    settings = QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, "CleanTextTest", "I18n")
    settings.clear()
    return I18nManager(settings)


def test_all_formal_languages_load_with_english_fallback() -> None:
    manager = _manager()
    for language in manager.languages():
        manager.set_language(language.code)
        assert manager.tr("action.clean")
        assert manager.tr("panel.source")


def test_language_switch_and_rtl_direction() -> None:
    manager = _manager()
    manager.set_language("ar")
    assert manager.direction().name == "RightToLeft"
    manager.set_language("en_US")
    assert manager.direction().name == "LeftToRight"


def test_missing_key_falls_back_to_english_and_internal_values_are_not_translated() -> None:
    manager = _manager()
    manager.set_language("ja_JP")
    assert manager.tr("paragraph.smart") == "Keep breaks only between major sections"
    assert manager.tr("missing.key") == "missing.key"
