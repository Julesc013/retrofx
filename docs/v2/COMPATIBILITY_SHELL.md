# RetroFX 2.x Compatibility Shell

RetroFX 2.x must coexist with RetroFX 1.x during the transition.
There is no flag day rewrite.

This document defines the compatibility shell that future prompts must respect.

## Current Truth

Right now:

- `./scripts/retrofx` is the real working CLI
- the shell implementation under `scripts/`, `backends/`, and `templates/` is 1.x-owned
- `v2/` is an internal scaffold for the future platform
- `docs/v2/` defines the 2.x truth, but the 2.x engine does not exist yet

No prompt should blur those facts.

## What Remains 1.x-Owned For Now

Until a later migration phase explicitly changes it, 1.x owns:

- current top-level CLI behavior
- apply, off, status, doctor, self-check, and repair
- current install and uninstall behavior
- the stable X11 plus `picom` plus GLX path
- current TTY and `tuigreet` shell backends
- current runtime state handling under `active/` and `state/`
- the existing 1.x profile loader and pack layout

## What 2.x May Implement Safely Now

2.x may implement these without interfering with the stable line:

- schema and validation primitives
- normalized and resolved profile planning
- target compiler interfaces
- non-user-facing target adapters
- pack manifests and pack metadata
- compatibility import and migration helpers
- internal tests under `v2/tests/`

2.x may not quietly take ownership of live user workflows until a later prompt explicitly covers that transition.

## Compatibility Shell Strategy

The compatibility shell is the boundary layer between:

- stable 1.x behavior
- the future 2.x engine
- migration tooling that converts or bridges between them

Its goals are:

- let 1.x stay stable
- let 2.x mature incrementally
- support migration without a repository-wide rewrite
- prevent experimental 2.x code from leaking into the stable path by accident

## Delegation Model For The Future Top-Level Command

This is a planned strategy, not something implemented in TWO-03.

### Phase 0: Current State

- `retrofx` remains 1.x-only in practice
- `v2/` is internal and non-user-facing

### Phase 1: Explicit Internal 2.x Entrypoints

- add non-default developer or test entrypoints for 2.x only when the schema and planner exist
- do not wire them into the default `retrofx` UX yet

### Phase 2: Dispatcher Layer

At a later stage, the top-level command may delegate explicitly:

- legacy 1.x lifecycle commands to the 1.x engine
- new 2.x schema or planning commands to the 2.x engine
- migration subcommands to the compatibility layer

Examples of future delegation patterns:

- `retrofx legacy apply ...` -> 1.x implementation
- `retrofx v2 inspect-profile ...` -> 2.x planner
- `retrofx migrate profile ...` -> compatibility tooling

The exact command surface is deferred.
The important rule is that delegation must be explicit and safe.

### Phase 3: Default Switchover Only After Parity

The default top-level path should not switch to 2.x until:

- the 2.x safety model exists
- repair and rollback semantics are trustworthy
- at least the first-class target matrix is implemented truthfully
- migration and fallback paths are documented

## No Flag Day Migration

Migration should happen incrementally:

1. keep 1.x stable
2. build 2.x planner and adapters under `v2/`
3. add compatibility import and migration helpers
4. expose new 2.x features behind explicit paths
5. only consider default delegation changes after real capability and lifecycle parity exist

That means future prompts should prefer bridges and adapters over wholesale replacement.

## Rules For Future Prompts

- Do not thread unfinished 2.x behavior through `scripts/retrofx` unless the prompt is explicitly about dispatcher work.
- Do not make 1.x lifecycle commands depend on half-built `v2/` modules.
- Do not put migration helpers in the 1.x shell tree when they are really 2.x compatibility work.
- Do not route user-facing commands to 2.x merely because the code exists; route only when the product contract is ready.
- Keep the compatibility layer thin: dispatch, import, upgrade, and bridge logic belong there, not core planning or target emission logic.

