# v2/compat/dev

Purpose:

- home of non-production developer entrypoints for 1.x compatibility inspection and draft migration output

Implemented now:

- `inspect_1x_profile.py`: inspect a RetroFX 1.x profile, map the supported subset into 2.x concepts, and optionally emit a generated draft 2.x profile bundle
- `inspect-1x-profile`: thin shell wrapper around the compatibility inspection module

What belongs here:

- dev-only 1.x intake and migration reporting
- deterministic draft emission for review
- machine-readable compatibility inspection output

What does not belong here:

- production CLI compatibility mode
- in-place upgrades of 1.x files
- live apply, install, or session behavior

Governing docs:

- `docs/v2/MIGRATION.md`
- `docs/v2/COMPATIBILITY.md`
- `docs/v2/RELATION_TO_1X.md`

Current rule:

- this surface is experimental and review-oriented
- emitted drafts land under `v2/out/migrations/` and must not be treated as authoritative production configs
- `scripts/retrofx` remains the working 1.x CLI
