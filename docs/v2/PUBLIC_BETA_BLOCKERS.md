# RetroFX 2.x Public Beta Blockers

This document lists the issues that still block a broader public beta.

For the current limited technical-beta line, there are no open `public-beta-blocker` items.
The remaining items below are non-blocking limitations for that line but still matter for any broader future public surface.

## Public-Beta-Blocker

None open for the limited technical-beta line.

## High

### 1. Real-host validation breadth remains intentionally narrow

- Severity: `high`
- Evidence: the candidate support matrix is intentionally anchored to one real X11 plus `i3` validation host plus bounded temp-HOME flows
- Why it matters: this is acceptable for a limited technical-beta audience, but it still blocks any broader public beta story

### 2. Migration breadth remains representative rather than broad

- Severity: `high`
- Evidence: migration remains available only on the internal developer surface and is not part of the technical-beta promise
- Why it matters: this is acceptable when fenced, but it blocks any broader public-facing compatibility claim

## Medium

### 3. Wayland remains export-oriented rather than live-runtime supported

- Severity: `medium`
- Evidence: the technical-beta wrapper allows plan, compile, bundle, and diagnostics on Wayland-like environments, but not bounded live apply
- Why it matters: acceptable for the limited technical-beta matrix, but still blocks broader cross-environment expectations

### 4. Toolkit exports remain advisory only

- Severity: `medium`
- Evidence: GTK, Qt, icon-cursor, and desktop-style outputs are deterministic exports, not live desktop ownership
- Why it matters: acceptable when documented, but not a basis for broader desktop-integration claims

## Current Result

For the current limited technical-beta line:

- `READY_FOR_LIMITED_PUBLIC_TECHNICAL_BETA=yes`
- current public surface position: `limited-public-technical-beta-candidate`
- recommended next step: circulate the narrowed copied-toolchain candidate to advanced testers while keeping broader claims fenced
