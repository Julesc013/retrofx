# RetroFX 2.x Alpha Blockers

This document lists the remaining blockers and residual risks for calling the current branch "controlled alpha-ready."

It is not a future wish list.
It is a concrete blocker list derived from [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md).

## Current Alpha-Blocker Status

There are no current `alpha-blocker` items after TWO-23 remediation.

Resolved in TWO-23:

- the explicit bounded X11 `picom` probe was run manually on a real X11 plus `i3` host
- the unified delegated help surface now reports `retrofx-v2 ...` usage headers rather than leaking `cli.py`
- bounded apply or off and uninstall now refuse cleanup targets outside the managed 2.x roots, with regression coverage

## Medium

### 1. Validation is still narrow compared with broader testing needs

- Severity: `medium`
- Evidence: TWO-23 now includes one real X11 host validation run plus simulated Wayland and TTY flows, but still not a second real host or a real Wayland compositor session
- Why it matters: this no longer blocks a narrow internal alpha cohort, but it still blocks broader testing claims
- Recommended next step: run the validation matrix on at least one additional real environment, ideally one real Wayland session and one more X11 host

### 2. Legacy migration validation is still representative rather than broad

- Severity: `medium`
- Evidence: TWO-22 exercised a real 1.x profile and the automated suite covers several more, but there is still no wider curated migration corpus review
- Why it matters: migration remains explicitly dev-only, but confidence in the diagnostics is still narrower than alpha-grade tooling should have
- Recommended next step: expand the validated legacy profile corpus and record the outcomes in the validation matrix

## Low

### 3. Controlled-alpha positioning is now acceptable but still requires a narrow cohort definition

- Severity: `low`
- Evidence: TWO-23 makes the docs and status output more explicit, but the branch still has many experimental surfaces with different maturity levels
- Why it matters: internal testers can work with this, but anything beyond a small internal alpha cohort would benefit from even tighter “safe to try” versus “observe only” labeling
- Recommended next step: keep the internal alpha cohort narrow and continue simplifying readiness language as validation broadens

## Not Blockers

These are intentionally incomplete but do not block controlled alpha on their own because the branch already documents them honestly:

- live Wayland render
- global desktop integration
- full 1.x runtime compatibility mode
- public packaging or distro integration

Those remain planned future scope, not regressions against the current branch promise.
