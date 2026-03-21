# scripts/dev

Purpose:

- home of experimental helper wrappers for the 2.x dev bundle, install, and bounded apply flow

Implemented now:

- `retrofx-v2`: unified experimental 2.x developer surface for status, resolve, plan, compile, packs, migration, install, package, diagnostics, apply, off, and smoke flows
- `retrofx-v2-bundle`: build a deterministic 2.x dev bundle from a profile or pack profile
- `retrofx-v2-package-alpha`: build a reproducible non-public internal-alpha package around one deterministic 2.x bundle plus bundled runbook docs
- `retrofx-v2-capture-diagnostics`: collect a local diagnostics directory for controlled internal alpha evidence and triage
- `retrofx-v2-install`: install one generated bundle into the isolated user-local `retrofx-v2-dev` footprint
- `retrofx-v2-apply`: stage and activate a bounded 2.x experimental profile in the managed current-state area
- `retrofx-v2-off`: clear the bounded 2.x experimental current activation without touching 1.x or uninstalling bundles
- `retrofx-v2-preview-x11`: stage bounded X11 render artifacts and optionally run an explicit short-lived picom probe
- `retrofx-v2-status`: inspect the current 2.x experimental activation plus the user-local install footprint
- `retrofx-v2-uninstall`: remove one installed experimental bundle safely

What does not belong here:

- replacements for `scripts/retrofx`
- 1.x install or runtime behavior
- hidden production aliases for the experimental 2.x scaffold

Current rule:

- these wrappers are dev-only and user-local
- they must not touch 1.x install paths such as `~/.config/retrofx` or `~/.local/bin/retrofx`
