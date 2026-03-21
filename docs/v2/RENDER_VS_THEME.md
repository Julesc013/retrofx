# RetroFX 2.x Render Versus Theme

RetroFX 2.x uses one profile, but two different appearance subsystems:

- theme
- render

Keeping them separate is essential.

## Why They Are Separate

Theme describes semantic appearance policy.
Render describes pixel or display transforms.

Theme answers:

- what colors, fonts, icons, cursors, and chrome choices should exist
- how terminals, WM configs, toolkits, and UI surfaces should be themed

Render answers:

- whether output should be quantized
- whether scanlines, dithering, glow, or display transforms should apply
- how a render-capable host should transform pixels

Current TWO-13 implementation note:

- theme compilation is already real for terminal, WM, and typography-policy outputs
- render is still mostly advisory, but display-policy values are now resolved, planned, and exported in the first X11/render-adjacent compiler slice
- this remains export-oriented and non-destructive, not live global display control

## Where They Overlap

They overlap conceptually because they share one resolved profile.

Examples:

- the same semantic palette may feed terminal theme files and render palette transforms
- `glow_tint` may be chosen by theme and consumed by render
- strictness may influence both theme defaults and acceptable render degradation

But overlap does not mean they should be implemented in one blob.

## Why One Ad Hoc Blob Is Wrong

If theme and render collapse into one subsystem:

- theme-only targets inherit render assumptions they cannot use
- render-capable targets may start owning typography or icon policy by accident
- target compilers have no clear contract for non-render outputs
- degradation becomes harder to explain

That is exactly what 2.x is meant to prevent.

## Theme-Only Profiles

Examples:

- a warm-night readability profile with strong typography and toolkit hints but no render effects
- a grayscale-focus workstation profile that mainly changes colors, fonts, and chrome

These should remain valuable even where no render-capable host exists.

## Render-Emphasis Profiles

Examples:

- an X11 CRT profile whose main change is quantization, scanlines, and glow while theme tokens remain close to defaults
- a phosphor-like render preset that keeps terminal outputs conservative but strongly changes the compositor path

Even here, the profile still has theme data.
The point is that render is the dominant differentiator.

## Combined Profiles

Examples:

- a strict green CRT profile with green semantic colors, bitmap-ish fonts, and X11 render transforms
- a VFD-inspired profile with warm theme tokens plus hotcore render behavior

These are likely common in RetroFX.
They still benefit from keeping the subsystems separate:

- theme compiles non-render outputs
- render compiles render-capable outputs

## Separation Rule

Use this rule in future prompts:

- if the work is about colors, typography, icons, cursors, chrome, terminal themes, or toolkit hints, it belongs to theme
- if the work is about quantization, palette transforms, scanlines, glow algorithms, or display transforms, it belongs to render

## Carry-Forward From 1.x

1.x often mixed exports, fonts, and render-adjacent behavior in one practical flow.
2.x keeps the useful ideas but separates the subsystems so target compilers and planners can stay coherent.
