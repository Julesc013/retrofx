# RetroFX 2.x Artifact Planning

Artifact planning is the stage that turns a capability-filtered target plan into an explicit inventory of files, metadata records, and lifecycle assets.
It exists so emission, apply, off, repair, and self-check all operate from the same contract.

## Why Artifact Planning Must Be Explicit

RetroFX 1.x demonstrated that lifecycle trust depends on explicit artifact classes.
2.x carries that lesson forward and makes it a planned compiler stage instead of an implementation afterthought.

Without explicit artifact planning:

- apply cannot know what success means
- off and repair cannot know what to restore or remove
- self-check cannot know what is missing versus optional
- export-only behavior gets confused with runtime ownership

## Why Artifact Planning Happens After Capability Filtering

Artifact planning must happen after capability filtering because the artifact set depends on what the engine will actually do.

Examples:

- a render-capable X11 plan may require shader and compositor-adjacent artifacts
- a `sway` plan may not require those artifacts at all
- a GNOME Wayland export-only plan may produce toolkit and terminal exports but no live runtime artifacts

Planning artifacts before truthful capability decisions would produce the wrong contract.

## Artifact Plan Inputs

Artifact planning consumes:

- resolved profile
- capability-filtered target plan
- session policy
- apply or export mode

It does not read raw profile text directly.

## Artifact Classes

The 2.x artifact plan should carry forward the useful 1.x distinctions with clearer planning semantics.

### `required-runtime`

Artifacts required for the selected active runtime plan to be correct.

Examples:

- active target config files
- required runtime metadata
- required session fragments

### `optional-runtime`

Artifacts emitted for runtime convenience or richer integration that do not define base health.

Examples:

- optional helper snippets
- optional convenience theme exports bundled with an apply

### `ephemeral-runtime`

Transient artifacts used for validation, staging, or runtime coordination.

Examples:

- staging files
- transient validation outputs
- temporary adapter reports

### `export-only`

Artifacts that are intentionally generated without claiming runtime ownership.

Examples:

- terminal config exports
- toolkit exports
- pack preview outputs

### `install-asset`

Assets required for later install, apply, repair, or compatibility operations.

Examples:

- wrapper templates owned by the install footprint
- copied pack assets needed by a compiled plan
- migration-generated helper data that future operations depend on

### `manifest-record`

Metadata artifacts that define what the engine believes exists and why.

Examples:

- current manifest
- last-good manifest
- artifact-plan summaries
- runtime intent records

### `ignored-log-or-cache`

Files the engine may create or touch, but which must not define runtime correctness.

Examples:

- logs
- caches
- preview thumbnails

## Artifact Plan Shape

Each planned artifact entry should contain at least:

- artifact id
- artifact class
- producing target or subsystem
- lifecycle role
- apply relevance
- export relevance
- requiredness
- manifest relevance
- reason for existence

Optional additional fields may include:

- destination scope
- staging behavior
- install ownership
- repair ownership

## Artifact Classes Versus Targets

Targets and artifact classes are different concepts.

- a target is a compilation destination such as `kitty`, `tty`, or `sway`
- an artifact class describes why a generated output exists in lifecycle terms

One target may produce multiple artifact classes.
For example:

- a terminal target may emit `required-runtime`, `export-only`, and `manifest-record` artifacts

## Manifest Concept

In a future 2.x engine, manifests should be derived from the artifact plan and actual emission results.
They conceptually belong to the session and lifecycle layer, but they must reflect core planning truth.

That means:

- core planning defines what should exist
- emission records what was actually produced
- session records what became active or installed
- manifest records the contract between those facts

## Future Lifecycle Use

### Apply

`apply` should use the artifact plan to determine:

- what must be staged
- what must be validated before activation
- what counts as a successful apply

### Off

`off` should use the artifact plan and manifest to determine:

- which active artifacts it owns
- which should be removed, disabled, or rolled back
- which export-only artifacts should be left alone

### Repair

`repair` should use the artifact plan and manifest to determine:

- what required artifacts are missing or corrupt
- whether a last-good state can be restored
- whether a degraded fallback plan is necessary

### Self-Check

`self-check` should validate:

- required runtime artifacts against the active manifest
- install assets against the install manifest
- export completeness separately from runtime correctness

## Planned Outputs

The artifact planning stage should produce:

- required artifact set
- optional artifact set
- export-only artifact set
- install-asset set
- manifest-intent set
- validation expectations for later lifecycle operations

## Carried Forward From 1.x

These lessons are intentionally preserved:

- explicit artifact classes
- manifest-based integrity reasoning
- clear separation between runtime correctness and convenience outputs
- conservative repair philosophy

These are intentional departures:

- artifact contracts should come from the target plan, not from ad hoc backend behavior
- export-only and runtime artifacts should be planned before emission, not inferred after the fact

