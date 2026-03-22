# RetroFX 2.x Technical Beta Matrix

This document records the real limited technical-beta execution pass against the merged `main` branch on 2026-03-22.

It is based on captured artifacts under:

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

It is not a synthetic success summary.
The matrix below reflects the actual copied-toolchain package run on `main`.

## Status Summary

- `pass`: 14
- `degraded-pass`: 1
- `partial`: 0
- `fail`: 0
- `blocked`: 0
- `not-tested`: 0

## Matrix

| Scenario | Environment | Commands | Expected | Actual | Status | Severity if failed | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| technical-beta package generation on clean `main` | real X11 plus `i3` host, clean tree | `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <report>/packages` | copied-toolchain package regenerates cleanly from current `main` | package succeeded; `version=2.0.0-techbeta.1`, `status_label=technical-beta`, `distribution_scope=limited-public-technical-beta`, `working_tree_clean=true` | pass | broader-beta-blocker | Evidence: `commands/package_technical_beta.out` and `packages/retrofx-v2--2.0.0-techbeta.1--modern-minimal--warm-night/`. |
| packaged wrapper help and status | packaged copied toolchain on real X11 plus `i3` host | `<package-dir>/bin/retrofx-v2-techbeta --help`; `status` | wrapper is reachable and remains narrower than the internal developer surface | both commands succeeded; help kept migration inspection and explicit X11 preview off the outside-facing surface; status reported `technical-beta` identity and the limited support matrix | pass | technical-beta-blocker | Evidence: `commands/techbeta_help.*`, `commands/techbeta_status.*`. |
| packaged smoke path | packaged copied toolchain on real X11 plus `i3` host | `<package-dir>/bin/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night --out-root <report>/smoke-out` | supported smoke path succeeds without hidden global mutation | smoke succeeded and emitted repo-local preview and compile artifacts under `smoke-out/` | pass | high | Evidence: `commands/techbeta_smoke.*`, `smoke-out/`. |
| CRT resolve and plan | packaged copied toolchain on real X11 plus `i3` host | `<package-dir>/bin/retrofx-v2-techbeta resolve --pack crt-core --profile-id green-crt`; `plan --write-preview --out-root <report>/out-crt` | retro profile resolves deterministically and plan stays capability-aware | resolve and plan both succeeded; `apply_preview_targets=[i3,x11-picom,x11-render-runtime,xresources]`, degraded targets stayed explicit | pass | high | Evidence: `commands/techbeta_resolve_crt.*`, `commands/techbeta_plan_crt.*`. |
| modern compile | packaged copied toolchain on real X11 plus `i3` host | `<package-dir>/bin/retrofx-v2-techbeta compile --pack modern-minimal --profile-id warm-night --out-root <report>/out-modern` | compile emits deterministic artifacts for the supported target families | compile succeeded and emitted terminal, WM, toolkit-export, display-policy, and X11-adjacent artifacts under `out-modern/warm-night/` | pass | high | Evidence: `commands/techbeta_compile_modern.*`, `out-modern/`. |
| target output inspection | packaged copied toolchain on real X11 plus `i3` host | inspect `out-modern/warm-night/` and compile JSON | terminal, WM, toolkit, and display-policy artifacts are present and advisory where documented | inspected outputs included `alacritty`, `kitty`, `tmux`, `vim`, `i3`, `sway`, `waybar`, `gtk-export`, `qt-export`, `fontconfig`, `desktop-style`, `x11-display-policy`, `x11-picom`, `x11-render-runtime`, `x11-shader`, and `xresources` | pass | medium | Advisory/export-only notes stayed explicit in the compile payload rather than pretending to be live desktop ownership. |
| bounded apply, post-apply status, and off | packaged copied toolchain on real X11 plus `i3` host and temp HOME | `<package-dir>/bin/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`; `status`; `off` | bounded activation remains reversible and stays inside 2.x-managed roots | apply succeeded with explicit warnings, post-apply status succeeded, and `off` removed only `active/current` and `current-state.json` while preserving bundle, install, last-good, and manifest roots | pass | technical-beta-blocker | Evidence: `commands/techbeta_apply_x11.*`, `commands/techbeta_status_after_apply.*`, `commands/techbeta_off_x11.*`. |
| active diagnostics capture | packaged copied toolchain on real X11 plus `i3` host and temp HOME | `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack crt-core --profile-id green-crt --output-root <report>/diagnostics --label active-main` | diagnostics capture active-state evidence and technical-beta identity | diagnostics succeeded and wrote `20260322-094027z--active-main/` with capture manifest, release status, platform status, source control, current activation, environment, resolved profile, session plan, and package-manifest evidence | pass | high | Evidence directory: `diagnostics/20260322-094027z--active-main/`. |
| temp-HOME install | packaged copied toolchain in temp HOME or XDG roots | `<package-dir>/bin/retrofx-v2-techbeta install <package-dir>/bundle` | install is bounded and records technical-beta metadata | install succeeded and recorded `version=2.0.0-techbeta.1`, `status_label=technical-beta`, `distribution_scope=limited-public-technical-beta` | pass | technical-beta-blocker | Evidence: `commands/techbeta_install_bundle.*`. This closes the earlier internal-alpha metadata leak. |
| installed diagnostics capture | packaged copied toolchain in temp HOME or XDG roots | `<package-dir>/bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <report>/diagnostics --label installed-main` | diagnostics capture install-state and package metadata for a tester-ready bug report | diagnostics succeeded and wrote `20260322-094028z--installed-main/` with install-state, package metadata, resolved profile, session plan, output inventory, release status, and source-control evidence | pass | high | Evidence directory: `diagnostics/20260322-094028z--installed-main/`. |
| uninstall cleanup | packaged copied toolchain in temp HOME or XDG roots | `<package-dir>/bin/retrofx-v2-techbeta uninstall modern-minimal--warm-night` | uninstall removes only bundle-store and installation records | uninstall succeeded and removed only bundle and installation JSON paths while preserving profile and pack config roots | pass | technical-beta-blocker | Evidence: `commands/techbeta_uninstall_bundle.*`. |
| degraded Wayland export-only plan | packaged copied toolchain, simulated Wayland plus `sway` | `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... <package-dir>/bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <report>/out-wayland` | degraded behavior is explicit and remains non-destructive | command succeeded; `apply_preview_targets=['sway']`, X11 live-runtime pieces stayed degraded, and export-only targets stayed export-only | degraded-pass | n/a | Evidence: `commands/techbeta_wayland_plan.*`, `out-wayland/`. |
| migration inspection | internal developer surface on real host | `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact` | deterministic compatibility inspection without crashing | inspection succeeded with explicit lossy or unsupported reporting | pass | medium | Internal-only evidence; not part of the outside-facing technical-beta promise. |
| X11 preview | internal developer surface on real X11 plus `i3` host | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <report>/preview-x11` | bounded internal X11 preview artifacts still emit where supported | preview succeeded with `implemented_mode=passthrough` and no warnings | pass | medium | Internal-only evidence; not part of the outside-facing technical-beta promise. |
| full 2.x test suite | repo-local dev | `./v2/tests/test.sh` | Python test suite stays green while technical-beta docs and package metadata are updated | suite passed; `Ran 143 tests in 2.878s`; `OK` | pass | n/a | Confirms the current documentation and package-support pass did not regress the 2.x test suite. |

## Interpretation

What this real main-branch execution pass proved:

- the copied-toolchain technical-beta package regenerates cleanly from current `main`
- the packaged wrapper is usable by advanced testers without dropping back to the internal developer surface
- bounded apply or off, diagnostics, install, and uninstall remain supportable and reversible
- packaged install now reports technical-beta release metadata end to end
- degraded Wayland behavior remains honest rather than misleading

What this execution pass did not prove:

- broader beta stabilization readiness
- multi-host or multi-operator breadth
- a real outside tester evidence corpus
