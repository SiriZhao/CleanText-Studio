from dataclasses import dataclass
from enum import StrEnum


class Theme(StrEnum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


@dataclass(slots=True, frozen=True)
class DesignToken:
    background: str
    surface: str
    surface_alt: str
    border: str
    border_hover: str
    text_primary: str
    text_secondary: str
    text_disabled: str
    accent: str
    accent_hover: str
    accent_pressed: str
    success: str
    warning: str
    error: str
    selection: str
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    radius_small: int = 6
    radius_medium: int = 10
    radius_large: int = 14


LIGHT = DesignToken(
    "#f5f7fb",
    "#ffffff",
    "#f0f3f9",
    "#d9deea",
    "#746be0",
    "#202437",
    "#687086",
    "#a2a8b7",
    "#6257d5",
    "#7469e2",
    "#5147bc",
    "#3b9b70",
    "#c58a2a",
    "#c84b55",
    "#ddd9ff",
)
DARK = DesignToken(
    "#171923",
    "#202330",
    "#272b3a",
    "#373c4e",
    "#8379ea",
    "#edf0f7",
    "#aeb6ca",
    "#697083",
    "#756be0",
    "#887ef0",
    "#6258c8",
    "#58b98c",
    "#d5a34c",
    "#e06b75",
    "#3e386d",
)


def stylesheet(theme: Theme) -> str:
    token = DARK if theme == Theme.DARK else LIGHT
    return f"""
    QMainWindow, QDialog, QMessageBox, QWidget {{ background:{token.background}; color:{token.text_primary}; }}
    QFrame#panel {{ background:{token.surface}; border:1px solid {token.border}; border-radius:{token.radius_large}px; }}
    QPlainTextEdit, QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:8px; selection-background-color:{token.selection}; }}
    QPlainTextEdit:focus, QLineEdit:focus, QComboBox:focus {{ border:1px solid {token.accent}; }}
    QPushButton, QToolButton {{ min-height:32px; padding:2px 12px; border:1px solid {token.border}; border-radius:{token.radius_medium}px; background:{token.surface}; }}
    QPushButton:hover, QToolButton:hover {{ border-color:{token.border_hover}; background:{token.surface_alt}; }}
    QPushButton:pressed {{ background:{token.accent_pressed}; color:white; }} QPushButton:disabled {{ color:{token.text_disabled}; }}
    QPushButton#primary {{ color:white; background:{token.accent}; border:none; min-height:42px; font-weight:600; }} QPushButton#primary:hover {{ background:{token.accent_hover}; }}
    QPushButton#danger {{ color:{token.error}; }} QLabel#muted {{ color:{token.text_secondary}; }}
    QComboBox {{ min-height:34px; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:0 32px 0 10px; background:{token.surface}; }}
    QComboBox::drop-down {{ width:28px; border:0; border-top-right-radius:{token.radius_medium}px; border-bottom-right-radius:{token.radius_medium}px; }}
    QComboBox QAbstractItemView {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:6px; selection-background-color:{token.selection}; outline:0; }}
    QCheckBox::indicator {{ width:17px; height:17px; border:1px solid {token.border}; border-radius:5px; background:{token.surface}; }} QCheckBox::indicator:checked {{ background:{token.accent}; border-color:{token.accent}; }}
    QRadioButton::indicator {{ width:17px; height:17px; border:1px solid {token.border}; border-radius:9px; }} QRadioButton::indicator:checked {{ background:{token.accent}; border:4px solid {token.surface}; }}
    QMenu {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:6px; }} QMenu::item:selected {{ background:{token.selection}; border-radius:6px; }}
    QToolTip {{ color:{token.text_primary}; background:{token.surface_alt}; border:1px solid {token.border}; border-radius:6px; padding:6px; }}
    QScrollBar:vertical {{ width:12px; background:transparent; }} QScrollBar::handle:vertical {{ min-height:30px; background:{token.border}; border-radius:6px; }} QScrollBar::handle:vertical:hover {{ background:{token.border_hover}; }} QScrollBar::add-line, QScrollBar::sub-line {{ height:0; }}
    """
