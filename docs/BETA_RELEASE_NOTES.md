# RetroFX 0.1.0-beta.1 Release Notes

## 1) What RetroFX Is

RetroFX is a profile-driven rendering toolkit for retro-styled visual output with deterministic generation, atomic apply/off, rollback safety, and honest capability reporting across X11 and degraded Wayland paths.

## 2) Who Should Test It

- Linux users on X11 (especially i3 + picom).
- Users who can test degraded Wayland behavior honestly (no global compositor shader expectations).
- Users willing to provide reproducible logs and environment details.

## 3) Supported Environments

- Full path: X11 + picom + GLX.
- Degraded path: Wayland (palette/exports/session-local outputs only).
- Optional backends: TTY ANSI16 palette, tuigreet snippet generation.

## 4) How To Install

Repo mode:

```bash
./scripts/retrofx list
./scripts/retrofx apply <profile>
```

User-local install mode:

```bash
./scripts/retrofx install --yes
~/.local/bin/retrofx status
```

## 5) How To Revert

```bash
./scripts/retrofx off --all
./scripts/retrofx self-check
./scripts/retrofx repair
```

Installed mode full removal:

```bash
retrofx uninstall --yes
```

## 6) How To Report Issues

Include:

- `./scripts/retrofx --version`
- `./scripts/retrofx doctor --json`
- `./scripts/retrofx compatibility-check`
- failing profile file
- `state/logs/retrofx.log` excerpts
- whether `--safe` was used

## 7) Known Limitations

- No global Wayland shader support.
- No curvature or temporal persistence.
- TTY limited to 16 colors.
- Custom palettes limited to <=32 explicit entries.

## 8) Performance Expectations

- Single-pass shader pipeline with bounded loops.
- No frame history and no multi-pass effects.
- Apply path skips unchanged states and minimizes compositor churn.
- Use `./scripts/retrofx perf` and `./scripts/retrofx sanity-perf` for quick checks.

## 9) GPU Compatibility Notes

- Best results on systems where picom GLX backend works reliably.
- Use `./scripts/retrofx compatibility-check` before daily use.
- If shader runtime checks fail, use degraded/safe mode and report logs.
