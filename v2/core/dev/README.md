# v2/core/dev

Purpose:

- home of non-production developer entrypoints for the experimental 2.x core

Implemented now:

- `resolve_profile.py`: load, validate, normalize, and resolve a 2.x profile fixture or file
- `resolve-profile`: thin shell wrapper around the Python module
- `compile_targets.py`: compile the implemented terminal/TUI, WM, typography-policy, bounded X11 render, and display-policy target families into `v2/out/<profile-id>/...`
- `compile-targets`: thin shell wrapper around the compiler entrypoint
- `plan_session.py`: detect the environment, build a capability-aware session plan, surface resolved typography and display policy, and optionally write a preview bundle
- `plan-session`: thin shell wrapper around the session planner
- `v2/session/dev/preview_x11_render.py`: explicit dev-only X11 render staging plus optional bounded `picom` probe
- `list_packs.py`: list built-in local 2.x packs from `v2/packs/`
- `list-packs`: thin shell wrapper around the local pack listing entrypoint
- `show_pack.py`: inspect one local pack manifest and its curated profiles
- `show-pack`: thin shell wrapper around the pack inspection entrypoint

What belongs here:

- dev-only inspection tools
- non-destructive debug entrypoints
- machine-readable pipeline output for fixtures and tests

What does not belong here:

- production CLI commands
- production target emission workflows
- default live apply or install behavior

Governing docs:

- `docs/v2/CORE_PIPELINE.md`
- `docs/v2/PROFILE_SCHEMA.md`
- `docs/v2/IMPLEMENTATION_SEQUENCE.md`

Current rule:

- these entrypoints are experimental and must not be presented as the real RetroFX user workflow
- emitted artifacts land under `v2/out/`, which is intentionally separate from 1.x `active/` and `state/`
- pack-aware resolution is local-only and uses `--pack <pack-id> --profile-id <profile-id>` instead of changing the 1.x CLI path
