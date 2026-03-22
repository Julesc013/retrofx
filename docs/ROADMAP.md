# RetroFX Roadmap

This roadmap is intentionally conservative.
It governs the stable `1.x` line and points to the experimental `2.x` line without conflating them.

## Current Repository Model

RetroFX now lives on one branch, but it still has two distinct tracks:

- `1.x`: production line, patch-only after `1.0.0`
- `2.x`: experimental redesign line under `v2/` and `docs/v2/`

The roadmap rule is simple:

- keep `1.x` boring
- let `2.x` evolve only through explicit experimental gates

## 1.x Scope (Implemented And Supported)

- profile-driven renderer with `passthrough`, `monochrome`, and `palette` modes
- X11 + `picom` + GLX full runtime path
- degraded Wayland apply path
- scoped TTY backend and `tuigreet` snippet generation
- repo-local mode and user-local install mode
- manifest-based integrity model:
  - `self-check`
  - `repair`
  - `state/last_good/`
- pack install relocation for profile-local assets
- Base16 JSON import/export as a deterministic lossy bridge
- regression suite and local CI wrapper

## 1.0.x Maintenance Track (Current)

Only this class of work belongs on the stable line:

- bug fixes in documented supported environments
- apply/off/install/repair safety fixes
- doc-truth corrections
- supported-host validation on the X11 + `picom` + GLX path
- conservative release/process cleanup

Not part of `1.0.x`:

- new rendering families
- new orchestration concepts
- broad DE or Wayland ownership work
- profile-schema redesign
- anything that belongs naturally under `v2/`

## 2.x Direction (Separate Experimental Track)

`2.x` is now real implementation work, not just future aspiration, but it is still experimental.

Current `2.x` direction:

- broaden RetroFX from a shell-heavy runtime tool into a profile compiler and bounded orchestration platform
- keep support classes explicit
- keep live ownership narrower than compile/export breadth
- gather evidence before widening promises

Current `2.x` planning truth:

- limited public technical beta: yes, through the narrowed copied-toolchain wrapper only
- broader beta stabilization: no
- `1.x` replacement: no

Use these docs instead of this file for 2.x planning:

- [docs/v2/README.md](v2/README.md)
- [docs/v2/IMPLEMENTED_STATUS.md](v2/IMPLEMENTED_STATUS.md)
- [docs/v2/TECHNICAL_BETA_READINESS.md](v2/TECHNICAL_BETA_READINESS.md)
- [docs/v2/NEXT_STAGE_VERDICT.md](v2/NEXT_STAGE_VERDICT.md)
- [docs/PLANNING_HANDOFF_2026-03-22.md](PLANNING_HANDOFF_2026-03-22.md)

## Decision Rule

When planning new work, ask:

- does this restore or protect documented `1.x` behavior
- or does it broaden RetroFX into a more general appearance compiler and orchestration platform

If it is the second case, it belongs in `2.x`, not in `1.0.x` maintenance.
