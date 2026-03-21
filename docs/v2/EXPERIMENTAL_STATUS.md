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

### `technical-beta`

Meaning:

- narrow outside circulation to technically literate testers is acceptable
- support matrix, cleanup, and diagnostics expectations are explicit
- the surface stays smaller than the broader internal developer toolchain

### `public-beta`

Meaning:

- intentionally not current
- would require a separate branch decision and public-release process

### `stable`

Meaning:

- intentionally future-only
- would require replacement-level confidence that does not exist today

## Current Truth

As of TWO-32:

- current branch status label: `internal-alpha`
- current branch version: `2.0.0-alpha.internal.2`
- current build kind: technical-beta candidate prep
- reserved proposed pre-beta candidate version: `2.0.0-prebeta.internal.1`
- approved limited technical-beta candidate version: `2.0.0-techbeta.1`
- approved limited technical-beta candidate status label: `technical-beta`
- readiness: narrow controlled internal alpha continuation is acceptable
- latest historical local alpha candidate: `2.0.0-alpha.internal.1`
- historical local alpha tag: `v2.0.0-alpha.internal.1`
- broader alpha: not ready yet
- controlled external alpha: ready only through the narrowed technical-beta surface
- non-public pre-beta: not ready yet
- limited public technical beta: ready
- local technical-beta tag candidate: ready
- local pre-beta tag candidate: not ready yet
- pre-beta candidate ready: no

That distinction is deliberate.
The broader internal developer surface remains internal-only.
The narrower copied-toolchain `technical-beta` candidate is now acceptable for advanced testers without pretending that RetroFX 2.x has crossed into general-public beta or stable territory.
