# v2/targets/terminal

Purpose:

- future home of terminal and TUI family target adapters

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

