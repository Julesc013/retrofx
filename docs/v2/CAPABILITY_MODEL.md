# RetroFX 2.x Capability Model

The capability model is a design law for RetroFX 2.x.
RetroFX does not infer support from optimism, from partial config generation, or from historical accident.

## Core Rule

- environments and backends advertise capabilities
- profiles request intent
- RetroFX intersects requested intent with supported capabilities
- the resulting apply or export plan is explicit and logged

Nothing may silently skip this model.

## Current Implementation Status

As of TWO-13:

- `v2/session/planning/plan.py` implements the first real capability-aware planning slice
- it intersects the resolved profile, detected environment, and currently implemented target families
- the planner now also interprets resolved display policy as `future-render-consumer`, `advisory-export-only`, or `degraded-ignored-live`
- the current planner is still narrow: it reasons only about implemented targets and remains preview-only
- artifact-plan-driven lifecycle execution is still future work

## Capability Categories

RetroFX 2.x capability declarations are grouped by domain.

| Category | Meaning |
| --- | --- |
| `theme` | Ability to express colors, roles, and non-render appearance outputs for a target. |
| `render` | Ability to host runtime or target-level visual transforms such as quantization, scanlines, glow, gamma, temperature, or bias. |
| `session` | Ability to participate in login, startup, wrapper, WM, DE, or compositor-adjacent session orchestration. |
| `typography` | Ability to apply or export font family, fallback, antialiasing, and hinting policy. |
| `palette` | Ability to preserve or map semantic color roles within the target's color model and limits. |
| `install` | Ability to stage and manage files in a RetroFX-owned install footprint. |
| `export` | Ability to emit deterministic standalone artifacts without claiming runtime ownership. |
| `recovery` | Ability to support trustworthy `off`, `repair`, rollback, or equivalent disable and restore flows. |

## Status Classes

Status classes describe the depth of truthful support for a target or environment.

### `full`

The target is explicitly supported for its intended contract.
RetroFX can compile and manage the declared theme, render, session, install, and recovery behaviors that the target is supposed to offer.
`full` does not mean every target supports every category.
It means RetroFX fully supports that target's real contract.

### `partial`

The target is supported, but only for a subset of requested or possible behavior.
A `partial` target may support theme generation and some session policy while omitting render transforms, toolkit integration, or deeper orchestration.
`partial` is still supported, but with explicit limits.

### `export-only`

RetroFX can generate artifacts for the target, but it cannot truthfully claim runtime ownership or full apply or repair semantics there.
This is a valid support class, not a euphemism.
It exists so generated output is useful without pretending that orchestration exists.

### `unsupported`

RetroFX has no truthful adapter path for the requested target or environment.
No config file generation trick should upgrade `unsupported` into a softer label.

## Supported, Degraded, And Export-Only

These terms are used precisely in 2.x:

- `supported` means a target is intentionally part of the 2.x product with a declared capability path.
- `supported` targets may have status class `full` or `partial`.
- `degraded` means the requested profile intent could not be fully realized on the selected target, so the resolved plan is a reduced but still valid supported outcome.
- `export-only` means RetroFX can emit artifacts for the target but does not claim managed apply or session ownership.
- `unsupported` means no truthful target path exists at all.

In other words:

- `supported` describes product intent
- `full`, `partial`, and `export-only` describe support depth
- `degraded` describes the result of capability intersection for a specific apply or export plan

## Capability Intersection

The planner must compute a target plan from three inputs:

1. profile intent
2. selected targets and environment facts
3. adapter capability declarations

The planner then produces:

- capabilities that are satisfied
- capabilities that are degraded
- capabilities that are unavailable
- whether the result is `apply`, `export-only`, or `unsupported`

Current TWO-13 implementation note:

- the implemented planner currently emits `compile-and-export`, `compile-and-apply-preview`, `compile-but-degraded`, and `skipped-unsupported` decisions
- display-policy interpretation is now included as a structured planner output alongside per-target decisions
- that output is meant to prove the architecture, not to claim production lifecycle ownership yet

## Logging And Truthfulness

Every apply or export decision should be explainable in plain language.
At minimum, RetroFX should be able to report:

- requested targets
- detected or selected environment
- matched adapters
- declared capabilities
- degraded intents
- exported-only artifacts
- skipped or unsupported intents

Silent fallback is architectural debt and should be treated as a bug.

## Example

A profile may request:

- terminal palette and typography
- `sway` integration
- scanlines and glow

If the selected environment is `sway`, RetroFX should be able to say:

- terminal and typography outputs are supported
- `sway` session integration is supported at `partial`
- global compositor-style render transforms are degraded or unsupported
- resulting status is `partial`, not `full`

That is the intended 2.x behavior: useful, explicit, and honest.
