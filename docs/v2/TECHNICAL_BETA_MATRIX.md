# RetroFX 2.x Technical Beta Matrix

This document records the first-pass limited technical-beta execution cycle for TWO-33.

It uses the current tagged candidate package and local diagnostics flow as a simulated advanced-tester run.
There is not yet a broader outside tester corpus.

Execution date: 2026-03-22

Evidence root:

- `/tmp/retrofx-two33.QPDZJN`

Status summary:

- `pass`: 11
- `degraded-pass`: 1
- `partial`: 0
- `fail`: 0
- `blocked`: 0
- `not-tested`: 0

## Matrix

| Scenario | Environment | Command/Flow | Expected | Actual | Status | Severity if failed | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| technical-beta wrapper help and status | real X11 plus `i3` host | `scripts/dev/retrofx-v2-techbeta --help` and `status` | narrowed outside-facing surface is visible and machine-readable status is truthful | `status_label=technical-beta`, `ready_for_limited_public_technical_beta=true`, local tag present at head, and help exposes only the curated command family | pass | n/a | Candidate surface is explicit and does not expose migration or `preview-x11`. |
| broader internal dev status remains separate | real X11 plus `i3` host | `scripts/dev/retrofx-v2 status` | internal developer surface still works without being confused with the outside-facing wrapper | internal status executed cleanly and remained separate from the technical-beta wrapper | pass | n/a | Confirms the branch still has a broader internal surface without collapsing it into the candidate promise. |
| technical-beta candidate package generation | clean tagged tree | `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <temp>` | copied-toolchain candidate package emits reproducibly with correct metadata | package emitted under `retrofx-v2--2.0.0-techbeta.1--modern-minimal--warm-night` with `distribution_scope=limited-public-technical-beta` and copied `bin/retrofx-v2-techbeta` wrapper | pass | n/a | This remains the main outside-facing delivery shape. |
| CRT resolve, plan, and compile | real X11 plus `i3` host via copied toolchain | `bin/retrofx-v2-techbeta resolve/plan/compile --pack crt-core --profile-id green-crt` | resolved CRT profile compiles deterministically and plan remains explicit | resolve succeeded, plan reported `apply_preview_targets=[i3,x11-picom,x11-render-runtime,xresources]`, and compile emitted deterministic CRT target artifacts under `<temp>/out/green-crt/` | pass | n/a | Confirms the retro-style profile family still behaves coherently through the candidate wrapper. |
| toolkit and theme export inspection | real X11 plus `i3` host via copied toolchain | `bin/retrofx-v2-techbeta compile --pack modern-minimal --profile-id warm-night --target gtk-export --target qt-export --target desktop-style --target icon-cursor --target fontconfig --out-root <temp>` | advisory toolkit exports compile deterministically and remain clearly non-owning | emitted `gtk-export.ini`, `qt-export.json`, `desktop-style.json`, `policy.json`, and `60-retrofx-fonts.conf` under `<temp>/out/warm-night/` with advisory-only notes | pass | n/a | Outside testers can inspect these artifacts without being told they own the desktop. |
| bounded apply and off | real X11 plus `i3` host via copied toolchain and temp HOME | `bin/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt` then `off` | bounded activation stays inside 2.x-owned roots and cleanup is reversible | apply completed with export-only and preview-capable distinctions intact; `off` removed only `active/current` and `current-state.json` while preserving manifests and install roots | pass | n/a | No unmanaged cleanup paths were touched. |
| temp-HOME install and uninstall | temp HOME via copied toolchain | `bin/retrofx-v2-techbeta install <package>/bundle` then `uninstall modern-minimal--warm-night` | user-local install footprint is explicit and reversible | install recorded `release_status=technical-beta`; uninstall removed only the bundle and install record and preserved config roots | pass | n/a | Confirms outside advanced testers can install and clean up safely. |
| diagnostics capture | temp HOME via copied toolchain | `bin/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <temp> --label technical-beta-cycle` | diagnostics bundle contains enough evidence for bug reports and uses technical-beta metadata | diagnostics wrote `capture-manifest.json`, `platform-status.json`, `environment.json`, `install-state.json`, `profile/resolved-profile.json`, `profile/session-plan.json`, `profile/source-package-manifest.json`, and `release-status.json` with `status_label=technical-beta` | pass | n/a | TWO-33 revalidated the earlier TWO-32 fix so the outside-facing diagnostics line no longer leaks internal-alpha metadata. |
| migration inspection | internal developer surface on real host | `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact` | legacy mapping report stays deterministic and explicit about loss | inspection succeeded with `mapping_summary={15 clean, 7 degraded, 6 manual, 0 unsupported}` | pass | n/a | Supplementary internal-only evidence; not part of the candidate promise. |
| X11 experimental render preview | internal developer surface on real X11 plus `i3` host | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <temp>` | bounded preview artifacts still emit cleanly where supported | preview succeeded with `implemented_mode=passthrough`, `probe.status=not-requested`, and no warnings | pass | n/a | Supplementary internal-only evidence; the explicit probe remains outside the public candidate surface. |
| degraded Wayland export-only plan | simulated Wayland plus `sway` via copied toolchain | `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | degraded/export-only reporting stays honest | `apply_preview_targets=['sway']`, X11 runtime targets degraded honestly, and warnings explicitly kept live orchestration out of scope | degraded-pass | n/a | This is the expected candidate behavior, not a failure. |
| full 2.x test suite | repo-local dev | `./v2/tests/test.sh` | suite remains green after the execution-cycle docs and validation updates | `Ran 143 tests in 2.738s` and `OK` | pass | n/a | Confirms the execution-layer docs and diagnostics truth pass did not regress the branch. |

## Interpretation

This first execution cycle found no technical-beta-blocker.

What it did prove:

- the copied-toolchain candidate package is usable without source-tree archaeology
- the bounded install, diagnostics, and cleanup paths remain trustworthy
- the narrowed outside-facing wrapper is supportable and honest
- degraded Wayland behavior is explicit rather than misleading

What it did not yet prove:

- broad outside tester success across multiple real hosts
- broader beta stabilization readiness
- live Wayland ownership or broad migration assurance
