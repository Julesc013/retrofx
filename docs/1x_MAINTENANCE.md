# RetroFX 1.x Maintenance

RetroFX 1.x is patch-only after `1.0.0`.

Use this file to keep the stable line boring, truthful, and maintainable.

## Acceptable 1.0.x Changes

- Verified bug fixes in supported environments.
- Safety/recovery fixes for `apply`, `off`, `self-check`, `repair`, `install`, and `uninstall`.
- Compatibility fixes for the documented X11 + picom + GLX path.
- Regression tests and doc-truth updates.
- Conservative install/wrapper fixes.
- Pack/profile fixes that restore documented 1.x behavior without broadening scope.

## Not For 1.x Patch Releases

- New rendering modes or visual effect families.
- New backends or broad WM/DE orchestration.
- Profile-schema redesign or inheritance systems.
- Generalized Wayland compositor/shader work.
- 2.0 appearance-compiler/platform work.
- Large UX or architecture rewrites that are not tied to a confirmed bug.

## Routing Rule

Classify incoming work into one of these buckets:

| Bucket | Use for | Typical examples |
| --- | --- | --- |
| `1.0.x patch candidate` | Supported-path bugs, safety issues, doc-truth corrections, install/recovery regressions | `apply`/`repair` bugs, compositor wrapper regressions, pack asset breakage, docs lying about support |
| `2.0 redesign material` | Improvements that require broader architecture or scope expansion | new theme systems, new backends, deep profile/token redesign, full DE orchestration |
| `Unsupported environment noise` | Reports outside the documented support matrix that do not expose destructive behavior or doc lies | unsupported Wayland compositor requests, broad DE theming expectations, non-core WM automation requests |

Unsupported-context reports still matter if they reveal:

- destructive behavior
- misleading docs
- a bug that also affects the supported matrix

## Patch Release Gate

For every 1.0.x patch candidate:

1. classify severity with `docs/BETA_TRIAGE.md`
2. reproduce the issue or write a clear failure statement
3. land the smallest correct fix
4. add a regression test, or record why automation is not feasible
5. update `CHANGELOG.md` if the fix is user-visible
6. update release notes if operator guidance or support truth changed
7. rerun `./scripts/test.sh`

## Stable-Line Principle

When in doubt, keep 1.x smaller, safer, and more predictable.

If a change makes RetroFX broader instead of more trustworthy, it belongs in 2.0 rather than a 1.0.x patch.
