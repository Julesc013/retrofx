# RetroFX 2.x Pre-Beta Readiness

This document answers the pre-beta question for the current 2.x branch after the TWO-32 technical-beta candidate pass.

It is not a public release note.
It does not imply public beta, stable release, or replacement of 1.x.

Decision date: 2026-03-22

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
- the branch now takes a narrower limited technical-beta route instead of reviving the blocked non-public pre-beta path
- the reserved pre-beta candidate version `2.0.0-prebeta.internal.1` is still only a blocked future candidate identity rather than an approved branch state

## Why Internal Hardening Should Continue

More internal hardening is still the correct next step because:

- the branch is already deterministic and truthful enough for continued internal-alpha work
- the unified dev surface is coherent and the package flow is now stricter about dirty-tree generation
- version, tag, and candidate state are now reported more truthfully for the current build
- public-surface docs now define a limited technical-beta candidate explicitly rather than leaving it as a vague future idea
- the remaining blockers for pre-beta are mostly about broader environment breadth rather than missing subsystems

## Tester Audience At This Stage

The broader internal developer audience remains:

- core contributors
- technically literate internal testers with repo access
- operators comfortable with temp-HOME validation, machine-readable manifests, and export-only caveats

The branch is not yet suitable for a wider non-public pre-beta cohort even though a narrower limited technical-beta candidate now exists.
