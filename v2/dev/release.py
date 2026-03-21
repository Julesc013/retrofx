"""Shared experimental release metadata for the current RetroFX 2.x branch."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from v2.session.install.layout import INSTALL_NAME

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"
DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT = REPO_ROOT / "v2" / "releases" / "internal-alpha"

EXPERIMENTAL_STATUS_SCHEMA = "retrofx.experimental-status/v2alpha1"
INTERNAL_ALPHA_PACKAGE_SCHEMA = "retrofx.internal-alpha-package/v2alpha1"

STATUS_LADDER = (
    "experimental",
    "internal-alpha",
    "controlled-alpha",
    "pre-beta",
    "public-beta",
    "stable",
)

CURRENT_EXPERIMENTAL_VERSION = "2.0.0-alpha.internal.1"
CURRENT_STATUS_LABEL = "internal-alpha"
CURRENT_PROMPT = "TWO-24"
CURRENT_DISTRIBUTION_SCOPE = "internal-non-public"
CURRENT_COHORT = "controlled-internal"


def build_experimental_release_metadata(
    *,
    version: str | None = None,
    status_label: str | None = None,
) -> dict[str, Any]:
    chosen_version = str(version or CURRENT_EXPERIMENTAL_VERSION)
    chosen_status = str(status_label or CURRENT_STATUS_LABEL)
    if chosen_status not in STATUS_LADDER:
        raise ValueError(
            f"Unsupported experimental status label `{chosen_status}`. Expected one of: {', '.join(STATUS_LADDER)}."
        )

    return {
        "schema": EXPERIMENTAL_STATUS_SCHEMA,
        "version": chosen_version,
        "status_label": chosen_status,
        "status_ladder": list(STATUS_LADDER),
        "distribution_scope": CURRENT_DISTRIBUTION_SCOPE,
        "cohort": CURRENT_COHORT,
        "prompt": CURRENT_PROMPT,
        "install_name": INSTALL_NAME,
        "public_release": False,
        "production_line": "1.x",
        "ready_for_internal_use": True,
        "ready_for_controlled_alpha": True,
        "ready_for_broader_testing": False,
        "needs_more_stabilization": True,
        "source_revision": _git_output(["rev-parse", "HEAD"]),
        "source_branch": _git_output(["rev-parse", "--abbrev-ref", "HEAD"]),
        "source_tree": str(REPO_ROOT),
        "unified_entrypoint": str(UNIFIED_ENTRYPOINT),
    }


def package_id_for_bundle(bundle_id: str, *, version: str | None = None) -> str:
    chosen_version = str(version or CURRENT_EXPERIMENTAL_VERSION)
    safe_version = chosen_version.replace("/", "-").replace(" ", "-")
    return f"retrofx-v2--{safe_version}--{bundle_id}"


def _git_output(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    return value or None
