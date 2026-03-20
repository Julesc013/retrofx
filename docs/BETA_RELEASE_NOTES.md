# RetroFX 0.1.0-beta.1 Release Notes

This beta is about stabilization, not feature expansion.

## What This Beta Covers

- Supported core path:
  - X11 + picom + GLX
- Degraded but intentional paths:
  - Wayland palette/session-local outputs
  - manual integration outside the documented i3 wrapper flow
- Safety and recovery:
  - atomic apply/off
  - `state/last_good/`
  - manifest-based `self-check`
  - `repair`

## Canonical Truth Docs

Use these as the current source of truth:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`
- `docs/TESTING.md`

## How To Try It

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx apply <profile>
./scripts/retrofx status
```

User-local install mode:

```bash
./scripts/retrofx install --yes
~/.local/bin/retrofx status
```

## Recovery

```bash
./scripts/retrofx off --all
./scripts/retrofx self-check
./scripts/retrofx repair
```

## Known Limits

- No global Wayland shader support.
- No automatic broad desktop-environment theming.
- Base16 import/export is intentionally lossy.
- TTY output remains 16-color semantic output.

## Reporting Issues

Include:

- `./scripts/retrofx --version`
- `./scripts/retrofx doctor --json`
- `./scripts/retrofx compatibility-check`
- failing profile file
- `state/logs/retrofx.log` excerpts
- whether `--safe` was used
