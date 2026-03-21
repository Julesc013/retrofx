# v2/targets/toolkit

Purpose:

- future home of toolkit and desktop export target adapters

What belongs here:

- GTK export adapters
- Qt export adapters
- cursor and icon theme selection exports
- future desktop-policy hint emitters

What does not belong here:

- silent DE ownership claims
- raw profile parsing
- X11 render logic

Governing docs:

- `docs/v2/FUTURE_TOOLKIT_TARGETS.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/TARGET_CAPABILITY_DECLARATIONS.md`

Later prompts should implement:

- truthful export-first toolkit targets that fit the same adapter contract as the rest of the platform

