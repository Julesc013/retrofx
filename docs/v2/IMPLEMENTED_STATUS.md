# RetroFX 2.x Implemented Status

This document is the current implementation truth for `2.x` on the current `main` branch.
It is intentionally blunt.

Repository truth:

- `1.x` remains the production line
- `2.x` remains experimental
- the broader internal developer surface and the narrower technical-beta candidate surface are both real, but they are not the same promise
- the current `main` HEAD is not automatically the same artifact as the latest local technical-beta tag

## Matrix

| Area | Implemented | Experimental | Planned | Notes |
| --- | --- | --- | --- | --- |
| schema validation | yes | yes | no | Raw and normalized validation are real in `v2/core/validation/`. |
| normalization | yes | yes | no | Defaults, canonicalization, and semantic derivation are real in `v2/core/normalization/`. |
| resolved profile | yes | yes | no | Resolved theme, typography, render, display, pack, and session policy are real in `v2/core/resolution/`. |
| terminal targets | yes | yes | no | `xresources`, `alacritty`, `kitty`, `tmux`, and `vim` compile deterministically. |
| WM targets | yes | yes | no | `i3`, `sway`, and `waybar` export config or style artifacts. |
| toolkit exports | yes | yes | no | `gtk-export`, `qt-export`, `icon-cursor`, `desktop-style`, and `fontconfig` are export-oriented and advisory. |
| typography outputs | yes | yes | no | Role-based typography is resolved and emitted where supported. |
| display policy outputs | yes | yes | no | Display policy is concrete, planned, exportable, and consumed by the bounded X11 render slice. |
| pack system | yes | yes | no | Local pack manifests and curated built-in packs are real. Remote/community distribution is not. |
| migration tooling | yes | yes | no | 1.x profile inspection and draft migration are real. Runtime compatibility is not. |
| install or bundle flow | yes | yes | no | Repo-local bundles, internal-alpha packages, limited technical-beta candidate packages, and isolated user-local experimental installs are real. Uninstall rejects paths outside the managed 2.x bundle store. |
| X11 render or compiler | yes | yes | no | Shader, picom, runtime metadata, and explicit bounded preview exist for X11 only. The explicit probe has one real X11 plus `i3` validation run and remains internal-only. |
| session planning | yes | yes | no | Environment detection and capability-aware planning are real and non-destructive. |
| bounded apply or off | yes | yes | no | TWO-19 current activation, manifests, last-good, and `off` are real but intentionally narrow, and cleanup now stays inside managed 2.x roots. |
| global desktop integration | no | no | yes | Live GNOME, Plasma, Xfce, and cross-DE mutation are not implemented. |
| live Wayland render | no | no | yes | Wayland render remains degraded or export-only. |
| full compatibility mode | no | no | yes | Migration exists, but 1.x runtime compatibility does not. |

## Surfaces In Scope

### Broader Internal Developer Surface

Implemented and coherent:

- `scripts/dev/retrofx-v2 status`
- `scripts/dev/retrofx-v2 resolve`
- `scripts/dev/retrofx-v2 plan`
- `scripts/dev/retrofx-v2 compile`
- `scripts/dev/retrofx-v2 packs list` and `packs show`
- `scripts/dev/retrofx-v2 migrate inspect-1x`
- `scripts/dev/retrofx-v2 bundle`, `install`, and `uninstall`
- `scripts/dev/retrofx-v2 package-alpha`
- `scripts/dev/retrofx-v2 package-technical-beta`
- `scripts/dev/retrofx-v2 diagnostics`
- `scripts/dev/retrofx-v2 apply`, `off`, and `preview-x11`
- `scripts/dev/retrofx-v2 smoke`
- `scripts/dev/retrofx-v2-techbeta`

### Narrower Technical-Beta Surface

Implemented and coherent:

- `scripts/dev/retrofx-v2-techbeta status`
- `scripts/dev/retrofx-v2-techbeta resolve`
- `scripts/dev/retrofx-v2-techbeta plan`
- `scripts/dev/retrofx-v2-techbeta compile`
- `scripts/dev/retrofx-v2-techbeta bundle`
- `scripts/dev/retrofx-v2-techbeta install`
- `scripts/dev/retrofx-v2-techbeta uninstall`
- `scripts/dev/retrofx-v2-techbeta diagnostics`
- `scripts/dev/retrofx-v2-techbeta apply`
- `scripts/dev/retrofx-v2-techbeta off`
- `scripts/dev/retrofx-v2-techbeta packs`
- `scripts/dev/retrofx-v2-techbeta smoke`

