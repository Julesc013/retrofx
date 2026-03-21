# v2/targets/toolkit

Purpose:

toolkit and desktop export target adapters, starting with session-local typography policy output

What belongs here:

- session-local `fontconfig`-style typography exports
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
- `docs/v2/TYPOGRAPHY_MODEL.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/TARGET_CAPABILITY_DECLARATIONS.md`

Implemented now:

- `fontconfig`: deterministic export-only session-local typography policy output
- `gtk-export`: deterministic GTK-facing advisory export artifact
- `qt-export`: deterministic Qt-facing advisory export artifact
- `icon-cursor`: deterministic icon and cursor policy artifact
- `desktop-style`: deterministic aggregate desktop-style export bundle

Later prompts should implement:

- truthful export-first toolkit targets that fit the same adapter contract as the rest of the platform without overstating desktop ownership
- bounded install or session-integration layers that consume these artifacts without claiming universal DE ownership
