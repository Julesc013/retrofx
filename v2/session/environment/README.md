# v2/session/environment

Purpose:

- future home of environment-model collection and environment-fact helpers

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

- fact collectors that feed capability filtering and session orchestration without bypassing either layer