Intentionally excluded from the technical-beta promise:

- `migrate inspect-1x`
- `preview-x11`
- the broader internal package surface

## Current Status Notes

- internal developer-line version identity: `2.0.0-alpha.internal.2`
- internal developer-line status label: `internal-alpha`
- limited technical-beta candidate identity: `2.0.0-techbeta.1`
- limited technical-beta status label: `technical-beta`
- latest historical alpha tag: `v2.0.0-alpha.internal.1`
- latest local technical-beta candidate tag: `v2.0.0-techbeta.1`
- current `main` may be ahead of the latest local technical-beta tag even when the technical-beta line remains approved

Still intentionally bounded:

- live apply only exists as a narrow 2.x-owned activation path plus the explicit short-lived X11 probe
- toolkit outputs are advisory exports, not live DE ownership
- install and current activation remain separated, but unified `status` now reports both surfaces together
- controlled internal alpha readiness is narrow and currently grounded most strongly in one real X11 plus `i3` validation host
- broader-alpha readiness is not approved; non-sway Wayland desktops are explicitly fenced as export-oriented validation environments
- internal-alpha packages are reproducible and self-describing, but they still assume a repo checkout rather than a standalone copied toolchain
- the limited technical-beta candidate is a separate copied-toolchain surface exposed through `retrofx-v2-techbeta`
- release-ish package generation now blocks dirty trees by default unless explicit internal triage mode is requested
- controlled internal alpha now has a real operational layer, and diagnostics now capture source-control state plus installed bundle or package evidence for the selected profile
- release-status metadata now distinguishes the current build from the historical local alpha candidate and makes broader-alpha or pre-beta no explicit in machine-readable form
- release-status metadata now also carries the blocked pre-beta-candidate identity explicitly so the current internal-alpha line is not mistaken for a non-public pre-beta candidate
- release-status metadata now also carries the technical-beta candidate identity, support matrix, and line-level `ready_for_limited_public_technical_beta=true`
- `package-alpha` now rejects pre-beta, beta, or stable-looking version or status overrides so the current internal package surface cannot fake a public-facing maturity level
- `package-technical-beta` now produces a local copied-toolchain candidate package and keeps the explicit X11 probe plus migration tooling outside the public-facing support promise
- the first limited technical-beta execution cycle has now been run against the tagged candidate package, with structured diagnostics evidence under the new technical-beta matrix and blocker docs
- the rapid merged-`main` execution pass has now re-run that surface directly on the current branch state and recorded one short remediation list before broader beta stabilization should be reconsidered
- the default repo-local release output path is now `v2/releases/internal-alpha/`, which is treated as generated machine-local output rather than committed source

Still not implemented:

- production CLI takeover
- release-quality stability guarantees
- global desktop ownership
- live Wayland render
- full 1.x runtime replacement or compatibility mode

Related truth docs:

- [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md) for the currently enforced code-side boundaries
- [STABILIZATION_CHECKLIST.md](STABILIZATION_CHECKLIST.md) for the next trust gates
- [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) for the first serious scenario-by-scenario validation pass
- [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md) and [ALPHA_READINESS.md](ALPHA_READINESS.md) for the current readiness decision

## Validation Snapshot

- internal experimental use: yes
- controlled internal alpha: yes, for a narrow internal cohort
- current local alpha tag candidate at HEAD: no
- alpha candidate ready for the current branch build: no
- latest historical local alpha candidate: `v2.0.0-alpha.internal.1`
- proposed pre-beta candidate version: `2.0.0-prebeta.internal.1`
- local pre-beta tag candidate: no
- pre-beta candidate ready: no
- latest local technical-beta candidate tag: `v2.0.0-techbeta.1`
- current local technical-beta tag candidate at HEAD: no
- broader alpha: no
- controlled external alpha: no
- non-public pre-beta: no
- limited public technical beta: yes
- limited public technical beta candidate ready: yes
- limited technical beta continuation: yes
- broader beta stabilization: no
- another fast remediation cycle before broader beta stabilization: yes
- pre-beta stabilization: no
- broader testing: no
- main reasons to avoid broader testing: live support remains intentionally narrow to the technical-beta matrix, the fallback technical-beta install path still leaks internal developer-line metadata, lower-level surfaced JSON still leaks prompt-era identifiers, real Wayland-host live-runtime evidence remains out of scope, and migration validation breadth remains limited
