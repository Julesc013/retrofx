# v2/compat

Purpose:

- home of the 2.x compatibility shell and early migration helpers

Implemented now:

- 1.x profile intake and normalization for the supported migration subset
- dev-only migration inspection and draft 2.x profile emission under `v2/compat/dev/`
- explicit reporting of clean, degraded, manual, and unsupported mappings

Do implement here later:

- bridges between legacy workflows and the 2.x engine
- future dispatcher shims once explicit prompts cover that transition
- broader pack and workflow migration once the 2.x runtime is ready

Do not implement here:

- core semantic planning logic
- target emission ownership
- experimental feature dumping ground logic

Current rule:

- `./scripts/retrofx` remains the working 1.x CLI until a later migration phase explicitly changes that.
- current compatibility tooling is dev-only inspection and draft generation, not runtime compatibility mode
