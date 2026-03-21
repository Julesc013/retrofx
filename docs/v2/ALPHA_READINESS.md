# RetroFX 2.x Alpha Readiness

This document records the TWO-24 readiness decision for the current 2.x branch.

Decision date: 2026-03-21

## Verdict

READY_FOR_INTERNAL_USE=yes

READY_FOR_CONTROLLED_ALPHA=yes

READY_FOR_BROADER_TESTING=no

NEEDS_MORE_STABILIZATION=yes

## Why

The branch is ready for internal experimental use and for a narrow controlled internal alpha because:

- the unified dev surface works across resolve, plan, compile, migration, bundle, install, apply, off, and status flows
- the validation matrix now shows broad `pass` coverage across the implemented feature set
- non-X11 environments degrade honestly instead of pretending unsupported live behavior exists
- bounded apply or off and install or uninstall flows behave correctly inside isolated temp homes
- bounded apply or off and uninstall now enforce managed-root ownership during cleanup rather than trusting arbitrary recorded paths
- the explicit live X11 `picom` probe has now been manually exercised on one real X11 plus `i3` host as a bounded timeout-based success case
- the full 2.x test suite is green
- delegated help now reports the unified `retrofx-v2` surface coherently rather than leaking `cli.py`
- internal-alpha package generation, metadata, runbook, and notes now make controlled non-public circulation reproducible instead of ad hoc
- the internal-alpha package flow has now been exercised end to end through package generation, isolated install, unified status inspection, and uninstall cleanup

The branch is not yet ready for broader testing because:

- validation remains too dependent on a single real host plus simulated environments
- there is still no real Wayland-host validation pass
- migration validation remains representative rather than broad

## Recommended Next Step

The correct next phase is:

1. Start a narrow controlled internal alpha on known-good internal hosts, with explicit emphasis on X11 plus `i3` validation first.
2. Re-run [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) on at least one more real environment, especially a real Wayland session.
3. Expand the migration validation corpus before making compatibility claims beyond the current representative set.
4. Use [INTERNAL_ALPHA_RUNBOOK.md](INTERNAL_ALPHA_RUNBOOK.md) plus the `package-alpha` flow as the standard internal circulation path.
5. Reassess broader testing only after the multi-host evidence improves.

## What This Is Not

This is not a public release claim.
It is not a statement that 2.x should replace 1.x.
It is a branch-health decision based on the currently implemented and validated experimental surface.
