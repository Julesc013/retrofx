# RetroFX 2.x Theme Tokens

This document defines the logical theme token taxonomy for RetroFX 2.x.

Some of these tokens already map directly to the current authored schema.
Others are theme-layer concepts that may be derived, pack-provided, or become explicit authored fields in later schema-expansion prompts.

The important rule is semantic consistency:

- theme tokens describe non-render appearance policy
- target adapters consume resolved theme tokens, not raw authored shortcuts

## A. Core Semantic Colors

These are the primary appearance anchors.

| Token | Meaning | Typical Fallback |
| --- | --- | --- |
| `bg0` | primary background | required |
| `bg1` | secondary surface | derive from `bg0` |
| `bg2` | tertiary or inactive surface | derive from `bg1` or `bg0` |
| `fg0` | primary foreground | required |
| `fg1` | secondary foreground | derive from `fg0` and `bg0` |
| `fg2` | muted foreground | derive from `fg1` |
| `accent_primary` | primary accent | family default, then `fg0` |
| `accent_info` | informational accent | `accent_primary` |
| `accent_success` | success accent | family default, then `accent_primary` |
| `accent_warn` | warning accent | family default, then `accent_primary` |
| `accent_error` | error accent | family default, then `accent_primary` |
| `accent_muted` | subtle accent | derive from `accent_primary` and `bg1` |

### Relationship To Terminal And TTY Palettes

- terminal and TTY palettes derive from these semantic anchors by default
- explicit terminal or TTY overrides may replace selected slots
- semantic tokens remain the real theme truth even when a target ultimately consumes ANSI slots

## B. Chrome / UI Tokens

These are theme and chrome hints, not render behavior.
Targets may consume only a subset.

| Token | Meaning | Typical Fallback |
| --- | --- | --- |
| `border_active` | active or focused border | `accent_muted`, then `bg2` |
| `border_inactive` | inactive border or divider | `bg2`, then `bg1` |
| `border_urgent` | urgent or alert border | `accent_error` |
| `selection_bg` | selection background | `accent_primary` |
| `selection_fg` | selection foreground | contrast-safe choice against `selection_bg` |
| `menu_bg` | menu or pop-up background | `bg1` |
| `menu_fg` | menu foreground | `fg0` |
| `status_bg` | status-line or bar background | `bg1` or `bg2` |
| `status_fg` | status-line or bar foreground | `fg0` or `fg1` |
| `glow_tint` | preferred highlight tint for glow-capable targets | `accent_primary`, or `fg0` in monochrome-like styles |
| `shadow_tint` | preferred shadow or low-emphasis tint | derive from `bg2` and `accent_muted` |
| `inactive_dim` | recommended dimming factor or dim color hint for inactive UI | derive from `fg2` or `bg2` |

### Important Boundary

- `glow_tint` is a theme token
- glow itself as an algorithm is render behavior

## C. Terminal / TUI Theme Tokens

These are logical target-facing theme tokens.
Current authored schema paths may still appear under `color.*`, but the theme layer treats them as a coherent token family.

| Token | Meaning | Default Source |
| --- | --- | --- |
| `terminal.ansi.0..15` | terminal ANSI palette | derived from semantic palette |
| `terminal.cursor` | terminal cursor color | `cursor` or `fg0` |
| `terminal.cursor_text` | cursor text color | contrast-safe against `terminal.cursor` |
| `terminal.selection_bg` | terminal selection background | `selection_bg` |
| `terminal.selection_fg` | terminal selection foreground | `selection_fg` |
| `tty.ansi.0..15` | TTY ANSI palette | inherit from terminal ANSI, then semantic palette |
| `tuigreet.background` | login presentation background | `bg0` or `bg1` |
| `tuigreet.foreground` | login presentation foreground | `fg0` |
| `tuigreet.accent` | login presentation accent | `accent_primary` |

### Default Mapping

