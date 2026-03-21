# RetroFX 2.x Validation Matrix

This document records the first serious validation pass for the current 2.x experimental platform.

Validated on: 2026-03-21

Validation context:

- repo root: `/mnt/btrfs-data/projects/retrofx`
- unified entrypoint: `scripts/dev/retrofx-v2`
- actual host environment used for non-destructive baseline commands: repo-local dev on X11 with `i3`
- simulated environments used where appropriate: Wayland plus `sway`, and TTY or headless
- apply or install validation used temp HOME or isolated XDG roots under `/tmp`
- explicit live X11 `picom` probe was run manually as a bounded 1.0-second validation step on the active X11 plus `i3` host using `passthrough-minimal.toml`

Status legend:

- `pass`
- `degraded-pass`
- `partial`
- `fail`
- `blocked`
- `not-tested`

Current summary:

- `pass`: 24
- `degraded-pass`: 2
- `partial`: 0
- `fail`: 0
- `blocked`: 0
- `not-tested`: 0

## Matrix

| Scenario | Environment | Command/Entry Path | Expected Result | Actual Result | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| valid 2.x profile resolve | repo-local dev | `scripts/dev/retrofx-v2 resolve v2/tests/fixtures/strict-green-crt.toml` | resolution succeeds | `ok=true`, `stage=resolution` | pass | Baseline resolve path is working through the unified surface. |
| malformed 2.x profile reject | repo-local dev | `scripts/dev/retrofx-v2 resolve v2/tests/fixtures/malformed-profile.toml` | validation failure with explicit errors | `ok=false`, `stage=validation`, errors include `missing-custom-palette-source` and `missing-session-targets` | pass | Failure is truthful and structured. |
| normalization defaults visible through resolve | repo-local dev | `scripts/dev/retrofx-v2 resolve v2/tests/fixtures/warm-night-theme-only.toml --include-normalized` | normalized defaults are materialized | normalized values include `terminal_primary=Berkeley Mono`, `ui_sans=Source Sans 3`, `cursor_size=24` | pass | Confirms default-filling remains observable through the dev surface. |
| 1.x compatibility inspection and draft generation | repo-local dev | `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/crt-green-p1-4band.toml --write-draft --out-root <temp>` | migration report plus generated draft bundle | `ok=true`, mapping summary `{15 clean, 7 degraded, 6 manual, 0 unsupported}`, draft bundle written under `out/migrations/` | pass | The result is intentionally lossy but explicit. |
| terminal or TUI compile | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/strict-green-crt.toml --target xresources --target alacritty --out-root <temp>` | deterministic terminal artifacts | compiled `xresources/Xresources` and `alacritty/alacritty.toml` | pass | Confirms the first compiler family still works through the unified surface. |
| WM compile | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/modern-minimal-wm.toml --target i3 --target sway --out-root <temp>` | deterministic WM artifacts | compiled `i3` and `sway` fragments successfully | pass | Export-oriented WM family is working. |
| toolkit export compile | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/retro-desktop-explicit.toml --target gtk-export --target qt-export --target icon-cursor --target desktop-style --out-root <temp>` | advisory toolkit artifacts emitted | compiled `gtk-export`, `qt-export`, `icon-cursor`, and `desktop-style` | pass | Desktop-facing export slice is functioning as designed. |
| display-policy artifact compile | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/strict-green-display-policy.toml --target x11-display-policy --out-root <temp>` | display-policy artifact emitted | wrote `x11-display-policy/display-policy.json` | pass | Advisory display-policy export path is real. |
| pack-aware profile resolution through unified surface | repo-local dev | `scripts/dev/retrofx-v2 compile --pack crt-core --profile-id green-crt --target xresources --out-root <temp>` | built-in pack profile compiles without path fallback | `pack.id=crt-core`, `profile_origin.type=pack`, Xresources artifact emitted | pass | A TWO-22 unified-surface selector bug was found here and fixed. |
| X11 planning preview | simulated X11 plus `i3` | `env DISPLAY=:1 XDG_SESSION_TYPE=x11 XDG_CURRENT_DESKTOP=i3 ... scripts/dev/retrofx-v2 plan v2/tests/fixtures/strict-green-crt.toml --write-preview --out-root <temp>` | honest X11 plan with preview-capable targets | `apply_preview_targets` include `i3`, `x11-picom`, `x11-render-runtime`, and `xresources`; `x11_render.overall_status=x11-live-preview-available` | pass | X11 planning aligns with the implemented bounded runtime slice. |
| Wayland planning preview | simulated Wayland plus `sway` | `env WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway ... scripts/dev/retrofx-v2 plan v2/tests/fixtures/warm-night-theme-only.toml --write-preview --out-root <temp>` | honest degradation for X11-only runtime pieces | `apply_preview_targets=['sway']`; degraded targets include `x11-picom`, `x11-render-runtime`, `x11-shader`, `xresources` | degraded-pass | Behavior is correct and honest, but the runtime path remains export-only outside X11. |
| TTY or headless planning preview | simulated TTY | `env RETROFX_V2_FORCE_SESSION_TYPE=tty TERM=linux ... scripts/dev/retrofx-v2 plan v2/tests/fixtures/strict-green-crt.toml --write-preview --out-root <temp>` | no fake live preview, explicit degradation | `apply_preview_targets=[]`; multiple GUI-facing targets are listed under `degraded_targets` | degraded-pass | The planner does not invent unsupported live behavior. |
| bounded apply or off for export-heavy profile | isolated temp HOME, simulated Wayland | `scripts/dev/retrofx-v2 apply`, `status`, `off` on `warm-night-theme-only.toml` | activation staged, status reports active, off clears owned current state | apply succeeded, status reported `current_active=true`, off removed `active/current` and `current-state.json` | pass | Confirms the bounded apply contract for export-heavy profiles. |
| bounded apply or off for live-eligible profile | isolated temp HOME, simulated X11 | `scripts/dev/retrofx-v2 apply`, `status`, `off` on `strict-green-crt.toml` | activation staged with X11-capable artifacts, off clears owned state | apply succeeded and staged X11-family artifacts; `live_applied_targets=[]`; off cleared owned state | pass | This validates staged activation, not the explicit live probe. |
| X11 render preview for CRT-like profile | simulated X11 | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/strict-green-crt.toml --out-root <temp>` | X11 preview artifacts and preview state emitted | `ok=true`, `implemented_mode=monochrome`, `probe.status=not-requested` | pass | Non-destructive render preview works for monochrome CRT mode. |
| X11 render preview for palette profile | simulated X11 | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/vga-like-palette.toml --out-root <temp>` | X11 preview artifacts and preview state emitted | `ok=true`, `implemented_mode=palette`, `probe.status=not-requested` | pass | Confirms bounded palette render compilation. |
| X11 render preview for passthrough profile | simulated X11 | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --out-root <temp>` | minimal passthrough artifacts emitted | `ok=true`, `implemented_mode=passthrough`, `probe.status=not-requested` | pass | Confirms minimal render path is stable. |
| explicit live X11 `picom` probe in real session | active X11 plus `i3` session | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/passthrough-minimal.toml --probe-picom --probe-seconds 1.0 --out-root /tmp/retrofx-v2-two23-probe` | short-lived explicit live probe | `ok=true`, `probe.status=timed-out`, bounded probe launched against the generated config and wrote preview-state metadata | pass | This is the first manual real-session validation of the explicit TWO-17 probe path. The timeout is an expected bounded-success outcome for this probe design. |
| bundle generation | repo-local dev | `scripts/dev/retrofx-v2 bundle --pack modern-minimal --profile-id warm-night --bundle-root <temp>` | deterministic bundle emitted | `ok=true`, bundle emitted under `<temp>/bundles/modern-minimal--warm-night` | pass | Pack-aware bundle generation now works through the unified surface. |
| internal-alpha package generation | repo-local dev plus isolated temp roots | `scripts/dev/retrofx-v2 package-alpha --pack modern-minimal --profile-id warm-night` then `scripts/dev/retrofx-v2 install <package-dir>/bundle` | reproducible non-public package emitted, then packaged bundle installs into isolated `retrofx-v2-dev` roots with release metadata | `ok=true`, package emitted under `v2/releases/internal-alpha/retrofx-v2--2.0.0-alpha.internal.1--modern-minimal--warm-night`; install record and unified status expose `release_version=2.0.0-alpha.internal.1`, `release_status=internal-alpha`, and `local_tag_name=v2.0.0-alpha.internal.1` | pass | TWO-27 validates the default repo-local candidate package root and the local-candidate metadata path end to end. |
| internal-alpha diagnostics capture | isolated temp HOME plus package-installed bundle | `scripts/dev/retrofx-v2 diagnostics --pack modern-minimal --profile-id warm-night --label alpha-smoke --output-root <temp>` | local diagnostic bundle captures platform status, environment, install state, and selected profile evidence without touching 1.x paths | `ok=true`, diagnostics bundle included `capture-manifest.json`, `platform-status.json`, `environment.json`, `install-state.json`, `profile/resolved-profile.json`, `profile/session-plan.json`, and `profile/output-inventory.json` | pass | TWO-25 adds the controlled-alpha evidence capture path needed for real tester feedback. |
| post-alpha diagnostics remediation pass | isolated temp HOME plus package-installed bundle | `scripts/dev/retrofx-v2 diagnostics --pack modern-minimal --profile-id warm-night --label candidate --output-root <temp>` | diagnostics bundle is self-describing and captures repo plus installed-bundle provenance strongly enough for remediation triage | `ok=true`, `capture-manifest.json` lists itself, `source-control.json` is present, and the bundle includes `profile/install-bundle-inventory.json`, `profile/install-bundle-manifest.json`, and `profile/source-package-manifest.json` while retaining the current candidate release metadata | pass | TWO-27 revalidates the stronger diagnostics bundle against the current candidate package path. |
| temp HOME install | isolated temp HOME | `scripts/dev/retrofx-v2 install <bundle-path>` | bundle copied into isolated `retrofx-v2-dev` footprint with install record | `ok=true`, bundle dir under `~/.local/share/retrofx-v2-dev/bundles/modern-minimal--warm-night` | pass | Install remains user-local and isolated from 1.x. |
| temp HOME uninstall or cleanup | isolated temp HOME | `scripts/dev/retrofx-v2 uninstall modern-minimal--warm-night` | installed bundle removed, user config roots preserved | removed bundle and installation record; preserved `profiles/` and `packs/` config roots | pass | Uninstall ownership remains explicit and reversible. |
| delegated help clarity through unified surface | repo-local dev | `scripts/dev/retrofx-v2 resolve --help` and `scripts/dev/retrofx-v2 bundle --help` | help should clearly present the `retrofx-v2` surface | usage headers now begin with `retrofx-v2 resolve` and `retrofx-v2 bundle` rather than `cli.py` | pass | TWO-23 sets explicit `prog` names on the delegated CLI modules. |
| full 2.x test suite | repo-local dev | `./v2/tests/test.sh` | full suite passes | `Ran 134 tests in 1.990s` and `OK` | pass | Automated coverage still matches the current branch state after the TWO-27 candidate-preparation changes. |

## Interpretation

The implemented 2.x surface now validates well enough for controlled internal alpha use:

- core pipeline, packs, migration, compile, package, install, and bounded apply or off flows all passed
- environment planning degraded honestly in non-X11 contexts
- X11 render compilation preview is real across monochrome, palette, and passthrough modes

The remaining gaps are about confidence and polish, not broad missing implementation:

- explicit live X11 probing now has one real-host bounded validation run
- delegated help now presents the unified `retrofx-v2` surface coherently
- diagnostics evidence is now strong enough to capture repo-checkout provenance plus installed-bundle or package context for remediation work
- the default repo-local candidate package root now works as a reproducible machine-local output path without being mistaken for committed source
- broader multi-host and migration-corpus validation remains limited, which still argues against wider testing
