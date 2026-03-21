# RetroFX 2.x Theme Compilation

Theme compilation is the path that turns resolved appearance policy into target-specific non-render theme inputs and artifacts.

The canonical shape is:

`resolved profile -> theme token set -> target-specific theme adapter inputs -> emitted theme artifacts`

## What Theme Compilation Consumes

Theme compilation consumes:

- resolved profile
- resolved semantic colors
- resolved terminal and TTY palette sets
- resolved typography policy
- resolved icon and cursor policy
- resolved chrome hints
- target plan
- artifact-planning context

It does not consume raw authored profile text directly.

## Theme Token Set

The theme token set is the target-agnostic appearance bundle prepared for theme-capable targets.

It should include:

- core semantic colors
- chrome tokens
- terminal and TUI theme tokens
- typography roles
- icon and cursor policy
- family-derived defaults already concretized

## What Theme Compilation Emits

Theme compilation itself should remain mostly side-effect free until target adapters emit files.
Conceptually it emits:

- target-family-specific theme adapter inputs
- token-consumption maps
- degradation records for unsupported theme semantics

Target adapters then emit:

- terminal theme files
- WM config fragments
- toolkit export hints
- icon or cursor selection exports

## Defaults And Overrides

Theme compilation should respect this order:

1. explicit resolved profile values
2. explicit target-level overrides already reflected in the resolved profile
3. family and pack defaults
4. deterministic theme fallback rules

No target adapter should invent a new default that bypasses this order.

## Unsupported Theme Tokens

Unsupported theme tokens should degrade explicitly.

Typical outcomes:

- consume fully
- ignore with warning
- map to nearest supported theme construct
- switch to export-only behavior if apply semantics would be false

Examples:

- a TTY target ignores `icon_theme`
- a terminal target ignores `menu_bg`
- a WM target maps `inactive_dim` to an available dim color field

## Reporting Requirements

Theme-capable target compilers should report:

- consumed tokens
- ignored tokens
- degraded mappings
- tokens that had no target representation

This reporting matters because theme degradation can otherwise become invisible.

## Theme Compilation Versus Render Compilation

Theme compilation answers:

- what should the environment look like
- which non-render constructs express that look

Render compilation answers:

- how should pixels or display output be transformed where supported

They can cooperate on the same profile, but neither should absorb the other.

## Relation To 1.x

1.x already had seeds of theme compilation in:

- Xresources generation
- Alacritty export
- session-local fontconfig generation

2.x generalizes that into a formal theme subsystem instead of scattering appearance work across export branches and runtime logic.

