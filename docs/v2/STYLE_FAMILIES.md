# RetroFX 2.x Style Families

Style families are higher-level appearance identities that sit above raw tokens.
They are not targets and they are not backend behaviors.

As of TWO-14, style-family identity is now embodied in real local pack manifests under `v2/packs/`.
The pack system remains local and dev-only, but family metadata is no longer docs-only.

## Purpose

A style family provides:

- aesthetic lineage
- default token tendencies
- typography preferences
- icon or cursor suggestions
- pack identity

It does not override explicit profile values.

## Families Versus Strictness

RetroFX 2.x should treat these as related but distinct:

- style family: what the appearance wants to feel like
- strictness or stance: how strongly it should preserve that identity versus compromise for usability

Examples:

- `warm-night` is a family
- `strict-authentic` is primarily a stance
- `practical-daily-driver` is primarily a stance

Some pack catalogs may present families and stances together as presets, but the engine should keep the concepts separate.

## Example Style Families

### `strict-authentic`

Used in practice as a style stance or preset label.
Characteristics:

- minimal compromise
- stronger tolerance for degraded comfort
- more likely to prefer era-correct fonts, palettes, and low-chrome output

### `modernized-retro`

Often a bridge between family and stance.
Characteristics:

- retro cues preserved
- readability and modern app compatibility improved

### `practical-daily-driver`

Primarily a stance.
Characteristics:

- balanced readability
- comfortable typography
- broader target usefulness

### `noir-minimal`

Characteristics:

- low-chroma palette
- restrained chrome
- subtle accents

### `cyberpunk`

Characteristics:

- high-contrast accent colors
- stronger chrome identity
- vivid terminal and launcher personality

### `warm-night`

Characteristics:

- warm dark surfaces
- reduced glare
- comfortable late-night readability

### `grayscale-focus`

Characteristics:

- neutral palette
- low distraction
- strong typography priority

### `workstation-classic`

Characteristics:

- conservative chrome
- practical terminals
- mature UI tones

### `vfd-nixie-terminal-industrial`

Characteristics:

- industrial display cues
- warm or phosphor-like accent tendencies
- specialized typography suggestions

## Influence Rules

Style families may influence:

- default semantic colors
- typography recommendations
- icon and cursor suggestions
- chrome defaults
- theme-side terminal or TUI tendencies

Style families must not:

- bypass explicit user values
- declare target capabilities
- force unsupported environments to pretend support

## Relation To Packs

Packs are likely to be the main carriers of style family identity.
They can provide:

- family metadata
- default theme token seeds
- preview metadata
- typography and icon suggestions

That makes style families especially important for future pack design.

Current implementation truth:

- built-in local packs now exist for `crt-core`, `terminal-classic`, and `modern-minimal`
- pack manifests now carry family metadata, tags, and curated profile catalogs
- pack-aware dev commands can resolve profiles from those packs and surface the originating family metadata
- pack-local recommendations and assets are metadata-only at this stage; they do not apply anything by themselves

## Relation To 1.x

1.x core packs already hinted at family identity through pack names and profile tags.
2.x formalizes that layer so packs can influence defaults cleanly without coupling aesthetic identity to implementation branches.
