# RetroFX Documentation Index

This index is the fastest way to navigate the repository without guessing which docs are current, historical, or product-line-specific.

RetroFX now lives on one branch, but it still contains two distinct tracks:

- `1.x`: the production line
- `2.x`: the experimental redesign line

If docs seem to disagree, use this priority order:

1. the current CLI or status surface for the line you are working on
2. the root [README](../README.md) and this file for repository-level truth
3. the current-truth docs for that line
4. historical gate or candidate docs as records, not as the latest state

The docs tree is intentionally split into:

- repository-level truth in [README](../README.md) and this index
- stable-line `1.x` product and operator docs under `docs/`
- experimental `2.x` current-truth docs under [`docs/v2/`](v2/README.md)
- historical gate records under `docs/v2/ALPHA_*`, `docs/v2/BROADER_ALPHA_*`, `docs/v2/PRE_BETA_*`, and `docs/v2/PUBLIC_BETA_*`

## Start Here

- [Repository README](../README.md): current repo-level status and the two-track model
- [Planning Handoff](PLANNING_HANDOFF_2026-03-22.md): the best single planning brief for both `1.x` and `2.x`

## 1.x Production Line

Use these when you need the stable product truth, operator guidance, or `1.0.x` maintenance rules.

- [1.x Product Truth](1x_PRODUCT.md)
- [1.x Maintenance](1x_MAINTENANCE.md)
- [Install Guide](INSTALL.md)
- [Quickstart](QUICKSTART.md)
- [Testing](TESTING.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Release Checklist](RELEASE_CHECKLIST.md)
- [Releasing](RELEASING.md)
- [Roadmap](ROADMAP.md)

## 2.x Current Truth

Use these first for the experimental platform as it exists today.

- [2.x Docs Index](v2/README.md)
- [2.x Implemented Status](v2/IMPLEMENTED_STATUS.md)
- [2.x Experimental Status](v2/EXPERIMENTAL_STATUS.md)
- [2.x Current Execution Baseline](v2/CURRENT_EXECUTION_BASELINE.md)
- [2.x Next Stage Verdict](v2/NEXT_STAGE_VERDICT.md)
- [2.x Technical Beta Readiness](v2/TECHNICAL_BETA_READINESS.md)
- [2.x Technical Beta Matrix](v2/TECHNICAL_BETA_MATRIX.md)
- [2.x Broader Beta Stabilization Readiness](v2/BROADER_BETA_STABILIZATION_READINESS.md)
- [2.x Relation To 1.x](v2/RELATION_TO_1X.md)
- [2.x Roadmap](v2/ROADMAP.md)

## 2.x Architecture And Contracts

Use these when working on design, implementation boundaries, compiler contracts, or model semantics.

- [2.x Product](v2/PRODUCT.md)
- [2.x Architecture](v2/ARCHITECTURE.md)
- [2.x Profile Schema](v2/PROFILE_SCHEMA.md)
- [2.x Resolved Model](v2/RESOLVED_MODEL.md)
- [2.x Capability Model](v2/CAPABILITY_MODEL.md)
- [2.x Target Compiler Contract](v2/TARGET_COMPILER_CONTRACT.md)
- [2.x Module Boundaries](v2/MODULE_BOUNDARIES.md)
- [2.x Implemented Interfaces](v2/IMPLEMENTED_INTERFACES.md)

## 2.x Operator And Tester Docs

Use these when exercising the bounded experimental workflows or the limited technical-beta package.

- [Internal Alpha Runbook](v2/INTERNAL_ALPHA_RUNBOOK.md)
- [Internal Alpha Notes](v2/INTERNAL_ALPHA_NOTES.md)
- [Technical Beta Notes](v2/TECHNICAL_BETA_NOTES.md)
- [Technical Beta Checklist](v2/TECHNICAL_BETA_CHECKLIST.md)
- [Technical Beta Candidate Notes](v2/TECHNICAL_BETA_CANDIDATE_NOTES.md)
- [Technical Beta Release Checklist](v2/TECHNICAL_BETA_RELEASE_CHECKLIST.md)
- [Technical Beta Execution Plan](v2/TECHNICAL_BETA_EXECUTION_PLAN.md)
- [Technical Beta Environment Report Template](v2/TECHNICAL_BETA_ENVIRONMENT_REPORT_TEMPLATE.md)
- [Technical Beta Feedback Template](v2/TECHNICAL_BETA_FEEDBACK_TEMPLATE.md)
- [Technical Beta Issue Template](v2/TECHNICAL_BETA_ISSUE_TEMPLATE.md)
- [Technical Beta Triage](v2/TECHNICAL_BETA_TRIAGE.md)

## Historical Gate Records

These docs are still useful, but they describe earlier gates, candidate decisions, and remediation cycles rather than the latest repo-wide truth.

- `docs/v2/ALPHA_*`
- `docs/v2/BROADER_ALPHA_*`
- `docs/v2/PRE_BETA_*`
- `docs/v2/PUBLIC_BETA_*`

Use them to understand why the branch looks the way it does, not as the first source of current state.
