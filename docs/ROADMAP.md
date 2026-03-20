# RetroFX Roadmap

This file is intentionally conservative. It distinguishes current 1.x scope from possible future work.

## Current 1.x Scope (Implemented)

- Profile-driven renderer with `passthrough`, `monochrome`, and `palette` modes.
- X11 + picom + GLX full runtime path.
- Wayland degraded apply path.
- Scoped TTY backend and tuigreet snippet generation.
- Repo-local mode and user-local install mode.
- Manifest-based integrity model:
  - `self-check`
  - `repair`
  - `state/last_good/`
- Pack install relocation for profile-local assets.
- Base16 JSON import/export as a deterministic lossy bridge.
- Regression suite and local CI wrapper.

## Remaining 1.x Work Before 1.0 Stable

- Continue stabilization only:
  - bug fixes
  - docs truth remediation
  - host validation on the supported X11 path
  - release packaging and release process cleanup
- No new rendering features are planned for the 1.x stabilization branch.

## Future / 2.x Direction (Not Part Of This Branch)

- Broader appearance-compiler or orchestration-platform work.
- Deeper desktop-environment theming automation.
- Any redesign that would require broader Wayland or DE integration assumptions.

These items are future direction only, not a commitment for 1.x.
