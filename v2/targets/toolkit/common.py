"""Shared helpers for toolkit-adjacent export targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from v2.core.color_utils import mix_colors, relative_luminance
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


@dataclass(slots=True)
class ToolkitStyleContext:
    profile_id: str
    profile_name: str
    family: str
    strictness: str
    requested_target_classes: list[str]
    theme_hint_name: str
    background: str
    background_alt: str
    background_inactive: str
    foreground: str
    foreground_alt: str
    foreground_muted: str
    accent_primary: str
    accent_info: str
    accent_success: str
    accent_warn: str
    accent_error: str
    accent_muted: str
    border_active: str
    border_inactive: str
    selection_bg: str
    selection_fg: str
    menu_bg: str
    menu_fg: str
    status_bg: str
    status_fg: str
    cursor_color: str
    cursor_text: str
    ui_sans: str
    ui_mono: str
    ui_mono_stack: list[str]
    terminal_primary: str
    terminal_fallbacks: list[str]
    emoji_policy: str
    aa_antialias: str
    aa_subpixel: str
    aa_hinting: str
    icon_theme: str
    icon_variant: str
    cursor_theme: str
    cursor_size: int
    cursor_variant: str
    prefer_dark_theme: bool


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


def build_toolkit_style_context(resolved_profile: Mapping[str, Any]) -> ToolkitStyleContext:
    identity = require_mapping(resolved_profile, "identity")
    semantics = require_mapping(resolved_profile, "semantics")
    color = require_mapping(semantics, "color")
    semantic = require_mapping(color, "semantic")
    typography = require_mapping(semantics, "typography")
    aa = require_mapping(typography, "aa")
    chrome = require_mapping(semantics, "chrome")
    session = require_mapping(semantics, "session")

    background = str(semantic["bg0"])
    background_alt = str(semantic["bg1"])
    background_inactive = str(semantic["bg2"])
    foreground = str(semantic["fg0"])
    foreground_alt = str(semantic["fg1"])
    foreground_muted = str(semantic["fg2"])
    accent_primary = str(semantic["accent_primary"])
    accent_muted = str(semantic["accent_muted"])
    menu_bg = str(semantic.get("menu_bg", background_alt))
    menu_fg = str(semantic.get("menu_fg", foreground))
    status_bg = str(semantic.get("status_bg", background_alt))
    status_fg = str(semantic.get("status_fg", foreground_alt))
    theme_hint_name = f"retrofx-{str(identity['id']).strip().lower()}"

    return ToolkitStyleContext(
        profile_id=str(identity["id"]),
        profile_name=str(identity["name"]),
        family=str(identity.get("family", "custom")),
        strictness=str(identity.get("strictness", "modernized-retro")),
        requested_target_classes=list(session["requested_targets"]),
        theme_hint_name=theme_hint_name,
        background=background,
        background_alt=background_alt,
        background_inactive=background_inactive,
        foreground=foreground,
        foreground_alt=foreground_alt,
        foreground_muted=foreground_muted,
        accent_primary=accent_primary,
        accent_info=str(semantic["accent_info"]),
        accent_success=str(semantic["accent_success"]),
        accent_warn=str(semantic["accent_warn"]),
        accent_error=str(semantic["accent_error"]),
        accent_muted=accent_muted,
        border_active=str(semantic["border_active"]),
        border_inactive=str(semantic["border_inactive"]),
        selection_bg=str(semantic["selection_bg"]),
        selection_fg=str(semantic["selection_fg"]),
        menu_bg=menu_bg,
        menu_fg=menu_fg,
        status_bg=status_bg,
        status_fg=status_fg,
        cursor_color=str(semantic["cursor"]),
        cursor_text=str(semantic["cursor_text"]),
        ui_sans=str(typography.get("ui_sans", "")),
        ui_mono=str(typography.get("ui_mono", "")),
        ui_mono_stack=[str(value) for value in typography.get("ui_mono_stack", [])],
        terminal_primary=str(typography.get("terminal_primary", "")),
        terminal_fallbacks=[str(value) for value in typography.get("terminal_fallbacks", [])],
        emoji_policy=str(typography.get("emoji_policy", "inherit")),
        aa_antialias=str(aa.get("antialias", "default")),
        aa_subpixel=str(aa.get("subpixel", "default")),
        aa_hinting=str(aa.get("hinting", "default")),
        icon_theme=str(chrome.get("icon_theme", "")),
        icon_variant=str(chrome.get("icon_variant", "")),
        cursor_theme=str(chrome.get("cursor_theme", "")),
        cursor_size=int(chrome.get("cursor_size", 24)),
        cursor_variant=str(chrome.get("cursor_variant", "")),
        prefer_dark_theme=relative_luminance(background) < 0.35,
    )


def build_toolkit_style_summary(
    resolved_profile: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> dict[str, Any]:
    context = build_toolkit_style_context(resolved_profile)
    session_type = str(environment.get("session_type", "unknown-headless"))
    meaningful_now = session_type in {"x11", "wayland", "remote-ssh"}
    overall_status = "export-only-advisory" if meaningful_now else "degraded-export-only"
    warnings: list[str] = []
    notes = [
        "Toolkit outputs are export-oriented advisory artifacts in TWO-18.",
        "Live GNOME, Plasma, or cross-DE settings mutation is not implemented.",
    ]
    if not context.icon_theme:
        warnings.append("No explicit icon theme is resolved; toolkit exports will leave icon-theme selection advisory or empty.")
    if not context.cursor_theme:
        warnings.append("No explicit cursor theme is resolved; toolkit exports will leave cursor-theme selection advisory or empty.")
    if not meaningful_now:
        warnings.append(
            f"Current environment `{session_type}` is not a live desktop session, so toolkit outputs are still emitted but remain advisory only."
        )

    return {
        "overall_status": overall_status,
        "environment_meaningful_now": meaningful_now,
        "future_target_families": ["toolkit", "desktop-style"],
        "resolved_values": {
            "theme_hint_name": context.theme_hint_name,
            "icon_theme": context.icon_theme,
            "icon_variant": context.icon_variant,
            "cursor_theme": context.cursor_theme,
            "cursor_size": context.cursor_size,
            "cursor_variant": context.cursor_variant,
            "ui_sans": context.ui_sans,
            "ui_mono": context.ui_mono,
            "prefer_dark_theme": context.prefer_dark_theme,
        },
        "warnings": warnings,
        "notes": notes,
    }


def toolkit_export_warnings(
    context: ToolkitStyleContext,
    supported_target_classes: tuple[str, ...],
    *,
    target_label: str,
) -> list[str]:
    warnings: list[str] = []
    if supported_target_classes and not set(context.requested_target_classes).intersection(supported_target_classes):
        warnings.append(
            f"This {target_label} target was compiled explicitly in dev mode even though the profile's requested target classes do not include it directly."
        )
    if not context.icon_theme:
        warnings.append("No explicit icon theme is resolved; icon-theme output remains advisory only.")
    if not context.cursor_theme:
        warnings.append("No explicit cursor theme is resolved; cursor-theme output remains advisory only.")
    return warnings


def derive_toolkit_palette_roles(context: ToolkitStyleContext) -> dict[str, str]:
    return {
        "window": context.background_alt,
        "window_text": context.foreground,
        "base": context.background,
        "alternate_base": context.background_alt,
        "text": context.foreground,
        "button": context.status_bg,
        "button_text": context.status_fg,
        "highlight": context.selection_bg,
        "highlighted_text": context.selection_fg,
        "tooltip_base": context.menu_bg,
        "tooltip_text": context.menu_fg,
        "link": context.accent_info,
        "link_visited": context.accent_muted,
        "bright_text": context.accent_warn,
        "border_active": context.border_active,
        "border_inactive": context.border_inactive,
        "cursor": context.cursor_color,
        "cursor_text": context.cursor_text,
    }


def derive_toolkit_theme_aliases(context: ToolkitStyleContext) -> dict[str, str]:
    return {
        "gtk_theme_hint_name": context.theme_hint_name,
        "qt_style_hint_name": "Fusion",
        "desktop_family": context.family,
        "desktop_strictness": context.strictness,
    }


def derive_toolkit_emphasis(context: ToolkitStyleContext) -> dict[str, str]:
    return {
        "menu_shadow": mix_colors(context.background_inactive, context.accent_muted, 0.35),
        "panel_outline": context.border_active,
        "panel_fill": context.status_bg,
    }
