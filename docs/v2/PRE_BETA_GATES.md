# RetroFX 2.x Pre-Beta Gates

This document defines what must be true before the 2.x branch can claim pre-beta-style hardening readiness.

It is intentionally stricter than the current internal-alpha gate.

## Required Gates

### 1. Broader Alpha Must Be Real First

- broader alpha must already be approved
- at least one real Wayland host must complete the supported checklist honestly
- at least one additional real X11 host must complete the same checklist

### 2. Deterministic Implemented Surface

- target compiler outputs remain deterministic for the implemented families
- package, install, uninstall, and diagnostics flows remain reproducible
- release metadata must distinguish current hardening builds from historical tagged alpha candidates truthfully
- release-ish package generation must not silently proceed from a dirty tree by default
- current-state, install-state, and manifest shapes remain contract-tested

### 3. Honest Supported Surface

- docs and status output clearly separate:
  - supported internal-alpha flows
  - broader-alpha-ready flows
  - export-only or degraded flows
- non-sway Wayland desktops remain clearly classified until real evidence broadens support
- X11 render remains explicitly bounded and not overclaimed

### 4. Bounded Runtime Trust

- apply or off stays inside managed 2.x roots
- install or uninstall ownership remains explicit
- diagnostics capture remains sufficient to reproduce tester reports

### 5. Compatibility Evidence

- migration validation expands beyond the current representative subset
- compatibility reports remain truthful about degraded, manual, and unsupported mappings

## Gate Failure Examples

Pre-beta remains blocked if any of these remain true:

- broader alpha is still not approved
- real-host validation is still narrow to one strong X11 host
- docs overstate broader readiness
- deterministic output or cleanup contracts regress

## Current Status

For TWO-29:

- broader alpha: not ready
- non-public pre-beta: not ready
- pre-beta: not ready
- current branch version: `2.0.0-alpha.internal.2`
- latest historical local alpha candidate: `v2.0.0-alpha.internal.1`
- current next step: continue internal alpha hardening rather than pre-beta staging
