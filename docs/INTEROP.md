# RetroFX Interop

RetroFX interop is intentionally minimal and offline-first.

## Supported

- Import Base16-style **JSON** schemes:
  - `retrofx import base16 <path-to-json> --name <profile-name>`
- Export Base16-style **JSON** from a profile:
  - `retrofx export base16 <profile> <output-path>`
- Existing exports remain supported:
  - `retrofx export alacritty <profile> <output-path>`
  - `retrofx export xresources <profile> <output-path>`
- Offline gallery browsing:
  - `retrofx gallery`
  - `retrofx install-pack <packname>`

## Not Supported

- Network pack fetching
- Automatic online gallery sync
- YAML Base16 import (JSON only in this build)

## Base16 Import Notes

- Required keys: `base00` .. `base0f`
- Accepted color format per key:
  - `#RRGGBB` (or `0xRRGGBB`)
- Imported profiles are written to:
  - `profiles/user/<name>.toml`
- Imported palette files are written to:
  - `palettes/imported/<name>.txt`

Import uses a direct 16-color mapping:

- `base00` -> ANSI 0
- `base01` -> ANSI 1
- ...
- `base0f` -> ANSI 15

Profile defaults for imported schemes are safe:

- blur = 2
- scanlines = false
- flicker = false

## Sharing Profiles

To share a profile offline, copy:

1. the profile TOML file (`profiles/user/*.toml`)
2. optional palette file referenced by `palette.custom_file` (if used)

Receiver can place them in `profiles/user/` (and palette path accordingly).
