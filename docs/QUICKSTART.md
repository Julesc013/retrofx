# RetroFX Quickstart

RetroFX 1.0 is best on X11 + picom + GLX. On Wayland, expect degraded outputs only. Run commands from the repository root unless you have installed RetroFX user-local.

## 1. Check Your Environment

```bash
./scripts/retrofx doctor
./scripts/retrofx compatibility-check
```

If you are on Wayland, RetroFX can still generate palette/session-local outputs, but it will not provide a global compositor shader path.

## 2. Browse Profiles

```bash
./scripts/retrofx list
./scripts/retrofx search crt
./scripts/retrofx info crt-green-p1-4band
./scripts/retrofx info c64
```

## 3. Apply, Inspect, Revert

```bash
./scripts/retrofx explain crt-green-p1-4band
./scripts/retrofx apply crt-green-p1-4band --dry-run
./scripts/retrofx apply crt-green-p1-4band
./scripts/retrofx status
./scripts/retrofx preview crt-green-p1-4band
./scripts/retrofx off
```

`explain` is read-only and reports the resolved runtime intent for the current environment. `apply --dry-run` renders and validates a temporary stage without changing `active/`, manifests, or backups.

TTY rollback only:

```bash
./scripts/retrofx off --tty
```

## 4. Recover Safely

```bash
./scripts/retrofx self-check
./scripts/retrofx repair
./scripts/retrofx apply crt-green-p1-4band --safe
```

## 5. Create, Import, Or Install Profiles

```bash
./scripts/retrofx new
./scripts/retrofx import base16 tests/fixtures/base16.json --name base16-demo
./scripts/retrofx install-pack core
```

- Wizard-created profiles are written to `profiles/user/`.
- `install-pack core` copies profiles into `profiles/user/` and relocates pack-local assets into `profiles/user_assets/`.
- Base16 import/export is a deterministic, lossy ANSI16 bridge, not a lossless round-trip format.

## 6. Optional Session-Local Font Overrides

```bash
./scripts/retrofx apply crt-green-fonts-aa
eval "$(./scripts/integrate/retrofx-env.sh)"
```

This affects apps launched from that shell/session only. RetroFX does not modify global fontconfig by default.

## 7. Optional User-Local Install

```bash
./scripts/retrofx install --yes
retrofx status
retrofx list
```

## Need Help?

- Support boundaries:
  - `docs/1x_PRODUCT.md`
  - `docs/CAPABILITIES.md`
- Recovery and diagnostics:
  - `docs/TROUBLESHOOTING.md`
  - `docs/TESTING.md`
