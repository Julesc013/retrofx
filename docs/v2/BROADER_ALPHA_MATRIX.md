# RetroFX 2.x Broader Alpha Matrix

This matrix records the broader-alpha-oriented validation pass carried forward through TWO-32.

It does not replace [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md).
It extends the branch evidence with broader environment and surface classification.

Validated on: 2026-03-22

Evidence sources:

- [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md)
- `scripts/dev/retrofx-v2 status`
- `./v2/tests/test.sh`
- TWO-28, TWO-29, and TWO-30 scenario reruns under `/tmp/retrofx-v2-two28-*`, `/tmp/retrofx-v2-two29-*`, and `/tmp/retrofx-v2-two30-*`
- latest tagged internal candidate `v2.0.0-alpha.internal.1`
- current internal-alpha hardening version `2.0.0-alpha.internal.2`
- current limited public technical-beta candidate version `2.0.0-techbeta.1`

Status legend:

- `pass`
- `degraded-pass`
- `partial`
- `fail`
- `blocked`
- `not-tested`

Current summary:

- `pass`: 18
- `degraded-pass`: 5
- `partial`: 0
- `fail`: 0
- `blocked`: 0
- `not-tested`: 0

## Matrix

| Scenario | Environment | Command/Entry Path | Expected Result | Actual Result | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| CRT family resolve and compile | repo-local dev | `scripts/dev/retrofx-v2 compile --pack crt-core --profile-id green-crt --target xresources --out-root <temp>` | pack-aware CRT profile compiles deterministically | current branch evidence still shows deterministic CRT compile output | pass | Inherited from the current validated compiler surface. |
| palette family X11 render preview | simulated X11 | `scripts/dev/retrofx-v2 preview-x11 v2/tests/fixtures/vga-like-palette.toml --out-root <temp>` | palette-mode shader and picom artifacts emit | current branch evidence still shows `implemented_mode=palette` | pass | Inherited from the bounded X11 render validation surface. |
| minimal or warm-night pack planning | repo-local dev plus simulated Wayland | `scripts/dev/retrofx-v2 plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | modern pack profile resolves and plans honestly | current branch evidence shows `sway` remains the only Wayland preview target and toolkit-facing outputs remain plan-visible while X11 runtime targets degrade honestly | pass | Core modern/minimal profile family remains solid. |
| migrated 1.x palette profile inspection | repo-local dev | `scripts/dev/retrofx-v2 migrate inspect-1x profiles/packs/core/ibm-vga16.toml --compact` | explicit clean, degraded, and manual mapping summary | `ok=true`, mapped cleanly `15`, degraded `7`, manual `6`, unsupported `0` | pass | Migration remains honest but still not broad. |
| pack-aware profile resolution | repo-local dev | `scripts/dev/retrofx-v2 resolve --pack crt-core --profile-id green-crt` | pack metadata and origin resolve deterministically | pack origin remains explicit and deterministic | pass | Pack system remains ready for internal use. |
| terminal or TUI outputs | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/strict-green-crt.toml --target xresources --target alacritty --out-root <temp>` | deterministic terminal artifacts | current branch evidence still shows deterministic terminal output | pass | Inherited from the existing matrix and green suite. |
| WM outputs on validated environments | simulated X11 plus `i3`, simulated Wayland plus `sway` | `scripts/dev/retrofx-v2 plan ...` and `compile ... --target i3 --target sway` | WM outputs compile; live-preview candidates remain environment-specific | current branch evidence still shows `i3` preview only on X11 and `sway` preview only on sway-like Wayland | pass | Honest environment split remains intact. |
| toolkit exports | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/retro-desktop-explicit.toml --target gtk-export --target qt-export --target icon-cursor --target desktop-style --out-root <temp>` | advisory toolkit artifacts compile deterministically | current branch evidence still shows export-oriented GTK, Qt, icon-cursor, and desktop-style artifacts | pass | Advisory only; not live desktop ownership. |
| typography outputs | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/warm-night-theme-only.toml --target fontconfig --out-root <temp>` | typography artifacts remain deterministic | current branch evidence still shows deterministic fontconfig output and resolved typography roles | pass | Typography remains export-oriented. |
| display-policy outputs | repo-local dev | `scripts/dev/retrofx-v2 compile v2/tests/fixtures/strict-green-display-policy.toml --target x11-display-policy --out-root <temp>` | display-policy artifact remains deterministic | current branch evidence still shows display-policy JSON and env artifact output | pass | Display policy remains advisory/export-oriented. |
| X11+i3-like planning and preview | actual X11 plus `i3` host | `scripts/dev/retrofx-v2 status` and `preview-x11 ... --probe-picom --probe-seconds 1.0` | X11 path reports as bounded and explicit | `status` still reports X11 plus `i3`, `ready_for_broader_alpha=false`, and the rerun bounded probe returned `probe.status=timed-out` against the generated `picom.conf` | pass | Real-host evidence remains strongest here, but still internal-only. |
| Wayland+sway-like planning | simulated Wayland plus `sway` | `scripts/dev/retrofx-v2 plan v2/tests/fixtures/warm-night-theme-only.toml --write-preview --out-root <temp>` | honest degradation with sway-only preview candidates | current branch evidence still shows `apply_preview_targets=['sway']` with degraded X11 targets | degraded-pass | Export-oriented validation is usable here; live runtime breadth is still limited. |
| Wayland+GNOME-like planning | forced Wayland plus `gnome` | `RETROFX_V2_FORCE_WM_OR_DE=gnome scripts/dev/retrofx-v2 plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | explicit export-only warning for non-validated Wayland desktop | `apply_preview_targets=[]`, environment warns that Wayland `gnome` is not part of the validated live-preview set | degraded-pass | TWO-28 adds the explicit warning instead of leaving this implicit. |
| Wayland+Plasma-like planning | forced Wayland plus `plasma` | `RETROFX_V2_FORCE_WM_OR_DE=plasma scripts/dev/retrofx-v2 plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | explicit export-only warning for non-validated Wayland desktop | `apply_preview_targets=[]`, environment warns that Wayland `plasma` is not part of the validated live-preview set | degraded-pass | This remains an export-oriented validation path only. |
| TTY or headless planning | forced TTY | `RETROFX_V2_FORCE_SESSION_TYPE=tty scripts/dev/retrofx-v2 plan --pack crt-core --profile-id green-crt --write-preview --out-root <temp>` | no fake live apply path | `apply_preview_targets=[]` and GUI-facing targets degrade honestly | degraded-pass | Conservative behavior remains correct. |
| bounded apply or off | temp HOME, safe contexts only | `scripts/dev/retrofx-v2 apply`, `status`, `off` | 2.x-owned state only, deterministic cleanup | `apply` on `warm-night-theme-only.toml` staged activation with `live_applied_targets=[]`; `status` reported the activation; `off` removed only `active/current` and `current-state.json` while preserving manifests and install roots | pass | Trust remains bounded to internal-safe contexts. |
| install, diagnostics, and uninstall | temp HOME install mode | `package-alpha`, `install`, `diagnostics`, `uninstall` | isolated install-state and reproducible diagnostics | install succeeded under `retrofx-v2-dev`, diagnostics captured release-status plus installed-bundle evidence, and uninstall removed only the bundle and installation record while preserving user config roots | pass | This is the strongest packaging/distribution surface currently available. |
| broader-alpha package shape | repo-local dev | `scripts/dev/retrofx-v2 package-alpha ...` | if broader-alpha ready, package metadata would say so | current package manifest still says `status_label=internal-alpha`, `version=2.0.0-alpha.internal.2`, `current_build_kind=untagged-post-alpha-hardening`, `ready_for_broader_alpha=false`, and `pre_beta_candidate_ready=false` | pass | Honest narrowing remains the intended result in TWO-29 and TWO-30. |
| public-looking package override fence | repo-local dev | `scripts/dev/retrofx-v2 package-alpha --pack modern-minimal --profile-id warm-night --status-label pre-beta` | public-looking package metadata should be rejected clearly | current branch evidence now shows `ok=false` with `errors[0].code=blocked-package-status-label` instead of minting misleading metadata | pass | TWO-31 keeps the internal package surface from pretending to be pre-beta or public-facing. |
| limited technical-beta wrapper surface | clean temp repo and copied-toolchain candidate package | `scripts/dev/retrofx-v2-techbeta --help`, `status`, and `package-technical-beta ...` | a narrower outside-facing surface exists without exposing the broader internal CLI | the wrapper exposes only curated advanced-tester commands; status reports `version=2.0.0-techbeta.1`, `status_label=technical-beta`, and `ready_for_limited_public_technical_beta=true`; package generation emits a copied-toolchain candidate under `retrofx-v2--2.0.0-techbeta.1--modern-minimal--warm-night` | pass | TWO-32 makes broader-alpha readiness less central by giving outside testers a smaller, more supportable surface. |
| limited technical-beta degraded Wayland plan | copied-toolchain candidate under simulated Wayland plus `sway` | `bin/retrofx-v2-techbeta plan --pack modern-minimal --profile-id warm-night --write-preview --out-root <temp>` | Wayland remains explicitly degraded/export-only rather than being overclaimed as supported live runtime | packaged wrapper planned successfully and reported honest degradation for X11-only runtime pieces | degraded-pass | This keeps the outside-facing support promise aligned with current implementation reality. |
| full 2.x suite after TWO-32 candidate prep | repo-local dev | `./v2/tests/test.sh` | suite remains green after adding the narrower technical-beta surface | `Ran 143 tests in 2.743s` and `OK` | pass | Final suite pass confirms the candidate wrapper and copied-toolchain package did not regress the implemented branch. |

## Interpretation

The branch remains unsuitable for the older broader-alpha framing, but it is no longer limited to internal-only circulation.

Broader alpha is still not the right next-stage label because:

- the strongest live-validation evidence still centers on one real X11 plus `i3` host
- non-sway Wayland desktops remain explicitly fenced as export-oriented validation paths
- migration validation breadth remains limited

The immediate value of TWO-32 is a narrower outside-facing promise:

- advanced testers now have a copied-toolchain candidate surface that does not require source-tree archaeology
- the broader internal developer surface remains available, but it is no longer the recommended outside-facing entrypoint
- broader-alpha language remains too wide for the current evidence, even though the limited public technical-beta candidate now clears its own narrower gates
