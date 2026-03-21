# RetroFX 2.x Repository Layout

This document defines where 2.x implementation work belongs in the repository.
It exists to stop 2.x from accreting inside the 1.x shell layout.

## Chosen Root

RetroFX 2.x implementation work lives under `v2/`.

`v2/` was chosen instead of `platform/` because:

- it aligns directly with the existing `docs/v2/` design namespace
- it makes the dual-track repo state obvious
- it avoids implying that the 1.x line is no longer part of the repository

## Top-Level Repository Zones

| Path | Primary Owner | Role |
| --- | --- | --- |
| `scripts/retrofx`, `backends/`, `templates/`, `active/`, `state/` | 1.x | Working stable shell implementation and current runtime state model. |
| `profiles/`, `profiles/packs/` | 1.x | Current 1.x profile and pack data. |
| `tests/` | 1.x | Current shell-oriented regression coverage. |
| `docs/` outside `docs/v2/` | 1.x | Current product, install, support, and maintenance truth for the stable line. |
| `docs/v2/` | 2.x design | Product, schema, architecture, layout, and implementation-guardrail documents for 2.x. |
| `v2/` | 2.x implementation scaffold | Future platform code, data, tests, and compatibility layers. |

## Scaffolded 2.x Tree

The repository now reserves this implementation root:

```text
v2/
  README.md
  core/
    README.md
  schema/
    README.md
  theme/
    README.md
  render/
    README.md
  session/
    README.md
  targets/
    README.md
  packs/
    README.md
  compat/
    README.md
  tests/
    README.md
```

This tree is intentionally small.
It is structural scaffolding only.

## Why Docs Stay In `docs/v2/`

The repository does not create a second documentation tree under `v2/docs/`.
Design truth stays under `docs/v2/`.

That separation is intentional:

- `docs/v2/` is the architectural constitution
- `v2/` is where later prompts may implement against that constitution

## Expected Future Growth

Later prompts may add deeper structure inside the scaffold, for example:

- `v2/targets/terminal/`
- `v2/targets/tui/`
- `v2/targets/x11/`
- `v2/targets/wayland/`
- `v2/targets/wm/`
- `v2/targets/toolkit/`
- `v2/compat/migration/`
- `v2/compat/dispatch/`
- `v2/packs/catalog/`
- `v2/tests/unit/`
- `v2/tests/integration/`

Those deeper trees should only appear when a later prompt implements the corresponding contracts.

## Placement Rules

- New 2.x implementation code goes under `v2/`, not under `scripts/`, `backends/`, or `templates/`.
- New 2.x design truth goes under `docs/v2/`, not inside scattered inline comments or ad hoc notes.
- 1.x code is not moved into `v2/` unless a later prompt is explicitly about compatibility shims or controlled migration.
- Target compiler code belongs under `v2/targets/`, not inside `v2/core/`.
- Session orchestration code belongs under `v2/session/`, not inside `v2/targets/`.
- Compatibility and migration bridges belong under `v2/compat/`, not inside the 1.x shell tree.
- 2.x pack data and metadata belong under `v2/packs/`; 1.x pack TOMLs remain in `profiles/packs/`.

## What This Layout Forbids

- growing a second 2.x planner inside `scripts/retrofx`
- treating `backends/` as the future home of target adapters
- mixing 1.x runtime state handling with unfinished 2.x planning code
- scattering migration helpers across unrelated directories
- duplicating product truth between `docs/v2/` and `v2/`

