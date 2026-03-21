# v2/core/models

Purpose:

- future home of the core pipeline data shapes

Primary model distinctions:

- raw profile input: authored text and source context
- normalized profile: canonical target-agnostic profile shape
- resolved semantic model: concrete semantic meaning before capability filtering
- resolved profile: resolved semantic model plus target and artifact planning

Do implement here later:

- stable internal model definitions
- provenance and warning record shapes
- planner-visible model helpers

Do not implement here:

- adapter-specific syntax objects
- live session state mutation logic
- hidden fallback behavior that changes model meaning outside the core pipeline

