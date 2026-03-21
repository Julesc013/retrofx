# RetroFX 2.x Future Toolkit Targets

Toolkit and desktop export targets are important to the long-term platform, but they are not required to be the first implementation wave.
This document exists so later toolkit work lands inside the same target-compiler contract instead of becoming ad hoc.

## Current Implementation Status

Most toolkit work remains future.
The one narrow implemented exception is TWO-12's session-local `fontconfig` typography export target.

Implemented now:

- `fontconfig`-style export for resolved typography policy

Still future:

- GTK exports
- Qt exports
- cursor-theme selection targets
- icon-theme selection targets
- broader desktop export hints

Guardrail:

- the implemented `fontconfig` target does not imply GTK, Qt, GNOME, or Plasma ownership
- it exists to prove typography-policy compilation, not to claim full desktop font orchestration

## Family Members

Deferred or future toolkit-facing targets include:

- GTK exports
- Qt exports
- cursor-theme selection hints
- icon-theme selection hints
- desktop or DE export hints where truthful

## GTK

Consumes:

- semantic theme tokens
- typography roles
- selected chrome hints

Emits:

- GTK-oriented export artifacts

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

Mode:

- export-capable
- install-capable

Limitations:

- often only advisory
- may not have truthful apply semantics across DE stacks

## Desktop Export Hints

These are future targets for:

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
