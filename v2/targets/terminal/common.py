"""Shared helpers for terminal and TUI target compilers."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetArtifact

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
    terminal_primary: str
    terminal_fallbacks: list[str]
    ui_mono: str
    render_mode: str
    render_effects: dict[str, Any]
    render_display: dict[str, Any]


def build_terminal_theme_context(resolved_profile: Mapping[str, Any]) -> TerminalThemeContext:
    identity = _require_mapping(resolved_profile, "identity")
    semantics = _require_mapping(resolved_profile, "semantics")
    color = _require_mapping(semantics, "color")
    semantic = _require_mapping(color, "semantic")
    typography = _require_mapping(semantics, "typography")
    render = _require_mapping(semantics, "render")
    session = _require_mapping(semantics, "session")
    terminal_ansi = _require_mapping(color, "terminal_ansi")

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
        terminal_primary=str(typography.get("terminal_primary", "")),
        terminal_fallbacks=[str(value) for value in typography.get("terminal_fallbacks", [])],
        ui_mono=str(typography.get("ui_mono", "")),
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

    if _has_non_default_display_policy(context.render_display):
        warnings.append("Render display-transform policy is ignored by terminal/TUI targets in TWO-09.")

    if supported_target_classes and not set(context.requested_target_classes).intersection(supported_target_classes):
        warnings.append(
            "This target was compiled explicitly in dev mode even though the profile's requested target classes do not include this target family directly."
        )

    return warnings


def write_target_artifact(
    *,
    target_name: str,
    output_dir: Path,
    file_name: str,
    content: str,
) -> TargetArtifact:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / file_name
    output_path.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    relative_path = f"{target_name}/{file_name}"
    return TargetArtifact(
        target_name=target_name,
        file_name=file_name,
        relative_path=relative_path,
        output_path=str(output_path),
        content_sha256=digest,
        byte_count=len(content.encode("utf-8")),
    )


def _require_mapping(container: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = container.get(key)
    if not isinstance(value, Mapping):
        raise KeyError(f"Resolved profile is missing required mapping `{key}`.")
    return value


def _has_non_default_display_policy(display: Mapping[str, Any]) -> bool:
    return any(
        (
            display.get("gamma", 1.0) != 1.0,
            display.get("contrast", 1.0) != 1.0,
            display.get("temperature", 6500) != 6500,
            display.get("black_lift", 0.0) != 0.0,
            display.get("blue_light_reduction", 0.0) != 0.0,
            display.get("tint_bias") is not None,
        )
    )
