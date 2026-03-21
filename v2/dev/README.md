# v2/dev

Purpose:

- home of the unified experimental developer surface for the 2.x branch

Implemented now:

- `cli.py`: top-level `retrofx-v2` dispatcher for resolve, plan, compile, packs, migration, install, apply, off, preview, and smoke flows
- `status.py`: machine-readable platform capability and current-state report
- `smoke.py`: safe end-to-end developer smoke workflow over the existing 2.x pipeline
- `package_alpha.py`: reproducible non-public internal-alpha package builder around the existing deterministic bundle primitive

What belongs here:

- thin orchestration over already-implemented dev entrypoints
- consolidated platform introspection
- non-destructive review and smoke helpers

What does not belong here:

- production CLI ownership
- new target compiler families
- hidden default runtime takeover

Current rule:

- this module is the unified experimental surface for 2.x developers
- it must stay honest about what is implemented, bounded, export-only, or still planned
