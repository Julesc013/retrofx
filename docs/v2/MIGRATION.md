# RetroFX 2.x Migration From 1.x

RetroFX 2.x is not a drop-in schema rename for RetroFX 1.x.
It is a redesign.

This file defines how 1.x concepts map into 2.x concepts, what can be migrated automatically, what needs manual review, and which old ambiguities 2.x resolves by design.

## Migration Principles

- 1.x remains valid on the 1.x line and should not be destabilized.
- 2.x migration should preserve user intent when that intent is clearly representable.
- When 1.x input was backend-heavy or ambiguous, 2.x should prefer explicit redesign over pretending the old field maps perfectly.
- Migration should produce semantic intent first and let the 2.x compiler derive target plans later.

## Direct Concept Mapping

| 1.x Concept | 2.x Concept | Migration Class | Notes |
| --- | --- | --- | --- |
| top-level `name` | `identity.name` | automatic | Direct copy. |
| top-level `description` | `identity.description` | automatic | Direct copy. |
| top-level `tags` | `identity.tags[]` | automatic | Direct copy. |
| top-level `author` | `identity.author` | automatic | Direct copy. |
| top-level `license` | `identity.license` | automatic | Direct copy. |
| profile file basename or pack id | `identity.id` | assisted | 1.x has no explicit stable id field; migration should derive a slug. |
| pack context | `identity.family` | assisted | Usually inferred from tags or pack lineage such as `crt`, `vfd`, `dos`, or `terminal`. |
| no direct 1.x equivalent | `identity.strictness` | manual | Needs user or pack intent; default to `modernized-retro` if unknown. |
| `mode.type` | `render.mode` | automatic | `passthrough`, `monochrome`, and `palette` map directly. |
| `monochrome.bands` | `render.quantization.bands` | automatic | Direct numeric carry-over. |
| `monochrome.phosphor` | semantic color defaults and `identity.family` | assisted | In 2.x phosphor color becomes semantic palette intent, not a dedicated mode field. |
| `monochrome.custom_rgb` | `color.semantic.fg0`, `accent_primary`, `glow_tint` | assisted | Usually becomes the main emitted hue for monochrome-like profiles. |
| `monochrome.hotcore` | `render.effects.hotcore` | automatic | Direct carry-over. |
| `palette.kind` | `render.palette.kind` | automatic | Direct copy in palette mode. |
| `palette.size` | `render.palette.size` | automatic | Direct copy or derive from kind if omitted. |
| `palette.custom_file` | `render.palette.source = "file:..."` | automatic | Relative path semantics stay explicit. |
| `effects.blur_strength` | `render.effects.blur` | automatic | Same intent scale in baseline 2.x. |
| `effects.scanlines` | `render.effects.scanlines` | automatic | Direct carry-over. |
| `effects.flicker` | `render.effects.flicker` | automatic | Direct carry-over. |
| `effects.dither` | `render.effects.dither` | automatic | Direct carry-over. |
| `effects.vignette` | `render.effects.vignette` | automatic | Direct carry-over. |
| `effects.scanline_preset` | family or strictness defaults for scanline behavior | manual | Intentionally not a baseline 2.x top-level token in TWO-02. |
| `effects.transparency` | adapter-scoped migration note | manual | Too backend-heavy for the 2.x core schema in TWO-02. |
| `scope.x11` | `session.targets[]` plus later capability filtering | automatic | `true` usually adds `x11` and often `wm`; `false` omits them. |
| `scope.tty` | `session.targets[]` | automatic | Adds `tty`. |
| `scope.tuigreet` | `session.targets[]` | automatic | Adds `tuigreet`. |
| implicit 1.x current-apply behavior | `session.apply_mode = "current-session"` | assisted | Good default for migrated apply-oriented profiles. |
| 1.x export commands | `session.apply_mode = "export-only"` and `session.persistence = "export-only"` | assisted | Depends on migration goal. |
| 1.x install mode | `session.apply_mode = "installed-default"` and `session.persistence = "installed"` | assisted | Chosen by workflow, not by profile contents alone. |
| `colors.background` | `color.semantic.bg0` | automatic | Direct anchor mapping. |
| `colors.foreground` | `color.semantic.fg0` | automatic | Direct anchor mapping. |
| missing 1.x semantic accents | derived semantic tokens | automatic | 2.x fills these from family, strictness, and anchors. |
| `fonts.tty` | `typography.console_font` | automatic | Direct carry-over. |
| `fonts.terminal` | `typography.terminal_primary` | automatic | Direct carry-over. |
| `fonts.terminal_fallback` | `typography.terminal_fallbacks[]` | automatic | Direct carry-over. |
| `fonts.ui` | `typography.ui_sans` | automatic | Direct carry-over, though 2.x also offers `ui_mono`. |
| no direct 1.x equivalent | `typography.ui_mono` | manual | Choose separately or default from terminal primary. |
| no direct 1.x equivalent | `typography.icon_font` | manual | New 2.x role. |
| no direct 1.x equivalent | `typography.emoji_policy` | manual | New 2.x policy role. |
| `font_aa.antialias` | `typography.aa.antialias` | automatic | Direct carry-over. |
| `font_aa.subpixel` | `typography.aa.subpixel` | automatic | Direct carry-over. |
| no direct 1.x equivalent | `typography.aa.hinting` | manual | New 2.x policy role. |
| 1.x pack metadata | `identity.family`, pack defaults, reserved `compose.*` hooks | assisted | Pack lineage becomes data instead of implicit behavior. |
| 1.x runtime manifest distinction | resolved `artifact_plan.required` and `artifact_plan.optional` | redesign | This moves from implementation detail to planned compiler output. |

