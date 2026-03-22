# RetroFX 2.x Limited Technical Beta Runbook

This is the practical runbook for advanced testers using the current `main`-branch technical-beta package.

Current execution evidence for this runbook:

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

## 1. Obtain The Current Package

Ask a maintainer for a current `package-technical-beta` output directory or build one from a clean tree:

- `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <dir>`

Use the packaged wrapper:

- `<package-dir>/bin/retrofx-v2-techbeta`

The shipped package should include:

- [TECHNICAL_BETA_NOTES.md](TECHNICAL_BETA_NOTES.md)
- [TECHNICAL_BETA_CHECKLIST.md](TECHNICAL_BETA_CHECKLIST.md)
- [TECHNICAL_BETA_OPERATIONS.md](TECHNICAL_BETA_OPERATIONS.md)
- this runbook

## 2. Minimum Environment Assumptions

- preferred supported live-runtime host: X11 plus `i3`-like
- safe install testing: temp HOME or isolated XDG roots
- degraded-path validation: Wayland plus `sway`-like

Do not expect:

- live Wayland ownership
- GNOME or Plasma desktop takeover
- replacement of `1.x`

## 3. First-Run Checks

- `<package-dir>/bin/retrofx-v2-techbeta --help`
- `<package-dir>/bin/retrofx-v2-techbeta status`

Confirm:

- the wrapper identifies itself as `technical-beta`
- the support matrix matches your environment

## 4. Recommended Smoke Path

- `<package-dir>/bin/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night`
- `<package-dir>/bin/retrofx-v2-techbeta resolve --pack crt-core --profile-id green-crt`
- `<package-dir>/bin/retrofx-v2-techbeta plan --pack crt-core --profile-id green-crt --write-preview --out-root <dir>`
- `<package-dir>/bin/retrofx-v2-techbeta compile --pack crt-core --profile-id green-crt --out-root <dir>`

## 5. Bounded Apply Or Off Cautions

Only use live `apply` on supported X11-oriented hosts.

- `<package-dir>/bin/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`
- `<package-dir>/bin/retrofx-v2-techbeta off`

Expected:

- only the bounded `retrofx-v2-dev` footprint is touched
- `1.x` is not modified

## 6. X11 Experimental Render Caveats

- X11 render artifacts are real and bounded
- the explicit `preview-x11` probe remains on the internal developer surface
- outside testers should focus on bounded `apply`, `plan`, `compile`, and emitted artifacts rather than internal preview tooling

## 7. Degraded Wayland Expectations

Wayland is still export-oriented or degraded in this line.

Valid uses:

- `status`
- `resolve`
- `plan`
- `compile`
- `bundle`
- `diagnostics`
- `smoke`

Do not treat Wayland live runtime ownership as supported.

## 8. Diagnostics Capture

Capture diagnostics after any meaningful scenario:

- `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <dir> --label <label>`

Share:

- the diagnostics bundle path
- the commands you ran
- expected versus actual behavior
- your environment details using [TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md](TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md)

## 9. Issue Reporting Expectations

Useful reports include:

- status/help mismatches
- wrong support-matrix classification
- non-reversible cleanup
- install or uninstall ownership problems
- missing or confusing diagnostics artifacts
- degraded paths that are not reported honestly

Not useful as bugs unless they contradict docs:

- missing live Wayland ownership
- lack of GNOME or Plasma takeover
- lack of `1.x` runtime replacement

Use these templates when filing issues:

- [TECHNICAL_BETA_FEEDBACK_TEMPLATE.md](TECHNICAL_BETA_FEEDBACK_TEMPLATE.md)
- [TECHNICAL_BETA_ISSUE_TEMPLATE.md](TECHNICAL_BETA_ISSUE_TEMPLATE.md)

## 10. Cleanup

- `<package-dir>/bin/retrofx-v2-techbeta off`
- `<package-dir>/bin/retrofx-v2-techbeta uninstall <bundle-id>`
- remove the temp HOME or temp output directory used for testing

If you used only repo-local compile or plan flows, cleanup is usually just deleting the temp output directory.
