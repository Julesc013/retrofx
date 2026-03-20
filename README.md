# RetroFX

RetroFX is a profile-driven retro rendering and theming tool for Linux sessions. RetroFX 1.x is centered on a supported X11 + picom + GLX path, plus deterministic terminal/theme exports, scoped TTY and tuigreet outputs, user-local install mode, and explicit recovery tooling. Current repository version: `1.0.0-beta.1`.

## Current Support

| Target / Environment | Status | Notes |
| --- | --- | --- |
| X11 + picom + GLX | Supported | Full shader/runtime path. Best-supported session flow is i3 + the RetroFX wrapper. |
| Other X11 sessions | Degraded | Core apply/export logic works, but session integration is more manual and less documented. |
| Wayland sessions | Degraded | No global shader/compositor path. Palette and session-local outputs only. |
| TTY palette backend | Supported | Optional 16-color backend. Real apply requires a compatible console. |
| tuigreet snippet generation | Supported | Generates `active/tuigreet.conf`; global greetd edits stay manual. |
| Base16 import/export | Supported | Deterministic, lossy ANSI16 bridge. |
| Broad DE orchestration / global Wayland shaders | Unsupported | Out of scope for 1.x. |

## Quick Start

```bash
./scripts/retrofx doctor
./scripts/retrofx list
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx status
./scripts/retrofx off
```

## Safety And Recovery

- `apply` is atomic and keeps `state/last_good/` as the rollback snapshot.
- `self-check` validates the active state against the artifact contract in `state/manifests/`.
- `repair` restores a manifest-valid `last_good` snapshot or falls back conservatively.
- User-local install mode lives under `~/.config/retrofx`; RetroFX does not edit `/etc` by default.

## Current Limits

- `1.0.0-beta.1` is a public beta candidate, not a stable release.
- Wayland support is degraded by design in 1.x.
- Wrapper/Xsession integration is explicit for i3; other WM/DE setups are more manual.
- Base16 import/export is intentionally lossy.
- Passing `./scripts/test.sh` is necessary but not sufficient for final release confidence.

## Documentation

- [1.x Product Truth](docs/1x_PRODUCT.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Quickstart](docs/QUICKSTART.md)
- [Install](docs/INSTALL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Profile Spec](docs/PROFILE_SPEC.md)
- [Integration](docs/INTEGRATION.md)
- [Interop](docs/INTEROP.md)
- [Testing](docs/TESTING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Beta Notes](docs/BETA_NOTES.md)
- [Release Notes (`1.0.0-beta.1`)](docs/RELEASE_NOTES_1.0.0-beta.1.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)
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
