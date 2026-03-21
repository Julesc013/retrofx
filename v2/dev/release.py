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

CURRENT_EXPERIMENTAL_VERSION = "2.0.0-alpha.internal.2"
CURRENT_STATUS_LABEL = "internal-alpha"
CURRENT_PROMPT = "TWO-31"
CURRENT_DISTRIBUTION_SCOPE = "internal-non-public"
CURRENT_COHORT = "controlled-internal"
PROPOSED_PRE_BETA_VERSION = "2.0.0-prebeta.internal.1"
PROPOSED_PRE_BETA_STATUS_LABEL = "pre-beta"
PUBLIC_BETA_BLOCKERS = [
    "no real Wayland-host validation pass exists yet",
    "package, install, and diagnostics surfaces remain repo-checkout dependent and intentionally internal-only",
    "migration validation remains representative rather than broad",
    "bounded X11 live probing remains a narrow single-host trust surface",
]


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
    tag_state = describe_local_tag_state(local_tag_name)
    latest_existing_local_alpha_tag = latest_matching_tag("v2.0.0-alpha.internal.*")
    proposed_pre_beta_tag_name = local_tag_name_for_version(PROPOSED_PRE_BETA_VERSION)
    latest_existing_local_pre_beta_tag = latest_matching_tag("v2.0.0-prebeta.internal.*")

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
        "ready_for_controlled_internal_alpha": True,
        "ready_for_controlled_alpha": False,
        "ready_for_local_alpha_tag_candidate": False,
        "alpha_candidate_ready": False,
        "ready_for_broader_alpha": False,
        "ready_for_continued_broader_alpha": False,
        "ready_for_controlled_external_alpha": False,
        "ready_for_non_public_pre_beta": False,
        "ready_for_local_pre_beta_tag_candidate": False,
        "pre_beta_candidate_ready": False,
        "ready_for_limited_public_technical_beta": False,
        "ready_for_public_technical_beta_candidate": False,
        "ready_for_pre_beta_stabilization": False,
        "ready_for_broader_testing": False,
        "needs_more_stabilization": True,
        "needs_public_surface_hardening": True,
        "public_surface_position": "internal-only",
        "broader_alpha_blockers": [
            "validation remains too dependent on one real X11+i3 host and simulated non-X11 environments",
            "no real Wayland-host validation pass exists yet",
            "migration validation remains representative rather than broad",
        ],
        "pre_beta_blockers": [
            "broader-alpha gates are not yet satisfied",
            "no real Wayland-host validation pass exists yet",
            "current package and diagnostics surfaces remain internal-only and repo-checkout dependent",
            "migration validation remains representative rather than broad",
        ],
        "public_beta_blockers": list(PUBLIC_BETA_BLOCKERS),
        "proposed_pre_beta_version": PROPOSED_PRE_BETA_VERSION,
        "proposed_pre_beta_status_label": PROPOSED_PRE_BETA_STATUS_LABEL,
        "proposed_pre_beta_tag_name": proposed_pre_beta_tag_name,
        "local_tag_name": local_tag_name,
        "local_tag_exists": tag_state["exists"],
        "local_tag_points_at_head": tag_state["points_at_head"],
        "local_tag_state": tag_state["state"],
        "local_tag_revision": tag_state["revision"],
        "latest_existing_local_alpha_tag": latest_existing_local_alpha_tag,
        "latest_existing_local_pre_beta_tag": latest_existing_local_pre_beta_tag,
        "current_build_kind": (
            "tagged-local-alpha-candidate"
            if tag_state["points_at_head"]
            else "untagged-post-alpha-hardening"
        ),
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


def latest_matching_tag(pattern: str) -> str | None:
    output = _git_output(["tag", "--list", pattern, "--sort=refname"])
    if output is None:
        return None
    tags = [line.strip() for line in output.splitlines() if line.strip()]
    if not tags:
        return None
    return tags[-1]


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


def describe_local_tag_state(tag_name: str) -> dict[str, Any]:
    head_revision = _git_output(["rev-parse", "HEAD"])
    if head_revision is None:
        return {
            "exists": None,
            "points_at_head": None,
            "revision": None,
            "state": "git-unavailable",
        }
    tag_revision = _git_output(["rev-list", "-n", "1", tag_name])
    if tag_revision is None:
        return {
            "exists": False,
            "points_at_head": False,
            "revision": None,
            "state": "missing",
        }
    return {
        "exists": True,
        "points_at_head": tag_revision == head_revision,
        "revision": tag_revision,
        "state": "current-head" if tag_revision == head_revision else "historical-other-commit",
    }
