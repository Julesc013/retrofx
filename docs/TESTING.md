# RetroFX Testing

Run tests from repository root.

## Full Regression

```bash
./scripts/test.sh
```

Pass criteria:

- command exits `0`
- profile applies generate expected active artifacts
- shader static checks pass
- semantic ANSI mapping files are generated and valid
- TTY mock-mode backend checks pass (no console access needed)
- tuigreet snippet generation check passes
- `apply -> off` restores passthrough profile state

## Manual Command Checks

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx preview
```

## Optional Static Analysis

```bash
shellcheck scripts/retrofx scripts/test.sh backends/tty/apply.sh backends/tuigreet/apply.sh
```

If `shellcheck` is unavailable, tests continue with a skip message.

## TTY Backend Test Mode

Use mock mode to avoid real console writes:

```bash
RETROFX_TTY_MODE=mock ./scripts/retrofx apply <profile-with-tty-scope>
```

Mock mode still validates palette generation, semantic mapping, and rollback files.

## Troubleshooting

- `picom not installed`
  - Expected in headless/minimal environments.
  - Runtime shader validation is skipped; static validation still runs.
- `DISPLAY is not set`
  - X11 runtime checks are skipped.
- `tty backend apply failed`
  - Use `RETROFX_TTY_MODE=mock` for non-console sessions.
  - Check `state/tty-backups/` and `state/tty-current.env`.
- `tuigreet backend` warning
  - Main apply still succeeds; inspect `active/semantic.env` and `active/tuigreet.conf` generation preconditions.
- profile parse failure
  - Unknown keys/sections or invalid values are rejected.
