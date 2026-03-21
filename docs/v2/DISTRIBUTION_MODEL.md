# RetroFX 2.x Distribution Model

RetroFX 2.x now has a first local distribution primitive: the dev bundle.
This is not a public package ecosystem.
It is a controlled, local-first shape for packaging resolved-profile outputs into something installable and inspectable.

## Current Implementation Status

As of TWO-24:

- repo-local bundles are real under `v2/bundles/<bundle-id>/`
- reproducible internal-alpha packages are real under `v2/releases/internal-alpha/<package-id>/`
- the bundle manifest schema is `retrofx.bundle/v2alpha1`
- the internal-alpha package manifest schema is `retrofx.internal-alpha-package/v2alpha1`
- bundles can be installed into an isolated user-local `retrofx-v2-dev` footprint
- uninstall and status are driven from install-state metadata
- the unified dev surface now exposes bundle, install, uninstall, and status through `scripts/dev/retrofx-v2`
- the unified dev surface now also exposes `package-alpha`
- public archives, remote registries, and distro packaging are still future work

## Distribution Units

### Dev Bundle

The current distribution unit is a deterministic bundle directory.

Shape:

- `manifest.json`
- `metadata/resolved-profile.json`
- `metadata/session-plan.json`
- `metadata/source.json`
- `metadata/summary.txt`
- `targets/<target>/...`

The bundle is designed to be:

- inspectable by humans
- machine-readable by future tooling
- local-first
- safe to regenerate

### Install-State Record

Bundles become installed state only when copied into the managed user-local footprint.
At that point the distribution story adds:

- `installations/<bundle-id>.json`
- `install-state.json`

Those files are not part of the source bundle itself.
They are lifecycle metadata owned by the install layer.

### Internal-Alpha Package

The current non-public release-like unit is the internal-alpha package directory.

Shape:

- `package-manifest.json`
- `bundle/`
- `docs/`
- `metadata/`

It is designed to be:

- reproducible
- self-describing
- non-public
- repo-checkout dependent on purpose

## What Bundles Contain

Bundles may contain:

- emitted target artifacts
- pack metadata
- source origin metadata
- session-plan preview metadata
- install hints
- experimental release metadata

Bundles currently do not contain:

- live runtime state
- session wrappers in active use
- 1.x compatibility runtime shims
- root/system integration

## Why Bundles Exist

The bundle layer exists to solve a practical problem:

- `v2/out/` is useful for direct compiler inspection
- but `v2/out/` is not a lifecycle-owned install shape

Bundles turn compiler output into a unit that can be:

- installed locally
- copied around for developer testing
- used as a future release primitive
- referenced in install-state metadata

## Current Boundaries

The first distribution slice is intentionally local-only.

Not implemented:

- remote bundle fetching
- signed bundle verification
- community pack registries
- archive publishing
- distro-native package generation

Future prompts may build those on top of the bundle manifest, but must not bypass it with ad hoc package shapes.
