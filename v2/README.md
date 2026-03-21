# RetroFX 2.x Implementation Scaffold

`v2/` is the future implementation root for RetroFX 2.x.
It is intentionally non-production at this stage.

Design truth stays in [`docs/v2/`](../docs/v2/README.md).
This tree exists so later prompts implement 2.x in the right places instead of expanding the 1.x shell layout.

## Current State

As of TWO-20:

- `v2/core/` contains an experimental stdlib-only Python scaffold for loading, validating, normalizing, and resolving 2.x profile documents
- `v2/tests/` contains isolated fixtures and tests for that scaffold
- `v2/targets/terminal/` contains the first real 2.x compiler family for terminal/TUI exports
- `v2/targets/wm/` now contains the second real 2.x compiler family for WM/theme-adjacent exports: `i3`, `sway`, and `waybar`
- `v2/targets/toolkit/` now contains session-local `fontconfig` output plus advisory GTK, Qt, icon-cursor, and desktop-style exports
- `v2/targets/x11/` now contains the first bounded X11 render family with shader, picom, runtime metadata, and display-policy outputs
- `v2/core/dev/compile-targets` writes deterministic dev-only artifacts under `v2/out/<profile-id>/`
- `v2/session/` now contains the first real session-planning slice: environment detection and capability-aware non-destructive planning
- `v2/core/dev/plan-session` previews what would be exported, degraded, skipped, or eventually applyable in the detected environment
- typography is now concretely resolved in the core scaffold and visible in both compile and plan previews
- display policy is now concretely resolved in the core scaffold and visible in both compile and plan previews
- `v2/packs/` now contains a real local pack manifest layer and curated built-in packs
- `v2/core/dev/list-packs` and `v2/core/dev/show-pack` inspect those packs without side effects
- the existing dev resolve, compile, and plan entrypoints can now resolve profiles from local packs via `--pack` and `--profile-id`
- `v2/compat/` now contains the first real 1.x compatibility and draft migration slice
- `v2/compat/dev/inspect-1x-profile` inspects supported 1.x profiles and can emit generated 2.x drafts under `v2/out/migrations/`
- `v2/session/install/` now contains the first real experimental bundle/install slice for 2.x
- `scripts/dev/retrofx-v2-bundle` now stages deterministic repo-local bundles under `v2/bundles/`
- `scripts/dev/retrofx-v2-install` and `retrofx-v2-uninstall` now manage that separate experimental install footprint
- `v2/session/apply/` now contains the first bounded experimental apply/off slice with current-state manifests, last-good state, and event logs
- `scripts/dev/retrofx-v2-apply`, `retrofx-v2-off`, and `retrofx-v2-status` now manage a bounded current activation inside the isolated `retrofx-v2-dev` footprint
- `v2/dev/` now provides a unified experimental branch surface for platform status, smoke flows, and top-level command dispatch
- `scripts/dev/retrofx-v2` now dispatches to the implemented 2.x developer workflows from one place
- public packaging, broad live session orchestration, and production command delegation still do not exist

Python is used only for the early 2.x internal scaffold because `tomllib` gives deterministic TOML parsing with no extra dependency burden.
This choice does not change the 1.x runtime or make Python the default user-facing path.

## Modules

- `core/`: normalization, resolution, capability filtering, and artifact planning
- `schema/`: schema contracts, validation helpers, and migration maps
- `theme/`: semantic theme and typography policy helpers
- `render/`: render policy and transform planning
- `dev/`: unified experimental developer dispatcher, status, and smoke helpers
- `session/`: planning, bounded apply/off state ownership, install-state ownership, and future repair orchestration
- `targets/`: target adapters and backend-specific emission
- `packs/`: pack metadata, family definitions, and pack-local assets
- `compat/`: legacy profile intake, migration helpers, and future dispatcher shims
- `tests/`: 2.x-only tests and fixtures

## Rules

- Do not treat this tree as a user-facing platform yet.
- Do not add fake CLI commands here just to make the scaffold feel active.
- Do not port 1.x shell code into `v2/` without an explicit migration prompt.
- Implement against the contracts in `docs/v2/`, especially `MODULE_BOUNDARIES.md` and `IMPLEMENTATION_SEQUENCE.md`.
