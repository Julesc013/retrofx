"""Compiler registry and orchestrator for the early 2.x WM target family."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.wm.i3 import I3Compiler
from v2.targets.wm.sway import SwayCompiler
from v2.targets.wm.waybar import WaybarCompiler

WM_COMPILERS = {
    "i3": I3Compiler(),
    "sway": SwayCompiler(),
    "waybar": WaybarCompiler(),
}


def list_wm_targets() -> list[str]:
    return sorted(WM_COMPILERS)


def compile_resolved_profile_targets(
    resolved_profile: Mapping[str, Any],
    out_root: str | Path,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    base_output_root = Path(out_root)
    profile_output_root = base_output_root / profile_id

    selected_targets = list_wm_targets() if not target_names else [name.strip().lower() for name in target_names]
    unknown_targets = [name for name in selected_targets if name not in WM_COMPILERS]
    if unknown_targets:
        raise ValueError(f"Unknown WM targets requested: {', '.join(sorted(unknown_targets))}")

    results: list[TargetCompileResult] = []
    for target_name in selected_targets:
        compiler = WM_COMPILERS[target_name]
        results.append(compiler.compile(resolved_profile, profile_output_root))

    return {
        "profile_id": profile_id,
        "profile_output_root": str(profile_output_root),
        "selected_targets": selected_targets,
        "compiled_targets": [result.to_dict() for result in results],
    }
