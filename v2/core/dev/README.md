# v2/core/dev

Purpose:

- home of non-production developer entrypoints for the experimental 2.x core

Implemented now:

- `resolve_profile.py`: load, validate, normalize, and resolve a 2.x profile fixture or file
- `resolve-profile`: thin shell wrapper around the Python module

What belongs here:

- dev-only inspection tools
- non-destructive debug entrypoints
- machine-readable pipeline output for fixtures and tests

What does not belong here:

- production CLI commands
- target emission workflows
- live apply or install behavior

Governing docs:

- `docs/v2/CORE_PIPELINE.md`
- `docs/v2/PROFILE_SCHEMA.md`
- `docs/v2/IMPLEMENTATION_SEQUENCE.md`

Current rule:

- these entrypoints are experimental and must not be presented as the real RetroFX user workflow
