"""Consolidated platform status reporting for the experimental RetroFX 2.x branch."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from v2.core.pipeline import IMPLEMENTATION_INFO as CORE_IMPLEMENTATION_INFO
from v2.packs import discover_packs
from v2.session.apply import describe_current_activation
from v2.session.environment import detect_environment
from v2.targets import list_target_families, list_targets

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_ENTRYPOINT = REPO_ROOT / "scripts" / "dev" / "retrofx-v2"

COMMAND_SUMMARY = [
    {
        "command": "status",
        "category": "inspect",
        "implemented": True,
        "description": "Show the current environment, implemented 2.x surface, and bounded current-state status.",
    },
    {
        "command": "resolve",
        "category": "core",
        "implemented": True,
        "description": "Load, validate, normalize, and resolve a 2.x profile or pack profile.",
    },
    {
        "command": "plan",
        "category": "session",
        "implemented": True,
        "description": "Preview capability-aware planning for the current environment without applying anything.",
    },
    {
        "command": "compile",
        "category": "targets",
        "implemented": True,
        "description": "Compile the implemented 2.x target families into deterministic export artifacts.",
    },
    {
        "command": "apply",
        "category": "session",
        "implemented": True,
        "description": "Run the bounded experimental 2.x apply path under the isolated user-local footprint.",
    },
    {
        "command": "off",
        "category": "session",
        "implemented": True,
        "description": "Clear the bounded experimental 2.x current activation without touching 1.x.",
    },
    {
        "command": "preview-x11",
        "category": "render",
        "implemented": True,
        "description": "Stage bounded X11 render artifacts and optionally run an explicit short-lived picom probe.",
    },
    {
        "command": "packs list",
        "category": "packs",
        "implemented": True,
        "description": "List curated local 2.x packs.",
    },
    {
        "command": "packs show",
        "category": "packs",
        "implemented": True,
        "description": "Inspect one local 2.x pack manifest.",
    },
    {
        "command": "migrate inspect-1x",
        "category": "compat",
        "implemented": True,
        "description": "Inspect a 1.x profile and emit a deterministic migration report or draft.",
    },
    {
        "command": "bundle",
        "category": "install",
        "implemented": True,
        "description": "Build a deterministic experimental 2.x bundle.",
    },
    {
        "command": "install",
        "category": "install",
        "implemented": True,
        "description": "Install one generated 2.x bundle into the isolated user-local footprint.",
    },
    {
        "command": "uninstall",
        "category": "install",
        "implemented": True,
        "description": "Remove one installed experimental 2.x bundle.",
    },
    {
        "command": "smoke",
        "category": "inspect",
        "implemented": True,
        "description": "Run the safe developer smoke flow: resolve, plan, compile, and optionally bounded apply.",
    },
]

IMPLEMENTED_STATUS_MATRIX = [
    {
        "area": "schema validation",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Stdlib-only TOML load plus raw and normalized validation are real in `v2/core/validation/`.",
    },
    {
        "area": "normalization",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Defaults, canonicalization, and semantic derivation are real in `v2/core/normalization/`.",
    },
    {
        "area": "resolved profile",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Resolved identity, theme, typography, render, display, and session policy are real in `v2/core/resolution/`.",
    },
    {
        "area": "terminal targets",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Xresources, Alacritty, Kitty, tmux, and Vim outputs are real and deterministic.",
    },
    {
        "area": "WM targets",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "i3, sway, and waybar exports are real config or style artifacts.",
    },
    {
        "area": "toolkit exports",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "GTK, Qt, icon-cursor, desktop-style, and fontconfig outputs are export-oriented and advisory.",
    },
    {
        "area": "typography outputs",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Resolved typography roles and session-local fontconfig or terminal font outputs are real.",
    },
    {
        "area": "display policy outputs",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Display policy is concrete, planned, exportable, and consumed by the bounded X11 render slice.",
    },
    {
        "area": "pack system",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Local pack manifests, curated packs, and pack-aware resolution are real; no network registry exists.",
    },
    {
        "area": "migration tooling",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "1.x profile inspection and draft 2.x migration output are real; full runtime compatibility is not.",
    },
    {
        "area": "install or bundle flow",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Deterministic bundles and isolated user-local install, uninstall, and status exist under `retrofx-v2-dev`.",
    },
    {
        "area": "X11 render or compiler",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Shader, picom, runtime metadata, and bounded preview are real for X11 only.",
    },
    {
        "area": "session planning",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "Environment detection and capability-aware planning are real and non-destructive.",
    },
    {
        "area": "bounded apply or off",
        "implemented": True,
        "experimental": True,
        "planned": False,
        "notes": "The TWO-19 current-state activation path is real but limited to 2.x-owned staging plus explicit X11 probe use.",
    },
    {
        "area": "global desktop integration",
        "implemented": False,
        "experimental": False,
        "planned": True,
        "notes": "Live GNOME, Plasma, Xfce, and cross-DE settings mutation remain future work.",
    },
    {
        "area": "live Wayland render",
        "implemented": False,
        "experimental": False,
        "planned": True,
        "notes": "Wayland render remains degraded or export-only; no compositor-owned live path exists.",
    },
    {
        "area": "full compatibility mode",
        "implemented": False,
        "experimental": False,
        "planned": True,
        "notes": "Migration exists, but 1.x runtime compatibility or takeover is not implemented.",
    },
]

PLATFORM_IMPLEMENTATION_INFO = {
    "status": "experimental-dev-only",
    "prompt": "TWO-20",
    "surface": "unified-dev-platform",
    "entrypoint": str(UNIFIED_ENTRYPOINT),
    "implemented_targets": list_targets(),
    "families": list_target_families(),
    "not_implemented": [
        "production CLI takeover",
        "release-ready stability guarantees",
        "global desktop ownership",
        "live Wayland render",
        "full 1.x runtime compatibility mode",
    ],
}


def build_platform_status(
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | Path | None = None,
    stdin_isatty: bool | None = None,
    path_lookup: Any | None = None,
) -> dict[str, Any]:
    environment = detect_environment(env=env, cwd=cwd, stdin_isatty=stdin_isatty, path_lookup=path_lookup)
    activation_status = describe_current_activation(env=env, cwd=cwd)
    packs = discover_packs()

    return {
        "ok": True,
        "stage": "platform-status",
        "implementation": PLATFORM_IMPLEMENTATION_INFO,
        "developer_start_here": {
            "entrypoint": str(UNIFIED_ENTRYPOINT),
            "first_commands": [
                "scripts/dev/retrofx-v2 status",
                "scripts/dev/retrofx-v2 smoke v2/tests/fixtures/strict-green-crt.toml",
                "scripts/dev/retrofx-v2 smoke --pack modern-minimal --profile-id warm-night",
            ],
        },
        "environment": environment,
        "dev_surface": {
            "unified_entrypoint": str(UNIFIED_ENTRYPOINT),
            "command_count": len(COMMAND_SUMMARY),
            "commands": COMMAND_SUMMARY,
            "legacy_wrappers": [
                "scripts/dev/retrofx-v2-apply",
                "scripts/dev/retrofx-v2-bundle",
                "scripts/dev/retrofx-v2-install",
                "scripts/dev/retrofx-v2-off",
                "scripts/dev/retrofx-v2-preview-x11",
                "scripts/dev/retrofx-v2-status",
                "scripts/dev/retrofx-v2-uninstall",
            ],
        },
        "implemented_surface": {
            "core_pipeline": {
                "implemented_stages": CORE_IMPLEMENTATION_INFO["implemented_stages"],
                "language": CORE_IMPLEMENTATION_INFO["language"],
            },
            "target_families": list_target_families(),
            "implemented_target_count": len(list_targets()),
            "packs": {
                "pack_count": len(packs),
                "profile_count": sum(len(pack["profiles"]) for pack in packs),
                "pack_ids": [pack["id"] for pack in packs],
            },
            "current_activation": activation_status,
        },
        "implemented_status_matrix": IMPLEMENTED_STATUS_MATRIX,
        "limitations": [
            "2.x remains experimental and dev-only; 1.x is still the production line.",
            "Not every compiled target can be live-applied yet.",
            "Toolkit exports are advisory; live desktop mutation remains future work.",
            "Wayland render remains unsupported for live runtime ownership.",
            "Compatibility work is inspection and draft migration only, not runtime parity.",
        ],
        "next_focus": {
            "phase": "controlled-stabilization",
            "doc": str(REPO_ROOT / "docs" / "v2" / "STABILIZATION_PLAN.md"),
            "goals": [
                "real-world test passes against the implemented dev surface",
                "interface hardening and cleanup instead of new feature sprawl",
                "documentation truth pass across the existing branch surface",
                "bounded runtime validation under temp or isolated homes",
            ],
        },
        "note": "This report describes the implemented 2.x experimental platform as it exists now. It is not a production readiness claim.",
    }
