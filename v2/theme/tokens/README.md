# v2/theme/tokens

Purpose:

- future home of logical theme token definitions and theme-token-set helpers

What belongs here:

- semantic theme token catalogs
- theme-side fallback logic
- token grouping for colors, chrome, terminal, and TTY appearance

What does not belong here:

- render algorithms
- backend-specific file rendering
- raw profile parsing

Governing docs:

- `docs/v2/THEME_TOKENS.md`
- `docs/v2/THEME_SYSTEM.md`

Later prompts should implement:

- stable theme token structures that target adapters can consume without re-deriving semantics

