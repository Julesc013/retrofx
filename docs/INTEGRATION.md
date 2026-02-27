# Integration Guide

## X11 + i3 + picom

1. Generate active config:

```bash
./scripts/retrofx apply <profile>
```

2. Launch picom with repo-local active config:

```bash
(cd ./active && picom --config picom.conf)
```

3. Point your i3 startup picom command to `active/picom.conf`.

## TTY Backend (Profile Scoped)

Enable in profile:

```toml
[scope]
tty = true
```

Run apply normally:

```bash
./scripts/retrofx apply <profile>
```

Behavior:

- Generates ANSI16 semantic palette in `active/tty-palette.env`.
- Attempts console palette apply when safe.
- Falls back to mock mode when console write is unavailable.
- Stores rollback backups under `state/tty-backups/`.

Useful environment controls:

- `RETROFX_TTY_MODE=auto` (default)
- `RETROFX_TTY_MODE=mock` (no console write, test-safe)
- `RETROFX_TTY_MODE=apply` or `force` (attempt write)
- `RETROFX_TTY_DEVICE=/dev/ttyN`

TTY rollback only:

```bash
./scripts/retrofx off --tty
```

## Tuigreet Snippet Generation (Profile Scoped)

Enable in profile:

```toml
[scope]
tuigreet = true
```

Apply profile:

```bash
./scripts/retrofx apply <profile>
```

Generated file:

- `active/tuigreet.conf`

This file is a user-level snippet and does not modify global greetd config.

## Disable / Rollback

- Default passthrough:

```bash
./scripts/retrofx off
```

- Restore TTY palette only:

```bash
./scripts/retrofx off --tty
```

- Passthrough + TTY restore:

```bash
./scripts/retrofx off --all
```
