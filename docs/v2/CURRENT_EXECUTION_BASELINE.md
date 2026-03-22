# RetroFX 2.x Current Execution Baseline

This document records what was actually present on the merged `main` branch during the real limited technical-beta execution pass on 2026-03-22.

It is factual on purpose.
It does not treat older branch-stage plans as current evidence.

## Evidence Root

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

That report root contains:

- copied-toolchain package output
- command stdout, stderr, and exit-code captures
- diagnostics bundles for active and installed states
- temp-HOME install, uninstall, and bounded apply or off evidence
- degraded Wayland planning evidence
- internal supplementary migration and X11 preview evidence

## Current Visible Surfaces

### Internal developer surface

Entrypoint:

- `scripts/dev/retrofx-v2`

Current internal surface includes:

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

Current technical-beta surface includes:

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

Current technical-beta surface intentionally excludes:

- `migrate inspect-1x`
- `preview-x11`
- `package-alpha`

## Current Package Bundle And Install Truth

- `package-technical-beta` now regenerates the copied-toolchain candidate package cleanly from the current `main` tree.
- the generated package exposes `bin/retrofx-v2-techbeta`, a bounded bundle, copied toolchain files, and tester docs
- the packaged install flow now records `technical-beta` release metadata end to end
- temp-HOME install state remains isolated under the managed `retrofx-v2-dev` footprint

## Current Status And Diagnostics Truth

- `scripts/dev/retrofx-v2 status` still reports the broader internal developer-line identity `2.0.0-alpha.internal.2`
- `scripts/dev/retrofx-v2-techbeta status` reports the narrowed outside-facing identity `2.0.0-techbeta.1`
- branch-level release metadata now reports the current execution prompt as `TWO-35`
- diagnostics capture remains usable on both the internal and technical-beta surfaces

## What Was Actually Exercised

- copied-toolchain package generation from a clean `main` tree
- packaged-wrapper `--help` and `status`
- packaged smoke path
- CRT resolve and plan
- modern compile plus artifact inspection
- bounded `apply`, post-apply `status`, and `off`
- active-state diagnostics capture
- temp-HOME install, diagnostics, and uninstall
- one degraded Wayland export-oriented plan scenario
- one internal migration inspection scenario
- one internal X11 preview scenario
- the 2.x Python test suite

## Remaining Risks

- evidence is still one operator and one real X11 plus `i3` host plus simulated Wayland and temp-HOME scenarios
- there is still no real outside tester corpus on `main`
- some subsystem JSON still leaks historical implementation prompt IDs such as `TWO-19`, `TWO-18`, `TWO-17`, and `TWO-15`
- Wayland remains degraded or export-only rather than supported for live runtime ownership

## Current Conclusion

The merged `main` branch is coherent enough to continue the limited technical beta.

It is not yet coherent enough to start broader beta stabilization.
The next step is not a fast remediation sprint.
The next step is to continue the limited technical beta, collect real outside-style reports, and broaden real-host evidence before revisiting broader beta stabilization.
