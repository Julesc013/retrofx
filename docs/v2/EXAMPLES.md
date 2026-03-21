# RetroFX 2.x Profile Examples

These examples are documentation-first schema examples.
As of TWO-14, several of the same ideas now also exist as real local curated pack profiles under `v2/packs/`, but this document still describes the semantic examples rather than the pack manifest format.

## 1. Strict Green CRT

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "strict-green-crt"
name = "Strict Green CRT"
family = "crt"
strictness = "strict-authentic"
tags = ["crt", "green", "x11", "retro"]

[color.semantic]
bg0 = "#061008"
fg0 = "#92ff84"
accent_primary = "#7dff70"
glow_tint = "#7dff70"
cursor = "#b7ffac"

[typography]
terminal_primary = "Terminus Nerd Font"
terminal_fallbacks = ["DejaVu Sans Mono", "Noto Color Emoji"]
ui_sans = "IBM Plex Sans"

[render]
mode = "monochrome"

[render.quantization]
bands = 4

[render.effects]
blur = 3
dither = "ordered"
scanlines = true
flicker = false
vignette = true
hotcore = false

[session]
targets = ["x11", "terminal", "wm"]
apply_mode = "current-session"
persistence = "ephemeral"
```

Important semantic intent:

- authenticity-first CRT family
- monochrome green semantics instead of generic grayscale
- render effects requested for render-capable targets

Conceptual compile result:

- X11 render-capable path would request scanlines, blur, and vignette.
- Terminal and WM targets would still compile coherent green semantic colors and typography even without runtime effects.

## 2. Amber VFD With Hotcore

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "amber-vfd-hotcore"
name = "Amber VFD Hotcore"
family = "vfd"
strictness = "modernized-retro"

[color.semantic]
bg0 = "#140d05"
fg0 = "#ffcb72"
accent_primary = "#ffb347"
accent_warn = "#ffc56b"
glow_tint = "#ffb347"

[render]
mode = "monochrome"

[render.quantization]
bands = 6

[render.effects]
blur = 2
dither = "ordered"
scanlines = false
flicker = false
vignette = true
hotcore = true

[render.display]
temperature = 4200
contrast = 1.05

[session]
targets = ["x11", "terminal", "tui"]
apply_mode = "current-session"
persistence = "ephemeral"
```

Important semantic intent:

- warm amber single-hue family
- hotcore highlight request
- mild warmth bias for display policy

Conceptual compile result:

- Render-capable targets would request hotcore and warm glow behavior.
- Terminal and TUI outputs would preserve amber semantics through ANSI mapping and typography defaults.

## 3. VGA16 DOS-Like Palette

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "vga16-dos-like"
name = "VGA16 DOS-Like"
family = "dos"
strictness = "strict-authentic"

[color.semantic]
bg0 = "#000000"
fg0 = "#c0c0c0"
accent_primary = "#55ffff"
accent_error = "#aa0000"
accent_success = "#00aa00"
accent_warn = "#aa5500"
accent_info = "#0000aa"

[render]
mode = "palette"

[render.palette]
kind = "vga16"
size = 16

[render.effects]
blur = 1
dither = "none"
scanlines = false
flicker = false
vignette = false
hotcore = false

[session]
targets = ["terminal", "tty", "tui", "x11"]
apply_mode = "current-session"
persistence = "ephemeral"
```

Important semantic intent:

- authentic VGA16 palette family
- palette mode is the primary look, not monochrome phosphor
- useful across TTY, terminal, and X11

Conceptual compile result:

- Terminal and TTY outputs would largely preserve VGA slot semantics directly.
- X11 render-capable targets would request palette quantization but no strong CRT-specific effects.

## 4. Modern Minimal Grayscale

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "modern-minimal-gray"
name = "Modern Minimal Gray"
family = "modern-minimal"
strictness = "practical-daily-driver"

[color.semantic]
bg0 = "#121212"
bg1 = "#1c1c1c"
bg2 = "#2a2a2a"
fg0 = "#efefef"
fg1 = "#c7c7c7"
fg2 = "#8f8f8f"
accent_primary = "#d0d0d0"
accent_muted = "#6d6d6d"

[typography]
terminal_primary = "Iosevka"
ui_sans = "IBM Plex Sans"
ui_mono = "Iosevka"
emoji_policy = "color"

[render]
mode = "passthrough"

[chrome]
gaps = 10
bar_style = "minimal"
launcher_style = "minimal"
notification_style = "minimal"

[session]
targets = ["terminal", "gtk", "qt", "wm", "launcher", "notifications"]
apply_mode = "installed-default"
persistence = "installed"
```

Important semantic intent:

- no render-heavy authenticity request
- strong theme-side semantics for daily-driver use
- chrome hints matter more than scanlines or quantization

Conceptual compile result:

- Terminal, toolkit, WM, launcher, and notification outputs would be primary.
- Render-capable targets would likely degrade to theme-only behavior because the profile does not ask for transform-heavy effects.

## 5. Warm-Night Readable Profile

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "warm-night-readable"
name = "Warm Night Readable"
family = "warm-night"
strictness = "practical-daily-driver"

[color.semantic]
bg0 = "#16120f"
bg1 = "#221b17"
fg0 = "#f0e3cf"
fg1 = "#d7c6af"
accent_primary = "#d9a066"
accent_info = "#8ab4c7"
accent_success = "#9ec48d"
accent_warn = "#d8b16a"
accent_error = "#c97b6b"
selection_bg = "#6a4b2e"

[typography]
terminal_primary = "Berkeley Mono"
terminal_fallbacks = ["DejaVu Sans Mono", "Noto Color Emoji"]
ui_sans = "Source Sans 3"

[typography.aa]
antialias = "on"
subpixel = "none"
hinting = "slight"

[render]
mode = "passthrough"

[render.display]
temperature = 4300
contrast = 1.03
blue_light_reduction = 0.35

[session]
targets = ["terminal", "tui", "gtk", "qt", "wm"]
apply_mode = "current-session"
persistence = "ephemeral"
```

Important semantic intent:

- comfortable nighttime readability over strict authenticity
- typography and display policy matter more than render effects
- broad theme-side portability

Conceptual compile result:

- Terminal, TUI, toolkit, and WM targets would receive warm semantic colors and AA policy.
- Render-capable targets could optionally apply warmth or contrast transforms, but the profile stays useful without them.

## 6. Theme-Only Export-Only Profile

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "theme-only-export-pack"
name = "Theme-Only Export Pack"
family = "terminal"
strictness = "modernized-retro"

[color.semantic]
bg0 = "#10131a"
bg1 = "#171d28"
fg0 = "#d9e2f2"
accent_primary = "#79a6ff"
accent_info = "#6ac1e8"
accent_success = "#8dc891"
accent_warn = "#d7b16b"
accent_error = "#d17b7b"

[typography]
terminal_primary = "JetBrains Mono"
ui_sans = "IBM Plex Sans"

[render]
mode = "passthrough"

[chrome]
icon_theme = "Papirus"
cursor_theme = "Bibata-Modern-Ice"

[session]
targets = ["terminal", "gtk", "qt", "icons", "cursors"]
apply_mode = "export-only"
persistence = "export-only"
```

Important semantic intent:

- compile themes without taking runtime session ownership
- useful for CI, pack generation, or dotfile export workflows
- render requests intentionally absent

Conceptual compile result:

- RetroFX would emit terminal, toolkit, icon, and cursor-related exports.
- No live apply plan would be claimed unless a later explicit workflow selects one.
