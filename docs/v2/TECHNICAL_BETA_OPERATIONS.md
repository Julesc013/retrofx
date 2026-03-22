# RetroFX 2.x Technical Beta Operations

This document describes how the limited public technical beta operates on the merged `main` branch.

It is written for the current repository state.
It is not a historical branch-plan document.

Current execution evidence:

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

## What Testers Should Use

Primary outside-facing surface for advanced testers:

- `scripts/dev/retrofx-v2 package-technical-beta --pack <pack> --profile-id <profile>`
- packaged wrapper: `<package-dir>/bin/retrofx-v2-techbeta`

Internal maintainer-only surface:

- `scripts/dev/retrofx-v2`

Outside testers should not be asked to use the broader internal developer surface unless they are explicitly helping with maintainer-only diagnostics.

## Current Package Shape

The current limited technical-beta package is a copied-toolchain directory under:

- `v2/releases/technical-beta/`

It includes:

- `bin/retrofx-v2-techbeta`
- `bundle/`
- `toolchain/v2/`
- `metadata/release-status.json`
- `package-manifest.json`
- the tester-facing docs shipped with the package, including this operations doc and [LIMITED_TECHNICAL_BETA_RUNBOOK.md](LIMITED_TECHNICAL_BETA_RUNBOOK.md)

It does not publish anything automatically.

## In-Scope Environments

Supported now:

- X11 plus `i3`-like for bounded live `apply` and `off`
- temp-HOME or user-local install, diagnostics, and uninstall

Degraded or export-only:

- Wayland plus `sway`-like for `status`, `resolve`, `plan`, `compile`, `bundle`, `diagnostics`, and `smoke`

Out of scope:

- live Wayland runtime ownership
- GNOME or Plasma live desktop ownership
- general-user desktop integration
- anything that implies replacing `1.x`

## Workflows Testers Should Exercise

1. `status` and `--help`
2. `resolve`, `plan`, and `compile`
3. `smoke`
4. bounded `apply` and `off` on supported X11 hosts only
5. temp-HOME `install`, `diagnostics`, and `uninstall`
6. one degraded Wayland or export-only scenario where available

## Diagnostics Capture

Use:

- `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack <pack> --profile-id <profile> --output-root <dir> --label <label>`

Current diagnostics bundles should capture:

- release status
- environment summary
- platform status
- source control state if available
- current activation and install state where relevant
- resolved profile and session plan
- output inventory and source package manifest where relevant
- package manifest and copied-toolchain metadata where relevant

## Issue Reporting

Current report inputs should include:

- candidate version or commit
- environment type
- WM or DE
- commands run
- expected versus actual behavior
- diagnostics bundle path
- whether the issue is `technical-beta-blocker`, `broader-beta-blocker`, `high`, `medium`, or `low`

Use:

- [TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md](TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md)
- [TECHNICAL_BETA_FEEDBACK_TEMPLATE.md](TECHNICAL_BETA_FEEDBACK_TEMPLATE.md)
- [TECHNICAL_BETA_ISSUE_TEMPLATE.md](TECHNICAL_BETA_ISSUE_TEMPLATE.md)

## Maintainer Classification Rules

Classify incoming reports as:

- `technical-beta-blocker` when the limited technical-beta surface becomes unsafe, misleading, or non-reversible
- `broader-beta-blocker` when the limited technical beta can continue but the next broader-beta stage remains blocked
- `high` when the current surface is still usable but confusing or too brittle for wider circulation
- `medium` when the issue is real and actionable but already within a documented degraded or internal-only area
- `low` when the issue is mostly presentational or procedural and does not materially change the support promise

## Current Maintainer Notes

- `1.x` remains the production line
- `2.x` remains experimental
- the technical-beta wrapper is the only outside-facing `2.x` surface
- migration inspection and `preview-x11` remain internal developer surfaces
- broader beta stabilization is still gated separately from continued limited technical-beta circulation
- the current next step is to collect real outside-tester evidence on top of this surface, not to force another fast remediation loop first
