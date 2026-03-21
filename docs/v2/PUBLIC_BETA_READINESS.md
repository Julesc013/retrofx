# RetroFX 2.x Public Beta Readiness

This document answers the public-surface question for the current 2.x branch after the TWO-33 execution pass.

It is not a public release note.
It does not authorize automatic publication.

Decision date: 2026-03-22

## Verdict

READY_FOR_LIMITED_PUBLIC_TECHNICAL_BETA=yes

READY_FOR_CONTINUED_NON_PUBLIC_PRE_BETA=no

NEEDS_ANOTHER_HARDENING_CYCLE=no

## What “Limited Public Technical Beta” Means Here

For RetroFX 2.x, a limited public technical beta now means:

- technically literate outside testers can use the copied-toolchain package without source-tree archaeology
- package, install, uninstall, diagnostics, and cleanup behavior are predictable enough for that narrow audience
- degraded and unsupported environments are explicit enough to keep support burden manageable
- 1.x remains the production line and 2.x remains clearly experimental

It still does not mean:

- general-public beta
- production readiness
- replacement of the 1.x runtime or CLI
- live Wayland render
- global desktop ownership
- broad migration compatibility promises

## Why The Answer Is Still Yes

- the externally visible tester surface is now the narrower `retrofx-v2-techbeta` wrapper rather than the broader internal developer surface
- the technical-beta package now carries a copied runnable toolchain instead of assuming a repo checkout
- bounded apply or off remains user-local and reversible, and is explicitly gated to X11-oriented environments
- migration and the explicit X11 probe are no longer overexposed; they remain on the internal developer surface
- TWO-33 executed the candidate workflow end-to-end and did not uncover a public-surface blocker for the narrowed technical-beta line

## What Remains Narrow

- validated live runtime support is still centered on X11 plus `i3`-like environments
- Wayland remains plan, compile, bundle, and diagnostics territory rather than supported live runtime ownership
- toolkit outputs remain advisory exports
- 1.x remains the production line

## Current Branch Position

- continue internal alpha: yes
- continue non-public pre-beta: no
- limited public technical beta: yes
- next step: continued limited technical-beta circulation, structured outside-style evidence capture, and broader-beta reassessment only after the current evidence base grows
