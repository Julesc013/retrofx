# RetroFX 2.x Validation Rules

This document defines the parser and validator contract for the 2.x profile language.
It covers hard errors, warning-only cases, and normalization defaults.

TWO-08 implements an experimental subset of this contract in `v2/core/validation/`.
The implemented subset focuses on structural validation, core enums and ranges, and a small set of documented incompatible combinations.
Capability-aware warnings and broader schema coverage remain future work.

## Validation Stages

1. Parse TOML syntax.
2. Validate schema identifier and known sections.
3. Validate field types, enums, and ranges.
4. Apply normalization defaults.
5. Validate mode-specific and session-specific combinations.
6. Resolve semantic derivations.
7. Run capability-aware warning generation during target planning.

The validator should fail on structural errors before capability filtering begins.

## Required Fields

| Field | Rule |
| --- | --- |
| `schema` | Required and must be `retrofx.profile/v2alpha1` for this schema revision. |
| `identity.id` | Required. Must be a stable slug. |
| `identity.name` | Required. Non-empty string. |
| `color.semantic.bg0` | Required. Valid color literal. |
| `color.semantic.fg0` | Required. Valid color literal. |
| `render.mode` | Required semantically; normalize to `passthrough` if omitted. |
| `session.apply_mode` | Required semantically; normalize to `current-session` if omitted. |
| `session.persistence` | Required semantically; derive from `apply_mode` if omitted. |
| `session.targets[]` | Required unless the profile is explicitly export-only. |

## Allowed Enums

| Field | Allowed Values |
| --- | --- |
| `identity.strictness` | `strict-authentic`, `modernized-retro`, `practical-daily-driver` |
| `render.mode` | `passthrough`, `monochrome`, `palette` |
| `render.palette.kind` | `vga16`, `mono2`, `mono4`, `mono8`, `mono16`, `cube32`, `cube64`, `cube128`, `cube256`, `custom` |
| `render.effects.dither` | `none`, `ordered` |
| `typography.emoji_policy` | `inherit`, `monochrome`, `color`, `text-only` |
| `typography.aa.antialias` | `default`, `on`, `off` |
| `typography.aa.subpixel` | `default`, `rgb`, `bgr`, `vrgb`, `vbgr`, `none` |
| `typography.aa.hinting` | `default`, `none`, `slight`, `medium`, `full` |
| `chrome.bar_style` | `minimal`, `boxed`, `dense`, `hidden` |
| `chrome.launcher_style` | `minimal`, `boxed`, `dense`, `fullscreen` |
| `chrome.notification_style` | `minimal`, `boxed`, `dense`, `toast` |
| `session.apply_mode` | `current-session`, `export-only`, `installed-default`, `explicit-only` |
| `session.persistence` | `ephemeral`, `installed`, `export-only` |
| `session.targets[]` | `tty`, `tuigreet`, `terminal`, `tui`, `x11`, `wayland`, `wm`, `gtk`, `qt`, `icons`, `cursors`, `notifications`, `launcher` |

## Numeric And Structured Ranges

| Field | Rule |
| --- | --- |
| `render.quantization.bands` | Integer `2..256` when meaningful. |
| `render.palette.size` | Integer `2..256`. Structured kinds must match their fixed size. |
| `render.effects.blur` | Integer `0..6`. |
| `render.display.gamma` | Number `0.5..2.0`. |
| `render.display.contrast` | Number `0.5..2.0`. |
| `render.display.temperature` | Integer `1000..12000`. |
| `render.display.black_lift` | Number `-0.2..0.2`. |
| `render.display.blue_light_reduction` | Number `0.0..1.0`. |
| `chrome.gaps` | Integer `0..64`. |
| `color.terminal.ansi.*` | Slot keys must be `0..15`. Values must be valid color literals. |
| `color.tty.ansi.*` | Slot keys must be `0..15`. Values must be valid color literals. |
| `identity.id` | Slug-like string matching `^[a-z0-9][a-z0-9-]{1,63}$`. |

## Incompatible Combinations: Hard Errors

These combinations should fail validation.

