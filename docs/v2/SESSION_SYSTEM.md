# RetroFX 2.x Session System

RetroFX 2.x session orchestration is the layer that turns planned outputs into explicit lifecycle behavior.

Its defining principle is:

- core planning decides what should happen
- target adapters emit what can be emitted
- session orchestration decides what side effects, installations, bindings, or runtime changes are truthful in a specific environment

Session orchestration is not "whatever happens after compile."
It is a first-class subsystem with explicit ownership and safety rules.

## Current Implementation Status

As of TWO-21:

- `v2/session/environment/` implements best-effort environment detection for the dev scaffold
- `v2/session/planning/` implements non-destructive capability-aware planning against the resolved profile and implemented target families
- `v2/core/dev/plan-session` exposes that planning layer as a dev-only preview surface
- planner output now includes structured display-policy interpretation in addition to target-family decisions
- planner output now also includes explicit `x11_render` capability summaries for the bounded TWO-17 X11 family
- `v2/session/dev/preview_x11_render.py` now stages real X11 render artifacts and can run an explicit short-lived `picom` probe without touching 1.x state
- `v2/session/install/` now also contains a separate experimental user-local bundle/install slice for `retrofx-v2-dev`
- `v2/session/apply/` now stages bounded 2.x-owned current activations, writes explicit manifests and last-good records, and can clear that active state safely
- `scripts/dev/retrofx-v2` now exposes planning, preview, apply, off, and status through one unified experimental entrypoint
- [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md) now documents the current plan, install, and activation record contracts that the TWO-21 test suite enforces structurally
- session-default install orchestration, broad repair, and login integration execution are still not implemented

## What The Session System Is Responsible For

The session subsystem is responsible for:

- execution-mode selection and sequencing
- current-session apply orchestration
- export-only versus live apply distinction
- install-state ownership
- login or startup integration planning
- environment scoping
- state recording and manifest ownership
- rollback, repair, and recovery boundaries
- lifecycle logging and explainability

In practical terms, the session subsystem is where 2.x decides:

- whether a target plan should stay export-only
- whether emitted artifacts can become live now
- whether install-owned assets should be written
- whether login or session integration hooks are appropriate
- what state records must be written so `off`, `repair`, and `self-check` can be trustworthy later

## What The Session System Is Not Responsible For

The session subsystem is not responsible for:

- raw profile parsing
- normalization or semantic resolution
- theme token design
- render math or shader logic
- target capability declaration
- target-specific config rendering
- inventing new target plans after compilation

It consumes planning truth.
It does not redefine it.

## Inputs

The session subsystem should eventually consume:

- resolved profile
- capability-filtered target plan
- artifact plan
- emitted-artifact reports
- execution mode
- environment model
- install context
- existing lifecycle state where relevant

It must not consume raw authored TOML directly.

## Outputs

The session subsystem should eventually produce:

- apply or export execution records
- install records
- current-state descriptors
- manifest updates
- recovery baselines
- integration-hook records
- warnings about skipped, degraded, or partial lifecycle outcomes

Current TWO-19 truth:

- the implemented planner produces environment records, per-target preview decisions, display-policy interpretation, degradation warnings, and optional preview bundles
- the implemented X11 preview path also writes isolated preview-state metadata under the 2.x output tree
- the implemented apply slice now also writes active-state, activation-manifest, last-good, and event-log records under the isolated `retrofx-v2-dev` state tree
- experimental install-state records still exist separately through the TWO-16 bundle/install helpers, and the apply slice reuses that managed footprint rather than redefining ownership

## Relation To Target Compilation

Target compilation and session orchestration are separate.

Target adapters:

- map resolved intent into backend-specific artifacts
- declare what artifacts exist and what modes they can support
- report degradation or refusal

Session orchestration:

- chooses whether those artifacts remain exported, become active, or become installed
- sequences side effects across multiple targets
- records the lifecycle truth for rollback and repair

A target adapter must never silently decide:

- to activate itself
- to install itself as default
- to mutate unrelated session state

Those are session-layer decisions.

## Relation To Core Planning

Core planning remains upstream.

Core owns:

- normalization
- semantic resolution
- capability filtering
- artifact planning

Session owns:

- execution against a real environment
- lifecycle state updates
- recovery ownership

If a lifecycle action needs to reinterpret profile meaning, the design is wrong.

## Execution Modes

The session subsystem must treat these as distinct lifecycle modes:

- `compile-only`
- `export-only`
- `apply-now`
- `install-for-session`
- `install-as-default`
- `explicit-session-integration`

Those modes are defined in detail in [APPLY_MODES.md](APPLY_MODES.md).

## Environment Scoping

The session subsystem operates inside an explicit environment model.

That model describes:

- session class such as `tty`, `x11`, or `wayland`
- context such as repo-local, installed, current-session, or startup
- runtime facts such as compositor availability or WM identity
- confidence and limits of detection

Environment facts inform lifecycle truth.
They must never be used to invent support the target layer did not claim.

## Safety Model

2.x carries forward the core 1.x safety lesson:

- lifecycle trust comes from explicit state, explicit manifests, and explicit rollback boundaries

That means the session subsystem should eventually own:

- current-state records
- last-good recovery baselines
- install-state records
- degraded fallback decisions
- repair and self-check coordination

No later prompt should push those concerns down into target adapters.

Current TWO-19 implementation note:

- current-state records now live under the isolated `retrofx-v2-dev` state area
- the active staged bundle now lives under the matching user-local data area
- `off` now clears only that 2.x-owned active state plus recorded preview-artifact roots
- 1.x paths remain outside the ownership boundary

## What Later Prompts Should Build Here

Future implementation prompts should build:

- environment-model collection helpers
- execution-mode planners
- session-local apply sequencing
- install-state writers and uninstall planning
- state-descriptor and manifest writers
- recovery and repair coordination
- bounded session-integration helpers

Future implementation prompts should not build:

- raw target compilers
- semantic token resolution
- render algorithms
- theme-token catalogs

## Carry-Forward From 1.x

2.x intentionally carries forward these 1.x ideas:

- explicit manifests
- explicit runtime intent
- explicit degraded behavior
- repo-local versus installed distinction
- repair and self-check as first-class lifecycle operations

2.x intentionally improves on 1.x by making:

- apply, export, and install separate lifecycle modes
- environment scoping more formal
- state and recovery records less ad hoc
- session integration a bounded subsystem instead of wrapper folklore
