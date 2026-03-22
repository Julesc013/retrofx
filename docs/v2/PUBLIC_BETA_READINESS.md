# RetroFX 2.x Public Beta Readiness

This document answers the public-surface question for the current `main` branch after the rapid technical-beta execution pass on 2026-03-22.

It is not a public release note.
It does not authorize automatic publication.

## Verdict

READY_FOR_LIMITED_PUBLIC_TECHNICAL_BETA=yes

READY_FOR_CONTINUED_NON_PUBLIC_PRE_BETA=no

NEEDS_ANOTHER_HARDENING_CYCLE=yes

## What “Limited Public Technical Beta” Means Here

For RetroFX 2.x, a limited public technical beta means:

- technically literate outside testers can use the narrower `retrofx-v2-techbeta` surface
- package, install, uninstall, diagnostics, and cleanup behavior are predictable enough for that narrow audience
- degraded and unsupported environments are explicit enough to keep support burden manageable
- `1.x` remains the production line and `2.x` remains clearly experimental

It still does not mean:

- general-public beta
- production readiness
- replacement of the `1.x` runtime or CLI
- live Wayland render
- global desktop ownership
- broad migration compatibility promises

## Why Limited Technical Beta Still Stands

- the externally visible tester surface remains the narrower `retrofx-v2-techbeta` wrapper rather than the broader internal developer surface
- the copied-toolchain technical-beta package remains the intended outside-facing delivery shape for advanced testers
- diagnostics capture, bounded `apply` or `off`, and temp-HOME install or uninstall remain usable for advanced testers
- degraded Wayland behavior remains explicit and supportable

## Why Another Hardening Cycle Is Still Needed

- the fallback install path still records internal developer-line release metadata
- the current evidence is still one real X11 plus `i3` host plus simulated or temp-HOME scenarios
- lower-level surfaced JSON still leaks prompt-era implementation metadata

## Current Branch Position

- continue limited public technical beta: yes
- broader beta stabilization: no
- next step: one short remediation cycle plus wider real-host evidence before any broader-beta discussion
