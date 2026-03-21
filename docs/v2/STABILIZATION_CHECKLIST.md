# RetroFX 2.x Stabilization Checklist

This checklist defines what the branch needs before it can move from broad experimental build-out into a controlled alpha-style validation phase.

It is not a release checklist.
It is a trust checklist for the experimental platform.

## Interface And Contract Readiness

- [x] The currently implemented internal interfaces are listed in [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md).
- [x] Code-side contract shapes exist in [v2/core/interfaces/contracts.py](/mnt/btrfs-data/projects/retrofx/v2/core/interfaces/contracts.py).
- [x] Contract-level tests cover resolved profiles, target compile results, session planning, apply or off state, packs, migration, and install records.
- [ ] No high-churn shape changes are happening without matching docs and tests.

## Developer Surface Readiness

- [x] `scripts/dev/retrofx-v2` is the unified experimental entrypoint.
- [x] The unified surface exposes only implemented commands.
- [x] `status` reports implemented targets, current activation, environment, and limitations.
- [x] The branch has a documented smoke path in [DEV_WORKFLOW.md](DEV_WORKFLOW.md).
- [ ] Help output across delegated subcommands is polished enough that developers do not need to guess which surface to use.

## Documentation Truth

- [x] [README.md](README.md) is the 2.x doc index.
- [x] [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md) is current and blunt.
- [x] [IMPLEMENTED_INTERFACES.md](IMPLEMENTED_INTERFACES.md) matches the current code-side contract layer.
- [x] Major lifecycle, packs, migration, install, and target docs have had a truth pass after the implementation build-out.
- [ ] Remaining architecture docs are fully free of future-tense language that reads like present implementation.

## Runtime And Artifact Trust

- [x] Implemented target outputs are deterministic.
- [x] Bundled and installed artifacts remain under a 2.x-owned user-local footprint.
- [x] Bounded apply or off writes explicit manifests and current-state records.
- [x] `off` clears only 2.x-owned active state and recorded preview roots.
- [ ] The bounded X11 live probe has enough real-world validation across supported X11 hosts to trust its current limitations.

## Ecosystem And Continuity

- [x] Local packs are discoverable and pack-aware profile resolution works.
- [x] 1.x migration inspection works for the currently supported subset.
- [x] Install, uninstall, and status metadata are explicit.
- [ ] Migration coverage and diagnostics have been exercised against a wider representative set of legacy profiles.

## Before The Next Maturity Step

The next phase should focus on:

- real-world validation under temp homes and isolated environments
- regression hunting instead of new target-family sprawl
- interface cleanup only where tests or docs expose drift
- output determinism checks across the implemented target families
- bounded runtime validation for the current X11 experimental path
- documentation cleanup where design intent still reads like implemented reality
