# RetroFX Beta Notes (`1.0.0-beta.1`)

RetroFX `1.0.0-beta.1` is the first serious 1.x public beta candidate. The supported core path is X11 + picom + GLX. Everything else should be judged against that support boundary, not against a future 2.0 vision.

## Support Summary

- Supported:
  - X11 + picom + GLX
  - repo-local mode
  - user-local install mode
  - `apply`, `apply --dry-run`, `off`, `status`, `doctor`, `self-check`, `repair`, `explain`
  - TTY palette backend
  - tuigreet snippet generation
- Degraded:
  - Wayland sessions
  - manual WM/DE integration outside the documented i3 path
  - Base16 round-trip fidelity
  - TTY font apply
- Unsupported:
  - global Wayland shader compositing
  - automatic full desktop-environment theming/orchestration

See:

- `docs/1x_PRODUCT.md`
- `docs/CAPABILITIES.md`
- `docs/RELEASE_NOTES_1.0.0-beta.1.md`

## Safety / Recovery

- Verify integrity:
  - `./scripts/retrofx self-check`
- Repair from bad state:
  - `./scripts/retrofx repair`
- Disable effects:
  - `./scripts/retrofx off`
- Apply a lower-risk profile transform:
  - `./scripts/retrofx apply <profile> --safe`
- Preview the resolved runtime intent first:
  - `./scripts/retrofx explain <profile>`
  - `./scripts/retrofx apply <profile> --dry-run`

## Before Daily Use

```bash
./scripts/retrofx --version
./scripts/retrofx doctor
./scripts/retrofx compatibility-check
```

## Reporting Issues

Include:

- `./scripts/retrofx --version`
- `./scripts/retrofx doctor --json`
- `./scripts/retrofx compatibility-check`
- relevant profile file (`profiles/...`) and whether `--safe` was used
- excerpts from `state/logs/retrofx.log`
