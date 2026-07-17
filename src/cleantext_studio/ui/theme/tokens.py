"""Design-system metrics. Widgets must not invent their own radii or spacing."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RadiusTokens:
    radius_xs: int = 4
    radius_sm: int = 7
    radius_md: int = 10
    radius_lg: int = 14
    radius_xl: int = 18


@dataclass(frozen=True, slots=True)
class SpacingTokens:
    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 12
    spacing_lg: int = 16
    spacing_xl: int = 24


@dataclass(frozen=True, slots=True)
class ControlHeightTokens:
    control_compact: int = 30
    control_normal: int = 36
    control_large: int = 42


@dataclass(frozen=True, slots=True)
class BorderTokens:
    border_normal: int = 1
    focus_ring_width: int = 1


RADIUS = RadiusTokens()
SPACING = SpacingTokens()
CONTROL_HEIGHT = ControlHeightTokens()
