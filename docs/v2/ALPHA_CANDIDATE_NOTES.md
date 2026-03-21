# RetroFX 2.x Local Alpha Candidate Notes

This document defines the first disciplined local or internal alpha-candidate position for the current 2.x branch.

It is not a public release note.
It is not a promise that 2.x should replace 1.x.

## Candidate Identity

- candidate version: `2.0.0-alpha.internal.1`
- status label: `internal-alpha`
- local tag candidate: `v2.0.0-alpha.internal.1`
- readiness basis: TWO-27 final local candidate gate
- circulation scope: local and internal only
- release path: repo-checkout-dependent internal-alpha package plus unified dev surface
- candidate approval: approved for local or internal-only circulation when [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md) passes on a clean committed tree
- broader-alpha approval: not approved

## Implemented In This Candidate

- load, validate, normalize, and resolve pipeline
- deterministic terminal, WM, toolkit, display-policy, and bounded X11 compiler families
- pack-aware profile resolution and curated built-in packs
- 1.x inspection plus draft migration output
- deterministic bundles, internal-alpha packages, and isolated `retrofx-v2-dev` install or uninstall flows
- bounded apply or off with explicit manifests, current-state tracking, and managed-root cleanup
- local diagnostics capture, runbook, alpha templates, and triage workflow

## Intentionally Experimental

- real-host confidence is still strongest on one X11 plus `i3` host
- bounded X11 `picom` probing remains an explicit opt-in developer action
- Wayland render remains export-only or degraded
- toolkit outputs remain advisory exports
- migration validation remains representative rather than broad
- the local alpha candidate still depends on a repo checkout rather than a copied standalone toolchain

## Supported And Validated Scenarios

- unified `status`, `resolve`, `plan`, `compile`, `bundle`, `package-alpha`, `install`, `uninstall`, `apply`, `off`, `diagnostics`, and `smoke` flows
- deterministic terminal and WM compile paths
- advisory toolkit export compilation
- bounded X11 preview compilation across passthrough, monochrome, and palette modes
- bounded apply or off in temp HOME or isolated XDG roots
- internal-alpha package generation plus isolated install or uninstall
- diagnostics capture with source-control and installed-bundle provenance

## Degraded Or Partial Areas

- Wayland and TTY remain planning plus export paths rather than live runtime ownership
- toolkit outputs are advisory and not live desktop integration
- migration is explicit inspection and draft generation, not runtime compatibility
- validation breadth is still narrow across real hosts

## Known Limitations

- broader testing is still not approved
- broader-alpha positioning remains blocked by missing real Wayland-host evidence and narrow multi-host coverage
- real Wayland-host validation is still absent
- public packaging and standalone copied-toolchain distribution do not exist
- 1.x remains the only production line

## Internal Tester Focus

Use this local candidate to:

- freeze a known internal testing snapshot
- let a narrow internal cohort run the checklist without branch churn underneath them
- gather another round of diagnostics-backed evidence before any broader alpha decision
- concentrate on state ownership, package/install behavior, real-host environment mismatches, and bounded apply or off trust

## Explicitly Out Of Scope

- public alpha or beta claims
- live Wayland render ownership
- global GNOME, Plasma, or Xfce settings mutation
- replacement of the 1.x runtime or CLI
- standalone copied-toolchain distribution

## Revert And Cleanup

- use `scripts/dev/retrofx-v2 off` to clear the bounded 2.x current activation
- use `scripts/dev/retrofx-v2 uninstall <bundle-id>` to remove installed bundles from `retrofx-v2-dev`
- prefer temp HOME or isolated XDG roots for candidate validation runs
- diagnostics capture is local-file based and does not clean state by itself

## Approval State

- candidate approved: `yes`, for local or internal-only circulation
- approval boundary: only after the checklist passes on a clean committed tree
- broader testing approval: `no`

## What This Candidate Is Not For

Do not use this candidate to:

- publish a public alpha
- replace the 1.x runtime
- claim multi-host confidence that does not exist yet
- skip the diagnostics and feedback workflow
