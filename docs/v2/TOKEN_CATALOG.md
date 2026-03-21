# RetroFX 2.x Token Catalog

This catalog is the canonical reference for 2.x profile keys and token families.
Token paths are written as logical dotted names even when TOML examples use quoted keys for numeric slots.

## Identity And Metadata

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `schema` | schema | yes | none | all | Current value: `retrofx.profile/v2alpha1`. |
| `identity.id` | metadata | yes | none | all | Stable slug for profile identity, migration, and pack references. |
| `identity.name` | metadata | yes | none | all | Human-readable display name. |
| `identity.description` | metadata | no | empty | all | Descriptive only. |
| `identity.tags[]` | metadata | no | empty | all | Descriptive and indexable. |
| `identity.author` | metadata | no | empty | all | Descriptive only. |
| `identity.license` | metadata | no | empty | all | Descriptive only. |
| `identity.family` | metadata | no | `custom` | all | May influence defaults and pack lookup, but not capability claims. |
| `identity.strictness` | policy | no | `modernized-retro` | all | Affects default derivation, not backend syntax. |

## Semantic Color Tokens

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `color.semantic.bg0` | color | yes | none | all theme-capable targets | Primary background anchor. |
| `color.semantic.bg1` | color | no | derive from `bg0` | terminal, tui, x11, wayland, wm, gtk, qt | Secondary surface. |
| `color.semantic.bg2` | color | no | derive from `bg1` or `bg0` | terminal, tui, x11, wayland, wm, gtk, qt | Tertiary surface or inactive chrome. |
| `color.semantic.fg0` | color | yes | none | all theme-capable targets | Primary foreground anchor. |
| `color.semantic.fg1` | color | no | derive from `fg0` and `bg0` | all theme-capable targets | Secondary foreground. |
| `color.semantic.fg2` | color | no | derive from `fg1` | all theme-capable targets | Muted or comment foreground. |
| `color.semantic.accent_primary` | color | no | family default, then `fg0` | terminal, tui, x11, wayland, wm, gtk, qt, notifications, launcher | Main accent. |
| `color.semantic.accent_info` | color | no | `accent_primary` | terminal, tui, x11, wayland, wm, gtk, qt, notifications | Informational accent. |
| `color.semantic.accent_success` | color | no | family default, then `accent_primary` | terminal, tui, x11, wayland, wm, gtk, qt, notifications | Success accent. |
| `color.semantic.accent_warn` | color | no | family default, then `accent_primary` | terminal, tui, x11, wayland, wm, gtk, qt, notifications | Warning accent. |
| `color.semantic.accent_error` | color | no | family default, then `accent_primary` | terminal, tui, x11, wayland, wm, gtk, qt, notifications | Error accent. |
| `color.semantic.accent_muted` | color | no | derive from `accent_primary` and `bg1` | terminal, tui, x11, wayland, wm, gtk, qt | Subtle accent. |
| `color.semantic.border_active` | color | no | `accent_muted`, then `bg2` | wm, x11, wayland, gtk, qt, notifications, launcher | Focus border or divider. |
| `color.semantic.border_inactive` | color | no | `bg2`, then `bg1` | wm, x11, wayland, gtk, qt | Inactive border or divider. |
| `color.semantic.selection_bg` | color | no | `accent_primary` | terminal, tui, gtk, qt, launcher | Selection background. |
| `color.semantic.selection_fg` | color | no | contrast-safe `bg0` or `fg0` | terminal, tui, gtk, qt, launcher | Selection foreground. |
| `color.semantic.glow_tint` | color | no | `accent_primary` or `fg0` in monochrome mode | render-capable x11 or wayland adapters | Render tint hint. |
| `color.semantic.cursor` | color | no | `fg0` | terminal, tui, gtk, qt, x11, wayland | Cursor color. |
| `color.semantic.cursor_text` | color | no | contrast-safe against `cursor` | terminal, tui, gtk, qt | Cursor text color. |

## Terminal And TTY ANSI Token Families

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `color.terminal.ansi.0..15` | color override family | no | derive from semantic ANSI mapping | terminal, tui, tuigreet | Logical ANSI16 terminal override slots. Partial overrides allowed. |
| `color.tty.ansi.0..15` | color override family | no | inherit from terminal ANSI, then semantic ANSI mapping | tty, tuigreet | TTY-specific override slots. Partial overrides allowed. |

