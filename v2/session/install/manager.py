"""User-local install, uninstall, and status helpers for RetroFX 2.x dev bundles."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
from typing import Any, Mapping

from .bundle import IMPLEMENTATION_INFO as BUNDLE_IMPLEMENTATION_INFO, load_bundle_manifest
from .layout import (
    INSTALL_NAME,
    REPO_ROOT,
    bundle_root_path,
    ensure_install_layout,
    install_root_relative_bundle_dir,
    install_root_relative_record_path,
    resolve_install_layout,
)
from .state import current_timestamp, list_install_records, load_install_record, write_install_index, write_install_record

INSTALL_IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-16",
    "surface": "user-local-install",
    "install_name": INSTALL_NAME,
    "mode": "user-local-managed-footprint",
    "not_implemented": [
        "1.x replacement or takeover",
        "root/system installation",
        "global desktop integration",
        "public package publishing",
        "standalone copied toolchain distribution",
    ],
}


def install_dev_bundle(
    bundle: str | Path | None = None,
    *,
    bundle_id: str | None = None,
    bundle_root: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    now: str | None = None,
) -> dict[str, Any]:
    layout = resolve_install_layout(env)
    ensure_install_layout(layout)

    bundle_dir = _resolve_bundle_input(bundle=bundle, bundle_id=bundle_id, bundle_root=bundle_root)
    manifest = load_bundle_manifest(bundle_dir)
    resolved_bundle_id = str(manifest["bundle_id"])

    source_bundle_dir = bundle_dir if bundle_dir.is_dir() else bundle_dir.parent
    destination_dir = Path(str(layout["bundle_store_root"])) / resolved_bundle_id
    replaced_existing = destination_dir.exists()
    if replaced_existing:
        shutil.rmtree(destination_dir)
    shutil.copytree(source_bundle_dir, destination_dir)

    installed_at = current_timestamp(env=env, now=now)
    record = _build_install_record(
        manifest=manifest,
        layout=layout,
        destination_dir=destination_dir,
        source_bundle_dir=source_bundle_dir,
        installed_at=installed_at,
    )
    record_path = write_install_record(layout, record)
    index_path = write_install_index(layout, list_install_records(layout))

    return {
        "ok": True,
        "stage": "install",
        "implementation": INSTALL_IMPLEMENTATION_INFO,
        "bundle": {
            "bundle_id": resolved_bundle_id,
            "source_path": str(source_bundle_dir),
            "manifest_path": str(source_bundle_dir / "manifest.json"),
        },
        "install": {
            "replaced_existing": replaced_existing,
            "bundle_dir": str(destination_dir),
            "record_path": str(record_path),
            "index_path": str(index_path),
            "layout": layout,
        },
        "record": record,
        "note": "This is an experimental user-local 2.x install flow. It does not replace the 1.x installer or runtime.",
    }


def describe_install_state(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
) -> dict[str, Any]:
    layout = resolve_install_layout(env)
    index_payload = _load_index_payload(layout)
    current_workdir = Path(cwd or os.getcwd()).resolve()
    toolchain_mode = _toolchain_mode_for_cwd(current_workdir)

    return {
        "ok": True,
        "stage": "status",
        "implementation": INSTALL_IMPLEMENTATION_INFO,
        "toolchain_mode": toolchain_mode,
        "install_layout": layout,
        "bundle_manifest_schema": "retrofx.bundle/v2alpha1",
        "install_index": index_payload,
        "installed_bundles": index_payload["installed_bundles"],
        "bundle_builder": {
            "repo_bundle_root": layout["repo_bundle_root"],
            "repo_out_root": layout["repo_out_root"],
            "implementation": BUNDLE_IMPLEMENTATION_INFO,
        },
        "note": "This status surface reports only the experimental 2.x user-local footprint and does not inspect 1.x state.",
    }


def uninstall_dev_bundle(
    bundle_id: str,
    *,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    layout = resolve_install_layout(env)
    record = load_install_record(layout, bundle_id)
    if record is None:
        return {
            "ok": False,
            "stage": "uninstall",
            "implementation": INSTALL_IMPLEMENTATION_INFO,
            "errors": [{"severity": "error", "code": "missing-install-record", "message": f"No installed dev bundle record exists for `{bundle_id}`."}],
        }

    removed_paths: list[str] = []
    bundle_dir = Path(str(record["install_targets"]["bundle_dir"]))
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
        removed_paths.append(str(bundle_dir))

    record_path = Path(str(layout["installations_root"])) / f"{bundle_id}.json"
    if record_path.exists():
        record_path.unlink()
        removed_paths.append(str(record_path))

    index_path = write_install_index(layout, list_install_records(layout))
    _prune_empty_dir(Path(str(layout["bundle_store_root"])))
    _prune_empty_dir(Path(str(layout["installations_root"])))

    return {
        "ok": True,
        "stage": "uninstall",
        "implementation": INSTALL_IMPLEMENTATION_INFO,
        "bundle_id": bundle_id,
        "removed_paths": removed_paths,
        "updated_paths": [str(index_path)],
        "preserved_paths": [
            str(Path(str(layout["user_profiles_root"]))),
            str(Path(str(layout["user_packs_root"]))),
        ],
        "note": "User-local config roots are preserved so experimental profiles and packs are not removed implicitly.",
    }


def _build_install_record(
    *,
    manifest: Mapping[str, Any],
    layout: Mapping[str, Any],
    destination_dir: Path,
    source_bundle_dir: Path,
    installed_at: str,
) -> dict[str, Any]:
    data_root = Path(str(layout["data_root"]))
    owned_data_paths = sorted(str(path.relative_to(data_root)) for path in destination_dir.rglob("*") if path.is_file())
    bundle_id = str(manifest["bundle_id"])
    return {
        "schema": "retrofx.install-record/v2alpha1",
        "install_name": layout["install_name"],
        "bundle_id": bundle_id,
        "installed_at": installed_at,
        "profile": {
            "id": manifest["profile"]["id"],
            "name": manifest["profile"]["name"],
            "family": manifest["profile"].get("family"),
        },
        "pack": manifest.get("pack"),
        "source_bundle": {
            "source_path": str(source_bundle_dir),
            "manifest_path": str(source_bundle_dir / "manifest.json"),
            "schema": manifest["schema"],
        },
        "install_roots": {
            "config_root": layout["config_root"],
            "data_root": layout["data_root"],
            "state_root": layout["state_root"],
            "bin_dir": layout["bin_dir"],
            "launcher_path": layout["launcher_path"],
        },
        "install_targets": {
            "bundle_dir": str(destination_dir),
            "bundle_dir_relative": install_root_relative_bundle_dir(bundle_id),
            "record_relative": install_root_relative_record_path(bundle_id),
        },
        "owned_paths": {
            "data_root_relative": owned_data_paths,
            "state_root_relative": [
                install_root_relative_record_path(bundle_id),
                "install-state.json",
            ],
        },
        "launcher": {
            "installed": False,
            "path": layout["launcher_path"],
        },
        "notes": [
            "This install record is owned by the experimental 2.x dev install flow.",
            "It does not imply live apply, default-session takeover, or 1.x replacement.",
        ],
    }


def _resolve_bundle_input(
    *,
    bundle: str | Path | None,
    bundle_id: str | None,
    bundle_root: str | Path | None,
) -> Path:
    if bundle is not None:
        return Path(bundle)
    if bundle_id is not None:
        return bundle_root_path(bundle_root) / bundle_id
    raise ValueError("Either a bundle path or --bundle-id is required.")


def _load_index_payload(layout: Mapping[str, Any]) -> dict[str, Any]:
    index_path = Path(str(layout["install_index_path"]))
    if not index_path.is_file():
        return {
            "schema": "retrofx.install-index/v2alpha1",
            "install_name": layout["install_name"],
            "installed_bundles": [],
        }
    return json.loads(index_path.read_text(encoding="utf-8"))


def _toolchain_mode_for_cwd(current_workdir: Path) -> str:
    try:
        current_workdir.relative_to(REPO_ROOT)
    except ValueError:
        return "installed-dev"
    return "repo-local-dev" if (REPO_ROOT / ".git").exists() else "installed-dev"


def _prune_empty_dir(path: Path) -> None:
    if path.is_dir() and not any(path.iterdir()):
        path.rmdir()
