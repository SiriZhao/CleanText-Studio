"""Semantic palette names shared by light and dark stylesheets."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ThemePalette:
    app_background: str
    surface: str
    surface_elevated: str
    surface_subtle: str
    surface_hover: str
    surface_pressed: str
    border: str
    border_hover: str
    border_focus: str
    text_primary: str
    text_secondary: str
    text_disabled: str
    accent: str
    accent_hover: str
    accent_pressed: str
    danger: str
    warning: str
    success: str
    selection: str
