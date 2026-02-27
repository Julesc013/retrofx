# Integration Guide

## X11 i3 Session Wrapper (Optional)

RetroFX now ships optional wrappers in `scripts/integrate/`:

- `i3-retro-session.sh`
- `generate-xsession.sh`

`i3-retro-session.sh` behavior:

1. Picks profile in this order:
   - explicit argument
   - `RETROFX_PROFILE` env
   - `crt-green-4band` if present
   - `passthrough` fallback
2. Runs `./scripts/retrofx apply <profile>`
3. Starts picom with `active/picom.conf` when available
4. `exec i3`

If `retrofx apply` fails, it logs a warning and still starts plain i3.

Run directly from repo:

```bash
./scripts/integrate/i3-retro-session.sh
```

## User-Local Xsession Entry (No Root)

Generate an Xsession desktop entry under `~/.local/share/xsessions/`:

```bash
./scripts/integrate/generate-xsession.sh --name "RetroFX i3"
```

This creates:

- `~/.local/share/xsessions/retrofx-i3.desktop`

The `Exec` path is absolute and points to this repository wrapper script.

## greetd + tuigreet Selection

If your tuigreet setup chooses entries from `.desktop` sessions, select:

- the generated `RetroFX i3` entry, or
- your existing `Default.desktop` flow that chains to an i3 startup script.

RetroFX does not modify global greetd configuration. `active/tuigreet.conf` is only a generated snippet.

## Wayland Degraded Integration (Honest Mode)

When Wayland is detected (`WAYLAND_DISPLAY` set), `retrofx apply` uses degraded mode:

- no picom/shader targets generated in `active/`
- no compositor shader pipeline claimed
- terminal palette artifacts still generated (`xresources`, `semantic.env`, `tty-palette.env`)
- optional scoped backends still honored:
  - TTY palette backend
  - tuigreet snippet generation

Expected message:

`Wayland session detected: shader pipeline disabled; applied degraded outputs only.`

## Optional Toolkit Env Hooks (Print Only)

These scripts print suggested env vars and do not apply system changes:

- `./scripts/integrate/x11-env.sh`
- `./scripts/integrate/wayland-env.sh`

Example:

```bash
eval "$(./scripts/integrate/wayland-env.sh)"
```

## Rollback / Disable

Default rollback to passthrough profile:

```bash
./scripts/retrofx off
```

TTY palette only rollback:

```bash
./scripts/retrofx off --tty
```

Profile + TTY rollback:

```bash
./scripts/retrofx off --all
```

In Wayland degraded sessions, `retrofx off` also attempts TTY restore when the previous active profile had `scope.tty = true`.
