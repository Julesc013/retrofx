# RetroFX 2.x Technical Beta Blockers

This document records blocker classification from the TWO-33 first-pass technical-beta execution cycle.

It is evidence-backed by [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md).

## Technical-Beta-Blocker

None open for continued limited technical-beta circulation.

The first-pass execution cycle did not uncover a workflow failure that makes the current copied-toolchain candidate unsafe or misleading for advanced outside testers.

## High

### 1. Real-host breadth is still narrow

- Severity: `high`
- Category: `environment-specific`
- Evidence: the executed matrix still depends on one real X11 plus `i3` host plus simulated Wayland or temp-HOME runs
- Why it matters: this does not block continued limited technical beta, but it still blocks any move toward broader beta stabilization

### 2. There is not yet a real outside tester evidence corpus

- Severity: `high`
- Category: `docs-dev-surface`
- Evidence: TWO-33 is the first-pass execution cycle run locally against the tagged candidate package
- Why it matters: the technical-beta process now exists, but broader beta stabilization should not be declared before real outside advanced-tester reports exist

## Medium

### 3. Wayland remains degraded or export-only

- Severity: `medium`
- Category: `environment-specific`
- Evidence: the executed Wayland scenario passed only as `degraded-pass`; X11 runtime pieces remained degraded and explicit
- Why it matters: this is acceptable for the current matrix, but it remains a real limitation for any broader next stage

### 4. Migration and explicit X11 preview remain supplementary internal evidence only

- Severity: `medium`
- Category: `migration-compatibility`
- Evidence: migration inspection and `preview-x11` were executed through the internal developer surface rather than the candidate wrapper
- Why it matters: they remain useful for maintainers, but they are not yet part of the outside-facing technical-beta promise

## Low

### 5. Toolkit exports remain advisory

- Severity: `low`
- Category: `toolkit-theme-export`
- Evidence: toolkit and desktop-style outputs compiled and inspected successfully, but the notes remain advisory-only
- Why it matters: this is documented correctly and does not block continued limited technical beta, but it still limits what feedback is meaningful

## Current Result

For TWO-33:

- `READY_FOR_LIMITED_TECHNICAL_BETA_CONTINUATION=yes`
- `READY_FOR_BROADER_BETA_STABILIZATION=no`
- `NEEDS_ANOTHER_TECHNICAL_BETA_REMEDIATION_CYCLE=no`

Recommended next step:

- continue the limited technical-beta line with the current candidate package
- collect real outside advanced-tester diagnostics bundles and feedback templates
- revisit broader beta stabilization only after that evidence grows beyond the current single-operator execution cycle
