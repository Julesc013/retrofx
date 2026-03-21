"""Dev-only target compilation entrypoint for the early 2.x scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from v2.core.pipeline import run_profile_pipeline
from v2.targets.terminal import compile_resolved_profile_targets, list_terminal_targets

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT_ROOT = REPO_ROOT / "v2" / "out"
IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-09",
    "family": "terminal-tui",
    "implemented_targets": list_terminal_targets(),
    "mode": "export-only-dev",
    "not_implemented": [
        "capability-filtered target planning",
        "artifact planning",
        "session orchestration",
        "apply/install/off behavior",
        "non-terminal target families",
    ],
}


def compile_profile_to_output(
    profile_path: str | Path,
    *,
    out_root: str | Path | None = None,
    target_names: list[str] | None = None,
) -> dict[str, Any]:
    pipeline_result = run_profile_pipeline(profile_path)
    chosen_out_root = Path(out_root) if out_root is not None else DEFAULT_OUT_ROOT

    if not pipeline_result.ok:
        return {
            "ok": False,
            "stage": pipeline_result.stage,
            "implementation": IMPLEMENTATION_INFO,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [error.to_dict() for error in pipeline_result.errors],
            "profile_output_root": None,
            "compiled_targets": [],
        }

    resolved_profile = pipeline_result.resolved_profile
    assert resolved_profile is not None
    compiled = compile_resolved_profile_targets(resolved_profile, chosen_out_root, target_names)
    return {
        "ok": True,
        "stage": "compile",
        "implementation": IMPLEMENTATION_INFO,
        "source": pipeline_result.source,
        "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
        "errors": [],
        "profile_id": resolved_profile["identity"]["id"],
        "profile_output_root": compiled["profile_output_root"],
        "selected_targets": compiled["selected_targets"],
        "compiled_targets": compiled["compiled_targets"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile experimental RetroFX 2.x terminal/TUI target artifacts from a 2.x profile.",
    )
    parser.add_argument("profile", help="Path to a RetroFX 2.x TOML profile.")
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Compile only the selected target. Repeat for multiple targets.",
    )
    parser.add_argument(
        "--out-root",
        default=str(DEFAULT_OUT_ROOT),
        help=f"Base output root. Defaults to {DEFAULT_OUT_ROOT}.",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print the implemented terminal/TUI targets and exit.",
    )
    args = parser.parse_args(argv)

    if args.list_targets:
        print(json.dumps({"targets": list_terminal_targets()}, indent=2))
        return 0

    try:
        payload = compile_profile_to_output(args.profile, out_root=args.out_root, target_names=args.targets)
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "compile",
                    "implementation": IMPLEMENTATION_INFO,
                    "errors": [{"severity": "error", "code": "unknown-target", "message": str(exc)}],
                },
                indent=2,
            )
        )
        return 2

    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
