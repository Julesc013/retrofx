# RetroFX 2.x Alpha Versioning

RetroFX 2.x now has an explicit experimental version policy for internal alpha circulation plus a separate limited technical-beta candidate identity.

1.x remains the production line.
2.x versioning here exists for the experimental branch surface, bundle metadata, internal-alpha package artifacts, and the local limited technical-beta candidate package.

## Current Version

- current 2.x experimental version: `2.0.0-alpha.internal.2`
- current status label: `internal-alpha`
- current packaging prompt milestone: `TWO-31`
- current technical-beta prompt milestone: `TWO-32`
- current version tag name: `v2.0.0-alpha.internal.2`
- latest local/internal alpha candidate tag: `v2.0.0-alpha.internal.1`
- current build kind: untagged post-alpha hardening
- reserved non-public pre-beta candidate version: `2.0.0-prebeta.internal.1`
- reserved non-public pre-beta candidate tag: `v2.0.0-prebeta.internal.1`
- approved limited technical-beta candidate version: `2.0.0-techbeta.1`
- approved limited technical-beta candidate tag: `v2.0.0-techbeta.1`
- code-side source of truth: `v2/dev/release.py`

## Format

The current internal format is:

`2.0.0-alpha.internal.<n>`

Example:

- `2.0.0-alpha.internal.2`

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

The separate limited technical-beta candidate identity means:

- a copied-toolchain candidate package can be produced for advanced testers
- the broader `retrofx-v2` developer surface still remains internal-only

## Version Discipline

Use this rule set for now:

- increment the trailing internal alpha number when the branch meaningfully changes its internal testing contract
- reserve the first matching `2.0.0-prebeta.internal.<n>` only when the pre-beta gates are actually satisfied
- do not invent multiple competing 2.x version formats
- keep the version static within a given committed internal-alpha state
- keep status labels separate from readiness decisions
- keep historical local candidate tags separate from newer untagged hardening builds
- keep the technical-beta candidate identity separate from both the internal-alpha line and the blocked pre-beta line

## Readiness Versus Version

Version and readiness are related but not identical.

Example:

- version: `2.0.0-alpha.internal.2`
- status label: `internal-alpha`
- readiness decision: controlled internal alpha is acceptable for a narrow cohort, but the current build is not a local alpha candidate and is not a non-public pre-beta candidate

That means the branch can be circulated internally without promoting the status label to anything public-facing.

For TWO-29 through TWO-32, the branch version remains on the internal-alpha line intentionally so the current hardening build is not mistaken for either the historical local alpha candidate tagged at `v2.0.0-alpha.internal.1` or the still-blocked reserved pre-beta candidate `v2.0.0-prebeta.internal.1`.

The limited technical-beta candidate uses a separate version identity:

- candidate version: `2.0.0-techbeta.1`
- candidate status label: `technical-beta`
- candidate package flow: `scripts/dev/retrofx-v2 package-technical-beta`
