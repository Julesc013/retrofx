# tty backend

Phase 2 functional backend.

Responsibilities:

- consume `active/tty-palette.env` semantic ANSI16 palette
- apply palette to Linux console when safe (or mock mode)
- keep rollback snapshots under `state/tty-backups/`
- restore prior palette via `off` command
