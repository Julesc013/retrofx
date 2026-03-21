"""Shared helpers for terminal and TUI target compilers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from v2.targets.common import (
    has_non_default_display_policy,
    has_non_default_typography_aa,
    require_mapping,
    write_target_artifact,
)

ANSI_NAMES = {
    "0": "black",
    "1": "red",
    "2": "green",
    "3": "yellow",
    "4": "blue",
    "5": "magenta",
    "6": "cyan",
    "7": "white",
    "8": "bright_black",
    "9": "bright_red",
    "10": "bright_green",
    "11": "bright_yellow",
    "12": "bright_blue",
    "13": "bright_magenta",
    "14": "bright_cyan",
    "15": "bright_white",
}


@dataclass(slots=True)
class TerminalThemeContext:
    profile_id: str
    profile_name: str
    requested_target_classes: list[str]
    background: str
    foreground: str
    cursor: str
    cursor_text: str
    selection_bg: str
    selection_fg: str
    terminal_ansi: dict[str, str]
    semantic: dict[str, str]
    console_font: str
    terminal_primary: str
    terminal_fallbacks: list[str]
    terminal_stack: list[str]
    ui_sans: str
    ui_mono: str
    icon_font: str
    emoji_policy: str
    aa_antialias: str
    aa_subpixel: str
    aa_hinting: str
    render_mode: str
    render_effects: dict[str, Any]
    render_display: dict[str, Any]


def build_terminal_theme_context(resolved_profile: Mapping[str, Any]) -> TerminalThemeContext:
    identity = require_mapping(resolved_profile, "identity")
    semantics = require_mapping(resolved_profile, "semantics")
    color = require_mapping(semantics, "color")
    semantic = require_mapping(color, "semantic")
    typography = require_mapping(semantics, "typography")
    render = require_mapping(semantics, "render")
    session = require_mapping(semantics, "session")
    terminal_ansi = require_mapping(color, "terminal_ansi")

    return TerminalThemeContext(
        profile_id=str(identity["id"]),
        profile_name=str(identity["name"]),
        requested_target_classes=list(session["requested_targets"]),
        background=str(semantic["bg0"]),
        foreground=str(semantic["fg0"]),
        cursor=str(semantic["cursor"]),
        cursor_text=str(semantic["cursor_text"]),
        selection_bg=str(semantic["selection_bg"]),
        selection_fg=str(semantic["selection_fg"]),
        terminal_ansi={str(slot): str(value) for slot, value in terminal_ansi.items()},
        semantic={str(key): str(value) for key, value in semantic.items()},
        console_font=str(typography.get("console_font", "")),
        terminal_primary=str(typography.get("terminal_primary", "")),
        terminal_fallbacks=[str(value) for value in typography.get("terminal_fallbacks", [])],
        terminal_stack=[str(value) for value in typography.get("terminal_stack", [])],
        ui_sans=str(typography.get("ui_sans", "")),
        ui_mono=str(typography.get("ui_mono", "")),
        icon_font=str(typography.get("icon_font", "")),
        emoji_policy=str(typography.get("emoji_policy", "inherit")),
        aa_antialias=str(typography.get("aa", {}).get("antialias", "default")),
        aa_subpixel=str(typography.get("aa", {}).get("subpixel", "default")),
        aa_hinting=str(typography.get("aa", {}).get("hinting", "default")),
        render_mode=str(render["mode"]),
        render_effects=dict(render.get("effects", {})),
        render_display=dict(render.get("display", {})),
    )


def render_warning_for_terminal_family(context: TerminalThemeContext, supported_target_classes: tuple[str, ...]) -> list[str]:
    warnings: list[str] = []

    if context.render_mode != "passthrough":
        warnings.append(
            "Resolved render policy is not emitted by terminal/TUI targets; only the resolved terminal palette and theme tokens were compiled."
        )

    if has_non_default_display_policy(context.render_display):
        warnings.append("Render display-transform policy is ignored by terminal/TUI targets in TWO-09.")

    if has_non_default_typography_aa(
        {
            "antialias": context.aa_antialias,
            "subpixel": context.aa_subpixel,
            "hinting": context.aa_hinting,
        }
    ):
        warnings.append(
            "Explicit typography AA policy is present in the resolved profile, but terminal targets only emit it when a concrete backend format supports it."
        )

    if supported_target_classes and not set(context.requested_target_classes).intersection(supported_target_classes):
        warnings.append(
            "This target was compiled explicitly in dev mode even though the profile's requested target classes do not include this target family directly."
        )

    return warnings
