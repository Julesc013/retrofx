# v2/session/recovery

Purpose:

- future home of current-state descriptors, manifests, rollback, repair, self-check, and explain helpers

What belongs here:

- current and last-good state record helpers
- manifest ownership helpers
- repair and rollback coordination
- dry-run or explain state inspection helpers

What does not belong here:

- target compilation
- semantic resolution
- direct environment detection beyond consuming environment facts

Governing docs:

- `docs/v2/STATE_AND_RECOVERY.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`
- `docs/v2/SESSION_SYSTEM.md`

Later prompts should implement:

- lifecycle integrity helpers that keep runtime state, install state, and degraded fallback records distinct
