# RetroFX 2.x Public Beta Risk Surface

This document inventories the externally visible or externally confusable 2.x surfaces on the current limited technical-beta line.

It is evidence-driven.
It does not imply general-public beta readiness.

## Inventory

| Surface | Current classification | Current truth | Current position |
| --- | --- | --- | --- |
| unified `scripts/dev/retrofx-v2` entrypoint | safe only for internal or non-public use | coherent and deterministic, but still a broader repo-oriented developer surface | kept internal-only and clearly separate from the technical-beta wrapper |
| `scripts/dev/retrofx-v2-techbeta` entrypoint | safe for external advanced testers | exposes only the narrowed technical-beta command family and documents the bounded support matrix | approved candidate surface |
| `status` and machine-readable release metadata | safe for external advanced testers when reached through `retrofx-v2-techbeta` | current and candidate release state, support matrix, and limitations are explicit | candidate-ready |
| `package-alpha` | safe only for internal or non-public use | reproducible and bounded, but intentionally tied to the internal-alpha line | kept internal-only |
| `package-technical-beta` | safe for operator use only | produces a copied-toolchain candidate package with local wrappers and docs | approved local candidate builder |
| `install` / `uninstall` via `retrofx-v2-techbeta` | safe for external advanced testers | deterministic, user-local, and bounded to `retrofx-v2-dev` roots | approved candidate surface |
| `apply` / `off` via `retrofx-v2-techbeta` | safe for external advanced testers on X11 only | bounded, reversible, and managed-root-only; live apply is not promised outside X11 | approved with explicit X11-only gate |
| `preview-x11` | safe only for internal or non-public use | one strong real X11 plus `i3` validation path exists, but the explicit live probe remains too narrow for outside support | fenced off from the technical-beta surface |
| migration tooling | safe only for internal or non-public use | deterministic and honest, but still representative rather than broad | fenced off from the technical-beta surface |
| toolkit/theme export outputs | safe for external advanced testers with caveats | deterministic and advisory; they do not imply live desktop ownership | approved as export-oriented artifacts only |
| diagnostics capture | safe for external advanced testers through the candidate package | local-file-only, non-invasive, and sufficient for bug reports when used with the copied toolchain | approved candidate surface |
| local tag and package naming | safe for external advanced testers with caveats | candidate naming is explicit and still non-public; no automation publishes it | approved local-only candidate identity |
| README and readiness docs | safe for external advanced testers | now distinguish the internal dev surface from the limited technical-beta wrapper and support matrix clearly | candidate-ready |

## Summary

The current 2.x branch now has two distinct surfaces:

- the broader `retrofx-v2` developer surface, which remains internal-only
- the narrower `retrofx-v2-techbeta` copied-toolchain surface, which is suitable for advanced external testers

The limited public technical beta is intentionally narrow.

It is suitable only when all of the following are true:

- the tester is technically literate and comfortable with JSON output, temp-HOME runs, and explicit cleanup
- the tester uses the copied-toolchain package rather than assuming a repo checkout
- bounded live checks stay inside the documented X11-oriented support matrix
- Wayland live ownership, broad migration assurance, and the explicit X11 probe remain outside the support promise
