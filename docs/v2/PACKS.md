# RetroFX 2.x Packs

RetroFX 2.x packs are local curated collections of profiles, metadata, family identity, and optional shared assets.
They are data containers for discovery and organization.
They are not runtime executables and they are not a network marketplace.

As of TWO-14, RetroFX 2.x has a real local pack manifest format and built-in curated packs under `v2/packs/`.
Pack-aware profile resolution is implemented only in the dev-only 2.x inspection, compile, and planning entrypoints.

## Purpose

A 2.x pack groups:

- related 2.x profile documents
- style-family identity
- descriptive metadata and tags
- shared local asset references
- typography or appearance recommendations

Packs help RetroFX answer questions that single profile files cannot answer cleanly on their own:

- which profiles belong to the same family
- what a built-in style collection should be called and tagged
- which local preview or recommendation assets travel with that collection
- where a resolved profile came from

## Manifest Format

Pack manifests use TOML and currently identify as:

```toml
schema = "retrofx.pack/v2alpha1"
```

The manifest is separate from the authored profile schema.
Profiles inside a pack remain normal `retrofx.profile/v2alpha1` profile files.

### Canonical Shape

```toml
schema = "retrofx.pack/v2alpha1"

[pack]
id = "crt-core"
name = "CRT Core"
description = "Curated phosphor-forward profiles."
family = "crt"
tags = ["crt", "retro", "display"]
author = "RetroFX"
source = "builtin-local"

[assets]
preview = "assets/preview.toml"

[recommendations.typography]
terminal_primary = "Terminus Nerd Font"
ui_sans = "IBM Plex Sans"

[[profiles]]
id = "green-crt"
file = "profiles/green-crt.toml"
name = "Green CRT"
description = "Authentic green phosphor baseline."
family = "crt"
tags = ["green", "phosphor", "strict"]
```

## Directory Layout

The current local-first layout is:

```text
v2/packs/
  crt-core/
    pack.toml
    profiles/
    assets/
  terminal-classic/
    pack.toml
    profiles/
    assets/
  modern-minimal/
    pack.toml
    profiles/
    assets/
```

Rules:

- `pack.toml` is required.
- pack directory name must match `pack.id`.
- profile entries explicitly map `profile.id` to a relative TOML file path.
- asset references must stay inside the pack root.
- packs are local and deterministic; they do not execute code.

## What Packs Own

Packs own:

- local discovery metadata
- style-family labeling
- profile grouping
- optional shared asset references
- recommendation metadata that later compilers or preview tools may consult

Packs do not own:

- profile schema validation
- target emission logic
- session apply or install behavior
- network fetching or update policy

## Current Implementation Truth

As of TWO-14:

- `v2/packs/loader.py` parses `retrofx.pack/v2alpha1` manifests
- `v2/core/dev/list-packs` lists built-in local packs
- `v2/core/dev/show-pack <pack-id>` inspects a pack manifest and its profiles
- `v2/core/dev/resolve-profile --pack <pack-id> --profile-id <profile-id>` resolves a profile through the normal 2.x core pipeline
- `v2/core/dev/compile-targets` and `v2/core/dev/plan-session` can also resolve profiles by pack id and profile id
- resolved profiles now carry pack-origin metadata when loaded from a pack

Not implemented yet:

- remote/community pack discovery
- pack installation workflows
- pack inheritance engines
- preview rendering systems
- marketplace or registry semantics

## Built-In Packs

The first built-in packs are:

- `crt-core`
- `terminal-classic`
- `modern-minimal`

These packs exist to give future 2.x prompts real local data to work with.
They are curated seed data, not a finalized ecosystem story.
