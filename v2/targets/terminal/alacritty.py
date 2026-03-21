"""Alacritty compiler for the early 2.x terminal family."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.common import build_terminal_theme_context, render_warning_for_terminal_family, write_target_artifact


class AlacrittyCompiler:
    target_name = "alacritty"
    family_name = "terminal-tui"
    output_file_name = "alacritty.toml"
    supported_target_classes = ("terminal", "tui")

    def compile(self, resolved_profile: Mapping[str, Any], profile_output_root: Path) -> TargetCompileResult:
        context = build_terminal_theme_context(resolved_profile)
        output_dir = profile_output_root / self.target_name
        warnings = render_warning_for_terminal_family(context, self.supported_target_classes)
        if context.terminal_fallbacks:
            warnings.append("Alacritty output can express only the primary terminal font family; fallback chains are omitted.")

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
            ],
            ignored_sections=[
                "semantics.render",
                "semantics.chrome",
                "semantics.session",
                "semantics.typography.terminal_fallbacks",
            ],
            warnings=warnings,
            notes=["Deterministic Alacritty theme artifact from the resolved profile."],
        )

    def _render(self, context: Any) -> str:
        def q(value: str) -> str:
            return json.dumps(value)

        lines = [
            "# RetroFX 2.x experimental terminal target: alacritty",
            f"# profile.id = {context.profile_id}",
            "",
            "[colors.primary]",
            f"background = {q(context.background)}",
            f"foreground = {q(context.foreground)}",
            "",
            "[colors.cursor]",
            f"cursor = {q(context.cursor)}",
            f"text = {q(context.cursor_text)}",
            "",
            "[colors.selection]",
            f"background = {q(context.selection_bg)}",
            f"text = {q(context.selection_fg)}",
            "",
            "[colors.normal]",
            f"black = {q(context.terminal_ansi['0'])}",
            f"red = {q(context.terminal_ansi['1'])}",
            f"green = {q(context.terminal_ansi['2'])}",
            f"yellow = {q(context.terminal_ansi['3'])}",
            f"blue = {q(context.terminal_ansi['4'])}",
            f"magenta = {q(context.terminal_ansi['5'])}",
            f"cyan = {q(context.terminal_ansi['6'])}",
            f"white = {q(context.terminal_ansi['7'])}",
            "",
            "[colors.bright]",
            f"black = {q(context.terminal_ansi['8'])}",
            f"red = {q(context.terminal_ansi['9'])}",
            f"green = {q(context.terminal_ansi['10'])}",
            f"yellow = {q(context.terminal_ansi['11'])}",
            f"blue = {q(context.terminal_ansi['12'])}",
            f"magenta = {q(context.terminal_ansi['13'])}",
            f"cyan = {q(context.terminal_ansi['14'])}",
            f"white = {q(context.terminal_ansi['15'])}",
        ]

        if context.terminal_primary:
            lines.extend(
                [
                    "",
                    "[font.normal]",
                    f"family = {q(context.terminal_primary)}",
                ]
            )

        lines.append("")
        return "\n".join(lines)
