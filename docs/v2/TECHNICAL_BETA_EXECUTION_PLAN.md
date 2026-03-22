# RetroFX 2.x Technical Beta Execution Plan

This document defines the rapid technical-beta execution set for the merged `main` branch.

This is an execution document, not a feature plan.
It is deliberately small enough to run in one operator pass and precise enough to support blocker triage.

Operational note:

- there is no dedicated `TECHNICAL_BETA_OPERATIONS.md` on this branch right now
- operational guidance is currently split across this plan, [TECHNICAL_BETA_RELEASE_CHECKLIST.md](TECHNICAL_BETA_RELEASE_CHECKLIST.md), [TECHNICAL_BETA_NOTES.md](TECHNICAL_BETA_NOTES.md), and the technical-beta templates and triage docs

Current rapid-pass evidence root:

- `v2/releases/reports/technical-beta-exec-20260322-072746Z`

## Audience

The limited technical beta is for:

- technically literate testers comfortable with temp-HOME workflows
- testers able to read machine-readable JSON output and explicit warnings
- testers who understand that 1.x remains the production line

It is not for:

- general users
- testers expecting global desktop integration
- testers expecting live Wayland ownership

## Rapid Scenario Set

### A. Core inspection

Commands:

- `scripts/dev/retrofx-v2 --help`
- `scripts/dev/retrofx-v2 status`
- `scripts/dev/retrofx-v2-techbeta --help`
- `scripts/dev/retrofx-v2-techbeta status`

Expected:

- help text is present and the outside-facing wrapper remains narrower than the internal surface
- machine-readable status distinguishes the internal developer line from the technical-beta line

Evidence:

- captured help output
- captured status JSON

### B. CRT profile resolve, plan, and compile

Commands:

- `scripts/dev/retrofx-v2-techbeta resolve --pack crt-core --profile-id green-crt`
- `scripts/dev/retrofx-v2-techbeta plan --pack crt-core --profile-id green-crt --write-preview --out-root <temp>`
- `scripts/dev/retrofx-v2-techbeta compile --pack crt-core --profile-id green-crt --out-root <temp>`

Expected:

- the retro-style profile resolves cleanly
- plan output remains explicit
- compile emits deterministic artifacts

Evidence:

- resolve JSON
- plan JSON
- compile JSON

### C. Modern or minimal profile resolve, plan, and compile

Commands:

- `scripts/dev/retrofx-v2-techbeta resolve --pack modern-minimal --profile-id warm-night`
- `scripts/dev/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>`
- `scripts/dev/retrofx-v2-techbeta compile --pack modern-minimal --profile-id warm-night --out-root <temp>`

Expected:

- the modern profile resolves cleanly
- plan output remains non-destructive and capability-aware
- compile emits toolkit, WM, terminal, and X11-adjacent outputs deterministically

Evidence:

- resolve JSON
- plan JSON
- compile JSON
- output inventory from diagnostics

### D. Bounded activation

Commands:

- `scripts/dev/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`
- `scripts/dev/retrofx-v2-techbeta status`
- `scripts/dev/retrofx-v2-techbeta off`

Expected:

- apply remains bounded to 2.x-owned roots
- `status` reflects the active state truthfully
- `off` removes only 2.x-owned active state

Evidence:

- apply JSON
- post-apply status JSON
- off JSON
- captured current-state or manifest files from diagnostics

### E. Package, bundle, and temp-HOME install path

Commands:

- `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <temp>`
- fallback if packaging is intentionally blocked on the current tree:
- `scripts/dev/retrofx-v2-techbeta bundle --pack modern-minimal --profile-id warm-night --out-root <temp>`
- `HOME=<temp-home> scripts/dev/retrofx-v2-techbeta install <bundle-dir>`
- `HOME=<temp-home> scripts/dev/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <temp> --label <label>`
- `HOME=<temp-home> scripts/dev/retrofx-v2-techbeta uninstall modern-minimal--warm-night`

Expected:

- a clean candidate tree can package reproducibly
- if current operator state blocks packaging, the block is explicit rather than ambiguous
- bundle, install, diagnostics, and uninstall remain bounded and reversible

Evidence:

- package or bundle JSON
- install JSON
- diagnostics bundle
- uninstall JSON

### F. X11 and degraded-path planning

Commands:

- `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <temp>`
- `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... scripts/dev/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>`

Expected:

- the internal X11 preview path works where supported
- the degraded Wayland plan remains honest and export-oriented

Evidence:

- preview JSON
- degraded plan JSON

### G. Compatibility inspection

Commands:

- `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact`

Expected:

- the current migration inspection path remains deterministic and explicit about lossy mappings

Evidence:

- migration inspection JSON

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

## Evidence To Capture

- current branch revision and status output
- help output for both entrypoints
- command stdout, stderr, and exit codes
- package or bundle manifest paths where applicable
- plan output for supported and degraded scenarios
- current-state and active-manifest evidence for bounded runtime checks
- diagnostics bundle paths
- install-state and uninstall summaries where relevant
- migration inspection output
- X11 preview output where supported

## Result Classes

- `pass`: expected workflow completed and output matched the declared support matrix
- `degraded-pass`: the workflow completed and reported a degraded or export-only condition honestly
- `partial`: the workflow completed but omitted important expected evidence or required manual interpretation
- `blocker`: the workflow failed in a way that makes the limited technical beta unsafe, misleading, or unfit for outside advanced testers
- `blocked`: the workflow could not be completed because a declared gate, operator-state restriction, or environment limitation prevented it

## Explicitly Out Of Scope

- replacing 1.x
- public general-user beta claims
- live Wayland ownership
- global desktop mutation
- broad migration compatibility guarantees
- external automation or automatic publication
