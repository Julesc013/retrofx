# RetroFX 2.x Product Definition

RetroFX 2.x is a profile-driven appearance compiler and session orchestration platform for Linux user environments.
Its job is to take one semantic appearance profile and compile it into multiple target-specific outputs across TTY, TUI, terminals, X11, Wayland-adjacent paths, and selected desktop tooling, with optional render transforms where those transforms are actually supportable.

RetroFX 2.x is broader than RetroFX 1.x.
It is not just a shader tool, not just an X11 effect wrapper, and not merely a collection of scripts.
It also does not promise identical behavior on all stacks.

Current branch truth as of TWO-21:

- the implemented branch surface is still experimental and developer-facing
- the unified entrypoint is `scripts/dev/retrofx-v2`
- 1.x remains the production runtime and CLI
- bounded apply or off, X11 preview, install, and toolkit exports exist, but they do not amount to production-ready desktop ownership

## Who It Is For

- Linux users who want one coherent retro or style-driven appearance across multiple tools and session layers.
- Dotfile and session integrators who want deterministic generated artifacts instead of hand-maintained theme sprawl.
- Profile and pack authors who want to describe appearance semantically rather than write one-off configs per app.
- Users who care about explicit support truth, recoverable apply/off behavior, and honest degraded paths.

## Problems It Solves

- A single style intent often has to be re-authored separately for terminals, TTY, TUIs, WM config, and session wrappers.
- Render effects, palette choices, typography, and session integration are usually mixed together in ad hoc scripts with unclear ownership.
- Linux environments do not expose the same theming or post-processing hooks, so users need truthful degradation instead of false promises.
- Exporting a theme is easier than safely applying and recovering it; RetroFX treats those as separate lifecycle concerns.
- Curated retro looks are easier to maintain as packs and style families than as scattered per-target snippets.

## How 2.x Differs From 1.x

RetroFX 1.x is a stable, narrower product centered on a documented X11 render path plus deterministic exports and scoped backends.
RetroFX 2.x keeps the profile-driven and safety-oriented mindset, but changes the product definition:

- 1.x is a retro rendering and theming tool with a primary X11 runtime path.
- 2.x is a platform that compiles one semantic profile into multiple target outputs and session plans.
- 1.x support truth is mostly described per environment.
- 2.x support truth is enforced through an explicit capability model and status classes.
- 1.x architecture is implementation-led.
- 2.x architecture is module-led: core, theme, render, session, packs, and target adapters are separated by contract.

## Major Product Pillars

### Appearance Profiles

Profiles describe intent at the semantic level: palette roles, typography preferences, style mode, render preferences, session policy, and target selection.
The profile is the source of truth; backend-specific config syntax is not.

### Target Compilers

Target compilers turn the resolved profile into concrete outputs for terminals, TUIs, TTY, WMs, toolkit exports, and session files.
Each compiler is bounded by a declared capability contract.

### Render Transforms

Optional render transforms cover effects such as quantization, dithering, scanlines, glow, gamma, temperature, and bias.
These are only promised where a backend can actually host them.

### Theme Generation

Static theme generation covers colors, fonts, icons, cursors, terminal themes, and WM or DE configuration outputs.
Theme generation is broader than runtime effects and must still be useful where render support is unavailable.

### Session Orchestration

RetroFX 2.x manages apply, export, install, off, repair, and environment scoping as explicit lifecycle operations.
It owns only declared integration points and does not rely on hidden global mutations.

### Packs And Style Families

Packs are curated style families with metadata, palettes, typography guidance, preview information, and reusable design language.
Packs are data products, not arbitrary executable customization bundles.

## Product Standard

RetroFX 2.x succeeds if it can truthfully say:

- what profile intent was requested
- what each target can really support
- what was compiled
- what was applied
- what was exported only
- what degraded and why

If those answers are unclear, the design is not ready.
