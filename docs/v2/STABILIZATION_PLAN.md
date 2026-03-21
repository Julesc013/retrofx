# RetroFX 2.x Stabilization Plan

TWO-20 is the handoff from architecture build-out to controlled stabilization.

The next phase should add fewer new feature families and spend more time on:

- interface hardening
- real-world testing under temp or isolated homes
- consistency across dev commands, manifests, and docs
- cleanup of overlapping experimental surfaces
- bounded runtime validation on the already-implemented X11 path

## Immediate Priorities

1. Harden the unified dev surface.
   The `scripts/dev/retrofx-v2` entrypoint should remain stable enough for repeated branch review and testing.

2. Expand branch-level validation.
   Focus on smoke paths, deterministic outputs, temp-HOME apply or off flows, and pack or migration review workflows.

3. Tighten current-state and install-state contracts.
   Manifest schemas, ownership boundaries, and cleanup semantics should stop drifting between prompts.

4. Run a documentation truth pass.
   The docs must keep distinguishing implemented, experimental, and planned behavior without optimism bias.

5. Validate the bounded X11 runtime path.
   Keep it explicit and dev-only, but make it more reliable and better documented before broader runtime ambitions.

## Things To Avoid In The Next Phase

- large new target families unless they unblock stabilization directly
- production CLI takeover
- hidden integration side effects
- premature public packaging claims
- over-refactoring working modules without a concrete stability payoff

## Candidate Internal Milestone

An appropriate next internal milestone is a branch-level `2.0.0-alpha-dev` review point with:

- the unified dev surface kept stable for a full test cycle
- the implemented-status matrix kept current
- reproducible smoke workflows
- no ambiguity about 1.x remaining the production line

That milestone would still be experimental.
It would mark branch coherence, not release readiness.
