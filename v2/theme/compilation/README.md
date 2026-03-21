# v2/theme/compilation

Purpose:

- future home of theme-token-set preparation and theme-side compilation helpers

What belongs here:

- resolved-profile to theme-token-set preparation
- target-family-specific theme adapter input shaping
- token-consumption and degradation reporting helpers

What does not belong here:

- direct target file emission
- render-effect math
- live session mutation

Governing docs:

- `docs/v2/THEME_COMPILATION.md`
- `docs/v2/RENDER_VS_THEME.md`

Later prompts should implement:

- side-effect-free theme compilation helpers that feed target adapters cleanly

