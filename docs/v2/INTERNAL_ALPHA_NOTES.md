# RetroFX 2.x Internal Alpha Notes

This is the non-public branch note for internal 2.x testers.

## Implemented And Usable Now

- load, validate, normalize, and resolve pipeline
- terminal, WM, toolkit, and bounded X11 target compilers
- session planning preview
- local pack discovery and pack-aware profile resolution
- 1.x inspection and draft migration output
- deterministic dev bundles
- isolated user-local install, uninstall, and status
- bounded apply or off with explicit manifests
- unified `scripts/dev/retrofx-v2` surface
- reproducible internal-alpha package generation
- local diagnostics capture for alpha evidence

## Experimental But Usable With Care

- bounded X11 `picom` probe on a safe X11 host
- staged apply or off under temp HOME or isolated XDG roots
- install or uninstall under the `retrofx-v2-dev` footprint
- migration inspection for representative legacy profiles
- internal-alpha package generation and diagnostics capture for repo-checkout-based internal testing

## Intentionally Missing

- live Wayland render
- global GNOME, Plasma, or Xfce settings mutation
- public packaging or distro integration
- full 1.x runtime compatibility mode
- standalone copied 2.x toolchain distribution
- default runtime takeover

## What You Should Not Trust Yet

- broad multi-host confidence
- real Wayland-host validation
- wide migration-corpus coverage
- anything that would imply public-beta readiness

## Environment Expectations

Best current fit:

- repo checkout available
- current branch version `2.0.0-alpha.internal.2` should be treated as an untagged post-alpha hardening build
- X11 plus `i3` is the strongest validated live-preview environment
- Wayland is currently best exercised through planning and export-oriented validation
- Wayland GNOME, Plasma, and unknown desktops should be treated as export-oriented validation environments only
- temp HOME or isolated XDG roots are strongly preferred for apply or install testing

## Safety Caveats

- 2.x remains experimental
- 1.x remains the production line
- bounded apply or off only manages 2.x-owned roots
- toolkit outputs are advisory artifacts, not live DE ownership
- internal-alpha packages are not standalone toolchains
- diagnostics capture is local-file based and intentionally does not collect unrelated user files or network telemetry
- diagnostics now capture source-control state plus installed bundle or package evidence when that context exists

## How 2.x Differs From 1.x

- 2.x is profile-resolution and compiler oriented first
- 2.x uses a unified experimental dev surface rather than a production CLI
- 2.x install state lives under `retrofx-v2-dev`, not `retrofx`
- 2.x migration is inspection-plus-draft output, not compatibility takeover

## Known Internal-Alpha Limitations

- controlled internal alpha is acceptable, but broader testing is still premature
- validation remains strongest on one real X11 host plus simulated non-X11 environments
- non-sway Wayland desktops remain explicitly fenced as export-oriented validation paths rather than trusted live-preview targets
- package generation is reproducible, but still repo-checkout dependent
- bundle and install metadata are explicit, but not public-release contracts
- internal alpha now depends on disciplined use of the diagnostics and feedback templates rather than ad hoc reports
- package-alpha is still an internal-alpha package flow, not a broader-alpha distribution surface
- `v2.0.0-alpha.internal.1` remains the latest historical local alpha candidate; the current branch is beyond that candidate snapshot
