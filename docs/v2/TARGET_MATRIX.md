# RetroFX 2.x Target Matrix

Status class is judged against the target's intended contract, not against the most feature-rich X11 render path.
For example, a target with no meaningful runtime render layer can still be `full` if RetroFX fully supports its intended theme or session contract.

| Target | Example environments | Theme support | Render support | Session integration | Status class | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| TTY | Linux virtual console, getty login | ANSI palette, console font policy where supported | None beyond target-native palette shaping | Login and apply or off hooks within declared scope | full | First-class console target; no compositor promises. |
| `tuigreet` | `greetd` + `tuigreet` | Palette, terminal theme, typography hints | None | Fragment generation and scoped integration | full | Presentation target, not display-manager takeover. |
| Terminal compilers | `Alacritty`, `Kitty`, `Xresources` consumers | Full terminal theme outputs | None | Session-local apply or export workflows | full | Deterministic target compilers are a core 2.x value. |
| TUI compilers | `tmux`, `vim` or `neovim`, `btop` | Full app theme exports within adapter contract | None | App-scoped config generation | full | Render intent collapses into theme semantics here. |
| Session-local typography policy | `fontconfig`-aware sessions on X11 or Wayland | Fonts, AA, hinting, fallback policy | None | Environment-scoped activation | full | Must stay user-scoped and reversible. |
| X11 + i3 + picom | Xsession, wrapper-managed `i3` sessions | Full | Full where declared by adapter | Full | full | Primary early render-capable orchestration path. |
| X11 other WMs | `awesome`, `bspwm`, `openbox`, `xmonad` | Strong theme coverage | Backend-dependent, not assumed | Partial or adapter-specific | partial | Supported with explicit variance instead of one-size-fits-all promises. |
| `sway` | `sway`, wlroots-based sessions | Strong theme and session coverage | No compositor-wide render guarantee; target-local transforms only if declared | Partial to strong, depending on adapter maturity | partial | First-class Wayland-era target without fake global shader claims. |
| Wayland terminal-only paths | `foot`, `Kitty`, `Alacritty` on Wayland | Full terminal and typography outputs | None | Limited to app or session-local exports | partial | Useful daily-driver path, not a global effects path. |
| `waybar`, `rofi`, `wofi` | wlroots and mixed sessions | Adapter-specific theme outputs | None | Limited and adapter-specific | partial | Secondary targets with useful but narrower orchestration depth. |
| GTK or Qt exports | GTK apps, Qt apps, toolkit config files | Exported theme data and hints | None | Manual or adapter-scoped only | export-only | Export is valid; full DE control is not implied. |
| GNOME Wayland | GNOME Shell sessions | Terminal, toolkit, icon, cursor, and font-related exports where possible | Unsupported for global post-processing | No truthful session ownership in baseline 2.x | export-only | No promise of shell-wide orchestration. |
| Plasma Wayland | KDE Plasma Wayland sessions | Terminal, toolkit, icon, cursor, and font-related exports where possible | Unsupported for global post-processing | No truthful session ownership in baseline 2.x | export-only | Treat as export surface until explicit capability paths exist. |
| Universal Wayland global render path | GNOME Shell, KWin, wlroots compositor-wide post-processing without target-specific adapters | None | No truthful baseline capability path | None | unsupported | Explicit non-goal until a concrete backend can declare and sustain support. |
| Install mode | User-local install workflows | Depends on selected targets | Depends on selected targets | Full lifecycle ownership of installed RetroFX-managed assets | full | Install mode is first-class, but only for declared files and paths. |
| Export-only workflows | CI, dotfile generation, offline artifact emission | Full artifact emission within adapter contract | Offline render-related outputs only where meaningful | None | export-only | Export-only is explicit, logged, and not misrepresented as apply support. |
