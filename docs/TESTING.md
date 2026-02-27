# RetroFX Testing

Run tests from the repository root.

## Quick Regression Run

```bash
./scripts/test.sh
```

Pass criteria:

- command exits `0`
- each profile in `profiles/*.toml` applies successfully
- `active/` contains `profile.toml`, `profile.env`, `picom.conf`, `shader.glsl`, `xresources`, and `meta`
- `apply -> off` returns to passthrough profile state
- `state/logs/retrofx.log` exists and receives entries

## Manual Command Checks

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx preview
```

## Optional Static Analysis

```bash
shellcheck scripts/retrofx scripts/test.sh
```

If `shellcheck` is unavailable, tests continue and print a skip message.

## Troubleshooting

- `picom not installed`
  - Expected in headless/minimal environments.
  - Runtime shader validation is skipped; generation and atomic swap should still work.
- `DISPLAY is not set`
  - Not in an X11 session.
  - `doctor` should warn, and `apply` should still render configs without launching runtime validation.
- shader/picom validation failure
  - `apply` fails safely.
  - RetroFX keeps or restores `active/` from `state/last_good/`.
  - Check `state/logs/retrofx.log` and stderr output for details.
- profile parse failure
  - Unknown keys/sections or invalid values are rejected.
  - Fix profile TOML and rerun `./scripts/retrofx apply <profile>`.
