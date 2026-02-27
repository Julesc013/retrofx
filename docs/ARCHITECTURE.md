# RetroFX Architecture

RetroFX is a profile-driven renderer that generates deterministic session-local artifacts under this repository and never touches system-wide configuration by default.

## Design Principles

- Deterministic generation from `profiles/*.toml`.
- Atomic apply: generate to temp -> validate -> backup -> rename swap.
- Fail-safe behavior: rollback to `state/last_good/` on failed transactions.
- Modular backends: profile scope controls X11/TTY/tuigreet hooks.
- Performance-first shader path: ordered dithering only, lightweight effects.

## Repository Roles

- `scripts/retrofx`: CLI entrypoint and orchestrator.
- `scripts/test.sh`: minimal regression harness.
- `profiles/*.toml`: strict v1 profile definitions.
- `templates/*`: static templates rendered into active artifacts.
- `active/`: currently active generated config.
- `state/backups/`: timestamped backups of previous `active/` (pruned to last N, default 10).
- `state/last_good/`: canonical rollback snapshot.
- `state/logs/retrofx.log`: append-only operational audit log.
- `backends/*`: backend-specific apply hooks.

## Apply Transaction

1. Parse and validate profile with strict schema and unknown-key rejection.
2. Render shader/picom/xresources/profile metadata into `state/stage.*`.
3. Validate with a picom test instance when runtime conditions allow.
4. Backup current `active/` to `state/backups/<timestamp>-<profile>/`.
5. Atomically rename staged output into `active/`.
6. Refresh `state/last_good/` from new `active/`.
7. Prune backup retention.
8. Trigger backend hooks for enabled scopes.

## Failure Handling

- Parse/render/validation failure: transaction aborts and rollback is attempted from `state/last_good/`.
- Swap failure: previous `active/` is restored immediately.
- Logging failures are best-effort and never fail user commands.
- `retrofx off` always maps to passthrough mode (`profiles/passthrough.toml` or built-in fallback).

## Backend Status

- `x11-picom`: functional in Phase 1 (config generation/check/run hook).
- `tty`: scaffold only (no-op with messaging).
- `tuigreet`: scaffold only (no-op with messaging).
- Wayland: documented as degraded future backend (not active in Phase 1).
