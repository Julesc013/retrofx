"""Color helpers for the experimental 2.x core scaffold."""

from __future__ import annotations

import re
from typing import Iterable

HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def is_hex_color(value: object) -> bool:
    return isinstance(value, str) and HEX_COLOR_RE.match(value) is not None


def normalize_hex_color(value: str) -> str:
    """Return a lower-case six-digit hex color."""
    if not is_hex_color(value):
        raise ValueError(f"Unsupported color literal: {value!r}")

    stripped = value.strip().lower()
    if len(stripped) == 4:
        return "#" + "".join(channel * 2 for channel in stripped[1:])
    return stripped


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    normalized = normalize_hex_color(value)
    return (
        int(normalized[1:3], 16),
        int(normalized[3:5], 16),
        int(normalized[5:7], 16),
    )


def rgb_to_hex(rgb: Iterable[int]) -> str:
    channels = tuple(max(0, min(255, int(channel))) for channel in rgb)
    return "#{:02x}{:02x}{:02x}".format(*channels)


def mix_colors(color_a: str, color_b: str, amount_a: float) -> str:
    """Blend two colors.

    `amount_a` expresses the weight of `color_a` in the result.
    """
    amount_a = max(0.0, min(1.0, amount_a))
    amount_b = 1.0 - amount_a
    a_r, a_g, a_b = hex_to_rgb(color_a)
    b_r, b_g, b_b = hex_to_rgb(color_b)
    return rgb_to_hex(
        (
            round(a_r * amount_a + b_r * amount_b),
            round(a_g * amount_a + b_g * amount_b),
            round(a_b * amount_a + b_b * amount_b),
        )
    )


def lighten(color: str, amount: float) -> str:
    return mix_colors(color, "#ffffff", 1.0 - amount)


def darken(color: str, amount: float) -> str:
    return mix_colors(color, "#000000", 1.0 - amount)


def relative_luminance(color: str) -> float:
    def _channel(value: int) -> float:
        component = value / 255.0
        if component <= 0.03928:
            return component / 12.92
        return ((component + 0.055) / 1.055) ** 2.4

    red, green, blue = hex_to_rgb(color)
    return 0.2126 * _channel(red) + 0.7152 * _channel(green) + 0.0722 * _channel(blue)


def contrast_ratio(color_a: str, color_b: str) -> float:
    lum_a = relative_luminance(color_a)
    lum_b = relative_luminance(color_b)
    lighter = max(lum_a, lum_b)
    darker = min(lum_a, lum_b)
    return (lighter + 0.05) / (darker + 0.05)


def pick_best_contrast(base: str, candidates: Iterable[str]) -> str:
    normalized_candidates = [normalize_hex_color(candidate) for candidate in candidates]
    return max(normalized_candidates, key=lambda candidate: contrast_ratio(base, candidate))

