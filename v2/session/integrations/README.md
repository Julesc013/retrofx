# v2/session/integrations

Purpose:

- future home of bounded login and startup integration helpers

What belongs here:

- TTY, `tuigreet`, Xsession, WM, and DE startup integration planning helpers
- managed wrapper and launch-helper preparation
- integration-manifest helpers

What does not belong here:

- target file emission
- raw login-manager takeover logic
- unsupported global desktop ownership

Governing docs:

- `docs/v2/SESSION_INTEGRATIONS.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Later prompts should implement:

- explicit integration helpers that remain capability-aware, user-local by default, and separate from target emission