| Condition | Reason |
| --- | --- |
| `render.mode = "monochrome"` and `render.quantization.bands` missing after defaults | Monochrome mode requires band quantization. |
| `render.mode = "palette"` and `render.palette.kind` missing | Palette mode requires palette selection. |
| `render.palette.kind = "custom"` and `render.palette.source` missing | Custom palette mode requires a source. |
| `render.mode != "palette"` and `render.palette.kind` is present | Core render mode and palette policy conflict. |
| `render.mode = "passthrough"` and `render.quantization.bands` is authored explicitly | Quantization request conflicts with passthrough semantics. |
| `session.targets` empty while `session.apply_mode != "export-only"` | Non-export-only profiles must declare a target surface. |
| `session.apply_mode = "export-only"` and `session.persistence != "export-only"` | Lifecycle posture conflicts with export-only mode. |
| `session.apply_mode = "installed-default"` and `session.persistence = "ephemeral"` | Installed default profiles must be install-persistent. |
| unknown top-level sections or unknown keys | 2.x validation remains strict by default. |
| `compose.*` authored before composition support is implemented | Reserved future feature must fail closed until explicitly supported. |

## Warning-Only Cases

These conditions should not fail the profile structurally, but they should be explicit.

| Condition | Warning Behavior |
| --- | --- |
| `identity.family` is unknown to the current pack set | Warn and continue with generic defaults. |
| `color.terminal.ansi.*` overrides only some slots | Warn or note that missing slots will derive from semantic mapping. |
| `color.tty.ansi.*` is absent | Note that TTY ANSI will inherit from terminal ANSI or semantic mapping. |
| `chrome.*` tokens are authored but selected targets have no chrome-capable adapters | Warn during target planning and ignore or export-only where appropriate. |
| render-heavy tokens are authored for theme-only or export-only targets | Warn during capability filtering and degrade deterministically. |
| `typography.icon_font` or `emoji_policy` has no matching adapter support | Warn and ignore for unsupported targets. |
| `session.targets` includes both `x11` and `wayland` | Warn that runtime selection will depend on environment and may degrade. |

## Defaulting Behavior

### Metadata Defaults

- `identity.description`, `tags`, `author`, and `license` default to empty.
- `identity.family` defaults to `custom` when unknown.
- `identity.strictness` defaults to `modernized-retro`.

### Semantic Color Defaults

- `bg1` derives from `bg0`.
- `bg2` derives from `bg1` or `bg0`.
- `fg1` derives from `fg0` and `bg0`.
- `fg2` derives from `fg1`.
- `accent_primary` defaults from family preset, then `fg0`.
- semantic accent roles default from `accent_primary` and family heuristics.
- border, selection, glow, and cursor roles derive from the nearest semantic anchors.

### Terminal And TTY Defaults

- `color.terminal.ansi.*` derives from semantic mapping.
- `color.tty.ansi.*` inherits terminal ANSI first, then semantic mapping.

### Typography Defaults

- `typography.terminal_fallbacks[]` defaults to empty.
- `typography.ui_mono` defaults from `terminal_primary` if absent.
- `typography.emoji_policy` defaults to `inherit`.
- `typography.aa.*` defaults to `default`.

### Render Defaults

- `render.mode` defaults to `passthrough`.
- `render.quantization.bands` defaults to `8` in monochrome mode.
- `render.palette.size` defaults from `render.palette.kind` for structured palette kinds.
- `render.effects.blur` defaults from family and strictness heuristics, otherwise `0`.
- `render.effects.dither` defaults to `none`.
- boolean effects default to `false`.
- `render.display.gamma` and `contrast` default to `1.0`.
- `render.display.temperature` defaults to `6500`.
- `render.display.black_lift` defaults to `0.0`.
- `render.display.blue_light_reduction` defaults to `0.0`.

### Session Defaults

- `session.apply_mode` defaults to `current-session`.
- `session.persistence` defaults by `apply_mode`:
  - `current-session -> ephemeral`
  - `installed-default -> installed`
  - `export-only -> export-only`
  - `explicit-only -> ephemeral`

## Error Versus Warning Rule

Use this rule consistently:

- fail with an error when the authored profile is internally contradictory or impossible to normalize
- warn when the authored profile is structurally valid but some selected targets cannot use all of its intent

Examples:

- `render.mode = "palette"` without `render.palette.kind` is an error
- `chrome.bar_style = "dense"` on a pure TTY target is a warning
- `render.effects.scanlines = true` on a terminal-only export profile is a warning with deterministic degradation

## Capability-Aware Validation

The validator should stop at structural correctness.
Capability-aware warnings belong to planning, but they follow this contract:

- unsupported target-specific use of a valid semantic token should warn and degrade
- structurally invalid token use for the chosen mode should fail
- export-only outcomes should be explicit, not silent fallback
