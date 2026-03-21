# RetroFX 2.x Core Pipeline

This document defines the future heart of the RetroFX 2.x engine.
It explains how authored profile intent becomes a capability-aware, target-ready plan without collapsing into direct profile-to-backend shortcuts.

## Why The Core Pipeline Exists

RetroFX 1.x succeeded when it was explicit about:

- deterministic generation
- truthful degradation
- explicit artifact contracts
- trustworthy apply, off, and repair behavior

RetroFX 2.x keeps those values, but it changes the internal shape.
No target compiler should read authored profile text and "figure it out" locally.
That would recreate the 1.x coupling problem at a larger scale.

The 2.x core pipeline exists to ensure:

- one interpretation of profile meaning
- one place for defaults and derivation
- one capability-filtered truth before emission
- one explicit artifact plan before side effects begin

## Canonical Pipeline Layers

RetroFX 2.x uses six layers:

1. raw profile input
2. normalized profile
3. resolved profile
4. capability-filtered target plan
5. artifact plan
6. emission and apply

These layers are sequential and intentional.
Later prompts should not collapse them for convenience.

## Layer 1: Raw Profile Input

Raw profile input is what the user authored.
It may contain:

- metadata
- semantic tokens
- render policy
- typography and chrome policy
- session policy
- future composition or inheritance references

Raw input is not safe to compile from directly because it may still contain:

- omitted defaults
- relative paths
- unresolved aliases
- composition references
- partial token groups
- author-facing values that need canonicalization

### Hard Rule

Target compilers must never read raw input directly.
If they do, the engine no longer has one semantic source of truth.

## Layer 2: Normalized Profile

The normalized profile is the target-agnostic output of early validation and canonicalization.
It is the first machine-safe representation of the authored profile.

### Normalization Responsibilities

- validate structure against schema contracts
- fill default values
- canonicalize enums and booleans
- canonicalize lists and maps
- normalize asset references and relative paths
- resolve aliases
- reserve or flatten composition when that feature exists
- compute deterministic fallback structures such as missing ANSI override groups

### What Does Not Happen Here

- no environment-specific degradation
- no adapter matching
- no backend-specific file generation
- no live apply behavior
- no session side effects

### Why This Layer Matters

Normalization removes authoring ambiguity without making capability decisions yet.
It lets the rest of the engine reason over one consistent shape.

## Layer 3: Resolved Profile

The resolved profile is the central 2.x compiler object.
It is built in two forms:

- a resolved semantic model
- a final resolved profile after capability filtering attaches planning data

### Resolved Semantic Model

This is environment-independent intent after semantic resolution.
It contains:

- canonical metadata
- concrete semantic color tokens
- concrete terminal and TTY palette sets
- concrete typography policy
- concrete render policy
- concrete session policy
- concrete chrome hints

### Final Resolved Profile

This extends the resolved semantic model with:

- capability context
- target plan
- artifact plan
- degradation records
- export-only records
- runtime requirements such as compositor need

### Why Resolved Profile Exists

The normalized profile is still about author input shape.
The resolved profile is about what the profile means after derivation.
Target compilers need meaning, not authoring shortcuts.

## Layer 4: Capability-Filtered Target Plan

This layer intersects resolved intent with:

- selected targets
- environment facts
- adapter capability declarations
- session policy constraints

It decides:

- what can be applied as requested
- what must degrade
- what is export-only
- what must be refused or skipped

This is where truthful degradation becomes concrete.

## Layer 5: Artifact Plan

The artifact plan turns the target plan into an explicit inventory of what must exist.
It answers:

- what files or generated outputs are required
- what is runtime-critical
- what is optional
- what is export-only
- what is installation-related
- what manifests and state records must be written later

Artifact planning happens after capability filtering because the required artifact set depends on what the engine will actually support in the selected environment.

## Layer 6: Emission And Apply

This is the first layer where side effects are allowed.

Emission consumes:

- resolved profile
- capability-filtered target plan
- artifact plan

It produces:

- target-specific artifacts
- staged runtime assets
- export artifacts
- session fragments
- manifest and state records

Apply is separate from export-only behavior:

- export-only emits artifacts without claiming runtime ownership
- apply emits artifacts and then performs scoped session or runtime actions

## Core Ownership

The future `v2/core/` module should own:

- load orchestration
- normalization orchestration
- semantic resolution orchestration
- capability filtering orchestration
- artifact planning orchestration
- compile or apply planning

The core should not own:

- target-specific syntax
- direct session mutation
- compositor-specific implementation hacks

## Pipeline Guarantees

Every later implementation prompt should preserve these guarantees:

- one raw input becomes one normalized profile
- one normalized profile becomes one resolved semantic model
- one resolved semantic model becomes one capability-filtered target plan
- one target plan becomes one artifact plan
- side effects begin only after planning is complete

If a design bypasses those guarantees, it is bypassing the 2.x core engine.

