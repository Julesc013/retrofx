# RetroFX 2.x Session Integrations

RetroFX 2.x session integrations are bounded entry-point helpers for supported login and startup contexts.

They are not a license to take over every display manager or desktop environment.

## Purpose

The session layer may use integration families to:

- connect emitted artifacts to login or startup paths
- prepare managed wrappers or launch helpers
- bind environment exports into a supported session flow

Integration families remain subordinate to:

- capability filtering
- target planning
- install ownership
- explicit session mode selection

## Integration Family Summary

| Family | What Session May Do | What Targets Provide | Outside RetroFX Scope | Likely Capability Class |
| --- | --- | --- | --- | --- |
| TTY login or session handling | apply or restore TTY palette or console-font data in scoped contexts | tty palette artifacts, console-font hints, restore data | system-wide getty policy, arbitrary console manager takeover | partial to full in scoped TTY paths |
| greetd or tuigreet integration | emit snippets, environment files, or managed helper hooks | login-theme artifacts, palette and typography snippets | editing global greetd config by default, universal DM ownership | partial or export-only unless explicitly managed |
| Xsession wrappers | create managed user-local Xsession entries or wrappers | X11 render artifacts, WM fragments, env exports | system-wide display-manager ownership | full or partial in managed X11 paths |
| i3 session startup | bind emitted i3, terminal, theme, and X11 artifacts into startup flow | i3 fragments, X11 helper artifacts, env exports | arbitrary third-party startup scripts | full or partial depending environment |
| sway session startup | bind sway-facing config and exportable theme outputs into startup flow | sway fragments, terminal or toolkit exports, env exports | global Wayland post-processing promises | partial |
| DE login or startup hooks | emit bounded user-local launch helpers or export hints | toolkit exports, icon or cursor hints, session helper snippets | deep GNOME or Plasma policy ownership | export-only or partial |
| export-only integration guidance | emit docs, examples, or unmanaged snippets for manual use | any target family's exportable artifacts | live apply, repair, or uninstall ownership | export-only |

## TTY Login Or Session Handling

Session may:

- stage TTY palette apply data
- stage restore data for later disable or repair
- apply only where TTY ownership is explicit

Targets provide:

- palette artifacts
- console-font hints or data where supported
- restore-oriented metadata if later implemented

Outside RetroFX scope:

- broad ownership of login managers
- arbitrary system console policy

## greetd Or Tuigreet Integration

Session may:

- generate snippets
- bind generated login-theme artifacts into managed helper paths
- prepare explicit startup guidance

Targets provide:

- `tuigreet` or login-facing theme artifacts
- palette and typography fragments

Outside RetroFX scope:

- editing global greetd config by default
- pretending to own every login manager

## Xsession Wrappers

Session may:

- generate managed user-local Xsession entries
- bind X11 render artifacts and WM startup fragments into those entries
- record install or integration ownership

Targets provide:

- X11 compositor and shader artifacts
- WM fragments
- exported environment snippets

Outside RetroFX scope:

- system-wide display-manager reconfiguration
- unsupported X11 runtime claims in non-X11 environments

## i3 Session Startup

Session may:

- compose i3-facing fragments with X11 render helpers
- stage environment exports needed by managed startup
- record a bounded user-local startup path

Targets provide:

- i3 config fragments
- X11 target artifacts
- terminal and theme exports as needed

Outside RetroFX scope:

- arbitrary custom startup scripts outside managed ownership

## sway Session Startup

Session may:

- compose sway config fragments with theme or export outputs
- stage startup helpers where capability is truthful

Targets provide:

- sway config fragments
- terminal or toolkit exports
- environment snippets

Outside RetroFX scope:

- universal global render transforms on Wayland
- pretending X11 compositor logic applies natively to sway

## DE Login Or Startup Hooks

This family is future-looking and intentionally conservative.

Session may:

- emit bounded user-local launch helpers
- emit export hints for toolkit, icon, cursor, or desktop-policy artifacts

Targets provide:

- toolkit exports
- icon and cursor hints
- optional session-helper snippets

Outside RetroFX scope:

- deep GNOME or Plasma control
- system-global policy mutation

## Export-Only Guidance

Some environments are best handled by explicit export guidance instead of live integration.

In those cases, the session layer may:

- emit manual-use snippets
- emit explanation files
- record that the result is export-only

It must not:

- claim repair or uninstall ownership over unmanaged manual steps

## Relation To 1.x

2.x carries forward the useful 1.x lesson that login and startup integration must stay bounded and explicit.

It improves the model by separating:

- target emission
- integration-hook ownership
- current-session apply
- install-state ownership
