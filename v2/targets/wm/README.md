# v2/targets/wm

Purpose:

- home of WM and adjacent UI target adapters for the experimental 2.x scaffold

Implemented now:

- `i3`: config-fragment compiler
- `sway`: config-fragment compiler
- `waybar`: stylesheet compiler
- shared WM theme-context helpers under `common.py`

What belongs here:

- i3 adapters
- sway adapters
- future awesome adapters
- waybar, rofi, and wofi-adjacent target adapters

What does not belong here:

- compositor shader logic
- raw profile parsing
- whole-session orchestration ownership

Governing docs:

- `docs/v2/WM_TARGETS.md`
- `docs/v2/TARGET_FAMILIES.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`

Later prompts should implement:

- additional WM-facing config emitters that keep theme/config output separate from session and render ownership
- optional launcher-adjacent targets such as `rofi` or `wofi`

Current rule:

- TWO-10 WM compilers emit deterministic export-only dev artifacts under `v2/out/<profile-id>/...`
- they do not apply, reload, install, or own session lifecycle behavior
