# v2/targets/terminal

Purpose:

- home of terminal and TUI family target adapters

Implemented now:

- real deterministic compilers for `xresources`, `alacritty`, `kitty`, `tmux`, and `vim`
- shared terminal-theme context helpers built from the resolved profile
- a registry used by the dev-only 2.x compile entrypoint

What belongs here:

- Xresources adapters
- Alacritty adapters
- Kitty adapters
- tmux, vim, and other TUI palette or theme adapters

What does not belong here:

- raw ANSI derivation from authored text
- console or TTY runtime ownership
- compositor or shader logic

Governing docs:

- `docs/v2/TERMINAL_TUI_TARGETS.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/EXPORT_VS_APPLY.md`

Later prompts should implement:

- deterministic terminal and TUI artifact emitters that consume resolved ANSI, semantic theme, and typography data

Current rule:

- the TWO-09 terminal compilers are export-oriented and dev-only
- they prove resolved-profile-driven emission without claiming session apply or install ownership yet
