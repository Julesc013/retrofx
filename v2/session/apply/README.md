# v2/session/apply

Purpose:

- home of bounded experimental execution-mode sequencing and current-session side-effect orchestration

Implemented now:

- the TWO-19 bounded apply manager for staging a 2.x-owned active bundle under the isolated `retrofx-v2-dev` footprint
- a machine-readable current-state record and per-activation manifest writer
- a matching bounded `off` path that clears only 2.x-owned active state and preview-artifact roots
- status helpers that report the current activation alongside the separate install-state view

What belongs here:

- `compile-only`, `export-only`, `apply-now`, and install-mode orchestration helpers
- sequencing logic that promotes emitted artifacts into active or installed state
- lifecycle-result reporting helpers
- current-state, manifest, last-good, and event-log helpers for session-owned state

What does not belong here:

- raw profile parsing
- target file rendering
- semantic token derivation
- install-bundle ownership itself

Governing docs:

- `docs/v2/SESSION_SYSTEM.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Later prompts should implement:

- stronger repair and rollback flows driven by current-state plus last-good records
- broader live target activation once capability truth and cleanup contracts are mature
- install-default and integration-aware orchestration without weakening the 1.x safety boundary
