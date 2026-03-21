# RetroFX 2.x State And Recovery

RetroFX 2.x must treat state and recovery as planned lifecycle concepts, not as whatever files happen to exist after apply.

This document defines the conceptual records and recovery boundaries that future prompts should implement.

## Why State Exists

State exists so RetroFX can answer:

- what is active now
- what was supposed to be active
- what is install-owned
- what can be repaired
- what can be removed
- what degraded fallback remains safe when the preferred state is broken

Without explicit state, `off`, `repair`, `self-check`, uninstall, and wrapper behavior become guesswork.

## Core Concepts

### Current State Descriptor

The current state descriptor is the session-layer record of the active or most recently activated plan.

It should capture at least:

- profile identity
- execution mode
- environment class
- applied target set
- degraded and export-only decisions
- runtime requirements such as compositor need
- references to manifests and recovery baselines

This is the 2.x evolution of the useful 1.x `active/meta` idea.

### Applied Target Plan Record

This record captures what target plan was actually executed, not just what was theoretically requested.

It should describe:

- which targets emitted artifacts
- which targets became active
- which targets stayed export-only
- which targets degraded
- which targets were skipped or refused

### Artifact Manifest

The artifact manifest records what the lifecycle layer believes should exist and why.

It should be derived from:

- artifact planning truth
- actual emission results
- actual activation or install outcomes

The manifest should preserve artifact classes such as:

- required runtime
- optional runtime
- ephemeral runtime
- export-only
- install asset
- manifest record
- ignored log or cache

### Recovery Baseline

The recovery baseline is the preferred known-good state that repair and rollback can trust.

It should usually include:

- a validated last-good current-state descriptor
- a matching applied target plan record
- matching manifests
- any install-state links needed to restore or disable safely

### Degraded Fallback State

The degraded fallback state is the safe reduced state used when the preferred recovery baseline is unavailable or invalid.

Examples:

- disabling compositor-owned runtime effects while keeping exportable theme outputs
- falling back to a plain session with preserved exported artifacts
- leaving install-owned assets intact while resetting current active state

Degraded fallback is not the same as pretending recovery succeeded fully.

## Recommended State Records

Future implementation prompts should plan at least these logical records:

- current state descriptor
- current artifact manifest
- last-good recovery baseline
- install-state descriptor
- install manifest
- recovery or explain logs

Exact filenames are deferred.
The important rule is that current-session state and install-owned state remain distinct.

## What Different Operations Act On

### `apply-now`

Acts on:

- emitted artifacts selected for live activation
- current state descriptor
- current manifest
- recovery baseline updates

Does not act on:

- arbitrary install-owned defaults unless explicitly combined with install modes

### `off`

Acts on:

- current active state
- active manifests
- session-owned runtime hooks

Does not act on:

- export-only artifacts outside active ownership
- install-owned assets unless the operation explicitly includes uninstall or install-reset semantics

### `repair`

Acts on:

- current runtime state
- current and last-good manifests
- install-state records when they are relevant to the broken path

Preferred behavior:

- restore a manifest-valid last-good baseline
- if that is impossible, fall back to a clearly logged degraded safe state

### `self-check`

Acts on:

- current runtime state versus runtime manifest
- install assets versus install manifest
- recovery baseline integrity

It should report those domains separately.

### Uninstall

Acts on:

- install-owned assets
- install manifests
- install-owned integration hooks

It must not act on:

- arbitrary current-session state unless explicitly coupled to a disable step
- user-owned exports outside install ownership

## Wrapper And Integration Trust Rules

Future session wrappers and startup helpers should trust:

- explicit recorded runtime intent
- explicit manifests
- explicit integration records

They should not trust:

- mere file presence
- guessed compositor need
- guessed ownership from destination paths alone

This directly carries forward a key 1.x lesson.

## Dry-Run And Explain

`dry-run` and `explain` should remain side-effect free.

They should operate on:

- resolved profile
- target plan
- artifact plan
- environment model
- existing state records when relevant

They should not:

- write active state
- mutate install state
- update recovery baselines

## Rollback Boundaries

Rollback should be scoped and explicit.

Examples of safe rollback boundaries:

- current-session active artifacts
- current-session integration side effects
- managed install-state changes from a single transaction

Examples of things that should not be treated as implicit rollback targets:

- export-only files outside RetroFX ownership
- arbitrary user-edited configs outside manifest ownership

## Relation To 1.x

2.x intentionally carries forward these 1.x lessons:

- explicit current versus last-good records
- manifest-based lifecycle integrity
- degraded fallback when perfect restore is impossible
- separate install-asset health and runtime health
- wrappers should trust recorded intent, not file existence alone

2.x improves the model by:

- separating current-state and install-state records more clearly
- treating applied target plans as explicit records
- making recovery boundaries part of the architecture instead of backend behavior
