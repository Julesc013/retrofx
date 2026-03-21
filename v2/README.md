# RetroFX 2.x Implementation Scaffold

`v2/` is the future implementation root for RetroFX 2.x.
It is intentionally non-production at this stage.

Design truth stays in [`docs/v2/`](../docs/v2/README.md).
This tree exists so later prompts implement 2.x in the right places instead of expanding the 1.x shell layout.

## Current State

As of TWO-11:

- `v2/core/` contains an experimental stdlib-only Python scaffold for loading, validating, normalizing, and resolving 2.x profile documents
- `v2/tests/` contains isolated fixtures and tests for that scaffold
- `v2/targets/terminal/` contains the first real 2.x compiler family for terminal/TUI exports
- `v2/targets/wm/` now contains the second real 2.x compiler family for WM/theme-adjacent exports: `i3`, `sway`, and `waybar`
- `v2/core/dev/compile-targets` writes deterministic dev-only artifacts under `v2/out/<profile-id>/`
- `v2/session/` now contains the first real session-planning slice: environment detection and capability-aware non-destructive planning
- `v2/core/dev/plan-session` previews what would be exported, degraded, skipped, or eventually applyable in the detected environment
- live session orchestration and production command delegation still do not exist

Python is used only for the early 2.x internal scaffold because `tomllib` gives deterministic TOML parsing with no extra dependency burden.
This choice does not change the 1.x runtime or make Python the default user-facing path.

## Modules

- `core/`: normalization, resolution, capability filtering, and artifact planning
- `schema/`: schema contracts, validation helpers, and migration maps
- `theme/`: semantic theme and typography policy helpers
- `render/`: render policy and transform planning
- `session/`: apply, export, install, off, and repair orchestration
- `targets/`: target adapters and backend-specific emission
- `packs/`: pack metadata, family definitions, and pack-local assets
- `compat/`: legacy bridges, upgrade tools, and future dispatcher shims
- `tests/`: 2.x-only tests and fixtures

## Rules

- Do not treat this tree as a user-facing platform yet.
- Do not add fake CLI commands here just to make the scaffold feel active.
- Do not port 1.x shell code into `v2/` without an explicit migration prompt.
- Implement against the contracts in `docs/v2/`, especially `MODULE_BOUNDARIES.md` and `IMPLEMENTATION_SEQUENCE.md`.
