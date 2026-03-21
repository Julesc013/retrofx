"""Xresources compiler for the early 2.x terminal family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.common import build_terminal_theme_context, render_warning_for_terminal_family, write_target_artifact


class XresourcesCompiler:
    target_name = "xresources"
    family_name = "terminal-tui"
    output_file_name = "Xresources"
    supported_target_classes = ("terminal", "tui", "x11")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_terminal_theme_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
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
                "semantics.color.terminal_ansi",
            ],
            ignored_sections=[
                "semantics.render",
                "semantics.chrome",
                "semantics.session",
                "semantics.typography.terminal_fallbacks",
            ],
            warnings=render_warning_for_terminal_family(context, self.supported_target_classes),
            notes=["Deterministic Xresources export from the resolved terminal palette."],
        )

    def _render(self, context: Any) -> str:
        lines = [
            "! RetroFX 2.x experimental terminal target: xresources",
            f"! profile.id: {context.profile_id}",
            f"! profile.name: {context.profile_name}",
            "",
            f"*foreground: {context.foreground}",
            f"*background: {context.background}",
            f"*cursorColor: {context.cursor}",
            f"*cursorTextColor: {context.cursor_text}",
            f"*highlightColor: {context.selection_bg}",
            f"*highlightTextColor: {context.selection_fg}",
            "",
        ]
        for slot in range(16):
            lines.append(f"*color{slot}: {context.terminal_ansi[str(slot)]}")
        lines.append("")
        return "\n".join(lines)
