from PySide6.QtCore import QObject, QTimer, Signal

from .theme import Theme


class SystemThemeReader:
    def current(self) -> Theme:
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return Theme.LIGHT if value else Theme.DARK
        except OSError:
            return Theme.LIGHT


class SystemThemeWatcher(QObject):
    changed = Signal(object)

    def __init__(self, reader: SystemThemeReader | None = None, interval_ms: int = 5000) -> None:
        super().__init__()
        self.reader = reader or SystemThemeReader()
        self._current = self.reader.current()
        self.timer = QTimer(self)
        self.timer.setInterval(max(3000, interval_ms))
        self.timer.timeout.connect(self.check)

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()

    def current(self) -> Theme:
        return self._current

    def check(self) -> None:
        current = self.reader.current()
        if current != self._current:
            self._current = current
            self.changed.emit(current)
