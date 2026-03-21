# v2/session/install

Purpose:

- future home of install-state ownership, default selection, and uninstall planning

What belongs here:

- user-local install ownership helpers
- install-manifest writers
- managed default-state logic
- uninstall and cleanup planning for install-owned assets

What does not belong here:

- current-session apply sequencing
- target config rendering
- unmanaged system-global takeover logic

Governing docs:

- `docs/v2/INSTALL_MODEL.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Later prompts should implement:

- reversible install ownership helpers that stay user-local and manifest-driven
