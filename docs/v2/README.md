# RetroFX 2.x Design Docs

This directory defines the RetroFX 2.x product and architecture before implementation begins.
It is the design constitution for future `2.x` work, not a description of current `1.x` behavior.

## Read Order

1. [PRODUCT.md](PRODUCT.md) for the product definition.
2. [NON_GOALS.md](NON_GOALS.md) and [SCOPE.md](SCOPE.md) for boundaries.
3. [PROFILE_SCHEMA.md](PROFILE_SCHEMA.md), [TOKEN_CATALOG.md](TOKEN_CATALOG.md), and [VALIDATION_RULES.md](VALIDATION_RULES.md) for the 2.x profile language.
4. [RESOLVED_MODEL.md](RESOLVED_MODEL.md) for the compiler-facing model.
5. [CAPABILITY_MODEL.md](CAPABILITY_MODEL.md) and [TARGET_MATRIX.md](TARGET_MATRIX.md) for support truth.
6. [EXAMPLES.md](EXAMPLES.md), [MIGRATION.md](MIGRATION.md), [PACKS.md](PACKS.md), and [COMPATIBILITY.md](COMPATIBILITY.md) for authoring, continuity, local pack structure, and 1.x intake reality.
7. [TERMINOLOGY.md](TERMINOLOGY.md) for precise language.
8. [ARCHITECTURE.md](ARCHITECTURE.md) and [PRINCIPLES.md](PRINCIPLES.md) for implementation guardrails.
9. [THEME_SYSTEM.md](THEME_SYSTEM.md), [THEME_TOKENS.md](THEME_TOKENS.md), [TYPOGRAPHY_MODEL.md](TYPOGRAPHY_MODEL.md), [ICON_CURSOR_MODEL.md](ICON_CURSOR_MODEL.md), [STYLE_FAMILIES.md](STYLE_FAMILIES.md), [THEME_COMPILATION.md](THEME_COMPILATION.md), and [RENDER_VS_THEME.md](RENDER_VS_THEME.md) for the theme subsystem.
10. [CORE_PIPELINE.md](CORE_PIPELINE.md), [NORMALIZATION_RULES.md](NORMALIZATION_RULES.md), [CAPABILITY_FILTERING.md](CAPABILITY_FILTERING.md), [ARTIFACT_PLANNING.md](ARTIFACT_PLANNING.md), and [COMPILATION_FLOW.md](COMPILATION_FLOW.md) for the core engine design.
11. [TARGET_COMPILER_CONTRACT.md](TARGET_COMPILER_CONTRACT.md), [ADAPTER_INTERFACE.md](ADAPTER_INTERFACE.md), [TARGET_CAPABILITY_DECLARATIONS.md](TARGET_CAPABILITY_DECLARATIONS.md), and [EXPORT_VS_APPLY.md](EXPORT_VS_APPLY.md) for the target layer contract.
12. [TARGET_FAMILIES.md](TARGET_FAMILIES.md), [TERMINAL_TUI_TARGETS.md](TERMINAL_TUI_TARGETS.md), [X11_TARGETS.md](X11_TARGETS.md), [WM_TARGETS.md](WM_TARGETS.md), and [FUTURE_TOOLKIT_TARGETS.md](FUTURE_TOOLKIT_TARGETS.md) for target-family design.
13. [SESSION_SYSTEM.md](SESSION_SYSTEM.md), [APPLY_MODES.md](APPLY_MODES.md), [ENVIRONMENT_MODEL.md](ENVIRONMENT_MODEL.md), [INSTALL_MODEL.md](INSTALL_MODEL.md), [DISTRIBUTION_MODEL.md](DISTRIBUTION_MODEL.md), [DEV_WORKFLOW.md](DEV_WORKFLOW.md), [UNINSTALL_MODEL.md](UNINSTALL_MODEL.md), [RELEASE_SHAPE.md](RELEASE_SHAPE.md), [STATE_AND_RECOVERY.md](STATE_AND_RECOVERY.md), [SESSION_INTEGRATIONS.md](SESSION_INTEGRATIONS.md), and [SIDE_EFFECT_POLICY.md](SIDE_EFFECT_POLICY.md) for lifecycle, orchestration, recovery, and experimental distribution behavior.
14. [REPO_LAYOUT.md](REPO_LAYOUT.md), [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md), [COMPATIBILITY_SHELL.md](COMPATIBILITY_SHELL.md), and [IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md) for repository structure and execution discipline.
15. [ROADMAP.md](ROADMAP.md) for phased delivery.
16. [RELATION_TO_1X.md](RELATION_TO_1X.md) for branch and migration discipline.

