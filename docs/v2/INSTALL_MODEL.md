# RetroFX 2.x Install Model

RetroFX 2.x now has its first real install slice, but it is still explicitly experimental.
Install in TWO-16 means:

- build a deterministic dev bundle from a resolved 2.x profile
- copy that bundle into a managed user-local 2.x footprint
- write install-state metadata so uninstall and status can be explicit

It does not mean:

- replacing the 1.x installer
- taking over the `retrofx` command
- mutating `/etc`
- enabling live session-default switching

## Current Implementation Status

As of TWO-21:

- repo-local dev mode is real and runs directly from the repository
- repo-local bundle generation is real under `v2/bundles/<bundle-id>/`
- experimental user-local install is real under isolated `retrofx-v2-dev` XDG roots
- uninstall and status are real for that experimental user-local footprint
- the bounded TWO-19 apply slice now reuses that same isolated footprint for `active/current`, manifests, last-good, preview-artifact roots, and event logs
- standalone copied toolchain installs, distro packages, and public release channels are still future work

## Concrete Modes

### Repo-Local Dev Mode

Characteristics:

- commands run from the repository checkout
- compiled artifacts remain under `v2/out/`
- bundles remain under `v2/bundles/`
- no user-local install is required

Current entrypoints:

- `scripts/dev/retrofx-v2 resolve`
- `scripts/dev/retrofx-v2 compile`
- `scripts/dev/retrofx-v2 plan`
- `scripts/dev/retrofx-v2 bundle`
- `scripts/dev/retrofx-v2 install`
- `scripts/dev/retrofx-v2 apply`
- `scripts/dev/retrofx-v2 off`
- `scripts/dev/retrofx-v2 status`
- `scripts/dev/retrofx-v2 uninstall`

### Installed Dev Mode

Characteristics in the first TWO-16 slice:

- uses a managed user-local 2.x footprint
- remains isolated from 1.x paths
- is still driven by repo-local experimental tooling
- owns copied bundles and install-state metadata only

Current roots:

| Purpose | Default path |
| --- | --- |
| config root | `~/.config/retrofx-v2-dev` |
| data root | `~/.local/share/retrofx-v2-dev` |
| state root | `~/.local/state/retrofx-v2-dev` |
| reserved launcher path | `~/.local/bin/retrofx-v2-dev` |

Current managed subpaths:

- `~/.local/share/retrofx-v2-dev/bundles/<bundle-id>/`
- `~/.local/share/retrofx-v2-dev/active/current/`
- `~/.local/share/retrofx-v2-dev/preview-artifacts/`
- `~/.local/state/retrofx-v2-dev/installations/<bundle-id>.json`
- `~/.local/state/retrofx-v2-dev/install-state.json`
- `~/.local/state/retrofx-v2-dev/current-state.json`
- `~/.local/state/retrofx-v2-dev/manifests/`
- `~/.local/state/retrofx-v2-dev/last-good/`
- `~/.local/state/retrofx-v2-dev/logs/`

Reserved but not yet actively managed:

- `~/.config/retrofx-v2-dev/profiles/`
- `~/.config/retrofx-v2-dev/packs/`
- `~/.local/bin/retrofx-v2-dev`

### Future Public Distribution

Not implemented now:

- copied standalone toolchain installs
- distro packaging
- signed release assets
- public package registries or remote galleries

Future distribution work must build on the bundle and install-state primitives introduced here instead of inventing a second ownership model.

## What Install Owns Now

The first install slice owns only assets that live inside the managed `retrofx-v2-dev` footprint and are recorded in install-state metadata.

Current install-owned assets:

- copied dev bundle contents under the managed data root
- per-bundle install records
- the install index file

Current install does not claim ownership of:

- the 1.x runtime tree
- `~/.config/retrofx`
- `~/.local/bin/retrofx`
- arbitrary WM or DE config trees
- export files written outside the managed 2.x footprint

## Install Versus Export

Export-only and install are still different:

- export-only produces inspectable artifacts but claims no lifecycle ownership
- bundle generation packages those artifacts into a deterministic distribution unit
- install copies that bundle into a managed user-local footprint and records ownership

That separation is deliberate.
It allows 2.x to become installable without quietly turning every export into managed state.

## Install Versus Apply

Install in TWO-19 is still non-live:

- it does not reload a terminal
- it does not touch a live WM session
- it does not enable a session default
- it does not execute session orchestration

It prepares a managed footprint only.

The new bounded apply slice is separate:

- it consumes compiled and installed bundle content
- it stages a current activation inside the same isolated footprint
- it still does not claim system-wide or 1.x ownership

## Ownership And Reversibility

Install remains safe by following these rules:

- user-local only
- no root required
- no writes to `/etc`
- explicit bundle ids
- explicit per-bundle install records
- uninstall driven by those records

This keeps the 2.x install slice aligned with the same safety philosophy that made 1.x trustworthy, without reusing the 1.x path layout.

## Current Limitations

The first install slice is intentionally narrow:

- it installs bundles, not live sessions
- it does not yet install a standalone 2.x toolchain
- it does not yet own desktop integration hooks
- it does not yet perform repair or upgrade orchestration

Those are future steps, not hidden promises.
