"""Shared helpers for the experimental 2.x X11 render compilers."""

from __future__ import annotations

from dataclasses import dataclass
from math import log
from pathlib import Path
from typing import Any, Mapping

from v2.core.color_utils import hex_to_rgb
from v2.render import build_display_policy_summary, build_x11_render_summary
from v2.targets.common import require_mapping


@dataclass(slots=True)
class X11RenderContext:
    profile_id: str
    profile_name: str
    requested_target_classes: list[str]
    background: str
    foreground: str
    glow_tint: str
    cursor: str
    selection_bg: str
    selection_fg: str
    terminal_ansi: dict[str, str]
    render_mode: str
    implemented_mode: str
    monochrome_bands: int
    palette_kind: str | None
    palette_size: int | None
    effects: dict[str, Any]
    display: dict[str, Any]
    display_policy: dict[str, Any]
    x11_render: dict[str, Any]


def build_x11_render_context(
    resolved_profile: Mapping[str, Any],
    *,
    environment: Mapping[str, Any] | None = None,
    display_policy: Mapping[str, Any] | None = None,
    x11_render: Mapping[str, Any] | None = None,
) -> X11RenderContext:
    identity = require_mapping(resolved_profile, "identity")
    semantics = require_mapping(resolved_profile, "semantics")
    color = require_mapping(semantics, "color")
    semantic = require_mapping(color, "semantic")
    render = require_mapping(semantics, "render")
    session = require_mapping(semantics, "session")
    terminal_ansi = require_mapping(color, "terminal_ansi")

    resolved_display_policy = dict(display_policy or build_display_policy_summary(resolved_profile, environment))
    resolved_x11_render = dict(x11_render or build_x11_render_summary(resolved_profile, environment))
    palette = dict(render.get("palette", {}))

    return X11RenderContext(
        profile_id=str(identity["id"]),
        profile_name=str(identity["name"]),
        requested_target_classes=list(session["requested_targets"]),
        background=str(semantic["bg0"]),
        foreground=str(semantic["fg0"]),
        glow_tint=str(semantic["glow_tint"]),
        cursor=str(semantic["cursor"]),
        selection_bg=str(semantic["selection_bg"]),
        selection_fg=str(semantic["selection_fg"]),
        terminal_ansi={str(slot): str(value) for slot, value in terminal_ansi.items()},
        render_mode=str(render["mode"]),
        implemented_mode=str(resolved_x11_render["implemented_mode"]),
        monochrome_bands=int(render.get("quantization", {}).get("bands") or 8),
        palette_kind=str(palette.get("kind")) if palette.get("kind") is not None else None,
        palette_size=int(palette.get("size")) if palette.get("size") is not None else None,
        effects=dict(render.get("effects", {})),
        display=dict(render.get("display", {})),
        display_policy=resolved_display_policy,
        x11_render=resolved_x11_render,
    )


def build_x11_warnings(context: X11RenderContext, supported_target_classes: tuple[str, ...]) -> list[str]:
    warnings = list(context.x11_render.get("warnings", []))
    for degraded in context.x11_render.get("degraded_fields", []):
        warnings.append(
            f"{degraded['path']} requested `{degraded['requested']}`; emitted X11 artifacts implement `{degraded['implemented_as']}` instead."
        )

    if supported_target_classes and not set(context.requested_target_classes).intersection(supported_target_classes):
        warnings.append(
            "This X11 target was compiled explicitly in dev mode even though the profile's requested target classes do not include `x11`."
        )

    return _dedupe(warnings)


def srgb_triplet(color: str) -> tuple[float, float, float]:
    red, green, blue = hex_to_rgb(color)
    return red / 255.0, green / 255.0, blue / 255.0


def linear_triplet(color: str) -> tuple[float, float, float]:
    return tuple(channel**2.2 for channel in srgb_triplet(color))


def glsl_vec3(color: str, *, linear: bool = True) -> str:
    triplet = linear_triplet(color) if linear else srgb_triplet(color)
    return "vec3({:.6f}, {:.6f}, {:.6f})".format(*triplet)


def display_tint_triplet(display: Mapping[str, Any]) -> tuple[tuple[float, float, float], float]:
    temperature = int(display.get("temperature", 6500))
    blue_light_reduction = float(display.get("blue_light_reduction", 0.0))
    tint_bias = display.get("tint_bias")

    temp_triplet = _kelvin_to_srgb_triplet(temperature)
    tint_strength = min(1.0, max(0.0, abs(6500 - temperature) / 3500.0 + blue_light_reduction * 0.65))
    if isinstance(tint_bias, str) and tint_bias:
        tint_triplet = srgb_triplet(tint_bias)
        temp_triplet = tuple(temp_triplet[idx] * 0.7 + tint_triplet[idx] * 0.3 for idx in range(3))
        tint_strength = max(tint_strength, 0.18)
    return temp_triplet, tint_strength


def _kelvin_to_srgb_triplet(temperature: int) -> tuple[float, float, float]:
    temp = max(1000, min(12000, int(temperature))) / 100.0
    if temp <= 66:
        red = 255.0
        green = 99.4708025861 * log(temp) - 161.1195681661
        blue = 0.0 if temp <= 19 else 138.5177312231 * log(temp - 10.0) - 305.0447927307
    else:
        red = 329.698727446 * ((temp - 60.0) ** -0.1332047592)
        green = 288.1221695283 * ((temp - 60.0) ** -0.0755148492)
        blue = 255.0
    return tuple(max(0.0, min(255.0, value)) / 255.0 for value in (red, green, blue))


def relative_shader_path(from_dir: Path, to_dir: Path, file_name: str) -> str:
    return str((Path("..") / to_dir.name / file_name).as_posix())


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
