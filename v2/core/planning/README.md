# v2/core/planning

Purpose:

- future home of target-plan and artifact-plan orchestration

Do implement here later:

- capability-filtered target planning
- artifact planning
- planner decision recording
- dry-run and inspect-mode planning helpers

Do not implement here:

- target-specific file emission
- runtime session mutation
- raw profile parsing shortcuts

Planning rule:

- this area should operate on resolved data only, never on raw authored TOML.

