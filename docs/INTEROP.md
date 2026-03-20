# RetroFX Interop

RetroFX interop is intentionally minimal and offline-first.

Status summary:

- Supported:
  - `xresources` export
  - `alacritty` export
  - Base16 JSON import/export as a deterministic lossy bridge
- Unsupported:
  - YAML Base16 import
  - networked gallery/pack behavior

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

RetroFX 1.x treats Base16 interop as a deterministic ANSI16 semantic bridge, not a lossless format conversion.

Import behavior:

- The imported palette file preserves all 16 source slots in order:
  - `base00` -> line 0 / ANSI slot 0
  - ...
  - `base0f` -> line 15 / ANSI slot 15
- The generated profile then anchors RetroFX semantic colors to:
  - `background = base00`
  - `foreground = base05`
- That keeps the imported profile usable in RetroFX's normal terminal/export pipeline, but it means later export is not a verbatim copy of the source scheme.

Export behavior:

- `retrofx export base16 ...` writes a Base16-shaped JSON approximation of the resolved RetroFX ANSI16 palette.
- Export metadata is explicit:
  - `"mapping": "resolved-retrofx-ansi16"`
  - `"round_trip": "lossy-best-effort"`
- Export is deterministic for the same profile/input.
- Round-trip fidelity is not guaranteed.
  - Example: importing the bundled fixture and exporting it again collapses `base07` to the resolved semantic foreground (`base05`) because RetroFX drives ANSI slot 7 from its foreground anchor.

Profile defaults for imported schemes are conservative:

- blur = 2
- scanlines = false
- flicker = false

Recommended use:

- Use Base16 import/export to bridge palettes between tools that already speak ANSI16/Base16-shaped JSON.
- Do not use it as a lossless archival round-trip format for RetroFX profiles.

## Sharing Profiles

To share a profile offline, copy:

1. the profile TOML file (`profiles/user/*.toml`)
2. optional palette file referenced by `palette.custom_file` (if used)

Receiver can place them in `profiles/user/` (and palette path accordingly).
