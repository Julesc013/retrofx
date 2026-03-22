# RetroFX 2.x Docs

This directory holds the design, implementation, validation, and readiness docs for the experimental `2.x` line.

It does not describe the current `1.x` production runtime.
It also does not imply that `2.x` is ready to replace `1.x`.

## Current Repo Truth

As of the current `main` branch state:

- `1.x` remains the production line
- `2.x` remains experimental
- the broader internal developer surface still reports the internal developer-line identity `2.0.0-alpha.internal.2`
- the narrower outside-facing candidate identity is `2.0.0-techbeta.1`
- the broader `retrofx-v2` developer surface remains internal-only
- the latest local `v2.0.0-techbeta.1` tag is a candidate snapshot, not proof that the current `main` HEAD is identical to that tagged build
- limited technical beta continuation is approved
- broader beta stabilization is not approved
- one fast remediation cycle is now recommended before revisiting broader beta stabilization

If docs seem to conflict, trust these first:

1. [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md)
2. [EXPERIMENTAL_STATUS.md](EXPERIMENTAL_STATUS.md)
3. [TECHNICAL_BETA_READINESS.md](TECHNICAL_BETA_READINESS.md)
4. [NEXT_STAGE_VERDICT.md](NEXT_STAGE_VERDICT.md)

## Start Here

### For Current 2.x Truth

- [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md)
- [EXPERIMENTAL_STATUS.md](EXPERIMENTAL_STATUS.md)
- [CURRENT_EXECUTION_BASELINE.md](CURRENT_EXECUTION_BASELINE.md)
- [TECHNICAL_BETA_READINESS.md](TECHNICAL_BETA_READINESS.md)
- [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md)
- [BROADER_BETA_STABILIZATION_READINESS.md](BROADER_BETA_STABILIZATION_READINESS.md)
- [TECHNICAL_BETA_CANDIDATE_SUMMARY.md](TECHNICAL_BETA_CANDIDATE_SUMMARY.md)
- [PUBLIC_BETA_READINESS.md](PUBLIC_BETA_READINESS.md)
- [NEXT_STAGE_VERDICT.md](NEXT_STAGE_VERDICT.md)

### For Product And Architecture

