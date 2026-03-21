# RetroFX 2.x Public Beta Readiness

This document answers the public-surface question for the current 2.x branch after the TWO-31 gating pass.

It is not a public release note.
It does not authorize publication.

Decision date: 2026-03-22

## Verdict

READY_FOR_LIMITED_PUBLIC_TECHNICAL_BETA=no

READY_FOR_CONTINUED_NON_PUBLIC_PRE_BETA=no

NEEDS_ANOTHER_HARDENING_CYCLE=yes

## What “Limited Public Technical Beta” Would Mean Here

For RetroFX 2.x, a limited public technical beta would mean:

- technically literate outside testers could use the documented workflows without source archaeology
- package, install, uninstall, diagnostics, and cleanup behavior are predictable enough for outside circulation
- degraded and unsupported environments are explicit enough to keep support burden manageable
- 1.x remains the production line and 2.x remains clearly experimental

It still would not mean:

- public general-user beta
- production readiness
- replacement of the 1.x runtime or CLI
- live Wayland render
- global desktop ownership

## Why The Answer Is Still No

- no real Wayland-host validation pass exists yet
- package, install, and diagnostics surfaces are still intentionally internal-only and repo-checkout dependent
- migration validation breadth is still too narrow
- the explicit X11 probe remains a narrow single-host surface

## Why Another Hardening Cycle Is Required

- the current branch is coherent enough for continued internal alpha work
- the public-facing docs can now be prepared safely without implying approval
- the remaining blockers are about external-surface trust and support burden, not missing core implementation

## Current Branch Position

- continue internal alpha: yes
- continue non-public pre-beta: no
- limited public technical beta: no
- next step: one more internal hardening cycle focused on real-host breadth and outside-tester support discipline
