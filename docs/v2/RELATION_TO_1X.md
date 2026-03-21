# RetroFX 2.x Relation To 1.x

RetroFX 1.x and RetroFX 2.x should coexist as separate tracks.
1.x remains the stable product line.
2.x is the redesign line.

## What 1.x Remains Responsible For

RetroFX 1.x remains responsible for the documented stable line:

- the supported X11 plus `picom` plus GLX path
- scoped TTY outputs
- `tuigreet` snippet generation
- deterministic terminal and export outputs
- current install, apply, off, self-check, and repair trust model
- patch-only maintenance, regression fixes, and doc-truth corrections

1.x should stay boring.
It should not absorb broad platform redesign work.

## Why 2.x Is A Separate Branch And Track

2.x needs a broader product model than 1.x:

- a semantic profile schema instead of only the current profile format
- a resolved profile and capability planner
- multiple target compilers and adapters
- session orchestration as a platform layer
- deeper separation between theme, render, and session concerns

That is redesign work, not a patch stream.
Putting it directly on the 1.x release line would destabilize the stable product and blur responsibility.

## What Carries Forward From 1.x

2.x should preserve these 1.x ideas:

- profile-driven generation
- deterministic artifacts
- truthful support boundaries
- explicit degraded behavior instead of fake promises
- user-scoped or session-scoped defaults over hidden system edits
- trustworthy apply, off, and repair behavior
- curated packs as a first-class concept

Current implementation truth:

- 2.x now has a dev-only local pack manifest layer and built-in curated packs under `v2/packs/`
- that pack layer is intentionally separate from 1.x pack/runtime behavior and does not replace 1.x workflows
- 2.x now also has a dev-only 1.x profile inspection and draft migration slice under `v2/compat/`
- that compatibility slice is review-oriented and does not replace the 1.x CLI or runtime

## What 2.x Replaces

2.x replaces the idea that future growth should happen by stretching the 1.x architecture indefinitely.
In practice, it replaces:

- the 1.x implementation-led architecture as the foundation for broader scope
- narrow X11-centric product framing as the long-term product definition
- backend-specific coupling that does not scale to multiple target families
- implicit support assumptions that are not backed by a capability contract

This does not mean 1.x was wrong.
It means 1.x is not the right long-term container for the broader platform.

## Migration Concerns

- 1.x profiles may not map directly to the eventual 2.x schema.
- 2.x may need compatibility import or migration tooling rather than promising direct schema reuse.
- 2.x local packs are currently curated seed data, not a migrated replacement for 1.x pack install or selection workflows.
- 2.x now has the first real import and migration tooling for a supported subset of 1.x profiles, but not full runtime compatibility.
- Existing 1.x users should be able to stay on 1.x without being forced into early 2.x semantics.
- 2.x should avoid breaking the current 1.x release workflow, packaging, or support promises while the redesign is still maturing.

## Branch Discipline

- `release/1.0` remains the maintenance branch for 1.x stability work.
- 2.x redesign work belongs on a dedicated design or architecture branch until implementation phases are ready.
- 1.x bug fixes may inform 2.x design, but 2.x architecture work should not be backported into 1.x.
- Reading 1.x for context is encouraged; redefining 1.x from within 2.x work is not.

## Decision Rule

When work is proposed, ask:

- does this restore or protect documented 1.x behavior
- or does it broaden RetroFX into a more general appearance compiler and orchestration platform

If it is the second case, it belongs in 2.x.
