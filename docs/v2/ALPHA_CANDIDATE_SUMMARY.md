# RetroFX 2.x Alpha Candidate Summary

This is the concise operator summary for the first local or internal 2.x alpha candidate.

## Candidate

- version: `2.0.0-alpha.internal.1`
- status label: `internal-alpha`
- local tag candidate: `v2.0.0-alpha.internal.1`
- circulation scope: local and internal only
- readiness verdict: `ALPHA_CANDIDATE_READY=yes`

## Package Shape

- default package root: `v2/releases/internal-alpha/`
- package naming pattern: `retrofx-v2--2.0.0-alpha.internal.1--<bundle-id>/`
- required entrypoint: `scripts/dev/retrofx-v2`
- install footprint: `retrofx-v2-dev`

## Major Supported Capabilities

- resolve, plan, compile, bundle, install, uninstall, apply, off, diagnostics, and smoke through the unified dev surface
- terminal, WM, toolkit-export, display-policy, and bounded X11 render compiler families
- pack-aware profile resolution plus deterministic internal-alpha packages
- bounded current-state activation with managed-root cleanup

## Major Limitations

- local or internal only, not public
- repo-checkout dependent, not a standalone copied toolchain
- Wayland render remains degraded or export-only
- toolkit outputs remain advisory
- real-host validation breadth remains narrow

## Next Human Steps

1. Confirm [ALPHA_RELEASE_CHECKLIST.md](ALPHA_RELEASE_CHECKLIST.md) passes on a clean committed tree.
2. Generate the package with `scripts/dev/retrofx-v2 package-alpha --pack modern-minimal --profile-id warm-night`.
3. Run the temp-HOME install, diagnostics, and uninstall flow.
4. If the candidate still passes, create or keep the local-only annotated tag `v2.0.0-alpha.internal.1`.
