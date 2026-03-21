"""Bounded experimental apply/off orchestration for RetroFX 2.x."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import Any, Callable, Mapping

from v2.core.dev.profile_input import run_selected_profile_pipeline
from v2.session.dev.preview_x11_render import preview_x11_render_profile
from v2.session.environment import detect_environment
from v2.session.install import build_dev_bundle, describe_install_state, install_dev_bundle
from v2.session.install.state import current_timestamp
from v2.session.planning import build_session_plan

from .state import (
    ACTIVATION_MANIFEST_SCHEMA,
    CURRENT_STATE_SCHEMA,
    ensure_apply_layout,
    load_current_state,
    remove_current_state,
    resolve_apply_layout,
    write_activation_manifest,
    write_current_state,
    write_event_log,
    write_last_good_manifest,
    write_last_good_state,
)

APPLY_IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-19",
    "surface": "bounded-apply-off",
    "mode": "user-local-current-activation",
    "not_implemented": [
        "1.x replacement or takeover",
        "global desktop mutation",
        "production session-default switching",
        "Wayland render ownership",
        "broad live desktop integration",
    ],
}


def apply_dev_profile(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
    now: str | None = None,
    probe_x11: bool = False,
    probe_seconds: float = 3.0,
    command_runner: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    layout = resolve_apply_layout(env)
    ensure_apply_layout(layout)
    activation_time = current_timestamp(env=env, now=now)

    pipeline_result = run_selected_profile_pipeline(
        profile=str(profile_path) if profile_path is not None else None,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
    )
    if not pipeline_result.ok:
        return {
            "ok": False,
            "stage": pipeline_result.stage,
            "implementation": APPLY_IMPLEMENTATION_INFO,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [error.to_dict() for error in pipeline_result.errors],
            "activation": None,
        }

    resolved_profile = pipeline_result.resolved_profile
    assert resolved_profile is not None
    profile_id = str(resolved_profile["identity"]["id"])
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    plan = build_session_plan(resolved_profile, environment)
    compile_targets = list(plan["compile_targets"])
    activation_id = f"{profile_id}--{_activation_slug(activation_time)}"

    if not compile_targets:
        return {
            "ok": False,
            "stage": "apply",
            "implementation": APPLY_IMPLEMENTATION_INFO,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [
                {
                    "severity": "error",
                    "code": "no-compile-targets",
                    "message": "The current environment and requested targets did not produce any compileable 2.x targets.",
                }
            ],
            "activation": None,
        }

    with TemporaryDirectory() as tmpbundle:
        bundle_payload = build_dev_bundle(
            profile_path,
            pack_id=pack_id,
            pack_profile_id=pack_profile_id,
            bundle_root=tmpbundle,
            target_names=compile_targets,
            env=env,
            cwd=cwd,
            stdin_isatty=stdin_isatty,
            path_lookup=path_lookup,
        )
        if not bundle_payload["ok"]:
            return {
                "ok": False,
                "stage": bundle_payload["stage"],
                "implementation": APPLY_IMPLEMENTATION_INFO,
                "source": pipeline_result.source,
                "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
                "errors": bundle_payload["errors"],
                "activation": None,
            }
        install_payload = install_dev_bundle(bundle_payload["bundle"]["output_dir"], env=env, now=activation_time)

    installed_bundle_dir = Path(str(install_payload["install"]["bundle_dir"]))
    pending_root = Path(str(layout["active_staging_root"])) / activation_id
    current_root = Path(str(layout["active_current_root"]))
    preview_owned_paths: list[str] = []
    if pending_root.exists():
        shutil.rmtree(pending_root)
    if pending_root.parent.exists():
        pending_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(installed_bundle_dir, pending_root)

    env_fragment = _write_session_env_fragment(pending_root, resolved_profile, plan)

    probe_payload = None
    live_applied_targets: list[str] = []
    warnings = _dedupe([warning["message"] for warning in [item.to_dict() for item in pipeline_result.warnings]])
    warnings.extend(plan["warnings"])
    if probe_x11:
        preview_base = Path(str(layout["preview_artifacts_root"])) / activation_id
        probe_payload = preview_x11_render_profile(
            profile_path,
            pack_id=pack_id,
            pack_profile_id=pack_profile_id,
            out_root=preview_base,
            env=env,
            cwd=cwd,
            stdin_isatty=stdin_isatty,
            path_lookup=path_lookup,
            probe_picom=True,
            probe_seconds=probe_seconds,
            command_runner=command_runner,
        )
        if probe_payload.get("preview"):
            preview_dir = Path(str(probe_payload["preview"]["output_dir"]))
            preview_state_path = Path(str(probe_payload["preview"]["preview_state_path"]))
            preview_owned_paths.extend([str(preview_dir), str(preview_state_path)])
            if preview_state_path.is_file():
                metadata_root = pending_root / "metadata"
                metadata_root.mkdir(parents=True, exist_ok=True)
                shutil.copy2(preview_state_path, metadata_root / "x11-preview-state.json")

        probe_status = probe_payload.get("preview", {}).get("probe", {}).get("status")
        if probe_status in {"ok", "timed-out"}:
            live_applied_targets = [
                target_name
                for target_name in ("x11-shader", "x11-picom", "x11-render-runtime")
                if target_name in compile_targets
            ]
        else:
            warnings.append(
                "Explicit X11 live probe was requested but did not complete successfully; the activation remains staged-only."
            )

    previous_state = load_current_state(layout)
    previous_manifest = None
    if previous_state is not None:
        previous_manifest_path = previous_state.get("manifest", {}).get("manifest_path")
        if previous_manifest_path and Path(str(previous_manifest_path)).is_file():
            previous_manifest = json.loads(Path(str(previous_manifest_path)).read_text(encoding="utf-8"))
            write_last_good_manifest(layout, previous_manifest)
        write_last_good_state(layout, previous_state)

    if current_root.exists():
        shutil.rmtree(current_root)
    current_root.parent.mkdir(parents=True, exist_ok=True)
    pending_root.rename(current_root)

    activated_targets = list(compile_targets)
    export_only_targets = [target for target in plan["export_only_targets"] if target in activated_targets]
    degraded_targets = [target for target in plan["degraded_targets"] if target in activated_targets]
    activation_manifest = _build_activation_manifest(
        activation_id=activation_id,
        activation_time=activation_time,
        resolved_profile=resolved_profile,
        source=pipeline_result.source,
        environment=environment,
        plan=plan,
        compile_targets=compile_targets,
        activated_targets=activated_targets,
        export_only_targets=export_only_targets,
        degraded_targets=degraded_targets,
        live_applied_targets=live_applied_targets,
        current_root=current_root,
        installed_bundle_dir=installed_bundle_dir,
        install_payload=install_payload,
        env_fragment=env_fragment,
        preview_payload=probe_payload,
        preview_owned_paths=preview_owned_paths,
        previous_state=previous_state,
        warnings=_dedupe(warnings),
    )
    manifest_path = write_activation_manifest(layout, activation_manifest)
    current_state = _build_current_state(activation_manifest, manifest_path, layout)
    current_state_path = write_current_state(layout, current_state)
    if previous_state is None and previous_manifest is None:
        write_last_good_manifest(layout, activation_manifest)
        write_last_good_state(layout, current_state)

    log_path = write_event_log(
        layout,
        event_name="apply",
        timestamp=activation_time,
        payload={
            "activation_id": activation_id,
            "profile_id": profile_id,
            "compile_targets": compile_targets,
            "live_applied_targets": live_applied_targets,
            "current_state_path": str(current_state_path),
        },
    )

    return {
        "ok": True,
        "stage": "apply",
        "implementation": APPLY_IMPLEMENTATION_INFO,
        "source": pipeline_result.source,
        "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
        "errors": [],
        "profile": {
            "id": profile_id,
            "name": resolved_profile["identity"]["name"],
            "pack": resolved_profile.get("pack"),
        },
        "environment": environment,
        "plan": {
            "compile_targets": compile_targets,
            "export_only_targets": export_only_targets,
            "degraded_targets": degraded_targets,
            "apply_preview_targets": plan["apply_preview_targets"],
            "skipped_targets": plan["skipped_targets"],
            "toolkit_style": plan["toolkit_style"],
            "x11_render": plan["x11_render"],
        },
        "activation": {
            "activation_id": activation_id,
            "current_root": str(current_root),
            "manifest_path": str(manifest_path),
            "current_state_path": str(current_state_path),
            "env_fragment_path": str(env_fragment),
            "activated_targets": activated_targets,
            "live_applied_targets": live_applied_targets,
            "export_only_targets": export_only_targets,
            "degraded_targets": degraded_targets,
            "preview_probe": probe_payload.get("preview") if probe_payload else None,
            "log_path": str(log_path),
        },
        "note": "This is a bounded experimental 2.x apply flow. It stages a 2.x-owned active bundle and optionally runs the explicit X11 live probe, but it does not replace 1.x.",
    }


def off_dev_profile(*, env: Mapping[str, str] | None = None, now: str | None = None) -> dict[str, Any]:
    layout = resolve_apply_layout(env)
    ensure_apply_layout(layout)
    current_state = load_current_state(layout)
    if current_state is None:
        return {
            "ok": True,
            "stage": "off",
            "implementation": APPLY_IMPLEMENTATION_INFO,
            "active": False,
            "removed_paths": [],
            "preserved_paths": [str(Path(str(layout["bundle_store_root"]))), str(Path(str(layout["installations_root"])))],
            "note": "No experimental 2.x activation is currently active.",
        }

    removed_paths: list[str] = []
    current_root = Path(str(layout["active_current_root"]))
    if current_root.exists():
        shutil.rmtree(current_root)
        removed_paths.append(str(current_root))

    for owned_path in current_state.get("cleanup", {}).get("data_paths", []):
        path = Path(str(owned_path))
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            removed_paths.append(str(path))

    current_state_path = Path(str(layout["current_state_path"]))
    if current_state_path.exists():
        current_state_path.unlink()
        removed_paths.append(str(current_state_path))

    timestamp = current_timestamp(env=env, now=now)
    log_path = write_event_log(
        layout,
        event_name="off",
        timestamp=timestamp,
        payload={
            "activation_id": current_state["activation"]["activation_id"],
            "removed_paths": removed_paths,
            "live_applied_targets": current_state["activation"]["live_applied_targets"],
            "note": "The bounded X11 probe is short-lived; off only clears 2.x-owned staged artifacts and state records.",
        },
    )
    remove_current_state(layout)

    return {
        "ok": True,
        "stage": "off",
        "implementation": APPLY_IMPLEMENTATION_INFO,
        "active": False,
        "deactivated_profile": current_state.get("profile"),
        "removed_paths": _dedupe(removed_paths),
        "preserved_paths": [
            str(Path(str(layout["bundle_store_root"]))),
            str(Path(str(layout["installations_root"]))),
            str(Path(str(layout["last_good_root"]))),
            str(Path(str(layout["manifests_root"]))),
        ],
        "log_path": str(log_path),
        "note": "Only 2.x-owned active state was cleared. Installed bundles and 1.x paths were preserved.",
    }


def describe_current_activation(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
) -> dict[str, Any]:
    layout = resolve_apply_layout(env)
    ensure_apply_layout(layout)
    current_state = load_current_state(layout)
    install_status = describe_install_state(env=env, cwd=cwd)
    active = current_state is not None

    return {
        "ok": True,
        "stage": "status",
        "implementation": APPLY_IMPLEMENTATION_INFO,
        "active": active,
        "activation": current_state,
        "install_state": install_status,
        "state_layout": {
            "active_current_root": layout["active_current_root"],
            "current_state_path": layout["current_state_path"],
            "manifests_root": layout["manifests_root"],
            "last_good_root": layout["last_good_root"],
            "logs_root": layout["logs_root"],
            "preview_artifacts_root": layout["preview_artifacts_root"],
        },
        "note": (
            "This status surface reports the experimental 2.x current activation plus the user-local install footprint."
            if active
            else "No experimental 2.x activation is currently active. Installed bundle metadata is reported separately below."
        ),
    }


def _write_session_env_fragment(
    active_root: Path,
    resolved_profile: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> Path:
    session_root = active_root / "session"
    session_root.mkdir(parents=True, exist_ok=True)
    env_path = session_root / "retrofx-v2-session.env"
    lines = [
        "# RetroFX 2.x experimental active session fragment",
        f"RETROFX_V2_ACTIVE=1",
        f"RETROFX_V2_PROFILE_ID={resolved_profile['identity']['id']}",
        f"RETROFX_V2_PROFILE_NAME={resolved_profile['identity']['name']}",
        f"RETROFX_V2_ACTIVE_ROOT={active_root}",
        f"RETROFX_V2_APPLY_MODE={resolved_profile['semantics']['session']['apply_mode']}",
        f"RETROFX_V2_COMPILE_TARGETS={','.join(plan['compile_targets'])}",
        f"RETROFX_V2_EXPORT_ONLY_TARGETS={','.join(plan['export_only_targets'])}",
        f"RETROFX_V2_DEGRADED_TARGETS={','.join(plan['degraded_targets'])}",
        f"RETROFX_V2_TOOLKIT_STATUS={plan['toolkit_style']['overall_status']}",
        f"RETROFX_V2_X11_RENDER_STATUS={plan['x11_render']['overall_status']}",
        "",
    ]
    for target_name in sorted(plan["compile_targets"]):
        env_key = "RETROFX_V2_TARGET_" + target_name.upper().replace("-", "_")
        lines.append(f"{env_key}={active_root / 'targets' / target_name}")
    lines.append("")
    env_path.write_text("\n".join(lines), encoding="utf-8")
    return env_path


def _build_activation_manifest(
    *,
    activation_id: str,
    activation_time: str,
    resolved_profile: Mapping[str, Any],
    source: Mapping[str, Any],
    environment: Mapping[str, Any],
    plan: Mapping[str, Any],
    compile_targets: list[str],
    activated_targets: list[str],
    export_only_targets: list[str],
    degraded_targets: list[str],
    live_applied_targets: list[str],
    current_root: Path,
    installed_bundle_dir: Path,
    install_payload: Mapping[str, Any],
    env_fragment: Path,
    preview_payload: Mapping[str, Any] | None,
    preview_owned_paths: list[str],
    previous_state: Mapping[str, Any] | None,
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "schema": ACTIVATION_MANIFEST_SCHEMA,
        "activation_id": activation_id,
        "activated_at": activation_time,
        "profile": {
            "id": resolved_profile["identity"]["id"],
            "name": resolved_profile["identity"]["name"],
            "family": resolved_profile["identity"]["family"],
            "strictness": resolved_profile["identity"]["strictness"],
        },
        "source": source,
        "pack": resolved_profile.get("pack"),
        "environment": {
            "session_type": environment["session_type"],
            "wm_or_de": environment["wm_or_de"],
            "context_class": environment["context_class"],
        },
        "bundle": {
            "bundle_id": install_payload["bundle"]["bundle_id"],
            "bundle_dir": str(installed_bundle_dir),
            "record_path": install_payload["install"]["record_path"],
        },
        "activation": {
            "mode": "experimental-apply",
            "active_root": str(current_root),
            "session_env_fragment": str(env_fragment),
            "compile_targets": compile_targets,
            "activated_targets": activated_targets,
            "live_applied_targets": live_applied_targets,
            "export_only_targets": export_only_targets,
            "degraded_targets": degraded_targets,
            "skipped_targets": plan["skipped_targets"],
            "used_x11_live_probe": bool(live_applied_targets),
        },
        "plan_summary": {
            "apply_preview_targets": plan["apply_preview_targets"],
            "toolkit_style": plan["toolkit_style"],
            "x11_render": plan["x11_render"],
        },
        "cleanup": {
            "data_paths": _dedupe(preview_owned_paths),
            "clear_current_state_path": True,
            "notes": [
                "Off removes the active 2.x bundle staging plus any preview-artifact roots recorded here.",
                "Installed bundles remain in the managed 2.x bundle store until explicitly uninstalled.",
            ],
        },
        "previous_state": {
            "activation_id": previous_state["activation"]["activation_id"] if previous_state else None,
            "manifest_path": previous_state["manifest"]["manifest_path"] if previous_state else None,
        },
        "warnings": warnings,
        "notes": [
            "This manifest is owned by the experimental TWO-19 apply/off workflow.",
            "Targets staged into the active area are not automatically live-applied unless explicitly listed in `live_applied_targets`.",
        ],
        "preview_probe": preview_payload.get("preview") if preview_payload else None,
    }


def _build_current_state(
    manifest: Mapping[str, Any],
    manifest_path: Path,
    layout: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": CURRENT_STATE_SCHEMA,
        "active": True,
        "profile": manifest["profile"],
        "pack": manifest.get("pack"),
        "bundle": manifest["bundle"],
        "activation": {
            "activation_id": manifest["activation_id"],
            "activated_at": manifest["activated_at"],
            "active_root": manifest["activation"]["active_root"],
            "activated_targets": manifest["activation"]["activated_targets"],
            "live_applied_targets": manifest["activation"]["live_applied_targets"],
            "export_only_targets": manifest["activation"]["export_only_targets"],
            "degraded_targets": manifest["activation"]["degraded_targets"],
            "used_x11_live_probe": manifest["activation"]["used_x11_live_probe"],
        },
        "manifest": {
            "manifest_path": str(manifest_path),
            "schema": manifest["schema"],
        },
        "cleanup": {
            "data_paths": manifest["cleanup"]["data_paths"],
            "clear_current_state_path": True,
        },
        "warnings": manifest["warnings"],
        "layout": {
            "active_current_root": layout["active_current_root"],
            "current_state_path": layout["current_state_path"],
        },
    }


def _activation_slug(timestamp: str) -> str:
    return timestamp.replace(":", "").replace("-", "").replace("T", "-").replace("Z", "z")


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
