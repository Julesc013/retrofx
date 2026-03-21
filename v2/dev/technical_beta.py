"""Limited technical-beta surface helpers for the RetroFX 2.x branch."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.session.environment import detect_environment

from .release import (
    PROPOSED_TECHNICAL_BETA_VERSION,
    TECHNICAL_BETA_LIMITATIONS,
    TECHNICAL_BETA_SUPPORT_MATRIX,
    build_technical_beta_candidate_metadata,
)
from .status import build_platform_status

REPO_ROOT = Path(__file__).resolve().parents[2]
TECHNICAL_BETA_ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2-techbeta"

TECHNICAL_BETA_COMMAND_SUMMARY = [
    {
        "command": "status",
        "category": "inspect",
        "implemented": True,
        "description": "Show the limited technical-beta status report, support matrix, and bounded current-state status.",
    },
    {
        "command": "resolve",
        "category": "core",
        "implemented": True,
        "description": "Resolve one 2.x profile or curated pack profile through the implemented pipeline.",
    },
    {
        "command": "plan",
        "category": "session",
        "implemented": True,
        "description": "Preview capability-aware planning without mutating the live session.",
    },
    {
        "command": "compile",
        "category": "targets",
        "implemented": True,
        "description": "Compile deterministic target artifacts for terminal, WM, toolkit-export, and X11 families.",
    },
    {
        "command": "bundle",
        "category": "install",
        "implemented": True,
        "description": "Build one deterministic bundle for the supported technical-beta surface.",
    },
    {
        "command": "install",
        "category": "install",
        "implemented": True,
        "description": "Install one generated bundle into the bounded `retrofx-v2-dev` footprint.",
    },
    {
        "command": "uninstall",
        "category": "install",
        "implemented": True,
        "description": "Remove one installed bundle from the bounded `retrofx-v2-dev` footprint.",
    },
    {
        "command": "diagnostics",
        "category": "inspect",
        "implemented": True,
        "description": "Capture a local diagnostics directory suitable for technical-beta bug reports.",
    },
    {
        "command": "apply",
        "category": "session",
        "implemented": True,
        "description": "Run the bounded apply flow on supported X11 environments only. Wayland remains compile or export-oriented only.",
    },
    {
        "command": "off",
        "category": "session",
        "implemented": True,
        "description": "Clear the bounded current activation without touching 1.x or uninstalling bundles.",
    },
    {
        "command": "packs list",
        "category": "packs",
        "implemented": True,
        "description": "List curated built-in packs shipped with the copied toolchain.",
    },
    {
        "command": "packs show",
        "category": "packs",
        "implemented": True,
        "description": "Inspect one curated built-in pack manifest.",
    },
    {
        "command": "smoke",
        "category": "inspect",
        "implemented": True,
        "description": "Run the supported smoke path: resolve, plan, compile, and optionally bounded apply on X11.",
    },
]

TECHNICAL_BETA_IMPLEMENTATION_INFO = {
    "status": "experimental-limited-technical-beta",
    "prompt": "TWO-32",
    "surface": "limited-technical-beta-candidate-surface",
    "entrypoint": str(TECHNICAL_BETA_ENTRYPOINT),
    "validated_primary_environment": "x11+i3-like",
    "not_exposed": [
        "package-alpha",
        "preview-x11",
        "migrate inspect-1x",
    ],
}


def build_technical_beta_status(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Any | None = None,
) -> dict[str, Any]:
    payload = build_platform_status(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    release_status = build_technical_beta_candidate_metadata()

    payload["stage"] = "technical-beta-status"
    payload["implementation"] = TECHNICAL_BETA_IMPLEMENTATION_INFO
    payload["release_status"] = release_status
    payload["developer_start_here"] = {
        "entrypoint": str(TECHNICAL_BETA_ENTRYPOINT),
        "first_commands": [
            "retrofx-v2-techbeta status",
            "retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night",
            "retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --label first-pass",
        ],
    }
    payload["environment"] = environment
    payload["dev_surface"] = {
        "entrypoint": str(TECHNICAL_BETA_ENTRYPOINT),
        "command_count": len(TECHNICAL_BETA_COMMAND_SUMMARY),
        "commands": TECHNICAL_BETA_COMMAND_SUMMARY,
        "support_matrix": TECHNICAL_BETA_SUPPORT_MATRIX,
        "hidden_internal_commands": [
            "package-alpha",
            "preview-x11",
            "migrate inspect-1x",
        ],
    }
    payload["limitations"] = [
        "This limited technical beta is for advanced testers only; 1.x remains the production line.",
        *TECHNICAL_BETA_LIMITATIONS,
        "Wayland planning and compile remain useful for export-oriented validation, but they are not part of the supported live technical-beta runtime path.",
        "Migration inspection remains available only on the internal developer surface and is not part of the limited technical-beta promise.",
    ]
    payload["technical_beta_scope"] = TECHNICAL_BETA_SUPPORT_MATRIX
    payload["next_focus"] = {
        "phase": "limited-public-technical-beta-candidate",
        "doc": str(REPO_ROOT / "docs" / "v2" / "TECHNICAL_BETA_CANDIDATE_NOTES.md"),
        "checklist": str(REPO_ROOT / "docs" / "v2" / "TECHNICAL_BETA_RELEASE_CHECKLIST.md"),
        "goals": [
            "keep the externally visible surface limited to the documented advanced-tester subset",
            "validate candidate packages on real X11+i3-like hosts and temp-home installs",
            "treat Wayland and migration breadth as explicitly out of scope for this limited technical-beta line",
        ],
    }
    payload["note"] = (
        "This report describes the limited public technical-beta candidate surface only. "
        "The broader internal developer surface remains available separately and includes commands that are intentionally not part of the public-facing support promise."
    )
    return payload


def is_supported_technical_beta_apply_environment(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Any | None = None,
) -> tuple[bool, dict[str, Any]]:
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    supported = environment["session_type"] == "x11"
    return supported, environment


def technical_beta_apply_environment_error(environment: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ok": False,
        "stage": "technical-beta-apply-gate",
        "implementation": TECHNICAL_BETA_IMPLEMENTATION_INFO,
        "release_status": build_technical_beta_candidate_metadata(),
        "environment": environment,
        "errors": [
            {
                "severity": "error",
                "code": "technical-beta-unsupported-apply-environment",
                "message": (
                    "The limited technical beta supports bounded `apply` only on X11-oriented environments. "
                    "Use resolve, plan, compile, bundle, install, uninstall, and diagnostics on unsupported environments."
                ),
            }
        ],
        "warnings": [
            "Wayland and other non-X11 environments remain export-oriented validation contexts only for the limited technical-beta line."
        ],
        "note": "This is a support-matrix gate, not a compiler failure.",
    }


def technical_beta_candidate_summary_text(package_path: str) -> str:
    return "\n".join(
        [
            "RetroFX 2.x Limited Technical Beta Candidate",
            f"candidate.version: {PROPOSED_TECHNICAL_BETA_VERSION}",
            "candidate.status: technical-beta",
            f"package.path: {package_path}",
            "validated.primary.environment: x11+i3-like",
            "degraded.environment: wayland+sway-like compile/export-only",
            "unsupported.for.candidate: gnome/plasma wayland live runtime, broad migration assurance, global desktop ownership",
        ]
    )
