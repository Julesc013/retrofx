# RetroFX 2.x Controlled Internal Alpha Plan

This document defines the first real controlled internal alpha program for the 2.x branch.

It is not a public release plan.
It is not a feature roadmap.
It is an evidence-gathering plan for a narrow internal tester cohort.

## Goals

The controlled internal alpha exists to:

- validate the load, validate, normalize, and resolve pipeline under real host conditions
- validate target compiler outputs for terminal, WM, toolkit, and bounded X11 render families
- validate bounded apply or off safety inside 2.x-owned roots
- validate repo-local bundle, internal-alpha package, install, and uninstall behavior
- discover environment mismatches that were not visible in simulated validation
- verify that docs, the unified dev surface, and diagnostics capture are sufficient for internal testers

## Scope

Environments to test:

- one or more real X11 hosts
- at least one real Wayland host when available
- temp HOME or isolated XDG-root runs for install and apply paths
- repo-local dev mode on a clean checkout

Profile families to test:

- one retro or CRT-style profile
- one modern or minimal profile
- one pack-aware profile
- one representative 1.x profile through migration inspection

Flows to test:

- `status`, `resolve`, `plan`, and `compile`
- WM plus terminal artifact generation
- toolkit export inspection
- bounded `apply` or `off`
- bundle, package, install, uninstall
- diagnostics capture
- X11 render preview and bounded explicit probe where the host supports it

Out of scope:

- live Wayland render ownership
- global GNOME, Plasma, or Xfce mutation
- public release packaging
- replacement of the 1.x runtime
- network-backed issue collection or telemetry

## Required Tester Scenarios

Every internal alpha tester should perform at least:

1. resolve, plan, and compile one retro profile
2. compile WM plus terminal outputs
3. inspect toolkit exports for one modern profile
4. run bounded `apply` and `off` in a temp HOME or isolated XDG roots
5. run bundle or internal-alpha package install or uninstall in a temp HOME
6. run `migrate inspect-1x` on at least one real 1.x profile
7. run `diagnostics` after at least one test pass
8. run `preview-x11` on an X11 host if supported

## Success Criteria

The alpha is succeeding when:

- testers can complete the required scenarios without touching 1.x paths
- reported failures are reproducible from commands plus captured diagnostics
- non-X11 environments degrade honestly rather than stumbling into fake live behavior
- bundle or install or uninstall ownership remains explicit and reversible
- the unified dev surface is sufficient for testers without code spelunking

## Failure Criteria

The alpha is failing if any of the following appear:

- 2.x writes outside its managed roots during apply, off, install, or uninstall
- current-state or install-state manifests lie about what happened
- a documented implemented command is not actually usable by internal testers
- diagnostics capture is insufficient to reproduce a reported issue
- real-host failures contradict the current readiness and limitation docs in material ways

## Status Labels During Alpha

Use these outcomes for test scenarios:

- `pass`
- `degraded-pass`
- `partial`
- `fail`
- `blocked`
- `not-tested`

Use the severity rules in [ALPHA_TRIAGE.md](ALPHA_TRIAGE.md) for issue handling.

## Expected Deliverables From Testers

Each tester should provide:

- one completed [ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md](ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md)
- one or more [ALPHA_FEEDBACK_TEMPLATE.md](ALPHA_FEEDBACK_TEMPLATE.md) entries
- one [ALPHA_ISSUE_TEMPLATE.md](ALPHA_ISSUE_TEMPLATE.md) entry per concrete issue
- one diagnostics directory from `scripts/dev/retrofx-v2 diagnostics`

## Exit Condition For This Alpha Round

This round is complete when:

- the required scenarios have been executed across the planned host set
- all `alpha-blocker` findings are either fixed or explicitly fenced off
- the branch decision is updated using [POST_ALPHA_DECISION_RULES.md](POST_ALPHA_DECISION_RULES.md)
