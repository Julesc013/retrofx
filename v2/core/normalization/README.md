# v2/core/normalization

Purpose:

- home of the first target-agnostic normalization layer for 2.x

Implemented now:

- schema-default filling for the initial core fields
- enum canonicalization
- basic path normalization for palette sources
- semantic-color derivation for omitted optional tokens
- default terminal and TTY ANSI palette construction

What belongs here:

- canonical internal profile shaping
- deterministic fallback generation
- source-path normalization without side effects

What does not belong here:

- capability filtering
- target emission
- session apply or install logic

Governing docs:

- `docs/v2/NORMALIZATION_RULES.md`
- `docs/v2/PROFILE_SCHEMA.md`

Later prompts should implement:

- richer family defaults
- composition flattening once supported
- broader alias handling if the schema grows
