# RetroFX 2.x Validation Matrix

This document records the first serious validation pass for the current 2.x experimental platform.

Validated on: 2026-03-21

Validation context:

- repo root: `/mnt/btrfs-data/projects/retrofx`
- unified entrypoint: `scripts/dev/retrofx-v2`
- actual host environment used for non-destructive baseline commands: repo-local dev on X11 with `i3`
- simulated environments used where appropriate: Wayland plus `sway`, and TTY or headless
- apply or install validation used temp HOME or isolated XDG roots under `/tmp`
- explicit live X11 `picom` probe was not run manually in this pass to avoid mutating an active session during validation

Status legend:

- `pass`
- `degraded-pass`
- `partial`
- `fail`
- `blocked`
- `not-tested`

Current summary:

- `pass`: 19
- `degraded-pass`: 2
- `partial`: 1
- `fail`: 0
- `blocked`: 0
- `not-tested`: 1

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
| explicit live X11 `picom` probe in real session | active X11 session | `scripts/dev/retrofx-v2 preview-x11 <profile> --probe-picom` | short-lived explicit live probe | not executed manually in TWO-22 | not-tested | Skipped intentionally to avoid mutating an active session during a validation prompt. Automated test coverage for the probe logic already exists. |
| bundle generation | repo-local dev | `scripts/dev/retrofx-v2 bundle --pack modern-minimal --profile-id warm-night --bundle-root <temp>` | deterministic bundle emitted | `ok=true`, bundle emitted under `<temp>/bundles/modern-minimal--warm-night` | pass | Pack-aware bundle generation now works through the unified surface. |
| temp HOME install | isolated temp HOME | `scripts/dev/retrofx-v2 install <bundle-path>` | bundle copied into isolated `retrofx-v2-dev` footprint with install record | `ok=true`, bundle dir under `~/.local/share/retrofx-v2-dev/bundles/modern-minimal--warm-night` | pass | Install remains user-local and isolated from 1.x. |
| temp HOME uninstall or cleanup | isolated temp HOME | `scripts/dev/retrofx-v2 uninstall modern-minimal--warm-night` | installed bundle removed, user config roots preserved | removed bundle and installation record; preserved `profiles/` and `packs/` config roots | pass | Uninstall ownership remains explicit and reversible. |
| delegated help clarity through unified surface | repo-local dev | `scripts/dev/retrofx-v2 resolve --help` and `scripts/dev/retrofx-v2 bundle --help` | help should clearly present the `retrofx-v2` surface | help works, but usage headers still show `cli.py` rather than `retrofx-v2 ...` | partial | Functional but still ambiguous enough to keep on the stabilization agenda. |
| full 2.x test suite | repo-local dev | `./v2/tests/test.sh` | full suite passes | `Ran 118 tests in 1.243s` and `OK` | pass | Automated coverage still matches the current branch state after TWO-22 changes. |

## Interpretation

The implemented 2.x surface now validates well enough for internal experimental use:

- core pipeline, packs, migration, compile, install, and bounded apply or off flows all passed
- environment planning degraded honestly in non-X11 contexts
- X11 render compilation preview is real across monochrome, palette, and passthrough modes

The remaining gaps are about confidence and polish, not broad missing implementation:

- the explicit live X11 probe still lacks manual real-session validation in this pass
- delegated help still leaks underlying module names
- broader legacy-profile and multi-host validation remains limited
