# RetroFX 2.x Icon And Cursor Model

Icon and cursor policy belongs in the 2.x theme layer because it is appearance policy, not render behavior.

## What Icon And Cursor Policy Represents

These tokens express:

- preferred icon-theme identity
- preferred cursor-theme identity
- optional size or variant preferences
- pack- or family-level styling hints

They are part of the platform's appearance story even when a target can only export or suggest them.

## Why This Belongs In Theme, Not Render

Icons and cursors:

- do not require pixel-transform algorithms
- are not compositor effects
- are not display transforms

They are style choices and environment hints.
That makes them theme concerns.

## Family And Pack Influence

Packs and style families may suggest icon and cursor policy.

Examples:

- a workstation-classic family may suggest restrained, low-color icons
- a cyberpunk family may suggest sharper or neon-accented icon sets
- a grayscale-focus family may suggest neutral cursor themes

These suggestions remain subordinate to explicit profile values.

## Target Behaviors

Targets may handle icon and cursor policy in three broad ways.

### Apply

Some environments may truthfully support scoped apply behavior.

Examples:

- session-scoped cursor selection in a managed environment

### Export Or Install

Many environments can support:

- config exports
- install-owned theme selections
- managed defaults

### Ignore With Warning

Some targets cannot use icon or cursor policy meaningfully.

Examples:

- TTY
- terminal-only targets
- render-only shader targets

## Capability Awareness

Icon and cursor support must remain capability-aware.

- not all targets can change icon state directly
- not all targets can change cursor state directly
- some DEs and toolkits only support export or session hints
- some targets should ignore these tokens entirely

That is acceptable if the behavior is explicit.

## Current v2alpha1 Schema Alignment

In the current authored schema:

- icon-theme choice is carried by `chrome.icon_theme`
- icon-theme variant is carried by `chrome.icon_variant`
- cursor-theme choice is carried by `chrome.cursor_theme`
- cursor size is carried by `chrome.cursor_size`
- cursor variant is carried by `chrome.cursor_variant`

That is acceptable for `v2alpha1`, but the logical model should remain:

- icon policy belongs to the theme icon subsystem
- cursor policy belongs to the theme cursor subsystem

If later schema work adds dedicated authored icon or cursor sections, target adapters should not need to relearn the semantic meaning.

## Relation To Target Families

Most relevant families:

- toolkit or desktop export targets
- WM-facing config targets
- session helper targets when they own a truthful path

Implemented now:

- TWO-18 adds export-only toolkit artifacts that serialize icon and cursor policy explicitly under `v2/out/<profile-id>/icon-cursor/` and `v2/out/<profile-id>/desktop-style/`
- these artifacts are intended for manual inspection or later session integration, not live DE mutation

Least relevant families:

- TTY
- pure terminal exports
- X11 shader sources

## Relation To 1.x

1.x largely treated icon and cursor choices as out of scope.
2.x broadens the product to include them as style policy, but still without promising universal DE ownership.
