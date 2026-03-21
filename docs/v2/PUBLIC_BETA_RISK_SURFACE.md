# RetroFX 2.x Public Beta Risk Surface

This document inventories the externally visible or externally confusable 2.x surfaces after TWO-31.

It is evidence-driven.
It does not imply that public technical beta is approved.

## Inventory

| Surface | Current classification | Current truth | TWO-31 action |
| --- | --- | --- | --- |
| unified `scripts/dev/retrofx-v2` entrypoint | safe only for internal/non-public use | coherent and deterministic, but still a repo-oriented developer surface | help text now says it is not yet approved for a limited public technical beta |
| `status` and machine-readable release metadata | safe only for internal/non-public use | truthful and contract-backed, but still describes an internal-alpha hardening line | release metadata now includes `ready_for_limited_public_technical_beta=false` and explicit public-beta blockers |
| `package-alpha` | safe only for internal/non-public use | reproducible and bounded, but intentionally internal-alpha only and repo-checkout dependent | package override foot-guns are now fenced; public-looking status or version overrides are rejected |
| `install` / `uninstall` | safe only for internal/non-public use | deterministic and user-local, but still part of the internal-alpha tooling contract | kept internal-only and explicitly bounded to `retrofx-v2-dev` roots |
| `apply` / `off` | safe only for internal/non-public use | deterministic inside managed roots, but still a narrow developer workflow rather than an outsider-safe runtime surface | help and status continue to frame this as bounded and internal-only |
| `preview-x11` | misleading or too fragile without fencing | one strong real X11 plus `i3` validation path exists, but live trust breadth is still narrow | remains explicitly internal-only and not pre-beta ready |
| migration tooling | misleading or too fragile without fencing | deterministic and honest, but based on a representative rather than broad corpus | help and docs now describe it as representative rather than broad assurance |
| toolkit/theme export outputs | docs-only or not yet exposed enough for broader claims | deterministic, but advisory only and not live DE ownership | kept clearly labeled as advisory exports |
| diagnostics capture | safe only for internal/non-public use | useful and non-invasive, but tuned for repo-based internal triage rather than outside support | remains internal-only; docs are preparatory for future external use |
| local tag and package naming | misleading / needs fencing | reserved pre-beta identity exists and could be confused with approval | release metadata and docs now keep that identity blocked and explicit |
| README and readiness docs | safe only for internal/non-public use | now truthful, but still describe an internal line rather than an outside-tester line | TWO-31 adds explicit public-beta gate docs instead of implying readiness |

## Summary

The current 2.x surface is strongest as an internal, technically literate developer or tester platform.

It is not yet safe to describe as a limited public technical beta because:

- validation breadth is still too narrow across real hosts
- the package and diagnostics surfaces still assume a repo checkout and internal operator literacy
- the X11 probe and migration tooling still need tighter evidence before outside circulation
