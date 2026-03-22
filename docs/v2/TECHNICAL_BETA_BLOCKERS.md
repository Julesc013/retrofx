# RetroFX 2.x Technical Beta Blockers

This document records blocker classification from the rapid technical-beta execution pass on the merged `main` branch on 2026-03-22.

It is evidence-backed by [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md) and [CURRENT_EXECUTION_BASELINE.md](CURRENT_EXECUTION_BASELINE.md).

## Technical-Beta-Blocker

None open for continued limited technical-beta circulation.

The rapid execution pass did not uncover a failure that makes the current limited technical-beta wrapper unsafe or misleading enough to stop circulation for advanced outside testers.

## Broader-Beta-Blocker

### 1. Fallback install evidence still reports the internal developer line

- Severity: `broader-beta-blocker`
- Category: `install-bundle`
- Evidence: `commands/techbeta_install_bundle.out` in the rapid execution report records `release_status.version=2.0.0-alpha.internal.2`, `status_label=internal-alpha`, and `distribution_scope=internal-non-public`
- Why it matters: broader beta stabilization cannot proceed while an outside-facing wrapper still produces install metadata that looks like the internal developer line

### 2. Real-host breadth is still too narrow

- Severity: `broader-beta-blocker`
- Category: `environment-specific`
- Evidence: the executed matrix still relies on one real X11 plus `i3` host plus simulated Wayland or temp-HOME scenarios
- Why it matters: broader beta stabilization needs more than one real host and more than one operator-style execution pass

## High

### 3. Surfaced JSON still leaks historical prompt-era implementation IDs

- Severity: `high`
- Category: `docs-dev-surface`
- Evidence: `techbeta_apply_x11.out`, `techbeta_plan_modern.out`, and `techbeta_install_bundle.out` still advertise `TWO-19`, `TWO-18`, and `TWO-16` in subsystem `implementation.prompt` fields
- Why it matters: the branch-level truth now says `TWO-33`, but lower-level surfaced JSON still makes the execution history harder to trust quickly

### 4. There is still no real outside tester evidence corpus

- Severity: `high`
- Category: `diagnostics-reporting`
- Evidence: this rapid pass was still run by one operator on the merged `main` branch, not by multiple outside advanced testers
- Why it matters: technical-beta continuation is still acceptable, but broader beta stabilization should not be declared before outside-style reports exist

## Medium

### 5. Wayland remains degraded or export-only

- Severity: `medium`
- Category: `environment-specific`
- Evidence: the executed Wayland scenario passed only as `degraded-pass`; live ownership remained out of scope and X11-oriented runtime pieces stayed degraded
- Why it matters: this is acceptable for the current technical-beta matrix, but it remains a real limitation for any broader next stage

### 6. Migration inspection and explicit X11 preview remain internal-only evidence

- Severity: `medium`
- Category: `migration-compatibility`
- Evidence: migration inspection and `preview-x11` were exercised only through the internal developer surface
- Why it matters: these remain useful for maintainers, but they are still not part of the technical-beta promise to outside advanced testers

## Low

### 7. Fresh candidate packaging was blocked on the in-flight working tree

- Severity: `low`
- Category: `package-bundle`
- Evidence: `package_technical_beta.out` reported `dirty-working-tree`
- Why it matters: this was an honest clean-tree gate rather than a crash, but broader-beta packaging readiness should still be rechecked from a clean committed state

## Current Result

For the rapid `main`-branch execution pass:

- `READY_FOR_LIMITED_TECHNICAL_BETA_CONTINUATION=yes`
- `READY_FOR_BROADER_BETA_STABILIZATION=no`
- `NEEDS_FAST_REMEDIATION_CYCLE_FIRST=yes`

Recommended next step:

1. fix the technical-beta install metadata leak
2. normalize the stale subsystem prompt-era metadata that is still exposed to operators
3. re-run clean-tree package generation
4. expand validation beyond the current single-host, single-operator pass before revisiting broader beta stabilization
