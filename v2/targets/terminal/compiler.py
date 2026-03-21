"""Compiler registry and orchestrator for the first 2.x terminal/TUI targets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal.alacritty import AlacrittyCompiler
from v2.targets.terminal.kitty import KittyCompiler
from v2.targets.terminal.tmux import TmuxCompiler
from v2.targets.terminal.vim import VimCompiler
from v2.targets.terminal.xresources import XresourcesCompiler

TERMINAL_COMPILERS = {
    "alacritty": AlacrittyCompiler(),
    "kitty": KittyCompiler(),
    "tmux": TmuxCompiler(),
    "vim": VimCompiler(),
    "xresources": XresourcesCompiler(),
}


def list_terminal_targets() -> list[str]:
    return sorted(TERMINAL_COMPILERS)


def compile_resolved_profile_targets(
    resolved_profile: Mapping[str, Any],
    out_root: str | Path,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    base_output_root = Path(out_root)
    profile_output_root = base_output_root / profile_id

    selected_targets = list_terminal_targets() if not target_names else [name.strip().lower() for name in target_names]
    unknown_targets = [name for name in selected_targets if name not in TERMINAL_COMPILERS]
    if unknown_targets:
        raise ValueError(f"Unknown terminal/TUI targets requested: {', '.join(sorted(unknown_targets))}")

    results: list[TargetCompileResult] = []
    for target_name in selected_targets:
        compiler = TERMINAL_COMPILERS[target_name]
        results.append(compiler.compile(resolved_profile, profile_output_root))

    return {
        "profile_id": profile_id,
        "profile_output_root": str(profile_output_root),
        "selected_targets": selected_targets,
        "compiled_targets": [result.to_dict() for result in results],
    }
