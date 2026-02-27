# RetroFX

RetroFX is a profile-driven retro rendering toolkit with deterministic generation, atomic apply/off, rollback safety, and honest backend capability reporting.

Current release: `0.1.0`

## What It Does

- Applies profile-defined visual pipelines for X11 + picom (full path).
- Supports degraded Wayland mode (palette/export/session-safe outputs only).
- Generates terminal/theming artifacts (`alacritty`, `Xresources`, semantic ANSI mapping).
- Supports scoped backends: X11, TTY palette, and tuigreet theme snippets.
- Maintains rollback snapshots and audit logs under `state/`.

## Core Guarantees

- Atomic apply: stage -> validate -> swap.
- Safe rollback to `state/last_good` on failure.
- Deterministic template/profile rendering.
- No destructive system-wide changes by default.
- Bounded shader complexity and predictable performance.

## Quick Start (Repo-Local)

```bash
# List profiles (core pack + user)
./scripts/retrofx list

# Preview current/target profile in terminal
./scripts/retrofx preview
./scripts/retrofx preview crt-green-p1-4band

# Apply / disable
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx off

# Diagnose environment
./scripts/retrofx doctor
./scripts/retrofx doctor --json

# Run full local CI checks
./scripts/ci.sh
```

## Main Commands

```bash
./scripts/retrofx --version
./scripts/retrofx status
./scripts/retrofx list
./scripts/retrofx search <keyword>
./scripts/retrofx info <profile>
./scripts/retrofx apply <profile>
./scripts/retrofx off [--tty|--all]
./scripts/retrofx doctor [--json]
./scripts/retrofx self-check
./scripts/retrofx repair
./scripts/retrofx perf [profile]
./scripts/retrofx preview [profile]
./scripts/retrofx new

# profile packs / interop
./scripts/retrofx gallery
./scripts/retrofx install-pack <packname>
./scripts/retrofx import base16 <scheme.json> --name <profile-name>
./scripts/retrofx export <alacritty|xresources|base16> <profile> <output_path>

# install mode
./scripts/retrofx install [--yes] [--path <dir>]
./scripts/retrofx uninstall [--yes] [--keep-profiles]
```

## Backend Capability Summary

- X11 + picom + GLX: full shader pipeline.
- Wayland: degraded outputs only, no global post-process compositor shader path.
- TTY: optional palette/font backend with safe/mock behavior.
- Tuigreet: generated config snippet in `active/tuigreet.conf`.

Use `./scripts/retrofx doctor` for exact host/session capability checks.

## Performance & Power Notes

- Apply path skips work when input signature is unchanged.
- Picom reload/restart path is minimized and gated by compositor-relevant config changes.
- Passthrough / blur-free profiles avoid compositor backend apply path (`Compositor not required.`).
- Run `./scripts/retrofx perf` for stage timing breakdown in milliseconds.

## Install Mode (User-Local)

RetroFX supports a user-local install mode under `~/.config/retrofx` with launcher at `~/.local/bin/retrofx`.

```bash
./scripts/retrofx install --yes
retrofx status
retrofx list
```

No root required. No `/etc` modifications.

## Documentation Index

- [Quickstart](docs/QUICKSTART.md)
- [Install](docs/INSTALL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Profile Spec](docs/PROFILE_SPEC.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Integration](docs/INTEGRATION.md)
- [Fonts](docs/FONTS.md)
- [Palettes](docs/PALETTES.md)
- [Interop](docs/INTEROP.md)
- [Testing](docs/TESTING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Releasing](docs/RELEASING.md)
- [Roadmap](docs/ROADMAP.md)

## Development

```bash
./scripts/test.sh
./scripts/ci.sh
```

If `shellcheck` is not installed, checks still run with a warning.

## License

See profile metadata for per-profile authorship/license notes where provided.
