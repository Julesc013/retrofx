# RetroFX Capabilities Matrix

## X11

Support level: full pipeline (when `picom` + GLX are available)

- Profile-driven shader generation (`shader.glsl`)
- Picom config generation (`picom.conf`)
- Runtime validation checks (best-effort)
- Structured arithmetic palettes (`2..256` families)
- Custom palettes up to 32 colors
- Optional per-window blur exclusion rules via picom config hints
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
  - session-local fontconfig output (`active/fontconfig.conf`) when requested
  - optional TTY backend
  - optional tuigreet snippet generation
  - optional toolkit env suggestion scripts (`scripts/integrate/*-env.sh`)

Font note:

- `FONTCONFIG_FILE` can affect Wayland and Xwayland clients launched from that environment, but behavior varies by toolkit/app.

Out of scope:

- Universal compositor shader injection for Wayland sessions
- System-wide GTK/Qt settings mutation
- Editing `/etc` or root-level display manager configuration by default
- Guaranteed per-window shader exclusion (picom limitations)

## TTY

Support level: optional 16-color semantic palette backend

- Applies ANSI16 palette when safe
- Mock mode for test/non-console environments
- Rollback stack under `state/tty-backups/`

## Tuigreet

Support level: optional snippet generation

- Generates `active/tuigreet.conf`
- No direct global greetd config edits
