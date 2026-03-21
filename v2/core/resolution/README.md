# v2/core/resolution

Purpose:

- home of the first resolved-profile construction scaffold for 2.x

Implemented now:

- compiler-facing resolved-profile shape creation from the normalized profile
- placeholder target-request, target-plan, and artifact-plan sections
- issue and normalization-note carry-forward for dev inspection

What belongs here:

- resolved semantic model construction
- compiler-facing JSON-serializable scaffolding
- explicit not-yet-implemented placeholders for later planning stages

What does not belong here:

- capability filtering
- target adapter binding
- session orchestration

Governing docs:

- `docs/v2/RESOLVED_MODEL.md`
- `docs/v2/CORE_PIPELINE.md`

Later prompts should implement:

- capability context population
- real target planning
- real artifact-plan construction
