# RetroFX 2.x Install Model

RetroFX 2.x must define "install" precisely.
Install is not just "copy some files" and it is not the same as current-session apply.

## Definition

In 2.x, install means:

- writing RetroFX-managed user-local assets and metadata into a declared install footprint
- recording ownership so those assets can later be repaired, updated, or uninstalled safely

Install must remain reversible and user-local by default.

## Key Distinctions

| Concern | Meaning In 2.x |
| --- | --- |
| repo-local use | run from the source tree without claiming a managed install footprint |
| user-local install | managed copy or managed runtime footprint under user-owned paths |
| target-specific installed assets | files a target needs for future managed use |
| session integration artifacts | wrappers, launch helpers, snippets, or desktop entries owned by install state |
| pack assets | copied pack-local assets needed by installed profiles |
| runtime-generated state | current-state descriptors, apply results, recovery baselines, transient active ownership |
| exports | generated outputs that do not imply install ownership unless explicitly installed |

## What Install Owns

Install should own only assets that RetroFX can later:

- identify
- validate
- repair
- remove or replace safely

Examples of install-owned data:

- managed user-local RetroFX home
- managed wrappers or launch helpers
- install-owned target artifacts
- copied pack-local assets needed by installed profiles
- install manifests and ownership records

## What Install Must Never Own

Install must not claim ownership of:

- global system configuration by default
- arbitrary user files outside a declared managed footprint
- unmanaged WM or DE config trees
- the current live session merely because files were installed
- arbitrary exported files left in ad hoc destinations

If RetroFX cannot uninstall or repair a path predictably, install should not claim it as managed.

## Repo-Local Use Versus User-Local Install

### Repo-Local Use

Characteristics:

- development or testing oriented
- no claim that the repository itself is an installed product footprint
- runtime state may still exist, but install ownership is separate

### User-Local Install

Characteristics:

- explicit managed home
- explicit manifest ownership
- explicit update, repair, and uninstall expectations

This mirrors the useful 1.x distinction while giving 2.x a cleaner ownership model.

## Install Versus Current-Session Apply

Install and apply are different.

`apply-now` means:

- make scoped current-session changes
- write active-session state and recovery records

`install-for-session` or `install-as-default` means:

- write managed assets for future use
- record install ownership
- optionally wire explicit integration hooks

Install may prepare a future session without changing the current one at all.

## Pack Assets

Pack-local assets should become install-owned only when:

- a managed installed profile depends on them
- RetroFX copies them into a managed destination
- install records track them explicitly

2.x should carry forward the 1.x safety idea that installed profiles must not depend on volatile pack source locations.

## Exports Versus Installed Assets

An export is not automatically an installed asset.

Examples:

- a generated `kitty` config dropped into an export directory is still just an export
- a generated Xsession helper under a managed install path can be an installed asset

The difference is ownership and lifecycle, not file syntax.

## Uninstall Concept

Future uninstall behavior should operate from install manifests and ownership records.

Conceptually uninstall should:

- remove install-owned assets
- remove install-owned integration hooks
- preserve or optionally back up user-owned profile data when policy says to do so
- avoid touching export-only outputs that were never install-owned

Uninstall must not rely on broad path deletion or guessing from filenames.

## Reversibility And Safety

Install should remain safe by following these rules:

- user-local by default
- explicit ownership records
- no silent takeover of unmanaged paths
- clean separation from current-session state
- uninstall driven by manifests, not heuristics

## Carry-Forward From 1.x

2.x intentionally carries forward these 1.x lessons:

- repo-local and installed modes should stay distinct
- install-asset health should be reported separately from runtime health
- pack assets may need relocation into user-managed space
- uninstall should preserve user-owned data when requested

2.x improves the model by:

- separating install ownership from active-session state
- making integration hooks explicit install artifacts
- making install manifest ownership a planned subsystem instead of a scattered implementation detail
