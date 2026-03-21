# v2/theme

Purpose:

- future home of semantic theme resolution, typography policy, and target-agnostic theme mapping helpers
- future home of non-render appearance policy

Do implement here later:

- semantic color derivation helpers
- typography, icon, and cursor policy helpers
- theme-side mapping utilities used by planning or targets
- style-family defaults and token-set compilation

Planned sub-areas:

- `tokens/`: logical theme token definitions and helpers
- `typography/`: typography roles and AA policy helpers
- `icons/`: icon-theme policy helpers
- `cursors/`: cursor policy helpers
- `families/`: style-family defaults and preset logic
- `compilation/`: theme-token-set preparation for target adapters

Do not implement here:

- shader generation
- session orchestration
- direct backend file emission outside target interfaces
- compositor effect algorithms

Governing docs:

- `docs/v2/THEME_SYSTEM.md`
- `docs/v2/THEME_TOKENS.md`
- `docs/v2/TYPOGRAPHY_MODEL.md`
- `docs/v2/ICON_CURSOR_MODEL.md`
- `docs/v2/STYLE_FAMILIES.md`
- `docs/v2/THEME_COMPILATION.md`
- `docs/v2/RENDER_VS_THEME.md`

Core rule:

- theme consumes the resolved profile and produces semantic appearance inputs for target adapters
- theme does not implement render algorithms or raw target emission
