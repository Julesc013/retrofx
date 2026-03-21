# RetroFX 2.x Broader Alpha Readiness

This document answers the broader-alpha question for the current 2.x branch after the TWO-28 hardening pass.

It is not a public release note.
It is not a promise that 2.x is ready for public alpha, beta, or production use.

## Verdict

READY_FOR_INTERNAL_ALPHA_CONTINUATION=yes

READY_FOR_BROADER_ALPHA=no

READY_FOR_CONTROLLED_EXTERNAL_ALPHA=no

READY_FOR_PRE_BETA_STABILIZATION=no

## Why

Internal alpha continuation remains acceptable because:

- the unified dev surface is coherent across resolve, plan, compile, bundle, install, uninstall, apply, off, diagnostics, and status
- bounded apply or off remains trustworthy inside isolated 2.x-owned roots
- internal-alpha package generation, install, uninstall, and diagnostics capture are reproducible
- the current branch state is now explicit about which environments are export-oriented only

Broader alpha is still not ready because:

- validation still depends too heavily on one real X11 plus `i3` host
- there is still no real Wayland-host validation pass for the currently declared surface
- non-sway Wayland desktops are still export-oriented validation environments, not trusted live-preview environments
- migration validation remains representative rather than broad

Controlled external alpha is not ready because:

- the current package shape still assumes a repo checkout
- the implemented surface still requires internal context to interpret correctly
- the branch still needs another hardening pass before external technically literate testers would get consistent signal

Pre-beta stabilization is not ready because:

- broader-alpha evidence is not yet strong enough
- cross-environment confidence is still too narrow
- the branch still needs another validation-driven hardening cycle rather than a pre-beta freeze posture

## Practical Reading

For TWO-28, the correct interpretation is:

- internal alpha only: yes
- local or internal alpha candidate: yes
- broader non-public alpha: no
- pre-beta hardening next: no

The immediate next step is another focused hardening cycle around real Wayland-host evidence, additional real-host validation, and broader migration-corpus review.
