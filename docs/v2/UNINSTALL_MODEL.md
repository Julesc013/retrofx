# RetroFX 2.x Uninstall Model

RetroFX 2.x uninstall must remain explicit and manifest-driven.
The first TWO-16 uninstall slice is narrow on purpose.

## Current Implementation Status

As of TWO-16, uninstall can remove:

- one installed dev bundle from the user-local `retrofx-v2-dev` data root
- its per-bundle install record
- the install index entry for that bundle

It does not:

- touch 1.x
- touch `/etc`
- remove user-owned profiles or packs under the reserved 2.x config root
- remove repo-local outputs under `v2/out/` or `v2/bundles/`

## Removal Scope

Current uninstall ownership is limited to:

- `~/.local/share/retrofx-v2-dev/bundles/<bundle-id>/`
- `~/.local/state/retrofx-v2-dev/installations/<bundle-id>.json`
- the corresponding entry in `~/.local/state/retrofx-v2-dev/install-state.json`

## Preserved Data

The first uninstall slice preserves:

- `~/.config/retrofx-v2-dev/profiles/`
- `~/.config/retrofx-v2-dev/packs/`
- any unmanaged files outside the explicit experimental 2.x footprint

This is the conservative choice.
It prevents accidental loss of user-authored 2.x material while the platform is still experimental.

## Current Cleanup Behavior

The current implementation:

- removes the owned bundle directory
- removes the owned per-bundle record
- rewrites the install index
- prunes now-empty managed subdirectories when safe

It does not attempt aggressive cleanup of the entire config root.

## Future Work

Future prompts may add:

- `--purge` style behavior for fully owned empty trees
- repair and self-check against install-state records
- standalone toolchain uninstall
- bundle upgrade/replacement logic

Those future steps must continue to respect the rule that uninstall removes only paths the install layer explicitly owns.
