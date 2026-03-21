# RetroFX 2.x Pre-Beta Blockers

This document lists the issues that still block a non-public pre-beta candidate for the current 2.x branch.

Current branch identity:

- current experimental version: `2.0.0-alpha.internal.2`
- current build kind: untagged post-alpha hardening
- latest local alpha candidate tag: `v2.0.0-alpha.internal.1`

This is not a future wish list.
It is the current blocker set derived from [BROADER_ALPHA_MATRIX.md](BROADER_ALPHA_MATRIX.md), [VALIDATION_MATRIX.md](VALIDATION_MATRIX.md), the current unified status surface, and the green automated suite.

## Current Pre-Beta-Blocker Status

There are current `pre-beta-blocker` items.
The branch is not ready for a non-public pre-beta candidate.

Resolved in TWO-29:

- release-status metadata now separates the current `.2` build from the historical `.1` local alpha candidate instead of conflating them
- `package-alpha` now blocks dirty working trees by default unless `--allow-dirty` is used for explicit internal triage
- the unified status and package surfaces now report the current build as an untagged post-alpha hardening build rather than a current tagged candidate

## Pre-Beta-Blocker

### 1. Broader-alpha gates are still not satisfied

- Severity: `pre-beta-blocker`
- Evidence: [BROADER_ALPHA_READINESS.md](BROADER_ALPHA_READINESS.md) still says `READY_FOR_BROADER_ALPHA=no`
- Why it matters: a non-public pre-beta candidate is stricter than broader alpha, so pre-beta cannot proceed while broader-alpha gates are still failing
- Recommended next step: satisfy the broader-alpha gate first and re-run the broader matrix on more than the current one strong real host

### 2. There is still no real Wayland-host validation pass

- Severity: `pre-beta-blocker`
- Evidence: current validation still relies on one real X11 plus `i3` host and simulated or forced Wayland classification
- Why it matters: pre-beta requires stronger cross-environment evidence than the branch currently has
- Recommended next step: run the supported checklist on at least one real Wayland host and record the result in the matrices

## High

### 3. Migration validation breadth is still too narrow for pre-beta positioning

- Severity: `high`
- Evidence: migration validation is still representative rather than broad, and the current branch docs still describe it that way honestly
- Why it matters: pre-beta should not expand tester trust around migration while the validated corpus is still narrow
- Recommended next step: validate a larger curated 1.x profile corpus and update the matrices with actual outcomes

## Medium

### 4. Package, install, and diagnostics flows are still intentionally internal-only

- Severity: `medium`
- Evidence: the package flow remains repo-checkout dependent, and the docs still position it as internal-alpha only
- Why it matters: this does not block internal hardening, but it means the current release shape is still not a broader tester package contract
- Recommended next step: keep these flows internal-only until broader-alpha gates are satisfied and the candidate audience expands deliberately

### 5. The X11 explicit probe remains a narrow single-host trust surface

- Severity: `medium`
- Evidence: the bounded X11 `picom` probe has one real X11 plus `i3` validation path and remains explicitly internal-only
- Why it matters: this is fine for internal hardening, but it is too narrow to anchor a pre-beta claim
- Recommended next step: keep the probe internal-only and revalidate it on at least one additional real host before widening exposure

## Low

### 6. Toolkit exports remain advisory rather than owned desktop integrations

- Severity: `low`
- Evidence: toolkit targets compile deterministically, but the docs and status surfaces still classify them as advisory exports
- Why it matters: this does not block internal use, but it limits what a pre-beta tester should infer from those outputs
- Recommended next step: keep toolkit exports clearly labeled as advisory until live ownership exists or is explicitly declared out of scope
