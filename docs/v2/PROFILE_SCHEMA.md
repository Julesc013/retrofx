# RetroFX 2.x Profile Schema

This document defines the authored profile language for RetroFX 2.x.
It describes what users write, not what adapters emit.

RetroFX 2.x keeps TOML as the canonical authoring format for now because it is readable, familiar in the repository, and easy to validate deterministically.
The authoring format may evolve later, but the semantic schema described here is the product contract.

## Design Laws

- Users author semantic intent, not backend-specific implementation whenever possible.
- Backends compile from the resolved model, not directly from raw profile text.
- Capability filtering is explicit and logged.
- Unsupported tokens are ignored with warning, downgraded deterministically, or rejected when they are structurally invalid for the chosen mode.
- 2.x is designed for extensibility but not for universal promises.

## Layer Model

RetroFX 2.x distinguishes four layers:

### Layer A: Input Profile

The authored TOML file.
It may omit optional values, rely on defaults, and declare intent in target classes such as `terminal` or `wm` rather than concrete backend syntax.

### Layer B: Normalized Profile

The canonical internal schema object after:

- structural validation
- default application
- canonical key normalization
- deduplication and ordering cleanup
- deferred composition flattening when that feature exists

The normalized profile is still capability-agnostic.

### Layer C: Resolved Profile

Layer C has two closely related forms:

- the `resolved semantic model`, where semantic tokens and policy are fully concretized
- the final `resolved profile`, where capability filtering has attached the target plan needed for compilation

Adapters consume the final resolved profile, not the raw authored text.

### Layer D: Target Emission

Concrete files and runtime plans such as terminal configs, WM snippets, toolkit exports, fontconfig files, session fragments, or render-capable artifacts.
This layer is adapter-specific and is not authored directly in the profile.

## Canonical Authoring Skeleton

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "crt-green-strict"
name = "CRT Green Strict"
family = "crt"
strictness = "strict-authentic"

[color.semantic]
bg0 = "#071109"
fg0 = "#86ff7a"
accent_primary = "#74ff68"

[render]
mode = "monochrome"

[render.quantization]
bands = 4

[render.effects]
blur = 3
dither = "ordered"
scanlines = true
vignette = true

