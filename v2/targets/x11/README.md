# v2/targets/x11

Purpose:

- future home of render-capable X11 target adapters

Implemented now:

- `x11-shader`: deterministic GLSL shader output for the bounded TWO-17 X11 render subset
- `x11-picom`: deterministic picom config output pointing at the generated shader
- `x11-render-runtime`: runtime metadata for the dev-only X11 preview path
- `x11-display-policy`: explicit display-policy export alongside the real bounded render outputs

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

- broader palette families beyond `vga16`
- stronger runtime validation and cleanup helpers
- truthful stable X11 lifecycle ownership once session orchestration is ready
