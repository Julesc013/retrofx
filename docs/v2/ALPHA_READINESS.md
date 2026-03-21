# RetroFX 2.x Alpha Readiness

This document records the TWO-22 readiness decision for the current 2.x branch.

Decision date: 2026-03-21

## Verdict

READY_FOR_INTERNAL_USE=yes

READY_FOR_CONTROLLED_ALPHA=no

READY_FOR_BROADER_TESTING=no

NEEDS_MORE_STABILIZATION=yes

## Why

The branch is ready for internal experimental use because:

- the unified dev surface works across resolve, plan, compile, migration, bundle, install, apply, off, and status flows
- the validation matrix shows broad `pass` coverage across the implemented feature set
- non-X11 environments degrade honestly instead of pretending unsupported live behavior exists
- bounded apply or off and install or uninstall flows behave correctly inside isolated temp homes
- the full 2.x test suite is green

The branch is not yet ready for a controlled alpha because:

- the explicit live X11 probe was not manually exercised in TWO-22
- validation remains too dependent on a single host plus simulated environments
- delegated help still has enough ambiguity to weaken operator trust

## Recommended Next Step

The correct next phase is:

1. Keep the branch available for internal experimental use only.
2. Close the blockers in [ALPHA_BLOCKERS.md](ALPHA_BLOCKERS.md).
3. Re-run [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) on at least one more real environment.
4. Reassess controlled-alpha readiness only after the live X11 probe and dev-surface clarity issues are addressed.

## What This Is Not

This is not a public release claim.
It is not a statement that 2.x should replace 1.x.
It is a branch-health decision based on the currently implemented and validated experimental surface.
