# Integration Guide

## X11 + i3 + picom (Phase 1)

1. Generate active config:

```bash
./scripts/retrofx apply <profile>
```

2. Launch picom with active config from repo-local `active/`:

```bash
(cd ./active && picom --config picom.conf)
```

3. For i3 startup, point your user-level picom command to `active/picom.conf`.
   Keep all RetroFX artifacts inside this repository.

## Disable Effects

```bash
./scripts/retrofx off
```

`off` applies passthrough mode and keeps rollback snapshots.

## TTY and tuigreet

Phase 1 includes only no-op scaffolds (`backends/tty/apply.sh`, `backends/tuigreet/apply.sh`).
No system palette/theme writes are performed.

## Fonts and AA

RetroFX does not modify global fontconfig or DE defaults.
Session-local font hooks are intentionally deferred to future phases to avoid cross-DE breakage.
