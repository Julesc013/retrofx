# RetroFX 1.0.0-beta.1 Release Notes

`1.0.0-beta.1` is the first serious 1.x public beta candidate. It is intended for users who can test the supported X11 path honestly, report issues with logs and profiles, and tolerate beta-level rough edges outside the documented support matrix.

## What RetroFX 1.x Is

RetroFX 1.x is a profile-driven retro rendering and theming tool for Linux sessions. The supported core path is X11 + picom + GLX, with deterministic terminal/theme exports, scoped TTY and tuigreet outputs, user-local install mode, and explicit recovery tooling.

## Intended Audience

- Linux users on X11 who want profile-driven retro rendering effects.
- Testers who can validate i3 + picom + GLX behavior on real hardware.
- Users who want deterministic exports, profile packs, and rollback-oriented state handling.
- Operators who prefer explicit recovery tools over hidden system mutation.

## Supported Environments

- Repo-local usage from a cloned tree.
- User-local install mode under `~/.config/retrofx`.
- X11 + picom + GLX runtime path.
- TTY ANSI16 palette backend.
- tuigreet snippet generation.
- `apply`, `off`, `status`, `doctor`, `compatibility-check`, `self-check`, `repair`, `explain`, and `apply --dry-run`.
- Pack installs and Base16 JSON import/export as implemented in 1.x.

## Degraded / Limited Environments

- Wayland sessions:
  - no global shader/compositor path
  - palette/export/session-local outputs only
- X11 environments outside the documented i3 wrapper path:
  - core apply/export logic still works
  - integration is more manual
- TTY font apply:
  - best-effort only
  - host-console dependent
- Base16 round-trip fidelity:
  - deterministic
  - intentionally lossy

## Install Methods

Repo-local:

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
```

User-local install:

```bash
./scripts/retrofx install --yes
~/.local/bin/retrofx status
```

## Recovery / Revert

```bash
./scripts/retrofx self-check
./scripts/retrofx repair
./scripts/retrofx off
./scripts/retrofx off --all
```

- `self-check` validates runtime state against the artifact contract.
- `repair` restores a manifest-valid `last_good` snapshot or falls back conservatively.
- `off` returns to a passthrough baseline without removing the install itself.

## Known Limitations

- No global Wayland shader support.
- No automatic broad desktop-environment theming/orchestration.
- No automatic greetd or other system display-manager configuration edits.
- TTY output remains 16-color semantic output.
- Base16 interop is a best-effort semantic bridge, not a lossless round-trip format.

## Recommended First-Run Commands

```bash
./scripts/retrofx --version
./scripts/retrofx doctor
./scripts/retrofx compatibility-check
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
```

## Issue Reporting Guidance

Include:

- `./scripts/retrofx --version`
- `./scripts/retrofx doctor --json`
- `./scripts/retrofx compatibility-check`
- the relevant profile file
- whether `--safe` or `--dry-run` was used
- excerpts from `state/logs/retrofx.log`
