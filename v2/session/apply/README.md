# v2/session/apply

Purpose:

- future home of execution-mode sequencing and current-session side-effect orchestration

What belongs here:

- `compile-only`, `export-only`, `apply-now`, and install-mode orchestration helpers
- sequencing logic that promotes emitted artifacts into active or installed state
- lifecycle-result reporting helpers

What does not belong here:

- raw profile parsing
- target file rendering
- semantic token derivation

Governing docs:

- `docs/v2/SESSION_SYSTEM.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Later prompts should implement:

- side-effect-aware execution helpers that consume target plans and artifact plans without inventing new planning truth
