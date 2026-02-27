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

- `kind` = `vga16` | `cube256` | `custom`
- `size` = integer `2..256`
- `custom_file` = optional path (required for `kind = "custom"`)

### `[effects]` (required)

- `blur_strength` = integer `0..6`
- `scanlines` = `true` | `false`
- `flicker` = `true` | `false`
- `dither` = `none` | `ordered`
- `vignette` = `true` | `false`

### `[scope]` (required)

- `x11` = `true` | `false`
- `tty` = `true` | `false`
- `tuigreet` = `true` | `false`

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
