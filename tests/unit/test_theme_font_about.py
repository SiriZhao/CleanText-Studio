from cleantext_studio.about_dialog import REPOSITORY, version_information
from cleantext_studio.font_manager import FontManager
from cleantext_studio.system_theme import SystemThemeWatcher
from cleantext_studio.theme import Theme, stylesheet


class Reader:
    def __init__(self, theme: Theme) -> None:
        self.theme = theme

    def current(self) -> Theme:
        return self.theme


def test_system_theme_watcher_is_mockable(qtbot) -> None:
    reader = Reader(Theme.LIGHT)
    watcher = SystemThemeWatcher(reader, 5000)
    changes = []
    watcher.changed.connect(changes.append)
    assert watcher.current() == Theme.LIGHT
    reader.theme = Theme.DARK
    watcher.check()
    assert changes == [Theme.DARK]


def test_styles_cover_modern_controls() -> None:
    css = stylesheet(Theme.DARK)
    for selector in (
        "QComboBox::drop-down",
        "QCheckBox::indicator",
        "QRadioButton::indicator",
        "QMenu",
        "QToolTip",
        "QScrollBar",
    ):
        assert selector in css


def test_font_fallback_order() -> None:
    assert (
        FontManager({"HarmonyOS Sans SC", "Microsoft YaHei UI"}).ui_family() == "HarmonyOS Sans SC"
    )
    assert FontManager({"Microsoft YaHei UI"}).ui_family() == "Microsoft YaHei UI"
    assert FontManager(set()).ui_family()


def test_about_information_has_no_sensitive_context() -> None:
    value = version_information()
    assert "v1.2.2" in value and REPOSITORY in value
    assert "API Key" not in value and "Users\\" not in value
