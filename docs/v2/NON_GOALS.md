# RetroFX 2.x Non-Goals

This file exists to reduce scope creep.
If a proposed feature fits one of these categories, it should not quietly enter 2.x under a different label.

## RetroFX 2.x Is Not

- not a compositor
- not a desktop environment
- not a replacement window manager
- not a universal Linux theming authority
- not a promise of identical effects on every environment
- not a promise of universal Wayland post-processing
- not a giant distro-specific hacks collection
- not a replacement for every native theming system
- not an excuse to mutate arbitrary global config by default
- not an opaque automatic rice machine
- not a generic dotfile sync engine
- not a plugin marketplace for arbitrary executable behavior

## Specific Boundary Calls

- RetroFX may emit GTK or Qt outputs, but it does not become the owner of every toolkit decision on the machine.
- RetroFX may orchestrate sessions, but it does not claim lifecycle ownership over environments it cannot repair or disable cleanly.
- RetroFX may express icon and cursor preferences, but it does not promise universal cross-DE enforcement.
- RetroFX may offer render transforms, but only where a target can host them honestly.
- RetroFX may ship packs and style families, but packs are curated data, not hidden imperative scripts.

## Rejected Failure Modes

2.x should reject these patterns even if they appear convenient:

- silently broadening support claims because an export file can be generated
- introducing backend-specific profile knobs into the core without a cross-target reason
- accumulating WM and DE special cases until the architecture becomes a compatibility junk drawer
- treating partial support as full support in docs or UI
- shipping integration paths that cannot be disabled or repaired predictably

