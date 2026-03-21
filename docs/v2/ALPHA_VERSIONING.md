# RetroFX 2.x Alpha Versioning

RetroFX 2.x now has an explicit non-public experimental version policy for internal alpha circulation.

1.x remains the production line.
2.x versioning here exists only for the experimental branch surface, bundle metadata, and internal-alpha package artifacts.

## Current Version

- current 2.x experimental version: `2.0.0-alpha.internal.1`
- current status label: `internal-alpha`
- current packaging prompt milestone: `TWO-25`

## Format

The current internal format is:

`2.0.0-alpha.internal.<n>`

Example:

- `2.0.0-alpha.internal.1`

Why this format:

- clearly distinct from 1.x
- clearly pre-release
- clearly non-public
- simple enough to stamp into bundle, install, and package metadata

## What The Version Applies To

The 2.x experimental version currently identifies:

- internal-alpha package manifests
- experimental release-status metadata in bundle manifests
- install-state records derived from those bundles
- machine-readable platform status output

It does not mean:

- a public release exists
- 2.x has replaced 1.x
- package-manager distribution is ready
- the runtime is stable

## Version Discipline

Use this rule set for now:

- increment the trailing internal alpha number when the branch meaningfully changes its internal testing contract
- do not invent multiple competing 2.x version formats
- keep the version static within a given committed internal-alpha state
- keep status labels separate from readiness decisions

## Readiness Versus Version

Version and readiness are related but not identical.

Example:

- version: `2.0.0-alpha.internal.1`
- status label: `internal-alpha`
- readiness decision: controlled internal alpha is acceptable for a narrow cohort

That means the branch can be circulated internally without promoting the status label to anything public-facing.
