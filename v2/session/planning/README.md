# v2/session/planning

Purpose:

- home of non-destructive capability-aware session planning for the experimental 2.x scaffold

Implemented now:

- environment-aware plan builders that classify requested targets into export, degraded, apply-preview, and skipped buckets
- preview-oriented plan summaries that bridge the resolved profile and implemented target compilers

What belongs here:

- capability-aware session plan generation
- family and target classification helpers
- preview-only lifecycle reasoning that stops short of side effects

What does not belong here:

- live apply or install execution
- raw target artifact rendering
- environment-fact collection itself

Governing docs:

- `docs/v2/SESSION_SYSTEM.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/CAPABILITY_MODEL.md`

Current rule:

- TWO-11 planning is dev-only and non-destructive
- the planner may write preview reports under `v2/out/<profile-id>/plan/`, but it must not mutate the live session
