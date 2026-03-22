# RetroFX 2.x Current Execution Baseline

This document records what was actually present on the merged `main` branch during the rapid technical-beta execution pass on 2026-03-22.

It is intentionally factual.
It does not restate older branch-era plans as if they were freshly verified.

## Evidence Root

- `v2/releases/reports/technical-beta-exec-20260322-072746Z`

That report root contains:

- command stdout, stderr, and exit-code captures
- diagnostics bundles for the rapid execution cycle
- temp-HOME install or apply evidence
- bundle or package logs where applicable

## Current Visible Surfaces

### Internal developer surface

Entrypoint:

- `scripts/dev/retrofx-v2`

Current surface includes:

- `status`
- `resolve`
- `plan`
- `compile`
- `bundle`
- `install`
- `uninstall`
- `package-alpha`
- `package-technical-beta`
- `diagnostics`
- `apply`
- `off`
- `preview-x11`
- `migrate inspect-1x`
- `packs`
- `smoke`

### Narrower technical-beta surface

Entrypoint:

- `scripts/dev/retrofx-v2-techbeta`

Current surface includes:

- `status`
- `resolve`
- `plan`
- `compile`
- `bundle`
- `install`
- `uninstall`
- `diagnostics`
- `apply`
- `off`
- `packs`
- `smoke`

Current surface intentionally excludes:

- `migrate inspect-1x`
- `preview-x11`
- `package-alpha`

## Current Package, Bundle, And Install Truth

- `package-alpha` remains the broader internal developer-line packaging flow.
- `package-technical-beta` is the narrowed copied-toolchain candidate packaging flow.
- `bundle`, `install`, and `uninstall` remain available on both the internal developer surface and the technical-beta wrapper.
- temp-HOME install state remains isolated under the managed `retrofx-v2-dev` footprint.

## Current Status And Diagnostics Truth

- `scripts/dev/retrofx-v2 status` reports the broader internal developer-line identity `2.0.0-alpha.internal.2`.
- `scripts/dev/retrofx-v2-techbeta status` reports the narrower outside-facing identity `2.0.0-techbeta.1`.
- the latest local `v2.0.0-techbeta.1` tag exists, but it is historical and does not point at the current `main` HEAD
- diagnostics capture is present and usable on both the internal and technical-beta surfaces

## What Was Actually Exercised In The Rapid Pass

- internal developer help and status
- technical-beta help and status
- CRT pack resolve, plan, and compile
- modern or minimal pack resolve, plan, and compile
- toolkit, WM, terminal, and display-policy output inspection
- bounded `apply` and `off`
- diagnostics capture
- technical-beta bundle, temp-HOME install, diagnostics, and uninstall
- one degraded Wayland export-oriented plan scenario
- one internal migration inspection scenario
- one internal X11 preview scenario
- the 2.x Python test suite

## Gaps And Risks Observed

- there is no dedicated `docs/v2/TECHNICAL_BETA_OPERATIONS.md`; current operations guidance is split across the execution plan, checklist, notes, templates, and triage docs
- a fresh `package-technical-beta` run was blocked during this pass because the working tree was dirty while docs and status updates were still in progress
- the fallback `bundle` plus `install` path still records internal developer-line release metadata even when exercised through the technical-beta wrapper
- some subsystem JSON still advertises historical implementation prompt IDs such as `TWO-18`, `TWO-19`, and `TWO-16` even though the current branch-level status surface reports `TWO-33`

## Current Conclusion

The merged `main` branch is coherent enough to continue the limited technical-beta line.

It is not yet coherent enough to start broader beta stabilization from this rapid pass alone.
The next step should be a short remediation cycle focused on metadata coherence and then a broader evidence pass on clean candidate artifacts and more than one real host.
