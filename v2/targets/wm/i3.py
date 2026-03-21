"""i3 WM fragment compiler for the early 2.x WM family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.wm.common import (
    build_wm_theme_context,
    focused_workspace_text,
    inactive_workspace_text,
    render_warning_for_wm_family,
    write_target_artifact,
)


class I3Compiler:
    target_name = "i3"
    family_name = "wm"
    output_file_name = "retrofx-theme.conf"
    supported_target_classes = ("wm", "x11")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_wm_theme_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = render_warning_for_wm_family(context, self.supported_target_classes)
        warnings.extend(_wm_fragment_warnings(context, "i3"))
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
                "semantics.session",
            ],
            ignored_sections=[
                "semantics.color.terminal_ansi",
                "semantics.color.tty_ansi",
                "semantics.render",
            ],
            warnings=warnings,
            notes=[
                "Deterministic i3 theme fragment from the resolved WM theme context.",
                "This file is intended to be included from a user-owned i3 config; TWO-10 does not reload or apply it.",
            ],
        )

    def _render(self, context: Any) -> str:
        bar_mode = "hide" if context.bar_style == "hidden" else "dock"
        lines = [
            "# RetroFX 2.x experimental WM target: i3",
            "# Include this fragment from an i3 config that you own.",
            f"# profile.id = {context.profile_id}",
            f"# profile.name = {context.profile_name}",
            "",
            f"set $retrofx_bg0 {context.background}",
            f"set $retrofx_bg1 {context.background_alt}",
            f"set $retrofx_bg2 {context.background_inactive}",
            f"set $retrofx_fg0 {context.foreground}",
            f"set $retrofx_fg1 {context.foreground_alt}",
            f"set $retrofx_fg2 {context.foreground_muted}",
            f"set $retrofx_accent_primary {context.accent_primary}",
            f"set $retrofx_accent_warn {context.accent_warn}",
            f"set $retrofx_accent_error {context.accent_error}",
            f"set $retrofx_border_active {context.border_active}",
            f"set $retrofx_border_inactive {context.border_inactive}",
            f"set $retrofx_border_urgent {context.border_urgent}",
            f"set $retrofx_status_bg {context.status_bg}",
            f"set $retrofx_status_fg {context.status_fg}",
            f"set $retrofx_menu_bg {context.menu_bg}",
            f"set $retrofx_menu_fg {context.menu_fg}",
            "",
        ]

        if context.ui_font:
            lines.append(f"font pango:{context.ui_font} 10")
        if context.gaps > 0:
            lines.extend(
                [
                    f"gaps inner {context.gaps}",
                    "gaps outer 0",
                ]
            )

        lines.extend(
            [
                "",
                "client.background $retrofx_bg0",
                "client.focused          $retrofx_border_active $retrofx_bg0 $retrofx_fg0 $retrofx_accent_primary $retrofx_border_active",
                "client.focused_inactive $retrofx_border_inactive $retrofx_bg1 $retrofx_fg1 $retrofx_bg2 $retrofx_border_inactive",
                "client.unfocused        $retrofx_border_inactive $retrofx_bg1 $retrofx_fg2 $retrofx_bg2 $retrofx_border_inactive",
                "client.urgent           $retrofx_border_urgent $retrofx_accent_error $retrofx_menu_fg $retrofx_accent_warn $retrofx_border_urgent",
                "client.placeholder      $retrofx_border_inactive $retrofx_bg1 $retrofx_fg2 $retrofx_bg2 $retrofx_border_inactive",
                "",
                "bar {",
                f"    mode {bar_mode}",
                "    colors {",
                "        background         $retrofx_status_bg",
                "        statusline         $retrofx_status_fg",
                "        separator          $retrofx_border_inactive",
                f"        focused_workspace  $retrofx_border_active $retrofx_accent_primary {focused_workspace_text(context)}",
                f"        active_workspace   $retrofx_border_inactive $retrofx_menu_bg $retrofx_menu_fg",
                f"        inactive_workspace $retrofx_border_inactive $retrofx_bg1 {inactive_workspace_text(context)}",
                "        urgent_workspace   $retrofx_border_urgent $retrofx_accent_error $retrofx_menu_fg",
                "        binding_mode       $retrofx_border_active $retrofx_accent_warn $retrofx_menu_fg",
                "    }",
                "}",
                "",
            ]
        )
        return "\n".join(lines)


def _wm_fragment_warnings(context: Any, target_name: str) -> list[str]:
    warnings: list[str] = []
    if context.icon_theme:
        warnings.append(f"{target_name} fragments do not emit icon-theme hints in TWO-10.")
    if context.cursor_theme:
        warnings.append(f"{target_name} fragments do not emit cursor-theme hints in TWO-10.")
    if context.launcher_style != "minimal":
        warnings.append(f"{target_name} fragments do not represent launcher styling hints in TWO-10.")
    if context.notification_style != "minimal":
        warnings.append(f"{target_name} fragments do not represent notification styling hints in TWO-10.")
    return warnings
