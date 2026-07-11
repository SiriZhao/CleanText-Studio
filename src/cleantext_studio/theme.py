from enum import StrEnum


class Theme(StrEnum):
    LIGHT = "light"
    DARK = "dark"


def stylesheet(theme: Theme) -> str:
    dark = theme == Theme.DARK
    bg, panel, text, border = (
        ("#171923", "#202330", "#edf0f7", "#34394a")
        if dark
        else ("#f4f6fb", "#ffffff", "#202437", "#dce1ec")
    )
    muted = "#aeb6ca" if dark else "#687086"
    return f"""
    QMainWindow, QWidget {{ background: {bg}; color: {text}; font-family: 'Microsoft YaHei UI','Segoe UI'; font-size: 13px; }}
    QFrame#panel {{ background: {panel}; border: 1px solid {border}; border-radius: 10px; }}
    QPlainTextEdit {{ background: {panel}; color: {text}; border: 1px solid {border}; border-radius: 8px; padding: 10px; font-size: 15px; selection-background-color: #6d63dc; }}
    QPushButton {{ min-height: 30px; padding: 2px 10px; border: 1px solid {border}; border-radius: 7px; background: {panel}; }}
    QPushButton:hover {{ border-color: #665bd8; }} QPushButton:disabled {{ color: {muted}; }}
    QPushButton#primary {{ color: white; background: #6257d5; border: none; min-height: 42px; font-weight: 600; }}
    QPushButton#danger {{ color: #c84b55; }} QComboBox {{ min-height: 30px; border: 1px solid {border}; border-radius: 7px; padding: 0 8px; background: {panel}; }}
    QLabel#muted {{ color: {muted}; }} QScrollBar:vertical {{ width: 12px; }}
    """
