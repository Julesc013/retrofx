"""Top-level target registry for the early 2.x implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.terminal import TERMINAL_COMPILERS, list_terminal_targets
from v2.targets.wm import WM_COMPILERS, list_wm_targets

TARGET_COMPILERS = {
    **TERMINAL_COMPILERS,
    **WM_COMPILERS,
}

if len(TARGET_COMPILERS) != len(TERMINAL_COMPILERS) + len(WM_COMPILERS):
    raise RuntimeError("Duplicate target names were registered across target families.")


def list_targets() -> list[str]:
    return sorted(TARGET_COMPILERS)


def list_target_families() -> dict[str, list[str]]:
    return {
        "terminal-tui": list_terminal_targets(),
        "wm": list_wm_targets(),
    }


def compile_resolved_profile_targets(
    resolved_profile: Mapping[str, Any],
    out_root: str | Path,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    base_output_root = Path(out_root)
    profile_output_root = base_output_root / profile_id

    if target_names:
        selected_targets = []
        for target_name in target_names:
            normalized = target_name.strip().lower()
            if normalized and normalized not in selected_targets:
                selected_targets.append(normalized)
    else:
        selected_targets = list_targets()

    unknown_targets = [name for name in selected_targets if name not in TARGET_COMPILERS]
    if unknown_targets:
        raise ValueError(f"Unknown 2.x targets requested: {', '.join(sorted(unknown_targets))}")

    results: list[TargetCompileResult] = []
    for target_name in selected_targets:
        compiler = TARGET_COMPILERS[target_name]
        results.append(compiler.compile(resolved_profile, profile_output_root))

    return {
        "profile_id": profile_id,
        "profile_output_root": str(profile_output_root),
        "selected_targets": selected_targets,
        "compiled_targets": [result.to_dict() for result in results],
    }
