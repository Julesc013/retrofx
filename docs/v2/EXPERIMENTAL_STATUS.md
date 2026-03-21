# RetroFX 2.x Experimental Status

This document defines the meaning of the current 2.x experimental status labels.

These labels do not apply to 1.x.
They do not imply public release readiness.

## Status Ladder

### `experimental`

Meaning:

- implemented enough to inspect locally
- not yet ready for organized circulation
- interface and docs may still churn significantly

### `internal-alpha`

Meaning:

- usable by the core development team and a narrow internal tester cohort
- packaging, install, and validation flow exist
- behavior is still explicitly experimental
- regressions and environment gaps are still expected

Current 2.x branch status:

- `internal-alpha`

### `controlled-alpha`

Meaning:

- broader but still non-public alpha circulation
- multi-host validation is materially better
- operational instructions are clearer
- blocker rate is lower than current internal-alpha expectations

Current 2.x branch status:

- not yet labeled `controlled-alpha`

### `pre-beta`

Meaning:

- feature growth has mostly stopped
- validation and interface hardening dominate the work
- broader internal confidence exists

### `public-beta`

Meaning:

- intentionally not current
- would require a separate branch decision and public-release process

### `stable`

Meaning:

- intentionally future-only
- would require replacement-level confidence that does not exist today

## Current Truth

As of TWO-26:

- current branch status label: `internal-alpha`
- readiness: narrow controlled internal alpha continuation is acceptable
- local alpha candidate: acceptable for local or internal-only use after the checklist pass
- broader testing: not ready yet

That distinction is deliberate.
The branch is ready for limited internal circulation without pretending it has crossed into public or broadly distributed alpha territory.
