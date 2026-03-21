# RetroFX 2.x Target Compiler Contract

This document defines the generic contract for 2.x target compilers and adapters.

The central rule is non-negotiable:

- target compilers consume the resolved profile, the capability-filtered target plan, and artifact-planning context
- target compilers do not consume raw profile TOML directly

If a compiler reads raw authored profile text, it is bypassing the 2.x engine.

## Current Implementation Status

TWO-09, TWO-10, TWO-12, and TWO-17 implement the first narrow subset of this contract under `v2/targets/terminal/`, `v2/targets/wm/`, `v2/targets/toolkit/`, and `v2/targets/x11/`.

Current truth:

- implemented compilers consume the resolved profile only
- they emit deterministic terminal, TUI, WM, typography, display-policy, and bounded X11 render artifacts into an explicit dev output root
- they run only in explicit dev export mode
- the TWO-17 X11 family additionally supports an explicit dev-only live probe path, but that probe still sits above the target compiler layer and does not make target compilers own session mutation

Still not implemented:

- capability-filtered target plan consumption
- artifact-plan consumption
- session apply or install ownership

That means the current implementation proves the resolved-model-to-artifact path without pretending the full target contract already exists.

## What A Target Compiler Is

A target compiler or adapter is the module responsible for turning resolved semantic intent into target-specific artifacts for one target family or one concrete target.

Examples:

- `kitty` theme emitter
- `tty` palette emitter
- `picom` config emitter
- `i3` config emitter
- future GTK export emitter

It is not responsible for deciding overall product policy.

## Inputs

Every target compiler should conceptually receive:

1. resolved profile
2. capability-filtered target plan entry or entries
3. artifact-planning context
4. execution mode
5. optional target-specific settings

### 1. Resolved Profile

This is the semantic source of truth:

- concrete tokens
- resolved typography and render policy
- resolved session policy
- resolved semantic palettes

### 2. Capability-Filtered Target Plan

This tells the compiler:

- whether the target is `apply`, `export-only`, `degraded`, or skipped
- which capabilities were satisfied
- which features degraded
- what runtime requirements apply

### 3. Artifact-Planning Context

This tells the compiler:

- which artifacts are required
- which are optional
- which are export-only
- which install assets or manifest records must be reported

### 4. Execution Mode

This determines allowed side effects:

- `compile-only`
- `export-only`
- `apply-now`
- `install-for-session`
- `install-as-default`

### 5. Target-Specific Settings

Only narrowly scoped, adapter-specific settings belong here.
They are not a substitute for raw profile parsing.

Examples:

- output path override
- install root override
- selected file naming strategy where the plan already allows it

## Outputs

A target compiler may return:

- emitted artifacts
- staged runtime actions
- install assets
- validation results
- warnings and degradation notes
- capability rejections

### Emitted Artifacts

These are the actual target files or fragments produced.

### Runtime Apply Actions

Only for targets that truthfully support apply behavior.
These must be explicit and scoped.

### Install Assets

Assets produced for installed workflows, such as managed config files or install-owned fragments.

### Warnings And Degradation Notes

Compilers must report when:

- tokens are unsupported
- features degraded deterministically
- optional outputs were skipped

### Capability Rejections

If a target-plan entry is not truthful to emit, the compiler should refuse and surface a structured failure instead of inventing behavior.

## Responsibilities

Target compilers are responsible for:

- mapping semantic tokens to target-specific constructs
- emitting deterministic files, fragments, or scripts
- declaring which target artifacts are required versus optional
- preserving reported degradation decisions
- avoiding mutation of unrelated targets
- reporting unsupported tokens cleanly
- returning enough data for manifest and lifecycle recording

## Non-Responsibilities

Target compilers are not responsible for:

- raw schema parsing
- global environment detection
- target selection policy
- capability intersection policy
- cross-target orchestration
- user prompting
- session policy invention
- semantic token derivation outside their declared target rules

## Side-Effect Policy

Some targets are:

- compile-only
- export-only
- apply-capable
- install-capable

The compiler must not assume which one it is from target name alone.
It must use the target plan and execution mode.

### Rules

- export-only targets may emit artifacts but must not claim runtime ownership
- apply-capable targets may request scoped runtime actions only when the target plan allows it
- install-capable targets may emit install assets only when install mode is selected
- a compiler must never perform undeclared side effects "because the file is easy to write"

## Determinism Rule

Given the same resolved profile, target plan, artifact plan, and execution mode, the compiler should produce the same emitted artifacts and the same structured results.

## Relation To 1.x

1.x provides useful precedents:

- `x11-picom` informs the X11 render-capable family
- `tty` informs the console target family
- `tuigreet` informs the login or greet target family
- Xresources and Alacritty exports inform terminal target compilers

But 2.x target compilers are not required to preserve 1.x directory layout or backend script style.
They carry forward concepts, not implementation debt.
