# v2/core/models

Purpose:

- home of the experimental 2.x core pipeline data shapes

Primary model distinctions:

- raw profile input: authored text and source context
- normalized profile: canonical target-agnostic profile shape
- resolved semantic model: concrete semantic meaning before capability filtering
- resolved profile: resolved semantic model plus target and artifact planning

Implemented now:

- dataclass-backed issue, raw-profile, normalized-profile, resolved-profile, and pipeline-result scaffolding in `types.py`

Do implement here later:

- stable internal model definitions
- provenance and warning record shapes
- planner-visible model helpers

Do not implement here:

- adapter-specific syntax objects
- live session state mutation logic
- hidden fallback behavior that changes model meaning outside the core pipeline

Current scope rule:

- the TWO-08 implementation provides only model scaffolding for load/validate/normalize/resolve
- capability filtering, target planning, artifact planning, and session ownership remain future work
