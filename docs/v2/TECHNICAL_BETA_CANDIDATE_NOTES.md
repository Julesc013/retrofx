# RetroFX 2.x Technical Beta Candidate Notes

Candidate version: `2.0.0-techbeta.1`

Candidate status: `technical-beta`

Candidate approval: `TECHNICAL_BETA_CANDIDATE_READY=yes`

## Candidate-Worthy Surface

- copied-toolchain package with `bin/retrofx-v2-techbeta`
- deterministic `resolve`, `plan`, `compile`, `bundle`, `install`, `uninstall`, `diagnostics`, and `smoke`
- bounded `apply` and `off` on X11-oriented environments only
- curated built-in packs and pack-aware profile selection

## Partial Or Experimental Areas

- Wayland remains compile or export-oriented rather than supported live runtime ownership
- toolkit outputs remain advisory exports
- the broader `retrofx-v2` developer surface still exposes more commands than this candidate promises

## Validated Scenarios

- X11 plus `i3`-like host for bounded runtime checks
- temp-HOME install, diagnostics, and uninstall
- pack-based resolve, plan, compile, and bundle generation
- degraded-path planning and compile on Wayland-like environments with explicit export-only reporting

## Degraded, Export-Only, Or Unsupported Areas

- degraded or export-only: Wayland plus `sway`-like plan, compile, bundle, diagnostics
- unsupported for this candidate: live Wayland runtime ownership
- unsupported for this candidate: migration assurance and the explicit X11 probe

## Who Should Test This

- advanced testers comfortable with command-line tooling and temp-HOME workflows
- users able to follow explicit cleanup and diagnostics instructions

## What To Focus On

- deterministic output regressions
- cleanup and ownership safety
- status/help wording drift
- environment misclassification
- missing evidence in diagnostics bundles

## Explicitly Out Of Scope

- 1.x replacement
- public general-user beta expectations
- global desktop mutation
- live Wayland ownership
- broad compatibility or migration guarantees

## Safe Cleanup

- `bin/retrofx-v2-techbeta off`
- `bin/retrofx-v2-techbeta uninstall <bundle-id>`
- remove temp HOME or temp XDG roots after validation
