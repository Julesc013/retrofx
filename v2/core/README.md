# v2/core

Purpose:

- future home of profile loading orchestration, normalization, resolution, capability filtering, artifact planning, and high-level compile or apply planning
- future center of gravity for the 2.x compiler heart

Implemented now:

- stdlib-only experimental load, validate, normalize, and resolve primitives
- dev-only inspection entrypoint for printing resolved-profile scaffolding

Do implement here later:

- normalized profile pipeline
- resolved semantic model creation
- resolved profile planning
- capability-filtered target planning
- artifact planning contracts
- core-to-target and core-to-session interfaces

Planned sub-areas:

- [`PIPELINE.md`](PIPELINE.md): high-level core pipeline map
- [`models/`](models/README.md): normalized and resolved data-shape ownership
- [`planning/`](planning/README.md): target-plan and artifact-plan ownership
- [`interfaces/`](interfaces/README.md): contracts exposed to targets and session

Do not implement here:

- target-specific file renderers
- backend shell hacks
- direct session startup logic

Current rule:

- this directory now contains an initial dev-only core scaffold, but it must not pretend the full 2.x engine is implemented
- capability filtering, target planning, artifact planning, and any live lifecycle behavior remain future work
