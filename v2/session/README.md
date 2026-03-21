# v2/session

Purpose:

- future home of apply, export, install, off, repair, environment detection, and session integration orchestration
- future home of side-effect ownership and lifecycle state management

Implemented now:

- environment detection under `environment/`
- capability-aware non-destructive planning under `planning/`
- explicit dev-only X11 preview staging under `dev/`
- no stable live apply, install, off, or recovery execution yet

Do implement here later:

- environment-scoped lifecycle logic
- login and session integration policy
- runtime ownership and recovery logic
- install-state ownership and uninstall planning
- state recording, last-good tracking, and explain or dry-run support

Planned sub-areas:

- `apply/`: execution-mode sequencing and side-effect orchestration
- `dev/`: explicit non-default preview helpers that exercise bounded runtime paths safely
- `environment/`: environment model and detection helpers
- `planning/`: capability-aware target/apply planning and preview reports
- `install/`: user-local install ownership and uninstall planning
- `recovery/`: state descriptors, manifests, rollback, repair, and self-check helpers
- `integrations/`: login/session hook planning for TTY, tuigreet, Xsession, WM, and DE entry points

Do not implement here:

- semantic token definitions
- raw target config rendering
- low-level shader logic
- target capability declaration logic

Governing docs:

- `docs/v2/SESSION_SYSTEM.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/ENVIRONMENT_MODEL.md`
- `docs/v2/INSTALL_MODEL.md`
- `docs/v2/STATE_AND_RECOVERY.md`
- `docs/v2/SESSION_INTEGRATIONS.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Core rule:

- session orchestration consumes the capability-filtered target plan and emitted artifacts, then decides what side effects are truthful in a specific environment
- session does not parse raw profiles or emit backend-specific target files directly
