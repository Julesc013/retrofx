# RetroFX 2.x Release Shape

RetroFX 2.x is not publicly released yet, but the shape of a future release should already be constrained.

## Current Implementation Status

As of TWO-16, the only real release-like unit is the local dev bundle.
That means release shape work is now grounded in real artifacts instead of speculation.

## Current Real Units

### Source Tree

The repository remains the authoritative source for:

- design docs
- the experimental Python scaffold
- dev entrypoints
- tests

### Dev Bundle

`retrofx.bundle/v2alpha1` is now the first concrete release primitive.
It contains:

- manifest
- metadata
- compiled target artifacts
- install hints

### User-Local Install Footprint

The experimental `retrofx-v2-dev` XDG footprint is now the first installable target shape for those bundles.

## Future Public Release Shape

Future public releases should likely separate:

- source archives
- curated pack content
- dev or preview bundles
- standalone toolchain packages
- release notes and migration notes

Those future shapes must reuse the current bundle and install-state concepts rather than inventing parallel release metadata.

## Explicitly Deferred

Not implemented now:

- signed releases
- distro packages
- GitHub release automation
- remote bundle feeds
- stable package-manager integration

The current goal is safe experimental installability, not wide distribution.