- [PRODUCT.md](PRODUCT.md)
- [SCOPE.md](SCOPE.md)
- [NON_GOALS.md](NON_GOALS.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [PRINCIPLES.md](PRINCIPLES.md)
- [PROFILE_SCHEMA.md](PROFILE_SCHEMA.md)
- [RESOLVED_MODEL.md](RESOLVED_MODEL.md)
- [CAPABILITY_MODEL.md](CAPABILITY_MODEL.md)

### For Current Implementation Boundaries

- [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md)
- [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md)
- [TARGET_COMPILER_CONTRACT.md](TARGET_COMPILER_CONTRACT.md)
- [TARGET_FAMILIES.md](TARGET_FAMILIES.md)
- [SESSION_SYSTEM.md](SESSION_SYSTEM.md)
- [PACKS.md](PACKS.md)
- [MIGRATION.md](MIGRATION.md)

### For Operator And Tester Workflows

- [DEV_WORKFLOW.md](DEV_WORKFLOW.md)
- [INTERNAL_ALPHA_RUNBOOK.md](INTERNAL_ALPHA_RUNBOOK.md)
- [TECHNICAL_BETA_NOTES.md](TECHNICAL_BETA_NOTES.md)
- [TECHNICAL_BETA_CHECKLIST.md](TECHNICAL_BETA_CHECKLIST.md)
- [TECHNICAL_BETA_CANDIDATE_NOTES.md](TECHNICAL_BETA_CANDIDATE_NOTES.md)
- [TECHNICAL_BETA_CANDIDATE_SUMMARY.md](TECHNICAL_BETA_CANDIDATE_SUMMARY.md)
- [TECHNICAL_BETA_RELEASE_CHECKLIST.md](TECHNICAL_BETA_RELEASE_CHECKLIST.md)
- [TECHNICAL_BETA_EXECUTION_PLAN.md](TECHNICAL_BETA_EXECUTION_PLAN.md)
- [TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md](TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md)
- [TECHNICAL_BETA_FEEDBACK_TEMPLATE.md](TECHNICAL_BETA_FEEDBACK_TEMPLATE.md)
- [TECHNICAL_BETA_ISSUE_TEMPLATE.md](TECHNICAL_BETA_ISSUE_TEMPLATE.md)
- [TECHNICAL_BETA_TRIAGE.md](TECHNICAL_BETA_TRIAGE.md)
- [TECHNICAL_BETA_BLOCKERS.md](TECHNICAL_BETA_BLOCKERS.md)
- [PUBLIC_BETA_RISK_SURFACE.md](PUBLIC_BETA_RISK_SURFACE.md)
- [PUBLIC_BETA_GATES.md](PUBLIC_BETA_GATES.md)
- [PUBLIC_BETA_BLOCKERS.md](PUBLIC_BETA_BLOCKERS.md)

### For Planning

- [ROADMAP.md](ROADMAP.md)
- [RELATION_TO_1X.md](RELATION_TO_1X.md)
- [STABILIZATION_PLAN.md](STABILIZATION_PLAN.md)
- [STABILIZATION_CHECKLIST.md](STABILIZATION_CHECKLIST.md)
- [../PLANNING_HANDOFF_2026-03-22.md](../PLANNING_HANDOFF_2026-03-22.md)

## Current Implementation Summary

The `2.x` platform now has real implementation in these areas:

- load, validate, normalize, and resolve under `v2/core/`
- deterministic target compilation under `v2/targets/`
- environment detection and planning under `v2/session/planning/`
- bounded current-state apply/off under `v2/session/apply/`
- bundle/install/uninstall under `v2/session/install/`
- curated pack resolution under `v2/packs/`
- 1.x profile inspection and draft migration under `v2/compat/`
- release metadata, diagnostics capture, and package builders under `v2/dev/`

Implemented target families today:

- terminal/TUI: `xresources`, `alacritty`, `kitty`, `tmux`, `vim`
- WM: `i3`, `sway`, `waybar`
- toolkit/export: `fontconfig`, `gtk-export`, `qt-export`, `icon-cursor`, `desktop-style`
- X11/render-adjacent: `x11-display-policy`, `x11-shader`, `x11-picom`, `x11-render-runtime`

Still not implemented:

- global desktop ownership
- live Wayland render ownership
- full 1.x compatibility mode
- production CLI takeover

Current packaging and circulation truth:

- `package-alpha` remains the internal developer-line package flow
- `package-technical-beta` builds the narrower copied-toolchain package for advanced testers
- the rapid `main`-branch execution pass confirmed continued limited technical beta, but it also exposed one short remediation list before broader beta stabilization should be discussed again

## Surfaces You Should Not Confuse

### Internal Developer Surface

Entrypoint:

- `scripts/dev/retrofx-v2`

Use this for:

- implementation work
- broad status inspection
- migration inspection
- preview and packaging work
- internal-only workflows that are intentionally not part of the outside-facing promise

### Limited Technical-Beta Surface

Entrypoint:

- `scripts/dev/retrofx-v2-techbeta`

Use this for:

- the narrower advanced-tester flow
- copied-toolchain package validation
- the limited public technical-beta support matrix

It intentionally does not expose:

- `migrate inspect-1x`
- `preview-x11`
- the broader internal-only package surface

## Historical Gate Docs

This tree contains many alpha-, broader-alpha-, and pre-beta-stage docs.

They are still useful, but they are historical stage records, not the first source of current truth.

Use them to answer:

- how the branch got here
- why certain promises are fenced
- what blockers were already remediated

Do not use them first to answer:

- what `2.x` currently supports
- what the current outside-facing promise is
- what the next stage decision is

For those questions, use the current-truth docs listed at the top of this file.

## Practical Start

### If You Are Developing 2.x

1. `scripts/dev/retrofx-v2 status`
2. `scripts/dev/retrofx-v2 smoke v2/tests/fixtures/strict-green-crt.toml`
3. `scripts/dev/retrofx-v2 smoke --pack modern-minimal --profile-id warm-night`
4. `scripts/dev/retrofx-v2 diagnostics --pack modern-minimal --profile-id warm-night --label first-pass`

### If You Are Evaluating The Limited Technical Beta

1. `scripts/dev/retrofx-v2 package-technical-beta --pack modern-minimal --profile-id warm-night`
2. `<package-dir>/bin/retrofx-v2-techbeta status`
3. `<package-dir>/bin/retrofx-v2-techbeta smoke --pack modern-minimal --profile-id warm-night`
4. read [TECHNICAL_BETA_EXECUTION_PLAN.md](TECHNICAL_BETA_EXECUTION_PLAN.md) and [TECHNICAL_BETA_MATRIX.md](TECHNICAL_BETA_MATRIX.md)
