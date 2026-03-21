"""waybar-style theme compiler for the early 2.x WM family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.wm.common import build_wm_theme_context, render_warning_for_wm_family, write_target_artifact

BAR_STYLE_METRICS = {
    "minimal": {"window_margin": 0, "module_margin": 0, "radius": 0, "padding_x": 8, "padding_y": 0, "border_width": 2},
    "boxed": {"window_margin": 6, "module_margin": 4, "radius": 8, "padding_x": 10, "padding_y": 2, "border_width": 1},
    "dense": {"window_margin": 0, "module_margin": 0, "radius": 0, "padding_x": 4, "padding_y": 0, "border_width": 1},
    "hidden": {"window_margin": 0, "module_margin": 0, "radius": 0, "padding_x": 4, "padding_y": 0, "border_width": 1},
}


class WaybarCompiler:
    target_name = "waybar"
    family_name = "wm"
    output_file_name = "style.css"
    supported_target_classes = ("wm", "wayland")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_wm_theme_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = render_warning_for_wm_family(context, self.supported_target_classes)
        warnings.extend(_waybar_warnings(context))
        artifact = write_target_artifact(
            target_name=self.target_name,
            output_dir=output_dir,
            file_name=self.output_file_name,
            content=self._render(context),
        )
        return TargetCompileResult(
            target_name=self.target_name,
            family_name=self.family_name,
            mode="export-only-dev",
            output_dir=str(output_dir),
            artifacts=[artifact],
            consumed_sections=[
                "identity",
                "semantics.color.semantic",
                "semantics.chrome",
                "semantics.typography",
            ],
            ignored_sections=[
                "semantics.color.terminal_ansi",
                "semantics.color.tty_ansi",
                "semantics.render",
                "semantics.session",
            ],
            warnings=warnings,
            notes=[
                "Deterministic waybar-style CSS theme artifact from the resolved WM theme context.",
                "This file is styling-only and does not manage waybar process lifecycle or configuration ownership.",
            ],
        )

    def _render(self, context: Any) -> str:
        metrics = BAR_STYLE_METRICS.get(context.bar_style, BAR_STYLE_METRICS["minimal"])
        font_declaration = ""
        if context.ui_font or context.ui_mono:
            fonts = [font for font in (context.ui_font, context.ui_mono) if font]
            quoted = ", ".join(f'"{font}"' for font in fonts)
            font_declaration = f"  font-family: {quoted};\n"

        lines = [
            "/* RetroFX 2.x experimental WM target: waybar */",
            "/* Style fragment only. Include from a waybar config you own. */",
            f"/* profile.id = {context.profile_id} */",
            "",
            f"@define-color retrofx-bg0 {context.background};",
            f"@define-color retrofx-bg1 {context.background_alt};",
            f"@define-color retrofx-bg2 {context.background_inactive};",
            f"@define-color retrofx-fg0 {context.foreground};",
            f"@define-color retrofx-fg1 {context.foreground_alt};",
            f"@define-color retrofx-fg2 {context.foreground_muted};",
            f"@define-color retrofx-accent-primary {context.accent_primary};",
            f"@define-color retrofx-accent-warn {context.accent_warn};",
            f"@define-color retrofx-accent-error {context.accent_error};",
            f"@define-color retrofx-border-active {context.border_active};",
            f"@define-color retrofx-border-inactive {context.border_inactive};",
            f"@define-color retrofx-border-urgent {context.border_urgent};",
            f"@define-color retrofx-status-bg {context.status_bg};",
            f"@define-color retrofx-status-fg {context.status_fg};",
            f"@define-color retrofx-menu-bg {context.menu_bg};",
            f"@define-color retrofx-menu-fg {context.menu_fg};",
            f"@define-color retrofx-shadow-tint {context.shadow_tint};",
            f"@define-color retrofx-inactive-dim {context.inactive_dim};",
            "",
            "* {",
        ]
        if font_declaration:
            lines.append(font_declaration.rstrip("\n"))
        lines.extend(
            [
                "}",
                "",
                "window#waybar {",
                "  background: @retrofx-status-bg;",
                "  color: @retrofx-status-fg;",
                f"  border-bottom: {metrics['border_width']}px solid @retrofx-border-active;",
                f"  margin: {metrics['window_margin']}px {context.gaps}px 0 {context.gaps}px;",
                "}",
                "",
                "#workspaces button {",
                "  background: transparent;",
                "  color: @retrofx-fg1;",
                f"  border-radius: {metrics['radius']}px;",
                f"  padding: {metrics['padding_y']}px {metrics['padding_x']}px;",
                f"  margin: 0 {metrics['module_margin']}px;",
                "}",
                "",
                "#workspaces button.focused {",
                "  background: @retrofx-accent-primary;",
                "  color: @retrofx-menu-fg;",
                "  border-bottom: 2px solid @retrofx-border-active;",
                "}",
                "",
                "#workspaces button.urgent {",
                "  background: @retrofx-accent-error;",
                "  color: @retrofx-menu-fg;",
                "  border-bottom: 2px solid @retrofx-border-urgent;",
                "}",
                "",
                "#clock,",
                "#battery,",
                "#cpu,",
                "#memory,",
                "#network,",
                "#pulseaudio,",
                "#tray,",
                "#window {",
                "  color: @retrofx-status-fg;",
                f"  padding: {metrics['padding_y']}px {metrics['padding_x']}px;",
                f"  margin: 0 {metrics['module_margin']}px;",
                f"  border-radius: {metrics['radius']}px;",
                "}",
                "",
                "tooltip {",
                "  background: @retrofx-menu-bg;",
                "  color: @retrofx-menu-fg;",
                "  border: 1px solid @retrofx-border-active;",
                "}",
                "",
            ]
        )
        return "\n".join(lines)


def _waybar_warnings(context: Any) -> list[str]:
    warnings: list[str] = []
    if context.bar_style == "hidden":
        warnings.append("waybar CSS cannot truthfully express hidden-bar lifecycle behavior; TWO-10 emits visible styling only.")
    if context.icon_theme:
        warnings.append("waybar CSS does not emit icon-theme hints in TWO-10.")
    if context.cursor_theme:
        warnings.append("waybar CSS does not emit cursor-theme hints in TWO-10.")
    if context.launcher_style != "minimal":
        warnings.append("waybar CSS does not represent launcher styling hints in TWO-10.")
    if context.notification_style != "minimal":
        warnings.append("waybar CSS does not represent notification styling hints in TWO-10.")
    return warnings
