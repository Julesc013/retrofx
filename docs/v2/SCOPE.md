# RetroFX 2.x Scope

This file defines what RetroFX 2.x aims to support, and at what level of ambition.
It is a target-direction document, not a promise that every item ships in the first implementation phase.

## Support Tiers

### First-Class Targets

First-class targets are direct design targets for 2.x.
They should have explicit capability models, active documentation, and dedicated testing once implemented.

- TTY appearance outputs, including palette and console-oriented typography policy where the host permits it.
- `tuigreet` and related greetd-adjacent terminal login presentation.
- Terminal compilers for `Alacritty`, `Kitty`, and `Xresources` consumers.
- TUI style exports for tools such as `tmux`, `vim` or `neovim`, and `btop`.
- Session-local `fontconfig` policy for terminal, TUI, WM, and compositor-adjacent sessions.
- X11 session orchestration with a first-class `i3`-centered render-capable path.
- X11 render-capable targets where the backend explicitly supports them.
- `sway` as a first-class Wayland-era orchestration target for theme and session policy, without pretending to offer universal compositor effects.
- Export and install workflows as first-class lifecycle modes.

### Secondary Targets

Secondary targets are explicitly in-scope, but with less orchestration depth or narrower testing expectations than first-class targets.

- Other X11 WMs such as `awesome`, `bspwm`, `openbox`, or `xmonad`.
- `waybar`, `rofi`, and `wofi`.
- GTK and Qt theme exports.
- Cursor and icon theme hints.
- Wayland terminal-only workflows outside `sway`.
- Additional toolkit- or app-specific theme compilers that can be implemented without distorting the core model.

### Stretch Or Future Targets

Stretch targets are plausible future expansion areas, but are not baseline promises for early 2.x.

- GNOME and KDE Plasma deep orchestration.
- DE-wide policy integration.
- Richer accessibility and display policy integration.
- Broader login-manager and display-manager orchestration beyond scoped fragment generation.
- More ambitious preview and inspection tooling across target families.

## Scope Standard

In 2.x, "in scope" does not mean "all features on all targets."
Each target is expected to land with an honest capability envelope:

- some targets are theme-heavy and render-light
- some targets are export-only by nature
- some targets may support session orchestration without supporting render transforms

That is acceptable if the capability contract is explicit.

## Deliberate Focus For Early 2.x

The early 2.x focus is the intersection of practical value and truthful support:

- profile semantics that travel across targets
- terminal and TUI compilers that are deterministic
- X11 render-capable integration where it is actually supportable
- session-local typography and environment policy
- Wayland-aware theming and session paths without fake compositor claims

