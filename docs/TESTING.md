# RetroFX Testing

Run tests from repository root.

For product scope and support boundaries, see:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`

## Full Regression

```bash
./scripts/test.sh
```

Pass criteria: command exits `0`.

`scripts/test.sh` is intentionally organized around release-critical categories:

- Parsing / CLI surface:
  - `--version`, `list`, `gallery`, `search`, `info`, `explain`, `--help`
  - profile parsing, wizard generation, command help surface
- Generation / static output:
  - export commands
  - shader static checks
  - profile apply matrix
  - rules/picom template generation
  - font/alacritty/fontconfig generation
- Artifact / integrity / repair:
  - manifest-aware `self-check`
  - zero-byte optional/runtime artifacts do not fail
  - missing or zero-byte required artifacts do fail
  - export-only gaps stay non-fatal for runtime integrity
  - `repair` restores manifest-valid `state/last_good/`
  - apply/off manifest transitions stay coherent
- Operator safety:
  - `apply --dry-run` must not mutate `active/`, manifests, or backups
  - mutating commands must report clear skip/repair/success states
- Wrapper / runtime intent:
  - compositor-required vs no-compositor wrapper policy
  - `scope.x11=false` suppresses X11 runtime outputs
  - stale X11 artifacts do not define active state
  - degraded Wayland state does not pretend to be full X11 runtime
- Install / pack / path:
  - `install-pack` relocation for pack-local assets
  - isolated `install --yes` / `uninstall --yes` cycle
  - installed launcher health/status behavior
- Interop:
  - Base16 import creates usable user profile + palette files
  - Base16 export is deterministic and emits the documented metadata
  - Base16 round-trip follows the documented lossy contract
  - invalid Base16 colors are rejected
- Backend / degraded mode:
  - Wayland degraded apply path omits `active/picom.conf` and `active/shader.glsl`
  - TTY mock-mode backend checks pass
  - tuigreet snippet generation check passes
  - doctor capability output matches simulated X11/Wayland expectations

## Execution Model

The suite is designed to stay runnable in repo-local mode without a full live desktop session.

- Simulated session environment:
  - X11-sensitive command paths use `DISPLAY=:99` and `XDG_SESSION_TYPE=x11`
  - Wayland-sensitive command paths use `WAYLAND_DISPLAY=wayland-0` and `XDG_SESSION_TYPE=wayland`
- Mocked integrations:
  - session wrapper tests stub `picom`, `i3`, and `pgrep`
  - TTY backend tests use `RETROFX_TTY_MODE=mock`
- Static validation:
  - shader output, manifest state, generated files, and interop files are checked directly on disk
- Optional host-sensitive validation:
  - live X11/picom shader validation only happens when the host actually supports it
  - if the environment lacks a reachable X11 server or `picom`, RetroFX warns and the suite continues with simulated/static coverage

## Confidence And Limits

- Passing `./scripts/test.sh` is necessary for 1.x release confidence.
- Passing `./scripts/test.sh` is not sufficient for final release confidence.
- Final release validation still needs host checks for:
  - live X11 + picom + GLX behavior
  - compositor startup in a real session
  - any desktop-environment-specific integration not covered by the mocked wrapper tests

## Manual Command Checks

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx preview
```

Doctor simulation examples (no real X server required):

```bash
DISPLAY=:99 WAYLAND_DISPLAY= XDG_SESSION_TYPE=x11 ./scripts/retrofx doctor
DISPLAY= WAYLAND_DISPLAY=wayland-0 XDG_SESSION_TYPE=wayland ./scripts/retrofx doctor
```

## Optional Static Analysis

```bash
shellcheck scripts/retrofx scripts/test.sh backends/tty/apply.sh backends/tuigreet/apply.sh
```

If `shellcheck` is unavailable, tests continue with a skip message.

## CI-Friendly Runner

Run the local CI wrapper:

```bash
./scripts/ci.sh
```

It runs:

- `./scripts/test.sh`
- `shellcheck` (if available)
- script LF/executable-bit checks

## TTY Backend Test Mode

Use mock mode to avoid real console writes:

```bash
RETROFX_TTY_MODE=mock ./scripts/retrofx apply <profile-with-tty-scope>
```

Mock mode still validates palette generation, semantic mapping, and rollback files.

## Integrity Regression Cases

`scripts/test.sh` includes explicit integrity regressions for:

- zero-byte optional runtime artifacts such as `active/picom-compat.log`
- missing required generated artifacts such as `active/fontconfig.conf`
- zero-byte required generated artifacts such as `active/shader.glsl`
- export-only gaps such as missing `active/xresources`
- install-asset damage in isolated installed homes
- manifest-aware `repair` restoring from `state/last_good/`
- apply/off manifest contract transitions for current runtime state
- `scope.x11=false` stale-artifact rejection

## Troubleshooting

- `picom not installed`
  - Expected in headless/minimal environments.
  - Runtime shader validation is skipped; static validation still runs.
- `DISPLAY is not set`
  - X11 runtime checks are skipped.
- `Global post-process shaders are not supported in this backend.`
  - Expected in Wayland mode; this is intentional degraded support.
  - Terminal palette outputs, TTY, and tuigreet generation still work.
- `tty backend apply failed`
  - Use `RETROFX_TTY_MODE=mock` for non-console sessions.
  - Check `state/tty-backups/` and `state/tty-current.env`.
- `tuigreet backend` warning
  - Main apply still succeeds; inspect `active/semantic.env` and `active/tuigreet.conf` generation preconditions.
- profile parse failure
  - Unknown keys/sections or invalid values are rejected.
