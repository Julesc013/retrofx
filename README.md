# retrofx

RetroFX is a profile-driven rendering system for retro visual effects.

## Commands

```bash
./scripts/retrofx list
./scripts/retrofx --version
./scripts/retrofx search <keyword>
./scripts/retrofx gallery
./scripts/retrofx install-pack <packname>
./scripts/retrofx info <profile>
./scripts/retrofx apply <profile>
./scripts/retrofx import base16 <path-to-json> --name <profile-name>
./scripts/retrofx export <alacritty|xresources|base16> <profile> <output_path>
./scripts/retrofx self-check
./scripts/retrofx repair
./scripts/retrofx status
./scripts/retrofx off
./scripts/retrofx doctor [--json]
./scripts/retrofx preview
./scripts/retrofx new
./scripts/ci.sh
```

## Phase 1

- Full support: X11 + picom
- Scaffolds: tty, tuigreet, wayland degraded mode (docs/roadmap)

Start here: `docs/QUICKSTART.md`

Additional docs:
- `docs/INSTALL.md`
- `docs/INTEROP.md`
- `docs/TROUBLESHOOTING.md`
- `docs/RELEASING.md`
- `docs/ARCHITECTURE.md`
- `docs/PROFILE_SPEC.md`
- `docs/PALETTES.md`
- `docs/FONTS.md`
- `docs/CAPABILITIES.md`
- `docs/INTEGRATION.md`
- `docs/TESTING.md`
