# RetroFX 2.x Implementation Sequence

This document defines the recommended implementation order after the TWO-03 scaffold.
It is meant to keep future prompts focused and prevent premature breadth.

## Current Progress

Status after TWO-08:

- Stage 1 now has an experimental implementation foothold in `v2/core/validation/`, `v2/core/load.py`, and `v2/tests/`
- the pre-capability-filtering part of Stage 2 now has an experimental implementation foothold in `v2/core/normalization/` and `v2/core/resolution/`
- Stage 3 now has a first lightweight implemented adapter interface under `v2/targets/interfaces/`
- Stage 4 has started narrowly with terminal/TUI target compilers under `v2/targets/terminal/`
- capability filtering, artifact planning, and session orchestration remain unimplemented

## Stage 1: Schema And Validation Primitives

Objective:

- implement the 2.x schema contracts in `v2/schema/`
- add structural parsing support and validation primitives
- make the profile language machine-checkable without compiling targets yet

Dependencies:

- [PROFILE_SCHEMA.md](PROFILE_SCHEMA.md)
- [TOKEN_CATALOG.md](TOKEN_CATALOG.md)
- [VALIDATION_RULES.md](VALIDATION_RULES.md)
- [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md)

What not to do yet:

- no target compilers
- no session apply logic
- no dispatcher changes

## Stage 2: Normalized And Resolved Profile Pipeline

Objective:

- implement normalized profile creation in `v2/core/`
- implement resolved semantic model creation
- implement capability-filtered resolved profile planning
- define artifact-plan data structures

Dependencies:

- Stage 1 schema and validation primitives
- [RESOLVED_MODEL.md](RESOLVED_MODEL.md)
- [CAPABILITY_MODEL.md](CAPABILITY_MODEL.md)

What not to do yet:

- no real backend emission
- no live apply behavior
- no broad compatibility shim work

## Stage 3: Target Compiler Interfaces

Objective:

- define target adapter interfaces in `v2/targets/`
- define how adapters consume the resolved profile
- define common artifact and capability reporting contracts

Dependencies:

- Stage 2 resolved-profile pipeline
- [TARGET_MATRIX.md](TARGET_MATRIX.md)
- [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md)

What not to do yet:

- no mass implementation of every target
- no session orchestration takeover
- no DE-wide promises

## Stage 4: Terminal And TUI Targets

Objective:

- implement first practical target adapters for terminals, TTY, `tuigreet`, and TUI exports
- prove the schema-to-artifact flow on deterministic targets first

Dependencies:

- Stage 3 adapter interfaces
- resolved ANSI, typography, and semantic palette planning from Stage 2

What not to do yet:

- no broad WM or DE orchestration
- no default CLI switchover
- no compositor-dependent behavior as the baseline path

## Stage 5: X11 Render Integration

Objective:

- implement the first render-capable path under `v2/render/` and `v2/targets/`
- connect resolved render policy to truthful X11-capable adapters

Dependencies:

- Stage 3 adapter interfaces
- Stage 4 deterministic target flow
- render-policy contracts from [PROFILE_SCHEMA.md](PROFILE_SCHEMA.md)

What not to do yet:

- no universal Wayland post-processing claims
- no deep session takeover
- no parity claims before recovery and orchestration exist

## Stage 6: Session Orchestration

Objective:

- implement apply, export, off, install, and repair orchestration under `v2/session/`
- add environment detection and scoped runtime ownership
- make the 2.x safety model real

Dependencies:

- Stages 2 through 5
- artifact plans and target outputs that session can reason about

What not to do yet:

- no top-level `retrofx` delegation by default
- no system-wide mutation by default
- no unsupported-target hand-waving

## Stage 7: Additional WM, Wayland, And DE Targets

Objective:

- add secondary adapters for WM, Wayland-era, launcher, notification, and toolkit targets
- expand the matrix carefully without weakening capability truth

Dependencies:

- stable adapter interfaces
- stable session orchestration for first-class targets

What not to do yet:

- no GNOME or Plasma "full support" claims without explicit capability paths
- no backfilling every target in one prompt
- no target-specific hacks leaking into core semantics

## Stage 8: Pack System

Objective:

- implement curated pack manifests, family defaults, pack-local assets, and preview metadata in `v2/packs/`
- make packs first-class data products in the new architecture

Dependencies:

- stable schema contracts
- stable resolved-model pipeline
- enough target coverage to make packs meaningful

What not to do yet:

- no arbitrary executable extension system
- no hidden pack logic bypassing validation
- no marketplace-style scope creep

## Stage 9: Compatibility And Migration Tooling

Objective:

- implement 1.x import, upgrade, and dispatch helpers under `v2/compat/`
- support explicit coexistence paths between the legacy shell and the new engine
- make profile migration practical without a flag day rewrite

Dependencies:

- usable 2.x schema
- usable resolved-profile planner
- enough target and session functionality to justify migration

What not to do yet:

- no forced migration for 1.x users
- no silent command rerouting
- no removal of the legacy engine before explicit deprecation planning

## Sequencing Rule

If a future prompt tries to jump ahead, use this test:

- does the earlier stage contract already exist and stay stable enough for later work

If the answer is no, the prompt should return to the earlier stage instead of expanding outward.
