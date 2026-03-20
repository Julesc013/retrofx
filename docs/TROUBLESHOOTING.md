# RetroFX Troubleshooting

## Quick Recovery

If state looks broken:

```bash
./scripts/retrofx self-check
./scripts/retrofx repair
```

`self-check` validates the current state against the artifact contract in `state/manifests/` when available. If a manifest is missing, it falls back to a conservative snapshot-derived check and warns that integrity metadata is incomplete.

Before first-time setup on a new machine:

```bash
./scripts/retrofx compatibility-check
```

For low-risk fallback apply:

```bash
./scripts/retrofx apply <profile> --safe
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

## Missing Required Generated Artifacts

- Typical examples:
  - `active/fontconfig.conf` for a font-enabled profile
  - `active/shader.glsl` or `active/picom.conf` for an X11 apply
- `self-check` now reports these as missing required artifacts instead of treating the whole tree generically.
- `repair` restores the last known-good snapshot when its contract still validates.

## Optional / Runtime Files

- Files such as `active/picom-compat.log` are treated as runtime-ephemeral.
- They may be missing or zero-byte without failing `self-check` on their own.
- Log/cache files under `state/` are not treated as direct health failures.

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

## Performance / Power Questions

- If `apply` feels slow:
  - run `./scripts/retrofx perf [profile]` to get stage timings in milliseconds.
- If repeated applies keep restarting work:
  - ensure you are applying the same profile file without local edits.
  - unchanged inputs should print `No changes; skipping apply.`
- For low-power or latency-sensitive sessions:
  - use passthrough/blur-free profiles when possible.
  - those profiles report `Compositor not required.` and avoid compositor backend application.
- Use `./scripts/retrofx doctor` to confirm current profile compositor requirements.
