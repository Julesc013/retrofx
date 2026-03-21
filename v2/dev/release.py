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
CURRENT_PROMPT = "TWO-27"
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
    source_control = build_source_control_summary()
    local_tag_name = local_tag_name_for_version(chosen_version)

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
        "ready_for_internal_alpha_continuation": True,
        "ready_for_controlled_alpha": True,
        "ready_for_local_alpha_tag_candidate": True,
        "alpha_candidate_ready": True,
        "ready_for_broader_testing": False,
        "needs_more_stabilization": True,
        "local_tag_name": local_tag_name,
        "local_tag_points_at_head": _git_tag_points_at_head(local_tag_name),
        "source_revision": _git_output(["rev-parse", "HEAD"]),
        "source_branch": _git_output(["rev-parse", "--abbrev-ref", "HEAD"]),
        "source_tree": str(REPO_ROOT),
        "source_control": source_control,
        "working_tree_clean": source_control["working_tree_clean"],
        "unified_entrypoint": str(UNIFIED_ENTRYPOINT),
    }


def package_id_for_bundle(bundle_id: str, *, version: str | None = None) -> str:
    chosen_version = str(version or CURRENT_EXPERIMENTAL_VERSION)
    safe_version = chosen_version.replace("/", "-").replace(" ", "-")
    return f"retrofx-v2--{safe_version}--{bundle_id}"


def local_tag_name_for_version(version: str) -> str:
    return f"v{version}"


def build_source_control_summary() -> dict[str, Any]:
    branch = _git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    revision = _git_output(["rev-parse", "HEAD"])
    porcelain = _git_output(["status", "--porcelain=v1", "--untracked-files=all"])
    if branch is None and revision is None and porcelain is None:
        return {
            "git_available": False,
            "working_tree_clean": None,
            "branch": None,
            "revision": None,
            "staged_count": 0,
            "modified_count": 0,
            "untracked_count": 0,
            "conflicted_count": 0,
            "status_entry_count": 0,
        }

    staged_count = 0
    modified_count = 0
    untracked_count = 0
    conflicted_count = 0
    status_lines = [line for line in (porcelain or "").splitlines() if line.strip()]
    for line in status_lines:
        if line.startswith("??"):
            untracked_count += 1
            continue
        if line.startswith("!!"):
            continue
        x = line[0]
        y = line[1]
        if x != " ":
            staged_count += 1
        if y != " ":
            modified_count += 1
        if "U" in (x, y):
            conflicted_count += 1

    return {
        "git_available": True,
        "working_tree_clean": len(status_lines) == 0,
        "branch": branch,
        "revision": revision,
        "staged_count": staged_count,
        "modified_count": modified_count,
        "untracked_count": untracked_count,
        "conflicted_count": conflicted_count,
        "status_entry_count": len(status_lines),
    }


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


def _git_tag_points_at_head(tag_name: str) -> bool | None:
    head_revision = _git_output(["rev-parse", "HEAD"])
    if head_revision is None:
        return None
    tag_revision = _git_output(["rev-list", "-n", "1", tag_name])
    if tag_revision is None:
        return False
    return tag_revision == head_revision
