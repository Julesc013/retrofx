# RetroFX 2.x Resolved Model

The resolved model is the object that future 2.x compilers should consume.
It is not authored directly.

This document defines the difference between raw input, normalized profile, resolved semantic model, and the final resolved profile handed to target compilers.

TWO-08 implements the first experimental resolved-profile scaffold in `v2/core/resolution/`.
That implementation produces the pre-capability-filtering semantic model plus explicit placeholder sections for capability context, target planning, and artifact planning.
It is intentionally incomplete and dev-only.

## Layer Boundaries

| Layer | Meaning | Still Missing At This Stage |
| --- | --- | --- |
| Raw profile input | The authored TOML file. | Defaults, derivation, canonical ordering, target plan. |
| Normalized profile | Canonical schema object after validation and defaults. | Concrete derived semantic values and capability decisions. |
| Resolved semantic model | All semantic tokens and policies are concretized. | Target adapter binding and artifact planning. |
| Resolved profile | Resolved semantic model plus capability-filtered target plan and artifact plan. | Backend-specific file emission only. |

## What Is Resolved Before Capability Filtering

The resolved semantic model must exist before environment-specific planning begins.
It contains the canonical intent of the profile independent of any particular adapter.

### Pre-Filter Resolved Fields

- canonical metadata
- family and strictness defaults outcome
- concrete semantic color tokens
- concrete terminal ANSI set
- concrete TTY ANSI set
- resolved typography roles
- resolved antialiasing and hinting policy
- resolved render mode and render policy
- resolved chrome hints
- resolved session policy
- requested target classes

At this point the model is concrete enough to say what the profile means, but not yet concrete enough to say which adapters will emit it.

## What Is Resolved After Capability Filtering

Capability filtering binds the resolved semantic model to an environment-aware plan.
The resulting resolved profile is the direct compiler input.

### Post-Filter Fields

- matched adapter candidates
- capability-filtered target plan
- degraded decisions
- export-only decisions
- unsupported request records
- compositor requirement
- required artifact plan
- optional artifact plan
- lifecycle notes for apply, export, install, off, and repair

## Canonical Resolved Profile Shape

The resolved profile should contain at least these sections.

### 1. `identity`

Canonical metadata copied from the normalized profile:

- `id`
- `name`
- `description`
- `tags`
- `author`
- `license`
- `family`
- `strictness`

### 2. `semantics.color`

- `semantic`
  - fully concrete values for `bg0`, `bg1`, `bg2`, `fg0`, `fg1`, `fg2`, accents, borders, selection, glow, and cursor tokens
- `terminal_ansi`
  - concrete slots `0..15`
- `tty_ansi`
  - concrete slots `0..15`
- `mapping_notes`
  - how ANSI derivation was chosen, such as semantic mapping, monochrome luminance mapping, or explicit overrides

### 3. `semantics.typography`

- `console_font`
- `terminal_primary`
- `terminal_fallbacks`
- `ui_sans`
- `ui_mono`
- `icon_font`
- `emoji_policy`
- `aa`
  - `antialias`
  - `subpixel`
  - `hinting`

### 4. `semantics.render`

- `mode`
- `quantization`
  - `bands`
- `palette`
  - `kind`
  - `size`
  - `source`
- `effects`
  - `blur`
  - `dither`
  - `scanlines`
  - `flicker`
  - `vignette`
  - `hotcore`
- `display`
  - `gamma`
  - `contrast`
  - `temperature`
  - `black_lift`
  - `blue_light_reduction`
  - `tint_bias`

### 5. `semantics.chrome`

- `gaps`
- `bar_style`
- `launcher_style`
- `notification_style`
- `icon_theme`
- `cursor_theme`

### 6. `semantics.session`

- `requested_targets`
- `apply_mode`
- `persistence`

This section should still be target-class oriented.
It describes desired scope, not specific emitted files.

### 7. `capability_context`

This is the planner input describing the environment or user-selected destination:

- selected environment facts
- selected backend preference, if any
- matched adapter candidates
- capability declarations considered during planning

### 8. `target_plan`

`target_plan` is a list of concrete plan entries.
Each entry should contain:

- `target_class`
- `target_name`
- `adapter_id`
- `status_class`
  - `full`
  - `partial`
  - `export-only`
  - `unsupported`
- `apply_mode`
  - `apply`
  - `export-only`
  - `skip`
- `capabilities_satisfied`
- `capabilities_degraded`
- `capabilities_unavailable`
- `degraded_reasons`
- `export_only_reasons`
- `compositor_requirement`
  - `required`
  - `optional`
  - `none`

### 9. `artifact_plan`

This section is split into:

- `required`
- `optional`

Each artifact plan entry should contain:

- artifact id
- target association
- artifact class
- lifecycle role
- reason it exists

Examples of artifact classes:

- required runtime artifact
- required export artifact
- session fragment
- preview or metadata artifact
- optional convenience export

### 10. `decisions`

The resolved profile should record:

- degradations
- export-only outcomes
- ignored token warnings
- unsupported target requests
- deterministic fallbacks applied

## Compositor Requirement

The resolved profile must record compositor requirement explicitly.
Use `required`, `optional`, or `none`, not an implied boolean.

- `required` means the selected target plan depends on a compositor or compositor-like host.
- `optional` means some adapters can use one but the plan remains valid without it.
- `none` means the plan does not require compositor behavior.

This can be recorded both globally and per target-plan entry.
The global value should be the strongest requirement across the active plan.

## What Remains Backend-Specific

Even after resolution, these items belong to adapters and emission logic:

- concrete file names and template syntax
- WM-specific config keys
- toolkit-specific variable names
- shader source generation details
- exact launcher or notification config syntax
- install paths and wrapper scripts
- runtime process control

The resolved profile should never contain backend-specific syntax as authored truth.

## Why This Separation Matters

Future implementation prompts should be able to build:

- validators against the normalized profile contract
- planners against the resolved profile contract
- target compilers against the target-plan and artifact-plan contract

without reinterpreting authored input for every backend.
