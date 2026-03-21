# v2/targets/tty

Purpose:

- future home of the TTY target family

What belongs here:

- console palette emitters
- console-font related target helpers
- TTY-specific validation or restore metadata helpers

What does not belong here:

- general terminal config emitters
- login-manager snippet generation
- compositor logic

Governing docs:

- `docs/v2/TARGET_FAMILIES.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/EXPORT_VS_APPLY.md`

Later prompts should implement:

- truthful TTY adapters that remain explicit about console access limits and scoped apply behavior

