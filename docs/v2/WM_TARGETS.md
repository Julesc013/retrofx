# RetroFX 2.x WM Targets

Window manager targets occupy the space between pure theme export and full session orchestration.
They are intentionally treated as their own family.

## Family Scope

The WM family includes:

- `i3`
- `sway`
- `awesome` as a future or secondary family member
- adjacent WM-facing targets such as `waybar`, `rofi`, and `wofi`

## i3

Type:

- mixed theme and session-adjacent target

Consumes:

- semantic color tokens
- typography roles
- selected chrome tokens such as gaps and bar style
- selected session hints when the plan includes an `i3`-owned path

Emits:

- i3 config fragments
- palette variables
- optional helper snippets

Mode:

- export-capable
- install-capable
- apply-now only when a future session plan explicitly owns i3 reload behavior

Limitations:

- does not itself decide X11 render behavior
- must stay separate from compositor or wrapper ownership

## sway

Type:

- mixed theme and session-adjacent target

Consumes:

- semantic theme tokens
- typography roles
- selected chrome tokens
- wayland-era WM config intent

Emits:

- sway config fragments
- related style variables

Mode:

- export-capable
- install-capable
- apply-now only when a future scoped sway integration path exists

Key limitation:

- sway may support theme and config targets without supporting global render transforms

This distinction must remain explicit.

## awesome

Type:

- future or secondary WM config target

Consumes:

- semantic theme tokens
- typography roles
- chrome hints where representable

Emits:

- awesome-oriented theme or config fragments

Mode:

- export-first
- install-capable when a managed config path exists

Limitations:

- first-class support should not be claimed before real adapter maturity exists

## waybar

Type:

- adjacent WM-facing target
- mostly theme-only

Consumes:

- semantic theme tokens
- typography roles
- bar-style hints

Emits:

- waybar config or style fragments

Mode:

- export-capable
- install-capable

Limitations:

- no render semantics
- no session ownership by itself

## rofi / wofi

Type:

- adjacent launcher targets

Consumes:

- semantic theme tokens
- typography roles
- launcher-style hints

Emits:

- launcher theme or config fragments

Mode:

- export-capable
- install-capable
- apply-now only if a future session path truthfully owns reload behavior

Limitations:

- no global render semantics
- may be useful on both X11 and Wayland without implying compositor ownership

## Degradation Expectations

WM targets should degrade explicitly when:

- render-heavy intent is not representable
- session ownership is unavailable
- only export/install paths are truthful

Common downgrade pattern:

- keep theme/config emission
- drop unsupported render behavior
- switch apply intent to export-only or install-only when needed

## Relation To 1.x

1.x focused on i3 wrapper flows and manual integration elsewhere.
2.x keeps i3 and sway important, but reframes them as target compilers plus separate session orchestration instead of one combined shell path.

