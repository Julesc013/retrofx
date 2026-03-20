# RetroFX Environment Report Template

Use this alongside `docs/BUG_REPORT_TEMPLATE.md` when the problem looks environment-specific.

## RetroFX

- Version:
- Execution mode:
  - repo-local / installed
- Active profile:

## Session

- `XDG_SESSION_TYPE`:
- `DISPLAY`:
- `WAYLAND_DISPLAY`:
- WM/DE:
- login/session launcher:

## Graphics Stack

- GPU:
- driver:
- Mesa / vendor info:
- `picom --version`:

## Host

- Distro:
- Kernel:
- Shell:
- Terminal:

## Diagnostics To Capture

Paste the outputs of:

```bash
./scripts/retrofx --version
./scripts/retrofx doctor
./scripts/retrofx status
./scripts/retrofx compatibility-check
```

If relevant, also capture:

```bash
echo "$XDG_SESSION_TYPE"
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
picom --version
```

## Notes

- Is the problem specific to one profile or all supported X11 profiles?
- Does `passthrough` behave correctly?
- Does `./scripts/retrofx apply <profile> --dry-run` already show the problem?
