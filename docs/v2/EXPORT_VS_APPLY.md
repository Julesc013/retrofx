# RetroFX 2.x Export Versus Apply

RetroFX 2.x must treat compile, export, apply, and install as distinct modes.
This document defines those modes at the target layer.

## Why This Distinction Matters

2.x cannot stay sane if every target is assumed to be "applyable."
Some targets:

- can only export
- can apply only in a scoped session
- can install defaults but not mutate the current session

The engine must represent those truths explicitly.

## Mode Definitions

### `compile-only`

Purpose:

- produce a target plan or staged target outputs without claiming user-facing export or runtime ownership

Allowed side effects:

- none beyond temporary staging in internal tooling contexts

Typical families:

- any family during dry-run or inspect workflows

Expected artifacts:

- planned artifacts
- optionally staged internal outputs

### `export-only`

Purpose:

- emit standalone artifacts without claiming runtime ownership

Allowed side effects:

- writing explicit export files only

Typical families:

- terminal and TUI
- toolkit exports
- WM fragments
- selected X11 artifacts for inspection

Expected artifacts:

- config files
- snippets
- palette exports

### `apply-now`

Purpose:

- emit artifacts and make scoped runtime changes for the current session or current environment

Allowed side effects:

- scoped runtime writes
- scoped process or session actions explicitly owned by the plan

Typical families:

- TTY
- selected X11 render targets
- limited WM or terminal targets where current-session ownership is truthful

Expected artifacts:

- required runtime artifacts
- runtime metadata
- optional convenience exports where planned

### `install-for-session`

Purpose:

- install managed assets for later explicit session usage without necessarily changing the current live session immediately

Allowed side effects:

- writing install-owned managed assets
- writing install manifests

Typical families:

- X11 helper outputs
- WM fragments
- toolkit exports
- session helper family

Expected artifacts:

- install assets
- manifest records
- managed config fragments

### `install-as-default`

Purpose:

- install managed defaults that become the preferred RetroFX-owned configuration state for future sessions

Allowed side effects:

- writing install-owned assets
- updating install manifests or default-owned records

Typical families:

- selected terminal and WM targets
- session helper family
- limited toolkit targets where install ownership is truthful

Expected artifacts:

- install assets
- default-owned manifest records
- maybe export copies if planned

## Family Support Expectations

| Family | compile-only | export-only | apply-now | install-for-session | install-as-default |
| --- | --- | --- | --- | --- | --- |
| TTY | yes | yes | yes | limited | limited |
| Tuigreet/Login | yes | yes | limited | yes | limited |
| Terminal/TUI | yes | yes | target-dependent | yes | yes |
| X11 render/compositor | yes | yes | yes when supported | yes | limited |
| WM config | yes | yes | limited or adapter-dependent | yes | yes |
| Toolkit/Desktop export | yes | yes | rarely truthful in early 2.x | limited | limited |
| Session/helper | yes | limited | limited | yes | yes |

## How This Differs From Session Orchestration

These modes describe what the target layer is allowed to do.
Session orchestration is the higher-level system that decides:

- whether those modes are appropriate now
- how multiple target actions combine
- how rollback, repair, and lifecycle state are managed

In short:

- targets declare and execute bounded operations
- session orchestrates whole-configuration ownership

## Carry-Forward From 1.x

1.x already distinguished between:

- active runtime outputs
- export-only outputs
- install assets

2.x formalizes that distinction so every target family follows the same rule instead of inheriting it informally from CLI paths.

