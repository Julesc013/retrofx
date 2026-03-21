# RetroFX 2.x Alpha Readiness

This document records the TWO-28 readiness decision for the current 2.x branch.

Decision date: 2026-03-21

## Verdict

READY_FOR_INTERNAL_USE=yes

READY_FOR_INTERNAL_ALPHA_CONTINUATION=yes

READY_FOR_CONTROLLED_INTERNAL_ALPHA=yes

READY_FOR_CONTROLLED_ALPHA=no

READY_FOR_LOCAL_ALPHA_TAG_CANDIDATE=yes

ALPHA_CANDIDATE_READY=yes

READY_FOR_BROADER_ALPHA=no

READY_FOR_CONTROLLED_EXTERNAL_ALPHA=no

READY_FOR_PRE_BETA_STABILIZATION=no

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
- the branch now has a controlled-alpha plan, diagnostics capture workflow, and triage templates for disciplined internal evidence gathering
- TWO-26 diagnostics remediation now captures source-control state, installed bundle inventory, installed bundle manifest, and source package manifest evidence for a selected profile
- TWO-27 now aligns the candidate version, candidate docs, status surface, and package manifests around the same local/internal alpha-candidate identity
- TWO-27 now exposes the local candidate tag name directly in release-status metadata instead of leaving it implicit in prose
- the TWO-27 final local validation subset now passes across full-suite tests, unified help or status, representative resolve or plan or compile, bounded apply or off, repo-local package generation, temp-HOME install or diagnostics or uninstall, and an explicit bounded X11 preview probe
- there are no current `alpha-blocker` or `high` findings left open in the remediation backlog
- TWO-28 now explicitly fences non-sway Wayland desktop sessions as export-oriented validation environments instead of leaving broader-alpha interpretation ambiguous
- TWO-28 now narrows machine-readable release-status and package metadata so they no longer imply broader-alpha approval

The branch is not ready for broader alpha, controlled external alpha, or pre-beta stabilization because:

- validation remains too dependent on a single real host plus simulated environments
- there is still no real Wayland-host validation pass
- non-sway Wayland desktops remain export-oriented validation paths rather than trusted live-preview targets
- migration validation remains representative rather than broad
- the current package shape is still repo-checkout dependent and intentionally internal-only

## Recommended Next Step

The correct next phase is:

1. Treat the current branch as acceptable for local or internal alpha use only after the working tree is clean, [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md) passes, and the candidate version remains `2.0.0-alpha.internal.1`.
2. Continue the narrow controlled internal alpha on known-good internal hosts, with explicit emphasis on X11 plus `i3` validation first.
3. Use [BROADER_ALPHA_MATRIX.md](BROADER_ALPHA_MATRIX.md), [BROADER_ALPHA_READINESS.md](BROADER_ALPHA_READINESS.md), [PRE_BETA_GATES.md](PRE_BETA_GATES.md), and [NEXT_STAGE_VERDICT.md](NEXT_STAGE_VERDICT.md) as the gate set before any broader-alpha discussion.
4. Re-run the matrix on at least one real Wayland host and one additional real X11 host.
5. Expand the migration validation corpus before making compatibility claims beyond the current representative set.
6. Keep `scripts/dev/retrofx-v2 preview-x11` and `package-alpha` positioned as internal-only surfaces until the broader-alpha gates are satisfied.
7. Reassess broader testing only after the multi-host evidence improves.

## What This Is Not

This is not a public release claim.
It is not a statement that 2.x should replace 1.x.
It is a branch-health decision based on the currently implemented and validated experimental surface.
