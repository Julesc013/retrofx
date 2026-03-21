# RetroFX 2.x Technical Beta Readiness

This document records the readiness decision after the TWO-33 technical-beta execution cycle.

It is based on [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md), [TECHNICAL_BETA_BLOCKERS.md](TECHNICAL_BETA_BLOCKERS.md), and the current tagged candidate package `v2.0.0-techbeta.1`.

Decision date: 2026-03-22

## Verdict

READY_FOR_LIMITED_TECHNICAL_BETA_CONTINUATION=yes

READY_FOR_BROADER_BETA_STABILIZATION=no

NEEDS_ANOTHER_TECHNICAL_BETA_REMEDIATION_CYCLE=no

## What “Limited Technical Beta” Means Here

For RetroFX 2.x at TWO-33, the limited technical beta means:

- advanced testers can use the copied-toolchain package without a repo checkout
- workflows remain user-local, reversible, and bounded
- supported, degraded, and unsupported environments are explicit
- diagnostics capture is sufficient for structured bug reports

It does not mean:

- general-public beta
- stable or production readiness
- live Wayland ownership
- broad migration guarantees
- replacement of 1.x

## Why Continuation Is Approved

- the first execution cycle completed without a technical-beta-blocker
- candidate package generation, install, diagnostics, uninstall, and cleanup all behaved as documented
- bounded X11 apply or off remained within 2.x-owned roots
- degraded Wayland behavior stayed honest instead of pretending to be supported live runtime

## Why Broader Beta Stabilization Is Not Approved

- the current evidence still comes from one operator and one real X11 plus `i3` host
- broader beta would need more real-host breadth and real outside tester evidence
- migration and explicit X11 preview remain supplementary internal surfaces rather than part of the outside-facing promise

## Recommended Next Step

Continue the limited technical beta with the current tagged candidate package, collect real outside advanced-tester reports through the new templates, and revisit broader beta stabilization only after the evidence base widens.
