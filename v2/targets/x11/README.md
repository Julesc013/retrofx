# v2/targets/x11

Purpose:

- future home of render-capable X11 target adapters

What belongs here:

- picom config adapters
- shader source adapters
- X11 render-adjacent emitted artifacts

What does not belong here:

- global environment detection
- session wrapper ownership
- toolkit-wide theming

Governing docs:

- `docs/v2/X11_TARGETS.md`
- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/TARGET_CAPABILITY_DECLARATIONS.md`

Later prompts should implement:

- truthful X11 adapters that consume resolved render policy and respect planner-owned compositor requirements

