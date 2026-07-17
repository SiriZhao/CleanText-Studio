import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from cleantext_studio.ui.theme.tokens import CONTROL_HEIGHT, RADIUS, SPACING


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
    xs: int = SPACING.spacing_xs
    sm: int = SPACING.spacing_sm
    md: int = SPACING.spacing_md
    lg: int = SPACING.spacing_lg
    xl: int = SPACING.spacing_xl
    radius_small: int = RADIUS.radius_sm
    radius_medium: int = RADIUS.radius_md
    radius_large: int = RADIUS.radius_lg
    radius_dialog: int = RADIUS.radius_xl
    control_height_small: int = CONTROL_HEIGHT.control_compact
    control_height_medium: int = CONTROL_HEIGHT.control_normal
    control_height_large: int = CONTROL_HEIGHT.control_large


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
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[2]))
    arrow = (root / "assets" / "icons" / "chevron-down.svg").as_posix()
    check = (root / "assets" / "icons" / "check.svg").as_posix()
    return f"""
    QMainWindow, QDialog, QMessageBox, QWidget {{ background:{token.background}; color:{token.text_primary}; }}
    QFrame#cardPanel {{ background:{token.surface}; border:1px solid {token.border}; border-radius:{token.radius_large}px; }}
    QLabel#panelTitle {{ background:transparent; padding:0 {token.xs}px; }}
    QLabel#ruleCount {{ background:{token.surface_alt}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:{token.sm}px; }}
    QPlainTextEdit, QTextEdit, QLineEdit, QSpinBox, QDoubleSpinBox {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:8px; selection-background-color:{token.selection}; }}
    QScrollArea {{ background:transparent; border:0; }} QScrollArea > QWidget > QWidget {{ background:transparent; }}
    QPlainTextEdit:focus, QLineEdit:focus, QComboBox:focus {{ border:1px solid {token.accent}; }}
    QPushButton, QToolButton {{ min-height:{token.control_height_medium}px; padding:2px 12px; border:1px solid {token.border}; border-radius:{token.radius_medium}px; background:{token.surface}; }}
    QPushButton:hover, QToolButton:hover {{ border-color:{token.border_hover}; background:{token.surface_alt}; }}
    QPushButton:pressed {{ background:{token.accent_pressed}; color:white; }} QPushButton:disabled {{ color:{token.text_disabled}; }}
    QPushButton#primary {{ color:white; background:{token.accent}; border:none; min-height:{token.control_height_large}px; font-weight:600; }} QPushButton#primary:hover {{ background:{token.accent_hover}; }}
    QPushButton#danger {{ color:{token.error}; }} QLabel#muted {{ color:{token.text_secondary}; }}
    QComboBox {{ min-height:{token.control_height_medium}px; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:0 32px 0 10px; background:{token.surface}; }}
    QComboBox::drop-down {{ width:28px; border:0; border-top-right-radius:{token.radius_medium}px; border-bottom-right-radius:{token.radius_medium}px; }} QComboBox::down-arrow {{ image:url({arrow}); width:12px; height:12px; }}
    QComboBox QAbstractItemView {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:6px; selection-background-color:{token.selection}; outline:0; }}
    QCheckBox {{ spacing:{token.sm}px; }} QCheckBox::indicator {{ width:17px; height:17px; border:1px solid {token.border}; border-radius:{token.radius_small}px; background:{token.surface}; }} QCheckBox::indicator:hover {{ border-color:{token.border_hover}; background:{token.surface_alt}; }} QCheckBox::indicator:pressed {{ background:{token.selection}; }} QCheckBox::indicator:checked {{ background:{token.accent}; border-color:{token.accent}; image:url({check}); }} QCheckBox::indicator:checked:hover {{ background:{token.accent_hover}; }} QCheckBox::indicator:checked:disabled {{ background:{token.text_disabled}; border-color:{token.text_disabled}; }} QCheckBox::indicator:focus {{ border:2px solid {token.accent}; }}
    QRadioButton::indicator {{ width:17px; height:17px; border:1px solid {token.border}; border-radius:9px; }} QRadioButton::indicator:checked {{ background:{token.accent}; border:4px solid {token.surface}; }}
    QMenu {{ background:{token.surface}; color:{token.text_primary}; border:1px solid {token.border}; border-radius:{token.radius_medium}px; padding:6px; }} QMenu::item:selected {{ background:{token.selection}; border-radius:6px; }}
    QToolTip {{ color:{token.text_primary}; background:{token.surface_alt}; border:1px solid {token.border}; border-radius:6px; padding:6px; }}
    QToolBar QToolButton {{ min-height:36px; padding:0 12px; font-size:13px; margin-left:6px; }} QToolButton::menu-indicator {{ image:none; width:0; }}
    QScrollBar:vertical {{ width:12px; background:transparent; }} QScrollBar::handle:vertical {{ min-height:30px; background:{token.border}; border-radius:6px; }} QScrollBar::handle:vertical:hover {{ background:{token.border_hover}; }} QScrollBar::add-line, QScrollBar::sub-line {{ height:0; }}
    """
