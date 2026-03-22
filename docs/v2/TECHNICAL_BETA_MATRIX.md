# RetroFX 2.x Technical Beta Matrix

This document records the rapid technical-beta execution pass against the merged `main` branch on 2026-03-22.

It is based on real command execution and captured artifacts under:

- `v2/releases/reports/technical-beta-exec-20260322-072746Z`

It is not a synthetic success summary.
Blocked and degraded scenarios are recorded as they happened.

## Status Summary

- `pass`: 11
- `degraded-pass`: 1
- `partial`: 0
- `fail`: 0
- `blocked`: 1
- `not-tested`: 0

## Matrix

| Scenario | Environment | Commands | Expected | Actual | Status | Severity if failed | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| internal developer help and status | real X11 plus `i3` host | `scripts/dev/retrofx-v2 --help`; `scripts/dev/retrofx-v2 status` | internal surface is reachable and status truthfully reports the broader developer line | help and status both succeeded; `version=2.0.0-alpha.internal.2`, `status_label=internal-alpha`, `current_build_kind=untagged-internal-developer-line` | pass | n/a | Confirms the broader internal surface still exists separately from the technical-beta wrapper. |
| technical-beta wrapper help and status | real X11 plus `i3` host | `scripts/dev/retrofx-v2-techbeta --help`; `scripts/dev/retrofx-v2-techbeta status` | narrowed outside-facing surface is reachable and status remains explicit | help and status both succeeded; `version=2.0.0-techbeta.1`, `status_label=technical-beta`, `ready_for_limited_public_technical_beta=true`, and the wrapper still excludes `migrate inspect-1x` and `preview-x11` | pass | n/a | The current branch build is ahead of the historical local tag, and status reports that honestly. |
| diagnostics capture on current main | real X11 plus `i3` host and temp HOME | `scripts/dev/retrofx-v2-techbeta diagnostics --pack modern-minimal --profile-id warm-night --output-root <temp> --label rapid-main` | diagnostics bundle is usable for triage and records the technical-beta identity | diagnostics succeeded and wrote 18 artifacts including `capture-manifest.json`, `platform-status.json`, `release-status.json`, `state/current-state.json`, `profile/output-inventory.json`, and `source-control.json` | pass | n/a | Bundle path: `v2/releases/reports/technical-beta-exec-20260322-072746Z/diagnostics/20260322-072823z--rapid-main/`. |
| CRT resolve, plan, and compile | real X11 plus `i3` host | `scripts/dev/retrofx-v2-techbeta resolve/plan/compile --pack crt-core --profile-id green-crt` | retro-style profile remains deterministic and the plan stays explicit | resolve, plan, and compile all succeeded; plan reported `apply_preview_targets=[i3,x11-picom,x11-render-runtime,xresources]` and compile emitted bounded CRT artifacts | pass | n/a | Confirms the retro profile family still behaves coherently through the narrowed wrapper. |
| modern or minimal resolve, plan, and compile | real X11 plus `i3` host | `scripts/dev/retrofx-v2-techbeta resolve/plan/compile --pack modern-minimal --profile-id warm-night` | modern daily-driver profile remains deterministic and capability-aware | resolve, plan, and compile all succeeded for `warm-night`; plan stayed non-destructive and compile emitted the expected target families | pass | n/a | Diagnostics later confirmed output inventory under `v2/out/warm-night/`. |
| target output inspection | real X11 plus `i3` host | inspect outputs from `techbeta_compile_modern` and diagnostics inventory | at least terminal, WM, toolkit, and display-policy artifacts are present and advisory where documented | compile reported implemented families for terminal, WM, toolkit, and X11; emitted outputs included terminal configs, WM configs, toolkit exports, and display-policy or render artifacts | pass | n/a | Output inventory stayed repo-local and inspectable without implying live desktop ownership. |
| bounded apply and off | real X11 plus `i3` host and temp HOME | `scripts/dev/retrofx-v2-techbeta apply --pack crt-core --profile-id green-crt`; `status`; `off` | bounded activation remains reversible and 2.x-owned | apply succeeded with clear `export_only_targets`, `degraded_targets`, and `apply_preview_targets`; `off` removed only `active/current` and `current-state.json` and preserved installs, manifests, and last-good data | pass | n/a | `skipped_cleanup_paths=[]`; cleanup stayed inside managed roots. |
| technical-beta candidate package generation on current working tree | current repo-local `main` checkout with in-flight doc changes | `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night --package-root <temp>` | fresh candidate package can be regenerated | command returned structured `dirty-working-tree` failure and did not emit a package | blocked | n/a | This was an honest operator-state gate, not a crash. The current rapid pass therefore fell back to bundle or install evidence instead of a fresh candidate package. |
| bundle, temp-HOME install, diagnostics, and uninstall fallback | temp HOME via technical-beta wrapper | `scripts/dev/retrofx-v2-techbeta bundle`; `install`; `diagnostics`; `uninstall` | bundle and user-local install flow remain bounded and reversible | bundle, install, diagnostics, and uninstall all succeeded; uninstall removed only bundle and install records | pass | medium | The flow worked, but the install JSON still carried internal developer-line release metadata instead of technical-beta metadata. |
| degraded Wayland export-only plan | simulated Wayland plus `sway` | `WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... scripts/dev/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | degraded or export-only behavior is surfaced honestly | command succeeded; `apply_preview_targets=['sway']`, X11 runtime pieces stayed degraded, and warnings kept live ownership out of scope | degraded-pass | n/a | This is the expected limited technical-beta behavior, not a failure. |
| migration inspection | internal developer surface on real host | `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact` | deterministic compatibility report with explicit loss classes | inspection succeeded with a compact mapping summary and no crash | pass | n/a | This remains internal-only evidence, not part of the outside-facing promise. |
| X11 preview | internal developer surface on real X11 plus `i3` host | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <temp>` | bounded preview artifacts still emit where supported | preview succeeded with `implemented_mode=passthrough`, `probe.status=not-requested`, and no warnings | pass | n/a | This remains internal-only evidence. |
| full 2.x test suite | repo-local dev | `./v2/tests/test.sh` | suite stays green while docs and status truth are updated | `Ran 143 tests in 2.806s`; `OK` | pass | n/a | Confirms the rapid execution documentation pass did not regress the Python test suite. |

## Interpretation

What this rapid pass proved:

- the merged `main` branch still supports continued limited technical beta
- the narrowed technical-beta wrapper remains reachable and supportable
- bounded apply, off, diagnostics, bundle, install, and uninstall remain usable for rapid evidence capture
- degraded Wayland planning is explicit rather than misleading

What this rapid pass also exposed:

- a fresh technical-beta package was not regenerated on this in-flight working tree because the clean-tree gate did its job
- the fallback install path still leaks internal developer-line release metadata
- lower-level JSON still leaks historical prompt IDs in some subsystem implementation blocks

What this rapid pass did not prove:

- broader beta stabilization readiness
- multi-host support breadth
- a real outside tester evidence corpus
