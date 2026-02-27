# RetroFX Quickstart

## Repo-Local Usage

No system install is required. Run all commands from the repository root.

```bash
cd /path/to/retrofx
./scripts/retrofx list
```

## Pick A Profile

Discover built-in pack profiles:

```bash
./scripts/retrofx list
./scripts/retrofx search crt
./scripts/retrofx info crt-green-p1-4band
./scripts/retrofx info c64
```

## Apply / Off

Apply a profile:

```bash
./scripts/retrofx apply crt-green-p1-4band
```

Disable effects (passthrough):

```bash
./scripts/retrofx off
```

TTY rollback only:

```bash
./scripts/retrofx off --tty
```

## Preview

Preview color and quantization output:

```bash
./scripts/retrofx preview
./scripts/retrofx preview crt-amber-p3-6band
```

## Create Your Own Profile

Run the wizard:

```bash
./scripts/retrofx new
```

Profiles created by the wizard are saved under `profiles/user/`.

## Palette Notes

- Structured palette profiles (`palette-2` .. `palette-256`) are optimized and fast.
- Custom palettes are supported up to 32 colors (see `palettes/c64.txt` and `docs/PALETTES.md`).

## Wayland Note (Degraded Mode)

On Wayland sessions, RetroFX does not provide global post-process compositor shaders. In this mode, `apply` generates degraded outputs only (terminal palette artifacts, optional TTY palette backend, optional tuigreet snippet) and reports this explicitly in command output and `doctor`.
