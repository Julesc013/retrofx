# RetroFX Architecture

RetroFX is a profile-driven renderer that generates deterministic session-local artifacts under this repository and never touches system-wide configuration by default.

## Design Principles

- Deterministic generation from `profiles/*.toml`.
- Atomic apply: generate to temp -> validate -> backup -> rename swap.
- Fail-safe behavior: previous active config remains intact on failure.
- Modular backends: profile scope controls X11/TTY/tuigreet hooks.
- Performance-first shader path: ordered dithering only, lightweight effects.

## Repository Roles

- `scripts/retrofx`: CLI entrypoint and orchestrator.
- `profiles/*.toml`: strict v1 profile definitions.
- `templates/*`: static templates rendered into active artifacts.
- `active/`: currently active generated config.
- `state/backups/`: timestamped backups of previous `active/`.
- `state/last_good/`: last successful active snapshot.
- `backends/*`: backend-specific apply hooks.

## Apply Transaction

1. Parse profile with strict schema and unknown-key rejection.
2. Render shader/picom/xresources into `state/stage.*`.
3. Validate with a picom test instance when runtime conditions allow.
4. Backup current `active/` to `state/backups/<timestamp>-<profile>/`.
5. Swap `stage` into `active/` with `mv` rename semantics.
6. Refresh `state/last_good/` from new `active/`.
7. Trigger backend hooks for enabled scopes.

## Failure Handling

- Parse/render/validation failure: transaction aborts before swap.
- Swap failure: rollback to previous active snapshot.
- Shader/picom validation failures do not delete existing active config.
- `retrofx off` always maps to passthrough profile behavior.

## Backend Status

- `x11-picom`: functional in Phase 1 (config generation/check/run hook).
- `tty`: scaffold only (no-op with messaging).
- `tuigreet`: scaffold only (no-op with messaging).
- Wayland: documented as degraded future backend (not active in Phase 1).
