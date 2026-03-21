# RetroFX 2.x Public Beta Blockers

This document lists the issues that still block a limited public technical beta.

It is separate from alpha and pre-beta blockers because the concern here is outside advanced-tester safety and support burden.

## Public-Beta-Blocker

### 1. No real Wayland-host validation pass exists yet

- Severity: `public-beta-blocker`
- Evidence: current validation still relies on one strong real X11 plus `i3` host and simulated or forced Wayland classification
- Why it matters: outside testers need a clearer environment matrix than the branch can honestly provide today

### 2. Package, install, and diagnostics flows remain repo-checkout dependent and internal-only

- Severity: `public-beta-blocker`
- Evidence: `package-alpha` still produces an internal-alpha package and the docs still frame install or diagnostics as repo-checkout-driven internal workflows
- Why it matters: this is too much hidden operator context for even a limited public technical beta

## High

### 3. Migration validation breadth is still too narrow

- Severity: `high`
- Evidence: migration docs and matrices still describe the validated corpus as representative rather than broad
- Why it matters: outside testers could over-trust migration reporting if this is not resolved first

### 4. The explicit X11 live probe remains a narrow single-host trust surface

- Severity: `high`
- Evidence: the bounded probe is real, but its real-host validation still centers on one X11 plus `i3` environment
- Why it matters: public technical beta should not make this look broader than it is

## Medium

### 5. Toolkit exports are deterministic but still advisory only

- Severity: `medium`
- Evidence: GTK, Qt, icon-cursor, and desktop-style outputs compile cleanly, but they do not provide live desktop ownership
- Why it matters: this is acceptable when documented, but it reduces what an outside tester can meaningfully validate

### 6. The unified dev surface still assumes high operator literacy

- Severity: `medium`
- Evidence: the branch is coherent, but it still expects familiarity with temp HOME, JSON output, and repo-local execution
- Why it matters: this is manageable internally, but it still raises the support burden for outside testers

## Current Result

For TWO-31:

- `READY_FOR_LIMITED_PUBLIC_TECHNICAL_BETA=no`
- current public surface position: internal-only
- recommended next step: another internal hardening cycle rather than outside circulation
