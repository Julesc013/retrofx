# RetroFX 2.x Alpha Blockers

This document lists the remaining blockers for calling the current branch "controlled alpha-ready."

It is not a future wish list.
It is a concrete blocker list derived from [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md).

## Alpha-Blocker

### 1. Explicit live X11 probe is still not manually validated on a safe real session

- Severity: `alpha-blocker`
- Evidence: [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md) marks the explicit live X11 `picom` probe as `not-tested`
- Why it blocks alpha: the branch now claims a bounded experimental X11 preview or apply surface, so controlled alpha should include at least one manual validation run of that explicit live probe on a suitable disposable or trusted X11 session
- What is already validated: non-destructive X11 artifact generation, preview-state generation, and simulated probe logic through automated tests
- What still needs to happen: run and document one real explicit probe on a safe X11 host, then confirm cleanup and user-visible limits

## High

### 2. Delegated unified-help output still leaks underlying module names

- Severity: `high`
- Evidence: `scripts/dev/retrofx-v2 resolve --help` and `scripts/dev/retrofx-v2 bundle --help` still print usage headers beginning with `cli.py`
- Why it matters: this makes the consolidated surface feel less trustworthy and more like a thin wrapper than a coherent experimental platform
- Recommended next step: set explicit `prog` values on delegated CLI modules or normalize delegated help output through the unified dispatcher

### 3. Validation is still single-host plus simulated-environment heavy

- Severity: `high`
- Evidence: Wayland and TTY validation in TWO-22 used environment simulation rather than a second real host session; the live X11 probe was not run manually
- Why it matters: the branch has enough evidence for internal experimental use, but not enough for a broader controlled alpha cohort
- Recommended next step: validate the current matrix on at least one additional real environment, ideally one real Wayland session for planning and apply-staging review plus one safe X11 host for the explicit probe

## Medium

### 4. Legacy migration validation is still representative rather than broad

- Severity: `medium`
- Evidence: TWO-22 exercised a real 1.x profile and the automated suite covers several more, but there is still no wider curated migration corpus review
- Why it matters: migration remains explicitly dev-only, but confidence in the diagnostics is still narrower than alpha-grade tooling should have
- Recommended next step: expand the validated legacy profile corpus and record the outcomes in the validation matrix

## Low

### 5. Controlled-alpha positioning still depends on careful operator reading

- Severity: `low`
- Evidence: the docs are now much more truthful, but the branch still has many experimental surfaces with different maturity levels
- Why it matters: internal testers can work with this, but broader alpha participants would benefit from even tighter “safe to try” versus “observe only” labeling
- Recommended next step: tighten readme and status-report wording once the X11 probe and environment-coverage blockers are addressed

## Not Blockers

These are intentionally incomplete but do not block controlled alpha on their own because the branch already documents them honestly:

- live Wayland render
- global desktop integration
- full 1.x runtime compatibility mode
- public packaging or distro integration

Those remain planned future scope, not regressions against the current branch promise.
