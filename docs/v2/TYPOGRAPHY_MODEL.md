# RetroFX 2.x Typography Model

Typography is a first-class part of RetroFX 2.x appearance policy.
It is not a terminal-export afterthought.

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

### Target-Specific Terminal Configuration

Best for:

- Alacritty
- Kitty
- other terminals that can express font family or size directly

Meaning:

- target-local and often directly actionable

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

## Relation To 1.x

1.x already proved the value of:

- session-local fontconfig generation
- terminal font export integration
- explicit AA policy

2.x carries those ideas forward, but makes typography a formal theme subsystem instead of a sidecar attached to selected exports.

