"""Kitty compiler for the early 2.x terminal family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.common import build_terminal_theme_context, render_warning_for_terminal_family, write_target_artifact


class KittyCompiler:
    target_name = "kitty"
    family_name = "terminal-tui"
    output_file_name = "kitty.conf"
    supported_target_classes = ("terminal", "tui")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_terminal_theme_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = render_warning_for_terminal_family(context, self.supported_target_classes)
        if context.terminal_fallbacks:
            warnings.append("Kitty output uses only `font_family`; fallback chains remain a future enhancement in TWO-12.")

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
                "semantics.typography.terminal_primary",
                "semantics.typography.aa",
            ],
            ignored_sections=[
                "semantics.render",
                "semantics.chrome",
                "semantics.session",
                "semantics.typography.terminal_fallbacks",
                "semantics.typography.console_font",
                "semantics.typography.emoji_policy",
            ],
            warnings=warnings,
            notes=[
                "Deterministic Kitty theme artifact from the resolved profile.",
                "Typography emission is currently limited to `font_family` because this dev-only target keeps the configuration narrow and portable.",
            ],
        )

    def _render(self, context: Any) -> str:
        lines = [
            "# RetroFX 2.x experimental terminal target: kitty",
            f"# profile.id: {context.profile_id}",
            f"foreground {context.foreground}",
            f"background {context.background}",
            f"cursor {context.cursor}",
            f"cursor_text_color {context.cursor_text}",
            f"selection_background {context.selection_bg}",
            f"selection_foreground {context.selection_fg}",
        ]
        if context.terminal_primary:
            lines.append(f"font_family {context.terminal_primary}")
        if context.ui_mono and context.ui_mono != context.terminal_primary:
            lines.append(f"# resolved ui_mono {context.ui_mono}")
        for slot in range(16):
            lines.append(f"color{slot} {context.terminal_ansi[str(slot)]}")
        lines.append("")
        return "\n".join(lines)
