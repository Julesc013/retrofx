# RetroFX 2.x Alpha Triage

This document defines severity and category rules for the controlled internal alpha.

It is intentionally separate from 1.x.

## Severity Classes

### `alpha-blocker`

Meaning:

- blocks continued internal alpha on the affected flow
- requires immediate containment, fix, or explicit scope reduction
- must gain regression or contract coverage if fixed in code

Examples:

- cleanup outside 2.x-owned roots
- current-state or install-state manifest materially lies
- a documented implemented command is unusable in the supported alpha cohort

### `high`

Meaning:

- does not necessarily stop all alpha activity
- does block movement toward a broader alpha milestone
- usually requires a focused fix and regression coverage

Examples:

- diagnostics omit key reproduction data
- package or install flow works inconsistently across the narrow cohort
- X11 preview behavior contradicts current docs on a supported host

### `medium`

Meaning:

- does not block the current narrow alpha
- should be fixed or documented before expanding the tester set
- regression coverage is recommended when a code path changes

Examples:

- migration diagnostics are confusing but still honest
- status output is missing a useful summary field
- a template or checklist step is unclear

### `low`

Meaning:

- does not block internal alpha progression
- mainly polish, documentation, or ergonomics
- regression coverage is optional unless the issue is easy to lock down

Examples:

- wording drift in docs
- awkward help text
- minor inconsistencies in package summary text

## Category Classes

- `schema-model`
- `target-compiler`
- `session-apply-off`
- `install-bundle`
- `migration-compatibility`
- `docs-dev-surface`
- `environment-specific`
- `x11-experimental-render`
- `toolkit-theme-export`

## Decision Rules

| Severity | Blocks continued internal alpha | Blocks broader alpha | Requires immediate regression coverage if fixed |
| --- | --- | --- | --- |
| `alpha-blocker` | yes | yes | yes |
| `high` | usually no for unaffected flows, yes for affected flow | yes | yes |
| `medium` | no | often yes if it clusters | recommended |
| `low` | no | no | optional |

## Triage Questions

For each issue, answer:

1. Does it break a documented implemented workflow?
2. Does it cause side effects outside 2.x-owned roots?
3. Does it make captured evidence insufficient for reproduction?
4. Does it contradict current readiness or limitation docs?
5. Is it specific to one environment or systemic?

## Required Artifacts For Triage

Every issue should reference:

- environment report
- feedback entry
- diagnostics directory
- exact commands run
- severity and category

Use:

- [ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md](ALPHA_ENVIRONMENT_REPORT_TEMPLATE.md)
- [ALPHA_FEEDBACK_TEMPLATE.md](ALPHA_FEEDBACK_TEMPLATE.md)
- [ALPHA_ISSUE_TEMPLATE.md](ALPHA_ISSUE_TEMPLATE.md)
