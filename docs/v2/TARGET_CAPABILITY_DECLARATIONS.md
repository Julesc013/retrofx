# RetroFX 2.x Target Capability Declarations

This document defines how target adapters conceptually declare support.

Capability declarations are the adapter-local half of truthful planning.
They do not replace global capability filtering, but global planning depends on them.

## Declaration Purpose

Each target adapter should be able to describe:

- what token classes it supports
- which execution modes it supports
- which artifact types it can emit
- what validation or apply behaviors it supports
- what environment constraints it depends on

## Conceptual Declaration Shape

A target capability declaration should conceptually contain:

```text
adapter_id
family
target_name
environment_constraints
execution_modes
token_support
artifact_support
session_action_support
validation_support
degradation_policy
install_support
export_support
apply_support
recovery_support
notes
```

## Declaration Sections

### Identity

- `adapter_id`
- `family`
- `target_name`

These identify the adapter in logs and target planning.

### Environment Constraints

Examples:

- requires X11
- requires compositor host
- requires console access
- requires toolkit config location
- supports offline export anywhere

### Execution Modes

Declare supported modes such as:

- `compile-only`
- `export-only`
- `apply-now`
- `install-for-session`
- `install-as-default`

### Token Support

Declare which token groups the adapter can consume meaningfully:

- semantic theme tokens
- ANSI palette tokens
- typography tokens
- render tokens
- chrome tokens
- session helper tokens

This should distinguish:

- fully supported
- partially supported
- ignored with warning
- invalid for this target

### Artifact Support

Declare which artifact classes the adapter may emit:

- required-runtime
- optional-runtime
- ephemeral-runtime
- export-only
- install-asset
- manifest-record

### Session Action Support

Declare whether the adapter can participate in:

- apply actions
- install actions
- validation actions
- recovery-aware flows

### Degradation Policy

Describe how the adapter behaves when requested intent exceeds support:

- drop with warning
- degrade to theme-only
- degrade to export-only
- refuse as invalid

## Interaction With Environment Facts

A declaration is not enough by itself.
It must be intersected with environment facts.

Examples:

- an X11 shader adapter may declare render support, but only when X11 and compositor requirements are met
- a TTY adapter may declare palette apply support, but real apply still depends on console access
- a GTK export adapter may declare export support regardless of session type

## Interaction With Profile Strictness

Strictness does not change what an adapter supports.
It changes how the planner may treat degradation.

Examples:

- a `strict-authentic` profile may escalate a dropped render feature into a more prominent warning or refusal
- a `practical-daily-driver` profile may accept export-only or theme-only fallback

The declaration itself should remain factual and not encode subjective policy.

## Interaction With User Mode

Capability declarations must also be intersected with user or invocation mode.

Examples:

- an adapter may support `apply-now`, but the user requested `export-only`
- an adapter may support install behavior, but the current run is compile-only
- an adapter may support export anywhere, but not runtime apply in the current environment

## Example Shapes

### Terminal Export Adapter

- theme tokens: strong
- render tokens: none
- apply support: target-dependent or limited
- export support: yes
- install support: yes
- validation support: syntax-level

### TTY Adapter

- ANSI palette support: strong
- typography support: limited
- render support: none
- apply support: yes when console access exists
- export support: yes
- install support: limited

### X11 Shader Adapter

- render support: strong
- theme support: indirect
- apply support: yes when compositor path exists
- export support: yes
- validation support: strong
- environment constraints: X11 plus compositor host

## Declarations Must Be Honest

Adapters must not declare:

- full apply support when they only emit export files
- render support when they only theme config
- recovery support when they cannot participate in manifest-driven lifecycle

Capability declarations are not marketing text.
They are planning inputs.

