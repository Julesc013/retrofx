# RetroFX 2.x Typography Model

Typography is a first-class part of RetroFX 2.x appearance policy.
It is not a terminal-export afterthought.

## Current Implementation Status

TWO-12 implements the first real typography slice under `v2/`.

Implemented now:

- normalized typography defaults for `console_font`, `terminal_primary`, `ui_sans`, and `ui_mono`
- resolved typography stacks for terminal and UI monospace roles
- deterministic export-only typography emission for Alacritty and Kitty primary font settings
- deterministic session-local `fontconfig`-style output under `v2/out/<profile-id>/fontconfig/`
- deterministic advisory GTK, Qt, and desktop-style exports now consume `ui_sans`, `ui_mono`, and AA policy where relevant
- typography visibility in the dev compile and session-planning entrypoints

Not implemented yet:

- live desktop font application
- TTY console font application in the 2.x runtime
- full fallback-chain emission for every terminal target
- global emoji fallback orchestration

Clarification:

- TWO-18 adds GTK and Qt-facing export artifacts that carry typography hints
- those exports are advisory and do not imply live toolkit font ownership

## Role-Based Font Design

Typography is defined by roles, not by backend filenames.

| Role | Meaning | Typical Targets |
| --- | --- | --- |
| `console_font` | console or TTY font | TTY, console login, some greet targets |
| `terminal_primary` | primary terminal monospace family | terminals, TUIs, session-local font policy |
| `terminal_fallbacks` | ordered terminal fallback chain | terminals, TUIs |
| `ui_sans` | general UI sans family | WM chrome, toolkit exports, bars, menus |
| `ui_mono` | UI monospace family | editors, bars, code-facing UI |
| `icon_font` | icon or symbol-capable font hint | bars, launchers, notifications |
| `emoji_policy` | emoji handling preference | terminals, toolkit exports, GUI sessions |

Current normalized defaults in the early implementation:

- `terminal_primary` defaults to `monospace`
- `console_font` defaults to `terminal_primary`
- `ui_sans` defaults to `sans-serif`
- `ui_mono` defaults to `terminal_primary`
- `terminal_stack` and `ui_mono_stack` are derived deterministically from the resolved roles

## Anti-Aliasing Policy

Typography policy includes:

- antialiasing
- subpixel mode
- hinting

### Antialiasing

- `default`
- `on`
- `off`

### Subpixel

- `default`
- `rgb`
- `bgr`
- `none`
- other explicit modes only when the schema later expands them

### Hinting

- `default`
- `none`
- `slight`
- `medium`
- `full`

## Scope Distinction

Typography policy may land in different places depending on target and capability.

### Session-Local Fontconfig

Best for:

- WM and toolkit contexts
- terminal sessions launched under a managed session

Meaning:

- session-wide hint or apply path
- still user-scoped, not system-global by default

Implemented now:

- `v2/targets/toolkit/fontconfig.py` emits a deterministic session-local `fontconfig` fragment
- the artifact is export-only and intended for later orchestration or manual inspection

### Target-Specific Terminal Configuration

Best for:

- Alacritty
- Kitty
- other terminals that can express font family or size directly

Meaning:

- target-local and often directly actionable

Implemented now:

- Alacritty emits `font.normal.family` from the resolved `terminal_primary`
- Kitty emits `font_family` from the resolved `terminal_primary`
- fallback chains are preserved in the resolved model, but not yet emitted by those targets

### Export-Only Hints

Best for:

- toolkit export targets
- mixed environments where direct apply is not truthful

Meaning:

- appearance hint only
- must not be misrepresented as guaranteed font control

## Retro Authenticity Versus Practicality

Typography policy is one of the clearest places where style and practicality diverge.

### Strict Bitmap-ish

Characteristics:

- bitmap-like console and terminal fonts
- limited or disabled AA
- strong authenticity

Typical tradeoff:

- lower convenience in mixed GUI environments

### Modernized-Retro

Characteristics:

- retro-feeling monospace choices
- moderate AA
- readable UI pairings

Typical tradeoff:

- less historically exact than strict authenticity

### Nerd-Font-Friendly

Characteristics:

- glyph-rich terminal primary
- stronger fallback strategy
- bar or launcher icon support

Typical tradeoff:

- wider dependency on locally installed fonts

### Emoji-Friendly

Characteristics:

- explicit emoji fallback policy
- practical terminal and GUI usage

Typical tradeoff:

- aesthetics may drift from strict retro authenticity

## Limitations

- TTY console fonts are fundamentally different from GUI fonts
- not every environment can honor every typography token
- some targets can only export hints
- session-local font policy is different from a terminal-specific font setting
- typography support must remain capability-aware and explicit
- the current `fontconfig` artifact is session-local and export-oriented, not a live global font switch
- current terminal compilers emit the primary font role only; fallback-chain support remains partial

## Relation To 1.x

1.x already proved the value of:

- session-local fontconfig generation
- terminal font export integration
- explicit AA policy

2.x carries those ideas forward, but makes typography a formal theme subsystem instead of a sidecar attached to selected exports.
