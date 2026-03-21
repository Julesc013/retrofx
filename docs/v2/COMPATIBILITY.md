# RetroFX 2.x Compatibility

RetroFX 2.x compatibility currently means inspection and draft migration of selected 1.x profile concepts.
It does not mean that 2.x can run the 1.x runtime model or replace the 1.x CLI.

As of TWO-15, the compatibility slice is real but narrow:

- 1.x profile intake exists under `v2/compat/`
- the supported 1.x subset can be mapped into a deterministic 2.x draft profile
- lossy, manual, and unsupported mappings are reported explicitly
- generated drafts are emitted only to `v2/out/migrations/`

## What Exists Now

Implemented now:

- load and validate the supported 1.x profile subset
- inspect the real 1.x profile path and infer legacy pack origin when present
- map core metadata, mode, palette, effects, scope, fonts, AA, and color anchors into 2.x concepts
- emit a machine-readable migration report
- optionally emit a generated 2.x draft profile for review

Implemented dev-only tools:

- `v2/compat/dev/inspect-1x-profile <path>`
- `python3 -m v2.compat.dev.inspect_1x_profile <path>`

## What Does Not Exist Yet

Not implemented:

- runtime compatibility mode
- direct execution of 1.x profiles through the 2.x engine
- in-place upgrade of 1.x profiles
- 1.x state, install, apply, off, or repair migration
- full 1.x pack installation or conversion workflows
- lossless migration of every 1.x field

## Mapping Classes

The first compatibility slice classifies each relevant 1.x field as one of:

- `clean`: direct mapping into a 2.x field
- `degraded`: mapped, but through a semantic or structural approximation
- `manual`: preserved in the report, but requires review or later design work
- `unsupported`: ignored for now and surfaced explicitly

Examples:

- `mode.type -> render.mode` is `clean`
- `monochrome.phosphor -> color.semantic.*` is `degraded`
- `effects.transparency` is `manual`
- `rules.*` is `unsupported`

## Output Convention

When draft emission is requested, artifacts are written under:

```text
v2/out/migrations/<profile-id>/
```

Typical artifacts:

- `draft-profile.toml`
- `migration-report.json`
- `summary.txt`

These are review artifacts only.
They do not replace the source 1.x profile and they are not active runtime state.

## Current Rule

`scripts/retrofx` remains the working 1.x CLI.
The 2.x compatibility slice is a bridge for inspection and migration planning, not a hidden handover.
