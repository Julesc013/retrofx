"""Shared experimental release metadata for the current RetroFX 2.x branch."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from v2.session.install.layout import INSTALL_NAME

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"
DEFAULT_INTERNAL_ALPHA_PACKAGE_ROOT = REPO_ROOT / "v2" / "releases" / "internal-alpha"
DEFAULT_TECHNICAL_BETA_PACKAGE_ROOT = REPO_ROOT / "v2" / "releases" / "technical-beta"

EXPERIMENTAL_STATUS_SCHEMA = "retrofx.experimental-status/v2alpha1"
INTERNAL_ALPHA_PACKAGE_SCHEMA = "retrofx.internal-alpha-package/v2alpha1"
TECHNICAL_BETA_PACKAGE_SCHEMA = "retrofx.technical-beta-package/v2alpha1"

STATUS_LADDER = (
    "experimental",
    "internal-alpha",
    "controlled-alpha",
    "pre-beta",
    "technical-beta",
    "public-beta",
    "stable",
)

CURRENT_EXPERIMENTAL_VERSION = "2.0.0-alpha.internal.2"
CURRENT_STATUS_LABEL = "internal-alpha"
CURRENT_PROMPT = "TWO-32"
CURRENT_DISTRIBUTION_SCOPE = "internal-non-public"
CURRENT_COHORT = "controlled-internal"
PROPOSED_PRE_BETA_VERSION = "2.0.0-prebeta.internal.1"
PROPOSED_PRE_BETA_STATUS_LABEL = "pre-beta"
PROPOSED_TECHNICAL_BETA_VERSION = "2.0.0-techbeta.1"
PROPOSED_TECHNICAL_BETA_STATUS_LABEL = "technical-beta"
TECHNICAL_BETA_SUPPORT_MATRIX = {
    "validated_supported": [
        {
            "environment": "x11+i3-like",
            "support_class": "supported",
            "flows": [
                "status",
                "resolve",
                "plan",
                "compile",
                "bundle",
                "install",
                "uninstall",
                "diagnostics",
                "apply",
                "off",
                "smoke",
            ],
            "notes": "Validated on one real X11 plus i3 host with bounded, user-local workflows only.",
        },
        {
            "environment": "temp-home-install",
            "support_class": "supported",
            "flows": ["install", "uninstall", "diagnostics"],
            "notes": "User-local install and cleanup remain bounded to the `retrofx-v2-dev` footprint.",
        },
    ],
    "degraded_export_only": [
        {
            "environment": "wayland+sway-like",
            "support_class": "degraded-export-only",
            "flows": ["status", "resolve", "plan", "compile", "bundle", "diagnostics", "smoke"],
            "notes": "Planning and compile flows are valid here, but live apply and X11 probe behavior are outside the technical-beta support matrix.",
        },
    ],
    "unsupported": [
        {
            "environment": "wayland+gnome-or-plasma-like",
            "support_class": "unsupported-for-technical-beta",
            "flows": ["apply", "preview-x11"],
            "notes": "Use export-oriented planning and compile only; live runtime ownership is out of scope.",
        },
        {
            "environment": "migration-broad-assurance",
            "support_class": "internal-only",
            "flows": ["migrate inspect-1x"],
            "notes": "Migration remains representative rather than broad and is not part of the limited technical-beta support promise.",
        },
    ],
}
TECHNICAL_BETA_LIMITATIONS = [
    "The limited technical beta is for advanced testers only and does not replace the 1.x runtime or CLI.",
    "Supported live runtime behavior is intentionally narrow and bounded to user-local, reversible workflows.",
    "Wayland render remains unsupported for live ownership.",
    "Toolkit exports remain advisory and do not imply live desktop ownership.",
    "The explicit bounded X11 picom probe remains internal-only and is not part of the public technical-beta contract.",
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
    proposed_technical_beta_tag_name = local_tag_name_for_version(PROPOSED_TECHNICAL_BETA_VERSION)
    technical_beta_tag_state = describe_local_tag_state(proposed_technical_beta_tag_name)
    latest_existing_local_technical_beta_tag = latest_matching_tag("v2.0.0-techbeta.*")

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
        "ready_for_controlled_external_alpha": True,
        "ready_for_non_public_pre_beta": False,
        "ready_for_local_pre_beta_tag_candidate": False,
        "pre_beta_candidate_ready": False,
        "ready_for_limited_public_technical_beta": True,
        "ready_for_public_technical_beta_candidate": True,
        "ready_for_pre_beta_stabilization": False,
        "ready_for_broader_testing": False,
        "needs_more_stabilization": True,
        "needs_public_surface_hardening": False,
        "public_surface_position": "limited-public-technical-beta-candidate",
        "broader_alpha_blockers": [
            "validation remains too dependent on one real X11+i3 host and simulated non-X11 environments",
            "the limited technical beta support matrix stays intentionally narrower than broader-alpha ambitions",
            "migration validation remains representative rather than broad",
        ],
        "pre_beta_blockers": [
            "broader-alpha gates are not yet satisfied",
            "the limited technical beta candidate intentionally skips the blocked non-public pre-beta path",
            "current broader-alpha and pre-beta gates remain stricter than the narrowed technical-beta support matrix",
            "migration validation remains representative rather than broad",
        ],
        "public_beta_blockers": [],
        "proposed_pre_beta_version": PROPOSED_PRE_BETA_VERSION,
        "proposed_pre_beta_status_label": PROPOSED_PRE_BETA_STATUS_LABEL,
        "proposed_pre_beta_tag_name": proposed_pre_beta_tag_name,
        "proposed_technical_beta_version": PROPOSED_TECHNICAL_BETA_VERSION,
        "proposed_technical_beta_status_label": PROPOSED_TECHNICAL_BETA_STATUS_LABEL,
        "proposed_technical_beta_tag_name": proposed_technical_beta_tag_name,
        "technical_beta_candidate_tag_name": proposed_technical_beta_tag_name,
        "technical_beta_candidate_tag_exists": technical_beta_tag_state["exists"],
        "technical_beta_candidate_tag_points_at_head": technical_beta_tag_state["points_at_head"],
        "technical_beta_candidate_tag_state": technical_beta_tag_state["state"],
        "technical_beta_candidate_tag_revision": technical_beta_tag_state["revision"],
        "latest_existing_local_technical_beta_tag": latest_existing_local_technical_beta_tag,
        "technical_beta_support_matrix": TECHNICAL_BETA_SUPPORT_MATRIX,
        "technical_beta_limitations": list(TECHNICAL_BETA_LIMITATIONS),
        "local_tag_name": local_tag_name,
        "local_tag_exists": tag_state["exists"],
        "local_tag_points_at_head": tag_state["points_at_head"],
        "local_tag_state": tag_state["state"],
        "local_tag_revision": tag_state["revision"],
        "latest_existing_local_alpha_tag": latest_existing_local_alpha_tag,
        "latest_existing_local_pre_beta_tag": latest_existing_local_pre_beta_tag,
        "current_build_kind": (
            "tagged-local-technical-beta-candidate"
            if technical_beta_tag_state["points_at_head"]
            else (
                "tagged-local-alpha-candidate"
                if tag_state["points_at_head"]
                else "technical-beta-candidate-prep"
            )
        ),
        "source_revision": _git_output(["rev-parse", "HEAD"]),
        "source_branch": _git_output(["rev-parse", "--abbrev-ref", "HEAD"]),
        "source_tree": str(REPO_ROOT),
        "source_control": source_control,
        "working_tree_clean": source_control["working_tree_clean"],
        "unified_entrypoint": str(UNIFIED_ENTRYPOINT),
    }


def build_technical_beta_candidate_metadata() -> dict[str, Any]:
    base = build_experimental_release_metadata()
    tag_name = local_tag_name_for_version(PROPOSED_TECHNICAL_BETA_VERSION)
    tag_state = describe_local_tag_state(tag_name)
    latest_existing_local_technical_beta_tag = latest_matching_tag("v2.0.0-techbeta.*")

    candidate = dict(base)
    candidate.update(
        {
            "version": PROPOSED_TECHNICAL_BETA_VERSION,
            "status_label": PROPOSED_TECHNICAL_BETA_STATUS_LABEL,
            "distribution_scope": "limited-public-technical-beta",
            "cohort": "advanced-external-testers",
            "ready_for_internal_alpha_continuation": True,
            "ready_for_controlled_internal_alpha": True,
            "ready_for_controlled_external_alpha": True,
            "ready_for_limited_public_technical_beta": True,
            "ready_for_public_technical_beta_candidate": True,
            "needs_public_surface_hardening": False,
            "public_surface_position": "limited-public-technical-beta-candidate",
            "public_beta_blockers": [],
            "technical_beta_support_matrix": TECHNICAL_BETA_SUPPORT_MATRIX,
            "technical_beta_limitations": list(TECHNICAL_BETA_LIMITATIONS),
            "local_tag_name": tag_name,
            "local_tag_exists": tag_state["exists"],
            "local_tag_points_at_head": tag_state["points_at_head"],
            "local_tag_state": tag_state["state"],
            "local_tag_revision": tag_state["revision"],
            "latest_existing_local_technical_beta_tag": latest_existing_local_technical_beta_tag,
            "current_build_kind": (
                "tagged-local-technical-beta-candidate"
                if tag_state["points_at_head"]
                else "untagged-technical-beta-candidate"
            ),
        }
    )
    return candidate


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
