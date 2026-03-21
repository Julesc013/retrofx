# RetroFX 2.x Side-Effect Policy

RetroFX 2.x needs a strict side-effect policy so later implementation prompts do not smuggle lifecycle behavior into planning, theme, render, or target code.

This document defines that policy.

## Side-Effect Classes

| Class | Meaning | Examples |
| --- | --- | --- |
| `none` | no filesystem or runtime mutation | validation, normalization, resolution, capability filtering, dry-run, explain |
| `artifact-emission-only` | generate artifacts without claiming live ownership | export files, emitted config fragments, preview outputs |
| `session-local` | scoped live-session mutation | activating current-session files, scoped runtime hooks, current-state records |
| `install-state` | managed install-footprint mutation | install assets, default records, install manifests |
| `login-or-session-integration` | managed startup or login hook mutation | Xsession entries, login snippets, launch helpers, managed integration records |

## Hard Rules

1. No side effects are allowed during raw loading, validation, normalization, semantic resolution, capability filtering, or artifact planning.
2. Target compilers emit artifacts; they do not invent session orchestration or live activation policy.
3. Session orchestration is the only layer allowed to trigger `apply-now`, install, uninstall, off, repair, or integration-hook side effects.
4. Side effects must always be attached to an explicit execution mode.
5. Side effects must be capability-aware and environment-aware.
6. Side effects must be logged and represented in lifecycle state or manifest records where relevant.
7. Export-only artifact emission must not be misrepresented as apply or install ownership.
8. If a path cannot be disabled, repaired, or uninstalled predictably, RetroFX should not claim strong lifecycle ownership over it.

## Stage Boundaries

### Stages With No Side Effects

These stages must stay side-effect free:

- raw profile loading
- schema validation
- normalization
- semantic resolution
- capability filtering
- artifact planning
- dry-run and explain

### Artifact Emission Boundary

Artifact emission begins only after planning is complete.

Artifact emission may:

- write exported outputs
- stage generated files
- record emission reports

Artifact emission may not:

- silently mark the session active
- silently mark artifacts installed
- silently update login hooks

### Session Boundary

Only the session subsystem may:

- promote emitted artifacts into active current-session state
- write current-state descriptors
- update last-good or recovery records
- write install manifests
- create managed integration hooks

## Logging And Manifest Expectations

Whenever side effects occur, later implementations should record:

- what mode ran
- what targets participated
- what side effects occurred
- what ownership was claimed
- what degraded or skipped decisions were made

That record may be split across manifests, state descriptors, and logs, but it must exist.

## Forbidden Patterns

Later prompts must not implement these patterns:

- target adapters that edit live config paths directly during emission
- render code that launches or controls compositor processes
- theme helpers that write terminal configs straight to active paths
- session wrappers that infer intent from file presence alone
- install code that claims ownership of unmanaged user config trees

## Dry-Run And Explain Policy

`dry-run` and `explain` are strict `none` side-effect modes.

They may:

- compute plans
- inspect existing state
- report warnings

They may not:

- emit persistent artifacts intended for users
- update manifests
- change active or install state

## Relation To Support Truth

Support classes and side-effect classes are related.

Examples:

- a target that only supports `artifact-emission-only` should usually be `export-only`
- a target that can emit but cannot be disabled or repaired cleanly should not claim strong apply or install support

This rule is essential to keep 2.x honest.

## Relation To 1.x

2.x carries forward the strongest 1.x lesson here:

- side effects must be explicit, bounded, and recoverable

It improves on 1.x by making that a subsystem rule rather than a property of a few shell commands and wrappers.