## Typography Tokens

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `typography.console_font` | typography | no | family default or empty | tty, tuigreet | Best-effort host-facing console font. |
| `typography.terminal_primary` | typography | no | family default or empty | terminal, tui, x11, wayland | Main terminal mono family. |
| `typography.terminal_fallbacks[]` | typography | no | empty | terminal, tui, x11, wayland | Ordered fallback families. |
| `typography.ui_sans` | typography | no | family default or empty | wm, gtk, qt, notifications, launcher | UI sans role. |
| `typography.ui_mono` | typography | no | `terminal_primary`, then empty | tui, wm, gtk, qt | UI mono role. |
| `typography.icon_font` | typography | no | empty | wm, notifications, launcher | Optional icon or symbol font hint. |
| `typography.emoji_policy` | typography policy | no | `inherit` | terminal, tui, gtk, qt, wm | Hint, not a universal guarantee. |
| `typography.aa.antialias` | typography policy | no | `default` | x11, wayland, wm, gtk, qt, terminal | Session-level AA policy where expressible. |
| `typography.aa.subpixel` | typography policy | no | `default` | x11, wayland, wm, gtk, qt, terminal | Session-level subpixel policy. |
| `typography.aa.hinting` | typography policy | no | `default` | x11, wayland, wm, gtk, qt, terminal | Session-level hinting policy. |

## Render Tokens

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `render.mode` | render policy | yes | `passthrough` if omitted during normalization | x11, wayland, terminal, export-only preview paths | One of `passthrough`, `monochrome`, `palette`. |
| `render.quantization.bands` | render policy | conditional | `8` in monochrome mode | render-capable targets, preview paths | Required semantically for `monochrome`; ignored or degraded elsewhere. |
| `render.palette.kind` | render policy | conditional | none | palette-capable targets, preview paths | Required in `palette` mode. |
| `render.palette.size` | render policy | conditional | derived from kind | palette-capable targets, preview paths | Must match structured palette kinds. |
| `render.palette.source` | render policy | conditional | none | palette-capable targets, preview paths | Required for `custom` palette. |
| `render.effects.blur` | render effect | no | family and strictness default | render-capable x11 or wayland adapters | Intent scale, not backend implementation detail. |
| `render.effects.dither` | render effect | no | `none` | render-capable adapters, preview paths | Ordered dither only in baseline schema. |
| `render.effects.scanlines` | render effect | no | `false` | render-capable adapters | Boolean request. |
| `render.effects.flicker` | render effect | no | `false` | render-capable adapters | Boolean request. |
| `render.effects.vignette` | render effect | no | `false` | render-capable adapters | Boolean request. |
| `render.effects.hotcore` | render effect | no | `false` | render-capable adapters | Useful for phosphor-like or VFD-like highlights. |
| `render.display.gamma` | display policy | no | `1.0` | render-capable adapters, some export paths | Global display intent. |
| `render.display.contrast` | display policy | no | `1.0` | render-capable adapters, some export paths | Global display intent. |
| `render.display.temperature` | display policy | no | `6500` | render-capable adapters, some export paths | Color temperature request in Kelvin-like units. |
| `render.display.black_lift` | display policy | no | `0.0` | render-capable adapters | Raise or lower black floor. |
| `render.display.blue_light_reduction` | display policy | no | `0.0` | render-capable adapters, some toolkit exports | Readability or comfort hint. |
| `render.display.tint_bias` | display policy | no | empty | render-capable adapters | Optional tint color request. |

## Chrome Tokens

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `chrome.gaps` | chrome policy | no | `0` | wm, wayland, x11 | Logical gap request. |
| `chrome.bar_style` | chrome policy | no | `minimal` | wm, waybar-like, bars, tuigreet | Adapter hint. |
| `chrome.launcher_style` | chrome policy | no | `minimal` | launcher, rofi, wofi | Adapter hint. |
| `chrome.notification_style` | chrome policy | no | `minimal` | notifications | Adapter hint. |
| `chrome.icon_theme` | chrome policy | no | family default or empty | gtk, qt, wm, icons | Theme id or style hint. |
| `chrome.cursor_theme` | chrome policy | no | family default or empty | x11, wayland, gtk, qt, cursors | Theme id or style hint. |

## Session Tokens

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `session.targets[]` | session policy | yes, except explicit export-only profiles | none | all | Authored target classes, not concrete adapters. |
| `session.apply_mode` | session policy | yes | `current-session` if omitted during normalization | all | One of `current-session`, `export-only`, `installed-default`, `explicit-only`. |
| `session.persistence` | session policy | yes | derived from `apply_mode` | all | One of `ephemeral`, `installed`, `export-only`. |

## Reserved Future Composition Hooks

| Token Name | Category | Required | Default Source | Used By Target Classes | Notes |
| --- | --- | --- | --- | --- | --- |
| `compose.base` | composition | no | none | all | Reserved for future base-profile inheritance. |
| `compose.mixins[]` | composition | no | empty | all | Reserved for future mixin support. |
| `compose.family_defaults` | composition | no | none | all | Reserved for future family default references. |
| `compose.assets[]` | composition | no | empty | all | Reserved for future pack-local asset references. |

