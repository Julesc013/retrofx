# v2/theme/typography

Purpose:

- future home of typography roles, fallback chains, and AA policy helpers

What belongs here:

- role-based font policy
- terminal and UI font selection helpers
- AA, subpixel, and hinting policy helpers

What does not belong here:

- terminal config rendering
- session orchestration
- compositor or shader logic

Governing docs:

- `docs/v2/TYPOGRAPHY_MODEL.md`
- `docs/v2/THEME_COMPILATION.md`

Later prompts should implement:

- typography token preparation for target adapters and session-local font policy exports

