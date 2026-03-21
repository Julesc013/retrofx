# RetroFX 2.x Capability Filtering

This document operationalizes the 2.x capability model.
It explains how the engine turns resolved profile intent into a truthful target plan.

## Purpose

Capability filtering is the stage that intersects:

- resolved profile intent
- current environment facts
- adapter capability declarations
- session and lifecycle policy

Its output is the capability-filtered target plan.

This is where 2.x decides whether to:

- apply as requested
- degrade but continue
- export only
- refuse as invalid

## Capability Inputs

Capability filtering uses four input groups.

### 1. Target And Backend Capabilities

Advertised by target adapters and environment-specific backends.

Examples:

- theme support
- render support
- typography support
- session integration support
- recovery support
- install support
- export support

### 2. Current Environment Facts

Facts detected or selected outside the profile.

Examples:

- session type
- compositor availability
- WM or DE identity
- whether install mode is active
- whether a compatible login or session integration path exists

### 3. User And Session Policy

Policy from the resolved profile or explicit invocation context.

Examples:

- requested target classes
- `apply_mode`
- `persistence`
- explicit export-only invocation
- selected target narrowing

### 4. Profile Policy And Strictness

Profile-level meaning that affects how aggressively the engine may degrade.

Examples:

- strictness level
- render mode
- render effects
- display transforms
- typography policy

## Filtering Outputs

Capability filtering must produce explicit outputs, not implied behavior.

### Supported Target Plan

Targets that can be compiled and, when policy allows, applied truthfully.

### Degraded Target Plan

Targets that remain valid, but with reduced features or reduced lifecycle ownership.

### Export-Only Plan

Targets that can produce useful artifacts but cannot claim runtime apply or repair semantics in the selected context.

### Unsupported Records

Requests that cannot be satisfied truthfully.
These should produce explicit warnings or errors depending on severity.

## Decision Classes

Every target-plan entry should resolve into one of these operational decisions.

### Apply As Requested

Use this when:

- required capabilities are satisfied
- lifecycle ownership is available
- no contradictory policy exists

### Degrade But Continue

Use this when:

- the target remains supported
- some requested features are unavailable
- the resulting behavior is still truthful

Examples:

- dropping render transforms while preserving theme output
- weakening session integration while preserving exports

### Export Only

Use this when:

- artifact generation is valid
- runtime ownership is not

Examples:

- GNOME Wayland toolkit and terminal exports
- explicit CI or pack-generation flows

### Refuse As Invalid

Use this when:

- the request is structurally contradictory
- the profile mode and requested features cannot produce a coherent outcome
- the selected operation would lie about ownership or support

Examples:

- apply-only request with no viable runtime target
- impossible install or repair expectations for an unsupported environment

## Filtering Algorithm Shape

The future implementation should reason in this order:

1. start from resolved semantic intent
2. narrow to requested target classes
3. bind candidate adapters for the selected environment
4. compare requested capabilities with advertised capabilities
5. decide apply, degrade, export-only, skip, or refuse
6. record reasons for every degraded or skipped capability
7. compute runtime requirements such as compositor need

The engine should prefer explicit downgrade records over silent fallback.

## Example Outcomes

### X11 + i3 + picom

Expected behavior:

- theme targets: apply as requested
- render targets: apply as requested
- session integration: apply as requested
- compositor requirement: `required` or `optional` depending on the target mix

Typical result:

- full render-capable X11 target plan
- required runtime artifacts for the render path

### Wayland + `sway`

Expected behavior:

- theme targets: supported
- typography and terminal outputs: supported
- session integration: partial or adapter-dependent
- global compositor-style render transforms: degrade or drop

Typical result:

- degrade but continue for render-heavy intent
- theme, typography, and selected session outputs remain valid

### TTY

Expected behavior:

- palette and console-font policy: supported where host permits it
- rich UI chrome and compositor behavior: unavailable
- target-specific session ownership: narrow but explicit

Typical result:

- apply palette and console-related outputs
- degrade or warn on unrelated chrome and render requests

### GNOME Wayland

Expected behavior:

- terminal and toolkit exports: possible
- icon and cursor hints: possible
- shell-wide render path: unsupported
- full runtime ownership: not truthful in the baseline design

Typical result:

- export-only plan or partial non-owning plan depending on invocation
- explicit warnings for unsupported render requests

## Strictness And Degradation

Strictness should influence degradation behavior, but it must not override support truth.

- `strict-authentic` may prefer refusal or prominent warnings when key style intent cannot survive degradation
- `practical-daily-driver` may accept more deterministic downgrades

The engine may vary warning severity or downgrade preference based on strictness, but it must not invent unsupported capabilities.

## What Capability Filtering Must Not Do

- it must not rewrite raw authored data
- it must not emit files
- it must not mutate runtime state
- it must not smuggle backend syntax into the resolved profile
- it must not pretend export-only output equals apply support

