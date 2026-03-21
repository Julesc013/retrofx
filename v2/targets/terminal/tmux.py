"""tmux compiler for the early 2.x terminal family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.common import build_terminal_theme_context, render_warning_for_terminal_family, write_target_artifact


class TmuxCompiler:
    target_name = "tmux"
    family_name = "terminal-tui"
    output_file_name = "tmux.conf"
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
                "semantics.chrome.icon_theme",
                "semantics.chrome.cursor_theme",
                "semantics.session",
                "semantics.typography",
            ],
            warnings=render_warning_for_terminal_family(context, self.supported_target_classes),
            notes=["tmux output is emitted as a theme snippet only; no reload or session integration exists in TWO-09."],
        )

    def _render(self, context: Any) -> str:
        lines = [
            "# RetroFX 2.x experimental terminal target: tmux",
            f"# profile.id: {context.profile_id}",
            f'set -g status-style "fg={context.foreground},bg={context.semantic["bg1"]}"',
            f'set -g message-style "fg={context.foreground},bg={context.semantic["bg1"]}"',
            f'set -g pane-border-style "fg={context.semantic["border_inactive"]}"',
            f'set -g pane-active-border-style "fg={context.semantic["border_active"]}"',
            f'set -g mode-style "fg={context.selection_fg},bg={context.selection_bg}"',
            f'set -g display-style "fg={context.foreground},bg={context.background}"',
            f'set -g status-left-style "fg={context.terminal_ansi["15"]},bg={context.terminal_ansi["4"]}"',
            f'set -g status-right-style "fg={context.terminal_ansi["15"]},bg={context.terminal_ansi["5"]}"',
            "",
        ]
        return "\n".join(lines)
