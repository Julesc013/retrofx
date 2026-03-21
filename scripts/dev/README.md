# scripts/dev

Purpose:

- home of experimental helper wrappers for the 2.x dev bundle and install flow

Implemented now:

- `retrofx-v2-bundle`: build a deterministic 2.x dev bundle from a profile or pack profile
- `retrofx-v2-install`: install one generated bundle into the isolated user-local `retrofx-v2-dev` footprint
- `retrofx-v2-status`: inspect that experimental user-local footprint
- `retrofx-v2-uninstall`: remove one installed experimental bundle safely

What does not belong here:

- replacements for `scripts/retrofx`
- 1.x install or runtime behavior
- hidden production aliases for the experimental 2.x scaffold

Current rule:

- these wrappers are dev-only and user-local
- they must not touch 1.x install paths such as `~/.config/retrofx` or `~/.local/bin/retrofx`
