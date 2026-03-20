# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-beta.1] - 2026-03-21

### Present
- Profile-driven rendering and theming workflow with strict TOML profile validation.
- `passthrough`, `monochrome`, and `palette` modes.
- Supported X11 + picom + GLX runtime path.
- Optional TTY ANSI16 backend with rollback/mock support.
- Optional tuigreet snippet generation.
- Repo-local and user-local install/uninstall workflows.
- `doctor`, `compatibility-check`, `self-check`, `repair`, `status`, `explain`, and `apply --dry-run`.
- Import/export support for `xresources`, `alacritty`, and Base16 JSON.
- Curated core pack profiles, user profiles, and pack install relocation into `profiles/user_assets/`.

### Stabilized
- Manifest-based artifact contract for `apply`, `off`, `self-check`, `repair`, install-mode health, and status reporting.
- Required/optional/export/runtime artifact semantics, including zero-byte optional-file handling and required-artifact enforcement.
- `install-pack` relocation and profile-local asset rewriting for copied pack profiles.
- Session wrapper compositor policy based on explicit runtime intent, not file presence.
- Strict `scope.x11` runtime semantics and stale-artifact cleanup.
- Deterministic, documented Base16 lossy-bridge contract.
- Release-critical regression coverage across integrity, wrapper behavior, degraded Wayland, install/uninstall, and pack workflows.
- CLI/operator clarity with read-only `explain`, `apply --dry-run`, and clearer apply/off/repair end-state messages.
- Docs truth pass, support matrix alignment, and release-preparation documentation.

### Known Limitations
- Wayland support is degraded only; there is no global Wayland shader/compositor path.
- X11 integration outside the documented i3 wrapper path is more manual and less validated.
- TTY output remains 16-color semantic output; `fonts.tty` remains best-effort host-dependent behavior.
- Base16 import/export is deterministic but intentionally lossy.
- RetroFX 1.x does not provide full desktop-environment-wide GTK/Qt/icon/cursor orchestration.

## [0.1.0-beta.1] - 2026-02-27

### Added
- Profile-driven rendering system.
- Monochrome 2–256 band support.
- Structured palette modes (VGA16, cube256, etc.).
- Ordered dithering.
- Scanlines, flicker, vignette.
- Safe-mode rendering.
- Atomic apply/off.
- TTY backend (optional).
- Tuigreet theme generation.
- Wayland degraded mode.
- Install/uninstall mode.
- Doctor, self-check, repair.
- Compatibility-check.
- Performance auditing.
- Profile packs + wizard.
- Base16 import/export.
- Session-local font handling.

### Safety Guarantees
- No system-wide modification by default.
- Atomic rollback.
- Corruption detection.
- Degraded fallback on failure.

### Known Limitations
- No global Wayland shader support.
- No curvature or temporal persistence.
- TTY limited to 16 colors.
- Custom palettes limited to <=32 explicit entries.

## [0.1.0-beta] - 2026-02-27

### Added
- Phase 1: profile-driven rendering core, strict TOML parsing, atomic apply/off, rollback snapshots, shader/picom generation.
- Phase 2: TTY palette backend, semantic ANSI role mapping, and tuigreet snippet generation.
- Phase 3: session wrappers, capability reporting, and honest Wayland degraded mode.
- Phase 4: curated core profile packs, improved profile wizard, search/info UX, and quickstart docs.
- Phase 5: structured palette families and bounded custom palette support (`<= 32`) with selective picom rules.
- Phase 6: profile-driven fonts/AA controls with session-local fontconfig and terminal exports.
- Phase 7: user-local install/uninstall/status workflows and managed Xsession integration.
- Phase 8: Base16 JSON interop (import/export) and offline gallery pack workflow.
- Phase 9: release engineering basics (single VERSION source, CI runner, doctor JSON, self-check/repair).
- Phase 10: apply-path optimization, no-op skip logic, minimized compositor restarts, and perf timing command.
- Phase 11: compatibility-check, safe apply mode, corruption checksum detection, sanity-perf, and beta safety docs.

### Changed
- Hardened self-check with checksum integrity verification and stronger corruption detection.
- Added environment guardrails for Wayland, missing DISPLAY, and SSH without X forwarding.
- Improved repair fallback behavior for safe degraded restoration when full state is unavailable.

### Known Limitations
- No global Wayland post-process shader pipeline.
- No curvature/warp effects.
- No temporal persistence/frame-history effects.
- TTY rendering is limited to 16-color palette semantics.
- Custom palettes above 32 colors are not supported.
