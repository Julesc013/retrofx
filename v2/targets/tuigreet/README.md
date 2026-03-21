# v2/targets/tuigreet

Purpose:

- future home of `tuigreet` and related login-presentation target adapters

What belongs here:

- generated greet fragments
- palette and typography mapping for login presentation targets

What does not belong here:

- global greetd ownership
- general session orchestration
- raw profile parsing

Governing docs:

- `docs/v2/TARGET_FAMILIES.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/EXPORT_VS_APPLY.md`

Later prompts should implement:

- explicit export or install-oriented adapters that do not overclaim display-manager ownership

