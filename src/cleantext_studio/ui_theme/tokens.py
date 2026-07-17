"""Single source of visual metrics for desktop widgets."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RadiusTokens:
    xs: int = 4
    sm: int = 7
    md: int = 10
    lg: int = 14
    xl: int = 18


@dataclass(frozen=True, slots=True)
class SpacingTokens:
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24


@dataclass(frozen=True, slots=True)
class ControlHeightTokens:
    compact: int = 30
    normal: int = 36
    large: int = 42


RADIUS = RadiusTokens()
SPACING = SpacingTokens()
CONTROL_HEIGHT = ControlHeightTokens()
