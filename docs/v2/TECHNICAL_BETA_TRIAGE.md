# RetroFX 2.x Technical Beta Triage

This document defines the severity and category model for the limited technical-beta line.

It is stricter than the earlier alpha-only workflow because the audience now includes advanced outside testers.

## Severities

### `technical-beta-blocker`

- blocks continued limited technical-beta circulation
- blocks any movement toward broader beta stabilization
- requires immediate regression coverage or an explicit fence if fixed by narrowing

Examples:

- bounded apply or off behaves outside managed 2.x roots
- package or install workflow is not reversible
- help or status materially misstates supported environments
- diagnostics capture omits essential evidence for bug reports

### `high`

- does not necessarily block continued limited technical beta immediately
- does block movement toward broader beta stabilization until addressed or fenced
- should gain regression coverage in the next remediation pass

Examples:

- environment classification is too optimistic
- degraded/export-only paths are not reported clearly enough
- package metadata is correct but still confusing for outside advanced testers

### `medium`

- does not block continued limited technical beta
- may block broader beta stabilization if it accumulates or affects multiple workflows
- regression coverage is recommended when the issue is fixed

Examples:

- advisory toolkit exports need clearer notes
- migration evidence is still representative rather than broad
- diagnostics are usable but missing some convenience detail

### `low`

- does not block continued limited technical beta
- does not by itself block broader beta stabilization
- regression coverage is optional unless the issue touches a prior failure mode

Examples:

- small wording drift
- minor checklist or template mismatches
- cosmetic documentation inconsistencies

## Categories

- `schema-model`
- `target-compiler`
- `session-apply-off`
- `install-bundle`
- `migration-compatibility`
- `toolkit-theme-export`
- `x11-experimental-render`
- `diagnostics-reporting`
- `docs-dev-surface`
- `environment-specific`

## Current Triage Use

For TWO-33:

- use `technical-beta-blocker` only for issues that would make the limited technical-beta package unsafe or misleading for advanced outside testers
- use `high` for issues that still block broader beta stabilization even if the current limited technical-beta track can continue
- prefer documenting evidence-backed limitations over expanding scope
