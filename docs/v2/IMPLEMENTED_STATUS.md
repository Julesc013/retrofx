# RetroFX 2.x Implemented Status

This document is the current truth pass for the 2.x branch as of TWO-21.
It is intentionally blunt.

1.x remains the production line.
2.x remains experimental and developer-facing.

## Matrix

| Area | Implemented | Experimental | Planned | Notes |
| --- | --- | --- | --- | --- |
| schema validation | yes | yes | no | Raw and normalized validation are real in `v2/core/validation/`. |
| normalization | yes | yes | no | Defaults, canonicalization, and semantic derivation are real in `v2/core/normalization/`. |
| resolved profile | yes | yes | no | Resolved theme, typography, render, display, pack, and session policy are real in `v2/core/resolution/`. |
| terminal targets | yes | yes | no | `xresources`, `alacritty`, `kitty`, `tmux`, and `vim` compile deterministically. |
| WM targets | yes | yes | no | `i3`, `sway`, and `waybar` export config or style artifacts. |
| toolkit exports | yes | yes | no | `gtk-export`, `qt-export`, `icon-cursor`, `desktop-style`, and `fontconfig` are export-oriented and advisory. |
| typography outputs | yes | yes | no | Role-based typography is resolved and emitted where supported. |
| display policy outputs | yes | yes | no | Display policy is concrete, planned, exportable, and consumed by the bounded X11 render slice. |
| pack system | yes | yes | no | Local pack manifests and curated built-in packs are real. Remote/community distribution is not. |
| migration tooling | yes | yes | no | 1.x profile inspection and draft migration are real. Runtime compatibility is not. |
| install or bundle flow | yes | yes | no | Repo-local bundles and isolated user-local experimental installs are real. |
| X11 render or compiler | yes | yes | no | Shader, picom, runtime metadata, and explicit bounded preview exist for X11 only. |
| session planning | yes | yes | no | Environment detection and capability-aware planning are real and non-destructive. |
| bounded apply or off | yes | yes | no | TWO-19 current activation, manifests, last-good, and `off` are real but intentionally narrow. |
| global desktop integration | no | no | yes | Live GNOME, Plasma, Xfce, and cross-DE mutation are not implemented. |
| live Wayland render | no | no | yes | Wayland render remains degraded or export-only. |
| full compatibility mode | no | no | yes | Migration exists, but 1.x runtime compatibility does not. |

## Developer Reality

Implemented and coherent now:

- `scripts/dev/retrofx-v2 status`
- `scripts/dev/retrofx-v2 resolve`
- `scripts/dev/retrofx-v2 plan`
- `scripts/dev/retrofx-v2 compile`
- `scripts/dev/retrofx-v2 packs list` and `packs show`
- `scripts/dev/retrofx-v2 migrate inspect-1x`
- `scripts/dev/retrofx-v2 bundle`, `install`, and `uninstall`
- `scripts/dev/retrofx-v2 apply`, `off`, and `preview-x11`
- `scripts/dev/retrofx-v2 smoke`

Still intentionally bounded:

- live apply only exists as a narrow 2.x-owned activation path plus the explicit short-lived X11 probe
- toolkit outputs are advisory exports, not live DE ownership
- install and current activation remain separated

Not implemented:

- production CLI takeover
- release-quality stability guarantees
- global desktop ownership
- live Wayland render
- full 1.x runtime replacement or compatibility mode

Related truth docs:

- [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md) for the currently enforced code-side boundaries
- [STABILIZATION_CHECKLIST.md](STABILIZATION_CHECKLIST.md) for the next trust gates
