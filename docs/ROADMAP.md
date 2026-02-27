# RetroFX Roadmap

## Phase 1 (Implemented)

- Profile-driven renderer (`passthrough`, `monochrome`, `palette`).
- Shader features: ordered dithering, scanlines, flicker, vignette, hotcore, phosphor tint, tone transform.
- Structured palettes: `vga16`, `cube256`.
- Atomic apply with validation, backup, and rollback-safe behavior.
- CLI commands: `list`, `apply`, `off`, `doctor`, `preview`, `new`.
- X11 + picom backend support.

## Phase 1 Scaffolds (Present)

- TTY backend apply hook placeholder.
- tuigreet backend apply hook placeholder.
- Wayland degraded mode documented (not enabled yet).

## Phase 2 (Planned)

- TTY palette application with reversible session helpers.
- tuigreet theme materialization hooks.
- Wayland degraded backend (no custom shader assumptions).
- Session-local font hook execution chain with AA mode toggles.
- Expanded integration tests for profile matrix and failure injection.
