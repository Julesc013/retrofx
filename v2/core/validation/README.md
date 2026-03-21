# v2/core/validation

Purpose:

- home of the first 2.x schema-facing validation primitives

Implemented now:

- required-structure checks
- enum and range checks for the early core fields
- strict unknown-key checks for the implemented schema surface
- warning versus error separation
- basic post-normalization compatibility checks

What belongs here:

- raw profile structural validation
- normalized-profile compatibility validation
- issue generation for dev-only inspection output

What does not belong here:

- environment-aware capability filtering
- target emission logic
- live session side effects

Governing docs:

- `docs/v2/PROFILE_SCHEMA.md`
- `docs/v2/VALIDATION_RULES.md`
- `docs/v2/MODULE_BOUNDARIES.md`

Later prompts should implement:

- broader schema coverage
- richer warning surfaces
- composition-aware validation once composition support exists
