# RetroFX Profile Spec v1

Profiles are TOML files under:

- `profiles/*.toml` (base)
- `profiles/packs/*/*.toml` (pack profiles)
- `profiles/user/*.toml` (user-created profiles)

## Required Top-Level Keys

- `name` (string)
- `version` (`1`)

## Optional Top-Level Keys

- `description` (string)
- `tags` (array of strings)
- `author` (string)
- `license` (string)

## Sections

### `[mode]`

- `type` = `passthrough` | `monochrome` | `palette`

### `[monochrome]` (required when `mode.type = "monochrome"`)

- `bands` = integer `2..256`
- `phosphor` = `green` | `amber` | `blue` | `white` | `custom`
- `custom_rgb` = optional `r,g,b` (required for `phosphor = "custom"`)
  - each component accepts `0..1` float or `0..255` integer
- `hotcore` = `true` | `false`

### `[palette]` (required when `mode.type = "palette"`)

- `kind` = `vga16` | `mono2` | `mono4` | `mono8` | `mono16` | `cube32` | `cube64` | `cube128` | `cube256` | `custom`
- `size` = integer `2..256`
- `custom_file` = optional path (required for `kind = "custom"`)
  - custom palettes are limited to `2..32` colors
  - for structured kinds, size must match kind (`mono2=2`, `cube64=64`, etc.)

### `[effects]` (required)

- `blur_strength` = integer `0..6`
- `scanlines` = `true` | `false`
- `flicker` = `true` | `false`
- `dither` = `none` | `ordered`
- `vignette` = `true` | `false`
- `scanline_preset` = optional `blur_on` | `blur_off`
- `transparency` = optional `off` | `on` | `rules` (default `off`)

### `[scope]` (required)

- `x11` = `true` | `false`
- `tty` = `true` | `false`
- `tuigreet` = `true` | `false`

### `[colors]` (optional)

- `background` = `#RRGGBB`
- `foreground` = `#RRGGBB`

### `[rules]` (optional, X11/picom hints)

- `exclude_wm_class` = array of strings
- `exclude_wm_name` = array of strings
- `exclude_opacity_below` = float `0..1`

### `[fonts]` (optional)

- `tty` = console font name (example: `ter-v16n`)
- `terminal` = preferred terminal font family (example: `Terminus Nerd Font`)
- `terminal_fallback` = array of fallback families
- `ui` = preferred UI sans font family for session-local fontconfig

Behavior:

- All keys are optional.
- If `[fonts]` is absent, no font family overrides are generated.
- `tty` is best-effort and only attempted by the TTY backend when safe.

### `[font_aa]` (optional)

- `antialias` = `default` | `on` | `off`
- `subpixel` = `default` | `rgb` | `bgr` | `none`

Behavior:

- `default` leaves fontconfig/system behavior unchanged.
- Non-default values generate a session-local `active/fontconfig.conf`.
- No global fontconfig files are modified by RetroFX.

Scope behavior:

- `x11=true` applies picom/X11 backend helpers.
- `tty=true` applies TTY ANSI16 palette backend (or mock mode when console write is unavailable).
- `tuigreet=true` generates `active/tuigreet.conf` snippet.

## Strict Parsing Rules

- Unknown sections are rejected.
- Unknown keys are rejected.
- Duplicate keys are rejected.
- Mode-specific constraints are enforced.
- Version must be `1`.
