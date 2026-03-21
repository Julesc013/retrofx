# RetroFX 2.x Roadmap

This roadmap is phased on purpose.
Each phase should narrow uncertainty before more implementation surface is added.

## Current Progress

Status after TWO-11:

- 2.0-C has an experimental implementation foothold for load, validate, normalize, and resolve in `v2/core/`
- 2.0-D has started with the first terminal/TUI compiler family under `v2/targets/terminal/`
- 2.0-D now also has the first WM theme/config compiler family under `v2/targets/wm/`
- 2.0-E has begun narrowly with non-destructive environment detection and capability-aware planning preview under `v2/session/`
- live session orchestration and broader target families remain future phases

## 2.0-A Product And Spec Design

Purpose:

- define the 2.x product
- define scope, non-goals, terminology, capability semantics, and architectural principles
- separate 2.x redesign work from 1.x maintenance

Prerequisites:

- current 1.x product truth and maintenance boundaries

Explicitly does not do:

- engine implementation
- new target compilers
- runtime behavior changes on the 1.x line

## 2.0-B Tokenized Profile Schema

Purpose:

- define the semantic profile schema
- define tokens, composition rules, style families, and resolved profile structure
- define which profile intents are target-agnostic and which are adapter-scoped

Prerequisites:

- 2.0-A design docs

Explicitly does not do:

- full compiler engine
- broad adapter implementation
- session orchestration logic

## 2.0-C Core Compiler Engine

Purpose:

- implement parsing, validation, normalization, token resolution, capability intersection, and artifact planning
- define machine-readable planner outputs and logging structure

Prerequisites:

- 2.0-B schema and resolved profile contract

Explicitly does not do:

- full session lifecycle
- complete target coverage
- deep WM or DE integration

## 2.0-D Target Compilers For Terminal, TUI, X11, And WM Basics

Purpose:

- implement first-wave adapters for terminal, TUI, TTY, `tuigreet`, core X11 outputs, and basic WM targets
- establish the first practical target matrix with truthful support classes

Prerequisites:

- 2.0-C planner and artifact model

Explicitly does not do:

- broad DE orchestration
- universal Wayland effect paths
- every secondary adapter in the matrix

Current implementation note:

- TWO-09 starts this phase narrowly with export-oriented terminal/TUI compilers
- TWO-10 extends that same export-oriented slice into WM theme/config compilers for `i3`, `sway`, and `waybar`
- X11, TTY, `tuigreet`, install/apply, and session orchestration are still future work

## 2.0-E Session Orchestration Layer

Purpose:

- implement apply, export, install, off, status, and repair around the new architecture
- define environment scoping and trustworthy recovery for supported targets

Prerequisites:

- 2.0-D target compilers for the first-class baseline

Explicitly does not do:

- deep GNOME or Plasma ownership
- global config mutation by default
- speculative installer breadth

Current implementation note:

- TWO-11 starts this phase with environment detection and preview planning only
- live apply, install, off, repair, and integration hooks are still future work

## 2.0-F Richer Theming And Display Policy

Purpose:

- add secondary theming outputs such as GTK, Qt, cursor, icon, and richer typography policy
- add stronger display-policy expression where explicit capability paths exist

Prerequisites:

- stable core lifecycle from 2.0-E

Explicitly does not do:

- pretend unsupported DE stacks are now fully orchestrated
- bypass the capability model for "close enough" targets
- over-centralize toolkit-specific logic in the core

## 2.0-G Packaging And Ecosystem

Purpose:

- mature packs, previews, metadata, migration aids, documentation, and distribution workflows
- strengthen testing and compatibility reporting around the supported matrix

Prerequisites:

- a stable first-class implementation baseline

Explicitly does not do:

- reopen architectural foundations already settled in earlier phases
- backfill every conceivable adapter before the ecosystem model is coherent

## Roadmap Discipline

Later phases should not quietly pull foundational work forward.
If a prompt requires rethinking product truth, capability semantics, or architecture boundaries, it belongs back in an earlier phase rather than being smuggled into implementation work.
