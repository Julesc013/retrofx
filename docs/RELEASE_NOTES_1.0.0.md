# RetroFX 1.0.0 Release Notes

RetroFX 1.0.0 is the first stable 1.x release for the documented support matrix. It is a profile-driven retro rendering and theming tool for Linux sessions with a supported X11 + picom + GLX path, deterministic terminal/theme exports, scoped TTY and tuigreet outputs, user-local install mode, and explicit recovery tooling.

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

## Installation Paths

Repo-local:

```bash
./scripts/retrofx doctor
./scripts/retrofx compatibility-check
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
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

## Recommended First-Run Flow

```bash
./scripts/retrofx --version
./scripts/retrofx doctor
./scripts/retrofx compatibility-check
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx status
```

## Upgrade Notes From Beta / RC

- No profile-schema reset is required for the supported 1.x workflow.
- Re-run `./scripts/retrofx doctor`, `./scripts/retrofx compatibility-check`, and `./scripts/retrofx self-check` after upgrading from prerelease builds.
- If you had local beta release archives, regenerate or replace them with the `1.0.0` stable artifacts before publication.

## Intended Audience

- Linux users who want a supported X11 + picom + GLX retro rendering workflow.
- Operators who want deterministic exports, profile packs, and rollback-oriented state handling.
- Users who prefer explicit recovery tools over hidden system mutation.
