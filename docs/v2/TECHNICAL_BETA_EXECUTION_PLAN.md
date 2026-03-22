# RetroFX 2.x Technical Beta Execution Plan

This document defines the real limited technical-beta execution set for the merged `main` branch.

It is based on the copied-toolchain package actually exercised on 2026-03-22, not on a branch-era plan.

Current evidence root:

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

Operational support docs:

- [TECHNICAL_BETA_OPERATIONS.md](TECHNICAL_BETA_OPERATIONS.md)
- [LIMITED_TECHNICAL_BETA_RUNBOOK.md](LIMITED_TECHNICAL_BETA_RUNBOOK.md)

## Audience

This line is for:

- advanced testers comfortable with temp-HOME or user-local testing
- testers willing to read explicit JSON status, warnings, and diagnostics output
- testers who understand that `1.x` remains the production line

It is not for:

- general users
- testers expecting live Wayland ownership
- testers expecting broad migration guarantees

## Executed Scenario Set

### A. Package and wrapper inspection

Commands:

- `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <report>/packages`
- `<package-dir>/bin/retrofx-v2-techbeta --help`
- `<package-dir>/bin/retrofx-v2-techbeta status`

Expected:

- package generation succeeds from a clean `main` tree
- the packaged wrapper exposes only the narrowed technical-beta surface
- status reports `technical-beta` identity and the limited support matrix

Evidence:

- `commands/package_technical_beta.*`
- `commands/techbeta_help.*`
- `commands/techbeta_status.*`
- `packages/.../package-manifest.json`

### B. Supported smoke path

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night --out-root <report>/smoke-out`

Expected:

- the copied-toolchain smoke path succeeds end to end without destructive side effects

Evidence:

- `commands/techbeta_smoke.*`
- `smoke-out/`

### C. CRT resolve and plan

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta resolve --pack crt-core --profile-id green-crt`
- `<package-dir>/bin/retrofx-v2-techbeta plan --pack crt-core --profile-id green-crt --write-preview --out-root <report>/out-crt`

Expected:

- the retro profile resolves deterministically
- plan output clearly separates apply-preview, degraded, and export-only targets

Evidence:

- `commands/techbeta_resolve_crt.*`
- `commands/techbeta_plan_crt.*`
- `out-crt/`

### D. Modern compile and artifact inspection

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta compile --pack modern-minimal --profile-id warm-night --out-root <report>/out-modern`

Expected:

- deterministic terminal, WM, toolkit-export, display-policy, and X11-adjacent artifacts are emitted
- advisory exports remain clearly advisory

Evidence:

- `commands/techbeta_compile_modern.*`
- `out-modern/`

### E. Bounded activation

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`
- `<package-dir>/bin/retrofx-v2-techbeta status`
- `<package-dir>/bin/retrofx-v2-techbeta off`

Expected:

- live checks remain bounded to managed `retrofx-v2-dev` roots
- post-apply status stays truthful
- `off` removes only 2.x-owned activation state

Evidence:

- `commands/techbeta_apply_x11.*`
- `commands/techbeta_status_after_apply.*`
- `commands/techbeta_off_x11.*`

### F. Temp-HOME install diagnostics and cleanup

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta install <package-dir>/bundle`
- `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <report>/diagnostics --label installed-main`
- `<package-dir>/bin/retrofx-v2-techbeta uninstall modern-minimal--warm-night`

Expected:

- install records technical-beta release metadata, not internal-alpha metadata
- diagnostics bundles capture install-state and package metadata
- uninstall removes only bounded install artifacts

Evidence:

- `commands/techbeta_install_bundle.*`
- `commands/techbeta_diagnostics_installed.*`
- `commands/techbeta_uninstall_bundle.*`
- `diagnostics/20260322-094028z--installed-main/`

### G. Active diagnostics capture

Commands:

- `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack crt-core --profile-id green-crt --output-root <report>/diagnostics --label active-main`

Expected:

- diagnostics are usable after bounded activation and capture current activation truth

Evidence:

- `commands/techbeta_diagnostics_active.*`
- `diagnostics/20260322-094027z--active-main/`

### H. Degraded Wayland plan

Commands:

- `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... <package-dir>/bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <report>/out-wayland`

Expected:

- the scenario succeeds only as degraded or export-only
- live ownership is not implied

Evidence:

- `commands/techbeta_wayland_plan.*`
- `out-wayland/`

### I. Internal supplementary checks: migration inspection and X11 preview

Commands:

- `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact`
- `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <report>/preview-x11`

Expected:

- internal maintainer-only surfaces remain deterministic
- these checks do not expand the outside-facing support promise

Evidence:

- `commands/dev_migrate_inspect.*`
- `commands/dev_preview_x11.*`
- `preview-x11/`

### J. Regression suite

Commands:

- `./v2/tests/test.sh`

Expected:

- the Python test suite stays green while the technical-beta docs and package surface are updated

Evidence:

- test output from the current run

## Result Classes

- `pass`: the workflow completed and matched the declared support matrix
- `degraded-pass`: the workflow completed and the degraded or export-only condition was surfaced honestly
- `partial`: the workflow completed but expected evidence was incomplete
- `fail`: the workflow completed with incorrect or misleading behavior
- `blocked`: the workflow could not be run because of an environment or gate restriction
- `not-tested`: the workflow was intentionally skipped

## Out Of Scope

- general-public beta claims
- live Wayland ownership
- broad migration assurance
- replacement of `1.x`
- automatic publication
