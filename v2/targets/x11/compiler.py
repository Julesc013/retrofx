"""Compiler registry for the early 2.x X11 and render-adjacent targets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.targets.interfaces import TargetCompileResult
from v2.targets.x11.display_policy import X11DisplayPolicyCompiler

X11_COMPILERS = {
    "x11-display-policy": X11DisplayPolicyCompiler(),
}


def list_x11_targets() -> list[str]:
    return sorted(X11_COMPILERS)


def compile_resolved_profile_targets(
    resolved_profile: Mapping[str, Any],
    out_root: str | Path,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    profile_id = str(resolved_profile["identity"]["id"])
    base_output_root = Path(out_root)
    profile_output_root = base_output_root / profile_id

    selected_targets = list_x11_targets() if not target_names else [name.strip().lower() for name in target_names]
    unknown_targets = [name for name in selected_targets if name not in X11_COMPILERS]
    if unknown_targets:
        raise ValueError(f"Unknown X11 targets requested: {', '.join(sorted(unknown_targets))}")

    results: list[TargetCompileResult] = []
    for target_name in selected_targets:
        compiler = X11_COMPILERS[target_name]
        results.append(compiler.compile(resolved_profile, profile_output_root))

    return {
        "profile_id": profile_id,
        "profile_output_root": str(profile_output_root),
        "selected_targets": selected_targets,
        "compiled_targets": [result.to_dict() for result in results],
    }
