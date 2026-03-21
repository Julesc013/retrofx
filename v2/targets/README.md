# v2/targets

Purpose:

- future home of target adapters and backend-specific emission
- future home of the 2.x adapter layer that consumes resolved planning and produces target-specific artifacts

Do implement here later:

- compiler interfaces for concrete targets
- emitted artifact generation for terminals, TTY, TUI, WM, toolkit, and render-capable targets
- adapter validation and capability declarations
- family-specific adapters under dedicated subdirectories

Planned sub-areas:

- `interfaces/`: shared adapter-layer contracts
- `terminal/`: terminal and TUI family adapters
- `tty/`: console palette and font family adapters
- `tuigreet/`: greet/login presentation adapters
- `x11/`: render-capable X11 adapters
- `wm/`: WM and adjacent UI target adapters
- `toolkit/`: future GTK, Qt, cursor, and icon export adapters

Do not implement here:

- raw profile parsing
- semantic token invention
- live environment mutation

Governing docs:

- `docs/v2/TARGET_COMPILER_CONTRACT.md`
- `docs/v2/ADAPTER_INTERFACE.md`
- `docs/v2/TARGET_CAPABILITY_DECLARATIONS.md`
- `docs/v2/EXPORT_VS_APPLY.md`

Core rule:

- target adapters consume the resolved profile, the capability-filtered target plan, and artifact-planning context
- they do not consume raw profile TOML directly

