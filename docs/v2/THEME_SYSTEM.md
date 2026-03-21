# RetroFX 2.x Theme System

RetroFX 2.x theme is the subsystem that turns semantic appearance policy into non-render target outputs.

Theme is not the same as render.

- Theme = semantic appearance policy compiled into target-specific non-render outputs
- Render = pixel or display transforms compiled into render-capable targets

## What The Theme System Is Responsible For

The 2.x theme system is responsible for:

- semantic color policy
- terminal and TUI theme mapping
- typography policy
- icon and cursor policy
- chrome and UI styling hints
- WM and toolkit-facing appearance hints
- theme-side defaults influenced by family and strictness

Typical outputs influenced by theme:

- terminal color configs
- TUI theme exports
- WM chrome colors and style fragments
- font stacks and AA policy hints
- icon and cursor theme selection hints
- toolkit export hints
- launcher, bar, and notification styling fragments

## What The Theme System Is Not Responsible For

The theme system is not responsible for:

- low-level shader math
- compositor-specific effect algorithms
- quantization or dithering algorithms
- display transform math
- environment detection
- session startup decision logic
- target selection policy
- raw profile parsing

## Relation To The Resolved Profile

Theme operates on the resolved semantic model inside the resolved profile.

That means theme compilation consumes:

- resolved semantic colors
- resolved typography policy
- resolved icon and cursor policy
- resolved chrome hints
- resolved terminal and TTY palette sets

Theme does not consume raw profile TOML directly.

## Relation To Target Compilers

Target compilers are the downstream consumers of theme outputs.

The sequence is:

- resolved profile
- theme token set
- target-specific theme adapter inputs
- emitted theme artifacts

Some targets consume theme only.
Some consume theme plus render.
But no target should be forced to reconstruct theme semantics locally.

## Relation To Session Orchestration

Theme does not decide when a target becomes live.
It only provides appearance policy and target-ready inputs.

Session orchestration decides:

- apply timing
- install timing
- ownership of live paths
- rollback, repair, and recovery behavior

## Relation To Render

Theme and render share the same resolved profile, but they are separate subsystems.

Theme handles:

- colors
- typography
- icons
- cursors
- chrome style
- toolkit and WM appearance hints

Render handles:

- quantization
- palette transforms
- scanlines
- glow as an effect algorithm
- display transforms

`glow_tint` is a useful example:

- as a theme token, it describes a preferred tint
- as a render effect, glow is the algorithm that may consume that tint

The tint belongs to theme.
The algorithm belongs to render.

## Theme Subsystem Outputs

The theme subsystem should eventually provide:

- canonical theme token sets
- target-family-specific theme adapter inputs
- token-usage and degradation reports

Those outputs are still side-effect free.
File emission stays in target adapters.

Current TWO-18 implementation note:

- toolkit-facing target adapters now consume resolved semantic colors, typography roles, and icon or cursor policy to emit advisory GTK, Qt, and desktop-style artifacts
- those outputs remain export-only and do not imply live desktop settings ownership

## What Later Prompts Should Build Here

Future implementation prompts should build:

- semantic color and chrome-token derivation helpers
- typography policy preparation for terminal, session-local, and export-oriented targets
- icon and cursor policy preparation that remains capability-aware
- family-driven theme default helpers that remain subordinate to explicit profile values
- side-effect-free theme compilation helpers that feed target adapters

Future implementation prompts should not build:

- compositor effect algorithms
- direct backend file emission
- session startup or apply ownership
- environment detection logic

## Carry-Forward From 1.x

2.x carries forward these 1.x ideas:

- terminal exports matter
- session-local font policy matters
- theme artifacts should be deterministic
- export and apply must remain distinct

2.x intentionally departs from 1.x here:

- theme is no longer an incidental side effect of a render path
- typography, icon, and cursor policy become first-class
- WM and toolkit theme compilation are part of the product definition, not ad hoc extras
