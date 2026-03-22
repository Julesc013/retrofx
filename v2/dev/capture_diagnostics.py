"""Local diagnostics capture for the RetroFX 2.x experimental surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping

from v2.core.dev.profile_input import add_profile_selection_args, run_selected_profile_pipeline
from v2.session import build_session_plan, detect_environment
from v2.session.apply import describe_current_activation
from v2.session.apply.state import load_current_state, resolve_apply_layout
from v2.session.install import describe_install_state
from v2.session.install.layout import REPO_ROOT, resolve_install_layout
from v2.session.install.state import current_timestamp, list_install_records

from .release import CURRENT_PROMPT, build_experimental_release_metadata, build_source_control_summary
from .status import build_platform_status

DEFAULT_DIAGNOSTICS_ROOT = REPO_ROOT / "v2" / "out" / "diagnostics"
DEFAULT_ARTIFACT_ROOT = REPO_ROOT / "v2" / "out"

IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": CURRENT_PROMPT,
    "surface": "current-2x-diagnostics",
    "mode": "local-file-based-evidence-capture",
    "not_implemented": [
        "network reporting",
        "telemetry",
        "standalone support bundles beyond the local checkout",
        "automatic redaction of arbitrary shell history or unrelated user files",
    ],
}


def capture_diagnostics(
    profile_path: str | Path | None = None,
    *,
    pack_id: str | None = None,
    pack_profile_id: str | None = None,
    output_root: str | Path | None = None,
    artifact_root: str | Path | None = None,
    label: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Callable[[str], str | None] | None = None,
    now: str | None = None,
    release_status: Mapping[str, Any] | None = None,
    platform_status_builder: Callable[..., dict[str, Any]] | None = None,
    implementation_info: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    chosen_release_status = dict(release_status) if release_status is not None else build_experimental_release_metadata()
    chosen_platform_status_builder = platform_status_builder or build_platform_status
    chosen_implementation_info = dict(implementation_info) if implementation_info is not None else dict(IMPLEMENTATION_INFO)
    timestamp = current_timestamp(env=env, now=now)
    slug = _capture_slug(timestamp=timestamp, label=label)
    chosen_output_root = Path(output_root) if output_root is not None else DEFAULT_DIAGNOSTICS_ROOT
    output_dir = chosen_output_root / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    platform_status = chosen_platform_status_builder(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    install_state = describe_install_state(env=env, cwd=cwd)
    install_records = list_install_records(resolve_install_layout(env))
    activation_status = describe_current_activation(env=env, cwd=cwd)
    apply_layout = resolve_apply_layout(env)
    current_state = load_current_state(apply_layout)
    source_control = build_source_control_summary()

    artifacts: list[dict[str, Any]] = []
    artifacts.append(_write_json_artifact(output_dir, "release-status.json", chosen_release_status))
    artifacts.append(_write_json_artifact(output_dir, "source-control.json", source_control))
    artifacts.append(_write_json_artifact(output_dir, "platform-status.json", platform_status))
    artifacts.append(_write_json_artifact(output_dir, "environment.json", environment))
    artifacts.append(_write_json_artifact(output_dir, "install-state.json", install_state))
    artifacts.append(_write_json_artifact(output_dir, "current-activation.json", activation_status))

    state_artifacts = _capture_state_artifacts(output_dir, apply_layout, current_state)
    artifacts.extend(state_artifacts)

    profile_section: dict[str, Any] | None = None
    if profile_path is not None or pack_id is not None or pack_profile_id is not None:
        try:
            profile_section, profile_artifacts = _capture_profile_artifacts(
                output_dir=output_dir,
                profile_path=profile_path,
                pack_id=pack_id,
                pack_profile_id=pack_profile_id,
                artifact_root=Path(artifact_root) if artifact_root is not None else DEFAULT_ARTIFACT_ROOT,
                install_records=install_records,
                env=env,
                cwd=cwd,
                stdin_isatty=stdin_isatty,
                path_lookup=path_lookup,
            )
        except ValueError as exc:
            error_payload = {
                "ok": False,
                "stage": "load",
                "implementation": chosen_implementation_info,
                "release_status": chosen_release_status,
                "warnings": [],
                "errors": [
                    {
                        "severity": "error",
                        "code": "invalid-profile-selector",
                        "message": str(exc),
                    }
                ],
                "capture": None,
            }
            error_artifact = _write_json_artifact(output_dir, "profile/pipeline-failure.json", error_payload)
            artifacts.append(error_artifact)
            return error_payload
        artifacts.extend(profile_artifacts)

    manifest = {
        "schema": "retrofx.diagnostics-capture/v2alpha1",
        "captured_at": timestamp,
        "capture_id": slug,
        "release_status": chosen_release_status,
        "label": label,
        "output_dir": str(output_dir),
        "implementation": chosen_implementation_info,
        "source_tree": str(REPO_ROOT),
        "source_control": source_control,
        "included_sections": {
            "source_control": True,
            "platform_status": True,
            "environment": True,
            "install_state": True,
            "current_activation": True,
            "profile": profile_section is not None,
            "state_files": bool(state_artifacts),
        },
        "profile": profile_section,
        "artifacts": ["capture-manifest.json", *[artifact["relative_path"] for artifact in artifacts]],
        "notes": [
            "This capture is local-only and intentionally limited to obvious 2.x debugging material.",
            "It does not gather unrelated user files, shell history, or network telemetry.",
            "1.x production paths are reported for comparison only and are not mutated by this command.",
        ],
    }
    manifest_artifact = _write_json_artifact(output_dir, "capture-manifest.json", manifest)
    artifacts.insert(0, manifest_artifact)

    return {
        "ok": True,
        "stage": "diagnostics",
        "implementation": chosen_implementation_info,
        "release_status": chosen_release_status,
        "capture": {
            "capture_id": slug,
            "output_dir": str(output_dir),
            "artifact_count": len(artifacts),
            "manifest_path": str(output_dir / "capture-manifest.json"),
            "profile": profile_section,
        },
        "artifacts": artifacts,
        "note": (
            "This diagnostics capture is for bounded 2.x evidence gathering across internal alpha and limited technical-beta workflows. "
            "It writes local files and does not perform network reporting or touch 1.x state."
        ),
    }


def main(
    argv: list[str] | None = None,
    *,
    release_status: Mapping[str, Any] | None = None,
    platform_status_builder: Callable[..., dict[str, Any]] | None = None,
    implementation_info: Mapping[str, Any] | None = None,
) -> int:
    parser = argparse.ArgumentParser(
        prog="retrofx-v2 diagnostics",
        description="Capture a local 2.x diagnostics directory for controlled internal alpha or limited technical-beta testing.",
    )
    add_profile_selection_args(parser)
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_DIAGNOSTICS_ROOT),
        help=f"Diagnostics output root. Defaults to {DEFAULT_DIAGNOSTICS_ROOT}.",
    )
    parser.add_argument(
        "--artifact-root",
        default=str(DEFAULT_ARTIFACT_ROOT),
        help=f"Compiled output root used for optional profile output inventory. Defaults to {DEFAULT_ARTIFACT_ROOT}.",
    )
    parser.add_argument(
        "--label",
        help="Optional short label appended to the diagnostics directory name.",
    )
    args = parser.parse_args(argv)

    payload = capture_diagnostics(
        args.profile,
        pack_id=args.pack_id,
        pack_profile_id=args.pack_profile_id,
        output_root=args.output_root,
        artifact_root=args.artifact_root,
        label=args.label,
        release_status=release_status,
        platform_status_builder=platform_status_builder,
        implementation_info=implementation_info,
    )
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0 if payload["ok"] else 1


def _capture_profile_artifacts(
    *,
    output_dir: Path,
    profile_path: str | Path | None,
    pack_id: str | None,
    pack_profile_id: str | None,
    artifact_root: Path,
    install_records: list[Mapping[str, Any]],
    env: Mapping[str, str] | None,
    cwd: str | Path | None,
    stdin_isatty: bool | None,
    path_lookup: Callable[[str], str | None] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    pipeline_result = run_selected_profile_pipeline(
        profile=str(profile_path) if profile_path is not None else None,
        pack_id=pack_id,
        pack_profile_id=pack_profile_id,
    )
    artifacts: list[dict[str, Any]] = []

    source_selector = {
        "profile": str(profile_path) if profile_path is not None else None,
        "pack_id": pack_id,
        "pack_profile_id": pack_profile_id,
    }
    artifacts.append(_write_json_artifact(output_dir, "profile/source-selector.json", source_selector))

    if not pipeline_result.ok:
        failure_payload = {
            "ok": False,
            "stage": pipeline_result.stage,
            "source": pipeline_result.source,
            "warnings": [warning.to_dict() for warning in pipeline_result.warnings],
            "errors": [error.to_dict() for error in pipeline_result.errors],
        }
        artifacts.append(_write_json_artifact(output_dir, "profile/pipeline-failure.json", failure_payload))
        return (
            {
                "ok": False,
                "stage": pipeline_result.stage,
                "source": pipeline_result.source,
            },
            artifacts,
        )

    resolved_profile = pipeline_result.resolved_profile
    assert resolved_profile is not None

    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    plan = build_session_plan(resolved_profile, environment)

    resolved_payload = pipeline_result.to_dict(include_normalized=True)
    artifacts.append(_write_json_artifact(output_dir, "profile/resolved-profile.json", resolved_payload))
    artifacts.append(_write_json_artifact(output_dir, "profile/session-plan.json", plan))

    profile_id = str(resolved_profile["identity"]["id"])
    profile_output_dir = artifact_root / profile_id
    inventory_payload = {
        "profile_id": profile_id,
        "artifact_root": str(artifact_root),
        "profile_output_dir": str(profile_output_dir),
        "present": profile_output_dir.is_dir(),
        "inventory_mode": "repo-out-root",
        "files": _inventory_tree(profile_output_dir) if profile_output_dir.is_dir() else [],
    }
    artifacts.append(_write_json_artifact(output_dir, "profile/output-inventory.json", inventory_payload))

    install_bundle_payload = _build_install_bundle_inventory(
        install_records,
        profile_id=profile_id,
        pack_id=pack_id,
    )
    artifacts.append(_write_json_artifact(output_dir, "profile/install-bundle-inventory.json", install_bundle_payload))
    if install_bundle_payload["present"]:
        bundle_manifest_path = Path(str(install_bundle_payload["manifest_path"]))
        if bundle_manifest_path.is_file():
            artifacts.append(_copy_text_artifact(output_dir, "profile/install-bundle-manifest.json", bundle_manifest_path))
        package_manifest_path = install_bundle_payload.get("package_manifest_path")
        if package_manifest_path and Path(str(package_manifest_path)).is_file():
            artifacts.append(
                _copy_text_artifact(output_dir, "profile/source-package-manifest.json", Path(str(package_manifest_path)))
            )

    return (
        {
            "ok": True,
            "id": profile_id,
            "name": resolved_profile["identity"]["name"],
            "origin": resolved_profile["source"]["origin"],
            "pack": resolved_profile.get("pack"),
            "output_inventory_present": inventory_payload["present"],
            "install_bundle_inventory_present": install_bundle_payload["present"],
        },
        artifacts,
    )


def _capture_state_artifacts(
    output_dir: Path,
    apply_layout: Mapping[str, Any],
    current_state: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []

    for relative_name, source_path in (
        ("state/current-state.json", Path(str(apply_layout["current_state_path"]))),
        ("state/last-good.json", Path(str(apply_layout["last_good_state_path"]))),
        ("state/last-good-manifest.json", Path(str(apply_layout["last_good_manifest_path"]))),
    ):
        if source_path.is_file():
            artifacts.append(_copy_text_artifact(output_dir, relative_name, source_path))

    if current_state is not None:
        manifest_path = current_state.get("manifest", {}).get("manifest_path")
        if manifest_path and Path(str(manifest_path)).is_file():
            artifacts.append(_copy_text_artifact(output_dir, "state/active-manifest.json", Path(str(manifest_path))))

    logs_root = Path(str(apply_layout["logs_root"]))
    log_files = sorted(logs_root.glob("*.json")) if logs_root.is_dir() else []
    latest_logs = log_files[-5:]
    log_inventory = {
        "logs_root": str(logs_root),
        "present": logs_root.is_dir(),
        "latest_logs": [str(path.name) for path in latest_logs],
    }
    artifacts.append(_write_json_artifact(output_dir, "state/log-inventory.json", log_inventory))
    for path in latest_logs:
        artifacts.append(_copy_text_artifact(output_dir, f"state/logs/{path.name}", path))

    return artifacts


def _inventory_tree(root: Path) -> list[str]:
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def _build_install_bundle_inventory(
    install_records: list[Mapping[str, Any]],
    *,
    profile_id: str,
    pack_id: str | None,
) -> dict[str, Any]:
    chosen_record = _select_install_record(install_records, profile_id=profile_id, pack_id=pack_id)
    if chosen_record is None:
        return {
            "present": False,
            "profile_id": profile_id,
            "pack_id": pack_id,
            "bundle_id": None,
            "bundle_dir": None,
            "manifest_path": None,
            "package_manifest_path": None,
            "inventory_mode": "installed-bundle",
            "files": [],
        }

    bundle_dir = Path(str(chosen_record["install_targets"]["bundle_dir"]))
    manifest_path = bundle_dir / "manifest.json"
    source_bundle_dir = Path(str(chosen_record["source_bundle"]["source_path"]))
    package_manifest_path = source_bundle_dir.parent / "package-manifest.json"
    return {
        "present": bundle_dir.is_dir(),
        "profile_id": profile_id,
        "pack_id": pack_id,
        "bundle_id": chosen_record["bundle_id"],
        "bundle_dir": str(bundle_dir),
        "manifest_path": str(manifest_path),
        "manifest_present": manifest_path.is_file(),
        "package_manifest_path": str(package_manifest_path) if package_manifest_path.is_file() else None,
        "installed_at": chosen_record.get("installed_at"),
        "release_version": chosen_record.get("experimental_release", {}).get("version"),
        "release_status": chosen_record.get("experimental_release", {}).get("status_label"),
        "inventory_mode": "installed-bundle",
        "files": _inventory_tree(bundle_dir) if bundle_dir.is_dir() else [],
    }


def _select_install_record(
    install_records: list[Mapping[str, Any]],
    *,
    profile_id: str,
    pack_id: str | None,
) -> Mapping[str, Any] | None:
    matches = []
    for record in install_records:
        record_profile = record.get("profile", {})
        record_pack = record.get("pack", {})
        if str(record_profile.get("id")) != profile_id:
            continue
        if pack_id is not None and str(record_pack.get("id")) != pack_id:
            continue
        matches.append(record)

    if not matches:
        return None
    matches.sort(key=lambda item: str(item.get("installed_at", "")))
    return matches[-1]


def _capture_slug(*, timestamp: str, label: str | None) -> str:
    base = (
        str(timestamp)
        .replace(":", "")
        .replace("-", "")
        .replace("T", "-")
        .replace("Z", "z")
        .replace(".", "")
    )
    if label:
        safe_label = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in str(label).strip()).strip("-")
        if safe_label:
            return f"{base}--{safe_label}"
    return base


def _write_json_artifact(output_dir: Path, relative_path: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return _write_text_artifact(output_dir, relative_path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _copy_text_artifact(output_dir: Path, relative_path: str, source_path: Path) -> dict[str, Any]:
    return _write_text_artifact(output_dir, relative_path, source_path.read_text(encoding="utf-8"))


def _write_text_artifact(output_dir: Path, relative_path: str, content: str) -> dict[str, Any]:
    path = output_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "relative_path": relative_path,
        "output_path": str(path),
        "byte_count": len(content.encode("utf-8")),
        "content_sha256": digest,
    }


if __name__ == "__main__":
    raise SystemExit(main())
