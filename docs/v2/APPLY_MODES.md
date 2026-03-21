# RetroFX 2.x Apply Modes

RetroFX 2.x must treat compile, export, apply, install, and integration as different lifecycle modes.
This document defines those modes from the session-orchestration point of view.

The target layer defines what a given family can support.
The session layer decides which mode is truthful in the current context.

## Current Implementation Status

As of TWO-11:

- `compile-only` and `export-only` now exist as real preview concepts in the dev planner
- `apply-now` exists only as an explicit preview category for selected targets such as `i3`, `sway`, or `xresources` when the environment matches
- no live mode mutates the user session yet

## Summary

| Mode | Intended Use | Allowed Side Effects | Expected Outputs | Must Never Do |
| --- | --- | --- | --- | --- |
| `compile-only` | inspect or dry-run planning | none | plans, diagnostics, optional staged internal reports | write live state, install assets, or integration hooks |
| `export-only` | generate artifacts for manual use | artifact emission only | export files, snippets, palette outputs, reports | claim runtime ownership or live apply |
| `apply-now` | activate supported changes in the current session | scoped session-local side effects | emitted artifacts, active state records, recovery records | silently install defaults or mutate unmanaged startup paths |
| `install-for-session` | prepare managed assets for later explicit session use | install-state writes | install assets, manifests, optional wrappers | claim the profile is active now unless `apply-now` also ran |
| `install-as-default` | make a managed user-local default for future sessions | install-state writes, managed default updates | default-owned assets, install manifests, optional exported copies | claim system-wide ownership or unscoped DE control |
| `explicit-session-integration` | generate or update login/startup integration hooks | managed integration-hook writes | wrappers, launch helpers, login snippets, integration records | silently take over unsupported login managers or global system config |

## 1. `compile-only`

Intended use:

- inspect a profile
- run dry-run planning
- explain degradation before any emission

Allowed side effects:

- none

Expected outputs:

- resolved plan summaries
- target plan summaries
- artifact-plan summaries
- diagnostics and warnings

Must never do:

- write exported files as if they were user outputs
- mutate current-session state
- mutate install manifests

Meaningful participants:

- every target family, because planning exists even when no emission will occur

Current TWO-11 implementation note:

- `v2/core/dev/plan-session` can inspect a profile, detect the environment, and build a compile-oriented preview plan without emitting target artifacts unless preview output is explicitly requested

## 2. `export-only`

Intended use:

- generate artifacts for manual inspection or manual integration
- support terminals, TUIs, WM snippets, toolkit hints, or preview workflows without claiming lifecycle ownership

Allowed side effects:

- writing explicit export artifacts only

Expected outputs:

- exported config files
- snippets
- palettes
- preview-oriented outputs
- export reports

Must never do:

- update active-session state
- write install manifests as if exports were installed assets
- imply that generated exports are live

Meaningful participants:

- terminal and TUI targets
- WM config targets
- toolkit and desktop export targets
- X11 artifacts intended for inspection rather than activation

Current TWO-11 implementation note:

- the implemented dev compiler families and the session planner both remain export-oriented by default

## 3. `apply-now`

Intended use:

- activate supported profile behavior in the current operating context

Allowed side effects:

- artifact emission required for the active plan
- session-local file writes
- scoped runtime process or environment actions that the plan explicitly owns
- current-state and recovery record updates

Expected outputs:

- active artifacts
- apply result records
- current-state descriptors
- last-good or recovery-baseline updates when appropriate

Must never do:

- silently widen scope from current session to installed default
- mutate unmanaged login-manager or DE-global state
- apply targets whose capability result was export-only or unsupported

Meaningful participants:

- TTY targets
- supported X11 render targets
- limited WM or terminal targets when current-session ownership is truthful

Important reminder:

- `apply-now` is capability- and environment-dependent
- a target may support `export-only` and `install-for-session` but not truthful current-session apply

Current TWO-11 implementation note:

- the session planner can mark `i3`, `sway`, or `xresources` as apply-preview candidates when the environment matches and the profile requests `current-session`
- those candidates remain preview-only; no side effects happen yet

## 4. `install-for-session`

Intended use:

- prepare a future managed session path without claiming the profile is active now

Allowed side effects:

- writing install-owned assets
- writing install manifests
- preparing wrappers, snippets, or managed helper files

Expected outputs:

- install assets
- session-helper artifacts
- install-state descriptors

Must never do:

- claim a live current-session apply happened
- silently activate integration hooks without explicit request
- treat unmanaged external configs as RetroFX-owned

Meaningful participants:

- X11 helper flows
- session-helper targets
- WM startup fragments
- toolkit exports intended for managed future sessions

## 5. `install-as-default`

Intended use:

- install a managed user-local default profile or configuration for supported targets

Allowed side effects:

- writing install-owned default assets
- updating managed default-selection records
- writing install manifests and uninstall metadata

Expected outputs:

- default-owned install assets
- manifest records for later uninstall, repair, or migration
- optional exported copies where planned

Must never do:

- claim system-wide default ownership
- overwrite unmanaged user files without an explicit ownership contract
- imply that install automatically means current-session activation

Meaningful participants:

- selected terminal targets
- selected WM targets
- session-helper flows with clear user-local ownership
- limited toolkit paths where default management is truthful

## 6. `explicit-session-integration`

Intended use:

- generate or update integration hooks for login and startup paths

Examples:

- `greetd` or `tuigreet` snippets
- Xsession wrappers
- WM or DE launch helpers

Allowed side effects:

- writing managed integration hooks
- updating integration manifests
- linking existing emitted artifacts into explicit startup paths

Expected outputs:

- wrapper scripts
- launch helpers
- environment snippets
- integration records

Must never do:

- silently edit global display-manager configuration by default
- claim universal DE ownership
- substitute for capability filtering

Meaningful participants:

- session-helper flows
- X11 startup helpers
- limited TTY or greetd-oriented integrations
- selected WM startup flows

## Mode Interaction Rules

These rules are mandatory:

- `export-only` is not `apply-now`
- `install-for-session` is not `apply-now`
- `install-as-default` is not proof that the current live session changed
- `explicit-session-integration` must stay explicit; it is not implied by generic install

The session subsystem may combine modes only when the prompt or CLI path requests it clearly.
Examples:

- `install-for-session` plus `explicit-session-integration`
- `export-only` plus preview reports

But a combined flow must still log each ownership step separately.

## Relation To The Target Layer

This document is the lifecycle view.
[EXPORT_VS_APPLY.md](EXPORT_VS_APPLY.md) remains the target-layer contract for what target families can support.

In short:

- targets declare support and emit artifacts
- session selects the truthful lifecycle mode and records the consequences
