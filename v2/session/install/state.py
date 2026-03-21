"""Install-state helpers for the experimental RetroFX 2.x install slice."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Mapping

INSTALL_INDEX_SCHEMA = "retrofx.install-index/v2alpha1"
INSTALL_RECORD_SCHEMA = "retrofx.install-record/v2alpha1"
FIXED_NOW_ENV = "RETROFX_V2_FIXED_NOW"


def current_timestamp(*, env: Mapping[str, str] | None = None, now: str | None = None) -> str:
    if now is not None:
        return str(now)

    env_map = {str(key): str(value) for key, value in (env or os.environ).items()}
    fixed = env_map.get(FIXED_NOW_ENV, "").strip()
    if fixed:
        return fixed
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_install_index(layout: Mapping[str, Any]) -> dict[str, Any]:
    index_path = Path(str(layout["install_index_path"]))
    if not index_path.is_file():
        return {
            "schema": INSTALL_INDEX_SCHEMA,
            "install_name": layout["install_name"],
            "installed_bundles": [],
        }
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_install_record(layout: Mapping[str, Any], bundle_id: str) -> dict[str, Any] | None:
    record_path = Path(str(layout["installations_root"])) / f"{bundle_id}.json"
    if not record_path.is_file():
        return None
    return json.loads(record_path.read_text(encoding="utf-8"))


def list_install_records(layout: Mapping[str, Any]) -> list[dict[str, Any]]:
    installations_root = Path(str(layout["installations_root"]))
    if not installations_root.is_dir():
        return []

    records: list[dict[str, Any]] = []
    for record_path in sorted(installations_root.glob("*.json")):
        records.append(json.loads(record_path.read_text(encoding="utf-8")))
    return records


def write_install_record(layout: Mapping[str, Any], record: Mapping[str, Any]) -> Path:
    record_path = Path(str(layout["installations_root"])) / f"{record['bundle_id']}.json"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(_json_text(record), encoding="utf-8")
    return record_path


def write_install_index(layout: Mapping[str, Any], records: list[Mapping[str, Any]]) -> Path:
    index_path = Path(str(layout["install_index_path"]))
    index_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": INSTALL_INDEX_SCHEMA,
        "install_name": layout["install_name"],
        "installed_bundles": [_record_summary(record) for record in sorted(records, key=lambda item: str(item["bundle_id"]))],
    }
    index_path.write_text(_json_text(payload), encoding="utf-8")
    return index_path


def _record_summary(record: Mapping[str, Any]) -> dict[str, Any]:
    profile = dict(record.get("profile", {}))
    pack = record.get("pack")
    install_targets = dict(record.get("install_targets", {}))
    launcher = dict(record.get("launcher", {}))
    release = record.get("experimental_release") if isinstance(record.get("experimental_release"), Mapping) else {}
    return {
        "bundle_id": record["bundle_id"],
        "profile_id": profile.get("id"),
        "profile_name": profile.get("name"),
        "pack_id": pack.get("id") if isinstance(pack, Mapping) else None,
        "release_version": release.get("version"),
        "release_status": release.get("status_label"),
        "installed_at": record.get("installed_at"),
        "bundle_dir": install_targets.get("bundle_dir"),
        "launcher_installed": bool(launcher.get("installed")),
    }


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
