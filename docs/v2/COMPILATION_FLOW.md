# RetroFX 2.x Compilation Flow

This document defines the end-to-end 2.x flow from authored profile to emitted artifacts and optional apply behavior.
It is the operational form of the core pipeline.

## Canonical Flow

1. load raw profile
2. validate schema
3. normalize profile
4. resolve semantic model
5. detect environment and capabilities
6. build capability-filtered target plan
7. build artifact plan
8. emit target artifacts
9. apply runtime or session actions if requested
10. record manifest and state

## Step Contract

### 1. Load Raw Profile

Purpose:

- load authored input and referenced pack metadata or assets

Inputs:

- authored profile path or object
- pack references
- optional selected target override

Outputs:

- raw profile input object
- load context such as source location

No-go responsibilities:

- no defaults
- no capability decisions
- no target emission

### 2. Validate Schema

Purpose:

- reject structurally invalid input before the engine reasons further

Inputs:

- raw profile input
- schema contracts

Outputs:

- validated raw input
- structural errors and warnings

No-go responsibilities:

- no backend matching
- no live environment detection
- no artifact planning

### 3. Normalize Profile

Purpose:

- produce the canonical target-agnostic profile shape

Inputs:

- validated raw input
- default rules
- alias and path normalization rules

Outputs:

- normalized profile
- normalization warnings

No-go responsibilities:

- no environment-specific degradation
- no adapter binding
- no file emission

### 4. Resolve Semantic Model

Purpose:

- turn normalized intent into concrete semantics

Inputs:

- normalized profile
- family defaults
- strictness rules
- theme and render derivation helpers

Outputs:

- resolved semantic model

No-go responsibilities:

- no environment detection
- no target emission
- no runtime mutation

### 5. Detect Environment And Capabilities

Purpose:

- gather the facts required for truthful planning

Inputs:

- user-selected targets or modes
- environment facts
- adapter capability declarations

Outputs:

- capability context

No-go responsibilities:

- no semantic reinterpretation of the profile
- no artifact emission
- no live apply

### 6. Build Capability-Filtered Target Plan

Purpose:

- decide what target outcomes are truthful in the selected environment

Inputs:

- resolved semantic model
- capability context
- session policy

Outputs:

- target plan with apply, degrade, export-only, skip, or refusal outcomes
- degradation and warning records
- runtime requirements such as compositor need

No-go responsibilities:

- no file generation
- no install or apply side effects

### 7. Build Artifact Plan

Purpose:

- determine the concrete artifact inventory required by the target plan

Inputs:

- resolved profile
- target plan

Outputs:

- required artifact set
- optional artifact set
- export-only artifact set
- manifest-intent data

No-go responsibilities:

- no target syntax rendering yet
- no filesystem mutation yet

### 8. Emit Target Artifacts

Purpose:

- run target adapters to render artifacts from the plan

Inputs:

- resolved profile
- target plan
- artifact plan

Outputs:

- emitted files and staged outputs
- adapter emission reports

No-go responsibilities:

- no direct session ownership decisions outside the plan
- no hidden fallback behavior outside logged decisions

### 9. Apply Runtime Or Session Actions If Requested

Purpose:

- perform scoped side effects only after planning and emission are complete

Inputs:

- emitted artifacts
- target plan apply modes
- session policy

Outputs:

- staged or active runtime changes
- apply results and recovery records

No-go responsibilities:

- no reinterpreting profile meaning
- no spontaneous target additions

### 10. Record Manifest And State

Purpose:

- preserve the artifact contract and lifecycle truth for later status, repair, off, and self-check behavior

Inputs:

- artifact plan
- emission results
- apply results

Outputs:

- manifest records
- state metadata
- lifecycle logs

No-go responsibilities:

- no planner backtracking
- no silent dropping of artifacts that were marked required

## Where Side Effects Begin

Side effects begin at Step 8.

Everything before Step 8 should be side-effect free.
That means:

- no active-state mutation
- no install mutation
- no wrapper writes
- no runtime process control

This separation is mandatory if 2.x is going to support truthful dry runs, inspect modes, and safe apply behavior.

## Apply Versus Export-Only

The flow supports both, but they diverge late:

- export-only usually stops after Step 8 and Step 10
- apply continues through Step 9 and then Step 10

Both flows must still produce an explicit target plan and artifact plan.
Export-only is not an excuse to skip planning.

## Carried Forward From 1.x

2.x keeps these successful ideas from 1.x:

- deterministic generation
- explicit runtime intent
- explicit artifact contracts
- trustworthy apply and repair philosophy

It departs from 1.x here:

- no raw profile to backend shortcuts
- no backend owning semantic interpretation
- no hidden degradation after emission begins

