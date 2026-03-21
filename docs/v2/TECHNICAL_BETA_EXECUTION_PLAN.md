# RetroFX 2.x Technical Beta Execution Plan

This document defines the first real limited technical-beta execution loop for the TWO-33 branch state.

This is a first-pass execution cycle.
It uses the current tagged candidate package, the existing runbook/checklist surface, and local diagnostics capture.
It is not yet based on a broad outside tester corpus.

## Audience

The limited technical beta is for:

- technically literate testers comfortable with temp-HOME workflows
- testers able to read machine-readable JSON output and explicit warnings
- testers who understand that 1.x remains the production line

It is not for:

- general users
- testers expecting global desktop integration
- testers expecting live Wayland ownership

## Required Scenarios

1. `resolve`, `plan`, and `compile` on one CRT-style curated profile
2. bounded `apply` and `off` on one X11-oriented curated profile
3. package generation plus temp-HOME `install`, `diagnostics`, and `uninstall`
4. toolkit or theme export inspection on one modern or minimal profile
5. one degraded Wayland or export-only plan scenario
6. one migration inspection on a real 1.x profile
7. one X11 experimental render preview where the host supports it

## Recommended Environments

- validated supported:
  - X11 plus `i3`-like
  - temp-HOME install mode
- degraded/export-only:
  - Wayland plus `sway`-like
- outside current candidate promise:
  - Wayland plus GNOME or Plasma-like live runtime ownership
  - broad migration assurance
  - explicit X11 live probe use by outside testers

## Required Commands And Workflows

- candidate package generation:
  - `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night`
- tester wrapper sanity:
  - `bin/retrofx-v2-techbeta --help`
  - `bin/retrofx-v2-techbeta status`
- core candidate workflow:
  - `bin/retrofx-v2-techbeta resolve --pack crt-core --profile-id green-crt`
  - `bin/retrofx-v2-techbeta plan --pack crt-core --profile-id green-crt --write-preview --out-root <temp>`
  - `bin/retrofx-v2-techbeta compile --pack crt-core --profile-id green-crt --out-root <temp>`
- bounded runtime workflow:
  - `bin/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`
  - `bin/retrofx-v2-techbeta off`
- install and diagnostics workflow:
  - `bin/retrofx-v2-techbeta install <package>/bundle`
  - `bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <temp> --label <label>`
  - `bin/retrofx-v2-techbeta uninstall modern-minimal--warm-night`
- degraded-path workflow:
  - `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>`
- supplementary internal-only evidence:
  - `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact`
  - `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <temp>`

## Evidence To Capture

- tagged candidate version or commit
- package manifest path
- `status` output
- plan output for both supported and degraded scenarios
- current-state manifest or `apply`/`off` output for bounded runtime checks
- diagnostics bundle path
- install-state and uninstall summary where relevant
- emitted output inventory for toolkit or theme export scenarios
- screenshots or logs only if they materially clarify a failure

## Result Classes

- `pass`: expected workflow completed and output matched the declared support matrix
- `degraded-pass`: the workflow completed and reported a degraded or export-only condition honestly
- `partial`: the workflow completed but omitted important expected evidence or required manual interpretation
- `blocker`: the workflow failed in a way that makes the limited technical beta unsafe, misleading, or unfit for outside advanced testers

## Explicitly Out Of Scope

- replacing 1.x
- public general-user beta claims
- live Wayland ownership
- global desktop mutation
- broad migration compatibility guarantees
- external automation or automatic publication
