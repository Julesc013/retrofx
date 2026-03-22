# RetroFX 2.x Technical Beta Readiness

This document records the readiness decision after the real `main`-branch technical-beta execution pass on 2026-03-22.

It is based on [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md), [TECHNICAL_BETA_BLOCKERS.md](TECHNICAL_BETA_BLOCKERS.md), and [BROADER_BETA_STABILIZATION_READINESS.md](BROADER_BETA_STABILIZATION_READINESS.md).

## Verdict

READY_FOR_LIMITED_TECHNICAL_BETA_CONTINUATION=yes

READY_FOR_BROADER_BETA_STABILIZATION=no

NEEDS_ANOTHER_TECHNICAL_BETA_REMEDIATION_CYCLE=no

## What “Limited Technical Beta” Means Here

For RetroFX 2.x on the current `main` branch, the limited technical beta means:

- advanced testers can use the copied-toolchain `retrofx-v2-techbeta` surface
- workflows remain user-local, reversible, and bounded
- supported, degraded, and unsupported environments are explicit
- diagnostics capture is sufficient for structured bug reports

It does not mean:

- general-public beta
- stable or production readiness
- live Wayland ownership
- broad migration guarantees
- replacement of `1.x`

## Why Continuation Is Approved

- the real copied-toolchain execution pass completed without a technical-beta-blocker
- clean-tree package generation now succeeds on current `main`
- bundled install, diagnostics, and uninstall remain bounded and now preserve technical-beta release metadata end to end
- bounded X11 `apply` and `off` remained within 2.x-owned roots
- degraded Wayland behavior stayed honest instead of pretending to be supported live runtime

## Why Broader Beta Stabilization Is Still Blocked

- the current evidence base is still one operator on one real X11 plus `i3` host
- there is still no outside-tester report corpus
- some lower-level JSON still leaks historical prompt-era metadata

## Why Another Fast Remediation Cycle Is Not Required First

- the previously reported clean-tree package and install metadata problems are no longer open
- the remaining blockers are mostly evidence-breadth and clarity issues rather than immediate correctness failures
- the right next step is continued limited technical beta with real incoming reports, not another forced fast remediation loop before circulation continues

## Recommended Next Step

Continue the limited technical beta on `main`, collect real outside-style diagnostics-backed reports on at least one additional real host, and revisit broader beta stabilization after the evidence corpus is no longer single-operator and single-host narrow.
