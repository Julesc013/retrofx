# v2/session/install

Purpose:

- home of experimental 2.x bundle install ownership, status reporting, and uninstall planning

Implemented now:

- deterministic dev bundle generation under `v2/bundles/`
- bundle manifests now carry explicit experimental release metadata for internal-alpha discipline
- isolated user-local install layout resolution for `retrofx-v2-dev`
- install-state record and index writers
- safe uninstall of owned experimental bundles
- JSON-facing install/status helpers used by `scripts/dev/retrofx-v2-*`

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
- `docs/v2/DISTRIBUTION_MODEL.md`
- `docs/v2/DEV_WORKFLOW.md`
- `docs/v2/UNINSTALL_MODEL.md`
- `docs/v2/APPLY_MODES.md`
- `docs/v2/SIDE_EFFECT_POLICY.md`

Later prompts should implement:

- standalone copied toolchain installs
- repair and upgrade flows driven by install-state metadata
- optional launcher/integration assets that remain isolated from 1.x
