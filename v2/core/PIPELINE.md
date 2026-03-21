# v2/core Pipeline

This file maps the future `v2/core/` implementation surface to the 2.x engine pipeline.

## Planned Core Stages

1. raw profile load orchestration
2. schema validation orchestration
3. normalized profile creation
4. resolved semantic model creation
5. capability-filtered target planning
6. artifact planning
7. compile or apply planning handoff

## Ownership

`v2/core/` should orchestrate the pipeline.
It should not render backend-specific files itself.

Expected future sub-areas:

- `models/` for normalized and resolved engine data shapes
- `planning/` for target-plan and artifact-plan orchestration
- `interfaces/` for contracts between core, targets, and session

## Current State

TWO-08 implements only the first narrow slice:

- raw profile loading
- schema-facing validation
- normalization
- resolved-profile scaffolding
- a dev-only inspection entrypoint

Still not implemented here:

- capability filtering
- target planning
- artifact planning
- target emission
- session orchestration
