# RetroFX 2.x Adapter Interface

This document defines the conceptual interface surface for 2.x target adapters.
It is design only, but it should be precise enough for later implementation in shell, Python, or another small implementation language.

## Interface Goal

Adapters should expose a predictable contract so core planning and session orchestration can treat different targets consistently.

## Conceptual Operations

### `declare_capabilities()`

Purpose:

- return the adapter's declared support contract

Should include:

- supported target family and concrete target id
- capability categories
- supported execution modes
- artifact kinds it can emit
- validation support level
- degradation policies or notes
- environment constraints

This operation must be side-effect free.

### `can_support(resolved_profile, environment)`

Purpose:

- answer whether the adapter can truthfully participate in planning for the given resolved profile and environment context

Should return:

- supported
- degraded
- export-only
- unsupported

And also:

- reasons
- unmet requirements
- whether degradation is deterministic

This is not a substitute for global capability filtering, but it gives core planning adapter-local truth.

### `plan_outputs(resolved_profile, target_plan, artifact_context)`

Purpose:

- describe what the adapter would emit for the accepted target-plan entry

Should return:

- planned artifact descriptions
- required versus optional distinction
- apply-capable actions if any
- install-capable outputs if any
- warnings or degradation notes

This operation should still be side-effect free.

### `emit(output_dir, resolved_profile, target_plan, artifact_plan)`

Purpose:

- render target-specific artifacts into a staging area or requested export location

Should return:

- emitted artifact records
- validation-ready metadata
- deterministic warnings

This is the first operation allowed to write files for the target.

### `apply(...)`

Purpose:

- perform target-scoped apply behavior where the target family truthfully supports it

Should exist only for adapters that actually support apply-like behavior.

Should return:

- apply result
- scoped actions performed
- rollback-relevant notes

### `validate(...)`

Purpose:

- validate emitted artifacts or target-local assumptions where supported

Examples:

- syntax sanity checks
- static validation of emitted config fragments
- target-local completeness checks

### `describe_degradation(...)`

Purpose:

- convert adapter-local downgrade decisions into structured notes for logs, status, and explainability

Should report:

- what degraded
- why it degraded
- whether the degradation was deterministic
- whether the result remains apply-capable or export-only

## Unsupported Input Behavior

Adapters should never quietly reinterpret unsupported input as if it were valid.

On unsupported input, an adapter should return one of:

- structured unsupported result
- structured degraded result
- structured export-only result

It should not:

- parse raw profile text itself
- silently drop major behavior without reporting it
- invent target capabilities that were not declared

## Warning Versus Hard Failure

### Warning

Use a warning when:

- the target remains valid
- unsupported tokens can be ignored or downgraded deterministically
- the emitted result is still truthful

Examples:

- unsupported chrome token ignored for a TTY target
- scanlines dropped for a terminal export target

### Hard Failure

Use a hard failure when:

- the target-plan entry itself is invalid
- required artifacts cannot be emitted
- claimed support would become false

Examples:

- an apply-capable X11 render target cannot emit its required render artifacts
- a target-plan entry requires install behavior the adapter does not support

## Deterministic Degradation

Deterministic degradation means:

- the adapter applies the same downgrade for the same resolved profile and environment
- the downgrade is recorded explicitly
- the adapter does not oscillate between behaviors based on hidden heuristics

Degradation should be expressed as:

- capability lost
- substituted behavior
- resulting mode change, if any

Examples:

- `render.scanlines -> dropped`
- `session.apply -> export-only`
- `chrome.notification_style -> ignored`

## Boundary Reminder

Adapters are downstream of core planning.
They do not own:

- raw profile parsing
- normalization
- capability-selection policy
- cross-target coordination

