# RetroFX 2.x Public Beta Gates

This document defines what must be true before the 2.x branch can claim a limited public technical beta.

This gate is narrower than the broader internal developer surface.
It is not a gate for general-public beta or stable release.

## A. Documentation

Required:

- README and readiness docs are truthful
- installation, uninstall, diagnostics, and cleanup flow are documented clearly
- supported versus degraded versus unsupported environments are explicit
- known limitations and non-goals are obvious to outside advanced testers

Current line state:

- satisfied for the limited technical-beta surface
- the candidate package ships the relevant notes, checklist, and readiness docs directly

## B. Workflow Safety

Required:

- no hidden destructive side effects
- bounded apply or off remains trustworthy in supported environments
- package, install, uninstall, and diagnostics flows are deterministic
- cleanup and ownership are explicit

Current line state:

- satisfied for the limited technical-beta surface
- apply is explicitly gated to X11-oriented environments and everything remains user-local

## C. Implementation Trust

Required:

- compiler outputs remain deterministic
- status, manifests, and install-state are trustworthy
- degraded and unsupported paths are surfaced explicitly
- risky internal-only paths are fenced off from outside testers

Current line state:

- satisfied for the limited technical-beta surface
- migration and the explicit X11 probe are now outside the support promise rather than overclaimed

## D. Audience Suitability

Required:

- a technically literate tester can succeed without source archaeology
- the branch does not impersonate production quality
- the support burden remains manageable for maintainers

Current line state:

- satisfied for the limited technical-beta surface
- the copied-toolchain package, wrapper, notes, and diagnostics flow remove the old repo-checkout requirement

## Gate Result

For the current limited technical-beta line:

- limited public technical beta: ready
- continued non-public pre-beta: not the active track
- continued internal alpha: yes
- next step: continue limited technical-beta circulation, gather diagnostics-backed tester evidence, and revisit broader beta only after the evidence base widens
