"""Vim colorscheme compiler for the early 2.x terminal family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.common import build_terminal_theme_context, render_warning_for_terminal_family, write_target_artifact


class VimCompiler:
    target_name = "vim"
    family_name = "terminal-tui"
    output_file_name = "retrofx.vim"
    supported_target_classes = ("terminal", "tui")

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
            notes=["Vim output is emitted as a colorscheme snippet only; install/apply remains future work."],
        )

    def _render(self, context: Any) -> str:
        lines = [
            '" RetroFX 2.x experimental terminal target: vim',
            f'" profile.id: {context.profile_id}',
            "hi clear",
            'if exists("syntax_on")',
            "  syntax reset",
            "endif",
            "set background=dark",
            f'let g:colors_name = "retrofx_{context.profile_id.replace("-", "_")}"',
            "",
        ]
        for slot in range(16):
            lines.append(f'let g:terminal_color_{slot} = "{context.terminal_ansi[str(slot)]}"')
        lines.extend(
            [
                "",
                f"hi Normal guifg={context.foreground} guibg={context.background}",
                f"hi Visual guifg={context.selection_fg} guibg={context.selection_bg}",
                f"hi Cursor guifg={context.cursor_text} guibg={context.cursor}",
                f"hi StatusLine guifg={context.foreground} guibg={context.semantic['bg1']}",
                f"hi LineNr guifg={context.semantic['fg2']} guibg={context.background}",
                "",
            ]
        )
        return "\n".join(lines)
