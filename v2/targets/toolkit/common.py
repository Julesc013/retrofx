"""Shared helpers for toolkit-adjacent export targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from v2.targets.common import require_mapping


@dataclass(slots=True)
class TypographyPolicyContext:
    profile_id: str
    profile_name: str
    requested_target_classes: list[str]
    console_font: str
    terminal_primary: str
    terminal_fallbacks: list[str]
    terminal_stack: list[str]
    ui_sans: str
    ui_mono: str
    ui_mono_stack: list[str]
    icon_font: str
    emoji_policy: str
    aa_antialias: str
    aa_subpixel: str
    aa_hinting: str
    fontconfig_aliases: dict[str, list[str]]


def build_typography_policy_context(resolved_profile: Mapping[str, Any]) -> TypographyPolicyContext:
    identity = require_mapping(resolved_profile, "identity")
    semantics = require_mapping(resolved_profile, "semantics")
    session = require_mapping(semantics, "session")
    typography = require_mapping(semantics, "typography")
    aa = require_mapping(typography, "aa")
    aliases = require_mapping(typography, "fontconfig_aliases")

    return TypographyPolicyContext(
        profile_id=str(identity["id"]),
        profile_name=str(identity["name"]),
        requested_target_classes=list(session["requested_targets"]),
        console_font=str(typography.get("console_font", "")),
        terminal_primary=str(typography.get("terminal_primary", "")),
        terminal_fallbacks=[str(value) for value in typography.get("terminal_fallbacks", [])],
        terminal_stack=[str(value) for value in typography.get("terminal_stack", [])],
        ui_sans=str(typography.get("ui_sans", "")),
        ui_mono=str(typography.get("ui_mono", "")),
        ui_mono_stack=[str(value) for value in typography.get("ui_mono_stack", [])],
        icon_font=str(typography.get("icon_font", "")),
        emoji_policy=str(typography.get("emoji_policy", "inherit")),
        aa_antialias=str(aa.get("antialias", "default")),
        aa_subpixel=str(aa.get("subpixel", "default")),
        aa_hinting=str(aa.get("hinting", "default")),
        fontconfig_aliases={str(key): [str(item) for item in value] for key, value in aliases.items()},
    )
