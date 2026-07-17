from PySide6.QtCore import QSettings

from cleantext_studio.i18n import I18nService


def test_i18n_service_exposes_catalog_validation() -> None:
    service = I18nService()
    completeness = service.catalog_is_complete("en_US")
    assert completeness is True


def test_complete_catalog_switches_to_requested_locale() -> None:
    settings = QSettings("CleanText Studio tests", "atomic locale")
    settings.clear()
    service = I18nService(settings)
    service.set_language("es_ES")
    assert service.active == "es_ES"