[session]
targets = ["x11", "terminal", "wm"]
apply_mode = "current-session"
persistence = "ephemeral"
```

## Top-Level Structure

| Key or Section | Role |
| --- | --- |
| `schema` | Required schema identifier, currently `retrofx.profile/v2alpha1`. |
| `[identity]` | Descriptive metadata and pack or family-facing defaults hints. |
| `[color.semantic]` | Semantic color foundation tokens. |
| `[color.terminal.ansi]` | Optional logical ANSI16 overrides for terminal targets. |
| `[color.tty.ansi]` | Optional logical ANSI16 overrides for TTY targets. |
| `[typography]` | Typography role tokens. |
| `[typography.aa]` | Session-level font antialiasing and hinting policy. |
| `[render]` | Render mode selection. |
| `[render.quantization]` | Quantization policy. |
| `[render.palette]` | Palette-mode policy. |
| `[render.effects]` | Effect requests. |
| `[render.display]` | Display transform requests. |
| `[chrome]` | UI and chrome-level theme hints. |
| `[session]` | Target classes and lifecycle policy. |
| `[compose]` | Reserved future composition hooks. Not baseline-authorable in the first implementation phase. |

## Identity And Metadata

`[identity]` separates descriptive metadata from metadata that may influence defaults.

### Purely Descriptive

- `id`
- `name`
- `description`
- `tags`
- `author`
- `license`

These describe the profile and survive into the resolved model, but they do not change target behavior directly.

### Metadata That May Influence Defaults

- `family`
- `strictness`

`family` identifies the style family or lineage such as `crt`, `vfd`, `terminal`, or `modern-minimal`.
It is a defaults hint, not a backend knob.

`strictness` identifies how aggressively the profile should preserve stylistic authenticity versus comfort and compatibility.
The initial vocabulary is:

- `strict-authentic`
- `modernized-retro`
- `practical-daily-driver`

`family` and `strictness` may affect default derivation for optional semantic tokens, typography recommendations, and effect baselines.
They do not bypass validation or capability filtering.

## Style Tokens: Color Foundation

The semantic palette is the real authored color truth for 2.x.
Terminal and TTY ANSI sets are derived outputs unless explicitly overridden.

### Semantic Color Tokens

| Token | Meaning | Required | Default If Omitted |
| --- | --- | --- | --- |
| `color.semantic.bg0` | Primary background. The darkest or base surface. | yes | none |
| `color.semantic.bg1` | Secondary surface or raised background. | no | derived from `bg0` by one tone step |
| `color.semantic.bg2` | Tertiary surface, panel, or inactive chrome surface. | no | derived from `bg1` or `bg0` by the next tone step |
| `color.semantic.fg0` | Primary foreground text. | yes | none |
| `color.semantic.fg1` | Secondary text or less emphasized foreground. | no | derived between `fg0` and `bg0` |
| `color.semantic.fg2` | Muted foreground, comments, or low-emphasis text. | no | derived from `fg1` with lower emphasis |
| `color.semantic.accent_primary` | Main highlight or brand accent. | no | family default, then `fg0` |
| `color.semantic.accent_info` | Informational semantic accent. | no | `accent_primary` |
| `color.semantic.accent_success` | Success semantic accent. | no | family default, then `accent_primary` |
| `color.semantic.accent_warn` | Warning semantic accent. | no | family default, then `accent_primary` |
| `color.semantic.accent_error` | Error semantic accent. | no | family default, then `accent_primary` |
| `color.semantic.accent_muted` | Subtle highlight for separators, inactive accents, or soft emphasis. | no | mix of `accent_primary` and `bg1` |
| `color.semantic.border_active` | Active border, rule, or focused frame. | no | `accent_muted`, then `bg2` |
| `color.semantic.border_inactive` | Inactive border or divider. | no | `bg2`, then `bg1` |
| `color.semantic.selection_bg` | Selection background. | no | `accent_primary` |
| `color.semantic.selection_fg` | Selection foreground text. | no | contrast-safe choice between `bg0` and `fg0` |
| `color.semantic.glow_tint` | Tint used by render-capable glow or bloom-like effects. | no | `accent_primary`; in monochrome profiles, usually `fg0` |
| `color.semantic.cursor` | Cursor block or insertion marker. | no | `fg0` |
| `color.semantic.cursor_text` | Text shown inside or against the cursor. | no | contrast-safe choice against `cursor` |

### Derivation Order

When an optional semantic token is omitted, RetroFX derives it in this order:

1. explicit authored value
2. pack or family default
3. strictness-influenced semantic derivation from required anchors
4. deterministic fallback from the nearest semantic role

If a required anchor such as `bg0` or `fg0` is missing, validation fails.

## Terminal And TTY Token Sets

RetroFX 2.x defines separate logical token groups for terminal and TTY ANSI output:

- `color.terminal.ansi.0..15`
- `color.tty.ansi.0..15`

In TOML examples, numeric ANSI slot keys should be quoted.

### Default Behavior

- Terminal ANSI slots inherit from the semantic palette by default.
- TTY ANSI slots inherit from terminal ANSI by default.
- TTY may also derive directly from the semantic palette when terminal output is not selected.
- Either set may be overridden explicitly per slot.

### Semantic-To-ANSI Mapping Strategy

The default logical mapping is:

| ANSI Slot | Default Semantic Source |
| --- | --- |
| `0` | `bg0` |
| `1` | `accent_error` |
| `2` | `accent_success` |
| `3` | `accent_warn` |
| `4` | `accent_info` |
| `5` | `accent_primary` |
| `6` | `accent_muted` |
| `7` | `fg1` |
| `8` | `bg2` |
| `9` | brightened `accent_error` |
| `10` | brightened `accent_success` |
| `11` | brightened `accent_warn` |
| `12` | brightened `accent_info` |
| `13` | brightened `accent_primary` |
| `14` | brightened `accent_muted` |
| `15` | `fg0` |

### Monochrome And Palette Behavior

- Monochrome themes preserve semantics by luminance band and contrast ordering, not by fake hue diversity.
- Palette themes preserve semantics by hue slot where possible and fall back to nearest contrast-safe entry when the palette is constrained.
- Explicit `color.terminal.ansi.*` or `color.tty.ansi.*` values override the mapping for those slots only.

## Typography Tokens

Typography is authored by role, not by backend file name.

| Token | Meaning |
| --- | --- |
| `typography.console_font` | Console or TTY-oriented font name where the host can apply one. |
| `typography.terminal_primary` | Preferred primary terminal monospace family. |
| `typography.terminal_fallbacks` | Ordered terminal fallback families. |
| `typography.ui_sans` | Preferred UI sans family. |
| `typography.ui_mono` | Preferred UI monospace family for editors, bars, and code-facing widgets. |
| `typography.icon_font` | Optional icon or symbol font hint. |
| `typography.emoji_policy` | Emoji rendering policy. |
| `typography.aa.antialias` | Session-level antialiasing policy. |
| `typography.aa.subpixel` | Session-level subpixel policy. |
| `typography.aa.hinting` | Session-level hinting policy. |

### Typography Scope

- `console_font` is mainly relevant to TTY and login-console targets.
- `terminal_primary` and `terminal_fallbacks` can affect terminal, TUI, and session-local fontconfig outputs.
- `ui_sans` and `ui_mono` are usually session-level or export-level hints for WM, toolkit, and DE-facing targets.
- `icon_font` and `emoji_policy` are target hints, not universal guarantees.
- `typography.aa.*` is session-level policy where a target can express it, usually through session-local fontconfig or toolkit exports.

## Render Policy Tokens

Render tokens express appearance intent, not a promise that every backend can execute the request.

### Core Render Mode

- `render.mode = "passthrough" | "monochrome" | "palette"`

### Quantization Policy

- `render.quantization.bands`

This is meaningful for `monochrome` mode and may be used by some palette-oriented adapters as a degradation hint.

### Palette Policy

- `render.palette.kind`
- `render.palette.size`
- `render.palette.source`

`render.palette.source` is a reference string for custom palette sources.
The initial reference namespaces are:

- `file:relative/or/absolute/path`
- `pack:pack-id/asset-id`
- `builtin:name`

### Effects

- `render.effects.blur`
- `render.effects.dither`
- `render.effects.scanlines`
- `render.effects.flicker`
- `render.effects.vignette`
- `render.effects.hotcore`

These values describe requested effect behavior.
Targets may honor them, downgrade them, or ignore them with explicit warnings depending on capability.

### Display Transform Requests

- `render.display.gamma`
- `render.display.contrast`
- `render.display.temperature`
- `render.display.black_lift`
- `render.display.blue_light_reduction`
- `render.display.tint_bias`

These are global appearance intents, not universal hardware or compositor promises.
They are especially likely to degrade outside render-capable targets.

## Chrome And UI Tokens

`[chrome]` defines theme-side hints for UI structure and integration-heavy targets.

| Token | Meaning |
| --- | --- |
| `chrome.gaps` | Requested window or panel gap size in logical pixels. |
| `chrome.bar_style` | Style hint for bars or status lines. |
| `chrome.launcher_style` | Style hint for launchers or application menus. |
| `chrome.notification_style` | Style hint for notifications or popups. |
| `chrome.icon_theme` | Preferred icon theme id or style hint. |
| `chrome.cursor_theme` | Preferred cursor theme id or style hint. |

These are intentionally optional.
Not all targets can use them, and many compile as hints for specific adapters rather than universal appearance controls.

## Session And Scope Policy

2.x replaces 1.x boolean scope flags with explicit session policy.

### Required Session Policy Fields

- `session.targets` for apply-oriented profiles, and strongly recommended even for export-only profiles
- `session.apply_mode`
- `session.persistence`

### Meaning

- `session.targets` is a list of target classes such as `tty`, `tuigreet`, `terminal`, `tui`, `x11`, `wayland`, `wm`, `gtk`, `qt`, `icons`, `cursors`, `notifications`, or `launcher`.
- `session.apply_mode` describes how the profile is intended to be used:
  - `current-session`
  - `export-only`
  - `installed-default`
  - `explicit-only`
- `session.persistence` describes lifecycle posture:
  - `ephemeral`
  - `installed`
  - `export-only`

### Why This Is Better Than 1.x Scope Booleans

- It separates target intent from lifecycle intent.
- It allows profiles that are valid for export without pretending they are meant for live apply.
- It gives the compiler clearer information for capability filtering and artifact planning.
- It avoids mixing "should compile," "should install," and "should apply now" into one boolean per backend.

## Pack, Family, And Inheritance Hooks

RetroFX 2.x is designed so pack composition can be added later without breaking the authored schema.

The reserved future section is `[compose]`, intended for fields such as:

- `compose.base`
- `compose.mixins`
- `compose.family_defaults`
- `compose.assets`

These concepts are intentionally deferred in TWO-02.
They are reserved so later schema work can add composition cleanly, but baseline 2.x parsers should fail closed on unsupported composition features until that phase lands.

## What This Schema Intentionally Defers

- backend-specific rules like compositor match expressions
- direct WM or toolkit config syntax
- arbitrary script hooks in profiles
- full inheritance and mixin resolution
- pack-defined imperative behavior
- universal per-target coverage for every token
