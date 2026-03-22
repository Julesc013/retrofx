# RetroFX 2.x Experimental Status

This document defines the 2.x status ladder and the current branch position.

These labels do not apply to `1.x`.
They do not imply public release readiness.

## Status Ladder

### `experimental`

- implemented enough to inspect locally
- not yet ready for organized circulation
- interfaces and docs may still churn significantly

### `internal-alpha`

- usable by the core development team and a narrow internal cohort
- packaging, install, and validation flow exist
- behavior is still explicitly experimental
- regressions and environment gaps are still expected

### `controlled-alpha`

- broader but still non-public alpha circulation
- multi-host validation is materially better
- operational instructions are clearer
- blocker rate is lower than internal-alpha expectations

### `pre-beta`

- feature growth has mostly stopped
- validation and interface hardening dominate the work
- broader internal confidence exists

### `technical-beta`

- narrow outside circulation to technically literate testers is acceptable
- support matrix, cleanup, and diagnostics expectations are explicit
- the exposed surface stays smaller than the broader internal developer toolchain

### `public-beta`

- intentionally future-only for now
- would require a separate publication decision and broader support obligations

### `stable`

- intentionally future-only
- would require production-line confidence that does not exist for 2.x

## Current Line Truth

As of the current `main` branch state:

- production line: `1.x`
- broader internal 2.x developer-line version on `main`: `2.0.0-alpha.internal.2`
- broader internal 2.x status label on `main`: `internal-alpha`
- limited technical-beta candidate version: `2.0.0-techbeta.1`
- limited technical-beta candidate status label: `technical-beta`
- the latest local technical-beta tag is a candidate snapshot; current `main` may be ahead of it
- reserved pre-beta version: `2.0.0-prebeta.internal.1`

Current readiness position:

- continued internal-alpha work: yes
- limited public technical beta: yes
- continued limited technical-beta circulation: yes
- broader beta stabilization: no
- non-public pre-beta: no
- general public beta: no
- stable: no

## How To Read That Correctly

The current repo does not have one single 2.x status identity.

It has:

- a broader internal developer surface that still carries the internal developer-line identity
- a narrower outside-facing candidate surface that carries the technical-beta identity
- historical candidate tags that record narrower outside-facing snapshots without implying that every later `main` commit is the same candidate

That distinction is deliberate.
It allows outside advanced-tester circulation without pretending that the whole broader internal platform has crossed the same maturity gate.

## What Is Approved Today

Approved:

- internal development and bounded internal-alpha workflows
- copied-toolchain technical-beta candidate workflow for advanced testers
- structured diagnostics-backed technical-beta circulation

Not approved:

- broader beta stabilization
- live Wayland ownership
- broad migration assurance
- 2.x takeover of the `1.x` production CLI
- general public beta or stable-release language
