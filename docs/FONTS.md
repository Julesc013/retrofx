# RetroFX Fonts and Antialiasing

RetroFX font controls are profile-driven and session-local.
They do not edit `/etc`, global fontconfig, or desktop settings by default.

## What RetroFX Generates

When a profile sets `[fonts]` and/or `[font_aa]`, RetroFX generates:

- `active/fontconfig.conf` (session-local fontconfig file)
- `active/alacritty.toml` (terminal colors + preferred font family)
- `active/Xresources` and `active/xresources` (terminal palette export)

## Session-Local Use

Use the helper to export `FONTCONFIG_FILE` for the current shell/session:

```bash
eval "$(./scripts/integrate/retrofx-env.sh)"
```

This only affects apps launched from that environment.
It does not persist globally.

## Recommended Retro Fonts

- Bitmap-ish terminal fonts:
  - Terminus
  - Tamzen
  - Fixed
- Nerd/retro-ish options:
  - BigBlueTerm Nerd Font
  - Terminus Nerd Font
- Emoji fallback:
  - Noto Color Emoji

## AA and Subpixel Guidance

- `antialias = off` + mild blur can look sharper/more phosphor-like.
- `antialias = on` + `subpixel = rgb|bgr` can improve readability on LCD panels.
- `subpixel = none` is safer across mixed panel/rotation setups.
- With strong blur, heavy AA can look soft; prefer subtle blur (`<= 3`).

## TTY Font Behavior

- `fonts.tty` is optional and best-effort.
- RetroFX attempts tty font apply only when safe and backup is possible.
- If backup/apply is not possible (permissions/tools/console context), RetroFX warns and continues.

## Keeping Other DEs Untouched

- Use session wrappers (`scripts/integrate/i3-retro-session.sh`) for opt-in sessions.
- Avoid globally exporting `FONTCONFIG_FILE` in shell/profile files.
- Run `./scripts/retrofx off` to return to passthrough-generated artifacts.