- semantic mapping derives terminal ANSI by default
- TTY inherits terminal ANSI unless it needs target-specific differences
- explicit target overrides replace only the slots or fields they set

### Why Terminal And TTY May Differ

They may differ because:

- TTY has harder palette and font constraints
- terminal apps may support richer cursor and selection styling
- login presentation targets may want a simplified accent set

## D. Typography Tokens

Typography tokens are role-based appearance policy.

| Token | Meaning |
| --- | --- |
| `typography.console_font` | console font for TTY-capable contexts |
| `typography.terminal_primary` | primary terminal monospace family |
| `typography.terminal_fallbacks` | terminal fallback chain |
| `typography.ui_sans` | UI sans family |
| `typography.ui_mono` | UI monospace family |
| `typography.icon_font` | icon-capable symbol font hint |
| `typography.emoji_policy` | emoji handling policy |
| `typography.aa.antialias` | antialias policy |
| `typography.aa.subpixel` | subpixel policy |
| `typography.aa.hinting` | hinting policy |

### Hints Versus Directly Actionable Tokens

- `console_font` may be directly actionable for TTY-capable targets
- terminal font roles may be directly actionable in some terminal targets
- UI font roles are often hints or export values for WM and toolkit targets
- AA policy may become session-local fontconfig output, target-specific terminal config, or export-only hints depending on capability

## E. Icon / Cursor Tokens

These are style-policy tokens, not universal guarantees.

| Token | Meaning | Typical Behavior |
| --- | --- | --- |
| `icon_theme` | preferred icon theme family | export or install hint in many environments |
| `icon_variant` | preferred icon-theme variant or density | optional hint only |
| `cursor_theme` | preferred cursor theme family | export, install, or session-local hint |
| `cursor_size` | preferred cursor size | target-specific and environment-specific |
| `cursor_variant` | cursor style variant | optional hint only |

### Capability Reminder

- some targets can apply these
- some targets can only export or install them
- some targets must ignore them with warning

That is expected and should stay explicit.

## Logical Theme Tokens Versus Authored Paths

The theme subsystem reasons in logical token categories.
Exact authored TOML nesting may evolve.

Examples:

- `terminal.ansi.*` currently maps to the terminal palette fields in the profile schema
- `icon_theme` and `cursor_theme` may be authored under chrome-style sections today, but they conceptually belong to icon and cursor policy

The theme compiler should preserve the logical categories even if authored-path details change later.

## Current v2alpha1 Alignment

The current `v2alpha1` authored schema already exposes some logical theme tokens directly and carries others through adjacent authored sections.

| Logical Theme Token Family | Current Authored Path | Notes |
| --- | --- | --- |
| `bg*`, `fg*`, `accent_*`, `border_*`, `selection_*`, `glow_tint`, `cursor*` | `color.semantic.*` | Primary authored theme color surface today. |
| `terminal.*` | `color.terminal.*` | Terminal-facing palette and cursor-related values. |
| `tty.*` | `color.tty.*` | TTY-specific palette values. |
| `typography.*` | `typography.*` | Role-based authored typography surface. |
| `icon_theme` | `chrome.icon_theme` | Authored under chrome today, but conceptually part of icon policy. |
| `cursor_theme` | `chrome.cursor_theme` | Authored under chrome today, but conceptually part of cursor policy. |
| bar, launcher, notification style hints | `chrome.*` | Chrome-style authored hints. |

Some logical theme tokens in this document are not yet first-class authored keys in `v2alpha1`.
Examples include `border_urgent`, `menu_bg`, `menu_fg`, `status_bg`, `status_fg`, `shadow_tint`, `inactive_dim`, `icon_variant`, and `cursor_variant`.

For the first implementation phases, those should be treated as:

- family- or pack-derived defaults
- target-family-specific derived theme helpers
- future schema-expansion candidates

They must not be faked as universally authored fields before the schema docs are deliberately updated.
