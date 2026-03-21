# RetroFX 2.x Future Toolkit Targets

Toolkit and desktop export targets are important to the long-term platform, but they are not required to be the first implementation wave.
This document exists so later toolkit work lands inside the same target-compiler contract instead of becoming ad hoc.

## Current Implementation Status

TWO-18 implements the first bounded desktop-facing toolkit slice under `v2/targets/toolkit/`.

Implemented now:

- `fontconfig`-style export for resolved typography policy
- `gtk-export` advisory export artifacts
- `qt-export` advisory export artifacts
- `icon-cursor` policy artifacts
- `desktop-style` aggregate export artifacts

Still future:

- live GNOME, Plasma, Xfce, or cross-DE settings mutation
- full GTK theme generation
- full Qt theme-engine integration
- icon or cursor theme installation workflows
- broader desktop or DE integration hooks

Guardrail:

- implemented toolkit targets are export-only and advisory
- they do not imply GNOME, Plasma, or global desktop ownership
- they exist to prove resolved-profile-driven desktop-facing compilation, not live orchestration

## Family Members

Implemented or active toolkit-facing targets now include:

- GTK advisory exports
- Qt advisory exports
- cursor-theme and icon-theme policy exports
- desktop-style aggregate hints

Broader future targets still include:

- desktop or DE integration fragments where truthful
- install-owned toolkit apply paths where bounded and reversible

## GTK

Consumes:

- semantic theme tokens
- typography roles
- selected chrome hints

Emits:

- GTK-oriented export artifacts

Implemented now:

- `gtk-export` emits a deterministic advisory file with GTK-facing font, icon, cursor, dark-preference, and palette hints

Mode:

- export-capable
- possibly install-capable
- rarely truthful as full apply-now in early 2.x

Limitations:

- does not imply GNOME Shell ownership
- does not imply global render support

## Qt

Consumes:

- semantic theme tokens
- typography roles
- selected chrome hints

Emits:

- Qt-oriented export artifacts

Implemented now:

- `qt-export` emits a deterministic advisory JSON artifact with Qt-facing palette, font, icon, and cursor hints

Mode:

- export-capable
- possibly install-capable

Limitations:

- does not imply Plasma-wide ownership
- often only a config-export or hint path

## Cursor Theme Targets

Consumes:

- cursor-related tokens
- cursor theme hints
- selected typography or contrast hints only where relevant

Emits:

- cursor theme selection exports or install assets

Implemented now:

- `icon-cursor` emits deterministic cursor policy artifacts for later session integration

Mode:

- export-capable
- install-capable

Limitations:

- does not itself own full desktop session policy

## Icon Theme Targets

Consumes:

- icon theme hints
- family defaults
- selected accent or contrast metadata where useful

Emits:

- icon-theme selection exports or install assets

Implemented now:

- `icon-cursor` emits deterministic icon policy artifacts for later session integration

Mode:

- export-capable
- install-capable

Limitations:

- often only advisory
- may not have truthful apply semantics across DE stacks

## Desktop Export Hints

These are now partially implemented for:

- advisory desktop-style export bundles
- environment-agnostic toolkit preference summaries

They are still future for:

- environment-scoped config hints
- DE integration fragments
- optional compatibility exports

They should remain within the same adapter contract:

- consume resolved profile and target plan
- emit explicit artifacts
- declare capabilities honestly

## Guardrail

Toolkit work must not become:

- a generic bag of ad hoc scripts
- silent DE ownership claims
- a reason to bypass the resolved profile and target-plan pipeline

Future toolkit targets should arrive only when they can truthfully declare what they support.
