# RetroFX 2.x Terminology

RetroFX 2.x should use these terms consistently.
If future prompts introduce new language that conflicts with this file, this file wins until updated explicitly.

| Term | Meaning |
| --- | --- |
| `profile` | The user-authored or pack-provided declarative description of desired appearance and session intent. |
| `resolved profile` | The canonical normalized model after validation, defaults, token resolution, and pack composition are complete. All target compilation starts from this form. |
| `token` | A semantic reference used inside a profile or pack, such as a named palette role, typography role, spacing or effect preset, or style family value. |
| `intent` | What the profile asks RetroFX to achieve across theme, render, typography, session, export, or install domains. |
| `target` | A user-visible output domain such as `tty`, `tuigreet`, `alacritty`, `kitty`, `xresources`, `tmux`, `sway`, or an X11 render-capable session. |
| `backend` | The runtime substrate or environment that constrains a target, such as `X11 + i3 + picom`, `sway`, or a Linux virtual console. |
| `adapter` | The concrete compiler and emitter that maps the resolved profile into artifacts for a target-backend combination. |
| `compiler` | A deterministic transformation stage that turns the resolved profile plus capability plan into target-specific artifacts. |
| `render transform` | A visual transformation beyond static theming, such as quantization, dithering, scanlines, glow, gamma, temperature, or bias. |
| `theme output` | A generated config file or asset that expresses colors, fonts, icons, cursors, or style settings without requiring a runtime render host. |
| `session orchestration` | RetroFX-managed apply, export, install, off, repair, environment scoping, and startup integration behavior. |
| `artifact` | A concrete emitted file, generated asset, metadata record, or managed state entry produced by a compiler or session stage. |
| `artifact plan` | The planned set of artifacts and lifecycle actions derived from capability intersection before emission occurs. |
| `pack` | A curated collection of profiles, style families, palettes, typography recommendations, and metadata. |
| `style family` | A reusable design language or curated appearance lineage that multiple profiles or packs may share. |
| `capability` | A declared feature claim for a target or backend within a named domain such as theme, render, session, typography, export, install, or recovery. |
| `supported` | Intentionally part of the 2.x product with a declared capability path. |
| `degraded` | A truthful result where requested intent is reduced because the selected target or backend cannot satisfy all requested capabilities. |
| `export-only` | A support depth where RetroFX can emit artifacts but does not claim managed apply or session ownership for that target. |
| `strict-authentic` | A profile stance that prioritizes historical or stylistic authenticity, even when that reduces convenience, gamut, typography comfort, or target coverage. |
| `practical-daily-driver` | A profile stance that preserves a style family while favoring readability, app compatibility, and broader target usefulness. |

## Usage Notes

- `target` and `backend` are not interchangeable. A terminal target may run on multiple backends.
- `adapter` is narrower than `target`. Multiple adapters may serve one target across different environments.
- `degraded` is not a synonym for `unsupported`.
- `export-only` is a first-class truth label, not a polite way to hide missing apply support.

