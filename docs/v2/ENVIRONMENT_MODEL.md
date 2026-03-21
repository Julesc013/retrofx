# RetroFX 2.x Environment Model

RetroFX 2.x needs an explicit environment abstraction so capability filtering and session orchestration can reason from facts instead of heuristics buried in wrappers.

The environment model is a fact record, not a second planner.

## Purpose

The environment model exists to answer questions such as:

- what kind of session is this
- is this repo-local or installed use
- is there a compositor-capable X11 path
- which WM or DE is present
- is this a login or startup context rather than an already-running session
- which targets are even plausible to apply now

## Session Classes

The environment model should classify at least these session classes:

| Session Class | Meaning |
| --- | --- |
| `tty` | interactive console session without GUI stack ownership |
| `login-tty` | login-time TTY context before a broader session is launched |
| `tuigreet` | greetd or login presentation context with TUI-like constraints |
| `x11` | active X11 session |
| `xwayland` | X11 clients running inside a Wayland session |
| `wayland` | active native Wayland session |
| `remote-ssh` | remote or forwarded shell context where local session ownership may be absent |
| `unknown-headless` | no trustworthy display or login/session ownership facts available |

`unknown-headless` is a valid outcome.
When detection is uncertain, the model should stay conservative rather than invent support.

## Context Classes

The environment model should also classify execution context:

| Context Class | Meaning |
| --- | --- |
| `repo-local-dev` | running from a source tree for development or testing |
| `installed` | running from a managed user-local install footprint |
| `current-session` | acting on a live already-running session |
| `login-session-startup` | generating or executing startup/login integration |
| `export-only` | generating artifacts without claiming live session ownership |

These context classes are orthogonal to session classes.

Examples:

- `repo-local-dev` plus `x11`
- `installed` plus `wayland`
- `login-session-startup` plus `tuigreet`
- `export-only` plus `unknown-headless`

## Environment Facts

The environment model should provide facts in at least these categories.

### Display And Session Facts

- display server class
- whether the session appears local or remote
- session startup versus already-running session
- XDG or desktop-session hints when available

### Compositor And Render Facts

- compositor availability
- compositor identity when detectably relevant
- whether an X11 compositor-hosted path looks possible
- whether the current environment is already degraded by design

### WM Or DE Facts

- detected WM identity
- detected DE identity
- confidence of that detection
- whether the environment is mixed or ambiguous

### Terminal And Login Facts

- terminal emulator identity when relevant
- whether the process is attached to a TTY
- whether the context resembles `tuigreet` or other login UI

### Install And Ownership Facts

- repo-local versus installed mode
- install home when relevant
- whether managed manifests or state stores are available

### Target-Specific Prerequisites

- required executables available or absent
- target-owned integration paths available or absent
- writable managed destination availability

### Capability Hints

- support hints that help capability filtering choose between full, degraded, export-only, or unsupported outcomes
- no hint may upgrade a target beyond what the adapter declaration allows

## What The Environment Model Provides To Capability Filtering

Capability filtering should consume environment facts such as:

- X11 versus Wayland versus TTY
- compositor availability
- WM or DE identity
- login/startup versus current-session context
- prerequisite availability

Those facts help answer:

- can this target apply as requested
- must this target degrade
- should this target stay export-only
- should this request be refused as invalid in this environment

## What The Environment Model Provides To Session Orchestration

Session orchestration should consume environment facts such as:

- whether current-session apply is truthful at all
- where managed install or state records belong
- whether the operation is acting at startup, live session, or export-only scope
- whether wrapper or integration generation is appropriate

The environment model therefore helps session answer:

- what scope this operation can own
- what side effects are allowed
- what recovery baseline is relevant

## What The Environment Model Must Not Decide

The environment model must not:

- reinterpret semantic profile intent
- compile target files
- invent target capabilities
- choose fallback token values
- silently rewrite session policy

It provides facts.
Planning and orchestration decide what those facts mean.

## Detection Principles

Later implementation prompts should follow these rules:

- best-effort detection is acceptable
- uncertainty must be represented explicitly
- missing facts should reduce claims, not increase them
- session wrappers must prefer explicit recorded state over guessed environment conclusions

## Relation To 1.x

1.x already learned that wrapper behavior becomes unsafe when compositor or session intent is inferred from file presence alone.

2.x improves on that by separating:

- environment facts
- target capability declarations
- recorded runtime intent

That separation should prevent ambiguous wrapper behavior and muddled degraded-mode claims.
