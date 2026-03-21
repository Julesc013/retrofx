"""Shared helpers for the early 2.x WM target family."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from v2.core.color_utils import mix_colors, pick_best_contrast
from v2.targets.common import has_non_default_display_policy, require_mapping, write_target_artifact


@dataclass(slots=True)
class WmThemeContext:
    profile_id: str
    profile_name: str
    requested_target_classes: list[str]
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
    border_urgent: str
    selection_bg: str
    selection_fg: str
    menu_bg: str
    menu_fg: str
    status_bg: str
    status_fg: str
    shadow_tint: str
    inactive_dim: str
    glow_tint: str
    gaps: int
    bar_style: str
    launcher_style: str
    notification_style: str
    icon_theme: str
    cursor_theme: str
    ui_font: str
    ui_mono: str
    terminal_primary: str
    render_mode: str
    render_effects: dict[str, Any]
    render_display: dict[str, Any]


def build_wm_theme_context(resolved_profile: Mapping[str, Any]) -> WmThemeContext:
    identity = require_mapping(resolved_profile, "identity")
    semantics = require_mapping(resolved_profile, "semantics")
    color = require_mapping(semantics, "color")
    semantic = require_mapping(color, "semantic")
    typography = require_mapping(semantics, "typography")
    render = require_mapping(semantics, "render")
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
    border_urgent = str(semantic.get("border_urgent", semantic["accent_error"]))
    shadow_tint = str(semantic.get("shadow_tint", mix_colors(background_inactive, accent_muted, 0.35)))
    inactive_dim = str(semantic.get("inactive_dim", foreground_muted))
    ui_font = str(typography.get("ui_sans") or typography.get("terminal_primary") or typography.get("ui_mono") or "").strip()

    return WmThemeContext(
        profile_id=str(identity["id"]),
        profile_name=str(identity["name"]),
        requested_target_classes=list(session["requested_targets"]),
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
        border_urgent=border_urgent,
        selection_bg=str(semantic["selection_bg"]),
        selection_fg=str(semantic["selection_fg"]),
        menu_bg=menu_bg,
        menu_fg=menu_fg,
        status_bg=status_bg,
        status_fg=status_fg,
        shadow_tint=shadow_tint,
        inactive_dim=inactive_dim,
        glow_tint=str(semantic["glow_tint"]),
        gaps=int(chrome.get("gaps", 0)),
        bar_style=str(chrome.get("bar_style", "minimal")),
        launcher_style=str(chrome.get("launcher_style", "minimal")),
        notification_style=str(chrome.get("notification_style", "minimal")),
        icon_theme=str(chrome.get("icon_theme", "")),
        cursor_theme=str(chrome.get("cursor_theme", "")),
        ui_font=ui_font,
        ui_mono=str(typography.get("ui_mono", "")),
        terminal_primary=str(typography.get("terminal_primary", "")),
        render_mode=str(render["mode"]),
        render_effects=dict(render.get("effects", {})),
        render_display=dict(render.get("display", {})),
    )


def render_warning_for_wm_family(context: WmThemeContext, supported_target_classes: tuple[str, ...]) -> list[str]:
    warnings: list[str] = []

    if context.render_mode != "passthrough":
        warnings.append(
            "Resolved render policy is not emitted by WM targets in TWO-10; only resolved theme and chrome tokens were compiled."
        )

    if has_non_default_display_policy(context.render_display):
        warnings.append("Render display-transform policy is ignored by WM targets in TWO-10.")

    if supported_target_classes and not set(context.requested_target_classes).intersection(supported_target_classes):
        warnings.append(
            "This WM target was compiled explicitly in dev mode even though the profile's requested target classes do not include this target family directly."
        )

    return warnings


def inactive_workspace_text(context: WmThemeContext) -> str:
    return context.foreground_muted or context.foreground_alt


def focused_workspace_text(context: WmThemeContext) -> str:
    return pick_best_contrast(context.accent_primary, (context.background, context.foreground))
