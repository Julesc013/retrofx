# RetroFX 2.x Implemented Interfaces

This document lists the current implemented interface contracts for the experimental 2.x branch.
It is intentionally narrower than the full architecture docs.

1.x remains the production line.
2.x remains experimental and developer-facing.

The code-side companion to this document is [v2/core/interfaces/contracts.py](/mnt/btrfs-data/projects/retrofx/v2/core/interfaces/contracts.py).

## Current Contract Set

| Interface | Producer | Consumer | Shape | Stability | Out Of Scope |
| --- | --- | --- | --- | --- | --- |
| resolved profile | `v2.core.resolution.build_resolved_profile` | target compilers, planning, bundle, apply | top-level resolved profile object with `identity`, `semantics`, `target_requests`, `capability_context`, `target_plan`, `artifact_plan`, and `decisions` | experimental internal | final capability-filtered resolved model, public API promises |
| target compile result | `v2.targets.interfaces.TargetCompileResult` | compile, bundle, apply, tests | deterministic target result with `artifacts`, `warnings`, `notes`, and consumed or ignored sections | experimental internal | raw-profile compilation, live apply ownership |
| session plan | `v2.session.planning.build_session_plan` | plan, bundle, apply, preview, status | explicit preview plan with compile/export/degraded/skipped categories plus `display_policy`, `x11_render`, and `toolkit_style` summaries | experimental internal | production session lifecycle guarantees |
| current activation state | `v2.session.apply.apply_dev_profile` | `off`, `status`, later repair work | `current-state.json` with active profile, bundle, activation, manifest, cleanup, and layout data | experimental internal | 1.x state takeover, cross-session ownership |
| activation manifest | `v2.session.apply.apply_dev_profile` | `off`, `status`, last-good, later repair work | machine-readable manifest for one bounded activation | experimental internal | universal runtime state recovery |
| pack manifest | `v2.packs.load_pack_manifest` | pack inspection and pack-aware profile selection | `retrofx.pack/v2alpha1` manifest with pack metadata, profiles, assets, and recommendations | experimental internal | remote registries, install workflows, inheritance engines |
| migration report | `v2.compat.inspect_legacy_profile` | migration inspection and draft generation | report with clean, degraded, manual, and unsupported buckets plus draft profile output | experimental internal | full 1.x runtime compatibility |
| install record | `v2.session.install.install_dev_bundle` | install status, uninstall, apply reuse | user-local install record with owned paths and bundle metadata | experimental internal | root or public packaging semantics |

## Practical Meaning

These are the interfaces that TWO-21 now treats as real enough to test structurally.

That means:

- changes to these shapes should update both code and tests together
- changes should also update [IMPLEMENTED_STATUS.md](IMPLEMENTED_STATUS.md) and this document
- new feature work should prefer extending these contracts cleanly rather than creating ad hoc side channels

Current TWO-23 hardening notes:

- `cleanup.data_paths` in activation state or manifests are only honored when they resolve inside the managed 2.x roots
- install records are not trusted to remove bundle directories outside the managed 2.x bundle store
- live-probed X11 targets are now kept separate from staged-only `export_only_targets` in the activation manifest

## Not A Public API Promise

These contracts are not a promise that RetroFX 2.x is stable or production-ready.
They are the current internal or dev-facing boundaries that make the branch inspectable and testable enough for the stabilization phase.
