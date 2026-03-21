"""State helpers for the experimental RetroFX 2.x apply/off slice."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from v2.session.install.layout import ensure_install_layout, resolve_install_layout

CURRENT_STATE_SCHEMA = "retrofx.current-state/v2alpha1"
ACTIVATION_MANIFEST_SCHEMA = "retrofx.activation-manifest/v2alpha1"
EVENT_LOG_SCHEMA = "retrofx.session-event/v2alpha1"


def resolve_apply_layout(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    layout = dict(resolve_install_layout(env))
    data_root = Path(str(layout["data_root"]))
    state_root = Path(str(layout["state_root"]))

    layout.update(
        {
            "active_root": str(data_root / "active"),
            "active_current_root": str(data_root / "active" / "current"),
            "active_staging_root": str(data_root / "active" / "staging"),
            "preview_artifacts_root": str(data_root / "preview-artifacts"),
            "current_state_path": str(state_root / "current-state.json"),
            "manifests_root": str(state_root / "manifests"),
            "last_good_root": str(state_root / "last-good"),
            "last_good_state_path": str(state_root / "last-good" / "last-good.json"),
            "last_good_manifest_path": str(state_root / "last-good" / "last-good-manifest.json"),
            "logs_root": str(state_root / "logs"),
        }
    )
    return layout


def ensure_apply_layout(layout: Mapping[str, Any]) -> None:
    ensure_install_layout(layout)
    for key in (
        "active_root",
        "active_staging_root",
        "preview_artifacts_root",
        "manifests_root",
        "last_good_root",
        "logs_root",
    ):
        Path(str(layout[key])).mkdir(parents=True, exist_ok=True)


def load_current_state(layout: Mapping[str, Any]) -> dict[str, Any] | None:
    current_state_path = Path(str(layout["current_state_path"]))
    if not current_state_path.is_file():
        return None
    return json.loads(current_state_path.read_text(encoding="utf-8"))


def write_activation_manifest(layout: Mapping[str, Any], manifest: Mapping[str, Any]) -> Path:
    manifests_root = Path(str(layout["manifests_root"]))
    manifests_root.mkdir(parents=True, exist_ok=True)
    manifest_path = manifests_root / f"{manifest['activation_id']}.json"
    manifest_path.write_text(_json_text(manifest), encoding="utf-8")
    return manifest_path


def write_current_state(layout: Mapping[str, Any], current_state: Mapping[str, Any]) -> Path:
    current_state_path = Path(str(layout["current_state_path"]))
    current_state_path.parent.mkdir(parents=True, exist_ok=True)
    current_state_path.write_text(_json_text(current_state), encoding="utf-8")
    return current_state_path


def write_last_good_state(layout: Mapping[str, Any], current_state: Mapping[str, Any]) -> Path:
    path = Path(str(layout["last_good_state_path"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_text(current_state), encoding="utf-8")
    return path


def write_last_good_manifest(layout: Mapping[str, Any], manifest: Mapping[str, Any]) -> Path:
    path = Path(str(layout["last_good_manifest_path"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_text(manifest), encoding="utf-8")
    return path


def write_event_log(layout: Mapping[str, Any], *, event_name: str, timestamp: str, payload: Mapping[str, Any]) -> Path:
    logs_root = Path(str(layout["logs_root"]))
    logs_root.mkdir(parents=True, exist_ok=True)
    safe_stamp = _timestamp_slug(timestamp)
    path = logs_root / f"{event_name}-{safe_stamp}.json"
    event_payload = {
        "schema": EVENT_LOG_SCHEMA,
        "event_name": event_name,
        "timestamp": timestamp,
        "payload": payload,
    }
    path.write_text(_json_text(event_payload), encoding="utf-8")
    return path


def remove_current_state(layout: Mapping[str, Any]) -> None:
    current_state_path = Path(str(layout["current_state_path"]))
    if current_state_path.exists():
        current_state_path.unlink()


def _timestamp_slug(value: str) -> str:
    return (
        str(value)
        .replace(":", "")
        .replace("-", "")
        .replace("T", "-")
        .replace("Z", "z")
        .replace(".", "")
    )


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
