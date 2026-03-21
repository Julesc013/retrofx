"""Compiler registry for toolkit-adjacent export targets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.toolkit.desktop_style import DesktopStyleCompiler
from v2.targets.toolkit.fontconfig import FontconfigCompiler
from v2.targets.toolkit.gtk import GtkExportCompiler
from v2.targets.toolkit.icon_cursor import IconCursorCompiler
from v2.targets.toolkit.qt import QtExportCompiler

TOOLKIT_COMPILERS = {
    "desktop-style": DesktopStyleCompiler(),
    "fontconfig": FontconfigCompiler(),
    "gtk-export": GtkExportCompiler(),
    "icon-cursor": IconCursorCompiler(),
    "qt-export": QtExportCompiler(),
}


def list_toolkit_targets() -> list[str]:
    return sorted(TOOLKIT_COMPILERS)


def compile_resolved_profile_targets(
    resolved_profile: Mapping[str, Any],
    out_root: str | Path,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    base_output_root = Path(out_root)
    profile_output_root = base_output_root / profile_id

    selected_targets = list_toolkit_targets() if not target_names else [name.strip().lower() for name in target_names]
    unknown_targets = [name for name in selected_targets if name not in TOOLKIT_COMPILERS]
    if unknown_targets:
        raise ValueError(f"Unknown toolkit targets requested: {', '.join(sorted(unknown_targets))}")

    results: list[TargetCompileResult] = []
    for target_name in selected_targets:
        compiler = TOOLKIT_COMPILERS[target_name]
        results.append(compiler.compile(resolved_profile, profile_output_root))

    return {
        "profile_id": profile_id,
        "profile_output_root": str(profile_output_root),
        "selected_targets": selected_targets,
        "compiled_targets": [result.to_dict() for result in results],
    }
