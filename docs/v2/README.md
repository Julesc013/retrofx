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
9. [REPO_LAYOUT.md](REPO_LAYOUT.md), [MODULE_BOUNDARIES.md](MODULE_BOUNDARIES.md), [COMPATIBILITY_SHELL.md](COMPATIBILITY_SHELL.md), and [IMPLEMENTATION_SEQUENCE.md](IMPLEMENTATION_SEQUENCE.md) for repository structure and execution discipline.
10. [ROADMAP.md](ROADMAP.md) for phased delivery.
11. [RELATION_TO_1X.md](RELATION_TO_1X.md) for branch and migration discipline.

## Intent

RetroFX 2.x is defined here as a profile-driven appearance compiler and session orchestration platform.
It is broader than RetroFX 1.x, but it is still bounded by explicit capability declarations, support classes, and non-goals.

