# RetroFX 1.x Capability Matrix

`Supported`, `Degraded`, `Export-only`, and `Unsupported` are used literally in this file.

| Target / Environment | Status | Notes |
| --- | --- | --- |
| Repo-local mode | Supported | Primary workflow from a cloned repository. |
| User-local install mode | Supported | `install`, `uninstall`, and `status` validate install assets separately from runtime state. |
| X11 + picom + GLX | Supported | Full shader/runtime path. RetroFX wrappers target this path explicitly. |
| X11 with manual integration on other WMs/DEs | Degraded | Core apply/export logic works, but wrapper and Xsession guidance are focused on i3. |
| X11 without working `picom` or GLX | Degraded | Exports and non-compositor profiles still work; full shader/runtime guarantees do not. |
| Wayland sessions | Degraded | No global shader/compositor path. Palette/export/session-local outputs only. |
| Wayland global post-process shader path | Unsupported | Not available in 1.x. |
| TTY ANSI palette backend | Supported | Optional 16-color backend with rollback; real apply requires console access. |
| TTY font apply (`fonts.tty`) | Degraded | Best-effort via `setfont`; depends on host console support. |
| tuigreet snippet generation | Supported | Generates `active/tuigreet.conf` only. Global greetd edits remain manual. |
| Session-local fontconfig (`[fonts]`, `[font_aa]`) | Supported | Generates `active/fontconfig.conf`; opt in with env hooks instead of global config edits. |
| Xresources / Alacritty export | Supported | Deterministic generated files from the resolved profile palette. |
| Base16 import/export | Supported | Deterministic, lossy ANSI16 semantic bridge. |
| Pack install into user space | Supported | Copies pack-local assets into `profiles/user_assets/` and rewrites profile paths. |
| Broad GTK/Qt/icon/cursor/DE orchestration | Unsupported | Non-goal for 1.x. |
| Automatic greetd or system display-manager config edits | Unsupported | Manual integration only. |