## What Can Be Migrated Automatically

These parts are structurally close enough for deterministic migration:

- descriptive metadata
- `mode.type`
- `monochrome.bands`
- `monochrome.hotcore`
- `palette.kind`, `palette.size`, and `palette.custom_file`
- `effects.blur_strength`, `scanlines`, `flicker`, `dither`, and `vignette`
- `scope.*` into `session.targets`
- `fonts.*`
- `font_aa.antialias`
- `font_aa.subpixel`
- `colors.background`
- `colors.foreground`

## What Needs Manual Migration Or Review

- choosing `identity.strictness`
- deciding whether a migrated profile is intended for `current-session`, `installed-default`, `explicit-only`, or `export-only`
- mapping `monochrome.phosphor` into a richer semantic palette when no explicit colors existed
- choosing additional semantic accents beyond what can be safely derived
- adding `typography.ui_mono`, `icon_font`, or `emoji_policy`
- translating 1.x `effects.transparency`
- translating 1.x `rules.*`
- adding chrome hints such as `bar_style`, `launcher_style`, or `notification_style`

## What 2.x Fixes About 1.x Ambiguity

### 1. Scope Becomes Policy

1.x `scope.x11`, `scope.tty`, and `scope.tuigreet` mix target choice with runtime behavior.
2.x splits this into:

- authored target classes under `session.targets`
- lifecycle posture under `session.apply_mode`
- persistence under `session.persistence`
- capability-filtered target plans in the resolved model

### 2. Color Intent Becomes Semantic

1.x mainly carried background, foreground, and render-mode color hints.
2.x gives profiles a semantic palette that can feed terminals, TTY, WM, toolkit, and render-capable adapters consistently.

### 3. Monochrome Phosphor Becomes Style Intent

1.x encodes phosphor as a render-mode knob.
2.x treats the visible hue as part of the semantic palette and family defaults.
That makes the same style family usable in targets that have no render path.

### 4. Export And Apply Become Separate Meanings

1.x often expresses export versus apply through CLI path and backend behavior.
2.x makes that a declared session policy.

### 5. Backend-Specific Hints Stop Polluting The Core

1.x `rules.*` and some effect options are closely tied to the old X11 path.
2.x keeps the core schema semantic and leaves backend-specific controls to adapters or future adapter-scoped extensions.

## Suggested Automatic Migration Posture

For a straightforward 1.x profile, a migration tool should usually:

1. copy metadata into `[identity]`
2. derive `identity.id` from filename or pack id
3. set `identity.family` from pack lineage or tags
4. default `identity.strictness` to `modernized-retro` unless the pack is clearly authenticity-focused
5. map `mode`, palette, effects, fonts, and AA directly
6. turn `scope.*` booleans into `session.targets`
7. choose `session.apply_mode = "current-session"` and `session.persistence = "ephemeral"` unless the migration is explicitly for export-only or installed workflows
8. derive missing semantic tokens from `colors.*`, phosphor, family, and render mode

## Example: 1.x To 2.x Conceptual Migration

1.x:

```toml
name = "CRT Green P1 4-Band"
version = 1

[mode]
type = "monochrome"

[monochrome]
bands = 4
phosphor = "green"
hotcore = false

[effects]
blur_strength = 3
scanlines = true
dither = "ordered"
vignette = true

[scope]
x11 = true
tty = false
tuigreet = false
```

2.x concept:

```toml
schema = "retrofx.profile/v2alpha1"

[identity]
id = "crt-green-p1-4band"
name = "CRT Green P1 4-Band"
family = "crt"
strictness = "strict-authentic"

[color.semantic]
bg0 = "#071109"
fg0 = "#86ff7a"
accent_primary = "#74ff68"
glow_tint = "#74ff68"

[render]
mode = "monochrome"

[render.quantization]
bands = 4

[render.effects]
blur = 3
scanlines = true
dither = "ordered"
vignette = true
hotcore = false

[session]
targets = ["x11", "terminal", "wm"]
apply_mode = "current-session"
persistence = "ephemeral"
```

The key redesign is that the green phosphor is no longer hidden inside a render-only field.
It becomes reusable semantic color intent.

