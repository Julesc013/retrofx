# v2/render

Purpose:

- future home of render policy, quantization, palette transforms, effect planning, and display transform logic

Implemented now:

- display-policy interpretation helpers for `gamma`, `contrast`, `temperature`, `black_lift`, `blue_light_reduction`, and `tint_bias`
- environment-aware advisory classification for display-policy planning and export

Do implement here later:

- render-policy helpers
- X11-capable render planning
- palette and display transform utilities

Do not implement here:

- generic profile parsing
- WM or DE session ownership
- unrelated UI theme policy
