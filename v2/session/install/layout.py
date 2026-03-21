"""Path layout helpers for the experimental RetroFX 2.x install slice."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[3]
INSTALL_NAME = "retrofx-v2-dev"
DEFAULT_BUNDLE_ROOT = REPO_ROOT / "v2" / "bundles"
DEFAULT_OUT_ROOT = REPO_ROOT / "v2" / "out"
PRODUCTION_1X_CONFIG_ROOT = "~/.config/retrofx"
PRODUCTION_1X_LAUNCHER_PATH = "~/.local/bin/retrofx"


def resolve_install_layout(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    env_map = {str(key): str(value) for key, value in (env or os.environ).items()}
    home = Path(env_map.get("HOME") or Path.home()).expanduser()

    config_base = Path(env_map.get("XDG_CONFIG_HOME") or (home / ".config")).expanduser()
    data_base = Path(env_map.get("XDG_DATA_HOME") or (home / ".local" / "share")).expanduser()
    state_base = Path(env_map.get("XDG_STATE_HOME") or (home / ".local" / "state")).expanduser()
    bin_dir = Path(env_map.get("RETROFX_V2_BIN_DIR") or (home / ".local" / "bin")).expanduser()

    config_root = config_base / INSTALL_NAME
    data_root = data_base / INSTALL_NAME
    state_root = state_base / INSTALL_NAME
    bundle_store_root = data_root / "bundles"
    installations_root = state_root / "installations"
    install_index_path = state_root / "install-state.json"
    launcher_path = bin_dir / INSTALL_NAME

    return {
        "install_name": INSTALL_NAME,
        "home": str(home),
        "config_root": str(config_root),
        "data_root": str(data_root),
        "state_root": str(state_root),
        "bundle_store_root": str(bundle_store_root),
        "installations_root": str(installations_root),
        "install_index_path": str(install_index_path),
        "bin_dir": str(bin_dir),
        "launcher_path": str(launcher_path),
        "user_profiles_root": str(config_root / "profiles"),
        "user_packs_root": str(config_root / "packs"),
        "repo_bundle_root": str(DEFAULT_BUNDLE_ROOT),
        "repo_out_root": str(DEFAULT_OUT_ROOT),
        "production_1x_paths": {
            "config_root": PRODUCTION_1X_CONFIG_ROOT,
            "launcher_path": PRODUCTION_1X_LAUNCHER_PATH,
        },
    }


def ensure_install_layout(layout: Mapping[str, Any]) -> None:
    for key in (
        "config_root",
        "data_root",
        "state_root",
        "bundle_store_root",
        "installations_root",
        "user_profiles_root",
        "user_packs_root",
    ):
        Path(str(layout[key])).mkdir(parents=True, exist_ok=True)


def bundle_root_path(bundle_root: str | Path | None = None) -> Path:
    return Path(bundle_root) if bundle_root is not None else DEFAULT_BUNDLE_ROOT


def install_root_relative_bundle_dir(bundle_id: str) -> str:
    return f"bundles/{bundle_id}"


def install_root_relative_record_path(bundle_id: str) -> str:
    return f"installations/{bundle_id}.json"
