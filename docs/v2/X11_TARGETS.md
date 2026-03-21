# RetroFX 2.x X11 Targets

The X11 family is the primary early render-capable target family in RetroFX 2.x.
It remains important, but it is no longer the definition of the whole product.

## Current Implementation Status

As of TWO-17:

- `v2/targets/x11/` now contains a real bounded X11 render family
- implemented dev-only targets currently cover:
  - `x11-shader`
  - `x11-picom`
  - `x11-render-runtime`
  - `x11-display-policy`
- implemented render scope is intentionally narrow:
  - passthrough
  - monochrome with bands
  - `vga16` palette mode
  - bounded `blur`, `ordered dither`, `scanlines`, `flicker`, `vignette`, and `hotcore`
- `v2/session/dev/preview_x11_render.py` and `scripts/dev/retrofx-v2-preview-x11` now stage those artifacts and can run an explicit short-lived `picom` probe
- this remains dev-only, X11-only, and non-default

## Family Scope

The X11 family includes targets such as:

- picom config target
- shader source target
- X11 render helper outputs where appropriate

Session wrappers and Xsession ownership remain primarily session-orchestration concerns, not generic target-compilation concerns.

## picom Config Target

Consumes:

- resolved render policy
- selected theme tokens relevant to compositor-side behavior
- X11 target-plan requirements

Emits:

- compositor config artifacts

Mode:

- export-capable
- apply-preview-capable only through the explicit TWO-17 dev X11 probe path
- not a production session owner
- install-capable in managed X11 session flows

Cannot represent:

- general DE theming
- toolkit-wide look and feel

## Shader Source Target

Consumes:

- resolved render mode
- quantization policy
- palette policy
- effects
- display transform policy
- glow tint and related semantic render inputs

Emits:

- shader or render-source artifacts

Mode:

- export-capable
- live-preview-capable only in the truthful X11 + `picom` dev path

Cannot represent:

- session policy by itself
- WM configuration
- toolkit exports

## X11 Helper Relationship

X11 targets may emit artifacts required by a future X11 session path, but they do not own wrapper or session lifecycle policy.

That means:

- the adapter emits compositor or shader inputs
- session orchestration decides whether and how those become active
- the current TWO-17 preview path only validates this relationship in a bounded dev-only way

## Relevant Token Classes

Most relevant:

- render mode
- quantization and palette policy
- effects
- display transforms
- selected semantic color tokens such as glow or cursor-related hints when the render path uses them

Usually irrelevant or only weakly relevant:

- deep toolkit theme hints
- many chrome tokens
- unrelated icon or cursor theme selection

## Where Compositor Requirement Is Decided

Compositor requirement is decided during capability filtering and target planning, not inside final X11 emission.

The X11 family may declare:

- that a target requires a compositor host
- that a target can operate only on X11

But the decision that the active plan requires a compositor belongs to the planner.

Current TWO-17 implementation note:

- the planner now computes an explicit `x11_render` summary
- that summary reports:
  - requested render mode
  - implemented bounded mode
  - whether live preview is possible in the detected X11 environment
  - what degraded cleanly to export-only or passthrough

## How X11 Targets Differ From Theme-Only Targets

X11 targets differ because they may:

- consume real render policy
- require runtime host support
- participate in stronger apply and validation behavior

Theme-only targets generally:

- consume tokens and emit config
- do not require compositor-hosted runtime semantics

## Limitations

- the X11 render family is not the same as desktop-wide theming
- the X11 path remains environment-dependent
- a truthful X11 target plan may still degrade or export-only when the compositor path is unavailable
- Wayland render remains unsupported in TWO-17
- the dev probe path does not replace the 1.x runtime and does not claim default session ownership

## Relation To 1.x

1.x `x11-picom` is the clearest source of practical lessons here:

- shader and compositor artifacts should be explicit
- runtime intent should be explicit
- degradation must be honest when the host path is unavailable

2.x keeps those lessons, but moves them behind target compilers and session orchestration rather than one shell backend.
