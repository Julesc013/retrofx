# v2/session/environment

Purpose:

- future home of environment-model collection and environment-fact helpers

Implemented now:

- best-effort session detection for `x11`, `wayland`, `tty`, `remote-ssh`, and `unknown-headless`
- best-effort WM or DE detection for `i3`, `sway`, `gnome`, `plasma`, and `unknown`
- repo-local versus installed context classification for the dev scaffold

What belongs here:

- session-class detection helpers
- context-class detection helpers
- prerequisite and capability-hint gathering
- conservative unknown-state handling

What does not belong here:

- target capability invention
- semantic profile reinterpretation
- direct apply or install logic

Governing docs:

- `docs/v2/ENVIRONMENT_MODEL.md`
- `docs/v2/SESSION_SYSTEM.md`

Later prompts should implement:

- richer fact collectors that feed capability filtering and session orchestration without bypassing either layer
