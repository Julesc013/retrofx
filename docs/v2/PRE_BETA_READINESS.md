# RetroFX 2.x Pre-Beta Readiness

This document answers the pre-beta question for the current 2.x branch after the TWO-31 public-surface gating pass.

It is not a public release note.
It does not imply public beta, stable release, or replacement of 1.x.

Decision date: 2026-03-21

## Verdict

READY_FOR_NON_PUBLIC_PRE_BETA=no

READY_FOR_CONTINUED_BROADER_ALPHA=no

READY_FOR_LOCAL_PRE_BETA_TAG_CANDIDATE=no

PRE_BETA_CANDIDATE_READY=no

READY_FOR_MORE_INTERNAL_HARDENING=yes

## What "Non-Public Pre-Beta" Means Here

For RetroFX 2.x, a non-public pre-beta candidate would mean:

- technically literate non-public testers beyond the narrow core internal cohort
- deterministic resolve, plan, compile, package, install, uninstall, and diagnostics workflows
- trustworthy current-state, install-state, and manifest inspection
- explicit and stable support boundaries for degraded or export-only environments
- no current blocker that still depends on one strong host plus simulated environments only

It still would not mean:

- public beta
- production readiness
- replacement of the 1.x runtime or CLI
- live Wayland render
- global desktop ownership
- full 1.x runtime compatibility mode

## Why The Current Branch Is Not There Yet

The branch is not ready for a non-public pre-beta candidate because:

- broader-alpha gates are still not satisfied
- there is still no real Wayland-host validation pass
- migration validation is still representative rather than broad
- current package and diagnostics surfaces remain intentionally internal-alpha oriented
- the reserved pre-beta candidate version `2.0.0-prebeta.internal.1` is still only a blocked future candidate identity rather than an approved branch state

## Why Internal Hardening Should Continue

More internal hardening is still the correct next step because:

- the branch is already deterministic and truthful enough for continued internal-alpha work
- the unified dev surface is coherent and the package flow is now stricter about dirty-tree generation
- version, tag, and candidate state are now reported more truthfully for the current build
- public-surface docs now also make limited-public-technical-beta no explicit instead of leaving that as an implied next step
- the remaining blockers are mostly about validation breadth and release-surface trust, not missing subsystems

## Tester Audience At This Stage

The current audience remains:

- core contributors
- technically literate internal testers with repo access
- operators comfortable with temp-HOME validation, machine-readable manifests, and export-only caveats

The branch is not yet suitable for a wider non-public pre-beta cohort.
