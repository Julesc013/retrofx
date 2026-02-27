# RetroFX Troubleshooting

## Quick Recovery

If state looks broken:

```bash
./scripts/retrofx self-check
./scripts/retrofx repair
```

To return to passthrough:

```bash
./scripts/retrofx off
./scripts/retrofx off --all
```

## picom Not Starting

- Run:
  - `./scripts/retrofx doctor`
- Common causes:
  - `picom` not installed
  - no active X11 `DISPLAY`
  - another compositor already running
- RetroFX still keeps generated files in `active/`; runtime validation is best-effort.

## Shader Compile/Validation Failures

- Run:
  - `./scripts/retrofx apply <profile>`
  - `./scripts/retrofx doctor`
  - `./scripts/retrofx self-check`
- On failure, RetroFX rolls back to `state/last_good/`.
- Ensure templates are intact under `templates/`.

## X11 vs Wayland Confusion

- Check:
  - `./scripts/retrofx doctor`
- On Wayland, global post-process shaders are intentionally not available.
- Wayland mode applies degraded outputs only (palette artifacts, optional tty/tuigreet).

## TTY Palette Not Applying

- Use mock mode for non-console testing:
  - `RETROFX_TTY_MODE=mock ./scripts/retrofx apply <profile>`
- Real apply requires writable tty device and compatible context.
- Check backups:
  - `state/tty-backups/`
  - `state/tty-current.env`

## Tuigreet Mismatch

- RetroFX only generates `active/tuigreet.conf`.
- It does not auto-edit greetd global config.
- Apply generated snippet manually to your greetd flow.

## Full Revert (User-Local Install)

```bash
retrofx uninstall --yes
```

If needed, remove managed xsession entries:

```bash
~/.config/retrofx/scripts/integrate/remove-xsession.sh --all-managed --yes
```
