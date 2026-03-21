# RetroFX 2.x Terminal And TUI Targets

Terminal and TUI targets are a first-class family in RetroFX 2.x.
They are a major reason the platform exists at all: they provide broad value without requiring global compositor ownership.

## Family Contract

These targets primarily consume:

- semantic color tokens
- terminal ANSI mappings
- typography roles
- selected chrome hints where an app can express them

They usually do not consume:

- compositor-bound render effects
- session-level wrapper logic

## Semantic ANSI Mapping

Terminal and TUI targets should consume the resolved ANSI sets, not re-derive them from raw semantic anchors.

That means:

- semantic-to-ANSI mapping happens in the core pipeline
- terminal and TUI adapters consume resolved terminal ANSI slots
- TTY-specific variants consume resolved TTY ANSI slots

This preserves cross-target consistency.

## Xresources

Consumes:

- semantic theme tokens
- resolved terminal ANSI palette
- terminal typography hints where representable

Emits:

- `Xresources`-style resource file or fragment

Mode:

- export-first
- install-capable
- limited apply via session-managed resource loading, not by the adapter inventing session policy

Cannot represent:

- compositor render transforms
- deep session policy
- most chrome hints

## Alacritty

Consumes:

- semantic theme tokens
- resolved terminal ANSI palette
- terminal typography roles

Emits:

- Alacritty config fragment or file

Mode:

- export-capable
- install-capable
- apply-now only when session orchestration explicitly manages it

Cannot represent:

- compositor render pipeline
- global session behavior
- most WM or DE chrome semantics

## Kitty

Consumes:

- semantic theme tokens
- resolved terminal ANSI palette
- terminal typography roles

Emits:

- Kitty config fragment or file

Mode:

- export-capable
- install-capable
- apply-now only in explicitly scoped session ownership

Cannot represent:

- compositor render transforms
- global DE policy

## tmux

Consumes:

- semantic theme tokens
- resolved terminal ANSI palette
- selected typography or style hints where tmux can express them

Emits:

- tmux theme fragment

Mode:

- export-capable
- install-capable
- apply-now only if a future session path truthfully owns tmux reload behavior

Cannot represent:

- typography in a desktop-wide sense
- real render effects

## vim Or Neovim

Consumes:

- semantic theme tokens
- resolved ANSI or derived app palette
- selected UI emphasis tokens

Emits:

- theme file or colorscheme fragment

Mode:

- export-capable
- install-capable
- usually not a core apply-now target in early 2.x

Cannot represent:

- session policy
- compositor behavior

## btop / htop-Style TUI Palette Targets

Consumes:

- semantic theme tokens
- resolved ANSI palette
- limited emphasis tokens

Emits:

- app palette fragments or config

Mode:

- export-capable
- install-capable

Cannot represent:

- typography ownership in most cases
- render effects

## Family Limitations

- terminal and TUI targets are theme-first, not render-first
- they benefit from the semantic pipeline, but they do not justify raw-profile shortcuts
- they may be apply-capable only when session orchestration explicitly owns the path

## Relation To 1.x

1.x already proved the value of:

- deterministic Xresources export
- deterministic Alacritty export
- ANSI-centric palette bridging

2.x carries those ideas forward, but makes them resolved-model target compilers rather than ad hoc export branches.

