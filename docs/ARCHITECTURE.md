# RetroFX Architecture

RetroFX is a profile-driven renderer that generates deterministic session-local artifacts under this repository and never touches system-wide configuration by default.

## Design Principles

- Deterministic generation from `profiles/*.toml`.
- Atomic apply: generate to temp -> validate -> backup -> rename swap.
- Fail-safe behavior: rollback to `state/last_good/` on failed transactions.
- Scoped backends: X11, TTY, and tuigreet are applied only when enabled in profile scope.
- Performance discipline: single-pass shader pipeline with bounded operations.

## Repository Roles

- `scripts/retrofx`: CLI entrypoint, profile parser, renderer, and transaction orchestrator.
- `scripts/test.sh`: regression harness including static shader checks and backend mock checks.
- `templates/*`: static templates rendered into active artifacts.
- `active/`: currently active generated config set.
- `state/backups/`: timestamped active snapshots (pruned to last N, default 10).
- `state/last_good/`: canonical rollback snapshot for failed apply.
- `state/logs/retrofx.log`: append-only audit log.
- `state/tty-backups/`: tty palette rollback stack.
- `backends/*`: backend-specific apply/off logic.

## Apply Transaction

1. Parse and validate profile.
2. Detect session type (`x11`, `wayland`, `unknown`) and WM/DE (best-effort).
3. Render stage artifacts into `state/stage.*`:
   - X11/unknown: shader + picom + palette artifacts
   - Wayland: degraded palette artifacts only (no shader/picom targets)
4. Validate generated stage:
   - X11/unknown: shader static checks + artifact checks
   - Wayland: degraded artifact checks (and assert shader/picom absence)
5. Optionally runtime-validate with picom when environment allows.
6. Backup current `active/`.
7. Atomically swap stage into `active/`.
8. Apply scoped backends:
   - `x11-picom` only outside Wayland
   - `tty` and `tuigreet` by profile scope
9. Persist new `state/last_good/` snapshot.

## Failure Handling

- Parse/render/validation failure: abort and rollback to `state/last_good/` when available.
- Swap failure: restore previous `active/` snapshot immediately.
- TTY backend failure: treated as critical when scoped, triggers rollback.
- Tuigreet backend failure: non-critical, logged warning only.
- Logging failures are best-effort and never fail commands.

## Rendering Pipeline (Formal Order)

1. Linearize input color (`sRGB -> linear`)
2. Transform / tint preparation
3. Quantize (mode-specific)
4. Ordered dither (when enabled and quantization active)
5. Scanlines
6. Flicker
7. Vignette
8. Encode output (`linear -> sRGB`)

## Rendering Complexity Guarantees

- Monochrome quantization: `O(1)`
- VGA16 quantization: `O(16)` (bounded loop)
- cube256 quantization: `O(1)` (arithmetic mapping)
- Ordered dither: `O(1)`
- Scanlines: `O(1)`
- Flicker: `O(1)`
- Vignette: `O(1)`
- No multi-pass, no frame history, no extra texture lookups

## Semantic Color Preservation Strategy

- A shared ANSI16 semantic palette is generated once per profile and reused by X11 terminal resources, TTY backend, and tuigreet theme snippet.
- Semantic roles are fixed to stable ANSI slots:
  - `background -> color0`
  - `normal -> color7`
  - `dim -> color8`
  - `bright -> color15`
  - `info -> color4`
  - `success -> color2`
  - `warning -> color3`
  - `error -> color1`
- Monochrome mode preserves meaning by ordered intensity mapping:
  - error >= warning >= success >= info
- Palette modes preserve hue whenever possible (notably vga16 and cube256 summary palette).
- TTY is constrained to 16 colors, so semantic fidelity is preserved by slot strategy rather than full gamut matching.

## Backend Status

- `x11-picom`: functional profile-scoped backend.
- `tty`: functional profile-scoped backend with safe mock/apply/off behavior and rollback backups.
- `tuigreet`: functional profile-scoped snippet generation (`active/tuigreet.conf`).
- Wayland: degraded support implemented with honest capability reporting (no global post-process shader pipeline).
