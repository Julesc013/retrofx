# RetroFX Capabilities Matrix

## X11

Support level: full pipeline (when `picom` + GLX are available)

- Profile-driven shader generation (`shader.glsl`)
- Picom config generation (`picom.conf`)
- Runtime validation checks (best-effort)
- Terminal semantic palette artifacts
- Optional TTY backend (`scope.tty = true`)
- Optional tuigreet snippet (`scope.tuigreet = true`)

Notes:

- Full shader capability depends on runtime (`picom`, GLX support, compositor constraints).
- If requirements are missing, RetroFX remains fail-safe and keeps prior good state.

## Wayland

Support level: degraded (honest capability mode)

- Global post-process shaders are **not** supported in this backend.
- RetroFX does not claim wlroots/sway-wide shader compositing.
- RetroFX still provides:
  - terminal palette artifacts (`xresources`, `semantic.env`, `tty-palette.env`)
  - optional TTY backend
  - optional tuigreet snippet generation
  - optional toolkit env suggestion scripts (`scripts/integrate/*-env.sh`)

Out of scope:

- Universal compositor shader injection for Wayland sessions
- System-wide GTK/Qt settings mutation
- Editing `/etc` or root-level display manager configuration by default

## TTY

Support level: optional 16-color semantic palette backend

- Applies ANSI16 palette when safe
- Mock mode for test/non-console environments
- Rollback stack under `state/tty-backups/`

## Tuigreet

Support level: optional snippet generation

- Generates `active/tuigreet.conf`
- No direct global greetd config edits
