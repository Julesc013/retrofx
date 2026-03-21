# RetroFX 2.x Broader Alpha Readiness

This document answers the broader-alpha question for the current 2.x branch after the TWO-32 technical-beta candidate pass.

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
- the current branch is an untagged post-alpha hardening build rather than a broader-alpha candidate line

Controlled external alpha is not ready on the broader developer surface because:

- the broader `retrofx-v2` developer surface still assumes internal context
- the approved external surface is now the narrower copied-toolchain `retrofx-v2-techbeta` candidate instead
- broader-alpha still implies more environment breadth than the current technical-beta support matrix provides

Pre-beta stabilization is not ready because:

- broader-alpha evidence is not yet strong enough
- cross-environment confidence is still too narrow
- the branch still needs another validation-driven hardening cycle rather than a pre-beta freeze posture

## Practical Reading

For TWO-32, the correct interpretation is:

- internal alpha only: yes
- current branch version: `2.0.0-alpha.internal.2`
- proposed pre-beta candidate version: `2.0.0-prebeta.internal.1`
- approved technical-beta candidate version: `2.0.0-techbeta.1`
- latest historical local alpha candidate: `v2.0.0-alpha.internal.1`
- broader non-public alpha: no
- limited public technical beta: yes, on the narrower copied-toolchain surface only
- more internal hardening next: no, but broader-alpha gates remain intentionally unsatisfied

The immediate next step is limited technical-beta circulation on the narrowed support matrix, not revival of the broader-alpha track.
