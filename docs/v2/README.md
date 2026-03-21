# RetroFX 2.x Design Docs

This directory defines the RetroFX 2.x product and architecture before implementation begins.
It is the design constitution for future `2.x` work, not a description of current `1.x` behavior.

## Read Order

1. [PRODUCT.md](PRODUCT.md) for the product definition.
2. [NON_GOALS.md](NON_GOALS.md) and [SCOPE.md](SCOPE.md) for boundaries.
3. [PROFILE_SCHEMA.md](PROFILE_SCHEMA.md), [TOKEN_CATALOG.md](TOKEN_CATALOG.md), and [VALIDATION_RULES.md](VALIDATION_RULES.md) for the 2.x profile language.
4. [RESOLVED_MODEL.md](RESOLVED_MODEL.md) for the compiler-facing model.
5. [CAPABILITY_MODEL.md](CAPABILITY_MODEL.md) and [TARGET_MATRIX.md](TARGET_MATRIX.md) for support truth.
6. [EXAMPLES.md](EXAMPLES.md) and [MIGRATION.md](MIGRATION.md) for authoring and continuity.
7. [TERMINOLOGY.md](TERMINOLOGY.md) for precise language.
8. [ARCHITECTURE.md](ARCHITECTURE.md) and [PRINCIPLES.md](PRINCIPLES.md) for implementation guardrails.
9. [THEME_SYSTEM.md](THEME_SYSTEM.md), [THEME_TOKENS.md](THEME_TOKENS.md), [TYPOGRAPHY_MODEL.md](TYPOGRAPHY_MODEL.md), [ICON_CURSOR_MODEL.md](ICON_CURSOR_MODEL.md), [STYLE_FAMILIES.md](STYLE_FAMILIES.md), [THEME_COMPILATION.md](THEME_COMPILATION.md), and [RENDER_VS_THEME.md](RENDER_VS_THEME.md) for the theme subsystem.
10. [CORE_PIPELINE.md](CORE_PIPELINE.md), [NORMALIZATION_RULES.md](NORMALIZATION_RULES.md), [CAPABILITY_FILTERING.md](CAPABILITY_FILTERING.md), [ARTIFACT_PLANNING.md](ARTIFACT_PLANNING.md), and [COMPILATION_FLOW.md](COMPILATION_FLOW.md) for the core engine design.
11. [TARGET_COMPILER_CONTRACT.md](TARGET_COMPILER_CONTRACT.md), [ADAPTER_INTERFACE.md](ADAPTER_INTERFACE.md), [TARGET_CAPABILITY_DECLARATIONS.md](TARGET_CAPABILITY_DECLARATIONS.md), and [EXPORT_VS_APPLY.md](EXPORT_VS_APPLY.md) for the target layer contract.
12. [TARGET_FAMILIES.md](TARGET_FAMILIES.md), [TERMINAL_TUI_TARGETS.md](TERMINAL_TUI_TARGETS.md), [X11_TARGETS.md](X11_TARGETS.md), [WM_TARGETS.md](WM_TARGETS.md), and [FUTURE_TOOLKIT_TARGETS.md](FUTURE_TOOLKIT_TARGETS.md) for target-family design.
13. [SESSION_SYSTEM.md](SESSION_SYSTEM.md), [APPLY_MODES.md](APPLY_MODES.md), [ENVIRONMENT_MODEL.md](ENVIRONMENT_MODEL.md), [INSTALL_MODEL.md](INSTALL_MODEL.md), [STATE_AND_RECOVERY.md](STATE_AND_RECOVERY.md), [SESSION_INTEGRATIONS.md](SESSION_INTEGRATIONS.md), and [SIDE_EFFECT_POLICY.md](SIDE_EFFECT_POLICY.md) for lifecycle, orchestration, and recovery behavior.
14. [REPO_LAYOUT.md](REPO_LAYOUT.md), [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md), [COMPATIBILITY_SHELL.md](COMPATIBILITY_SHELL.md), and [IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md) for repository structure and execution discipline.
15. [ROADMAP.md](ROADMAP.md) for phased delivery.
16. [RELATION_TO_1X.md](RELATION_TO_1X.md) for branch and migration discipline.

## Intent

RetroFX 2.x is defined here as a profile-driven appearance compiler and session orchestration platform.
It is broader than RetroFX 1.x, but it is still bounded by explicit capability declarations, support classes, and non-goals.

## Current Implementation State

As of TWO-12:

- `v2/core/` contains an experimental dev-only scaffold for loading, validating, normalizing, and resolving 2.x profiles
- `v2/tests/` contains isolated 2.x fixtures and tests for that scaffold
- `v2/targets/terminal/` contains the first real 2.x compiler family: `xresources`, `alacritty`, `kitty`, `tmux`, and `vim`
- `v2/targets/wm/` now contains the second real 2.x compiler family: `i3`, `sway`, and `waybar`
- `v2/targets/toolkit/` now contains the first real typography-policy export target: `fontconfig`
- `v2/core/dev/compile-targets <profile>` compiles those implemented targets into `v2/out/<profile-id>/...`
- `v2/session/` now contains real environment detection and capability-aware session planning preview code
- `v2/core/dev/plan-session <profile>` detects the environment, builds a preview plan, and can write a non-destructive preview bundle under `v2/out/<profile-id>/plan/`
- resolved typography defaults, stacks, and session-local font-policy artifacts now exist, but global font orchestration does not
- live apply, install, off, artifact planning, and full session orchestration are still future work
- the working product line remains 1.x; no default CLI migration has happened