## Intent

RetroFX 2.x is defined here as a profile-driven appearance compiler and session orchestration platform.
It is broader than RetroFX 1.x, but it is still bounded by explicit capability declarations, support classes, and non-goals.

## Current Implementation State

As of TWO-18:

- `v2/core/` contains an experimental dev-only scaffold for loading, validating, normalizing, and resolving 2.x profiles
- `v2/tests/` contains isolated 2.x fixtures and tests for that scaffold
- `v2/targets/terminal/` contains the first real 2.x compiler family: `xresources`, `alacritty`, `kitty`, `tmux`, and `vim`
- `v2/targets/wm/` now contains the second real 2.x compiler family: `i3`, `sway`, and `waybar`
- `v2/targets/toolkit/` now contains the first real typography-policy export target: `fontconfig`
- `v2/targets/toolkit/` now also contains bounded desktop-facing export targets: `gtk-export`, `qt-export`, `icon-cursor`, and `desktop-style`
- `v2/targets/x11/` now contains a real bounded X11 render family: `x11-shader`, `x11-picom`, `x11-render-runtime`, plus `x11-display-policy`
- `v2/core/dev/compile-targets <profile>` compiles those implemented targets into `v2/out/<profile-id>/...`
- `v2/session/` now contains real environment detection and capability-aware session planning preview code
- `v2/core/dev/plan-session <profile>` detects the environment, builds a preview plan, and can write a non-destructive preview bundle under `v2/out/<profile-id>/plan/`
- `v2/session/dev/preview_x11_render.py` and `scripts/dev/retrofx-v2-preview-x11` now stage X11 render artifacts and can run an explicit short-lived `picom` probe in X11
- resolved typography defaults, stacks, and session-local font-policy artifacts now exist, but global font orchestration does not
- resolved icon/cursor and desktop-style policy now compile into advisory toolkit artifacts, but live desktop integration does not
- resolved display policy is now concrete, planned, exportable, and consumable by the bounded X11 render slice, but global display mutation does not exist
- `v2/packs/` now contains a real local pack system with `retrofx.pack/v2alpha1` manifests and curated built-in packs
- `v2/core/dev/list-packs` and `v2/core/dev/show-pack` now inspect those local packs
- `v2/core/dev/resolve-profile`, `compile-targets`, and `plan-session` can now resolve profiles from local packs via `--pack <pack-id> --profile-id <profile-id>`
- `v2/compat/` now contains the first real 1.x compatibility slice for profile inspection and draft migration output
- `v2/compat/dev/inspect-1x-profile <path>` analyzes a 1.x profile, reports clean/degraded/manual mappings, and can emit a generated 2.x draft under `v2/out/migrations/<profile-id>/`
- `v2/session/install/` now contains the first real experimental bundle/install slice for 2.x
- `scripts/dev/retrofx-v2-bundle` now builds deterministic repo-local bundles under `v2/bundles/<bundle-id>/`
- `scripts/dev/retrofx-v2-install`, `retrofx-v2-status`, and `retrofx-v2-uninstall` now manage an isolated user-local `retrofx-v2-dev` footprint
- that install flow is still dev-only, user-local, and non-destructive to 1.x
- stable live apply, session-default switching, public packaging, Wayland render, and full session orchestration are still future work
- the working product line remains 1.x; no default CLI migration has happened
