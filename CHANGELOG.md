# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-27

### Added
- Phase 1 foundation: profile-driven rendering pipeline, atomic apply/off, rollback, and strict TOML parsing.
- X11 + picom backend (full path) with shader template generation and validation.
- Preview, doctor, wizard, pack profiles, search/info UX, and logging/audit trail.
- Structured palettes and bounded custom palette support.
- TTY backend + semantic ANSI mapping and tuigreet snippet generation.
- Session integration helpers and honest Wayland degraded mode.
- Session-local fonts/AA controls with generated fontconfig/alacritty/xresources artifacts.
- User-local install/uninstall/status workflow and managed Xsession helpers.
- Base16 JSON interop (import/export), offline gallery, and pack install workflow.

### Changed
- Hardened apply/off transaction discipline for deterministic and fail-safe behavior.
- Expanded test harness to cover static shader invariants, degraded mode behavior, backend scaffolding, install flow, and interop.

### Documentation
- Added architecture, profile spec, capabilities, integration, quickstart, testing, installation, fonts, palettes, and interop guides.
