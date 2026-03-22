# RetroFX 2.x Technical Beta Blockers

This document records blocker classification from the real limited technical-beta execution pass on the merged `main` branch on 2026-03-22.

It is evidence-backed by [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md), [CURRENT_EXECUTION_BASELINE.md](CURRENT_EXECUTION_BASELINE.md), and the captured report root:

- `v2/releases/reports/technical-beta-main-20260322-094027Z`

## Technical-Beta-Blocker

None open for continued limited technical-beta circulation.

The real copied-toolchain run on `main` did not uncover a failure that makes the current limited technical-beta surface unsafe or misleading enough to stop advanced-tester circulation.

## Broader-Beta-Blocker

### 1. Real-host validation breadth is still too narrow

- Severity: `broader-beta-blocker`
- Category: `environment-specific`
- Evidence: the current matrix is still one real X11 plus `i3` host plus simulated Wayland and temp-HOME scenarios
- Why it matters: broader beta stabilization needs more than one real host and more than one operator-style execution pass

### 2. There is still no real outside tester evidence corpus

- Severity: `broader-beta-blocker`
- Category: `diagnostics-reporting`
- Evidence: both current technical-beta execution passes were maintainer-run on `main`; no captured outside-tester reports exist yet
- Why it matters: broader beta stabilization should be based on real incoming reports, not only maintainer self-validation

## High

### 3. Surfaced subsystem JSON still leaks historical prompt-era implementation IDs

- Severity: `high`
- Category: `docs-dev-surface`
- Evidence:
  - `commands/techbeta_apply_x11.out` still reports `implementation.prompt=TWO-19`
  - `commands/techbeta_wayland_plan.out` still reports `implementation.prompt=TWO-18`
  - `commands/dev_preview_x11.out` still reports `implementation.prompt=TWO-17`
  - `commands/dev_migrate_inspect.out` still reports `implementation.prompt=TWO-15`
- Why it matters: branch-level status now reports the current execution prompt correctly, but lower-level surfaced JSON still makes the execution history harder to trust quickly

## Medium

### 4. Wayland remains degraded or export-only

- Severity: `medium`
- Category: `environment-specific`
- Evidence: the executed Wayland scenario passed only as `degraded-pass`; live ownership remained out of scope and X11 runtime pieces stayed degraded
- Why it matters: this is acceptable for the current technical-beta matrix, but it still blocks a broader next-stage promise

### 5. Migration inspection and explicit X11 preview remain internal-only evidence

- Severity: `medium`
- Category: `migration-compatibility`
- Evidence: migration inspection and `preview-x11` were exercised only through the internal developer surface
- Why it matters: these remain useful maintainer checks, but they are still not part of the limited technical-beta promise

## Resolved In This Pass

- clean-tree `package-technical-beta` generation succeeded on current `main`
- the packaged install flow now reports `technical-beta` metadata instead of leaking the internal developer line
- packaged diagnostics and uninstall remained bounded and supportable

## Current Result

For the current `main`-branch technical-beta line:

- `READY_FOR_LIMITED_TECHNICAL_BETA_CONTINUATION=yes`
- `READY_FOR_BROADER_BETA_STABILIZATION=no`
- `NEEDS_ANOTHER_FAST_REMEDIATION_CYCLE=no`

Recommended next step:

1. continue the limited technical beta on `main`
2. collect real outside-tester reports using the current package, runbook, and diagnostics flow
3. add at least one more real-host execution pass before revisiting broader beta stabilization
4. normalize the stale subsystem prompt-era metadata as a follow-up hardening task, not as a gate for continued limited technical beta
