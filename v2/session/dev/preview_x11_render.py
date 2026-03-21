"""Explicit dev-only X11 render preview for the first 2.x render slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable, Mapping

from v2.core.dev.compile_targets import DEFAULT_OUT_ROOT, compile_profile_to_output
from v2.core.dev.profile_input import add_profile_selection_args
from v2.core.dev.plan_session import plan_profile_session

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_X11_TARGETS = ["x11-shader", "x11-picom", "x11-render-runtime", "x11-display-policy"]
IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-17",
    "surface": "x11-render-preview",
    "mode": "non-destructive-preview",
    "targets": DEFAULT_X11_TARGETS,
}


def preview_x11_render_profile(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    out_root: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
    probe_picom: bool = False,
    probe_seconds: float = 3.0,
    command_runner: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    compile_payload = compile_profile_to_output(
        profile_path,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
        out_root=out_root,
        target_names=DEFAULT_X11_TARGETS,
        env=env,
        cwd=cwd,
        stdin_isatty=stdin_isatty,
        path_lookup=path_lookup,
    )
    chosen_out_root = Path(out_root) if out_root is not None else DEFAULT_OUT_ROOT

    if not compile_payload["ok"]:
        return {
            "ok": False,
            "stage": compile_payload["stage"],
            "implementation": IMPLEMENTATION_INFO,
            "errors": compile_payload["errors"],
            "warnings": compile_payload["warnings"],
            "compile": compile_payload,
            "preview": None,
        }

    plan_payload = plan_profile_session(
        profile_path,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
        env=env,
        cwd=cwd,
        stdin_isatty=stdin_isatty,
        path_lookup=path_lookup,
        out_root=chosen_out_root,
        write_preview=True,
    )
    environment = compile_payload["environment"]
    x11_render = compile_payload["x11_render"]
    preview_state = _build_preview_state(compile_payload, plan_payload)

    probe_result = {
        "attempted": False,
        "eligible": bool(x11_render["live_preview_possible"]),
        "status": "not-requested",
        "command": None,
        "timed_out": False,
        "returncode": None,
        "stderr_tail": "",
        "stdout_tail": "",
    }
    ok = True
    errors: list[dict[str, Any]] = []

    if probe_picom:
        probe_result["attempted"] = True
        live_check = _validate_live_probe_prereqs(environment, path_lookup or shutil.which)
        if live_check is not None:
            ok = False
            probe_result["status"] = "unavailable"
            errors.append(live_check)
        else:
            picom_config = Path(compile_payload["profile_output_root"]) / "x11-picom" / "picom.conf"
            probe_result = _run_picom_probe(
                picom_config=picom_config,
                env=env,
                cwd=cwd,
                probe_seconds=probe_seconds,
                command_runner=command_runner or subprocess.run,
                executable_path=(path_lookup or shutil.which)("picom") or "picom",
            )
            ok = probe_result["status"] in {"ok", "timed-out"}
            if not ok:
                errors.append(
                    {
                        "severity": "error",
                        "code": "picom-probe-failed",
                        "message": "The explicit X11 live probe did not complete successfully.",
                    }
                )

    preview_root = Path(compile_payload["profile_output_root"]) / "x11-render-runtime"
    preview_root.mkdir(parents=True, exist_ok=True)
    preview_state["probe"] = probe_result
    preview_state_path = preview_root / "preview-state.json"
    preview_state_path.write_text(json.dumps(preview_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "ok": ok,
        "stage": "x11-render-preview",
        "implementation": IMPLEMENTATION_INFO,
        "errors": errors,
        "warnings": compile_payload["warnings"],
        "compile": compile_payload,
        "plan": plan_payload["plan"] if plan_payload["ok"] else None,
        "preview": {
            "output_dir": str(preview_root),
            "preview_state_path": str(preview_state_path),
            "probe": probe_result,
        },
        "note": "This surface is dev-only. It stages X11 artifacts and can perform a bounded explicit picom probe, but it does not replace the 1.x runtime.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 preview-x11",
        description="Stage the experimental RetroFX 2.x X11 render artifacts and optionally run a bounded picom probe.",
    )
    add_profile_selection_args(parser)
    parser.add_argument(
        "--out-root",
        default=str(DEFAULT_OUT_ROOT),
        help=f"Base output root. Defaults to {DEFAULT_OUT_ROOT}.",
    )
    parser.add_argument(
        "--probe-picom",
        action="store_true",
        help="Attempt an explicit bounded picom probe with the generated config when the current environment is X11 and picom is available.",
    )
    parser.add_argument(
        "--probe-seconds",
        type=float,
        default=3.0,
        help="Timeout for the explicit picom probe. Defaults to 3.0 seconds.",
    )
    args = parser.parse_args(argv)

    payload = preview_x11_render_profile(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        out_root=args.out_root,
        probe_picom=args.probe_picom,
        probe_seconds=args.probe_seconds,
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _build_preview_state(compile_payload: Mapping[str, Any], plan_payload: Mapping[str, Any]) -> dict[str, Any]:
    compiled_targets = [entry["target_name"] for entry in compile_payload["compiled_targets"]]
    return {
        "schema": "retrofx.x11-preview-state/v2alpha1",
        "profile": {
            "id": compile_payload["profile_id"],
            "origin": compile_payload["profile_origin"],
            "pack": compile_payload.get("pack"),
        },
        "environment": {
            "session_type": compile_payload["environment"]["session_type"],
            "wm_or_de": compile_payload["environment"]["wm_or_de"],
            "picom_available": compile_payload["environment"]["executables"].get("picom", False),
        },
        "render": {
            "requested_mode": compile_payload["x11_render"]["requested_mode"],
            "implemented_mode": compile_payload["x11_render"]["implemented_mode"],
            "overall_status": compile_payload["x11_render"]["overall_status"],
            "compositor_required": compile_payload["x11_render"]["compositor_required"],
        },
        "compiled_targets": compiled_targets,
        "plan_summary": {
            "compile_targets": plan_payload["plan"]["compile_targets"] if plan_payload["ok"] else [],
            "apply_preview_targets": plan_payload["plan"]["apply_preview_targets"] if plan_payload["ok"] else [],
        },
    }


def _validate_live_probe_prereqs(environment: Mapping[str, Any], path_lookup: Callable[[str], str | None]) -> dict[str, Any] | None:
    if str(environment["session_type"]) != "x11":
        return {
            "severity": "error",
            "code": "not-x11-session",
            "message": "The explicit picom probe requires an X11 session.",
        }
    if not path_lookup("picom"):
        return {
            "severity": "error",
            "code": "picom-not-found",
            "message": "The explicit picom probe requires `picom` in PATH.",
        }
    return None


def _run_picom_probe(
    *,
    picom_config: Path,
    env: Mapping[str, str] | None,
    cwd: str | Path | None,
    probe_seconds: float,
    command_runner: Callable[..., Any],
    executable_path: str,
) -> dict[str, Any]:
    command = [executable_path, "--config", str(picom_config)]
    working_directory = str(picom_config.parent)
    try:
        result = command_runner(
            command,
            cwd=working_directory,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=probe_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "attempted": True,
            "eligible": True,
            "status": "timed-out",
            "command": command,
            "timed_out": True,
            "returncode": None,
            "stderr_tail": (exc.stderr or "")[-400:],
            "stdout_tail": (exc.stdout or "")[-400:],
        }

    status = "ok" if result.returncode == 0 else "failed"
    return {
        "attempted": True,
        "eligible": True,
        "status": status,
        "command": command,
        "timed_out": False,
        "returncode": result.returncode,
        "stderr_tail": (result.stderr or "")[-400:],
        "stdout_tail": (result.stdout or "")[-400:],
    }


if __name__ == "__main__":
    raise SystemExit(main())
