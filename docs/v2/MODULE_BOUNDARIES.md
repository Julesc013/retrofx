# RetroFX 2.x Module Boundaries

This document defines hard boundaries for the 2.x scaffold.
These are rules, not suggestions.

## Hard Rules

1. No target compiler reads raw profile TOML directly.
2. The normalized profile and resolved profile pipeline lives before target emission.
3. Capability filtering occurs before target emission.
4. The resolved profile is the only source of truth for target compilers.
5. No render module decides session policy.
6. No session module invents semantic tokens or color derivation rules.
7. No theme module emits backend-specific files directly except through target interfaces.
8. No target compiler mutates the live environment directly; it emits artifacts and target-specific plans.
9. Only session orchestration owns live apply, off, install, and repair behavior.
10. The compatibility layer may call into 2.x modules, but core 2.x modules must not depend on `compat/`.
11. Packs are data inputs, not hidden imperative logic.
12. 1.x shell code is not treated as a utility library for 2.x core planning.

## Module Ownership

| Module | Owns | Must Not Own |
| --- | --- | --- |
| `v2/core/` | load orchestration, validation orchestration, normalized profile creation, resolved semantic model creation, capability filtering, artifact planning, high-level compile or apply planning | target file emission, backend-specific shell hacks, direct compositor logic |
| `v2/schema/` | schema contracts, validation helpers, migration maps, token catalog support, model definitions | runtime apply logic, target emission, environment mutation |
| `v2/theme/` | semantic theme resolution, typography policy, icon and cursor policy, target-agnostic theme mapping helpers | shader generation, session startup behavior, live apply logic |
| `v2/render/` | quantization policy, palette transforms, display transforms, effect policy, render-capable planning helpers | generic profile parsing, WM or DE session orchestration, unrelated UI theme logic |
| `v2/session/` | environment detection, apply or off orchestration, install and repair lifecycle, login and session integration policy | semantic token definitions, low-level shader code, raw target file rendering |
| `v2/targets/` | target adapters, backend-specific emission, adapter validation, concrete artifact generation | raw profile parsing, semantic invention, live environment mutation |
| `v2/packs/` | pack manifests, family definitions, pack-local assets, curated pack metadata | apply logic, planner logic, direct runtime behavior |
| `v2/compat/` | legacy bridges, migration helpers, profile upgrade tooling, future dispatch shims | core semantic truth, target planning ownership, new feature logic that belongs in core modules |
| `v2/tests/` | 2.x-only test fixtures and coverage for schema, planning, adapters, and compatibility shims | 1.x stable-line regression ownership |

## Allowed Dependencies

Read this section as `consumer -> allowed dependency`.

```text
theme   -> schema
render  -> schema
core    -> schema, theme, render, packs
targets -> schema, core
session -> schema, core, targets
compat  -> schema, core, session
tests   -> any v2 module
```

Interpretation:

- `schema/` is upstream of every implementation module that needs shared contracts.
- `packs/` is primarily data; core planning consumes it, but packs do not become an execution layer.
- `theme/` and `render/` are semantic engines that feed planning; they do not own orchestration.
- `core/` is the planner center of gravity.
- `targets/` compiles what `core/` resolved.
- `session/` applies or exports what `targets/` emitted.
- `compat/` sits at the outer edge and bridges old and new worlds.
- direct `targets -> theme` or `targets -> render` dependencies should be avoided unless a later prompt introduces a deliberate shared helper surface and updates this document.

## Boundary Laws By Concern

### Parsing And Validation

- Raw profile loading and normalization entrypoints belong in `v2/core/` using contracts from `v2/schema/`.
- Validation rules are defined in `v2/schema/` and orchestrated by `v2/core/`.
- A target adapter must never decide that a broken raw profile is "close enough" to parse locally.

### Semantic Resolution

- Token derivation, defaults, and resolved semantic decisions belong to the core pipeline.
- Theme and render helpers may participate in semantic resolution, but they do so under core orchestration.
- Session modules do not reinterpret profile meaning.

### Target Emission

- Target-specific config syntax belongs in `v2/targets/`.
- Shared theme or render helper code may be used by targets, but target emission ownership stays in `v2/targets/`.
- No target adapter may bypass the resolved profile and reach back into raw authored data.

### Session Application

- Writing active state, install state, wrapper state, or repair state belongs to `v2/session/`.
- A target adapter may describe what files it emitted, but it does not decide when or how they become live.
- Session logic may select among compiled target plans, but it does not alter semantic profile meaning.

### Compatibility

- Legacy profile import, profile upgrade, and dispatch shims belong in `v2/compat/`.
- Compatibility code may adapt 1.x inputs into 2.x schema or route commands to legacy implementations.
- Compatibility code must not become a second planner or a dumping ground for unfinished architecture.

## Rules For Later Prompts

- If a change adds target-specific syntax handling, it probably belongs in `v2/targets/`.
- If a change adds semantic token derivation or resolved-model planning, it probably belongs in `v2/core/`, `v2/theme/`, or `v2/render/`.
- If a change touches live session behavior, it probably belongs in `v2/session/`.
- If a change is primarily about legacy coexistence or profile upgrade, it belongs in `v2/compat/`.
- If a proposed change needs to violate these rules, the prompt should say so explicitly and update this document rather than silently crossing the boundary.
