# RetroFX 2.x Local Alpha Candidate Notes

This document defines the first local-only alpha-candidate position for the current 2.x branch.

It is not a public release note.
It is not a promise that 2.x should replace 1.x.

## Candidate Identity

- candidate version: `2.0.0-alpha.internal.1`
- readiness basis: TWO-26 post-alpha remediation
- circulation scope: local and internal only
- release path: repo-checkout-dependent internal-alpha package plus unified dev surface

## Why A Local Candidate Is Acceptable

- there are no current `alpha-blocker` items
- the recent high-severity diagnostics gaps were remediated in TWO-26
- bounded apply, install, uninstall, and diagnostics flows are covered by regression tests
- internal-alpha packaging remains reproducible and isolated from 1.x
- the current branch truth now explicitly records the residual risks instead of implying broader readiness

## What Remains Experimental But Acceptable

- real-host confidence is still strongest on one X11 plus `i3` host
- Wayland render remains export-only or degraded
- toolkit outputs remain advisory exports
- migration validation remains representative rather than broad
- the local alpha candidate still depends on a repo checkout rather than a copied standalone toolchain

## What This Candidate Is For

Use this local candidate to:

- freeze a known internal testing snapshot
- let a narrow internal cohort run the checklist without branch churn underneath them
- gather another round of diagnostics-backed evidence before any broader alpha decision

## What This Candidate Is Not For

Do not use this candidate to:

- publish a public alpha
- replace the 1.x runtime
- claim multi-host confidence that does not exist yet
- skip the diagnostics and feedback workflow
