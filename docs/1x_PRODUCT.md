# RetroFX 1.x Product Truth

RetroFX 1.x is a profile-driven retro rendering and theming tool for Linux sessions. The supported core path is X11 + picom + GLX, with additional deterministic exports, scoped TTY and tuigreet outputs, user-local install mode, and explicit integrity/recovery tooling. Wayland and some integration paths are intentionally limited rather than pretending to offer universal compositor control.

## Supported

- Repo-local mode from a cloned repository.
- User-local install mode under `~/.config/retrofx`.
- Profile apply/off/status/doctor/self-check/repair.
- X11 + picom + GLX shader/runtime path.
- Terminal/theme exports (`xresources`, `alacritty`, semantic env files).
- Pack + user profile workflow, including pack-asset relocation into `profiles/user_assets/`.
- TTY ANSI16 palette backend.
- tuigreet snippet generation.
- Base16 import/export as a deterministic lossy bridge.

## Degraded Or Limited

- Wayland sessions:
  - no global shader/compositor path
  - palette/export/session-local outputs only
- X11 sessions outside the documented i3 wrapper flow:
  - core apply/export works
  - session integration is more manual
- TTY font apply:
  - best-effort only
  - depends on console access and `setfont`
- Base16 round-trip fidelity:
  - deterministic
  - not lossless
- greetd/display-manager integration:
  - generated snippets and Xsession helpers only
  - no automatic global config edits

## Export-Only Or Session-Local

- `retrofx export xresources ...`
- `retrofx export alacritty ...`
- `retrofx export base16 ...`
- `active/fontconfig.conf` via `scripts/integrate/retrofx-env.sh`
- `active/tuigreet.conf` as a generated snippet

## Command Surface Summary

- Inspect:
  - `--version`, `status`, `list`, `search`, `info`, `explain`, `gallery`, `preview`, `doctor`, `compatibility-check`
- Lifecycle:
  - `apply`, `apply --dry-run`, `off`, `self-check`, `repair`
- Profiles / interop:
  - `new`, `install-pack`, `import base16`, `export`
- Install mode:
  - `install`, `uninstall`
- Diagnostics:
  - `perf`, `sanity-perf`

Run `./scripts/retrofx --help` for the exact current CLI surface.

## Unsupported / Non-Goals For 1.x

- Global Wayland post-process shaders.
- Universal desktop theming/orchestration across GNOME, KDE Plasma, and other DE stacks.
- Automatic GTK/Qt/icon/cursor/theme mutation.
- Automatic greetd or system display-manager config edits.
- Lossless interchange with arbitrary theme formats.
- 2.0 appearance-compiler/platform work on the 1.x branch.

## Safety And Maturity

- Current repository version: `1.0.0`.
- Current maturity: 1.0 stable for the documented support matrix.
- Atomic apply, rollback snapshotting, manifest-based `self-check`, and `repair` are core 1.x guarantees.
- The automated suite remains strong for regressions, and the supported X11 path still depends on periodic real-host validation for future 1.0.x maintenance.
