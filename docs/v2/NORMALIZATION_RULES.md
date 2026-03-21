# RetroFX 2.x Normalization Rules

Normalization is the step that converts validated authored input into the canonical target-agnostic profile shape.
It sits after schema validation and before semantic resolution or capability filtering.

## What Normalization Means

Normalization means turning flexible author input into one deterministic internal representation.

It includes:

- default filling
- alias resolution
- canonical enum and scalar conversion
- list and map normalization
- asset path normalization
- deterministic placeholder structures for omitted optional groups
- future composition flattening when that feature exists

It does not mean environment-specific decision making.

## What Gets Normalized

### Metadata

- fill omitted descriptive fields with empty defaults
- normalize `identity.id`
- canonicalize tags and ordered lists
- canonicalize `family` and `strictness` enum values

### Color And Token Groups

- ensure semantic token groups have canonical keys
- canonicalize color literal form
- normalize partial ANSI override sets into stable slot maps
- compute default ANSI mappings when explicit overrides are absent

### Typography

- normalize scalar versus list forms where supported
- canonicalize AA and hinting enums
- normalize empty or omitted fallback sets to explicit empty lists

### Render Policy

- fill mode defaults
- normalize palette source references into canonical reference strings
- canonicalize numeric ranges and booleans
- fill omitted effect and display defaults

### Session Policy

- canonicalize requested target classes
- normalize `apply_mode` and `persistence`
- normalize empty or duplicate target entries

### Paths And Assets

- resolve relative asset paths against profile source location
- canonicalize asset-reference namespaces
- preserve the distinction between author intent and absolute machine path

### Future Composition

When composition exists later, normalization should:

- resolve includes or base references into a deterministic flattened form
- preserve provenance metadata where useful
- reject ambiguous or cyclic composition graphs

Composition flattening is a normalization concern, not a target-adapter concern.

## What Normalization Must Not Do

- no environment-specific degradation
- no adapter matching
- no backend-specific file generation
- no live session detection
- no apply or install side effects
- no runtime validation

Normalization must stay target-agnostic.

## What Definitely Does Not Happen Yet

These belong to later stages:

- semantic derivation driven by current environment
- target-plan creation
- artifact planning
- emission
- apply, off, repair, or self-check

## Errors Versus Warnings At Normalization Time

### Errors

Normalization should fail when input cannot be converted into one deterministic canonical form.

Examples:

- invalid enum values
- impossible path references
- duplicate canonical keys after alias collapse
- malformed color literals
- structurally contradictory session policy
- cyclic or unresolved composition references once composition exists

### Warnings

Normalization may warn when input is valid but incomplete or non-ideal.

Examples:

- partial ANSI overrides that rely on derived defaults
- unknown family value that falls back to generic defaults
- deprecated alias forms once aliases exist

Warnings at normalization time should not depend on the current environment.

## Canonical Normalization Outputs

The normalization stage should produce:

- normalized profile object
- normalization warnings
- provenance or source-location metadata where useful

The normalized profile should be safe for later semantic resolution without re-reading the raw authored text.

## Why Target Compilers Must Not See Pre-Normalized Input

If target compilers receive raw input:

- each adapter may apply defaults differently
- each adapter may resolve paths differently
- capability decisions become inconsistent
- the engine loses determinism

That is precisely what the 2.x core pipeline is designed to prevent.

## Carried Forward And Changed

From 1.x, 2.x keeps:

- strict validation discipline
- deterministic generation expectations
- conservative handling of ambiguous input

2.x changes:

- normalization becomes a first-class pipeline stage
- semantic defaults and structural canonicalization happen before any adapter sees the profile
- raw profile text stops being the operational source of truth once normalization succeeds

