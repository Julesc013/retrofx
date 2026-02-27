# RetroFX Beta Notes (`0.1.0-beta`)

## Supported Environments

- X11 sessions with picom + GLX: full RetroFX shader pipeline.
- Wayland sessions: degraded mode only (palette/export/session-local outputs).
- TTY backend: optional ANSI16 palette path.
- Tuigreet backend: generated snippet integration only.

Use `./scripts/retrofx compatibility-check` and `./scripts/retrofx doctor` before daily use.

## Known Limitations

- No global Wayland post-process shader pipeline.
- No curvature/warp effects.
- No temporal persistence/frame-history effects.
- TTY output is limited to 16-color semantics.
- Custom palettes above 32 colors are not supported.

## Safety / Recovery

- Verify state integrity:
  - `./scripts/retrofx self-check`
- Repair from corruption or bad state:
  - `./scripts/retrofx repair`
- Disable effects quickly:
  - `./scripts/retrofx off`
- Apply low-risk profile transforms:
  - `./scripts/retrofx apply <profile> --safe`

## Full Revert

Repo-local:
- `./scripts/retrofx off --all`

Installed mode:
- `retrofx uninstall --yes`

## Reporting Issues

When filing a bug report, include:
- `./scripts/retrofx --version`
- `./scripts/retrofx doctor --json`
- `./scripts/retrofx compatibility-check`
- relevant profile file (`profiles/...`) and whether `--safe` was used
- excerpts from `state/logs/retrofx.log`
