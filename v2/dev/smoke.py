"""Safe smoke workflow for the consolidated RetroFX 2.x dev surface."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.core.dev.compile_targets import DEFAULT_OUT_ROOT, compile_profile_to_output
from v2.core.dev.plan_session import plan_profile_session
from v2.core.dev.profile_input import run_selected_profile_pipeline
from v2.session.apply import apply_dev_profile, describe_current_activation

from .release import CURRENT_PROMPT

SMOKE_IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": CURRENT_PROMPT,
    "surface": "developer-smoke-workflow",
    "mode": "safe-by-default",
    "not_implemented": [
        "production readiness checks",
        "automatic destructive cleanup outside 2.x ownership",
        "broad live desktop integration",
    ],
}


def run_smoke_workflow(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    out_root: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Any | None = None,
    apply: bool = False,
    probe_x11: bool = False,
    probe_seconds: float = 3.0,
    command_runner: Any | None = None,
) -> dict[str, Any]:
    chosen_out_root = Path(out_root) if out_root is not None else DEFAULT_OUT_ROOT
    resolved = run_selected_profile_pipeline(
        profile=str(profile_path) if profile_path is not None else None,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
    )
    if not resolved.ok:
        return {
            "ok": False,
            "stage": resolved.stage,
            "implementation": SMOKE_IMPLEMENTATION_INFO,
            "steps": {
                "resolve": resolved.to_dict(include_normalized=False),
                "plan": None,
                "compile": None,
                "apply": None,
                "status": None,
            },
            "note": "Smoke stopped during profile resolution.",
        }

    resolve_payload = resolved.to_dict(include_normalized=False)
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
    compile_payload = compile_profile_to_output(
        profile_path,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
        env=env,
        cwd=cwd,
        stdin_isatty=stdin_isatty,
        path_lookup=path_lookup,
        out_root=chosen_out_root,
    )

    apply_payload = None
    current_status = None
    if apply:
        apply_payload = apply_dev_profile(
            profile_path,
            pack_id=pack_id,
            pack_profile_id=pack_profile_id,
            env=env,
            cwd=cwd,
            stdin_isatty=stdin_isatty,
            path_lookup=path_lookup,
            probe_x11=probe_x11,
            probe_seconds=probe_seconds,
            command_runner=command_runner,
        )
        current_status = describe_current_activation(env=env, cwd=cwd)

    ok = bool(plan_payload["ok"] and compile_payload["ok"] and (apply_payload["ok"] if apply_payload is not None else True))
    return {
        "ok": ok,
        "stage": "smoke",
        "implementation": SMOKE_IMPLEMENTATION_INFO,
        "profile_selector": {
            "profile": str(profile_path) if profile_path is not None else None,
            "pack_id": pack_id,
            "pack_profile_id": pack_profile_id,
        },
        "steps": {
            "resolve": resolve_payload,
            "plan": plan_payload,
            "compile": compile_payload,
            "apply": apply_payload,
            "status": current_status,
        },
        "note": (
            "Smoke completed with bounded apply because --apply was requested."
            if apply
            else "Smoke completed in non-destructive mode. No apply step was executed."
        ),
    }
