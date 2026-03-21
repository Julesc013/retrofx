# v2/targets/wm

Purpose:

- future home of WM and adjacent UI target adapters

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

- WM-facing config emitters that keep theme/config output separate from session and render ownership

