# RetroFX 2.x Implementation Scaffold

`v2/` is the future implementation root for RetroFX 2.x.
It is intentionally non-functional at this stage.

Design truth stays in [`docs/v2/`](../docs/v2/README.md).
This tree exists so later prompts implement 2.x in the right places instead of expanding the 1.x shell layout.

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

